"""
Yesanio v2 API — Production
============================
A clean, two-level budgeting backend with a proper migration system.

Data model:
  plans → plan_groups → plan_items
  goals (standalone, long-term)

Write semantics:
  PUT /plan/{month} fully replaces the month's plan (delete cascades).
  All writes are wrapped in a transaction with rollback on error.

Migrations:
  Schema changes are tracked in the `schema_migrations` table.
  Add new entries to MIGRATIONS to evolve the schema without losing data.
  See README "Adding a migration" for the workflow.
"""

import os
import time
from contextlib import asynccontextmanager
from decimal import Decimal
from typing import List, Optional

import pymysql
import pymysql.cursors
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


# ----------------------------------------------------------------------
# DB CONNECTION
# ----------------------------------------------------------------------
def get_conn():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "yesanio-db"),
        user=os.getenv("DB_USER", "yesanio_app"),
        password=os.getenv("DB_PASSWORD", "yesanio_app_change_me"),
        database=os.getenv("DB_NAME", "yesanio"),
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False,
        charset="utf8mb4",
    )


def wait_for_db(retries: int = 30, delay: int = 2) -> None:
    last_err: Optional[Exception] = None
    for i in range(retries):
        try:
            conn = get_conn()
            conn.close()
            print(f"[yesanio] DB ready after {i+1} attempt(s)", flush=True)
            return
        except Exception as e:
            last_err = e
            print(f"[yesanio] DB not ready (attempt {i+1}/{retries}): {e}", flush=True)
            time.sleep(delay)
    raise RuntimeError(f"Could not connect to DB: {last_err}")


# ----------------------------------------------------------------------
# MIGRATIONS
# ----------------------------------------------------------------------
# Each migration is a (version, description, list_of_sql_statements) tuple.
# Versions must be sequential integers starting from 1.
# Once a version is in production, NEVER edit its SQL — add a new migration.
#
# To add a migration:
#   1. Append a new dict here with the next version number.
#   2. Test on a backup first.
#   3. Deploy. Migrations run automatically on startup.
#   4. Check `docker compose logs yesanio-backend` for confirmation.
# ----------------------------------------------------------------------

MIGRATIONS = [
    {
        "version": 1,
        "description": "Initial schema",
        "sql": [
            """
            CREATE TABLE IF NOT EXISTS plans (
                id          INT AUTO_INCREMENT PRIMARY KEY,
                month       VARCHAR(7) NOT NULL,
                income      DECIMAL(10,2) NOT NULL DEFAULT 0,
                currency    VARCHAR(8) NOT NULL DEFAULT 'GBP',
                notes       TEXT,
                created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            ON UPDATE CURRENT_TIMESTAMP,
                UNIQUE KEY uk_plans_month (month)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """,
            """
            CREATE TABLE IF NOT EXISTS plan_groups (
                id          INT AUTO_INCREMENT PRIMARY KEY,
                plan_id     INT NOT NULL,
                name        VARCHAR(100) NOT NULL,
                kind        ENUM('FIXED','VARIABLE') NOT NULL,
                group_limit DECIMAL(10,2) NULL,
                sort_order  INT NOT NULL DEFAULT 0,
                CONSTRAINT fk_groups_plan
                    FOREIGN KEY (plan_id) REFERENCES plans(id)
                    ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """,
            """
            CREATE TABLE IF NOT EXISTS plan_items (
                id         INT AUTO_INCREMENT PRIMARY KEY,
                group_id   INT NOT NULL,
                name       VARCHAR(150) NOT NULL,
                amount     DECIMAL(10,2) NOT NULL DEFAULT 0,
                notes      TEXT,
                status     ENUM('none','pending','done') NOT NULL DEFAULT 'none',
                sort_order INT NOT NULL DEFAULT 0,
                CONSTRAINT fk_items_group
                    FOREIGN KEY (group_id) REFERENCES plan_groups(id)
                    ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """,
            """
            CREATE TABLE IF NOT EXISTS goals (
                id         INT AUTO_INCREMENT PRIMARY KEY,
                name       VARCHAR(100) NOT NULL,
                kind       VARCHAR(50),
                target     DECIMAL(10,2) NOT NULL,
                current    DECIMAL(10,2) NOT NULL DEFAULT 0,
                sort_order INT NOT NULL DEFAULT 0
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """,
        ],
    },
    {
        "version": 2,
        "description": "Add recurring flag to plan_items (default TRUE = backwards compatible)",
        "sql": [
            "ALTER TABLE plan_items ADD COLUMN recurring BOOLEAN NOT NULL DEFAULT TRUE",
        ],
    },
    {
        "version": 3,
        "description": "Add tags column to plans (comma-separated)",
        "sql": [
            "ALTER TABLE plans ADD COLUMN tags VARCHAR(500) NULL",
        ],
    },
    {
        "version": 4,
        "description": "Add is_giving flag to plan_groups",
        "sql": [
            "ALTER TABLE plan_groups ADD COLUMN is_giving BOOLEAN NOT NULL DEFAULT FALSE",
        ],
    },
    {
        "version": 5,
        "description": "Add settings table for user preferences",
        "sql": [
            """CREATE TABLE IF NOT EXISTS settings (
                setting_key VARCHAR(50) PRIMARY KEY,
                setting_value TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )""",
        ],
    },
    {
        "version": 6,
        "description": "Goal linking: is_saving flag, date windows, wipe current",
        "sql": [
            "ALTER TABLE plan_items ADD COLUMN is_saving BOOLEAN NOT NULL DEFAULT FALSE",
            "ALTER TABLE goals ADD COLUMN count_from VARCHAR(7) NULL",
            "ALTER TABLE goals ADD COLUMN count_to VARCHAR(7) NULL",
            "UPDATE goals SET current = 0",
        ],
    },
    {
        "version": 7,
        "description": "Track when a goal was first achieved",
        "sql": [
            "ALTER TABLE goals ADD COLUMN achieved_at DATE NULL",
        ],
    },
    {
        "version": 8,
        "description": "Drop unused group_limit column from plan_groups",
        "sql": [
            "ALTER TABLE plan_groups DROP COLUMN group_limit",
        ],
    },
    {
        "version": 9,
        "description": "Simplify item status (none/pending/done) to paid boolean",
        "sql": [
            "ALTER TABLE plan_items ADD COLUMN paid BOOLEAN NOT NULL DEFAULT FALSE",
            "UPDATE plan_items SET paid = TRUE WHERE status = 'done'",
            "ALTER TABLE plan_items DROP COLUMN status",
        ],
    },
]


def run_migrations() -> None:
    """
    Apply any pending migrations.

    Special case: on first run against an existing pre-migration database
    (i.e. one created by an earlier version of yesanio that didn't track
    migrations), we detect the existing `plans` table and mark v1 as
    applied without re-running its DDL. This means upgrading from
    pre-migration yesanio to migration-aware yesanio is a no-op for data.
    """
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    version     INT PRIMARY KEY,
                    description VARCHAR(255),
                    applied_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            conn.commit()

            cur.execute("SELECT version FROM schema_migrations")
            applied = {row["version"] for row in cur.fetchall()}

            # Pre-migration upgrade path: existing plans table → mark v1 done
            if 1 not in applied:
                cur.execute("SHOW TABLES LIKE 'plans'")
                if cur.fetchone():
                    print(
                        "[yesanio] Existing pre-migration schema detected — "
                        "marking v1 as applied without re-running",
                        flush=True,
                    )
                    cur.execute(
                        "INSERT INTO schema_migrations (version, description) "
                        "VALUES (%s, %s)",
                        (1, "Initial schema (pre-existing)"),
                    )
                    conn.commit()
                    applied.add(1)

            # Apply pending migrations in order
            pending = [m for m in MIGRATIONS if m["version"] not in applied]
            pending.sort(key=lambda m: m["version"])

            if not pending:
                print("[yesanio] Schema up to date "
                      f"(version {max(applied) if applied else 0})", flush=True)
                return

            for mig in pending:
                version = mig["version"]
                desc = mig["description"]
                print(f"[yesanio] Applying migration {version}: {desc}", flush=True)
                try:
                    for stmt in mig["sql"]:
                        cur.execute(stmt)
                    cur.execute(
                        "INSERT INTO schema_migrations (version, description) "
                        "VALUES (%s, %s)",
                        (version, desc),
                    )
                    conn.commit()
                    print(f"[yesanio] Migration {version} applied successfully",
                          flush=True)
                except Exception as e:
                    conn.rollback()
                    print(f"[yesanio] MIGRATION {version} FAILED: {e}", flush=True)
                    raise RuntimeError(
                        f"Migration {version} ({desc}) failed: {e}. "
                        "Database is in a partial state. Restore from backup "
                        "and investigate before retrying."
                    )
    finally:
        conn.close()


# ----------------------------------------------------------------------
# APP LIFESPAN
# ----------------------------------------------------------------------
def _auto_complete_wizard_for_existing_users():
    """If the DB already has plans or a user_name set, mark the wizard as
    completed — existing installs skip the first-run wizard on v2.5.1 upgrade."""
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT setting_value FROM settings WHERE setting_key=%s", ("wizard_completed",))
            if cur.fetchone():
                return
            cur.execute("SELECT COUNT(*) AS n FROM plans")
            has_plans = (cur.fetchone() or {}).get("n", 0) > 0
            cur.execute("SELECT setting_value FROM settings WHERE setting_key=%s", ("user_name",))
            row = cur.fetchone()
            has_name = bool(row and (row.get("setting_value") or "").strip())
            if has_plans or has_name:
                cur.execute(
                    """INSERT INTO settings (setting_key, setting_value) VALUES (%s, %s)
                       ON DUPLICATE KEY UPDATE setting_value=VALUES(setting_value)""",
                    ("wizard_completed", "true"))
                conn.commit()
    finally:
        conn.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    wait_for_db()
    run_migrations()
    _auto_complete_wizard_for_existing_users()
    yield


app = FastAPI(title="Yesanio API", version="2.6.1", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------------------------------------------------------------------
# MODELS  (with length validation matching the DB schema)
# ----------------------------------------------------------------------
class ItemIn(BaseModel):
    name: str = Field(default="", max_length=150)
    amount: Decimal = Decimal("0")
    notes: str = Field(default="", max_length=10000)
    paid: bool = False
    recurring: bool = True
    is_saving: bool = False


class GroupIn(BaseModel):
    name: str = Field(..., max_length=100)
    kind: str = Field(..., max_length=10)
    is_giving: bool = False
    items: List[ItemIn] = Field(default_factory=list)


class PlanIn(BaseModel):
    income: Decimal = Decimal("0")
    currency: str = Field(default="GBP", max_length=8)
    notes: str = Field(default="", max_length=10000)
    tags: List[str] = Field(default_factory=list)
    groups: List[GroupIn] = Field(default_factory=list)


class GoalIn(BaseModel):
    name: str = Field(..., max_length=100)
    kind: str = Field(default="", max_length=50)
    target: Decimal
    current: Decimal = Decimal("0")
    sort_order: int = 0
    count_from: Optional[str] = None
    count_to: Optional[str] = None


# ----------------------------------------------------------------------
# HELPERS
# ----------------------------------------------------------------------
def _to_float(row: dict, fields: tuple) -> dict:
    for f in fields:
        if f in row and row[f] is not None:
            row[f] = float(row[f])
    return row


def _tags_from_str(s: Optional[str]) -> List[str]:
    if not s:
        return []
    return [t.strip() for t in s.split(",") if t.strip()]


def _tags_to_str(tags: List[str]) -> Optional[str]:
    if not tags:
        return None
    # Strip commas from individual tags to keep the encoding unambiguous,
    # dedupe while preserving order, and cap to fit the column.
    seen = set()
    cleaned = []
    for t in tags:
        if not t:
            continue
        t = t.replace(",", " ").strip()
        if not t or t in seen:
            continue
        seen.add(t)
        cleaned.append(t)
    joined = ",".join(cleaned)
    return joined[:500] if joined else None


def fetch_plan(conn, month: str) -> Optional[dict]:
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM plans WHERE month=%s", (month,))
        plan = cur.fetchone()
        if not plan:
            return None

        cur.execute(
            "SELECT * FROM plan_groups WHERE plan_id=%s ORDER BY sort_order, id",
            (plan["id"],),
        )
        groups = cur.fetchall()

        for g in groups:
            cur.execute(
                "SELECT * FROM plan_items WHERE group_id=%s ORDER BY sort_order, id",
                (g["id"],),
            )
            items = cur.fetchall()
            # Normalise: amount → float, recurring → bool
            for i in items:
                _to_float(i, ("amount",))
                i["recurring"] = bool(i.get("recurring", True))
                i["is_saving"] = bool(i.get("is_saving", False))
                i["paid"] = bool(i.get("paid", False))
            g["items"] = items
            g["is_giving"] = bool(g.get("is_giving", False))

    return {
        "month": plan["month"],
        "income": float(plan["income"]),
        "currency": plan["currency"],
        "notes": plan["notes"] or "",
        "tags": _tags_from_str(plan.get("tags")),
        "updated_at": plan["updated_at"].isoformat() if plan.get("updated_at") else None,
        "groups": groups,
    }


# ----------------------------------------------------------------------
# PLANS
# ----------------------------------------------------------------------
@app.get("/months")
def list_months():
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT month FROM plans ORDER BY month DESC")
            return [r["month"] for r in cur.fetchall()]
    finally:
        conn.close()


@app.get("/plan/{month}")
def get_plan(month: str):
    if len(month) != 7 or month[4] != "-":
        raise HTTPException(status_code=422, detail="Month must be YYYY-MM")
    conn = get_conn()
    try:
        plan = fetch_plan(conn, month)
        if plan is None:
            raise HTTPException(status_code=404, detail="No plan for month")
        return plan
    finally:
        conn.close()


@app.put("/plan/{month}")
def upsert_plan(month: str, payload: PlanIn):
    """
    Full replace inside one transaction:
      - delete existing plan row (cascades to groups + items)
      - re-insert plan, groups, items
    Any failure rolls back; the previous state remains intact.
    """
    if len(month) != 7 or month[4] != "-":
        raise HTTPException(status_code=422, detail="Month must be YYYY-MM")

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM plans WHERE month=%s", (month,))
            cur.execute(
                """INSERT INTO plans (month, income, currency, notes, tags)
                   VALUES (%s, %s, %s, %s, %s)""",
                (month, payload.income, payload.currency, payload.notes,
                 _tags_to_str(payload.tags)),
            )
            plan_id = cur.lastrowid

            for g_idx, g in enumerate(payload.groups):
                if g.kind not in ("FIXED", "VARIABLE"):
                    raise HTTPException(
                        status_code=422,
                        detail=f"Group '{g.name}': kind must be FIXED or VARIABLE",
                    )
                cur.execute(
                    """INSERT INTO plan_groups
                       (plan_id, name, kind, is_giving, sort_order)
                       VALUES (%s, %s, %s, %s, %s)""",
                    (plan_id, g.name, g.kind,
                     1 if g.is_giving else 0, g_idx),
                )
                group_id = cur.lastrowid

                for i_idx, it in enumerate(g.items):
                    cur.execute(
                        """INSERT INTO plan_items
                           (group_id, name, amount, notes, paid, recurring, sort_order, is_saving)
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                        (group_id, it.name, it.amount, it.notes,
                         1 if it.paid else 0,
                         1 if it.recurring else 0, i_idx,
                         1 if it.is_saving else 0),
                    )
            # Auto-create goals for is_saving items
            _auto_create_goals(cur, payload)
        conn.commit()
        # Recompute goal progress after commit
        _recompute_goals()
        return fetch_plan(conn, month)
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


@app.delete("/plan/{month}")
def delete_plan(month: str):
    if len(month) != 7 or month[4] != "-":
        raise HTTPException(status_code=422, detail="Month must be YYYY-MM")
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM plans WHERE month=%s", (month,))
            deleted = cur.rowcount
        conn.commit()
        if deleted == 0:
            raise HTTPException(status_code=404, detail="No plan for month")
        return {"status": "deleted", "month": month}
    finally:
        conn.close()


# ----------------------------------------------------------------------
# HISTORY  (lightweight monthly summaries for charts)
# ----------------------------------------------------------------------
@app.get("/history")
def history(months: int = 12):
    """
    Return a lightweight summary of the most recent N months.
    Each entry: { month, income, fixed_total, variable_total, allocated, currency }
    Computed at query time via SQL aggregation, no per-item iteration in Python.
    """
    if months < 1:
        months = 1
    if months > 120:
        months = 120

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            # One query: aggregate items grouped by plan + group kind, then
            # roll up in Python for the response shape.
            cur.execute(
                """
                SELECT
                    p.month       AS month,
                    p.income      AS income,
                    p.currency    AS currency,
                    pg.kind       AS kind,
                    pg.is_giving  AS is_giving,
                    COALESCE(SUM(pi.amount), 0) AS subtotal
                FROM plans p
                LEFT JOIN plan_groups pg ON pg.plan_id = p.id
                LEFT JOIN plan_items pi  ON pi.group_id = pg.id
                GROUP BY p.id, p.month, p.income, p.currency, pg.kind, pg.is_giving
                ORDER BY p.month DESC
                """
            )
            rows = cur.fetchall()

        # Roll up to one entry per month
        by_month: dict = {}
        for r in rows:
            m = r["month"]
            entry = by_month.setdefault(m, {
                "month": m,
                "income": float(r["income"] or 0),
                "currency": r["currency"] or "GBP",
                "fixed_total": 0.0,
                "variable_total": 0.0,
                "giving_total": 0.0,
                "allocated": 0.0,
            })
            kind = r["kind"]
            sub = float(r["subtotal"] or 0)
            if r.get("is_giving"):
                entry["giving_total"] += sub
            if kind == "FIXED":
                entry["fixed_total"] += sub
            elif kind == "VARIABLE":
                entry["variable_total"] += sub
            entry["allocated"] = entry["fixed_total"] + entry["variable_total"]

        # Take the most recent N months, return chronologically (newest last
        # is conventional for time series). But we'll keep newest first to
        # match /months; the frontend sorts as needed.
        all_months = sorted(by_month.keys(), reverse=True)[:months]
        return [by_month[m] for m in all_months]
    finally:
        conn.close()


# ----------------------------------------------------------------------
# GOALS
# ----------------------------------------------------------------------


# ----------------------------------------------------------------------
# GOAL LINKING HELPERS
# ----------------------------------------------------------------------
def _auto_create_goals(cur, payload):
    """Create goals for any is_saving item names that don't have a matching goal."""
    saving_names = set()
    for g in payload.groups:
        for it in g.items:
            if it.is_saving and it.name.strip():
                saving_names.add(it.name.strip())
    if not saving_names:
        return
    cur.execute("SELECT name FROM goals")
    existing = {r["name"] for r in cur.fetchall()}
    for name in saving_names:
        if name not in existing:
            cur.execute(
                """INSERT INTO goals (name, kind, target, current, sort_order)
                   VALUES (%s, 'saving', 0, 0, 999)""",
                (name,),
            )


def _recompute_goals():
    """Recompute all goal.current values from is_saving+done items across plans.
    Also maintains achieved_at: set to today when current first crosses target,
    cleared when current drops back below target."""
    from datetime import date
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, target, count_from, count_to, achieved_at FROM goals")
            goals = cur.fetchall()
            for goal in goals:
                sql = """SELECT COALESCE(SUM(pi.amount), 0) AS total
                         FROM plan_items pi
                         JOIN plan_groups pg ON pg.id = pi.group_id
                         JOIN plans p ON p.id = pg.plan_id
                         WHERE pi.is_saving = TRUE AND pi.paid = TRUE
                           AND pi.name = %s"""
                params = [goal["name"]]
                if goal.get("count_from"):
                    sql += " AND p.month >= %s"
                    params.append(goal["count_from"])
                if goal.get("count_to"):
                    sql += " AND p.month <= %s"
                    params.append(goal["count_to"])
                cur.execute(sql, params)
                total = float(cur.fetchone()["total"])
                target = float(goal.get("target") or 0)
                achieved_at = goal.get("achieved_at")
                # Determine new achieved_at value
                if target > 0 and total >= target and achieved_at is None:
                    new_achieved = date.today()
                elif total < target and achieved_at is not None:
                    new_achieved = None
                else:
                    new_achieved = achieved_at  # unchanged
                cur.execute(
                    "UPDATE goals SET current = %s, achieved_at = %s WHERE id = %s",
                    (total, new_achieved, goal["id"]))
        conn.commit()
    finally:
        conn.close()


def _get_pending(conn):
    """Get pending (is_saving=True but status!='done') amounts per goal name."""
    with conn.cursor() as cur:
        cur.execute("""
            SELECT pi.name, COALESCE(SUM(pi.amount), 0) AS pending_amount,
                   COUNT(*) AS pending_count
            FROM plan_items pi
            JOIN plan_groups pg ON pg.id = pi.group_id
            JOIN plans p ON p.id = pg.plan_id
            WHERE pi.is_saving = TRUE AND pi.paid = FALSE
            GROUP BY pi.name
        """)
        return {r["name"]: {"amount": float(r["pending_amount"]),
                            "count": r["pending_count"]} for r in cur.fetchall()}



class SettingIn(BaseModel):
    value: str = Field(default="", max_length=5000)


@app.get("/settings")
def get_all_settings():
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT setting_key, setting_value FROM settings")
            rows = cur.fetchall()
            return {r["setting_key"]: r["setting_value"] for r in rows}
    finally:
        conn.close()


@app.put("/settings/{key}")
def set_setting(key: str, payload: SettingIn):
    if len(key) > 50:
        raise HTTPException(status_code=422, detail="Setting key too long")
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO settings (setting_key, setting_value) VALUES (%s, %s)
                   ON DUPLICATE KEY UPDATE setting_value=VALUES(setting_value)""",
                (key, payload.value))
        conn.commit()
        return {"key": key, "value": payload.value}
    finally:
        conn.close()


class RenameIn(BaseModel):
    old_name: str = Field(..., max_length=150)
    new_name: str = Field(..., max_length=150)


@app.post("/goals/rename")
def cross_month_rename(payload: RenameIn):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE plan_items SET name = %s WHERE name = %s AND is_saving = TRUE",
                (payload.new_name, payload.old_name),
            )
            renamed = cur.rowcount
            cur.execute(
                "UPDATE goals SET name = %s WHERE name = %s",
                (payload.new_name, payload.old_name),
            )
        conn.commit()
        _recompute_goals()
        return {"renamed_items": renamed, "old_name": payload.old_name, "new_name": payload.new_name}
    finally:
        conn.close()




class GoalReorderIn(BaseModel):
    order: List[int] = Field(default_factory=list)


@app.post("/goals/reorder")
def reorder_goals(payload: GoalReorderIn):
    """Set sort_order on goals based on the order of IDs given."""
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            for idx, goal_id in enumerate(payload.order):
                cur.execute("UPDATE goals SET sort_order = %s WHERE id = %s", (idx, goal_id))
        conn.commit()
        return {"reordered": len(payload.order)}
    finally:
        conn.close()


@app.get("/goals")
def list_goals():
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM goals ORDER BY sort_order, id")
            goals = [_to_float(g, ("target", "current")) for g in cur.fetchall()]
        pending = _get_pending(conn)
        for g in goals:
            p = pending.get(g["name"], {"amount": 0, "count": 0})
            g["pending"] = p["amount"]
            g["pending_count"] = p["count"]
            g["count_from"] = g.get("count_from")
            g["count_to"] = g.get("count_to")
            ach = g.get("achieved_at")
            g["achieved_at"] = ach.isoformat() if ach else None
        return goals
    finally:
        conn.close()


@app.post("/goals")
def create_goal(goal: GoalIn):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO goals (name, kind, target, current, sort_order, count_from, count_to)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (goal.name, goal.kind, goal.target, goal.current, goal.sort_order,
                 goal.count_from, goal.count_to),
            )
            new_id = cur.lastrowid
        conn.commit()
        return {
            "id": new_id,
            "name": goal.name,
            "kind": goal.kind,
            "target": float(goal.target),
            "current": float(goal.current),
            "sort_order": goal.sort_order,
        }
    finally:
        conn.close()


@app.put("/goals/{goal_id}")
def update_goal(goal_id: int, goal: GoalIn):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """UPDATE goals
                      SET kind=%s, target=%s, sort_order=%s, count_from=%s, count_to=%s
                    WHERE id=%s""",
                (goal.kind, goal.target, goal.sort_order,
                 goal.count_from, goal.count_to, goal_id),
            )
            if cur.rowcount == 0:
                raise HTTPException(status_code=404, detail="Goal not found")
        conn.commit()
        _recompute_goals()
        cur2 = get_conn()
        try:
            with cur2.cursor() as c:
                c.execute("SELECT * FROM goals WHERE id=%s", (goal_id,))
                row = c.fetchone()
                if row:
                    _to_float(row, ("target", "current"))
                    return row
        finally:
            cur2.close()
        return {"id": goal_id, "status": "updated"}
    finally:
        conn.close()


@app.delete("/goals/{goal_id}")
def delete_goal(goal_id: int):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM goals WHERE id=%s", (goal_id,))
            if cur.rowcount == 0:
                raise HTTPException(status_code=404, detail="Goal not found")
        conn.commit()
        return {"status": "deleted", "id": goal_id}
    finally:
        conn.close()


# ----------------------------------------------------------------------
# HEALTH  (actually checks the DB)
# ----------------------------------------------------------------------
@app.get("/health")
def health():
    try:
        conn = get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                cur.fetchone()
                cur.execute("SELECT MAX(version) AS v FROM schema_migrations")
                row = cur.fetchone()
                schema_version = row["v"] if row and row["v"] is not None else 0
        finally:
            conn.close()
        return {
            "status": "ok",
            "db": "ok",
            "schema_version": schema_version,
            "version": "2.6.1",
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"DB unreachable: {e}")


@app.get("/")
def root():
    return {"name": "Yesanio API", "version": "2.6.1", "docs": "/docs"}

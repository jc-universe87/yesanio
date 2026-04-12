# Yesanio Concepts

This document explains the non-obvious ideas at the heart of Yesanio. If you're going to use it seriously — or fork it — read this first.

## Planning, not tracking

Most budgeting tools are built around tracking: you record what you spend, they show you where the money went, and you try to do better next month. This is *retrospective* budgeting — the numbers describe the past.

Yesanio is built around *planning*: before the month begins, you decide where every pound goes. The plan is the truth. Whether reality matches the plan is a separate concern, and frankly, Yesanio doesn't care. It's not a spending tracker. It doesn't import bank transactions. It doesn't know what you actually spent on groceries this week.

This matters because the failure mode of tracking tools is shame — they make you feel bad about things you can no longer change. The failure mode of planning tools is *incomplete planning* — and the fix for that is right there in front of you: assign the pound that doesn't have a job.

## "Pay yourself first"

Savings, giving, and long-term commitments are set aside at the *start* of the month — as first-class line items in your FIXED groups — not whatever happens to be left over at the end. The "end of the month" version almost never works. You don't save because something always comes up, and the money is gone.

Yesanio encodes "pay yourself first" structurally. Every goal contribution, every tithe, every pension payment is a planned item. When you save the plan, those commitments exist. Whether you then fund daily life with whatever's left is up to you — but the important things are already on paper.

## Cash-flow models

There are two common patterns for how variable spending flows through a monthly plan, and Yesanio supports both.

### Pattern 1: Credit card, pay off the month after

Variable spending (groceries, fuel, eating out, small purchases) goes on a credit card during the month. The statement arrives and is paid off in the *next* month's plan as a single line item.

So April's plan might contain a line "Credit card payment — £1,800" in a VARIABLE group. That £1,800 is **March's** variable spending, being paid off in April. April's actual variable spending lives invisibly on the credit card and only surfaces in May's plan.

This works well if you have the discipline to clear the card in full every month and the cash flow to do so. The VARIABLE groups in any given month represent *last* month's behaviour, not this month's.

### Pattern 2: Debit card or spending account, allocate up front

Variable spending comes directly from a current account or debit card. Money is set aside in VARIABLE groups at the start of the month — "Groceries £400", "Personal allowance £200", "Fuel £150" — and the household draws against those envelopes during the month.

This is closer to classic envelope budgeting. The VARIABLE groups in any given month represent what you've allocated for *this* month. No statement lag, no credit exposure. Requires more discipline at the point of spending, less at the point of bill-paying.

### Which should you use?

Yesanio doesn't care. Both models assign every pound a job before the month begins. Both produce a zero saldo as the goal state. The FIXED + GIVING + SAVING workflow is identical in both cases — only the semantics of the VARIABLE group differ. Pick the one that matches how your household actually runs money.

## Groups and items

A **plan** is one month of your budget. Inside a plan are **groups** — categories like Housing, Giving, Groceries. Inside each group are **items** — individual line entries with a name, an amount, notes, and a status.

Groups have a `kind`: either `FIXED` (commitments — bills, subscriptions, long-term savings) or `VARIABLE` (flexible living costs). On Home, FIXED and VARIABLE are surfaced differently: FIXED groups feed the "Bills for April" sentence, VARIABLE groups are less prominent (in a credit-card-pay-off-next-month model, VARIABLE groups often represent last month's spending being paid off).

Groups can also be flagged `is_giving=true`. A giving group is pulled out of the Bills line and shown in its own "Set aside for giving" sentence on Home. Use this for tithes, donations, mission offerings — anything you want the household to see as a distinct value statement, not buried in bills.

## The Home page

The Home view is Yesanio's most important surface. It's **read-only** — anyone in the household can open it safely — and it summarises the current month's plan in plain English:

- A heading: *"April 2026"*
- A byline: *"handled by [your name] · last looked at today"*
- A hero sentence in one of four states (fresh / planned / surplus / over) with soft background colour
- Three optional sentences about bills, giving, saving
- A bottom line: *"Income £X · everything assigned a job."*

The Home page is the trust signal for your household. It should make the reader feel that someone is looking after this carefully, that the bills are handled, and that what you're saving and giving toward is visible.

## Goal linking (`is_saving`)

A plan item can be flagged as a saving contribution by clicking the 💰 toggle in the Plan view. When an item is flagged:

1. On save, Yesanio auto-creates a **goal** matching the item's name (if one doesn't exist already).
2. A recompute runs across all plans: every item flagged `is_saving=true` AND with the Paid box ticked contributes its amount to the matching goal.
3. The goal's `current` value is updated.

The link is **by name**. Rename an item in one month without renaming elsewhere, and the link breaks for that month's contribution only — the item no longer matches any goal. Yesanio warns you when you attempt this and offers a cross-month rename option.

The **paid-flag gate** is important. An item flagged `is_saving=true` but with the Paid box unticked is a *pending contribution* — Yesanio shows "+£X pending" on the goal. This surfaces the common mistake of planning a saving contribution but forgetting to mark it as actually transferred. If pending exceeds 10% of the goal's target, the goal gets a 🕒 warning marker.

## Date windows on goals

Goals can optionally have a `count_from` and `count_to` month. If set, only contributions from plans in that range count toward progress. Leave both empty for all-time counting.

Use cases:
- "Holiday 2026" — set `count_from=2026-01`, `count_to=2026-12`. Next year's holiday gets a new goal.
- "Emergency fund" — leave both empty. Counts forever.
- "Car down payment, starting April" — set `count_from=2026-04`. Earlier contributions (if any existed under the same name for a different purpose) don't count.

## The recompute engine

Every time you save a plan, Yesanio walks all plans in the database, sums matching items per goal (respecting date windows and the status gate), and writes the result to each goal's `current`. This is why `goals.current` is read-only in the UI — it's computed, not entered.

For typical household data (dozens of plans, hundreds of items), the recompute completes in single-digit milliseconds. It's cheap enough to run on every save without special-casing.

## Migrations

Yesanio uses a simple forward-only migration system. The current schema version is stored in a `schema_version` table; on backend startup, the `MIGRATIONS` list in `backend/main.py` is compared to what's applied, and pending migrations are run in order. Each migration is a list of SQL statements executed in a single transaction.

To add a new migration: append a dict to the `MIGRATIONS` list with `version`, `description`, and `sql` keys, then redeploy. Never modify an already-applied migration — always add a new one.

## Backup

The `backup.sh` script takes a MariaDB dump of the `yesanio` database. Run it before any deploy that worries you, before experimenting with the schema, or on a schedule via cron. For a personal household tool, a nightly backup to a location outside the docker volume is a sensible minimum.

#!/bin/bash
# =====================================================================
# Yesanio backup script
# =====================================================================
# Dumps the yesanio database to a timestamped .sql file and rotates old
# backups, keeping the last N days. Designed to be run from cron.
#
# Usage:
#   ./backup.sh                    # backup with defaults
#   BACKUP_DIR=/mnt/nas ./backup.sh   # custom destination
#
# Cron example (daily at 03:15, keep 30 days):
#   15 3 * * * cd ~/docker-compose/yesanio && ./backup.sh >> backup.log 2>&1
#
# Restore example:
#   gunzip -c yesanio-2026-04-10.sql.gz | docker exec -i yesanio_db \
#     mariadb -u yesanio_app -pyesanio_app_change_me yesanio
# =====================================================================

set -euo pipefail

# --- Config (override via env vars) ---
BACKUP_DIR="${BACKUP_DIR:-./backups}"
RETENTION_DAYS="${RETENTION_DAYS:-30}"
DB_CONTAINER="${DB_CONTAINER:-yesanio_db}"
DB_USER="${DB_USER:-yesanio_app}"
DB_PASSWORD="${DB_PASSWORD:-yesanio_app_change_me}"
DB_NAME="${DB_NAME:-yesanio}"

# --- Pre-flight checks ---
if ! command -v docker &>/dev/null; then
  echo "[backup] ERROR: docker not found in PATH" >&2
  exit 1
fi

if ! docker ps --format '{{.Names}}' | grep -q "^${DB_CONTAINER}$"; then
  echo "[backup] ERROR: container '${DB_CONTAINER}' is not running" >&2
  exit 1
fi

mkdir -p "${BACKUP_DIR}"

# --- Dump ---
TIMESTAMP=$(date +%Y-%m-%d_%H%M)
OUTFILE="${BACKUP_DIR}/yesanio-${TIMESTAMP}.sql.gz"

echo "[backup] $(date -Is) — dumping to ${OUTFILE}"

docker exec "${DB_CONTAINER}" mariadb-dump \
  --single-transaction \
  --routines \
  --triggers \
  --add-drop-table \
  -u "${DB_USER}" \
  -p"${DB_PASSWORD}" \
  "${DB_NAME}" | gzip > "${OUTFILE}"

# Sanity check the dump isn't empty
if [ ! -s "${OUTFILE}" ]; then
  echo "[backup] ERROR: dump file is empty, removing" >&2
  rm -f "${OUTFILE}"
  exit 1
fi

SIZE=$(du -h "${OUTFILE}" | cut -f1)
echo "[backup] $(date -Is) — wrote ${SIZE}"

# --- Rotate ---
DELETED=$(find "${BACKUP_DIR}" -name 'yesanio-*.sql.gz' -mtime "+${RETENTION_DAYS}" -print -delete | wc -l)
if [ "${DELETED}" -gt 0 ]; then
  echo "[backup] $(date -Is) — pruned ${DELETED} backup(s) older than ${RETENTION_DAYS} days"
fi

echo "[backup] $(date -Is) — done"

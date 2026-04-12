#!/usr/bin/env bash
# Yesanio restore script — restores the database from a backup.sh dump.
# Usage: bash restore.sh path/to/yesanio-backup-YYYY-MM-DD-HHMMSS.sql
#
# WARNING: this REPLACES the current database. Run a fresh backup first
# if you have any data you want to preserve.

set -e

if [ -z "$1" ]; then
  echo "Usage: bash restore.sh <backup-file.sql>"
  echo ""
  echo "Available backups:"
  ls -1 ./backups/*.sql 2>/dev/null || echo "  (none found in ./backups/)"
  exit 1
fi

BACKUP_FILE="$1"

if [ ! -f "$BACKUP_FILE" ]; then
  echo "Error: backup file not found: $BACKUP_FILE"
  exit 1
fi

echo "About to restore from: $BACKUP_FILE"
echo "This will REPLACE all current Yesanio data."
echo "(If you want to keep the current data first, press Ctrl+C now and run: bash backup.sh)"
read -p "Type 'restore' to confirm: " CONFIRM

if [ "$CONFIRM" != "restore" ]; then
  echo "Cancelled."
  exit 1
fi

echo "Restoring..."
docker compose exec -T yesanio-db mariadb -uroot -pyesanio_root_change_me yesanio < "$BACKUP_FILE"
echo "Restore complete."
echo "Restart the backend so it picks up the restored data:"
echo "  docker compose restart yesanio-backend"

# Installing Yesanio

> **New to self-hosting?** This doc assumes you're comfortable with Docker and a terminal. If not, see [INSTALL-FOR-EVERYONE.md](INSTALL-FOR-EVERYONE.md) — a patient walkthrough for non-developers.

## Requirements

- Docker and Docker Compose (Docker Desktop on Windows/macOS; Docker Engine on Linux)
- ~500MB free disk space
- Ports 6210 and 6211 free on the host

## Quick install

Download the latest release zip from [Releases](https://github.com/jc-universe87/yesanio/releases/latest), or clone the repo:

```bash
git clone https://github.com/jc-universe87/yesanio.git
cd yesanio
docker compose up -d
```

Wait ~10 seconds for migrations to complete, then open `http://localhost:6210`. The first-run wizard guides you through setup.

## Platform notes

**Windows:** Install Docker Desktop with WSL2 backend. Run all commands in PowerShell or Windows Terminal from the extracted folder.

**macOS:** Install Docker Desktop. Apple Silicon and Intel both work — the FastAPI and MariaDB images are multi-arch.

**Linux:** Install Docker Engine and the `docker-compose-plugin`. Add yourself to the `docker` group to avoid `sudo`.

**Chromebook:** Enable Linux (Settings → Advanced → Developers → Linux development environment). Inside the Linux terminal, install Docker, then follow the Linux flow. Open `http://localhost:6210` in the ChromeOS Chrome browser — port forwarding from the Linux container works automatically on recent ChromeOS versions.

## Ports

- `6210` — frontend (nginx)
- `6211` — backend API (FastAPI)
- DB port is internal only

## Credentials

`docker-compose.yml` ships with placeholder credentials named `*_change_me`. Change them before running on anything other than localhost. Yesanio has **no built-in authentication** — for any non-localhost deployment, add auth at the reverse proxy layer.

## Updating

```bash
cd yesanio
git pull   # or download the new release zip and replace files
docker compose down
docker compose build --no-cache yesanio-backend
docker compose up -d --force-recreate
```

Migrations run automatically on backend startup. The DB volume `yesanio_db_data` is preserved across upgrades.

## Backup

```bash
bash backup.sh
```

Writes a timestamped `.sql` dump to `./backups/`. Cron it nightly for a household-grade backup.

To restore: `bash restore.sh ./backups/yesanio-backup-YYYY-MM-DD-HHMMSS.sql` — prompts for confirmation before replacing the database.

## Troubleshooting

**Port already in use** — change the host-side port mappings in `docker-compose.yml`, e.g. `"6310:6210"`.

**Can't connect to backend from frontend** — confirm both containers are running (`docker compose ps`) and that the backend is reachable directly: `curl http://localhost:6211/health` should return `{"status":"ok",...}`.

**Migrations fail on startup** — check `docker compose logs yesanio-backend`. The most common cause is a partial schema from an interrupted earlier deploy. Restoring from backup and re-deploying clean is usually faster than chasing the inconsistency.

**Frontend changes not appearing** — the frontend is bind-mounted, so file edits should be live. Hard-refresh the browser (Ctrl+Shift+R / Cmd+Shift+R) to bypass cache.

## Architecture

See [concepts.md](concepts.md) for the design philosophy and data model. See the main [README](../README.md) for the project overview.

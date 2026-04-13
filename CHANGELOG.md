# Changelog

All notable changes to Yesanio.

## 2.5.22 — April 2026
Doc-only release. No code or schema changes.
- **README.md**: the upgrade instructions used `cd ~/docker-compose/yesanio` — a path specific to the author's server setup. Replaced with `cd yesanio` and a comment saying "navigate to wherever you installed Yesanio". Users with the folder at `~/yesanio`, `~/Downloads/yesanio`, or elsewhere no longer need to mentally translate.
- **INSTALL-FOR-EVERYONE.md**: all 8 embedded screenshots converted from plain markdown to HTML `<img>` tags with `width="560"`. At native resolution they rendered huge on GitHub, dominating the text around them. 560px fits comfortably in GitHub's rendered content column while keeping all image detail readable.
- **README.md**: home and plan screenshots also scaled from 720 to 560 for visual consistency with the install docs.

## 2.5.21 — April 2026
Doc-only release. No code or schema changes.

**INSTALL-FOR-EVERYONE.md** improvements from a real Windows install walkthrough:
- Seven real screenshots embedded in the install guide (Windows About page, Docker download page, Docker configuration checkboxes, Docker welcome screen, WSL-needs-updating error, extracted folder structure, Yesanio welcome wizard).
- **Windows chip guidance**: AMD64 vs ARM64, with where to check (System type on the About page) and which button to click on the Docker download page.
- **Mac chip guidance**: Apple Silicon (M1/M2/M3/M4) vs Intel, with how to check and why it matters.
- **Windows Docker Desktop configuration**: corrected from "two checkboxes" to three — tick WSL 2, leave Windows Containers UNticked, tick Add shortcut. The doc had it wrong before.
- **Windows restart reality**: it's a full Windows restart, not a sign-out, and sometimes two restarts are needed if WSL2 itself needs updating.
- **WSL needs updating** inline help: the exact error dialog is documented with a screenshot, and the user is walked through `wsl --update` in admin PowerShell.
- **Docker Desktop sign-in screen**: corrected from "Continue without signing in" to the actual "Skip" link in the top-right of the sign-in card.

## 2.5.20 — April 2026
Doc-only release. No code or schema changes. Users running v2.5.19 don't need to redeploy.
- **INSTALL-FOR-EVERYONE.md** — multiple improvements after a real Chromebook install test surfaced gaps:
  - Chromebook: use `newgrp docker` to activate the docker group in the current shell (faster than the full Linux container restart, which is now documented as the fallback only).
  - Chromebook: reframed the `docker compose` vs `docker-compose` guidance — not "Chromebook needs hyphen" but "try one, if it fails try the other, both work."
  - Chromebook: documented that both `localhost:6210` and `penguin.linux.test:6210` work on current ChromeOS, and that `penguin.linux.test` is a ChromeOS-wide convention (any Chromebook with default Linux setup), not device-specific.
  - Chromebook: added an optional `git clone` path as an alternative to downloading the zip. Also documented how to remove a previous `~/yesanio` folder before reinstall.
  - Windows version floor corrected: WSL2 needs Windows 10 version 2004 (May 2020 update) or newer, not the previously-stated 1903.
  - macOS version floor corrected: Docker Desktop now requires macOS 12 (Monterey), not macOS 11 (Big Sur).
  - Added an Apple Silicon note: Docker Desktop may prompt for Rosetta 2 installation on first launch.
  - "Ask for help" language updated throughout: in addition to asking a more technical friend, users are now pointed to AI assistants like ChatGPT or Claude for paste-the-error-and-explain help. Removed the suggestion to file questions on the GitHub repo, since this invites ongoing support load on the maintainer.
  - Added a closing footnote honestly flagging which install paths are personally verified (Linux, Chromebook) versus which describe Docker Desktop's documented behaviour without hands-on testing (Windows, macOS).
- **INSTALL.md** — same Chromebook findings applied in condensed form.

## 2.5.19 — April 2026
- **Compatibility fix:** Yesanio now runs on systems with legacy `docker-compose` (1.x), including Chromebook's default Linux environment, Debian Bookworm, and older Ubuntu installs. The `name: yesanio` directive at the top of `docker-compose.yml` was a Compose v2.x feature that broke compose-1.x with `'name' does not match any of the regexes` error. Removed. Container/volume names now derive from folder name, so users should always unzip into a folder called `yesanio`.
- `restore.sh` now auto-detects whether `docker compose` (space) or `docker-compose` (hyphen) is available and uses whichever exists.
- INSTALL.md and INSTALL-FOR-EVERYONE.md: corrected the Linux/Chromebook install commands. The package name `docker-compose-plugin` only exists in Docker's own apt repo (not added by default on Debian/Chromebook); the Debian package is `docker-compose` (hyphen). Fixed `usermod -aG newgrp docker` typo to `usermod -aG docker $USER`. Documented that Chromebook needs a full Linux container restart, not just a terminal reopen, for the docker group to take effect.

## 2.5.18 — April 2026
- README now shows the Yesanio logo, and two screenshots (Home view and Plan view) placed inline with the explanations they illustrate. Images live in `docs/images/`.
- Added the *"Clarity. Overview. Control."* tagline to the README header, matching the in-app wordmark.

## 2.5.17 — April 2026
- **Bug fix:** the v2.5.16 hamburger menu broke the fixed-floating header on narrow viewports. The dropdown was positioned `absolute` relative to the header, which forced the header itself to `position: relative` — undoing the global `position: fixed`. Now the dropdown is `position: fixed` and anchored to the viewport directly (54px from top, 8px from right), so the header stays floating at all widths.

## 2.5.16 — April 2026
- Top navigation collapses into a hamburger menu (☰) at viewport widths of 760px or below. Previously the rightmost nav items got clipped on narrow browser windows. The hamburger opens a clean dropdown menu, closes on view selection, on outside-click, and on Escape. Active view still highlighted in the dropdown.

## 2.5.15 — April 2026
- Terminology sweep: four pieces of explanatory copy still talked about "marking items done" from before the v2.5.14 status→paid migration. Updated the Goals helper tip and three lines in the README to consistently describe "ticking the Paid box". The data model already used `paid` everywhere; this catches the remaining text references.

## 2.5.14 — April 2026

Cleanup release based on a full project audit. No new features; many small improvements that compound.

**Removed dead code & redundancies**
- Dead `loadSettings()` one-liner (v2.4.x leftover, never called) removed
- Dead `/settings/user_name` GET and PUT endpoints + `UserNameIn` model removed (superseded by generic `/settings` endpoints in v2.5.1)
- Migration v8: drops the unused `group_limit` column from `plan_groups`. The column had a UI input, persistence, and zero behavioural consequence — a phantom feature
- Frontend cleanup of `group_limit` references in markup, CSS, save payload, CSV import/export, and the `addGroup()` helper
- Unused `Literal` import removed from backend

**Status simplified to Paid (Path 2)**
- Migration v9: replaces three-state `status` field (none/pending/done) with a `paid BOOLEAN` field. Existing data: items with `status='done'` become `paid=true`; everything else becomes `paid=false`. Information-preserving for the goal-tracking use case (only "done" mattered for goal progress).
- Frontend: status dropdown becomes a single Paid checkbox. Cleaner, faster to mark, more obviously meaningful
- CSV format updated: "Status" column becomes "Paid". Legacy CSVs with "Done"/"Not started"/"Pending" still import correctly (Done → true, others → false)
- Backend `_recompute_goals` and `_get_pending` now gate on `paid` not `status`

**User-friendliness**
- Goals view gets a serif title and one-line subtitle clarifying what goals are for
- Stronger month-delete confirmation: must type the month name (e.g. `2026-04`) before the Delete button enables. Prevents accidental loss of a whole month's planning
- INSTALL-FOR-EVERYONE: stronger credentials callout with ⚠️ marker
- INSTALL-FOR-EVERYONE: hardcoded `yesanio-v2.5.7.zip` URLs updated to use versioned `releases/download/v...` pattern with a clear "find current version" instruction

**New: data restoration**
- Added `restore.sh` script: takes a backup file, prompts for typed "restore" confirmation, replaces the database
- README and both INSTALL docs document the restore flow

**Documentation consistency**
- Canonical Yesanio one-line description used across README and concepts: *"Yesanio is a self-hosted budgeting tool for households that plan their money together — built around the principle that every pound has a job before the month begins."*
- concepts.md updated to describe `paid` instead of `status`

## 2.5.13 — April 2026
- Removed the Load button on the Plan view — typing a month directly into the month input now auto-loads it (previously you had to type the month then click Load). The existing dirty-check confirms before discarding unsaved edits.
- Renamed "Copy previous" to "📋 Copy from previous month" with an explanatory tooltip clarifying it copies all groups and recurring items from the prior month.

## 2.5.12 — April 2026
- **Critical fix:** Plan-view drag-and-drop now actually works. Root cause: `initPlanSortables()` was defined and exported but never called. The v2.5.9 regex that was supposed to wire the hook into `render()` failed to match (whitespace mismatch) and silently no-op'd. v2.5.12 explicitly calls the init at the end of `render()`. Diagnosed by `_sortableInstances.length === 0` in browser console.
- **Bug fix:** Goals reorder now works repeatedly, not just once. Old Sortable instances on the goals list weren't destroyed before re-creating new ones on each `loadGoals()` call, causing stale instances to interfere with subsequent drags. Now tracked in `_goalSortableInstances` and destroyed before re-init.

## 2.5.11 — April 2026
- **Bug fix:** drag-and-drop reordering of items and groups in the Plan view now actually works. Two underlying causes: (1) item drag handle was using a generic `.drag-handle` class also matched by group handles, causing event ambiguity; switched to the more specific `.col-drag` selector. (2) HTML5 native drag-and-drop has a known issue with `<tr>` elements inside `<tbody>` — switched all SortableJS instances to `forceFallback: true` which uses SortableJS's own drag implementation, more reliable inside tables and on touch.
- Item drag also now explicitly excludes inserted warning rows (rename-warn, delete-warn) from being draggable.
- Drag handle column is wider (30px), has a hover background, and a higher-contrast handle icon — much easier to spot and click.
- Goal drag handle moved to the LEFT side of each goal card (inline, vertically centred), matching the leftmost-handle convention used elsewhere.

## 2.5.10 — April 2026
- **Bug fix:** drag-and-drop reordering of items within a group now works. The drop handler was calling `render()`, which destroyed the SortableJS instance mid-callback and lost the move. Item drops now skip the re-render (the DOM is already in the right order) and just update state. Group drops still re-render (because each child group's `dataset.gIdx` needs refreshing) but defer the call to a microtask so SortableJS can finish first.
- **Bug fix:** Home view no longer shows empty state on first page load. After `loadMonth()` completes, if Home is the active view, it re-renders with the freshly-loaded data. Previously you had to navigate to Plan and back for Home to show your data.
- **Bug fix:** the brief "Backend unreachable" flash on page load is gone. Frontend now waits for the backend `/health` endpoint to respond OK before initialising the UI. If the wait exceeds 500ms, a calm "Connecting…" overlay appears (typical Docker cold start is 5–8 seconds). Times out after 30 seconds with a clear error.

## 2.5.9 — April 2026
- **Bug fix:** the v2.5.8 undo/redo/revert toolbar buttons were missing entirely. The patch script anchored on a markup pattern that didn't exist in the actual file, so the toolbar `<button>` elements were never inserted. The history JS was wired but had nothing to wire to. v2.5.9 ships the toolbar properly.
- Drag-and-drop reordering on Plan view (items within a group, and groups themselves) and on Goals view. Drag handles on the leftmost column of items, on group headers, and on goal cards. Touch-friendly long-press behaviour on mobile.
- Drag operations on the Plan view push to the undo history — drag a row, undo restores it.
- Goal reorder persists immediately via new `POST /goals/reorder` endpoint (no save needed on the Goals page).
- SortableJS 1.15.6 added as a self-hosted vendored library (`frontend/Sortable.min.js`, ~45KB, MIT licensed). No CDN dependency.

## 2.5.8 — April 2026
- Undo / Redo / Revert in the Plan view (toolbar buttons + Ctrl+Z / Ctrl+Shift+Z keyboard shortcuts). History captures up to 100 edit steps with debounced per-field-blur granularity. History clears on save and on month load. Revert reloads the last saved version from the database after confirmation.
- Cancel button added to the rename warning panel. Cancel restores the item name to its original value before the edit.
- Delete confirmation for `is_saving` items now shows a goal-aware warning panel: explains that deleting removes this month's contribution from the goal's progress (other months unaffected), suggests unchecking status as a softer alternative, and includes a Cancel button.
- Achieved goals (where current ≥ target) drop into a separate "✓ Achieved goals" section below active goals, in calm forest-green styling with a "Reached this month / last month / [Month Year]" date line. Section has a Hide/Show toggle that persists per user.
- Top header is now fixed on desktop too (was already fixed on mobile). Page content has top-padding so it doesn't slide under the bar.
- Migration v7: `goals.achieved_at DATE NULL`. Recompute engine now sets/clears `achieved_at` based on whether current crosses target. No data loss; existing goals start with NULL and get populated on the next plan save.
- Backend version 2.5.8.

## 2.5.7 — April 2026
- Added `docs/INSTALL.md` — terse install guide for developers comfortable with Docker. Covers Windows, macOS, Linux, Chromebook.
- Added `docs/INSTALL-FOR-EVERYONE.md` — patient, no-jargon walkthrough for non-developers. Covers all four platforms with full step-by-step instructions, troubleshooting at every step, an honest "before you start" preview of what installing Yesanio actually involves, and an update flow for future versions.
- README updated to surface both install docs prominently.
- No code or schema changes.

## 2.5.6 — April 2026
- Currency dropdown expanded to 121 currencies, with the 10 most-traded (USD/EUR/JPY/GBP/CNY/AUD/CAD/CHF/HKD/SGD) grouped at the top under "Most common". Remainder grouped alphabetically under "All currencies".
- Same currency list now used in both the Plan view and the wizard step 3.
- Yesanio logogram added to the top of every wizard step.

## 2.5.5 — April 2026
- Wizard adapts to existing users: if the database has any saved plans, step 4 (template/blank chooser) is hidden and step 3 ends with "Finish" instead of "Next". Existing users who re-run the wizard now land on Home, not Plan, with their data untouched.
- Skip wizard button now available on every step.
- Added a save reminder note on step 4 for new users: the template loads in Plan but isn't auto-saved.
- Charts now render at their natural width based on month count, capped at the screen width — small datasets no longer stretch across the whole page.
- "Show welcome tour again" button now triggers the wizard inline without a page reload.

## 2.5.4 — April 2026
- **Critical fix:** v2.5.3 patch left orphaned syntax garbage in `index.html` from a too-greedy regex in the saveSettings rewrite. The fragment `}/settings/user_name`,{method:"PUT"...` after the new saveSettings function broke JavaScript parsing, killing nav button handlers, the wizard, and the entire DOMContentLoaded wire-up downstream of line 1510.
- Verified with `node --check` this time — clean parse, no syntax errors.
- No backend, schema, or feature changes.

## 2.5.4 — April 2026
- **Critical fix:** v2.5.3 shipped with an orphaned code fragment from a botched regex replacement that left `}/settings/user_name`...` dangling after the new `saveSettings` function. The browser parsed `}/...` as a regex literal, threw `SyntaxError: Invalid regular expression flags`, and the entire script failed to parse — meaning ALL nav buttons, settings, wizard, and tips were broken in v2.5.3. v2.5.4 ships the clean source.
- Added missing `window.saveGoalInline` export so inline onclick handlers in Goals tab work.
- No backend or schema changes.

## 2.5.3 — April 2026
- **Critical fix:** wizard, helper tips, and settings persistence now actually work. The v2.5.1/v2.5.2 JS block was placed outside the script tag and never executed — every wizard/tip function was undefined. Functions now correctly defined and exposed on `window` for inline onclick handlers.
- `saveSettings` rewired to use the generic settings endpoint
- No schema or backend logic changes

## 2.5.2 — April 2026
- Fixed settings persistence: helper tip dismissal, toggle, and "Show welcome tour again" now save correctly
- Charts constrained to 960px max-width on large screens
- Generic-ified helper tips and documentation (no more AMEX-specific or personal group-name references)
- Added SECURITY.md with GitHub private vulnerability reporting
- Added Data and privacy section to README (GDPR household-activity exemption, no telemetry)
- Copyright line updated to `Johannes Kim (Pistio)` combined form
- Documentation now describes both credit-card and debit-card cash-flow patterns

## 2.5.1 — April 2026
- First-run welcome wizard introducing the "pay yourself first" principle
- Contextual helper notes on Plan, Goals, Charts, Home (dismissible per-user)
- Improved rename warning explaining goal-link consequences in plain language
- About section in Settings with version, GitHub link, MIT licence notice
- "Show helper tips" toggle and "Show welcome tour again" button in Settings
- Generic `/settings` endpoint for future preference storage
- Auto-complete wizard flag on upgrade for existing installations
- `LICENCE`, `CHANGELOG.md`, `.env.example`, `docs/concepts.md` added

## 2.5.0 — April 2026
- Goal linking: `is_saving` flag on plan items
- Goals auto-create when linked items are saved
- Status-gated contributions (only `status=done` items count toward progress)
- Per-goal date windows (`count_from`, `count_to`) for yearly/rolling goals
- Pending contribution warning surfaced on Goals and Home
- Cross-month rename endpoint (`POST /goals/rename`)
- Goals tab read-only for `name` and `current`; editable for target/kind/dates
- Migration v6: `is_saving` column, goal date-window columns, wipe `goals.current`

## 2.4.5 — April 2026
- Editorial Home view with Lora serif headline
- Warm cream palette, narrow 720px reading column
- Self-hosted Inter, Lora, Nunito fonts (no external CDN)
- "April 2026" page heading treatment in Lora

## 2.4.1 – 2.4.4 — April 2026
- Home view replaces Dashboard as default landing
- Sentence-based layout (bills, giving, saving) replacing stat cards
- Settings tab with user name preference
- Typography polish passes, warm colour palette, small-caps bylines
- Migration v5: `settings` table for user preferences

## 2.4.0 — April 2026
- `is_giving` flag on plan groups
- Giving shown separately on Home and in exports
- Migration v4: `is_giving` column on `plan_groups`

## 2.x — earlier
- Refactored to plans/groups/items data model
- Migration framework for schema evolution
- Multi-currency support (per-plan)
- Month-level notes and tags
- Status tracking per item (none/pending/done)
- CSV import/export
- Historical charts

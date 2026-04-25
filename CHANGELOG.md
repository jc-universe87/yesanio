# Changelog

All notable changes to Yesanio.

## 2.7.1 — April 2026
**Visual fix.** Frontend-only.

The ✎ edit pencil added in v2.7.0 was rendering on top of the progress amount text on the right side of each goal tile (e.g. "2%" overlapping with the pencil glyph). Fixed by reserving right-padding on the tile head so amount text leaves room for the absolutely-positioned button. Pencil also slightly smaller and softer (lower opacity at rest, full on hover) so it doesn't compete with the goal name visually.

## 2.7.0 — April 2026
**Goals view redesign.** Frontend-only — no backend or schema changes.

The Goals view had accumulated edit fields that pushed the actual progress out of focus. Every goal card showed all the configuration (target input, kind input, two date pickers, save button) at all times — even though most visits to the Goals page are just to glance at progress, not to reconfigure anything.

Redesigned around progress-first, configuration-on-demand:

- **Tile view (default state)** — Each goal card shows the name, the progress amount (e.g. *"£100 of £500 · 20%"* or *"£50 saved · no target set"*), a wider progress bar, and a pending row if relevant. Nothing else. Clean dashboard tile.
- **Edit on demand** — A small ✎ pencil icon in the top-right corner of each card opens the edit panel. Target amount, optional Count from / Count to date range, Save / Cancel / Delete buttons. Card collapses back to tile view on Save or Cancel.
- **Visual refresh** — More breathing room, bigger typography for the goal name (Lora serif), softer meta text. Achieved goals get a subtle green tint instead of competing for attention.
- **Hidden but preserved**: the "Kind" field (which had no behavioural meaning in the app — it was a cosmetic label) is no longer in the edit UI. Existing goal records keep their `kind` value in the database; the API still accepts it; users just can't edit it from the Goals page anymore. Reduces UI surface area without data loss.

Drag-to-reorder still works. Pending warnings still show. Confirm-to-delete still requires two clicks.

## 2.6.6 — April 2026
Small addition: a permanent footer visible on every view shows the current Yesanio version and attribution. Reads:

> Yesanio v2.6.6 · © Pistio · MIT

The version number links to the release page on GitHub for that specific tag, so a user noticing they're on an older version can click through and see what's in the current version. Frontend-only, no schema changes.

## 2.6.5 — April 2026
**Bug fix: goals without a target were showing as empty on both the Goals page and Home, even when they had accumulated contributions.**

The backend was (correctly) summing contributions into `goals.current` for every saving item. But the frontend card-rendering logic only displayed the `current` value **when target > 0**. If target was 0 (the default for auto-created goals), the card silently showed "no target set" and hid the £100 or £500 of contributions already accumulated. Similarly on Home: the savings line filtered for `target > 0` and so never mentioned targetless goals.

Fixed in both places:
- **Goals page**: targetless goals with progress now display *"£100 saved · no target set"* instead of just *"no target set"*. Data that was always in the database is now visible.
- **Home view**: savings line now includes targetless goals too. Shown as *"Saving toward Junior ISA Yeri (£50 saved)"* rather than a percentage. Targeted goals still show percentage; targetless goals show the absolute amount.

No schema changes, no backend changes — just frontend conditionals that were hiding real data.

## 2.6.4 — April 2026
**Feature.** Frontend-only.

The Calculator panel can now be dragged. Click and hold on the panel's header (the bar with "Calculator" at the top) and drag it anywhere on screen. Useful for the recurring problem of the panel sitting on top of the items you're trying to add to it — drag it out of the way once and continue working.

Behaviour:
- **Desktop (>760px)**: drag the header to move the panel anywhere. The panel can't be dragged off the visible area — it snaps back inside the viewport on release.
- **Mobile (≤760px)**: the panel docks to the bottom of the screen as a full-width sheet, no dragging. Bottom-sheet is the native mobile pattern and works regardless of where you scroll.
- **Position resets on each open.** The panel doesn't remember where you last put it across page reloads (or even between opens) — every fresh open starts at the default bottom-right position. Avoids "where did I last leave it?" confusion.
- **Window resize** while the panel is open re-clamps the position so it stays in view (useful if you rotate a tablet or resize a window).

A small ⋮⋮ handle icon shows on the left of the header on desktop, and the cursor changes to "move" — both signals that the header is grabbable.

## 2.6.3 — April 2026
**Calculator panel — usability improvements.** Frontend-only, no schema change.

The Calculator panel previously sat fixed in the bottom-right corner, exactly where the most-edited rows often are. This release makes it work on every screen size:

- **Desktop (>760px wide)**: The panel header is now a drag handle (cursor changes to "move", subtle ⋮⋮ grip indicator on hover). Drag the panel anywhere on screen. Position is constrained inside the viewport — drop too far off-screen and it snaps back inside the visible area on release. Position resets to default when you close the panel; reopening starts fresh in the bottom-right corner.
- **Phone (≤760px wide)**: The panel docks as a full-width bottom sheet, taking the entire bottom of the screen up to 60% viewport height. No dragging on phones (it would just end up off-screen or covering the whole screen anyway). The standard mobile pattern.
- Window-resize handler re-clamps a dragged panel back inside the viewport if you resize the browser smaller than the panel's current position.

## 2.6.3 — April 2026
**Bug fix.** Frontend-only.

The Calculator's per-item +/− buttons broke when groups or items were reordered via drag-and-drop. The selected state was lost, and clicking a button after a reorder added the wrong item to the calculation.

Root cause: the calculator was tracking items by their array indices `(gIdx, iIdx)`, which become stale the moment items move. After a reorder, the calculator was looking up "item at position 3" but position 3 now held a different item.

Fix: switched the calculator to track items by direct JavaScript object reference. Object references survive reordering — the calculator now knows "I have THIS specific item in my sum" and doesn't care where it lives in the array. Three benefits:

- Reordering preserves the calculator state and the +/− button highlighting
- The calculator amount stays live as you edit the item's amount field on the Plan view
- Items deleted from the Plan are auto-removed from the Calculator on next render (no zombie lines)

Custom amount entries (typed values, not item-linked) are unaffected — they were already tracked independently.

## 2.6.2 — April 2026
Three small UX tweaks. Frontend-only, no schema changes.
- **Renamed "Transfer calculator" to just "Calculator".** The original name implied a single use case (deciding bank transfer amounts). The tool is useful for any "what's the sum of these items?" question — recurring subscription totals, savings goal contributions, anything. The shorter name doesn't constrain it.
- **Item delete button moved to the rightmost position** in each row. The new column order is: drag, name, amount, notes, paid, savings, recurring, calculator (+/−), delete. The delete column always sits at the end so muscle memory works whether the calculator is open or closed.
- **Replaced ✕ with ⊗ for all delete actions** — group delete, item delete, goal delete, tag chip remove, and the remove-from-calculation button on each calc line. The ✕ character read too closely to the multiplication sign in the calculator context. ⊗ (circled X) is the standard "remove/dismiss" glyph in modern UIs and reads unambiguously. Cancel buttons (which dismiss without deleting) still use ✕ to keep the visual distinction between "cancel" and "delete."

## 2.6.1 — April 2026
**Bug fix + feature.** Frontend-only, no schema changes.

The `updateTotals()` function had been an empty stub since v2.4.0. It was called from 15+ places across the codebase every time something changed (typing a number, ticking Paid, saving, dragging), but did nothing. No one noticed because the Home view's editorial summary handled the "how's this month looking?" question. But the Plan view — where you're actually editing — had no running totals visible. Embarrassing oversight, now fixed.

- **Group totals** now populate in each group card header (right side) as `£X,XXX.00`, updating live as you type or tick items.
- **New Plan summary bar** at the top of the Plan view, below the month/income/notes toolbar and above the first group. Three cells: **Income** (what you earn), **Allocated** (sum of everything planned), **Saldo** (what's left over).
- **Saldo visual states** follow the Yesanio philosophy ("every pound has a job — zero is the goal state"):
  - **Zero** → calm green, "✓ Fully planned"
  - **Positive** (surplus) → warm gold, "£X unassigned"
  - **Negative** (over) → red warning, "£X over"

Same visual vocabulary as the Home view, applied to the editing surface.

## 2.6.0 — April 2026
New feature. Frontend-only — no schema changes.

**Transfer calculator.** A small floating panel on the Plan view, for the specific use case of "how much do I need to move between bank accounts this month?" Click the 🧮 button in the bottom-right corner of the Plan view. While the panel is open:

- Every item row shows small **+** and **−** buttons on the right
- Clicking **+** adds the item's amount to a running total
- Clicking **−** subtracts it
- Clicking the same button again removes the item from the calculation
- Clicking the opposite button flips its sign
- A text input at the top of the panel accepts custom amounts — either a number or a simple expression like `50+30`
- **Copy total** puts the number on your clipboard, ready to paste into your bank's transfer screen

The calculation resets when you reload the page. It's a session tool, not a saved object. No backend involvement, no persistence — pure frontend state.

## 2.5.23 — April 2026
Doc and UI-text polish pass. No code logic or schema changes. Users on v2.5.22 don't need to redeploy, but this release is the cleaner face for anyone landing on the public repo.
- **README Home view example**: changed the example name from "JOHANNES" to the generic "ALEX", so the illustration reads as an example rather than as the author's real budget.
- **README Home view example giving line**: changed the giving category examples from "Tithes + Offering, Mission Offering, Compassion Donation" (specifically Christian) to "Tithe, Mission Giving, Charity Donation" (denomination-neutral). The giving feature itself is unchanged — the user can name their giving categories anything. This is just the example copy.
- **Settings and Wizard "Your name" input placeholders**: changed from `e.g. Johannes` to `e.g. Alex` in both spots. The placeholder now reads as a generic example rather than as a suggested default.
- The author's name is preserved where it belongs — in the MIT licence copyright line (LICENCE, README footer, frontend footer), as required for attribution.

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

# CbD Scheduled Tasks Reference

Last updated: 2026-04-18

---

## Active Scheduled Tasks

### `cbd-base-hygiene`

| Field | Value |
|-------|-------|
| **Name** | cbd-base-hygiene |
| **Schedule** | Every Friday at 8:03 AM |
| **Created** | 2026-04-18 |

**Purpose:** Weekly Airtable base hygiene check. Audits the Products and Vocabulary tables for fill-rate gaps that would block the Pinterest brief, Tailwind CSV generation, or vocabulary dashboard. Outputs a tiered report (🔴 Blocking / 🟡 Needs Attention / 🔵 Vocabulary) to `_Operations/Hygiene Reports/CbD_Base_Hygiene_[YYYY-MM-DD].md`.

**Checks run:**
1. Live products with empty Pinterest URL → blocks daily brief auto-detect
2. TPT-listed products with empty Canva Image 1 Share URL → blocks Tailwind
3. Pinterest ✓ checkbox / Pinterest URL mismatch → auto-corrects the checkbox
4. Live products missing Canva Pin Design ID → blocks fresh-pin rotation
5. Vocabulary: words with empty Word Type, Core words missing Core Tier tag

**Output folder:** `_Operations/Hygiene Reports/` (created on first run if missing)

**⚠️ Pre-approve:** Run manually once first (Scheduled sidebar → Run now) to pre-approve the Airtable MCP tool before the first automated Friday run.

---


### `cbd-dashboard-refresh`

| Field | Value |
|-------|-------|
| **Name** | cbd-dashboard-refresh |
| **Schedule** | 3× daily: 8:16 AM, noon, 11:30 PM |
| **Last Updated** | 2026-04-05 |

**Purpose:** Regenerates all 4 CbD dashboards from Airtable + hardcoded data.

**CRITICAL:** HTML edits to dashboards are overwritten on every run. ALL data corrections must go in this task's prompt — not directly in the HTML files.

**Prompt updates (Apr 5 2026):**
- PB Companion row: hardcoded with actual word counts (not derived from Airtable — PB vocab not synced yet)
- Poetry Unit 1: shows 28 words with "(not synced)" note — never pendingBuild, just unsynced
- Core/Fringe/Heart columns: show actual word counts, not checkmarks
- KPI corrected: 501 words (was wrong before)

**How to trigger:** Runs automatically 3× daily. To manually refresh: open Scheduled Tasks → find `cbd-dashboard-refresh` → Run now.

---

### `cbd-pinterest-daily`

| Field | Value |
|-------|-------|
| **Name** | cbd-pinterest-daily |
| **Schedule** | 9:06 AM daily (disabled by default — run manually) |
| **Prompt version** | v3.0 (updated 2026-04-01) |
| **Prompt file** | `Distrubution/Pinterest/CBD_Pinterest_Daily_Task.md` |

**Purpose:** Generates a daily Pinterest pin brief file. Pulls live products from Airtable Products table, builds keyword-weighted pin content for up to 3 products (2 from List A: needs first pin + 1 from List B: fresh pin cycle), outputs today's repin target based on thin-board priority, saves brief to `Distrubution/Pinterest/Daily Briefs/`. Does NOT attempt Pinterest browser automation.

**Key rules:**
- Queries **Products table** (`tbl2YSRQiW7RHEPY5`), Pinterest ✓ field = `fldhVp0lOxQaB9PUB` — NOT Work Items table
- Pin titles lead with search keyword (40% algorithm weight), not brand name
- Fresh pin cycle: each product should have 3–5 substantially different designs at 60–90 day intervals
- Thin boards override day-of-week repin rotation until boards reach 15+ pins

**How to trigger:** Run the `cbd-pinterest-daily` scheduled task manually, or ask Claude to "generate today's Pinterest brief."

---

### `cbd-tpt-browser-tasks`

| Field | Value |
|-------|-------|
| **Name** | cbd-tpt-browser-tasks |
| **Trigger** | Manual (ad-hoc) — run on demand |
| **Created** | 2026-03-27 |
| **Last Updated** | 2026-03-27 (expanded from TPT-only to full CbD) |

**Purpose:** Reads the Airtable Work Items table for records where "Ready to Pick Up" is checked, then executes each task via browser automation across all CbD platforms. Verifies completion, marks Done, unchecks "Ready to Pick Up", and sets social checkboxes.

**Platforms covered:** TPT, Substack, Facebook (special education groups), Instagram, Pinterest, Canva

**Workflow:**
1. Read Airtable (`appeaT8hkeXWqQKIj`) → Work Items where "Ready to Pick Up" = true
2. Group tasks by platform
3. Execute each task in the browser (TPT listing updates, Substack drafts/publishes, social posts, Canva edits)
4. Verify completion by checking the result on the platform
5. Mark Work Item as Done = true, uncheck "Ready to Pick Up"
6. Set social platform checkboxes as applicable (Pinterest ✓, Instagram ✓, Facebook ✓)

**How to trigger:** Ask Claude to "run the CbD browser task queue" or "execute ready tasks" — Claude will call this scheduled task.

---

## Airtable Structure Reference

| Table | ID | Purpose |
|-------|----|---------|
| Work Items | `tblZFoHoKnkJqySSQ` | All CbD tasks, content, platform actions (44 records) |
| Products | `tbl2YSRQiW7RHEPY5` | One record per product with pipeline milestone checkboxes (32 records) |

**Products table linked field:** "Work Items" field = `fldQqKF1j3rZKRifK` (links to Work Items records)
**Work Items inverse field:** `fldEGq3wWjgCurfkv` (auto-created "Products" column)

---

## Work Items Field Reference

| Field | ID | Notes |
|-------|----|-------|
| Product Line | `fldG4I9Ba9k9OfrL8` | Only valid values: AT/AAC IEP Team, AT/AAC Family, Nonfiction, UFLI Phonics, Picture Book Companions, Trading Cards, Bundle, Fiction Anchor Texts. Operations is NOT a valid Product Line. |
| Task Category | `flddTbX7EhIE1EV28` | "Product Work" or "Operations". Operations tasks leave Product Line blank. |

## Notes

- 3 blank Work Items records pending manual deletion in Airtable UI: recacRAoUpf2Pm7K6, reccV2W1OY0Z4xHgI, recm3WsrttywsUP6p
- "Operations" choice still exists in Product Line field options — remove it manually in Airtable field settings (no records use it anymore).
- **Pinterest ✓ field:** Products table (`fldhVp0lOxQaB9PUB`) is authoritative. Work Items table also has a Pinterest ✓ field (`fldAKwTPAY570wV2Q`) but it reflects platform-action task status, not product pin status. Daily Pinterest task uses Products table only.

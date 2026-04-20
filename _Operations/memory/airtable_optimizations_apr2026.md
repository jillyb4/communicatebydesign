# Airtable Optimizations — April 2026
*Three changes from the Airtable audit session. All require manual action in the Airtable UI.*

---

## 1. Add Pinterest Status Select Field to Products Table

**Why:** The `Pinterest URL` field (fldx9FesXwfqZhWYp) currently does double duty — it stores data (the URL) AND signals workflow state (pinned vs. not pinned). The daily brief has to *infer* status by checking whether the URL is empty. Adding a dedicated `Pinterest Status` select field separates data from logic, makes Interfaces cleaner, and lets automations branch on a real value instead of an emptiness check.

**Do this once in the Airtable UI:**

1. Open the **Products** table (`tbl2YSRQiW7RHEPY5`)
2. Scroll to the far right of the field list → click **+** to add a new field
3. Name it: `Pinterest Status`
4. Type: **Single select**
5. Add these options in this order (colors suggested — match your brand):

| Option | Color | Meaning |
|--------|-------|---------|
| Not Pinned | Gray | No pin exists yet for this product |
| Pinned — Active | Green | First pin is live; in 60-day fresh-pin window |
| In Fresh Cycle | Blue | Active rotation — 2nd or 3rd pin design live |
| Pinned — Archived | Light gray | 5 pins built; product has aged off rotation |

6. Click **Save**
7. Position the field: drag it to sit **immediately after** `Pinterest URL` in the field order

**Then — populate it for all live products:**

Open each Live product record and set `Pinterest Status` based on:
- `Pinterest URL` is empty → **Not Pinned**
- `Pinterest URL` has a URL, `Pinterest Pin Count` = 1 → **Pinned — Active**
- `Pinterest URL` has a URL, `Pinterest Pin Count` 2–4 → **In Fresh Cycle**
- `Pinterest Pin Count` = 5 → **Pinned — Archived**

**Then — set up the Automation trigger:**

In Airtable → **Automations** → Create new automation:

- **Trigger:** When record updated → Products table → watch field: `Pinterest URL`
- **Condition:** `Pinterest URL` is not empty AND `Pinterest Status` = "Not Pinned" (or is empty)
- **Action 1:** Update record → set `Pinterest Status` = "Pinned — Active"
- **Action 2:** Update record → set `Pinterest ✓` checkbox = true

This replaces the conceptual "auto-detect rule" that was previously only documented in CLAUDE.md with a real, working Airtable automation. When you paste a URL into `Pinterest URL`, the status field flips automatically — no other step needed.

**Field ID to use in scripts:** Once created, find the field ID by opening the field settings → the URL will contain `fld...` — add it to this file.

---

## 2. Build the Launch Runway Interface

**Why:** The current daily workflow requires opening the Products grid, manually toggling field visibility, and scrolling past fields that aren't relevant to the current stage. The Launch Runway Interface gives you a single view — grouped by Workflow Stage, showing only what matters right now — that you can open every morning as your default working view.

**Do this once in the Airtable UI:**

### Step 1 — Create the Interface

1. Click **Interfaces** in the top navigation (the icon that looks like a grid/window)
2. Click **+ New interface**
3. Name it: `Launch Runway`
4. Choose **Blank** (not a template)

### Step 2 — Add a Record List component

1. Inside the blank interface, click **+ Add element**
2. Choose **Record list**
3. Data source: **Products** table
4. Click **Customize** on the record list

### Step 3 — Configure grouping

1. **Group by:** `Workflow Stage` (fldQuczj4Nhbt7BSA)
2. Check **Show group counts** — this gives you "Building (3)" etc. at a glance
3. Group order (drag to match):
   - Building
   - Ready to List
   - Live
   - Planning
   - Idea
   *(Move Idea and Planning to the bottom — they're not actionable today)*

### Step 4 — Configure visible fields

Show **only** these fields on the record card:

| Field | Why |
|-------|-----|
| Product Name | Primary identifier |
| Product Line | Color-coded — instant visual scan |
| Target Date | What's due |
| Docx Built ✓ | Stage gate: is the build done? |
| QC Passed ✓ | Stage gate: is it clean? |
| TPT Listed ✓ | Stage gate: is it live? |
| Pinterest Status | New field — where is this in pin rotation? |

Hide everything else. You can always click into a record to see all fields.

### Step 5 — Add a filter

Add a filter so Idea-stage records from the full 30+ record list don't clutter the view:

- Filter: `Workflow Stage` **is not** `Idea`

*(Or keep Idea in — just collapsed at the bottom. Dealer's choice.)*

### Step 6 — Configure the record detail panel

When you click into a record from the Interface, you want to see the relevant fields for that stage. Set the detail panel to show:

- Product Name, Product Line, Workflow Stage, Target Date
- Milestone checkboxes: Docx Built, QC Passed, Preview PDF ✓, Canva Cover ✓, TPT Listed ✓
- Pinterest fields: Pinterest Status, Pinterest URL, Pinterest First Pin Date, Pinterest Pin Count, Canva Pin Design ID
- Social: Instagram ✓, Facebook ✓, In Bundle ✓
- Notes

### Step 7 — Set as your default view

1. In Interfaces, click the **⋯** menu on the Launch Runway interface
2. Set as **default interface** — this is what opens when you click Interfaces from now on

### Optional: Add a second component — Marketing Gaps filter

Below the Record List, add a second **Record List** component with:
- Same data source: Products table
- Filter: `TPT Listed ✓` = true AND `Pinterest URL` is empty
- Title: `⚠️ Pinnable but Not Pinned`
- Fields: Product Name, Product Line, Pinterest Status, Canva Pin Design ID

This surfaces the exact list the daily brief needs — products live on TPT with no pin yet — directly in your morning Interface without running a script.

---

## 3. Weekly Base Hygiene Scheduled Task

**Status: CREATED ✓** — Task ID: `cbd-base-hygiene`

**Schedule:** Every Friday at 8:03 AM (runs after the Pinterest brief at 8:00 AM)

**What it checks:**
- Live products with no Pinterest Pin URL (blocks daily brief)
- TPT-listed products with no Canva Image 1 Share URL (blocks Tailwind CSV)
- Pinterest ✓ checkbox / Pinterest URL mismatches (auto-corrects these)
- Live products missing Canva Pin Design ID (blocks fresh-pin rotation)
- Vocabulary table: words with empty Word Type, Core words missing Core Tier tag

**Output:** Report file saved to `_Operations/Hygiene Reports/CbD_Base_Hygiene_[YYYY-MM-DD].md` — a new folder that will be created on first run.

**⚠️ Pre-approve tools before first auto-run:**
Open Scheduled Tasks sidebar → find `cbd-base-hygiene` → click **Run now** to pre-approve the Airtable MCP tool. Future Friday runs will then fire without pausing for permission prompts.

**Report format:** Three-tier (🔴 Blocking / 🟡 Needs Attention / 🔵 Vocabulary) so you know at a glance what requires action before Monday.

---

## Reference: Field IDs Updated After These Changes

| Field | Table | Field ID | Status |
|-------|-------|----------|--------|
| Pinterest URL | Products | fldx9FesXwfqZhWYp | Existing — data field |
| Pinterest ✓ | Products | fldhVp0lOxQaB9PUB | Existing — checkbox (now auto-set by automation) |
| Pinterest Status | Products | *add ID here after creation* | NEW — trigger/status field |
| Pinterest First Pin Date | Products | fldwrWqdlHarNopcD | Existing |
| Pinterest Pin Count | Products | fld0w7mq9rfixZ5n9 | Existing |
| Canva Image 1 Share URL | Products | fldYDDTNbdlE8AfNv | Existing |
| Canva Pin Design ID | Products | fldIzVfpce6fDpV7x | Existing |

---

*Created: 2026-04-18 | Source: Airtable audit session*

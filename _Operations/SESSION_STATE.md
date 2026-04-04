# CbD Session State
**Last updated:** 2026-04-03
**Read this file FIRST at every session start — before doing any work.**

---

## ⛔ iCloud Mount Check — MUST PASS BEFORE ANY WORK
Run: `ls "/sessions/relaxed-stoic-goodall/mnt/Communicate by Design/"`

**If it fails → FULL STOP. Do not proceed. Do not work from memory. Do not answer product questions.**

Tell Jill: "The Communicate by Design folder is not mounted. We need to fix this before starting."

Diagnose:
- Run `ls /sessions/relaxed-stoic-goodall/mnt/` — what is mounted?
- If folder is missing: Jill needs to reopen Cowork and re-select the Communicate by Design folder
- If folder is there but empty/stale: iCloud may not have synced — check System Settings → Apple ID → iCloud → wait for sync, then retry
- Do NOT start work until this check passes and SESSION_STATE.md is readable

---

## What Is Live on TPT (Authoritative — check Airtable Products table to confirm)
| Product | Status | Price | Notes |
|---------|--------|-------|-------|
| IEP AT Consideration Toolkit | LIVE | $4.00 | — |
| AAC Communication Data & Trackers | LIVE | $3.00 | — |
| AAC Communication Partner Quick Guide | LIVE | $3.00 | — |
| IEP AT Consideration Checklist | LIVE FREE | FREE | — |
| Finding Symbols for AAC Visual Support | LIVE FREE | FREE | — |
| Visual Schedule Template Pack | LIVE | $4.00 | — |
| Universal AAC Data Tracker | LIVE FREE | FREE | — |
| AT & AAC Toolkit Bundle | LIVE | $10.00 | — |
| Keiko: A Whale's Journey | LIVE | $9.95 | v2 cover uploaded ✓ Apr 3 |
| All the Way to the Top Companion | LIVE | $5.00 | Listed Apr 4 2026 · TPT ID: 15979429 · ⚠️ Run sync_vocab_to_airtable.js · ⚠️ Add Pinterest pin |
| Radium Girls | LIVE | $11.95 | v2 cover uploaded ✓ Apr 3 |
| Zitkala-Ša | LIVE | $9.95 | v2 cover uploaded ✓ Apr 3 |
| 504 Sit-In | LIVE | $11.95 | v2 cover uploaded ✓ Apr 3 |
| Frances Kelsey | LIVE | $11.95 | v2 cover uploaded ✓ Apr 3 |
| Capitol Crawl 1990 | LIVE | $9.95 | v2 cover uploaded ✓ Apr 3 |
| Wonder – Character Analysis | LIVE | TBD | Pricing + cover color not yet locked |
| Nonfiction Bundle — Keiko + Radium Girls | LIVE | $18.00 | Needs cover + Pinterest |

## Built But NOT Yet Listed on TPT
| Product | Status | Blocker | Next Step |
|---------|--------|---------|-----------|
| UFLI AAC Companion — Lessons 1–5 FREE | Content blocker | Formatting/consistency issues across lesson packets | Resolve consistency → list FREE |
| UFLI AAC Companion — Lessons 6–34 + Guide $20 | Content blocker | Same consistency issue | Resolve consistency → list $20 |
| Poetry Unit 1 — What the Voice Carries | QC PASSED ✓ | Jill: re-export PDF from Word | PDF → GitHub → Canva cover export → TPT listing |

---

## Key Decisions Made (Do Not Re-Litigate)
- UFLI pricing LOCKED: FREE (Lessons 1–5) / $20 (Lessons 6–34). Old $1/lesson pricing RETIRED.
- UFLI covers: ✓ DONE in Canva. Pinterest/reel: ✓ Linked. Blocker is content consistency, not covers.
- Poetry color LOCKED: docs = #6B21A8 / digital = #C084FC
- Fiction color: TBD
- "NON-SPEAKING" is NOT CbD language — use "complex communicators" or "students who use AAC"
- Year 1 goal = drive traffic to TPT store. This is the direction, not a question.
- Dashboard location = `_Operations/Dashboards/` only. Never create a new one elsewhere.
- Sub-brand for trading cards = CbD Card Collection (Year 2 / 2027 — not in 2026 tracking)
- AAC Trading Cards = Year 2/2027 ONLY. Do not surface in 2026 dashboards, tasks, or KPIs.

---

## Folder Structure — AUTHORITATIVE PATHS (Updated 2026-04-03)
```
_Operations/
├── Build/                        ← ALL shared build scripts
│   ├── cbd_docx_template.js      ← docx template
│   ├── cbd_unit_vocab.js         ← vocabulary data (all non-UFLI product lines)
│   ├── fitzgerald_key.js
│   ├── sync_vocab_to_airtable.js ← run at BUILD TIME, not TPT listing
│   ├── build_all_previews.py     ← TPT preview PDFs (nonfiction)
│   ├── build_all_units.py        ← CAP all 6 nonfiction units
│   └── [all other shared scripts]
├── Dashboards/                   ← ALL dashboards — never loose in root
│   ├── CbD_Launch_Dashboard.html
│   ├── CbD_Task_Dashboard.html
│   ├── CbD_Workflow_Visual.html
│   └── CbD_Vocabulary_Dashboard.html  ← NEW Apr 3
├── Symbols/                      ← AUTHORITATIVE — never duplicate
│   ├── symbol_library/           ← 400 symbols
│   └── symbol_cache/             ← 741 ARASAAC PNGs
├── _Shared_Inserts/              ← About, Accessibility, Terms docx
├── memory/                       ← reference .md files
├── QC/
├── SESSION_STATE.md              ← THIS FILE — read first every session
└── node_modules/                 ← shared — do NOT duplicate in product folders
```

**⚠️ Path rules — NEVER guess, NEVER use old paths:**
- Symbol library → `_Operations/Symbols/symbol_library/` (NOT `_Operations/symbol_library/`)
- Symbol cache → `_Operations/Symbols/symbol_cache/` (NOT `_Operations/symbol_cache/`)
- Build scripts → `_Operations/Build/[script]` (NOT `_Operations/[script]`)
- Dashboards → `_Operations/Dashboards/[file]` (NOT anywhere else)
- Vocab data → `_Operations/Build/cbd_unit_vocab.js`

**⚠️ Manual cleanup still needed (iCloud locked — Jill does in Finder):**
- Delete `Products/UFLI Phonics/symbol_library/` (duplicate — use `_Operations/Symbols/`)
- Delete `Products/UFLI Phonics/node_modules/` (use `_Operations/node_modules/`)
- Delete `Products/Poetry Reading Units/Unit 1/node_modules/` (use `_Operations/node_modules/`)

---

## Active Build Rules (Read Before Any Build)
- Template: `_Operations/Build/cbd_docx_template.js`
- Shared builders: `_Operations/Build/`
- Symbol library: `_Operations/Symbols/symbol_library/`
- Symbol cache: `_Operations/Symbols/symbol_cache/`
- Vocab data: `_Operations/Build/cbd_unit_vocab.js` — all non-UFLI product lines
- Nonfiction require path: `path.join(__dirname, "..", "..", "..", "_Operations", "Build", "cbd_docx_template")`
- Poetry require path: same 3-level pattern from unit folder into `_Operations/Build/`
- Fiction require path: same 3-level pattern from unit folder into `_Operations/Build/`
- PDF export: Word → File → Save As → PDF only. Never LibreOffice, never Print to PDF.
- Dashboards: read existing file in `_Operations/Dashboards/` — NEVER create a new one
- About/Accessibility/Terms: read from `_Operations/_Shared_Inserts/` — NEVER rewrite from scratch
- Vocab sync: run `sync_vocab_to_airtable.js` at BUILD TIME after framework gates — not at TPT listing
- Skip `pendingBuild: true` stubs in vocab sync — words must be confirmed first

---

## Dashboard Auto-Refresh Log
- **Last dashboard refresh:** Apr 4 2026 (scheduled task: cbd-dashboard-refresh — automated run, second pass)
- **Products Live count:** 16 (Nonfiction: 6 · AT/AAC IEP Team: 7 · Bundles: 2 · Picture Book: 1) — unchanged from prior run
- **Vocab DB count:** 773 (Core: 192, Fringe: 581 · UFLI: 605, Nonfiction: 160, Fiction: 24) — unchanged, confirmed match
- **Work Items pulled:** 133 total · High-priority not-done: 43 items
- **Status changes detected this run:**
  - Alert banner refreshed: removed 504 Sit-In cover upload (confirmed uploaded Apr 3 per Products Notes) · replaced with Vocabulary Core Tier tagging task
  - 504 Sit-In cover confirmed UPLOADED in Products table Notes (Apr 3 2026) — alert banner updated accordingly
  - Keiko cover still ⚠ pending TPT upload (cover file: CbD_Cover_Keiko_v2.png in Brand Assets/Nonfiction Lesson/TPT Image Cover Pending/)
  - 4 new tasks added to Task Dashboard (ids 45–48): Vocab Core Tier tagging · Vocab Product Lines fix · Pinterest Family board · Substack Profile Rewrite
  - Units In Progress KPI updated: Picture Book now shows "6 Picture Book ↗" (1 live + 5 in build)
  - Vocabulary Dashboard footer date updated to Apr 4 2026
  - Workflow Visual footer updated to note Apr 4 2026 auto-refresh
- **Airtable pull results:** Products (39 records) · Work Items (133 records) · Launch Pipeline (83 records) · Vocabulary (773 records)
- **No Airtable errors this run**

---

## What Changed This Session (2026-04-04 — Picture Book Pipeline + Canva CSV)
- **Picture Book pipeline research complete** — `Research/CbD_PictureBook_Pipeline_Research.md` built: 28 title candidates, 4-gate selection framework, priority scoring, TPT SEO gap analysis (zero competition confirmed for 5 titles: A Friend for Henry, I Talk Like a River, Ian's Walk, Emmanuel's Dream, My Friend Isabelle).
- **5 new picture book companion build scripts written** — `build_symbol_pages_picbook.py` (symbol pages + comm board) created for all 5 titles. Each script: unit-specific vocabulary, FK overrides, same architecture as All the Way to the Top. Saved in `Products/Picture Book Companions/[Title]/`.
- **Canva bulk import CSV created** — `Distrubution/Pinterest/PB_Companions_Canva_BulkImport.csv` — 6 rows (all 6 companions), 8 columns: book_title, series_label, skill_focus, skill_short, standards, grade_band, hook_text, tpt_tag. Ready for Canva bulk image creation of all 6 pins.
- **5 new Airtable Products records created** — A Friend for Henry, I Talk Like a River, Ian's Walk, Emmanuel's Dream, My Friend Isabelle — all status: Building, price: $5, product line: Picture Book Companions.
- **⚠️ Pending for all 5 new titles:** Teacher Packet docx build · Student Activities · Welcome Packet PDF · assembled Student COMPLETE · TPT Preview · Canva cover export · TPT listing.

## What Changed This Session (2026-04-03 — Picture Book Companion build)
- **All the Way to the Top Companion — BUILD COMPLETE** — Full file set delivered: Welcome Packet (2pp) · Teacher Packet (9pp, Word export) · Student COMPLETE (12pp assembled) · Communication Board (1pp) · Symbol Pages (2pp) · TPT Preview (10pp). Airtable record created: `recPx1oIQOMEUBP9E` (Ready to List). TPT listing package with Output 0 delivered. Tax code: Digital Images - Streaming / Electronic Download. Price: $5. Target list date: July 26 2026 (ADA anniversary).
- **Symbol pages hard rule LOCKED** — Symbol pages for picture book companions are Python/ReportLab ONLY (`build_symbol_pages_picbook.py`). Never inside `.js` docx build. Card spec locked: symbol + ALL CAPS label + FK border only — no category bars, no star, no POS labels. Documented in `build_system_reference.md` + `PictureBook_Companion_QC_Checklist.md` with hard blocking gates.
- **`buildSymbolCardsSection()` removed from `build_all_the_way_to_the_top.js`** — function call removed from `studentChildren`; comment added explaining Python-only rule.
- **New build scripts created:** `build_symbol_pages_picbook.py` (symbol pages + comm board) · `build_welcome_packet.py` (welcome PDF matching Wonder layout).
- **Communication board built** — FK-colored cell backgrounds (SGD topic page layout), 4-col × 5-row, canvas-based Python/ReportLab, ARASAAC attribution footer.
- **Jennifer Keelan bundle** — Pair "All the Way to the Top" ($5) + Capitol Crawl ($9.95) for Disability Pride Month July 2026.
- **⚠️ Pending Jill actions added:** Upload to TPT after Canva cover is done · Run sync_vocab_to_airtable.js after listing · Update Airtable to Live · GitHub push for session build scripts.

## What Changed Previous Session (2026-04-03 — continuation)
- **4 dashboards** now linked as a suite: Operations, Tasks, Workflow, Vocabulary
- **CbD_Vocabulary_Dashboard.html** created (NEW) — vocabulary framework reference, Airtable field map, Fitzgerald Key, unit word tables
- **cbd-dashboard-refresh** scheduled task created — runs 8:15 AM, noon, 11:30 PM daily — pulls Airtable → updates all 4 dashboards
- **cbd_unit_vocab.js** updated — added Poetry Unit 1 vocabulary (28 words), Picture Book Companion vocabulary (18 words), Fiction Units 2–6 as pending stubs
- **sync_vocab_to_airtable.js** updated — now handles Poetry Reading Unit, Picture Book Companion product lines; skips pendingBuild stubs; Picture Book and Poetry added to UNIT_TITLE_MAP
- **UFLI status corrected** — covers ✓ done, blocker is content consistency (not covers)
- **504 Sit-In + Capitol Crawl v2 covers** — marked uploaded ✓ Apr 3 and removed from all dashboard alerts/priority lists
- **CLAUDE.md folder structure** — corrected to show new paths (Build/, Dashboards/, Symbols/); fixed build_all_previews.py path
- **Hard rules added to CLAUDE.md** — vocab sync timing, Trading Cards Year 2, completed tasks must be cleared immediately

## What Changed Previous Session (2026-04-03 — earlier)
- Poetry Unit 1 QC PASSED — 4 issues fixed
- UFLI pricing restructured (two products, new prices)
- Folder restructure: Build/ and Symbols/ created in _Operations
- All shared build scripts moved to _Operations/Build/
- All dashboards consolidated to _Operations/Dashboards/
- SESSION_STATE.md created

---

## Pending Jill Actions
- [ ] Re-export Poetry COMPLETE.docx → PDF from Word (existing PDF is LibreOffice — violates CbD rule)
- [ ] Push Poetry to GitHub after PDF re-export
- [ ] Export Poetry Canva cover (DAHFebI7Z2k) → TPT listing
- [ ] Resolve UFLI formatting/consistency issues across lesson packets
- [ ] Delete duplicate symbol_library and node_modules from Finder (iCloud locked — 3 folders)
- [ ] Wonder: confirm pricing ($8.95/$9.95) and cover color before TPT listing
- [ ] Run `cbd-dashboard-refresh` task once manually to pre-approve Airtable tool permissions

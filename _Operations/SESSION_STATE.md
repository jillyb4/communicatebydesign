# CbD Session State
**Last updated:** 2026-04-11 (Session — UDL 3.0, Build Lock, Worksheet Template System)
**Read this file FIRST at every session start — before doing any work.**

---

## What Changed This Session (2026-04-12 — TPT Taxonomy Locked in Airtable)

- **TPT Tag Grid rebuilt** — `Distrubution/Teachers Pay Teachers/CbD_TPT_Tag_Grid.html` and `_Operations/Dashboards/CbD_TPT_Tag_Grid.html` (both in sync). All 23 products assigned Subject Area, Tags, Custom Categories using ONLY verified TPT screenshot values. Hard rule documented at top of grid: never invent, rename, or add options.
- **Airtable TPT Format field (`fldB9lPPVDht1pW8D`) — CORRECT** — 22 verified options matching TPT Format dropdown exactly (Audio, Digital: Boom Cards, Digital: Canva, Digital: Prezi, Digital: Seesaw, Digital: Other (Digital), Easel: Easel Activities, Easel: Easel Assessments, eBook, Fonts, Google Apps, Image, Interactive Whiteboards: Activboard Activities, Interactive Whiteboards: ActiveInspire Flipchart, Interactive Whiteboards: SMART Notebook, Microsoft: Microsoft Excel, Microsoft: Microsoft OneDrive, Microsoft: Microsoft PowerPoint, Microsoft: Microsoft Publisher, Microsoft: Microsoft Word, PDF, Video). Do not touch.
- **Airtable TPT Tags field (`fldA8BMhXXrDkrjji`) — OLD, singleLineText — DELETE MANUALLY** — Was a plain text field, cannot hold dropdown choices. New field created: **`TPT Tags (NEW)` (`fldGl1bOucir0OQZO`)** — multipleSelects, 129 exact TPT Tag options (Audience, Language, Programs & Methods, Resource Type, Supports, Specialty, Speech Therapy, Theme/Holiday, Theme/Seasonal). After deleting old field, rename new field to "TPT Tags."
- **Airtable TPT Subject Areas field (`fldDXxOjBk4YZJyfF`) — STILL HAS INVENTED VALUES** — Current bad values: English Language Arts, Special Education, Speech Therapy, Life Skills, Social Skills, Phonics, Vocabulary. These do not exist in TPT's Subject Area dropdown. ⚠️ Needs to be replaced with full verified TPT Subject Area list (see Key Decisions below).
- **HARD RULE established and documented:** Airtable TPT fields (Subject Areas, Tags, Format, Custom Categories) must contain ONLY exact strings from TPT's dropdown UI. Never invent, abbreviate, or rename. Screenshots are the source of truth.

## What Changed Previous Session (2026-04-11 — Research Library + Weekly Scan)

- **Airtable Research Library created:** New table `tblKpzHsm4HHe3qsa` in base `appeaT8hkeXWqQKIj`. Fields: Title, Authors, Year, Journal/Source, DOI/URL, Topic Area (15 multiselect tags), Key Findings, CbD Application, CbD File, Full Text Access, Used in Substack, Used in Product, Date Added.
- **10 existing research files migrated to Airtable:** All research from `Research/` folder inventoried and logged. Includes Romano et al. 2026 (LSHSS writing/AAC study — paywalled, email sent to Nicole Romano 4/11/2026), Spencer & Petersen 2020, OpenAAC State of AAC 2026, UFLI framework, AAC phonics/literacy, core vocabulary, alternative pencils, picture book companions, poetry units, and i-Ready concerns.
- **Weekly Research Scan scheduled:** Task `cbd-research-scan` runs every Monday at 7:30 AM. Searches PubMed + key journals for new AAC/literacy/writing/complex communicators research, checks for duplicates, logs new articles to Airtable, saves scan summary to `Research/WeeklyScans/scan_[date].md`, and creates a Gmail draft summary to jillyb4@gmail.com.
- **⚠️ Action needed:** Click "Run now" on `cbd-research-scan` in Scheduled sidebar to pre-approve tools before first automated run Monday 4/14.
- **Romano et al. 2026 email draft:** Gmail draft created to Nicole Romano (Penn State CSD) requesting full text of writing/AAC article. Jill needs to add Nicole's email address before sending.

## What Changed Previous Session (2026-04-11 — Worksheet Template System v2.1 Complete)

- **`cbd_worksheet_templates.py` v2.1 — COMPLETE AND COMMITTED** — All 8 templates locked and tested. Word bank implemented on `make_short_answer_page()` and `make_cer_page()`. Sentence frame convention locked (use `...` or `:`, never single `___` blank). "Key Words" label (not "Word Bank"). Design is modality-neutral: no access method instruction anywhere.
- **Version differentiation rule locked:** V1/V2/V3 differences use the SAME template functions with different content params — NOT separate template functions. `word_bank=None` = V1/V2. `word_bank=[...]` = V3 only. Words must come from CAP, not introduce new vocabulary.
- **`build_system_reference.md` updated:** Version Differentiation section added with code examples. Sentence frame hard rule documented with ✓ / ✗ examples.
- **CLAUDE.md updated:** Full Student Worksheet Template System section locked.
- **GitHub committed:** `cbd_worksheet_templates.py` v2.1 committed to main. Open GitHub Desktop → push origin.
- **Manual cleanup still needed (iCloud permissions block sandbox deletion):**
  - Delete from Finder: `_Operations/Build/cbd_worksheet_demo.pdf`
  - Delete from Finder: `_Operations/Build/cbd_worksheet_templates_v2_demo.pdf`
  - Delete from Finder: `_Operations/Build/cbd_word_bank_test.pdf`
  - Delete from Finder: `_Operations/Build/cbd_keywords_test.pdf`
  - Delete from Finder: `_Operations/Build/__pycache__/` folder

## What Changed Previous Session (2026-04-11 — UDL 3.0, Build Lock, Worksheet Template System)

- **UDL Guidelines updated to v3.0:** All frameworks now cite `CAST. (2024). UDL Guidelines v3.0`. Authoritative citation in CLAUDE.md. PDF filed: `Research/CAST_UDL_Guidelines_3.0_WithNumbers.pdf`. Full alignment map: `Research/CbD_UDL_Alignment_Map.md`.
- **Build Lock established:** Nonfiction Units 1–6 and PB Companions 1–6 are LOCKED. No rebuilds. Improvements apply forward only (Unit 7+ and PB Companion 7+). Rule documented in CLAUDE.md "Build Lock Rule" section.
- **Student Worksheet Template System created:** `_Operations/Build/cbd_worksheet_templates.py` v2.1 — ReportLab PDF templates for all student activity pages. ALL new units use this. Locked design: modality-neutral (no access method instruction), print-first, no fills in response areas.
  - Templates: MCQ, Short Answer, CER, Evidence Sort, Vocab Preview, Annotation Guide
  - Philosophy: worksheets don't say HOW to respond — sentence frames + CAP carry access load
  - Both key formats accepted (stem/options OR text/choices, prompt/sentence_frame OR text/frame)
  - Symbol size locked: `SYM_SIZE = 88` pts
- **New-unit trigger documented:** Phase 1 Gate now requires `cbd_worksheet_templates.py` checkbox for student activity pages. Trigger applies to: Nonfiction Unit 7+, PB Companion 7+, Fiction Unit 2+, Poetry Unit 2+, all UFLI new builds.
- **`build_system_reference.md` updated:** v2.1 spec, corrected design rules, integration workflow.
- **.gitignore updated:** Added `__pycache__/`, `*.pyc`, `*_demo.pdf` exclusions.
- **Manual cleanup needed (iCloud permissions block sandbox deletion):**
  - Delete from Finder: `_Operations/Build/cbd_worksheet_demo.pdf`
  - Delete from Finder: `_Operations/Build/cbd_worksheet_templates_v2_demo.pdf`
  - Delete from Finder: `_Operations/Build/__pycache__/` folder

---

## What Changed Previous Session (2026-04-10 — Skill Update)

- **Business Plan created:** `CbD_Business_Plan_April2026.docx` — 8 sections, full financial model (Low $2,880 / Base $9,000 / High $20,200 net), 6-week launch metrics captured, 90-day roadmap.
- **Skill file updated:** Rebuilt `communicate-by-design-updated.skill` (60 KB). Four stale reference files corrected:
  - `fiction.md` — Wonder LIVE ($6, TPT 15945146), pricing locked, 6-unit set documented
  - `products.md` — Wonder + Poetry Unit 1 LIVE, Fiction + Poetry pricing tables added, Substack 5 posts with URLs, paid tier strategy
  - `substack.md` — Posts 4+5 LIVE, Post #6 pipeline, paid tier ($8/mo or $80/yr at 200 subscribers)
  - `picture-book-companions.md` — 1 LIVE + 5 built, 3-file architecture, LibreOffice PDF rule, all 6 titles with IDs
- **Skill file saved to workspace:** `Communicate by Design/communicate-by-design-updated.skill` — double-click to install

---

## ⛔ iCloud Mount Check — MUST PASS BEFORE ANY WORK
Run: `ls "/sessions/[current-session-id]/mnt/Communicate by Design/"`

**If it fails → FULL STOP. Do not proceed. Do not work from memory. Do not answer product questions.**

Tell Jill: "The Communicate by Design folder is not mounted. We need to fix this before starting."

Diagnose:
- Run `ls /sessions/[current-session-id]/mnt/` — what is mounted?
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
| All the Way to the Top Companion | LIVE | $5.00 | Listed Apr 4 2026 · TPT ID: 15979429 · Vocab synced ✓ |
| Radium Girls | LIVE | $11.95 | v2 cover uploaded ✓ Apr 3 |
| Zitkala-Ša | LIVE | $9.95 | v2 cover uploaded ✓ Apr 3 |
| 504 Sit-In | LIVE | $11.95 | v2 cover uploaded ✓ Apr 3 |
| Frances Kelsey | LIVE | $11.95 | v2 cover uploaded ✓ Apr 3 |
| Capitol Crawl 1990 | LIVE | $9.95 | v2 cover uploaded ✓ Apr 3 |
| Wonder — Fiction Anchor Text Unit | LIVE | $6.00 | LIVE Apr 2026 · TPT ID: 15945146 · Price LOCKED $6 |
| Poetry Unit 1 — What the Voice Carries | LIVE | $9.95 | LIVE Apr 10 2026 · TPT ID: 16037413 · ⚠️ Pinterest 3 pins + IG + FB pending |
| Nonfiction Bundle — Keiko + Radium Girls | LIVE | $18.00 | TPT ID: 15922531 · Needs Pinterest pin |

## Built But NOT Yet Listed on TPT
| Product | Status | Blocker | Next Step |
|---------|--------|---------|-----------|
| UFLI AAC Companion — Lessons 1–5 FREE | Content blocker | Formatting/consistency issues across lesson packets | Resolve consistency → list FREE |
| UFLI AAC Companion — Lessons 6–34 + Guide $20 | Content blocker | Same consistency issue | Resolve consistency → list $20 |


---

## Strategic Priorities (Locked Apr 10 2026)
1. **TPT Product Lines** — primary revenue driver. All product builds, listings, and launches are #1.
2. **Substack** — #2. Goal: **200 followers to unlock paid monthly subscriber feature.** Every post + FB drop must actively drive toward this number. Check follower count at start of each Substack session.

## Key Decisions Made (Do Not Re-Litigate)
- **TPT taxonomy fields in Airtable (LOCKED 2026-04-12):** Subject Areas, Tags, Format, Custom Categories must use ONLY exact TPT dropdown strings from screenshots. No inventing, abbreviating, or renaming. TPT Tag Grid HTML is the authoritative reference doc. Format field is correct (22 options). Tags (NEW) field created with 129 options — delete old singleLineText TPT Tags field and rename TPT Tags (NEW) → TPT Tags. Subject Areas still needs old invented values removed.
- **Verified TPT Subject Area options (from screenshots):** ELA: Reading · Literature · Poetry · Writing · Vocabulary · Spelling · Writing-Expository · Writing-Essays · Other (ELA) | Social Emotional: Social Emotional Learning · Character Education · Classroom Community · School Counseling · School Psychology | Social Studies: U.S. History · Native Americans · Black History · AAPI History · African History · Ancient History · Asian Studies · Economics · Elections - Voting · European History · Geography · Government · Latino and Hispanic Studies · Middle Ages · Psychology · Religion · World History · Australian History · British History · Criminal Justice - Law · Other (Social Studies) | Science: Environment · Anatomy · Archaeology · Astronomy · Basic Principles · Biology · Chemistry · Computer Science - Technology · Earth Sciences · Engineering · Family Consumer Sciences · Forensics · General Science | Math (full list confirmed) | World Languages (full list confirmed) | For All Subjects · Not Subject Specific
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
│   ├── CbD_Vocabulary_Dashboard.html  ← NEW Apr 3
│   └── CbD_Skills_Dashboard.html       ← NEW Apr 10 (Skills & grade band coverage)
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
- **Last dashboard refresh:** Apr 4 2026 (scheduled task: cbd-dashboard-refresh — automated run, third pass)
- **Products Live count:** 16 (Nonfiction: 6 · AT/AAC IEP Team: 7 · Bundles: 2 · Picture Book: 1) — confirmed via Airtable Products table
- **Vocab DB count:** 773 (Core: 192, Fringe: 581) — confirmed via Airtable Vocabulary table full pull
- **Work Items pulled:** 133 total · High-priority not-done: 43 items active
- **Status changes detected this run (third pass):**
  - Alert banner refreshed: Autism Acceptance Month tags (overdue Apr 1) + Canva pins AT Toolkit/Comm Partner Guide (overdue Apr 3) + Pinterest logo + Keiko v2 cover as top 4 items
  - Priority Actions section refreshed: consolidated Apr 8 tasks, combined Apr 10 tasks, maintained 9 rows
  - 4 new tasks added to Task Dashboard (ids 49–52): Capitol Crawl v2 cover uploaded ✓ (Done) · 504 Sit-In v2 cover uploaded ✓ (Done) · 504 Sit-In Preview PDF (Jun 1 deadline) · Substack #6 IEP Goals (Apr 8)
  - CbD_Workflow_Visual.html — no changes needed (already current, Apr 4 2026 date confirmed)
  - CbD_Vocabulary_Dashboard.html — no changes needed (773 words confirmed, Apr 4 2026 date confirmed)
- **Airtable pull results:** Products (39 records) · Work Items (133 records) · Vocabulary (773 records) · Launch Pipeline: not pulled this pass
- **Airtable errors:** Work Items filter failed (unknown column name — pulled all and filtered locally); Vocabulary fieldId required table schema lookup — resolved

---

## What Changed This Session (2026-04-10 — Business Plan Synthesis)

- **CbD_Business_Plan_April2026.docx CREATED** — Unified business plan synthesizing 5 source documents: Product Update & Launch Strategy (Mar 24) · Business Model Overview (Apr 3) · Revenue Analysis Prompt · 6-Week Launch Analysis HTML (Apr 10) · Business Budget xlsx. Saved to root of Communicate by Design folder. 8 sections: Who We Are · Product Lines · Instructional Frameworks · Distribution & Marketing · Launch Performance (real metrics) · Financial Model · 90-Day Roadmap · Partnerships. Styled in full CbD brand (Navy/Teal/Amber). This is now the authoritative single business plan document.
- **Financial model captured** — Low/Base/High 12-month projection: Low $2,880 / Base $9,000 / High $20,200 net. Revenue scorecard included (7 dimensions). Key assumption: base case requires FB group strategy activated + UFLI launch executed + 2–3 TPT reviews earned by July.
- **6-Week launch metrics locked** — As of Apr 10: $1.35 YTD revenue · 23 products live · 93 TPT views · 11 wishlist adds (11.8% rate) · 1,366 Pinterest impressions · 5 outbound clicks · 1,900 FB views · 2 Substack subscribers. Pinterest is fastest-moving channel (4 outbound clicks from Picture Book board in 5 days). Zero TPT reviews is #1 conversion blocker.
- **Key action confirmed** — Drop Post #5 FB group link TODAY. Email one buyer for review TODAY. These two actions are highest ROI with zero build time.

## What Changed This Session (2026-04-10 — Dashboard Audit + Skills Dashboard)

- **All 5 dashboards fully audited and updated** — Operations, Tasks, Workflow, Vocabulary, Skills all current as of Apr 10 2026.
- **Operations Dashboard:** KPI corrected to 23 products live. All 6 Picture Book Companions now listed in product table (was only showing 1). KPI breakdown updated. Keiko v2 cover warning removed. Notes column is now forward-looking only.
- **Skills Dashboard (NEW `CbD_Skills_Dashboard.html`):** Poetry Reading Units section converted from card layout to proper grade-band table (K–10 columns, ✓ marks per grade). Picture Book Companions section added entirely (section header, grade-band table K–3, 6 titles, KPI card, Standards Crosswalk column). 6th KPI card added.
- **Picture Book Companions badge corrected:** "1 live · 5 built" → "6 live" across Skills Dashboard and Operations Dashboard.
- **Vocabulary count confirmed 641** — all sync warnings removed from all dashboards. Airtable Work Item created.
- **CLAUDE.md updated:** TPT store 23 products, Poetry row rewritten to LIVE, Wonder row updated to LIVE, vocab table updated to 641 synced, Skills Dashboard added to folder structure.
- **TASKS.md updated:** Vocab sync marked done, Skills Dashboard completion logged, new task added to update `cbd-dashboard-refresh` scheduled task prompt.
- **⚠️ Pending Jill actions from this session:** Pinterest 3 pins + IG carousel + FB post for Poetry Unit 1 · FB group drop for Substack Post #5 · Update `cbd-dashboard-refresh` task prompt (knows about Poetry LIVE + 641 vocab + Skills Dashboard).

## What Changed This Session (2026-04-10 — Substack Post #5 Published)

- **Substack Post #5 LIVE** — "Who Gets to Decide If the Voice Is Real?" published April 10, 2026. URL: https://communicatebydesign.substack.com/p/who-gets-to-decide-if-the-voice-is. Pillar: 🔴 Policy & Advocacy. Topic: facilitated spelling skepticism, presuming competence of student AND partner, ASL interpreter analogy, partner training standards, evidence double standard for low-tech vs. partner-supported AAC. Personal: Jill's daughter (Tobii eye gaze, 13 yrs speech therapy) questioned by adults AND peers. *Out of My Mind* / Whiz Kids scene as anchor. Draft saved: `Substack/Substack_Draft_WhoGetsToDecide_Voice.md`.
- **Airtable Work Item created** — Record `recOmsKtrwrGpNqq9` (Status: Done, Type: Content, Priority: High, Category: Operations).
- **CLAUDE.md updated** — Substack pipeline now shows 5 live posts. Jennifer Keelan age corrected to 9 (was 8).
- **TASKS.md updated** — Post #5 marked done. Two follow-up tasks added: FB group drop + Canva photo overlay quote.
- **⚠️ Pending Jill actions (from this session):** Drop post link in 2–3 SPED Facebook groups · Make Canva photo overlay quote (navy bg, "The voice is there. The question is whether we've decided to hear it.").

## What Changed This Session (2026-04-08 — Nonfiction Symbol Pages + AAC Section Fixes)

- **Nonfiction symbol pages built for all 6 units** — New gold-standard symbol pages PDF (`*_Symbol_Pages.pdf`) built for every nonfiction unit using the exact same spec as the picture book companion and Wonder symbol pages (Python/ReportLab, 3-col × 4-row grid, 2"×2" cards, FK-colored border, ARASAAC symbol, ALL CAPS word label — nothing else). Files saved to each unit's `_TPT/` subfolder. Build script: `/sessions/focused-beautiful-johnson/build_nonfiction_symbol_pages.py` (session temp — should be moved to `_Operations/Build/` if permanent).
  - Frances Kelsey: 5 pages (3 core + 2 fringe) — old `Symbol_Cards.pdf` replaced
  - 504 Sit-In: 4 pages (2 core + 2 fringe)
  - Keiko: 5 pages (3 core + 2 fringe)
  - Radium Girls: 5 pages (3 core + 2 fringe)
  - Capitol Crawl: 4 pages (2 core + 2 fringe)
  - Zitkala-Ša: 4 pages (2 core + 2 fringe) — rebuilt after word list fix
- **Old Frances Kelsey `Symbol_Cards.pdf` retired** — Replaced by new `Frances_Kelsey_Symbol_Pages.pdf`. Old file still exists (iCloud permission blocked delete) — Jill: trash `Frances_Kelsey_TPT/Frances_Kelsey_Symbol_Cards.pdf` in Finder.
- **Zitkala-Ša fringe word list corrected** — Build script was missing all Tier 2 structural fringe words. Corrected list: cause, effect, problem, solution, structure, organize, result, evidence, policy, identity, culture + boarding school, assimilation, reservation, hair cutting, spirit, testimony, zitkala, dakota (19 fringe total).
- **Zitkala-Ša `build_zitkala_sa.js` updated** — Added `cbd_aac_support.js` require + replaced old plain-text AAC Support paragraphs + makeTable with proper `AAC.aacSupportSection()` call. Now matches the Radium Girls / Keiko gold standard. DOCX patched in-place (draft file missing — patch applied via python-docx). Old orphan "IEP Goal Stems" heading + 3 plain goal paragraphs also removed from DOCX.
- **504 Sit-In `build_504_sit_in.js` updated** — Added `cbd_aac_support.js` require + replaced old custom AAC Users block (heading2 + bullets + custom makeTable + IEP bullets) with proper `AAC.aacSupportSection()` call using confirmed 504 word lists. Full rebuild ran successfully (draft exists). New DOCX copied to `504_Sit_In_TPT/` folder.
- **Root cause documented** — Zitkala-Ša and 504 Sit-In were built before `cbd_aac_support.js` existed. Both build scripts and DOCXs now match gold standard. ⚠️ Both units need Word → Save As PDF re-export before re-uploading to TPT.
- **⚠️ Pending: move build script to permanent location** — `build_nonfiction_symbol_pages.py` is in session temp (`/sessions/focused-beautiful-johnson/`). Move to `_Operations/Build/build_nonfiction_symbol_pages.py` for permanent access.

## What Changed This Session (2026-04-08 — TPT Discounts + Tailwind Exploration)

- **TPT 10% new follower discount** — Active. Automatically applied when a new buyer follows the CbD store on TPT.
- **TPT Spring Sale — 10% off, one week** — Active sale running for one week. All live products discounted 10%. Note: stacks with new follower discount if applicable.
- **Tailwind for Pinterest** — Jill started exploring Tailwind (tailwindapp.com) as a scheduling/distribution tool for Pinterest. 4 Pinterest fields added to Airtable last session (Pin Title, Pin Description, Alt Text, Canva Media URL) — these will feed Tailwind scheduling workflow. Next step TBD: evaluate Tailwind trial, determine if it replaces or supplements the daily brief task.

## What Changed This Session (2026-04-08 — Airtable TPT ID + Data Audit Cleanup)

- **TPT Product IDs fully populated for all live products** — All 22 live products now have TPT Product ID in Airtable Products table. IDs added this session: Zitkala-Ša (15846486), Radium Girls (15849285), 504 Sit-In (15848748), Keiko (15817061), Frances Kelsey (15849346), Nonfiction Bundle — Keiko + Radium Girls (15922531), AT & AAC Toolkit Bundle (15798556), AAC Communication Partner Quick Guide (15789219), AAC Data Collection Forms (15790089), Visual Schedule Template Pack (15785835), Universal AAC Communication Data Tracker (15922302). Frances Kelsey TPT URL also corrected in Airtable.
- **Wonder marked Live in Airtable** — `fldvrDOZ3rnYGdljl` (TPT Listed ✓) = true, Workflow Stage = Live. TPT Product ID 15945146 confirmed. Wonder is now the first Fiction Anchor Text unit live on TPT.
- **Poetry Unit (What the Voice Carries) Airtable fields fixed** — Learning Target rewritten from raw standard text to student-facing "I can" format: "I can determine the meaning of figurative and connotative language in a poem and analyze how word choices shape meaning and tone." Skill, Standard, SubHeading, and Grade Levels (6th/7th/8th) all populated. Record: `receS8L09qmIxUmcO`.
- **4 new Pinterest fields added to Airtable Products table** — Pinterest Pin Title (`fldQV0iXyTZNZE1bq`), Pinterest Pin Description (`fldBoDY3YOfkBeIfl`), Pinterest Alt Text (`fldQHiO3oo2D10n0a`), Pinterest Canva Media URL (`fldK5T4kf7Oxmv0W9`). All 22 products populated with Pin Title, Pin Description, and Alt Text from Tailwind CSV.
- **Skill/Essential Question/Learning Target populated for all instructional products** — PB Companions (6), Nonfiction (6), Fiction/Wonder, Poetry Unit 1 all now have these fields in Airtable. AT/AAC tool products intentionally left blank (not instructional units).
- **AAC Resource Book List created** — `Research/CbD_AAC_Resource_Book_List.md` — living curation reference, separate from build pipeline. 5 sections, 10 MaiStoryBook titles + key existing titles cross-referenced. Template for ongoing additions.
- **PB Companion pipeline extended to 38 titles** — `Research/CbD_PictureBook_Pipeline_Research.md` updated: new #8 (A Day with No Words) and #9 (This is How We Talk) added as Category A; 8 MaiStoryBook titles added as new Category E (#31–38). Renumbering confirmed clean.
- **A Friend for Henry confirmed FREE (lead magnet)** — $0 price in Airtable is intentional — it is the entry-point freebie for the Picture Book Companions line.
- **Wonder Notes field** — still contains stale "Price TBD ($8.95/$9.95)" text. Price is LOCKED at $6.00. Update Notes field manually or flag for next session.
- **5 AT/AAC products still missing Pinterest URLs** — Products have been pinned (Pinterest ✓ checked) but live pin URLs not yet stored in Airtable `fldx9FesXwfqZhWYp`. Jill action: paste URLs for AAC Data Collection Forms, AAC Communication Partner Quick Guide, Visual Schedule Template Pack, AT & AAC Toolkit Bundle, Finding Symbols Freebie.

## What Changed This Session (2026-04-05 — UFLI Airtable Cleanup + Skill Reference Updates)
- **UFLI Airtable cleanup complete** — 4 old records retired (marked [RETIRED], stage = Retired): UFLI Lessons 5–34 Individual Packets ($1), UFLI Teacher Guide ($5), UFLI Complete Set ($28), UFLI Lessons 5–34 Bundle ($25). 2 new records created: `recCeJ479OD5BEHb5` (FREE, L1–5) + `recas76MabrgRnmL1` (PAID $20, L6–34 + Guide). Both stage: Building, target May 1 2026, Docx Built ✓, QC Passed ✓.
- **TPT Listings doc bugs fixed** — `TPT_Listings_UFLI_AAC_Companion.md`: (1) FREE title trimmed from 81→80 chars (FREE→Free); (2) Lesson 10 label fixed (CVC CVC Practice → CVC Practice); (3) Lesson 11 label fixed (Nasalized A Nasalized /ă/ → Nasalized /ă/); (4) Lesson 19 label fixed (VC & CVC VC & CVC Practice → VC & CVC Practice).
- **Picture Book Companion Canva Cover Link populated in Airtable** — All 6 PB Companion Products records now have `Canva Cover Link` = `https://www.canva.com/design/DAHF6DObHZ4/edit`. Canva cover workflow confirmed locked: text = Lane B (bulk CSV auto-fills), images = Lane A (Jill places manually). Design ID `DAHF6DObHZ4` added to CLAUDE.md Canva Designs table.
- **⚠️ Skill files need manual update on Mac** — `.claude/skills/communicate-by-design/references/products.md` and `references/ufli.md` are read-only in session (iCloud mount). Must update on Mac. Changes needed: UFLI pricing table (retire old, add FREE+$20), UFLI status (covers done, blocker = content consistency), PB Companions section (add 5 new titles + Canva workflow), Substack status (now 4 posts live).

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
- [ ] Wonder: fix Notes field in Airtable — remove stale "Price TBD ($8.95/$9.95)" text. Price LOCKED at $6.00.
- [ ] Wonder: confirm cover color before next session (product is live — cover still TBD)
- [ ] Run `cbd-dashboard-refresh` task once manually to pre-approve Airtable tool permissions
- [ ] Update skill files on Mac (read-only in session): `.claude/skills/communicate-by-design/references/products.md` — fix UFLI pricing (retire old, add FREE + $20) + add PB Companions live section. `references/ufli.md` — fix pricing table + status (covers done, blocker = content consistency).
- [ ] Check `Canva Cover ✓` in Airtable Products for each PB Companion as you finish placing images in Canva bulk template (DAHF6DObHZ4)

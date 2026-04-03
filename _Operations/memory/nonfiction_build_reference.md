# Nonfiction Build Reference

Deep reference for nonfiction unit builds. Pull this file for nonfiction build sessions.

## Standard Nonfiction Unit Sections (all 22 required)

Every nonfiction unit draft (.md) and build script must include ALL of the following:

1. Standards Alignment
2. Unit at a Glance / Pacing Guide (table)
3. Vocabulary Reference (table with terms, first appears, definitions)
4. Vocabulary Preview Routine (5-min routine + priority vocab by lesson)
5. Teacher Support Reference (reading versions table, annotation tools table)
6. Instructional Design Foundations (6 research-based principles)
7. Differentiating for All Learners (MLL strategies, AAC core/fringe word TABLE, participation table, IEP goal stems)
8. Modeling Session / Think-Aloud Script (parallel text + script)
9. Learning Progression Visual (classroom poster — lesson-by-lesson "I can" statements)
10. Teacher Checkpoint Protocol (post-Lesson 2 decision tree + re-teach script)
11. Student Materials: Annotation Guide (code definitions + examples)
12. Student Materials: How to Mark Your Annotations (tools table + tips)
13. Word Bank (annotation words, Tier 2 academic words with word parts, writing words, unit vocab)
14. Sentence Frames (for each annotation code, citing evidence, final product sections)
15. Tools That Help Me Learn (For Reading/Writing/Annotating tables + TTS/STT instructions)
16. Unit Prompt + Choose Your Format (6 format options)
17. Before You Submit / Self-Assessment Checklist
18. Rubric (scoring table)
19. Research Choice Board (6 sources organized by annotation code)
20. Evidence Recording Sheet (structured form with sections A–D)
21. Teacher Answer Key (MCQ answers + SA sample responses for all versions)
22. Supplemental Resources & References (books, film, research sources, passage source notes)

## Nonfiction Unit Build Workflow

Run these phases in order for every unit:

| Phase | Step | Notes |
|-------|------|-------|
| 1 | Draft `.md` content | All 22 sections required |
| 2 | Run `build_*.js` → `*_COMPLETE.docx` | Uses `cbd_docx_template.js` |
| 3 | Convert `.docx` → unit PDF (LibreOffice headless) | Required for packet + preview builds |
| 4 | **Build Communication Access Packet** | Run `_Operations/build_all_units.py` (multi-unit; all 6 units configured) or `_Operations/build_comm_access_packet.py` (Frances Kelsey single-unit reference). Word lists confirmed in Per-Unit Word Lists table below. → outputs `*_Communication_Access_Packet.pdf` |
| 5 | Build TPT Preview PDF | Run `python3 _Operations/build_all_previews.py` (all units) or `--unit [key]` (single). **Source must be Word-exported PDF** in `_TPT/` folder — NOT LibreOffice. Preview outputs to `_TPT/` folder (with COMPLETE.pdf, CAP, etc.) AND to `Preview PDFs/` central folder. Standard: 11 pages (10 for 504 Sit-In). See Preview Standard below. |
| 6 | QC — Unit | Run unit QC checklist below |
| 7 | QC — Communication Access Packet | Run packet QC checklist below |
| 8 | **Assemble TPT Folder** | `build_all_units.py` creates `[UNIT]_TPT/` with: COMPLETE.docx, Symbol_Cards.pdf (if exists), Communication_Access_Packet.pdf, Welcome_and_Terms.pdf. Zip the folder for upload. |
| 9 | TPT Listing Package | Output 0 first, then full listing |
| 10 | Upload to TPT | Zip `[UNIT]_TPT/` → upload; verify live listing |

---

## TPT Preview PDF — Standard (locked 2026-04-02)

**Script:** `_Operations/build_all_previews.py`
**Output:** `[Unit]_TPT/[Unit]_TPT_Preview.pdf` (primary, lives with all TPT upload files) + `Preview PDFs/` central folder (reference copy)

### Rules — Never Violate
- **Source PDF:** Always use the Word-exported PDF in `_TPT/` subfolder. NOT LibreOffice. LibreOffice breaks table formatting, creates blank MCQ pages, and causes content overhangs.
- **MCQ pages are banned from previews.** MCQ questions are stored in Word tables; pypdf cannot merge them and they render blank. Use passage pages and Short Answer / Evidence Sort activity pages instead.
- **Page selection must show all 3 Lexile versions** (V1 + V2 + V3 passage and activity pages where possible).
- **Comm Access vocabulary page** is always pulled from `[Unit]_Communication_Access_Packet.pdf`, page index set per unit (the "Priority Vocabulary for Communication Access" branded page with symbols). 504 Sit-In has no CAP file — no symbol page.
- Never rebuild from scratch. Always edit `UNITS` dict in `build_all_previews.py` with targeted `str_replace`.
- Run `--inspect --unit [key]` to verify page indices before changing selections.

### Standard Page Structure (per unit)
| Slot | Content | Notes |
|------|---------|-------|
| 1 | Branded cover (generated) | Navy background, PREVIEW badge, preview_items list |
| 2 | Lesson overview / Standards alignment | idx varies by unit |
| 3 | Comm-Access or differentiation section | "This unit is designed for AAC users" / "Component AAC access point" / "Differentiating for All Learners" |
| 4 | V1 passage — actual reading text | NOT the V1 section header — find the page with running text |
| 5 | V1 activity (Short Answer or Evidence Sort) | Skip MCQ — find Short Answer or Evidence Sort page |
| 6 | V2 passage — actual reading text | |
| 7 | V3 passage — actual reading text | |
| 8 | V3 activity (Short Answer or Evidence Sort) | |
| 9 | (optional) Additional V2 activity or unique activity type (e.g., Perspective Comparison, Quote Selection) | Unit-specific |
| 10 | Communication Access vocabulary page from CAP | `symbol_page_idx` = page with "Priority Vocabulary for Communication Access" |
| 11 | Branded back page (generated) | Price, full_items list, TPT URL, bundle callout |

### Current Unit Configs (page indices verified 2026-04-02)
| Unit | Source PDF | source_pages | symbol_page_idx |
|------|-----------|-------------|-----------------|
| keiko | `Keiko_TPT/Keiko_COMPLETE.pdf` | [3, 8, 24, 28, 45, 47, 58, 60] | 2 (CAP) |
| radium_girls | `Radium_Girls_TPT/Radium_Girls_COMPLETE.pdf` | [3, 8, 23, 25, 44, 46, 63, 65] | 2 (CAP) |
| zitkala_sa | `Zitkala_Sa_TPT/Zitkala_Sa_COMPLETE.pdf` | [3, 9, 16, 21, 29, 35, 40, 44] | 1 (CAP) |
| 504_sit_in | `504_Sit_In_Unit_COMPLETE.pdf` | [5, 18, 39, 45, 53, 55, 65, 70] | none |
| frances_kelsey | `Frances_Kelsey_TPT/Frances_Kelsey_COMPLETE.pdf` | [3, 8, 27, 38, 44, 65, 66, 70] | 0 (Symbol_Cards) |
| capitol_crawl | `Capitol_Crawl_TPT/Capitol_Crawl_COMPLETE.pdf` | [3, 12, 16, 18, 27, 33, 40, 44] | 2 (CAP) |

### When Adding a New Nonfiction Unit
1. Export COMPLETE.docx → PDF from Word → save to `[Unit]_TPT/[Unit]_COMPLETE.pdf`
2. Run `--inspect --unit [key]` to map all page indices
3. Select 8 pages: overview + comm-access + V1 passage + V1 SA + V2 passage + V3 passage + V3 SA + one more
4. Set `symbol_pdf` to `[Unit]_TPT/[Unit]_Communication_Access_Packet.pdf` and find `symbol_page_idx` for the "Priority Vocabulary" page
5. Add unit config to `UNITS` dict in `build_all_previews.py`
6. Run `--unit [key]` to build and verify

---

## Communication Access Packet — Build Reference

**Script:** `_Operations/build_comm_access_packet.py`
**Shared tracker:** `Products/Nonfiction Units/AAC_Communication_Session_Tracker.pdf`

### Packet Structure (10 pages — standard for all nonfiction units)

| Pages | Content | Source |
|-------|---------|--------|
| 1–3 | Real unit pages: MLL & AAC teacher reference (idx 7, 8, 9 of unit PDF) | Extracted from unit PDF |
| 4 | Top 5 Priority Vocabulary callout (Top 5 Core + Top 5 Fringe, symbol + word) | Built — reportlab |
| 5–7 | Core word symbol cards — 3×4 grid (12 per page), 2"×2" per card | Built — reportlab + ARASAAC cache |
| 8–9 | Fringe word symbol cards — 3×4 grid (12 per page), 2"×2" per card | Built — reportlab + ARASAAC cache |
| 10 | AAC Communication Session Tracker | Appended PDF |

### Symbol Card Design Rules (ALL packets)
- Card size: exactly 2"×2" (144pt × 144pt)
- Grid: 3 columns × 4 rows = 12 per page
- Card style: white center, Fitzgerald Key colored border (3pt), 10pt white gap between cards (nested table)
- Symbol image: 88pt ARASAAC PNG from `_Operations/symbol_cache`
- Word label: 13pt Helvetica-Bold, navy, centered
- No category name text on card — color border IS the Fitzgerald Key indicator
- Fitzgerald Key categories: green=verbs, orange=adjectives, yellow=pronouns, blue=prepositions, pink=social, white(grey)=nouns/other

### Top 5 Callout Page Rules
- Section title: "Priority Vocabulary for Communication Access"
- Intro text: "These are the highest-priority vocabulary words for this unit. Core words appear on most AAC systems. Fringe words are unit-specific — students may use printed cards, symbols from an existing PEC set, or programmed device pages."
- Two columns: TOP 5 CORE (teal header) | TOP 5 FRINGE (navy header)
- Word cells: white background, Fitzgerald Key colored BOX border (2pt)
- No device-assumption language anywhere in the packet

### Per-Unit Word Lists (confirmed — sourced from unit DRAFTs + trading card JSON)

Page count per section: `ceil(word_count / 12)` — do NOT force fixed page counts.
Build script: `_Operations/build_all_units.py` (all 6 units; multi-unit runner)
Single-unit script: `_Operations/build_comm_access_packet.py` (Frances Kelsey reference)

| Unit | Core Words | Fringe Words | Top 5 Core | Top 5 Fringe | CAP Pages |
|------|-----------|--------------|------------|--------------|-----------|
| Frances Kelsey | say, think, know, want, not, good, bad, wrong, right, help, stop, go, more, different, same, because, but, if, true, question, answer, prove, show, tell, believe, strong, weak (27) | drug, safe, test, approve, deny, claim, evidence, thalidomide, company, pressure, review, scientist, law, protect (14) | not, show, wrong, because, strong | safe, test, deny, pressure, claim | 10 |
| 504 Sit-In | people, change, feel, fight, help, make, need, show, sit, stop, tell, think, want, brave, different, fair, free, important, right, safe, same, strong, wrong (23) | approve, crawl, demand, deny, occupy, organize, protest, prove, sign, access, advocate, barrier, building, community, disability, discrimination, equal, federal, government, law, rights, section (22) | fight, show, stop, right, change | protest, law, disability, equal, rights | 8 |
| Keiko | think, feel, know, good, bad, best, free, live, place, because, why, help, care, same, different, more, less, before, after, true, false, show, mean, prove, first, then, last, which (28) | captivity, ocean, whale, park, sick, healthy, home, family, pod, human, wild, move, swim, learn, die, freedom, safe, danger, company, protect, today (21) | free, because, help, show, true | captivity, whale, ocean, wild, freedom | 9 |
| Radium Girls | think, feel, know, good, bad, right, wrong, because, why, help, stop, fight, change, same, different, more, less, before, after, true, false, show, mean, prove, first, then, last (27) | radium, factory, worker, paint, sick, law, court, safe, danger, company, money, protect, today, bone, doctor, lie, proof (17) | prove, wrong, stop, fight, show | radium, factory, safe, danger, lie | 9 |
| Capitol Crawl | think, know, true, false, same, different, good, bad, strong, weak, because, but, agree, disagree, why, who, what, where, when (19) | crawl, Capitol, steps, protest, law, ADA, ADAPT, source, reliable, corroborate, evidence, claim, verify, contradict (14) | because, agree, strong, true, same | protest, law, evidence, claim, ADA | 9 |
| Zitkala-Ša | think, know, feel, why, because, but, and, same, different, change, make, do, help, stop, want, need, right, wrong, good, bad (20) | zitkala, boarding, assimilation, dakota, reservation, hair, spirit, testimony, organize (9) | change, need, right, stop, because | assimilation, boarding, spirit, testimony, reservation | 6 |

---

## QC Checklist — Communication Access Packet (Phase 7)

Run before marking packet complete. Every item must pass before moving to TPT listing.

**Structure**
1. ☐ Page count = (# AAC unit pages) + 1 Top 5 + ceil(core_count/12) + ceil(fringe_count/12) + 1 tracker. Do NOT enforce a fixed 10-page count — page count varies by word count.
2. ☐ First pages are the real MLL & AAC teacher reference pages from the unit (not redesigned, not rewritten)
3. ☐ Top 5 callout has correct unit-specific Top 5 Core and Top 5 Fringe words
4. ☐ Core word grids follow Top 5; Fringe word grids follow; tracker is last page
5. ☐ Final page is `AAC_Communication_Session_Tracker.pdf` (1 page, CbD branded)

**Symbol Cards**
6. ☐ All symbol cards are 2"×2" with 3 columns × 4 rows = 12 per page
7. ☐ Fitzgerald Key color border present on every card (correct category color)
8. ☐ White center on all cards (no filled color backgrounds)
9. ☐ Physical white gap visible between all cards (nested table approach — not just a border line)
10. ☐ Word label is bold, navy, uppercase — no Fitzgerald Key category name printed as text
11. ☐ Symbol image present for each word (or `(no symbol)` placeholder if not in cache)
12. ☐ Section heading reads "Core Words" / "Fringe Words — Unit-Specific Vocabulary" (no "Pre-Program" language)

**Language Standards**
13. ☐ No device-assumption language anywhere ("pre-program", "program your device", "SGD required")
14. ☐ Top 5 callout uses neutral language: "printed cards, symbols from an existing PEC set, or programmed device pages"
15. ☐ No SLP gatekeeping language ("work with your SLP" as sole instruction)
16. ☐ Running header on all built pages: italic unit title (left) + COMMUNICATE (teal) BY DESIGN (amber) (right)
17. ☐ Footer on all built pages: `[Unit Title] · Communication Access Packet · Communicate by Design · teacherspayteachers.com/store/communicate-by-design`

**Brand**
18. ☐ Teal is #006DA0 (document teal — not #00B4D8)
19. ☐ Navy is #1B1F3B
20. ☐ Amber is #FFB703

---

## QC Checklist (Phase 6 of Nonfiction Unit Workflow)

Run programmatically before TPT listing:
1. ☐ Essential question appears in ALL version sections
2. ☐ Annotation codes consistent across V1, V2, V3
3. ☐ No ability-sorting language (grep for: "above grade level", "below grade level", "low readers", "struggling", "remedial")
4. ☐ AAC core/fringe word TABLE present — `makeTable()`, not bullet lists
5. ☐ Core words identified
6. ☐ Print-safe (no problematic color fills on student pages)
7. ☐ All fonts are Arial
8. ☐ No placeholder text (TBD, TODO, PLACEHOLDER, [INSERT)
9. ☐ End-matter sequence correct: Accessibility Statement → About the Creator → Terms of Use → end page
10. ☐ All 3 versions present with correct part count
11. ☐ No heading2/heading3 pollution in student worksheet sections (check TOC rendering)
12. ☐ V3 passages include actual passage text (not just vocabulary boxes)

## Skill Number Assignments (LOCKED — do not change without Jill's approval)
| Unit | Skill # | Skill Name |
|------|---------|-----------|
| Keiko | #1 | Close Reading and Annotation |
| Radium Girls | #1 | Close Reading and Annotation |
| Zitkala-Ša | #3 | — |
| 504 Sit-In | #4 | — |
| Frances Kelsey | #5 | — |
| Capitol Crawl | #6 | — |

## Nonfiction Unit Folder Standard
Each unit folder contains:
- `build_*.js` — build script
- `*_Unit_DRAFT.md` or `*_Lesson_DRAFT.md` — source content
- `*_COMPLETE.docx` — built product
- `*_Complete.zip` — TPT package
- `*_Printable_Kit.docx` — printable kit
- `*_Symbol_Cards.pdf` — symbol card set
- `*_Communication_Access_Packet.pdf` — AAC Communication Access Packet (built after docx, before QC)
- `*_TPT_Listing_Package.md` — TPT listing copy **must contain Output 0 as first section**
- Unit-specific images, Pinterest pins, trading card files

## TPT Listing Package — Output 0 Standard (REQUIRED — every product, every listing)

Output 0 is the FIRST section of every `*_TPT_Listing_Package.md`. It contains three copy/paste-ready fields for the TPT seller dashboard. Generate this BEFORE writing the full listing description.

```markdown
## OUTPUT 0: SEO-READY UPLOAD FIELDS (Use these for TPT — copy/paste directly)

### TPT Title (XX chars — verified under 80)
[Topic] | [Historical/Subject Angle] | [Adapted Reading or Differentiator] | [SPED Grades 6-10]

### TPT Description Opening — First 180 Characters (keyword-dense — paste as FIRST line of description)
[Product name] nonfiction unit | Special education grades 6-10. [Historical angle] at three reading levels — adapted reading, [skill focus], AAC supports for SPED classrooms.

### Custom Keyword Tags (enter all 7 in TPT keyword field)
[topic keyword], [historical angle], nonfiction, special education, adapted reading, SPED, grades 6-10
```

**Title rules:**
- ≤80 characters — verify character count before finalizing
- Lead with the topic name (what teachers search — the event, person, or book name)
- Pipe-separated segments
- Must include "SPED" or "Special Education" and "Grades 6-10"
- Must include "Adapted Reading" OR a specific historical angle as differentiator
- Never use abbreviations like "SpEd" — use "SPED"

**Description opening rules:**
- ≤180 characters
- Keyword-dense, NOT hook-style (no "Your students..." openers in this block)
- Must contain: product name + "special education" + "grades 6-10" + "adapted reading" + "AAC"
- This block is PREPENDED to the existing narrative description — it does not replace the hook

**Tag rules:**
- 7 custom keywords in TPT keyword field (separate from category tags)
- Always include: nonfiction, special education, adapted reading, SPED, grades 6-10
- Add topic-specific terms (person/event name, historical angle) in remaining slots

## TPT Preview PDF — Standardized Format

All nonfiction units must have a watermarked TPT preview PDF saved to:
`Products/Nonfiction Units/Preview PDFs/[UnitName]_TPT_Preview.pdf`

**Build script:** `/sessions/.../build_all_previews.py` (parameterized — add new units by adding a config dict to UNITS)

### Preview Structure (8–9 pages depending on symbol card availability)

| Page | Content | Source |
|------|---------|--------|
| 1 | Designed TOC — matches student-facing style (white bg, running header, Name/Class/Teacher, two-column layout) | reportlab build |
| 2 | V1 Passage — Part 1 | Unit PDF, idx `v1_passage` |
| 3 | V3 Passage — Part 1 | Unit PDF, idx `v3_passage` |
| 4 | V1 Activity — MCQ or Evidence Sort, Part 1 | Unit PDF, idx `v1_activity` |
| 5 | V3 Activity — MCQ or Evidence Sort (Part 1 or 2 if Part 1 V3 has no MCQ) | Unit PDF, idx `v3_activity` |
| 6 | Symbol Cards — Core Words grid (if symbol PDF exists; skip if not) | Symbol Cards PDF, idx 0 |
| 7 | Word Bank student page | Unit PDF, idx `word_bank` |
| 8 | Version Overview (Unit Overview — Three Versions) | FK preview idx 6 (generic) |
| 9 | Instructional Design Foundations | FK preview idx 7 (generic) |

All pages receive a diagonal "PREVIEW" watermark (navy, 10% opacity, 72pt Helvetica-Bold, 45°).

### Page Index Map by Unit

| Unit | v1_passage | v3_passage | v1_activity | v3_activity | word_bank | symbol_idx |
|------|-----------|-----------|------------|------------|----------|-----------|
| Frances Kelsey | 26 | 64 | 42 | 65 | 19 | 0 (FK Symbol Cards) |
| 504 Sit-In | 36 | 42 | 38 | 55 | 24 | 0 (504 Symbol Cards) |
| Keiko | 23 | 57 | 36 (Quote Selection P3 V1) | 67 (Perspective Comparison P4 V3) | 13 | — (none) |
| Radium Girls | 21 | 62 | 27 (Evidence Sort P2 V1) | 63 (MCQ P1 V3) | 12 | — (none) |
| Zitkala-Ša | 14 | 37 | 20 | 41 | 48 | 0 (Zitkala-Sa Symbol Cards) |
| Capitol Crawl | 16 | 26 | 30 | 33 | 45 | — (none) |

### Design Rules for Designed TOC Page
- White background only — NO navy panels
- Running header: italic unit title (left) + COMMUNICATE (teal) BY DESIGN (amber) — bold (right)
- 1.5pt teal horizontal rule under header
- "Table of Contents" title in 18pt navy Helvetica-Bold
- Name/Class/Teacher line in 9pt gray
- 0.5pt light gray rule under Name/Class/Teacher
- Two-column layout: Teacher Reference + Student Handouts (left) | V1/V2/V3 by passage + Symbol Cards (right)
- Column divider: 0.5pt light gray vertical rule
- Footer: unit title · Communicate by Design · Where AT Meets Practice · TPT store URL

## Build Script Output Note
All nonfiction build scripts output COMPLETE .docx to `../` (Nonfiction Units root), NOT into the unit folder. After rebuilding, move/copy the output into the unit folder.

## UFLI QC Evaluation Rubric
Full rubric: `_Operations/UFLI_QC_Evaluation_Rubric.md`
Evaluates all 8 UFLI steps for: (a) alternative response pathway, (b) low-tech access, (c) SGD compatibility note, (d) auditory confirmation loop preservation. Also checks AAC modality coverage, strength-based language, pacing guidance, product structure. Target: all 8 steps at ✅.

## Preview PDF Build
`build_preview_pdfs.py` (pypdf + ReportLab). Generates branded 10-page watermarked preview PDFs.
Structure: Branded cover (navy bg, CbD logo, unit title, "PREVIEW") → 8 watermarked sample pages → "Get the Full Unit" back page with pricing.
Output: `Products/Nonfiction Units/Preview PDFs/`

## Step 0d: Grade Range Recommendation
For new units, recommend grade range based on source material complexity:
- 6–8 (younger): lower Lexile source, accessible vocabulary
- 6–10 (full range): standard CbD range
- 8–10 (older): higher complexity source, mature themes

All 6 existing units are 6–10.

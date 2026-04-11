# Build System Reference

Deep build notes for CbD. Pull this file when doing code/build work.

---

## Student Worksheet Template System — ReportLab v2.1 (Locked 2026-04-11)

**All new units (started after 2026-04-11) MUST use this system for student activity pages.**
Do NOT retrofit Units 1–6 nonfiction or PB Companions 1–6 — those builds are LOCKED.

### Core Philosophy (Hard Rules — Never Violate)
These worksheets do not specify how a student responds. Symbol cards glued to the page, eye gaze + scribe, pencil, typed output on a device — all are equally valid and demonstrate the same skill. The worksheet's job is accessible language design, not access method instruction.

- **NO** `access_note` defaults that instruct students HOW to respond ("write, type, or use your device" = WRONG)
- `access_note` parameter: optional, prints nothing by default. Only use to point to language support (e.g., "Key vocabulary is in your communication packet.")
- **NO** filled response areas, NO gray boxes. Print-first: white background throughout.
- Zone identity = 3pt colored left-bar (`LINEBEFORE`) only — not filled headers.
- Sentence frames carry the AAC access load. The CAP is the vocabulary document.

### File
`_Operations/Build/cbd_worksheet_templates.py` — v2.1

### Template Catalog — 8 Templates (v2.1)
| # | Function | Purpose | Instructional Activity |
|---|----------|---------|----------------------|
| 1 | `make_mcq_page()` | Multiple choice, 4 options, ○ circles | Close Reading & Annotation |
| 2 | `make_short_answer_page()` | Open response with optional sentence frame | Write-Ables, Inferencing Scaffolds |
| 3 | `make_cer_page()` | Claim-Evidence-Reasoning (amber/teal/navy left bars) | CER Framework, Critical Response Scaffolds |
| 4 | `make_evidence_sort_page()` | 3-column evidence sort / text interaction | Story Grammar, VSDs |
| 5 | `make_vocab_preview_page()` | Vocabulary pre-teaching with ARASAAC symbols | IRA Vocabulary Stops, Descriptive Teaching |
| 6 | `make_annotation_guide_page()` | Annotation codes reference (3-code system) | Close Reading & Annotation |
| 7 | `make_descriptor_board_page()` | Attribute grid (Appearance/Action/Emotion) + composition zone | Describe to Draw, Descriptive Teaching Model |
| 8 | `make_partner_prompt_card()` | Teacher/partner-facing CROWD/ALM prompt cards | Dialogic Reading, ALM — goes in Teacher Packet NOT Student Activities PDF |

**Instructional Activity → Template mapping is tracked in Airtable** (`tblHJlkbCF7c4tCNP` → `Worksheet Template` field).
Check Airtable before building any new unit's student pages — the mapping is already done for all 13 activities.

**3 activities have NO student worksheet:**
- Story Bags & Multisensory Grounding — tactile/object-based, no page
- Shared Reading with ALM — partner card only (`make_partner_prompt_card()` in teacher build)
- Dialogic Reading with CROWD Prompts — partner card only (`make_partner_prompt_card()` in teacher build)

### WorksheetDoc — Always Create First
```python
from cbd_worksheet_templates import WorksheetDoc, make_mcq_page, make_cer_page

doc = WorksheetDoc(
    output_path="path/to/output.pdf",
    unit_title="Fred Korematsu: The Man Who Said No",
    product_line="Nonfiction Reading Unit",
    version_label="V1",   # or None — shown in header only
)
story = []
story += make_mcq_page(doc, "Part 1 Comprehension Check", questions=[...])
story += make_short_answer_page(doc, "Short Answer", questions=[...])
story += make_cer_page(doc, "Claim-Evidence-Reasoning", prompt="Was...")
doc.build(story)
```

### Data Formats — Both Key Styles Accepted
```python
# MCQ — either format works:
{"text": "Question stem", "choices": [("A", "Option one"), ("B", "Option two"), ...]}
{"stem": "Question stem", "options": ["A  Option one", "B  Option two", ...]}

# Short answer — either format works:
{"text": "Question", "frame": "I think ___ because ___.," "lines": 4}
{"prompt": "Question", "sentence_frame": "I think ___ because ___.", "lines": 4}
```

### Version Differentiation — Content Parameters, Not Separate Templates
V1/V2/V3 differences use the SAME template functions with different data passed in.
There is NO `make_short_answer_v3_page()` — there is only `make_short_answer_page()`.

| What changes | How |
|---|---|
| Version label in header | `WorksheetDoc(version_label="V3")` |
| Key words strip above questions | `word_bank=["evidence", "approve", "safe", ...]` |
| Sentence frame below question | `sentence_frame="Kelsey refused because..."` |
| Fewer writing lines | `lines=2` vs default 4 |
| V1/V2 — no word bank | `word_bank=None` (default) — nothing printed |

**Sentence frame convention (hard rule):** Frames must end with `...` or `:` — never a single `___` blank. A single blank implies one-word fill-in, which doesn't match multi-word CAP vocabulary and telegraphs a wrong response strategy.
  - ✓ `"Kelsey refused because..."` → student continues onto the writing lines
  - ✓ `"The author's claim is: "` → student writes below
  - ✗ `"Kelsey refused because ___."` → implies one word, conflicts with key words strip

**`word_bank` parameter** — available on `make_short_answer_page()` and `make_cer_page()`.
- Words should come from the CAP — not introduce new vocabulary.
- Reduces retrieval demand; comprehension task stays the same.
- V3 scaffold only. V1/V2: pass `word_bank=None` or omit.

```python
# V3 short answer with word bank:
make_short_answer_page(doc, "Part 1 — V3", questions=[...],
    word_bank=["evidence", "approve", "safe", "test", "protect"])

# V3 CER with word bank:
make_cer_page(doc, "CER — V3", prompt="Was Kelsey right?",
    claim_frame="Kelsey was _____ because _____.",
    word_bank=["evidence", "approve", "safe", "test", "protect"])

# V1/V2 — same function, no word bank:
make_short_answer_page(doc, "Part 1 — V1", questions=[...])
```

### Symbol Size — LOCKED
`SYM_SIZE = 88` pts — matches `build_comm_access_packet.py`. Never change.
`SYM_COL_W = 1.5 * inch` — holds 88pt image with padding. Never change.

### New-Unit Trigger — Phase 1 Gate Checklist Item
At Phase 1 Gate (before any build starts), confirm:
> ☐ Student worksheet pages → `cbd_worksheet_templates.py`
> ☐ Teacher content, passages, partner scripts, vocab tables, CAP → `.js` docx build
> ☐ These are TWO SEPARATE outputs — do not merge activity pages into the docx

### Integration with .js Docx Builds
1. `.js` build → `[Unit]_COMPLETE.docx` + `[Unit]_Student_Print_Materials.docx` (teacher + passage content)
2. `cbd_worksheet_templates.py` → `[Unit]_Student_Activities.pdf` (all response pages)
3. Both go into the 4-file TPT zip
4. To merge into a single Student Packet PDF: use `pypdf.PdfWriter` (see `build_all_units.py` pattern)

---

## Symbol Pages — Hard Build Rules — LOCKED (Apr 2026)

### ⛔ STOP — Read this before touching any symbol page code

**Symbol pages are NEVER built inside a `.js` docx build. Period.**

Every CbD product that includes symbol pages must build them as a **Python/ReportLab PDF** using `build_symbol_pages_pdf()` and `make_card()` ported from `_Operations/Build/build_comm_access_packet.py`. The `.js` build handles the `.docx` content only. Symbol pages are a separate PDF merged at assembly.

If you are in a `.js` build file and you are about to write a `symbolCard()` function or a `buildSymbolCardsSection()` function — **stop. Close the `.js` file. Open a Python file.**

### Card spec — LOCKED — no exceptions
Card = symbol image (or `(no symbol)` italic fallback) + word label (ALL CAPS, Helvetica-Bold, 13pt, navy, centered) + FK-colored 3pt border. **Nothing else.**
- NO category bar
- NO core/fringe label ("Core Word", "Unit Vocabulary", etc.)
- NO star marker (★) on the card face
- NO part-of-speech label ("verb", "noun", "adj.", etc.)
- NO extra text of any kind
- Word label ALWAYS present, even on `(no symbol)` fallback cards
- Empty/padding cells at end of page: invisible Spacer — NOT a visible blank card

### Card dimensions — LOCKED
- Card size: 2" × 2" (144pt) fixed — NEVER resize per product
- Symbol image: 88pt within the card
- Grid: 3 columns × 4 rows = 12 cards per page
- Gap: 5pt white space each side of a card (physical gap, not just a border line)
- FK border: 3pt colored border matching `FKC_BORDER` dict

### Two-section structure — required for every product
Symbol pages are always two separate labeled sections:
1. **Core Words** — section header, then core word grid
2. **Fringe Words — Unit-Specific Vocabulary** — section header, then fringe word grid

Never merge core and fringe into one undivided grid.

### The gold standard function is `make_card()` in `build_comm_access_packet.py`
- Do NOT rewrite it from scratch for a new product
- Port it to a product-specific Python file (e.g., `build_symbol_pages_picbook.py`) with updated paths and word lists
- The function logic, card dimensions, FK color mapping, and fallback behavior must match exactly

### Root cause note (Apr 2026)
The symbol card spec was violated three times in one session because the spec lived in prose but was not enforced as a build gate. The fix: if you are not in a Python file using `build_symbol_pages_pdf()` + `make_card()`, you are not building symbol pages yet. This rule supersedes any in-line instinct to add labels, markers, or category information to cards.

## Core Build Warnings

- **ALWAYS spread array-returning template functions:** `writeOnLines()`, `studentHandoutHeader()`, `esrPageHeader()`, `mcqPageHeader()`, `saPageHeader()`, `passageHeader()`, `titlePage()`, `tocPage()`, `endMatter()`, `accessibilityStatement()`, `aboutTheCreator()`, `termsOfUse()` — ALL return arrays, ALL need `...` spread. Missing spread causes `<0/>` XML corruption.
- **End-of-document order in every teacher doc:** `...T.accessibilityStatement()` → `...T.aboutTheCreator()` → `...T.termsOfUse()` → `...T.endMatter()`
- **`studentHandoutHeader` takes 3 args:** `(unitTitle, title, subtitle)` — not just the section name. Do NOT pair with a preceding `heading1` call — causes duplicate blank pages.
- **`titlePage` opts:** `{ unitTitle, unitSubtitle, skillNumber, skillName, gradeRange, versions, parts }` — match property names exactly.
- **`assembleAndWrite` arg order:** `(unitShortTitle, children, outputPath, meta)` — title first, then children.
- **Regex lookaheads for extraction:** use `(?=end_marker|$)` not bare `content|end_marker|$`
- **V3 passage extraction: NEVER use `---\s*\n` as a regex end boundary** — V3 passages have `---` separators between vocab boxes and passage text. Use `(?=### Version \d|*Word count:|## )` or similar content-aware boundaries.
- **Heading pollution: student worksheet instructions must NOT use `heading2()` or `heading3()`** — use `T.p(text, { bold: true, size: 24, before: 200, after: 80 })` instead. Headings appear in the TOC.
- **Keep heading2/heading3 ONLY for:** real teacher material section headers and major student handout section names (after studentHandoutHeader).
- **NEVER prefix student-facing heading2 with "STUDENT MATERIALS:"** — that label is for code comments only. Render just the section name.
- **`makeTable` rows MUST be plain string arrays** — NEVER pass `{ text: "...", bold: true }` objects. Use `**text**` markdown for bold. `String({ text: "..." })` renders as `[object Object]`.
- **Nonfiction require path:** `path.join(__dirname, "..", "..", "..", "_Operations", "cbd_docx_template")` — 3 levels up from unit folder. Using 4 levels up is a bug.
- **Output path — iCloud mount eats freshly built files:** Writing outputPath to the iCloud FUSE mount (`/mnt/com~apple~CloudDocs/...`) reports success but the file disappears before Word can open it (iCloud eviction). **ALWAYS write to the sandbox temp dir and deliver via `mcp__cowork__present_files`:** `const outputPath = "/sessions/[session-id]/[filename].docx"` then call `mcp__cowork__present_files` with that path.
- **Do NOT add secondary `require("docx")` imports in build scripts:** Only use `const T = require(".../cbd_docx_template")`. Adding a second `require("node_modules/docx")` can silently corrupt document assembly even though the ZIP and XML validate. If you need Paragraph/TextRun classes, use `T.Paragraph`, `T.TextRun` — they are exported by the template.
- **keepNext on H2:** The current docx npm version does not support `keepNext: true` on Paragraph — the property is silently ignored. Do not attempt. Handle orphan headings with explicit page breaks or accept the behavior.

## Nonfiction TPT Folder Architecture — LOCKED (Apr 2026)

Each nonfiction unit's `[Unit]_TPT/` folder contains **exactly 4 files**. No more, no less.

| File | Built by | Notes |
|------|----------|-------|
| `[Unit]_COMPLETE.docx` | `build_*.js` | Full teacher + student + AK document |
| `[Unit]_Student_Print_Materials.docx` | `build_*.js` (same script, second output) | Student-facing content only — NO teacher content, NO AK |
| `[Unit]_Welcome_to_the_Product.pdf` | `build_welcome_nonfiction.py` | 3 intro pages + Teacher AK pages from DRAFT.md |
| `[Unit]_Communication_Access_Packet.pdf` | `build_all_units.py` (CAP build only) | Symbol cards + Priority Vocab + Session Tracker |

**Critical build order:** Run `build_*.js` → export COMPLETE.docx to PDF (see below) → run CAP build → run `build_welcome_nonfiction.py` LAST.

**Automated PDF export (replaces manual Word → Save As — locked Apr 10 2026):**
Use `_Operations/Build/export_docx_to_pdf.py` — calls the actual Word engine via docx2pdf/osascript, identical output to File → Save As → PDF. NEVER LibreOffice for nonfiction/poetry/fiction units.
```bash
# Single file:
python3 _Operations/Build/export_docx_to_pdf.py "Products/Poetry Reading Units/Unit 1 - What the Voice Carries/WhatTheVoiceCarries_COMPLETE.docx"

# Entire product line:
python3 _Operations/Build/export_docx_to_pdf.py --product-line poetry
python3 _Operations/Build/export_docx_to_pdf.py --product-line nonfiction
python3 _Operations/Build/export_docx_to_pdf.py --product-line fiction
```
Requires: `pip install docx2pdf --break-system-packages` + Microsoft Word for Mac installed. The welcome build must always run after the CAP build because `build_all_units.py`'s `assemble_tpt_folder()` function is outdated and will overwrite welcome PDFs if triggered.

**NEVER call `assemble_tpt_folder()` from `build_all_units.py`.** That function is outdated: it copies COMPLETE.docx to the wrong location (SameFileError when COMPLETE.docx is already in the TPT folder), calls the old `build_welcome_pdf()` that produces only 2 pages, and produces the wrong file set. Call only `build_comm_access_packet()` directly.

### Student Print Materials — Index-Marker Pattern (all nonfiction build scripts)

Every `build_*.js` script captures `children.length` at key boundaries to enable student/AK separation:

```js
// STUDENT MATERIALS: ANNOTATION GUIDE
const handoutStart = children.length; // start of student handout section

// VERSION 1
const v1Start = children.length;

// VERSION 2
const v2Start = children.length;

// VERSION 3
const v3Start = children.length;

// TEACHER ANSWER KEY
const akStart = children.length;

// --- assembly ---
const handoutElements = children.slice(handoutStart, v1Start);
const v1Elements = children.slice(v1Start, v2Start);
const v2Elements = children.slice(v2Start, v3Start);
const v3Elements = children.slice(v3Start, akStart);
const studentChildren = [...handoutElements, ...v1Elements, ...v2Elements, ...v3Elements];
// studentChildren never contains AK content
```

**If `both()` is used in the script:** Capture `const studentHandoutsEnd = studentHandouts.length` immediately before the AK section begins, then use `studentHandouts.slice(0, studentHandoutsEnd)` for student file assembly. Never let `both()` calls inside the AK section pollute the student array.

### Welcome PDF — `build_welcome_nonfiction.py`

- Script: `_Operations/Build/build_welcome_nonfiction.py`
- Reads `*_DRAFT.md` for each unit, extracts `## Teacher Answer Key` section via `page4_answer_key()`
- Output page counts (verified Apr 2026): Frances Kelsey=11pp, Radium Girls=8pp, Keiko=7pp, Zitkala-Sa=4pp, 504 Sit-In=7pp, Capitol Crawl=4pp
- **ALWAYS run this last** — after `build_all_units.py` has completed its CAP build
- Never run `assemble_tpt_folder()` before or after — it will overwrite the output

### CAP Build — Scratch PDF Naming

`build_all_units.py` expects COMPLETE PDFs in `/sessions/[session-id]/` (scratch), not in TPT subfolders. Copy the Word-exported PDF to scratch using the expected filename:

| Unit | Expected scratch filename |
|------|--------------------------|
| Frances Kelsey | `Frances_Kelsey_Unit_COMPLETE.pdf` |
| Zitkala-Sa | `Zitkala_Sa_Unit_COMPLETE.pdf` |
| 504 Sit-In | `504_Sit_In_Unit_COMPLETE.pdf` |
| Capitol Crawl | `Capitol_Crawl_Lesson_COMPLETE.pdf` |
| Keiko | `Keiko_Unit_COMPLETE.pdf` |
| Radium Girls | `Radium_Girls_Unit_COMPLETE.pdf` |

---

## Build Scripts Reference

| Product | Build Script | Output |
|---------|-------------|--------|
| 504 Sit-In | `Products/Nonfiction Units/504 Sit In/build_504_sit_in.js` | `504_Sit_In_TPT/504_Sit_In_COMPLETE.docx` + `504_Sit_In_Student_Print_Materials.docx` |
| Frances Kelsey | `Products/Nonfiction Units/Frances Kelsey/build_frances_kelsey.js` | `Frances_Kelsey_TPT/Frances_Kelsey_COMPLETE.docx` + `Frances_Kelsey_Student_Print_Materials.docx` |
| Capitol Crawl | `Products/Nonfiction Units/Capitol Crawl/build_capitol_crawl.js` | `Capitol_Crawl_TPT/Capitol_Crawl_COMPLETE.docx` + `Capitol_Crawl_Student_Print_Materials.docx` |
| Zitkala-Ša | `Products/Nonfiction Units/Zitkala-Sa/build_zitkala_sa.js` | `Zitkala_Sa_TPT/Zitkala_Sa_COMPLETE.docx` + `Zitkala_Sa_Student_Print_Materials.docx` |
| Radium Girls | `Products/Nonfiction Units/Radium Girls/build_radium_girls.js` | `Radium_Girls_TPT/Radium_Girls_COMPLETE.docx` + `Radium_Girls_Student_Print_Materials.docx` |
| Keiko | `Products/Nonfiction Units/Keiko/build_keiko.js` | `Keiko_TPT/Keiko_COMPLETE.docx` + `Keiko_Student_Print_Materials.docx` |
| UFLI Teacher Guide | `Products/UFLI Phonics/UFLI/build_teacher_guide.js` | UFLI_Teacher_Guide_and_Communication_Partner_Guide.docx |
| UFLI Per-Lesson | `Products/UFLI Phonics/UFLI/build_ufli_packet.js` + `ufli_lesson_configs.js` | Output/UFLI_Lesson[XX]_[letter]_Packet.docx |
| Letter Card Library | `build_letter_cards.py` (ReportLab) | UFLI_Letter_Cards_Lowercase.pdf |
| Session Data Tracker | `build_data_tracker.py` (ReportLab) | UFLI_Session_Data_Tracker.pdf |
| Symbol Binder Guide | `build_binder_guide.py` (ReportLab) | UFLI_Symbol_Binder_Guide.pdf |
| Trading Cards (all) | `_Operations/build_trading_card_decks.py --deck all` | — |
| Nonfiction Kits | `_Operations/build_nonfiction_kits.js` | Products/Nonfiction Units/Printable_Kits/ |
| Preview PDFs | `build_preview_pdfs.py` (pypdf + ReportLab) | Products/Nonfiction Units/Preview PDFs/ |

## TPT Packaging Structure

Each TPT zip contains:
1. Complete doc (Google Doc + Word + PDF)
2. Student Materials (tabbed by version/part)
3. Teacher Answers (answer keys separated)
4. Preview PDF (branded cover + sample pages + "Purchase full unit" back page)
5. Trading Card Deck PDF (for any product with AAC words — via `cbd_trading_cards.py`)

## Nonfiction Printable Kits (5 components per kit)
1. Communication Partner Word List
2. Symbol Cards (trading card size, 3-zone layout, Fitzgerald Key color-coding)
3. Word Cards (text-only matching cards, 4/row)
4. Communication Board (Level 2 access sizing)
5. Reading Practice Cards

- Vocab config: `_Operations/cbd_unit_vocab.js` (all 6 units, 248 total words)
- Default access level: Level 2 (4/row, 1.25", eye gaze/direct selection)
- Kit builder: `_Operations/build_unit_printable_kit.js`

## Student Packet / Student Activity PDF Standard — HARD RULES

CbD student response packets are **b&w printable** for classroom use. Any file named `*_Student_Packet.pdf`, `*_Student_Handout.pdf`, `*_Printable_Packet.pdf`, or similar must meet these rules.

**RULE 1 — White background everywhere.**
No navy, violet, amber, teal, or any colored background on the page itself or on response areas. The page background is white.

**RULE 2 — Only one thin header bar per page (navy fill, 16–20pt height, white text).**
Each student page may have one thin section/poem label bar at the top (NAVY `#1B1F3B` fill, WHITE text, height 16–20pt). This is the only filled colored element allowed on student pages. Match Wonder Layer 5: `BAR_H = 18; c.rect(M_X, y - BAR_H, AVAIL_W, BAR_H, fill=1, stroke=0)`.

**RULE 3 — No colored fills on interactive elements.**
- NFMA step labels, section labels, prompt headers: bold text only. Use a thin left accent bar (3–4pt wide, navy) if needed — no amber/violet pill fills.
- Checkbox options: `[ ]  text` plain text — no colored borders on checkboxes.
- Version labels (V1/V2/V3): plain bold text with a thin gray rule below — no color text, no colored badges.

**RULE 4 — Response areas: white fill, light gray border.**
`c.setFillColor(colors.white)` + `c.setStrokeColor(colors.HexColor("#CBD5E1"))` + `c.setLineWidth(0.7)`. Never use colored tints (#F3E8FF, #EFF6FF, etc.) on response/indicate areas — those print as mid-gray on photocopiers.

**RULE 5 — FK vocabulary chips ARE allowed in color.**
Fitzgerald Key category colors on vocabulary chips are intentionally colored for AAC recognition. These are exempt from Rule 1–4. Symbol card pages in the CAP/Printable Packet are also exempt.

**RULE 6 — Cover pages: white background, text only.**
A student packet cover page (if included) must use white background, black/navy text. No full-page colored backgrounds. Simple horizontal rules to separate sections are fine.

**Violation check — before running any student packet build:**
If `fill_box`, `step_label`, `poem_title_bar`, or similar functions use `setFillColor(VIOLET)`, `setFillColor(AMBER)`, `setFillColor(LIGHT)` with `fill=1` on areas larger than 20pt height → STOP. That is a violation. Refactor to b&w standard before running.

**Reference implementation:** Wonder `build_wonder_printable_packet.py` Layer 5 student response pages (lines 1240–1480) — this is the gold standard for student page layout.

---

## CAP Language Rules — HARD RULES (apply to every CAP, every product line)

These rules govern how vocabulary access is framed in every Communication Access Packet. Violations here create products that contradict the CbD capacity-building framework.

1. **No SLP-as-gatekeeper language.** The SLP is a team member — not the lead, not the decision-maker for vocabulary access. Never write "SLP leads," "SLP decides," or structure the CAP so that a student is waiting for SLP action before they can participate.

2. **Two-tier access framing required in every CAP:**
   - Tier 1 (immediate): Symbol cards, e-trans boards, printed choice boards — any team member can provide these on Day 1, no SLP involvement required.
   - Tier 2 (team conversation): What goes on the SGD is a separate, student-driven team discussion. The CAP supplies the vocabulary list; it does not decide what gets programmed.

3. **No single word = one cell assumption.** When writing CAP guidance about SGD programming, always note that phrase banks, sentence starters, and fillers should be considered alongside individual words. "I think the poet means ___" as one button reduces motor planning more than 5 individual word selections.

4. **Student interest drives fringe programming — say this explicitly.** A student who demonstrates understanding via low-tech has met the standard. Whether fringe words go on the SGD depends on whether the student will use them again — not on whether the unit includes them.

5. **Checklist headers and role tables must use team framing:**
   - ❌ "SLP Pre-Programming Checklist"
   - ✅ "Vocabulary Access Checklist" or "Communication Team Checklist"
   - ❌ "SLP | Leads pre-programming"
   - ✅ "SLP | Contributes fringe vocabulary list for potential SGD programming"

6. **"Communication team" is the unit of responsibility** — not any single role. The special educator, para, SLP, and classroom teacher all share ownership of vocabulary access.

## Student Packet / Printable Packet Standards — HARD RULES

These rules apply to ALL student-facing printable PDFs across every product line: nonfiction Printable Packets, fiction Printable Packets, poetry Student Packets, picture book companion student pages, UFLI lesson packets.

**RULE 1 — Student packets are print-first, b&w by default.**
The standard CbD student should be able to print any student-facing packet on a black-and-white laser printer and have it be fully usable. Color is an enhancement, not a requirement. If a page does not work in grayscale, it fails the print standard.

**What this means in practice:**
- Navy/teal/violet backgrounds = ❌ not on student pages (teacher pages only)
- Color-filled section headers spanning full width = ❌ on student pages
- Thin hairline borders on response boxes, lightly shaded label bars, or bold black text for section names = ✅
- Fitzgerald Key category color bars on symbol cards = ✅ (small, functional, clearly labeled — these are the exception)
- Navy footer strip = ✅ (standard across all pages — narrow, not dominant)

**RULE 2 — Look at the nonfiction and fiction Printable Packets as the reference.**
Before building any student-facing PDF, look at an existing product's student pages:
- `Products/Nonfiction Units/[any unit]/[unit]_Printable_Kit.pdf`
- `Products/Fiction Anchor Texts/Wonder - Character Analysis/Wonder_Character_Analysis_Printable_Packet.pdf`

These are the structural gold standard. Match the layout density, border weight, label style, and color use.

**RULE 3 — Structure beats design on student pages.**
Student activity pages prioritize:
1. Clear activity heading (bold, black, left-aligned or centered — not inside a colored box)
2. Brief instruction line
3. Response area (lines, boxes, T-chart, draw space) — generous white space
4. Vocabulary strip or FK cards if applicable (bottom of page)
5. Footer (unit name + page number)

Do NOT add: full-width colored header bands, heavy background fills, decorative color blocks, or anything that looks like a Canva graphic template.

**RULE 4 — Violation flag.**
If you are building a student packet and any of these are true, stop and correct before running:
- Background color on student response pages (anything that isn't white or very light gray)
- Font size below 11pt on student-facing instruction text
- Response area smaller than 2 inches tall (lines) or 1.5 inches (draw box)
- Color-only differentiation (no b&w equivalent for FK colors or status indicators)

**RULE 5 — The CAP and Session Tracker are NOT student packets.**
CAPs and Session Trackers are teacher/team documents. They can use CbD teal headers, section color bars, and structured design elements. The student packet is the separate printable the student actually holds. Never confuse the two in terms of design standards.

## Session Tracker and Data Roll-Up Rules — HARD RULES

These rules prevent building new data trackers from scratch when a shared standard tracker already exists.

**THE ONE SHARED TRACKER:**
`Products/Nonfiction Units/AAC_Communication_Session_Tracker.pdf`
This is the single authoritative roll-up tracker for ALL CbD product lines — nonfiction, fiction, picture book companions, poetry, UFLI. It is NOT a nonfiction-only file. Its location in the Nonfiction Units folder is historical; its purpose is cross-product.

**RULE 1 — Always append the shared tracker to every CAP.**
Every `build_[x]_cap.py` must merge `AAC_Communication_Session_Tracker.pdf` as the final page(s) of the CAP output. Use `pypdf` PdfReader/PdfWriter. If the shared tracker file is not found, print a warning — never silently skip.

**RULE 2 — Path formula from any unit folder:**
```python
import os
BASE = os.path.dirname(os.path.abspath(__file__))   # e.g. Unit 1 - What the Voice Carries/
# Products/ is two levels up from a unit inside a product-line subfolder:
SHARED_TRACKER = os.path.join(BASE, "..", "..", "Nonfiction Units", "AAC_Communication_Session_Tracker.pdf")
# From a nonfiction unit (already inside Nonfiction Units/):
# SHARED_TRACKER = os.path.join(BASE, "..", "AAC_Communication_Session_Tracker.pdf")
```
Adjust the number of `..` levels based on where the unit folder sits in the Products tree. NEVER hardcode absolute paths.

**RULE 3 — Unit-specific trackers are ALLOWED — but they are not the roll-up.**
A `build_[x]_session_tracker.py` that creates a per-poem, per-chapter, or per-lesson quick-score tracking PDF is fine and expected. These capture granular in-session data. They do NOT replace the shared tracker — they supplement it. The shared tracker is where para data feeds IEP-level reporting.

**RULE 4 — Violation flag.**
If you are about to write a new standalone Session Tracker PDF that:
- Has no reference to `AAC_Communication_Session_Tracker.pdf`
- Is appended to a CAP without also appending the shared tracker
- Recreates IEP-level goal tracking fields that already exist in the shared tracker

…STOP. That is the violation. Add the shared tracker append to the CAP instead.

**RULE 5 — Merge pattern (copy/paste into every CAP build function):**
```python
from pypdf import PdfReader, PdfWriter
import io, os

SHARED_TRACKER = os.path.join(BASE, "..", "..", "Nonfiction Units", "AAC_Communication_Session_Tracker.pdf")

writer = PdfWriter()
sources = [
    PdfReader(io.BytesIO(cover_bytes)),
    PdfReader(io.BytesIO(inner_bytes)),
    # add other unit-specific sections here
]
if os.path.exists(SHARED_TRACKER):
    sources.append(PdfReader(SHARED_TRACKER))
else:
    print(f"⚠️  Shared tracker not found: {SHARED_TRACKER}")

for src in sources:
    for page in src.pages:
        writer.add_page(page)

buf = io.BytesIO()
writer.write(buf)
```

## Symbol Card PDF Template
`_Operations/cbd_symbol_cards.py` (ReportLab) — STANDARD card generator for ALL product lines.
Usage: `from cbd_symbol_cards import build_symbol_cards; build_symbol_cards(unit_title, words, output_path)`
Words format: `[{"word": "think", "type": "core"}, ...]`
Install: `pip install reportlab --break-system-packages`

**HARD RULES — apply to every symbol card in every product (standalone decks, CAP inline cards, student packet cards):**

1. **Always call `build_symbol_cards()` — NEVER recreate card layout inline.** Even when embedding cards inside a CAP or packet, call the shared function. Do not write a new `draw_card()` or `card_cell()` function in any unit build script.
2. **3 zones only — no extra content:**
   - Zone 1: Fitzgerald category bar + color dot + category label (e.g., "NOUNS", "ACTIONS")
   - Zone 2: ARASAAC symbol with Fitzgerald-color border — OR empty "draw it ✏" box if no symbol exists
   - Zone 3: Word (bold, Fitzgerald word color) + POS sublabel underneath — nothing else
3. **No notes, definitions, context phrases, or instructional text on any card.** The card is a visual referent, not a teaching tool. Teaching language belongs in the teacher guide and CAP reference tables — not on the card itself.
4. **Text-label cards (no ARASAAC symbol available):** Same 3-zone structure. Zone 2 = empty drawing box with "draw it ✏" tucked top-right. Zone 3 = word + POS label. Still no definitions.
5. **Word data passed to `build_symbol_cards()` is always `{"word": str, "type": "core"|"fringe"}` — no notes field.** If you catch yourself adding a third key to the word dict, that's the violation: stop and remove it.

**Why this matters:** Cards are used by students and paras during instruction. Extra text creates visual noise, is inaccessible at gaze distance, and adds content that hasn't been vetted for strengths-based language or AAC phrasing standards.

## Fiction Anchor Text Line
- Concept: Evidence-based instructional activities anchored to fiction texts — designed for ALL students, not SPED-specific. Differentiated for SPED, LD, MLL, and AAC users.
- Workflow: `_Operations/CbD_Production_Workflows.xlsx` → 📖 Fiction Workflow tab (9-phase, 48-step)
- Pricing: TBD

## Core Beliefs

### Capacity-Building Approach to AT (RESNA)
> "The capacity-building approach focuses on increasing the knowledge and skills of education-related professionals in active service through different types of training, including individual coaching, group presentations, and the creation of on-demand resources… the capacity-building approach looks for ways to equip all members of a student's team to take responsibility for AT services that are within their scope of practice."
> — RESNA Position Paper on AT Specialists in PreK-12 Educational Settings

**CbD is the capacity-building infrastructure.** Every resource, post, and tool builds the whole team — not just specialists.

### AT Device Definition
**IDEA/Tech Act (1988):** "Any item, piece of equipment, or product system, whether acquired commercially off the shelf, modified, or customized, that is used to increase, maintain, or improve functional capabilities of individuals with disabilities."
**WHO (2018):** "Products that maintain or improve an individual's functioning and independence, thereby promoting their well-being."

## QC Checklists by Product Line

| Product Line | QC File | When to Run |
|---|---|---|
| UFLI Phonics | `_Operations/QC/UFLI_QC_Evaluation_Rubric.md` | Before publishing any UFLI lesson packet |
| Picture Book Companions | `_Operations/QC/PictureBook_Companion_QC_Checklist.md` | Phase 1 (pre-build on DRAFT.md) + Phase 2 (post-build on .docx) + Phase 3 (pre-PDF export) |

**Picture Book Companion QC covers:** Phase 1 (content + language + brand), Phase 1B (symbol pre-build — fetch, FK classification, core/fringe tagging, symbol page structure, comm board sizing, attribution), Phase 2 (page density, insert page breaks, print fidelity, orphaned headings, response box sizing), Phase 3 (pre-export final checks). Phase 1B must pass before any build script runs.

---

## Canonical File Paths (updated 2026-03-29)
| File | Actual Location |
|------|----------------|
| Launch Calendar | `Distrubution/Teachers Pay Teachers/CbD_TPT_Launch_Calendar.xlsx` |
| SEO Keyword Research | `Marketing/SEO Reports/CbD_SEO_Keyword_Research.xlsx` |
| SEO Audits | `Marketing/SEO Reports/` |
| TPT Strategy docs, CSVs | `Distrubution/Teachers Pay Teachers/` |
| Unit Design Master Reference | `_Operations/memory/CbD_Unit_Design_Master_Reference.md` |
| Accessible Document Research | `Research/CbD_Accessible_Document_Research_and_Plan.md` |
| TPT Inventory tracking CSV | `Distrubution/Teachers Pay Teachers/data.csv` |
| AAC Trading Card deck folders | `Products/AAC Trading Cards/[Deck Name]/` (flat — no nested subfolder) |

## Business Expenses
Tracker: `_Operations/CbD_Business_Budget.xlsx` (Expenses tab + Print Orders tab)
First prototype order: Order #82750 (9 Cent Copy, 2026-03-24) — UFLI spiral-bound guide + trading cards + tax = $60.00

# Build System Reference

Deep build notes for CbD. Pull this file when doing code/build work.

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

## Build Scripts Reference

| Product | Build Script | Output |
|---------|-------------|--------|
| 504 Sit-In | `_Operations/build_504_sit_in.js` | 504_Sit_In_COMPLETE.docx |
| Frances Kelsey | `Products/Nonfiction Units/Frances Kelsey/build_frances_kelsey.js` | Frances_Kelsey_Unit_v2.docx |
| Capitol Crawl | `Products/Nonfiction Units/Capitol Crawl/build_capitol_crawl.js` | — |
| Zitkala-Ša | `Products/Nonfiction Units/Zitkala-Sa/build_zitkala_sa.js` | — |
| Radium Girls | `Products/Nonfiction Units/Radium Girls/build_radium_girls.js` | — |
| Keiko | `Products/Nonfiction Units/Keiko/build_keiko.js` | — |
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

- Vocab config: `_Operations/nonfiction_unit_vocab.js` (all 6 units, 248 total words)
- Default access level: Level 2 (4/row, 1.25", eye gaze/direct selection)
- Kit builder: `_Operations/build_unit_printable_kit.js`

## Symbol Card PDF Template
`_Operations/cbd_symbol_cards.py` (ReportLab) — STANDARD card generator for ALL product lines.
Usage: `from cbd_symbol_cards import build_symbol_cards; build_symbol_cards(unit_title, words, output_path)`
Words format: `[{"word": "think", "type": "core"}, ...]`
Install: `pip install reportlab --break-system-packages`
Do NOT create new card generators per unit — always use this template.

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

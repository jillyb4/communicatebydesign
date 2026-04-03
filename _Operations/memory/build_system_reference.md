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

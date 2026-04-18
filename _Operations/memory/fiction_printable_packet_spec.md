# Fiction Printable Packet — Build Specification

**Established:** 2026-03-29
**Status:** LOCKED — do not build without reading this first

---

## Standard Product Folder Structure (LOCKED 2026-04-17)

Every fiction unit uses this identical folder layout. Apply to all new units at build time.

```
[Title] - [Skill]/
├── Builds/                          ← all build scripts for this unit
│   ├── build_[unit].js
│   ├── build_[unit]_printable_packet.py
│   └── build_[unit]_welcome.py
├── Product Files/                   ← source-of-truth product files
│   ├── [Unit]_Teaching_Materials.docx
│   ├── [Unit]_Printable_Packet.pdf
│   └── [Unit]_Welcome_to_the_Product.pdf
├── TPT Product Files/               ← upload-ready set (4 files + zip)
│   ├── [Unit]_Teaching_Materials.docx
│   ├── [Unit]_Printable_Packet.pdf
│   ├── [Unit]_Welcome_to_the_Product.pdf
│   ├── [Unit]_TPT_Preview.pdf
│   └── [Unit]_TPT.zip
└── Marketing/
    ├── [Unit]_Marketing_Plan.md     ← ALL copy: TPT title/description/tags, pins, socials, FB drop, bundle strategy
    ├── [Unit]_Canva_BulkImport.csv  ← one row, for this unit only
    ├── [Unit]_Tailwind.csv          ← when built
    └── Images/
        ├── [Unit]_Image2_CommBoard.png
        ├── [Unit]_Image3_SymbolCards.png
        ├── [Unit]_Image4_PartnerSetup.png
        ├── [Unit]_Image5_StudentActivity1.png
        └── [Unit]_Image6_StudentActivity2.png
```

**Rules:**
- Everything for a product lives inside that product's folder — no files scattered across Distribution/ or Marketing/
- Marketing_Plan.md is the single file you open for any copy/paste task (TPT listing, pin text, FB drop, Canva import path)
- Canva CSV is per-unit — one row, lives in Marketing/ not in Distribution/Pinterest/
- Images are per-unit — in Marketing/Images/ not in a shared Marketing/ folder elsewhere
- Build scripts live in Builds/ — not in the root of the unit folder

**Stale items to clean up in Finder (cannot delete via code — iCloud permissions):**
- Old `[Unit]_TPT/` subfolder (now replaced by `TPT Product Files/`)
- Old `[Unit]_TPT_Listing_Package.md` in unit root (now `Marketing/[Unit]_Marketing_Plan.md`)
- Old build scripts in unit root (now in `Builds/`)
- Old loose docx/pdf files in unit root (now in `Product Files/`)
- Shared `Marketing/Product Images/Fiction Anchor Texts/` folder (images now per-unit)
- Shared `Distrubution/Pinterest/Fiction_Canva_BulkImport.csv` (now per-unit)
- Shared `Distrubution/Teachers Pay Teachers/Fiction_TPT_BulkImport.csv` (superseded — use per-unit Marketing_Plan.md)

---

## What It Is

A purpose-designed printable (**13 pages for Wonder; 7–9 pages baseline**) that gives any team — regardless of a
student's current AAC access level — exactly what they need to run a fiction
anchor text unit with complex communicators, while systematically building a
vocabulary library.

**What it is NOT:** An extraction from the unit PDF (that is the nonfiction model).
Not a standalone lesson. Not a replacement for the book or the teacher's existing
ELA differentiation.

Fiction units are supplements. Teachers already have the book. What Communicate by
Design adds is the AAC and language access layer that most supplements don't include.
This is more like the UFLI supplement model — highly targeted, evidence-based,
filling the specific gap.

---

## AAC Design Philosophy (Embedded in Every Layer)

The student is managing stacked cognitive load: holding the idea + locating the
word on the board or device + executing the motor plan + building the next word,
simultaneously. Students with AAC may also have LD — working memory is not a
bonus resource. It is the bottleneck.

**Framework:**
Teach → Model → Identify barriers → Remove barriers → Continue teaching →
Presume competency → When it comes together, the rigor was always there.

We do not stop at the first page of core because the student can't yet navigate
to it. We build the access so that as motor planning, working memory, and navigation
develop, the vocabulary library is already there.

**The ecosystem is tandem, not singular:**
Device + low-tech gaze board + symbol cards + word cards + switches + sentence
starters. Different access points for different moments. All of them working together.

---

## Packet Structure (13 pages — Wonder build; 7–9 pages baseline)

| Page(s) | Layer | Content |
|---------|-------|---------|
| 1 | Layer 1: Communication Environment Setup | Partner reference — modes, prompt hierarchy, barrier check |
| 2–3 | Layer 2: Vocabulary Access | Symbol cards — core Set A (12 words) + fringe Set A (12 words, chapter order) |
| 4–6 | Layer 3: Communication Boards | Board A: Character Description (landscape) · Board B: Emotion + Reasoning · Board C: Literary Discussion Moves |
| 7 | Layer 4a: Unit Vocabulary Map | Cumulative library tracker — all unit words with tracking circles |
| 8–9 | Layer 4b: AAC Session Tracker | Appended unchanged |
| 10–14 | **Layer 5: Student Response Pages** | **NEW (Session 21).** One print-ready student response page per Part (5 total). Each: Part bar, student info row, teal prompt box, FK vocabulary strip, response area, annotation code chips, footer. Response types: draw box · T-chart · sentence frame + lines · before/after columns · sentence starters + lines |

**Note:** Layer 5 added in Session 21. Wonder build = 13 pages. Baseline (new fiction units) starts at 4 layers / 9 pages; add Layer 5 student pages when building.

---

## Layer 1: Communication Environment Setup (1 page)

Not a training manual. What a para or teacher needs IN HAND during the lesson.

**Contents:**

**Partner Mode guide** — all 3 modes with explicit when-to-use:
- Mode 1: Instructional — prompt hierarchy + data collection. Use during targeted
  communication skill instruction.
- Mode 2: Partnership — no demands, follow student lead, note spontaneous comms.
  Use during reading, discussion, exploration.
- Mode 3: Facilitated Participation — enable access only, no interpretation.
  Use when student is engaging with the text independently.
- ⚠️ Note: Defaulting to Mode 1 all day is the #1 AAC barrier. Most partners
  were never taught when to switch.

**5-level prompt hierarchy** (compact visual — Mode 1 only):
1. Wait (3–5 seconds minimum)
2. Indirect Cue — gesture toward communication system
3. Direct Cue — point to specific symbol/location
4. Verbal Model — say the word + show it on the system
5. Reassess Access — non-response = environment data, not intent failure

**Barrier check** (5 items, circle before each session):
- Wait time given? ○ Yes ○ No
- Student positioned for their access method? ○ Yes ○ No
- Lighting adequate for symbol visibility? ○ Yes ○ No
- Access method available and within reach? ○ Yes ○ No
- Symbols/board positioned correctly? ○ Yes ○ No

**Tools + Access quick reference** — pre-filled with the tools in this unit's
packet. Partner knows what they're working with before the session starts.

**Print cadence:** One per team, not one per session. Laminate recommended.

---

## Layer 2: Vocabulary Access (2–3 pages)

**Card format (identical to nonfiction Communication Access Packet):**
- Card size: 2"×2" (144pt × 144pt)
- Grid: 3 columns × 4 rows = 12 per page
- Style: white center, Fitzgerald Key colored border (3pt), 10pt white gap between cards
- Symbol: 88pt ARASAAC PNG from `_Operations/symbol_cache/arasaac_[word].png`
- Word label: 13pt Helvetica-Bold, navy (#1B1F3B), centered, uppercase
- No category name text on card — color border IS the Fitzgerald Key indicator

**⚠️ This is NOT the 2.5"×3.5" UFLI trading card format. Do not use build_unit_printable_kit.js.**

**Fitzgerald Key colors:**
- Green (#00A86B bg #E8F5E9) — Verbs / Actions
- Orange (#FF8C00 bg #FFF3E0) — Descriptions / Adjectives
- Yellow (#D4A800 bg #FFF8DC) — People / Pronouns
- Brown (#8B6914 bg #FFF5D6) — Nouns
- Blue (#4A90D9 bg #E3F2FD) — Little Words / Prepositions
- Pink (#E88CA5 bg #FCE4EC) — Social / Feelings

---

### ⚠️ Two vocabulary sets — keep them separate throughout

**VOCABULARY SET A — SDI Instruction Targets**
Source: `_Operations/cbd_unit_vocab.js` — the unit's entry in the master
vocabulary database. These are the words the team explicitly models, tracks on
the Session Tracker, and adds to the Vocabulary Map. Fewer words, targeted focus.
For Wonder: 12 core + 12 fringe = 24 words.

These words appear on: symbol card pages (Layer 2), Vocabulary Map (Layer 4a),
Session Tracker "Core Word / Vocabulary Use" section.

**VOCABULARY SET B — Communication Board Vocabulary**
Broader than Set A. All the words a student needs to participate in the unit's
activities — discussion moves, evidence-citing language, literary structure frames,
and response connectors. Many are already on the student's device. All must be on
the communication board during activities.

Includes: all Set A words PLUS discussion moves ("I think...", "I feel...", "Because...",
"I agree...", "I disagree..."), evidence language ("The evidence shows...", "On page...",
"This shows..."), annotation code symbols ([TRAIT] / [WHY] / [CHANGE]), motivation
connectors (because, maybe, probably), Write-Ables frame starters.

These words appear on: Communication Board (Layer 3) only — NOT all on symbol card pages.

**Rule: Layer 2 = Set A only. Layer 3 = Set B (which includes Set A).**

---

**Symbol card pages (Layer 2 — 2 sets):**

**Core word cards** (1–2 pages):
- Set A core words only — the SDI instruction targets that are core vocabulary
- Organized by Fitzgerald Key category
- Maximum 12 per page — do NOT compress to fit more

**Fringe word cards** (1–2 pages):
- Set A fringe words only — the unit-specific SDI instruction targets
- Organized by WHERE IN THE BOOK they first appear (chapter/section), NOT alphabetically
- Section header: "Unit-Specific Vocabulary — Fringe SDI Targets"
- Language note: "Students may use printed cards, symbols from an existing symbol
  set, or programmed device pages."

**No device-assumption language anywhere.** Never: "pre-program," "program your
device," "SGD required." Never assume fringe words are on a student's current system.
**No team direction language on student-facing or vocabulary-facing pages.** Never:
"confirm with AAC team," "consult the team," "check with your SLP." These belong
in teacher guidance only, not on cards or packet pages.

---

## Layer 3: Communication Boards for Activities (2–3 pages)

Layer 3 contains THREE boards. Each is designed to be laminated and reused.
Print all three before the unit begins.

**Cell size rule for all boards:** Minimum 2"×2" per cell. Students using gaze
or partner-assisted scanning need more real estate than symbol cards. Never compress.
**Language rule for all boards:** Neutral verbs only — "indicate," "select," "identify."
Never "point to" as the sole interaction verb.

---

### Board A: Character Description Board (1 page — used in Part 1 and throughout)

Organized by description category. This is the access layer for Describe to Draw
and any activity that asks "who is this character?" It is NOT name-recall —
it is description construction.

| Category | Vocabulary on board |
|----------|-------------------|
| LOOKS LIKE | big / small / old / young / wears / carries / [face looks different] |
| DOES | runs / hides / fights / cries / laughs / helps / leaves / saves / lies / tells the truth |
| FEELS | sad / scared / happy / alone / angry / confused / proud / brave / worried |
| WANTS | want / belong / friend / kind / choose / invisible / ordinary / different |

Each cell: ARASAAC symbol + word label. Fitzgerald Key color borders.
Students build a character description by selecting across rows — one attribute at a time.
Partner records. Description builds into evidence.

---

### Board B: Emotion + Reasoning Board (1 page — used Before Reading and throughout)

Pre-loaded with Wonder-specific emotional and mental state vocabulary.
Used before and during reading for spontaneous communication (Mode 2)
AND for activity responses (Mode 1).

**Emotional vocabulary:** feel / sad / scared / happy / alone / angry / confused /
proud / brave / worried / kind / different / belong / invisible

**Reasoning connectors** (prominent placement — core vocabulary for Parts 3–4):
because / maybe / probably / think / know / change

These are core vocabulary words already on most devices — but they need to be
prominent on this board because they carry the inference and motivation work of
Parts 3 and 4. Placement matters: they should be in a distinct row or section,
not buried in the grid.

---

### Board C: Literary Discussion Moves Board (1 page — used during all activities)

The literary MOVES the unit requires: discussion, evidence citing, and annotation.
Not a sentence frame worksheet — a communication board.

*Discussion moves:*
"I think..." | "I feel..." | "The character..." | "I agree..." | "I disagree..." | "Because..."

*Citing evidence:*
"The evidence shows..." | "On page..." | "The author says..." | "This shows..."

*Unit annotation codes* (Wonder-specific — LOCKED 2026-03-29):
[TRAIT] — who the character is
[WHY] — why they act that way
[CHANGE] — how the character changes

All three annotation codes as symbol + word + bracketed code.

**Reuse:** Laminate all three boards. Use throughout the unit.
Board A is most active in Parts 1–2. Board B throughout. Board C in all parts.

---

## Layer 4a: Unit Vocabulary Map (1 page)

**What it is:** The cumulative unit-level picture of vocabulary growth. Different
from the Session Tracker — this shows the library being built across the whole unit.

**Format:** Table, landscape preferred.

Pre-filled template:

| Word | Type | Introduced | Modeled | Spontaneous Use | Generalized | Notes |
|------|------|:----------:|:-------:|:---------------:|:-----------:|-------|
| feel | core | ○ | ○ | ○ | ○ | |
| ... | | | | | | |

**Required header:** "Building a Vocabulary Library: [Unit Title]"

**Required note on page:**
"These words belong to this student's permanent vocabulary library — not just this
unit. Words marked Generalized are ready to add to their AAC system or communication
book."

**Fill cadence:** Team fills across the full unit, not session by session. The
Session Tracker (Layer 4b) captures the per-session data; this captures the arc.

---

## Layer 4b: AAC Session Tracker (1 page — appended)

Append `Products/Nonfiction Units/AAC_Communication_Session_Tracker.pdf` unchanged.
Same tracker used across all CbD units — universal, already designed, carry forward.

**How the layers connect to the tracker:**
- Layer 1 → informs what partner circles in the Tools/Access header
- Layer 2 → vocabulary cards are what goes in "Core Word / Vocabulary Use" section
- Layer 3 → literary moves are the "Communication Targets" rows
- Mastery Decision checkboxes → "Add vocabulary to device" = library action
- Layer 4a → accumulates the check/M/*/— data across sessions into the unit picture

**Footer note on packet:** "Print one per session. Transfer data to the Universal
AAC Communication Data Tracker."

---

## QC Checklist — Fiction Printable Packet

Run before marking packet complete. Every item must pass.

### Access (non-negotiable)
1. ☐ Every component functions without an SGD — works with e-trans board, symbol exchange, alternative pencil, partner-assisted scanning
2. ☐ No device-assumption language anywhere ("pre-program," "program your device," "SGD required")
3. ☐ Fringe words labeled for full AAC team coordination — not "have the SLP do it"
4. ☐ Core board: maximum 12 per page, appropriate cell size for gaze access
5. ☐ Communication board: minimum 2"×2" per cell

### Language
6. ☐ Sentence starter board uses neutral verbs only — never "point to" as sole verb
7. ☐ No ability-sorting language anywhere in the packet
8. ☐ Vocabulary map uses "permanent library" framing — not "unit words"
9. ☐ No SLP gatekeeping: fringe coordination note names "the team," not "the SLP"
10. ☐ Input level ≠ output level is preserved — access method does not lower the expectation

### Partner Support — Layer 1
11. ☐ All 3 partner modes present with when-to-use guidance
12. ☐ Prompt hierarchy visible with "Reassess Access" as 5th level
13. ☐ Mode 1 default warning present
14. ☐ Non-response framing: "environment data, not intent failure"

### Vocabulary — Layer 2
15. ☐ Core and fringe are separate card sets — never mixed
16. ☐ Fringe cards organized by chapter/section appearance, not alphabetically
17. ☐ Symbol present for every word OR `(no symbol)` placeholder — no blank cells
18. ☐ Fitzgerald Key color border correct for each word's category
19. ☐ Card format: 2"×2", 3×4 grid, white center, 88pt symbol, 13pt label

### Communication Boards — Layer 3 (3 boards required)
20. ☐ Board A (Description): 4 categories present — LOOKS LIKE / DOES / FEELS / WANTS
21. ☐ Board B (Emotion + Reasoning): emotional vocabulary present + reasoning connectors (because / maybe / probably) in distinct placement
22. ☐ Board C (Literary Moves): discussion moves + evidence citing + all 3 annotation codes present
23. ☐ Annotation codes match the unit's locked 3-code set
24. ☐ All boards minimum 2"×2" cell size — not compressed
25. ☐ All boards designed to be laminated and reused (noted on page)

### Vocabulary Map — Layer 4a
26. ☐ All unit words pre-filled
27. ☐ Columns: Word | Type | Introduced | Modeled | Spontaneous | Generalized | Notes
28. ☐ "Permanent library" language present on page
29. ☐ "Ready to add to AAC system" note on Generalized column or footer

### Brand + Structure
30. ☐ Session Tracker is final page, appended unchanged
31. ☐ Running header on all built pages: italic unit title (left) + COMMUNICATE (teal #006DA0) BY DESIGN (amber #FFB703) (right)
32. ☐ Footer: `[Unit Title] · Fiction Printable Packet · Communicate by Design · teacherspayteachers.com/store/communicate-by-design`
33. ☐ Teal = #006DA0 | Navy = #1B1F3B | Amber = #FFB703

---

---

## Print Standards — LOCKED (2026-04-17)

These rules apply to every page of every fiction printable packet. No exceptions.

### Color treatment
- **FK color = border only.** All symbol card cells, communication board cells,
  vocabulary chips, and annotation code chips use white fill + FK colored border.
  Never use FK background fills — they print as undifferentiated gray on B&W copiers
  and waste ink on color printers.
- **Section header bars** (Board B/C category labels): white fill + colored left
  accent bar (3pt) + navy text. Never solid fill with reversed white text.
- **Column headers** (Before/After, T-chart, comparison columns): white fill +
  colored border + navy text. Never solid fill with reversed white text.
- **The only solid fills allowed:** the Part label bar (navy, white text) and the
  teal left accent bar on response boxes — these are structural, not decorative.

### Response and writing areas
- **No fill where students write.** Response boxes, sentence frame boxes, draw
  boxes, column bodies: white only. No gray (#F8FAFC), no amber wash (#FFFBEB),
  no tinted fill of any kind.
- Structure comes from borders and the navy left accent bar, not from fill.
- Ruled lines on white: #94A3B8 at 0.75pt, 32pt spacing — wide enough for all
  access methods (pencil, stylus, e-trans scribe).

### Prompt language
- **Prompts ask the question. They do not narrate the page.**
- Never: "Use the sentence frame to get started," "Use the vocabulary strip,"
  "Use the starters below to begin," "Write or draw your ideas in the chart."
  The page shows those affordances. The prompt asks the literary question only.
- One exception: if referencing evidence count is part of the standard
  ("Use evidence from at least two parts of the book") — that is content, not navigation.

### Student info row
- **Fields: Name · Class · Teacher · Date.** Four fields, full width of the page.
- **Never:** "Name / AAC User," "AAC Student," or any disability-identifying label.
  Every student in the class fills in the same four fields. The worksheet does not
  signal who it was designed for.
- **Fill: white only.** No tinted background (#F0F9FF or similar) on the info row.
- This is locked across all fiction packets, all product lines, and the template system.

### AAC access language
- **AAC Access Note column** in vocab tables: two values only.
  - Core words: `"Core — part of most AAC ecosystems"`
  - Fringe words: `"Fringe — SDI target; include in communication packet"`
  No "confirm with," "coordinate with," "consult," or team direction of any kind.
- **Section notes** on symbol card pages: state what the words are and how they
  may be used. Never direct the team to consult anyone.
- **No team direction language anywhere on student-facing pages.**

---

## Build Method

**Tool:** Python/ReportLab — same toolchain as `_Operations/build_comm_access_packet.py`.
Gives precise layout control for cell sizing, gaze-access boards, and PDF appending.

**Per-unit script:** `build_[unit]_printable_packet.py` (in unit folder)
**Session Tracker source:** `Products/Nonfiction Units/AAC_Communication_Session_Tracker.pdf`
**Symbol source:** `_Operations/Symbols/symbol_cache/arasaac_[word].png`
⚠️ Use the full path `_Operations/Symbols/symbol_cache/` — NOT `_Operations/symbol_cache/` (wrong path, causes broken placeholder images)

### REQUIRED: Check the template system before designing any student activity page

Before writing any new canvas function or custom layout for Layer 5 student response pages:

1. **Read `_Operations/Build/cbd_worksheet_templates.py`** — the full template catalog.
2. **Check this list first:**
   - `make_mcq_page()` — multiple choice
   - `make_short_answer_page()` — open response + optional sentence frame + word bank + annotation codes
   - `make_cer_page()` — Claim-Evidence-Reasoning + annotation codes
   - `make_evidence_sort_page()` — 3-column sort
   - `make_vocab_preview_page()` — pre-teaching with Descriptive Teaching Model
   - `make_annotation_guide_page()` — annotation code reference page
   - `make_descriptor_board_page()` — Describe to Draw / attribute board
   - `make_before_after_page()` — 2-column comparison (Before/After, Cause/Effect, etc.)
   - `make_partner_prompt_card()` — CROWD/ALM partner guide (Teacher Packet only)
3. If the layout you need is already there → **use it, do not recreate it**.
4. If a genuinely new layout is needed → **add it to `cbd_worksheet_templates.py` as a named function first**, then call it from the unit build script. Never build one-off inline layouts inside a unit script.

This rule exists so every unit inherits every future improvement to print standards, color treatment, and language automatically.

**Build order (within full unit workflow):**
1. Unit docx complete + QC passed
2. Check template catalog (above) before writing any Layer 5 page code
3. Run printable packet script → `[Unit]_Fiction_Printable_Packet.pdf`
4. Run packet QC checklist (above)
5. Assemble TPT folder: unit docx + printable packet PDF + welcome/terms
6. **Build TPT preview PDF** — run BEFORE creating any TPT listing:
   - `python3 _Operations/Build/build_fiction_previews.py --unit [key]`
   - Output: `TPT Product Files/[Unit]_TPT_Preview.pdf` — lives with all other upload files, nowhere else
   - Preview = 8 pages: branded cover + 6 pages from printable packet (partner setup · symbol cards · Board A · Board C · Part 1 student page · Part 5 synthesis) + branded back
   - To add a new unit to the registry: add an entry to `UNITS` in `build_fiction_previews.py`
7. Run `python3 _Operations/Build/export_fiction_marketing_images.py --title "[Unit]"` → exports 5 marketing PNGs to **`[Unit Folder]/Marketing/Images/`** (per-unit — NOT a shared folder)
8. Upload all 5 PNGs to Canva media library
9. Open Canva fiction bulk pin template `DAHGBZ-LtRo` → add unit page → export cover PNG (Image 1)
   - **Canva bulk import CSV:** `[Unit Folder]/Marketing/[Unit]_Canva_BulkImport.csv` (per-unit — NOT in Distrubution/Pinterest/)
   - Fill: Product Name, SubHeading, Essential Question, Skill, Standard, Learning Target, TPT Grade Levels, tpt_url, image2_filename (CommBoard), image3_filename (StudentActivity1)
   - Upload image PNGs to Canva media library first, then run Bulk Create → import CSV
10. All TPT copy lives in **`[Unit Folder]/Marketing/[Unit]_Marketing_Plan.md`** — TPT title/description/tags, all 3 Pinterest pins, Instagram caption, FB drop, seasonal hooks, bundle strategy. No shared TPT bulk import CSV.
11. Hand off to Jill: she completes Image 1 + Image 2/3 Canva templates, then gives Claude 3 Canva image URLs + TPT product URL → Claude builds 3 Pinterest pins + social post

---

## 5-Image Marketing Standard — LOCKED (2026-04-17)

| Image | Content | Source |
|-------|---------|--------|
| **Image 1** | Cover | Canva bulk template `DAHGBZ-LtRo` — Jill exports |
| **Image 2** | Communication Board A — Character/Theme Vocabulary (landscape) | Printable Packet p.4 (idx 3) |
| **Image 3** | Core Word Symbol Cards — Set A | Printable Packet p.2 (idx 1) |
| **Image 4** | Partner/Communication Environment Setup page | Printable Packet p.1 (idx 0) |
| **Image 5** | Student Activity Part 1 — first response page | Printable Packet p.9 (idx 8) |
| **Image 6** | Student Activity Part 2 — second response page | Printable Packet p.10 (idx 9) |

**Export script:** `_Operations/Build/export_fiction_marketing_images.py`
**Output folder (LOCKED 2026-04-17):** `[Unit Folder]/Marketing/Images/` — per-unit, NOT a shared folder
**Naming:** `[Key]_Image2_CommBoard.png` · `[Key]_Image3_SymbolCards.png` · `[Key]_Image4_PartnerSetup.png` · `[Key]_Image5_StudentActivity1.png` · `[Key]_Image6_StudentActivity2.png`

To add a new unit to the registry, add an entry to `FICTION_UNITS` in the export script.

**Marketing Plan (replaces all shared CSVs):** `[Unit Folder]/Marketing/[Unit]_Marketing_Plan.md`
One file per unit. Contains ALL copy: TPT title/description/tags, all 3 Pinterest pin titles+descriptions+alt text, Instagram caption, FB group drop, seasonal hooks, bundle strategy, pre-listing checklist, metadata table with TPT ID + URL. Open this file for any copy/paste task — nothing else needed.

**Wonder script (first fiction unit):**
`Products/Fiction Anchor Texts/Wonder - Character Analysis/build_wonder_printable_packet.py`

---

## Wonder: Character Analysis — Packet Specifics

**Annotation codes (LOCKED 2026-03-29):**
- [TRAIT] — who the character is (description, appearance, personality, what they do)
- [WHY] — why they act that way (motivation, internal feelings, cause)
- [CHANGE] — how the character changes (before/after, growth, resolution)

**SDI instruction targets — Set A (cbd_unit_vocab.js entry #7):**
- Core (12): feel, want, think, know, change, because, maybe, sad, scared, happy, alone, kind
- Fringe (12): different, belong, invisible, brave, loyal, bully, ordinary, friend, helmet, school, choose, face looks different

**Missing symbols (8) — fetch from ARASAAC before building packet:**
alone, belong, invisible, loyal, bully, ordinary, helmet, face looks different

**Board A vocabulary (Character Description):**
LOOKS LIKE: big, small, old, young, wears, carries, face looks different
DOES: runs, hides, fights, cries, laughs, helps, leaves, saves, lies, tells the truth
FEELS: sad, scared, happy, alone, angry, confused, proud, brave, worried
WANTS: want, belong, friend, kind, choose, invisible, ordinary, different

**Board B vocabulary (Emotion + Reasoning):**
Emotional: feel, sad, scared, happy, alone, angry, confused, proud, brave, worried, kind, different, belong, invisible
Reasoning connectors (prominent): because, maybe, probably, think, know, change

**Board C vocabulary (Literary Discussion Moves):**
Discussion: I think / I feel / the character / I agree / I disagree / because
Evidence: the evidence shows / on page / the author says / this shows
Annotation codes: [TRAIT] / [WHY] / [CHANGE]

**Comparison Board + Before/After Strip:**
Already built into main unit docx (Sections 8 and 10 of build_wonder_character_analysis.js).
Do NOT rebuild in the Printable Packet — they are student activity pages in the unit.

**Page count estimate:** 10–12 pages
- Layer 1: 1 page
- Layer 2: 3 pages (1 core + 2 fringe — 12+12 words at 12/page)
- Layer 3: 3 pages (Board A + Board B + Board C)
- Layer 4a: 1 page
- Layer 4b: 1 page (Session Tracker)
- Total: 9 pages + possible overflow

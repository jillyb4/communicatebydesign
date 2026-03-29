# CbD New Product Line Workflow
*Added: 2026-03-29 | Version 1.0*

**Purpose:** Before any new product line (or significant new product within an existing line) moves into build, it must pass through these phases in order. This workflow prevents building without a research foundation, vocabulary framework, or clear ecosystem fit.

**Rule:** Answer all Phase 0 and Phase 1 questions BEFORE any document draft, code, or build begins. If a question cannot be answered, that is the first task.

---

## Phase 0: Concept Validation (Before Anything Else)

These questions must be answered before a product line idea moves forward. If answers are not clear, do the research first.

### 0.1 — What is the instructional gap?

What is a real practitioner actually stuck on? Where is the evidence this gap exists?

Evidence sources (in priority order):
1. Facebook group posts from SPED teachers, SLPs, families with 100+ comments — these are confirmed needs
2. TPT search with no AAC-adapted results = confirmed market gap
3. Jill's direct classroom experience or consultation work
4. Session 18+ Airtable Work Items flagged as "Real Questions" from the field

**Decision gate:** Can we name one or two sentences that describe the problem this product solves for the practitioner in the room on Monday? If not, the idea is not ready.

### 0.2 — What ELA or literacy standard does this serve?

Every CbD product targets a specific standard or set of standards. Identify:
- ELA strand (RL / RI / L / foundational phonics / writing)
- Grade band
- Specific standard codes (e.g., RL.6.3 / RI.8.8)
- Which skill is the unit targeting? (One skill per unit — no exceptions)

**Decision gate:** If the product targets "general reading" or "general communication" without a standard anchor, it is not a CbD ELA product. It may be an AT/AAC product — use the AT/AAC IEP Team workflow instead.

### 0.3 — Who is the buyer persona?

| Persona | What they need | Pricing sensitivity |
|---------|---------------|---------------------|
| SPED teacher (sole buyer) | Ready-to-use; no SLP coordination required for basic use | Medium ($8–$15) |
| SLP (technical buyer) | Research citations, AAC precision, IEP goal language | Low (will pay more) |
| General ed + SPED co-teacher | Collaborative product; scaffolds that don't single out | Medium |
| Family / homeschool | Plain language, no jargon, accessible without specialist knowledge | High sensitivity |
| IEP team (group decision) | Administrators want compliance language; teachers want usability | Bundled |

One product = one primary persona. Secondary personas are fine, but the primary persona drives design decisions.

### 0.4 — Is there a competitor product?

Run a TPT search before claiming a gap. Identify:
- Who else sells this? (Kate Ahern, PrAACtical AAC, specialized SPED sellers)
- What do their products NOT include that CbD would?
- Is the CbD version differentiated by AAC access design, ELA standards depth, or research foundation?

**Decision gate:** If a strong competitor product exists without a meaningful CbD differentiator, this is not the right product to build first. Redirect energy to a clearer gap.

---

## Phase 1: Framework Application (Required Before Build)

### 1.1 — Vocabulary Framework Gate

This is required for every product. Answer these questions:

**A. What TYPE of vocabulary does this product involve?**

| Product Type | Vocabulary Type | Framework Section |
|--------------|----------------|------------------|
| UFLI Phonics | Decode targets (fixed — do not select) | Section 4a of full framework |
| Nonfiction reading unit | Tier 2 academic + Tier 3 content | Section 4b |
| Fiction anchor text | Emotional/mental state + narrative fringe | Section 4c |
| Picture book companion | IRA read-aloud + thematic conceptual | Section 4d |
| AT/AAC product | Functional communication vocabulary | Not yet fully defined — flag for research |
| Chapter book (future) | Sustained vocabulary across chapters | Section 4e (partial) |

**B. Does the existing vocabulary framework cover this product type?**
- If YES → load `_Operations/memory/vocabulary_selection_reference.md` and apply it
- If NO or PARTIAL → a vocabulary research session is required BEFORE build begins

**C. Can the 6-step word selection process be applied?**
Run through the 6 steps from the vocabulary reference. If any step produces "unknown" answers, that is the first build task — research first.

**D. Can the CAP (Communication Access Packet) be built for this product?**
- Are symbol sources available (ARASAAC)?
- Is the core/fringe word count reasonable (≤30 fringe)?
- Is there SLP handoff language defined?
- If NO to any of these → resolve before architecture decisions

**Decision gate:** If vocabulary type is unclear OR the framework doesn't cover it → the FIRST deliverable is a vocabulary research session that extends `Research/CbD_Vocabulary_Selection_Framework.md`. Build does not begin until framework coverage is confirmed.

### 1.2 — Research Foundation Gate

Every product line needs a research foundation document. Check:

- Does a research file exist in `Research/` that covers this product line?
  - Nonfiction: Partial (via nonfiction_build_reference.md + annotated evidence in units)
  - Fiction: ✅ `Fiction_Narrative_Research_Foundation.md`
  - UFLI: ✅ `CbD_Research_Reference_AAC_Phonics_Literacy.md` + `UFLI_AAC_Phonics_Research_Reference.md`
  - Picture Book Companions: ✅ `Picture_Book_Companions_Research_Foundation.md` (created 2026-03-29)
  - AT/AAC IEP Team: Partial (brand guidelines + accessibility docs)
  - Chapter Books: ⚠️ Not yet created

If no research file exists:
1. Create one using `Research_Template.md`
2. Answer: What professional organizations (ASHA, CEC, CAST, IRIS) ground this product?
3. What HLPs apply? (Every CbD product must map to at least 2 HLPs)
4. What does the research say a student with AAC needs to succeed with this content type?

### 1.3 — Product Architecture Decision

Define what files the product ships with:

| Required for every product | Notes |
|---------------------------|-------|
| Main content file (docx or PDF) | Built via `cbd_docx_template.js` or Python/ReportLab |
| Communication Access Packet (CAP) | 10-page standard (nonfiction) or adapted format |
| Symbol cards | 2"×2" ARASAAC grid, Fitzgerald Key borders |
| IEP goal stems | Minimum 3 per product |
| Partner mode guidance | Mode 1 / Mode 2 / Mode 3 described |
| Session tracker insert | Appended to CAP |

| Optional / line-specific | Trigger |
|--------------------------|---------|
| Printable Packet PDF (fiction) | Fiction Anchor Texts only — 4 layers, 9 pages |
| Lesson chips + interactive activity link | UFLI only |
| Visual Scene Displays | Fiction + Picture Book Companions (V2) |
| Trading Card companion deck | Triggered by `cbd_trading_cards.py` — any product with fringe vocabulary |
| Preview PDF (watermarked) | Every TPT listing that includes the main docx |

### 1.4 — Build System Check

Before writing any code:
- Does an existing build script cover this product? (`build_all_units.py`, `cbd_docx_template.js`, `build_covers_v2.py`)
- What new scripts or templates are needed?
- What is the folder structure for this product? (`Products/[Line]/[Product Name]/`)
- Has the Airtable Products table record been created for this product?
- Has the Launch Pipeline record been created?

### 1.5 — Brand and Identity Decision

| Decision | Where to find the answer |
|----------|--------------------------|
| Product line color | `Brand Assets/CbD-Brand-Guidelines.pdf` — not yet assigned for all lines |
| Cover type | Nonfiction = dark navy; Fiction = bright/light (TBD); K–3 = TBD |
| Footer Line 2 text | Defined per product line; fiction/K-3 TBD before first cover build |
| Hero illustration concept | Defined per title — must be decided before any cover build |
| Build script | Always `build_covers_v2.py` — never from scratch |

**Hard rule:** Do not build any cover until background direction AND hero color are locked. Do not deviate from `build_covers_v2.py`.

---

## Phase 2: Ecosystem Coherence Check

Every new product must be evaluated against the whole CbD ecosystem. Answer all of these:

### 2.1 — Vocabulary Ecosystem

- Does this product share core response vocabulary (*because, show, prove, agree*) with existing products in the same line?
- Will a student who has used other CbD products have a motor planning advantage with this vocabulary?
- Should any of these words be added to the Airtable Vocabulary table (`tblL2KH04WijW8XUb`)?

### 2.2 — Trading Card Companion

- Does this product generate enough fringe vocabulary to justify a companion Trading Card deck?
- If yes, does the vocabulary map to `cbd_trading_cards.py`?
- Are the ARASAAC symbols available for all fringe words?

### 2.3 — Bundle Strategy

From day one, identify:
- What existing CbD product pairs naturally with this? (thematic, skills-based, or population-based pairing)
- Is a bundle planned? At what price point?
- Example: 504 Sit-In + Capitol Crawl (both disability rights, source analysis, July launch hook)
- Example: Jennifer Keelan picture book companion + Capitol Crawl nonfiction unit (K–3 + 6–10 cross-line bundle)

### 2.4 — Substack / Marketing Angle

Every product launch needs:
- One Substack post (700–900 words, answers a real FB group question)
- One Pillar assignment (red=policy/advocacy, orange=family/teaching, blue=UFLI/SOR, green=nonfiction, yellow=real questions)
- A seasonal hook or milestone date if applicable (ADA anniversary, disability awareness month, etc.)
- FB group comment template: *"I actually wrote about this — [link]. The short version: [one sentence]."*

### 2.5 — Freebie / Entry Point

Every product line should have a free or near-free entry point:
- UFLI: IEP AT Consideration Checklist (free)
- Nonfiction: Keiko Part 1 (free freebie version — pending)
- AT/AAC Family: F0 Freebie (pipeline)
- Fiction: Does a free preview or sample unit exist? If not, plan for one.
- Picture Book Companions: Does a free read-aloud guide exist?

If no freebie exists for this line, add a freebie to the Launch Pipeline with `fldOyYzJzeZCafEuB = "Idea"`.

### 2.6 — IEP Goal Coherence

Every CbD product ships with IEP goal stems. Before build, confirm:
- What is the performance expectation? (80% accuracy / 4 of 5 sessions / with X level of support)
- What is the access method descriptor? ("using their AAC system," "using any access method," "using partner-confirmed verbal response")
- What is the condition? ("given a grade-level text and visual support," "given the Communication Access Packet")
- The goal stem must be usable as-is — not a template that requires specialist knowledge to complete

---

## Phase 3: Pre-Build Gates

Run all vocabulary QC gates from `vocabulary_selection_reference.md` PLUS:

- [ ] Research foundation document exists or is being created in parallel
- [ ] All 22 nonfiction sections mapped (if applicable) → `nonfiction_build_reference.md`
- [ ] Fiction sections mapped (if applicable) → `fiction_reference.md`
- [ ] Airtable Products record created with correct Workflow Stage = "Building"
- [ ] Airtable Launch Pipeline record updated
- [ ] TASKS.md updated with build steps
- [ ] Brand/cover direction confirmed
- [ ] Pricing model decided
- [ ] Companion product / bundle identified
- [ ] Substack angle identified
- [ ] WCAG 2.2 AA plan confirmed (all docs use `#006DA0`, PDF via Word → Save As)

---

## Phase 4: Build

Follow the standard production workflow in `CbD_Production_Workflows.xlsx`.

Key rules that apply to every build regardless of product line:
- `str_replace` over rebuilds always — targeted edits, not full rebuilds
- Never build without explicit instruction — answer first
- Flag usage cost before large multi-unit builds
- Every unit requires: Accessibility Statement → About the Creator → Terms of Use (in this order, at end)
- Symbol cards use Fitzgerald Key border colors — no exceptions
- Never "point to" as the sole interaction verb
- "Communication Access" is the section heading — never "AAC Support"

---

## Phase 5: Launch Readiness

Before listing on TPT:
- [ ] QC checklist passed (see `nonfiction_build_reference.md` or fiction/UFLI equivalent)
- [ ] Vocabulary QC gates passed (see above)
- [ ] Preview PDF built (watermarked, 8–9 pages)
- [ ] Canva cover built and saved to `Brand Assets/Nonfiction Lesson/TPT Image Cover Pending/`
- [ ] Cover Index updated (`Distrubution/Teachers Pay Teachers/CbD_TPT_Cover_Index.md`)
- [ ] Output 0 completed (TPT title ≤80 chars, description ≤180 chars, 7 keyword tags)
- [ ] Airtable Products record updated: Workflow Stage = "Ready to List" or "Cover Ready"
- [ ] Pinterest board planned
- [ ] Instagram post drafted
- [ ] Substack post either live or scheduled

---

## Decision Log

Use this section to record key decisions made during each new product line development. This is the institutional memory that prevents revisiting resolved questions.

| Product Line | Decision | Date | Notes |
|---|---|---|---|
| Fiction Anchor Texts | Whole-book scope for Wonder | 2026-03-18 | Revisit per title |
| Fiction Anchor Texts | Two-file model: main unit docx + Printable Packet PDF | 2026-03-27 | Python/ReportLab for packet |
| Picture Book Companions | First product: All the Way to the Top (Jennifer Keelan) | 2026-03-26 | K–3, IRA + Dialogic + ALS framework |
| Fiction Anchor Texts | Annotation codes LOCKED: [TRAIT] / [WHY] / [CHANGE] | 2026-03-29 | Wonder only — define per title |
| All lines | Vocabulary framework required before build | 2026-03-29 | `Research/CbD_Vocabulary_Selection_Framework.md` |
| Picture Book Companions | Research foundation document created | 2026-03-29 | `Research/Picture_Book_Companions_Research_Foundation.md` — IRA + Dialogic + ALS framework documented; HLPs 12/13/14/16 mapped; K–3 vocabulary ceiling: 15–20 words; primary standard RL.K-3.3 + secondary RL.K-3.4 |
| Picture Book Companions | Three-reading structure locked | 2026-03-29 | IRA read / vocabulary re-read / student-led re-read |
| Picture Book Companions | ALS one-pager embedded in every companion (non-negotiable) | 2026-03-29 | Partner training is the predictor variable per Binger & Light 2007 |
| Picture Book Companions | Visual Scene Displays → V2 only | 2026-03-29 | Grid default for V1; VSD planned for second iteration |

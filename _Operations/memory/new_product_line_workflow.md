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

All seven framework gates must pass before build begins. Load each reference file — do not work from memory.

---

### 1.1 — Vocabulary Framework Gate
→ Reference: `_Operations/memory/vocabulary_selection_reference.md`

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
- If YES → load the reference and apply it
- If NO or PARTIAL → vocabulary research session required BEFORE build begins; extend `Research/CbD_Vocabulary_Selection_Framework.md` first

**C. Can the 6-step word selection process be applied?**
Run through the 6 steps from the vocabulary reference. Any "unknown" answer = first build task.

**D. Can the CAP be built for this product?**
- Are symbol sources available (ARASAAC)?
- Is the fringe word count ≤30?
- Is there SLP handoff language defined?

**Decision gate:**
- [ ] Vocabulary type confirmed
- [ ] Framework coverage confirmed
- [ ] Word list drafted (core + fringe, Top 5 each)
- [ ] CAP buildable (symbols available, fringe ≤30)
- [ ] Words added to `_Operations/cbd_unit_vocab.js`

---

### 1.2 — Differentiation Framework Gate
→ Reference: `_Operations/memory/differentiation_reference.md`

**A. Are V1/V2/V3 Lexile targets confirmed for this product type?**

| Version | Nonfiction | Fiction / Picture Book |
|---------|-----------|----------------------|
| V1 | 900–1050L | Grade-band equivalent |
| V2 | 650–800L | 5th/6th grade comprehension |
| V3 | 400–550L | 3rd/4th grade reading level |

**B. Are the locked constants defined for this unit?**
- ELA standard (identical across all versions)
- Essential question (identical across all versions)
- Vocabulary list (same across all versions)
- Skill type (one skill per unit — no exceptions)
- Response task category (format scaffolds; task does not change)
- HLPs (same category across all versions; scaffold changes, not the practice)

**C. Does every V3 activity pass the IDEA access test?**
> "Can a student completing this activity be said to have *demonstrated the skill* the standard requires? Or has the task been reduced to factual recall?"
- If recall only → rewrite before build begins

**D. Is the V3 vocabulary instruction step (Descriptive Teaching Model) planned — not just a glossary?**

**Decision gate:**
- [ ] Lexile targets confirmed for all three versions
- [ ] All locked constants defined
- [ ] V3 activities pass IDEA access test
- [ ] V3 vocabulary instruction step planned (Descriptive Teaching Model format)
- [ ] HLPs labeled and consistent across versions

---

### 1.3 — Communication Access Framework Gate
→ Reference: `_Operations/memory/communication_access_reference.md`

**A. Is the CAP vocabulary list complete (core + fringe)?**
The CAP must be ready to deliver to the SLP 1–2 weeks before Day 1 of instruction. It cannot be an afterthought.

**B. Does every activity in every version have at least one non-speech AAC response pathway?**
No activity in any CbD product may accept oral response only.

**C. Is the consistent core response vocabulary present across all activities?**
Required core set: *because, show, prove, agree, different, same, not, true, wrong* — these build the cross-unit motor pathway.

**D. Is partner guidance written at the point of use (not in an appendix)?**
Every activity where AAC response is expected must have embedded guidance — not a separate "AAC guide."

**Decision gate:**
- [ ] CAP vocabulary list complete (fringe list finalized, symbols sourced)
- [ ] CAP delivery timeline documented (1–2 weeks before Day 1)
- [ ] Every activity has an AAC-compatible response opportunity
- [ ] No activity relies on oral response only
- [ ] Core response vocabulary consistent with cross-unit set
- [ ] Partner guidance embedded at point of use in activity design

---

### 1.4 — Communication Partner Framework Gate
→ Reference: `_Operations/memory/communication_partner_reference.md`

Partner guidance must be written before the unit is built — it cannot be added after.

**A. Are all four evidence-based partner behaviors planned for each version level?**

| Behavior | Required |
|---------|---------|
| Model (ALgS) | Name specific vocabulary + when to model |
| Wait | Must specify 5 seconds — not "give extra time" |
| Expand | Accept AAC output → add 1–2 words |
| Offer Choice | When no response after waiting — 2 genuine options from the text |

**B. Does every guidance callout pass the Circle 3 test?**
Write for a substitute para with no AAC training, 5 minutes before the lesson. Disposition-based language ("be patient") fails. Behavior-specific language ("count silently to 5") passes.

**C. Is partner guidance present in all required locations?**
- Unit introduction (AAC orientation)
- Vocabulary Preview (which words to model and when)
- Reading activities (read-aloud guidance; V3 vocabulary teaching step)
- Response activities (wait time; how to expand; choice if no response)
- CAP page 1 (SLP + partner preparation)

**Decision gate:**
- [ ] All four partner behaviors planned for all version levels
- [ ] At least one callout specifies wait time in seconds (5 seconds)
- [ ] At least one callout names specific vocabulary to model
- [ ] At least one callout explains what to do with a student AAC response
- [ ] All callouts are 5 lines or fewer (Circle 3 test)
- [ ] Partner guidance location plan confirmed (embedded, not appended)

---

### 1.5 — SDI Framework Gate
→ Reference: `_Operations/memory/sdi_reference.md`

**A. Which CbD components in this product are SDI-level (vs. accommodation)?**

| SDI-Level Component | Accommodation-Level Component |
|---------------------|-------------------------------|
| V2/V3 adapted text | Symbol Cards PDF |
| Vocabulary Preview Routine | Extended time |
| CAP used with SLP collaboration | Read-aloud (test accommodation) |
| AAC Response Pathway as primary modality | Sentence frames (test accommodation) |
| Partner Read-Aloud Protocol | Preferential seating |
| V3 Vocabulary Instruction (Descriptive Teaching Model) | |

**B. Is there a documented SDI trail planned?**
For every SDI-level component: IEP annual goal → IEP SDI section naming the adaptation → CAP delivery timestamp → Session Tracker data.

**C. Is the SDI vs. accommodation distinction explained in teacher guidance?**
Teachers need to know what to write in the IEP and where. This must be in the teacher document — not assumed.

**Decision gate:**
- [ ] SDI components identified and labeled for this product
- [ ] Accommodation components listed separately
- [ ] SDI vs. accommodation distinction drafted for teacher guidance
- [ ] CAP confirmed as the SDI delivery tool for the AAC component
- [ ] Documentation trail planned (IEP goal → CAP → Session Tracker → data)

---

### 1.6 — IEP Goal Ecosystem Gate
→ Reference: `_Operations/memory/iep_goal_ecosystem_reference.md`

Every CbD unit ships with a minimum of two goal stems: one academic (ELA skill) + one AAC communication.

**A. Is the academic goal stem written for this unit's specific skill type?**

Goal stem structure:
```
Given [condition: version + specific supports],
[student] will [observable verb] [skill + standard]
as measured by [data tool in the product],
achieving [performance criterion] + [consistency criterion] by [date].
```

| Skill Type | Observable Verbs |
|-----------|-----------------|
| Close Reading / Annotation | identify, annotate, cite, locate, mark |
| Author's Purpose / Perspective | explain, distinguish, compare, defend |
| CER | state, identify, select, write, construct |
| Text Structure | label, organize, sequence, categorize |
| Sourcing / Corroboration | evaluate, rate, compare, justify |
| Character Analysis (Fiction) | identify, describe, compare, support with evidence |

**Never use:** understand, know, appreciate, be aware of, learn.

**B. Does the academic goal stem pass the accommodation test?**
> "Is the ELA standard in this goal the same standard peers are working toward, with a different access method?"

**C. Is the AAC goal stem written and separate from the academic goal?**
Academic progress and communication progress are not the same. Both need separate goals and separate data.

**Decision gate:**
- [ ] Academic goal stem drafted (full IDEA structure: condition + verb + standard + measure + criterion + date)
- [ ] Goal uses observable verb from the approved list
- [ ] Goal passes the accommodation test (same standard, different access)
- [ ] AAC communication goal stem drafted and separate from academic goal
- [ ] Default mastery criteria applied (see Assessment & Data Framework)

---

### 1.7 — Assessment & Data Framework Gate
→ Reference: `_Operations/memory/assessment_data_reference.md`

**A. Is a rubric designed for every scored response activity?**
- 3 levels: Does Not Yet Meet / Approaching / Meets
- Each level = observable student behavior (not "excellent/good/needs work")
- Identical across V1/V2/V3
- On the student's response document — not a separate sheet
- Scorable by a para with no content expertise

**B. Are default mastery criteria applied?**

| Skill | Academic Criterion | AAC Criterion |
|-------|-------------------|---------------|
| Close Reading / Annotation | 80%, 3 consecutive sessions | 4/5 opp., 2+ sessions |
| CER | Claim + 2 evidence aligned, 4 of 5 trials | CER via AAC, 3/5 trials |
| Author's Purpose / Perspective | 2 perspectives w/ evidence, 3 of 4 trials | 2+ symbol sequence, 4/5 opp. |
| Text Structure | 3 of 4 elements labeled, 3 consecutive | Cause/effect via AAC, 4/5 opp. |
| Sourcing / Corroboration | 3/4 sources rated w/ justification, 2 consecutive | Source rated via AAC, 3/5 |

Minimum: 70%. Generalization: across 2+ partners before reporting mastery.

**C. Are data roles assigned in teacher guidance?**
- Special educator → rubric scores + session accuracy
- Para → Communication Session Tracker + symbol output tallies
- SLP → vocabulary pre-programming confirmation + CAP delivery date

**Decision gate:**
- [ ] Rubric designed for every scored activity (3-level, behavioral descriptions)
- [ ] Rubric identical across V1/V2/V3
- [ ] Rubric placed on student response document (not separate)
- [ ] Session Tracker included in CAP
- [ ] Default mastery criteria applied (minimum 70%; 2+ partners for generalization)
- [ ] Data roles assigned in teacher guidance

---

### 1.8 — Research Foundation Gate

Every product line needs a research foundation document before build.

| Product Line | Status |
|---|---|
| Nonfiction | Partial (via `nonfiction_build_reference.md` + annotated evidence in units) |
| Fiction | ✅ `Fiction_Narrative_Research_Foundation.md` |
| UFLI | ✅ `CbD_Research_Reference_AAC_Phonics_Literacy.md` + `UFLI_AAC_Phonics_Research_Reference.md` |
| Picture Book Companions | ✅ `Picture_Book_Companions_Research_Foundation.md` |
| AT/AAC IEP Team | Partial |
| Chapter Books | ⚠️ Not yet created |

If no research file exists: create one using `Research_Template.md`. Answer: what professional organizations (ASHA, CEC, CAST, IRIS) ground this product? What HLPs apply (minimum 2)? What does the research say a student with AAC needs to succeed with this content type?

**Decision gate:**
- [ ] Research foundation document exists in `Research/`
- [ ] Minimum 2 HLPs mapped to this product
- [ ] Professional organization grounding identified

---

### 1.9 — Product Architecture Decision

Define exactly what files the product ships with before writing any code.

| Required for every product | Notes |
|---------------------------|-------|
| Main content file (.docx or PDF) | Built via `cbd_docx_template.js` or Python/ReportLab |
| Communication Access Packet (CAP) | 10-page standard (nonfiction) or adapted format |
| Symbol cards | 2"×2" ARASAAC grid, Fitzgerald Key borders |
| IEP goal stems | Minimum 2 per product (academic + AAC) |
| Partner guidance | Embedded in unit document — not supplemental |
| Session Tracker | Appended to CAP |

| Optional / line-specific | Trigger |
|--------------------------|---------|
| Printable Packet PDF | Fiction Anchor Texts only — 4 layers, 9 pages, Python/ReportLab |
| Lesson chips + interactive activity link | UFLI only |
| Visual Scene Displays | Fiction + Picture Book Companions (V2) |
| Trading Card companion deck | Any product with fringe vocabulary → `cbd_trading_cards.py` |
| Preview PDF (watermarked, 8–9 pages) | Every TPT listing that includes the main docx |

---

### 1.10 — Build System Check

Before writing any code:
- Does an existing build script cover this product? (`build_all_units.py`, `cbd_docx_template.js`, `build_covers_v2.py`)
- What new scripts or templates are needed?
- What is the folder structure? (`Products/[Line]/[Product Name]/`)
- Has the Airtable Products table record been created?
- Has the Launch Pipeline record been created?

---

### 1.11 — Brand and Identity Decision

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

### Vocabulary Pipeline Gate (required before build begins)

Once vocabulary is finalized for the unit, lock it into the ecosystem:

1. Add the unit entry to `_Operations/cbd_unit_vocab.js` — this is the source of truth for all unit vocabulary (fiction and nonfiction)
2. Add the product entry to `_Operations/rebuild_vocab_explorer.js`:
   - Add to `UNIT_KEY` mapping (full unit title → short key)
   - If fiction: add short key to `FICTION_UNITS` Set
   - Add product card to `PRODUCTS_BLOCK` with `status: 'In Production'`
3. Run `node _Operations/rebuild_vocab_explorer.js` → AAC Vocabulary Explorer updates; product appears with "In Production" badge
4. Run `AIRTABLE_API_KEY=xxx node _Operations/sync_vocab_to_airtable.js` → Airtable Vocabulary table (`tblL2KH04WijW8XUb`) updated with new words

**Verification:** Open `cbd-vocabulary-explorer.html` → filter by Fiction or Nonfiction line → confirm unit appears, word count matches source, and product card shows "In Production".

---

## Phase 4: Build

Follow the standard production workflow in `CbD_Production_Workflows.xlsx`.

### Universal Build Rules (Apply to Every Product)

- `str_replace` over rebuilds always — targeted edits, not full rebuilds
- Never build without explicit instruction — answer first, build when asked
- Flag usage cost before large multi-unit builds (all 30 UFLI packets, all 6 nonfiction units, etc.)
- Every unit requires end matter in this order: Accessibility Statement → About the Creator → Terms of Use
- Symbol cards use Fitzgerald Key border colors — no exceptions
- Never "point to" as the sole interaction verb — always "select, point to, or use gaze to indicate"
- Section heading is always "Communication Access" — never "AAC Support"
- WCAG 2.2 Level AA on all documents; use `#006DA0` in .docx/.pdf (never `#00B4D8`)
- PDF generation: Word → File → Save As → PDF (not Print to PDF, not LibreOffice)

### Build Sequence by Product Type

**Nonfiction Reading Unit**
1. Run Phase 1 Framework Gate checklist (all 7 gates) — do not skip
2. Build V1 passage → V2 → V3 (in this order; V3 is a reduction of V2, not independent)
3. Build activities for each version (Close Reading → Vocabulary Preview → Response Activity)
4. Build CAP: vocabulary list → Fitzgerald categories → ARASAAC symbols → Session Tracker → SLP handoff page
5. Build symbol cards (`cbd_symbol_cards.py`) — Fitzgerald Key borders, 2"×2" grid
6. Add IEP goal stems (academic + AAC) and SDI labeling to teacher guidance
7. Embed partner guidance at point of use (vocabulary preview, reading, response activities)
8. Run 22-section QC checklist (`_Operations/memory/nonfiction_build_reference.md`)
9. Run all framework QC gates (differentiation, communication access, partner, SDI, IEP, assessment)
10. Build preview PDF (watermarked, 8–9 pages)

**Fiction Anchor Text Unit**
1. Run Phase 1 Framework Gate checklist (all 7 gates)
2. Build main unit docx: story grammar framework → annotation activities → vocabulary instruction → response activities
3. Build Fiction Printable Packet (Python/ReportLab, 4 layers, 9 pages) — spec: `_Operations/memory/fiction_printable_packet_spec.md`
4. Build CAP for fiction vocabulary (emotional/mental state + story grammar fringe)
5. Build symbol cards for Set A (SDI instruction targets) and Set B (full communication board vocab)
6. Add IEP goal stems and SDI labeling
7. Embed partner guidance
8. Build preview PDF (watermarked)

**UFLI Phonics Lesson Packet**
1. Run vocabulary gate (UFLI words are fixed — do not add or remove)
2. Build lesson packet via `build_ufli_packet.js` — do not start from scratch
3. Confirm Communication Partner Guide is generated alongside each packet
4. Run QC: `_Operations/memory/ufli_build_reference.md`

**Picture Book Companion**
1. Run Phase 1 Framework Gate checklist (all 7 gates)
2. Build 3-reading structure: IRA read / vocabulary re-read / student-led re-read
3. Vocabulary ceiling: 15–20 words maximum
4. Embed ALS one-pager (non-negotiable)
5. Build CAP (vocabulary list, symbols, partner guidance)
6. Apply RL.K-3.3 and RL.K-3.4 standards
7. Build preview PDF

### Build Completion Checklist (All Types)

- [ ] All framework QC gates passed (use checklist from each reference file)
- [ ] 22 sections present (nonfiction) or equivalent structure (fiction/picture book)
- [ ] Partner guidance embedded at point of use — not in appendix
- [ ] Rubric on student response document — not separate
- [ ] CAP complete: vocabulary, symbols, Session Tracker, SLP handoff
- [ ] IEP goal stems included (academic + AAC, full IDEA structure)
- [ ] End matter in correct order: Accessibility Statement → About the Creator → Terms of Use
- [ ] WCAG check: all headings have styles, teal is `#006DA0`, contrast passes
- [ ] PDF generated via Word → Save As (not Print to PDF)

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
- [ ] Pinterest board planned (one board per product line — named for teacher search term, not internal CbD name)
- [ ] Pinterest pin created and Pin URL added to Airtable field `fldx9FesXwfqZhWYp`
- [ ] Instagram post drafted
- [ ] Substack post either live or scheduled

---

### TPT Listing Field Workflow (locked 2026-04-05)

**Source of truth:** Airtable Products table (`tbl2YSRQiW7RHEPY5`) — all TPT metadata fields are populated per product during development, not at listing time. Fields:

| Airtable Field | TPT Field | Type | Notes |
|---|---|---|---|
| Product SubHeading | Product Name | Text ~80–100 chars | Pipe-separated: Topic \| Differentiator \| SPED Grades. Keyword-heavy for SEO. |
| — | Product File | Upload (≤1GB direct, ≤500MB via Google Drive) | The deliverable zip or PDF. Uploaded by Jill — not in Airtable. |
| — | Preview File | Upload (PDF or Video, optional) | Highly recommended. TPT can auto-generate from PDF. Uploaded by Jill. |
| — | Thumbnails | Upload (up to 4 images) | TPT can auto-generate from PDF, or upload cover PNGs manually. Up to 4. |
| Description | Description | Rich text (no strict char limit) | SEO-optimized. Opening line keyword-dense. No strict limit — be thorough. |
| Price | Price | $ | Per product line pricing table in CLAUDE.md |
| Tax Code | Tax Code | Drop-down | "Digital Images - Streaming / Electronic Download" for CbD digital products |
| Grade Levels | Grade Levels | Checkboxes | e.g. "Kindergarten, 1st, 2nd, 3rd" — spell out exact grade names |
| Subject Areas | Subject Areas | Checkboxes — verified options only (see below) | Never invent values. Use only verified TPT options from the list below. |
| Resource Types | Resource Types | Checkboxes (max 3) — verified options only | See verified list below. Max 3. |
| Teaching Duration | Teaching Duration | Drop-down — exact labels | See verified list below. CbD multi-read units = "1 Month" |
| Answer Key | Answer Key | Drop-down — exact labels | CbD units with rubrics = "Included with Rubric" |
| Page Count | Number of Pages | Number | Teacher + Student + Welcome combined |
| Standards | Standards | Text | e.g. "RL.K.3, RL.1.3, RL.2.3, RL.3.3" |

**What Jill handles manually at listing time (not in Airtable):** Product File upload · Preview File upload · Thumbnails (auto-generate from PDF or upload PNGs). Everything else copies from the spreadsheet.

**Output format for listing:** Single-sheet Excel (`TPT_Listings_[Line].xlsx`) — one row per product, columns match TPT field order. Built via `build_[line]_tpt_v[N].py`. Green row = Live. Copy/paste directly from spreadsheet into TPT listing form.

---

### Verified TPT Dropdown Values (locked 2026-04-05)

**CRITICAL RULE:** Only use values from these lists. Never invent a value — TPT will reject or not surface listings with invalid field entries.

**Teaching Duration** (drop-down, select one):
N/A · 30 Minutes · 40 Minutes · 45 Minutes · 50 Minutes · 55 Minutes · 1 Hour · 90 Minutes · 2 Hours · 3 Hours · 2 Days · 3 Days · 4 Days · 1 Week · 2 Weeks · 3 Weeks · 1 Month · 2 Months · 3 Months · 1 Semester · 1 Year · Lifelong Tool

**Answer Key** (drop-down, select one):
N/A · Included · Not Included · Included with Rubric · Rubric Only · Does Not Apply

**Subject Areas — English Language Arts** (checkboxes):
Alphabet · Balanced Literacy · Close Reading · Creative Writing · ELA Test Prep · Grammar · Handwriting · Informational Text · Library Skills · Literature · Novel Studies · Phonics & Phonological Awareness · Poetry · Reading · Reading Strategies · Science of Reading · Short Stories · Sight Words · Spelling · Vocabulary · Writing · Other (ELA)

**Subject Areas — Supports > Special Education** (checkboxes):
Applied Behavior Analysis · Data · Life Skills · Neurodiversity · Screenings and Assessments · Social Skills · Visual Supports · Other (Special education)

**Subject Areas — Supports > Speech Therapy** (checkboxes):
AAC · Fluency and Stuttering · Language · Speech Articulation · Voice · Other (Speech therapy)

**Subject Areas — Social Emotional** (checkboxes):
Character Education · Classroom Community · School Counseling · School Psychology · Social Emotional Learning

**Subject Areas — Social Studies** (checkboxes):
AAPI History · African History · Ancient History · Asian Studies · Australian History · Black History · Civics · Criminal Justice - Law · Economics · Elections - Voting · European History · Geography · Government · Latino and Hispanic Studies · Middle Ages · Native Americans · Psychology · Religion · U.S. History · World History · Other (Social Studies)

**Subject Areas — Theme > Holiday** (checkboxes):
AAPI History Month · April Fools' Day · Arbor Day · Black History Month · Christmas-Chanukah-Kwanzaa · Cinco de Mayo · Day of the Dead / Dia de los Muertos · Diwali · Earth Day · Easter · Father's Day · Groundhog Day · Halloween · Hispanic Heritage Month · July 4/Independence Day · Juneteenth · Labor Day · Lunar New Year · Mardi Gras · Martin Luther King Day · Memorial Day · Mother's Day · New Year · Passover · Presidents' Day · Ramadan · St. Patrick's Day · Thanksgiving · Valentine's Day · Veterans Day · Women's History Month

**Subject Areas — Theme > Seasonal** (checkboxes):
Autumn · Back to School · End of Year · Spring · Summer · Winter

**Subject Areas — Specialty** (checkboxes — partial, includes):
Career and Technical Education · Child Care · Coaching · Cooking · Leadership · Occupational Therapy · Physical Therapy · Professional Development · Service Learning · Vocational Education · Other (Specialty)

**Subject Areas — Teacher Tools** (checkboxes — partial):
Awards and Certificates · Classroom Management · Homeschool Curricula · Leadership Lessons · Lectures · Lessons · Outlines · Reflective Journals for Teachers · Rubrics · Syllabi · Teacher Manuals · Teacher Planners · Thematic Unit Plans · Tools for Common Core

**Resource Types** (checkboxes, max 3 — verified options):
Printables · Handouts · Worksheets · Graphic Organizers · Scaffolded Notes · Interactive Notebooks · Guided Reading Books · Independent Work Packet · Task Cards · Workbooks · Flash Cards · Scripts · Projects · Research · Simulations · Songs · Webquests · Rubrics · Study Guides · Homework · Assessment · Movie Guides

**Standard CbD subject area selections by product line:**

| Product Line | Subject Areas to Select |
|---|---|
| Picture Book Companions | Reading, Literature, Neurodiversity, Other (Special education), AAC + one social/SEL option per title |
| Nonfiction Reading Units (grades 6–10) | Reading, Informational Text, Close Reading, Neurodiversity, Other (Special education), AAC + relevant Social Studies topic |
| Fiction Anchor Texts | Reading, Literature, Novel Studies, Neurodiversity, Other (Special education), AAC |
| UFLI Phonics | Phonics & Phonological Awareness, Science of Reading, Reading, Other (Special education), AAC |
| AT/AAC IEP Tools | Other (Special education), Applied Behavior Analysis, Data, Neurodiversity, AAC, Language |
| Poetry Reading Units | Poetry, Reading, Literature, Close Reading, Other (Special education), AAC |

**Standard CbD resource type selections:**
Most products: `Handouts, Printables, Worksheets`
UFLI Phonics packets: `Handouts, Printables, Scaffolded Notes`
AT/AAC tools: `Handouts, Printables, Graphic Organizers`

---

### Pinterest Upload Workflow (locked 2026-04-05)

**File:** `Distrubution/Pinterest/[Line]_Pinterest_BulkUpload.csv`

**Fields and sources:**

| CSV Column | Source | Notes |
|---|---|---|
| Title | Airtable Product Name (short) + grade/type qualifier | **Book/topic title first.** Formula: `[Title] \| AAC Read-Aloud Companion \| Special Education K–[X]`. Never lead with skill or framework. |
| Description | Airtable Description (condensed) + hashtags | 500 chars max. Lead with what it does (not a hook). Include: book title, AAC, special education, grade level, topic. End with 5–7 hashtags. |
| Link | Airtable TPT URL field | Full TPT product URL. Always https://www.teacherspayteachers.com/Product/... |
| Board | Pinterest board name | One board per pin. Do not split same product across multiple boards. |
| Image Path/URL | Blank in CSV — Jill fills after Canva export | Export cover PNG from Canva → paste path or upload manually in Pinterest. |
| Alt Text | Cover description for screen readers | Format: "AAC read-aloud companion cover for [Book Title] — [color scheme] showing [what's visible on cover]" |
| Published Date | Leave blank or set to upload date | Pinterest schedules from this field if populated. |

**Product Tag (Pinterest Shopping):** After uploading each pin, use Pinterest's Product Tags → "Use a Link" → paste the same TPT URL from the Link column. This shows the $[price] badge on the pin and links directly to purchase.

**Canva export workflow:** Export Canva cover as PNG (1080×1080 for square pins). File naming: `[BookTitle]_PB_Companion_Pinterest.png`. Save to `Distrubution/Pinterest/[Line]/` alongside the CSV.

**Pinterest SEO rule:** Pinterest works like a search engine. Teachers search the book title first. Title MUST lead with the book/topic name — never with skill, framework, or brand name. Board name should match what teachers search (e.g., "Picture Book AAC Companion" not "Communicate by Design").

**Populate at development time:** Both the TPT listing fields and Pinterest CSV fields should be populated in Airtable during product development — not assembled at listing time. This enables same-day listing on TPT + same-day Pinterest upload with no scramble.

### Vocabulary Explorer Launch Gate (required at go-live)

When the product goes live on TPT:

1. Update `PRODUCTS_BLOCK` in `_Operations/rebuild_vocab_explorer.js`:
   - Change `status: 'In Production'` → `status: 'Live'`
   - Add `platforms: [{ name: 'TPT', url: 'https://www.teacherspayteachers.com/Product/...' }]`
2. Run `node _Operations/rebuild_vocab_explorer.js` → product badge updates to "Live"
3. Run `AIRTABLE_API_KEY=xxx node _Operations/sync_vocab_to_airtable.js` → Airtable confirms no vocabulary drift

**Vocabulary QC check:** Open `cbd-vocabulary-explorer.html` → click any word from this unit → confirm:
- "Vocabulary in These Products" shows the correct unit with a Live badge
- "Appears in X products" count matches the number of product cards shown
- No words are missing or unexpected (compare against the word list in `cbd_unit_vocab.js`)

If any word is missing from the explorer or count is wrong → recheck `cbd_unit_vocab.js` entry and rebuild before the listing goes live.

---

## Phase 6: Post-Launch Maintenance

A product going live is not the end of the workflow. These steps keep the ecosystem in sync.

### At Launch (Within 48 Hours of TPT Listing Going Live)

- [ ] Vocabulary Explorer status updated: `status: 'In Production'` → `status: 'Live'` + TPT URL added in `rebuild_vocab_explorer.js` PRODUCTS_BLOCK
- [ ] Run `node _Operations/rebuild_vocab_explorer.js` → Live badge active in explorer
- [ ] Pinterest pin created for this product
- [ ] **Pinterest Pin URL added to Airtable Products field `fldx9FesXwfqZhWYp`** — this is the trigger that tells the daily brief the product is pinned. Once this field is populated, the brief automatically moves the product to List B (fresh pin rotation) on the next morning run. No other Pinterest tracking step needed.
- [ ] Pinterest First Pin Date (`fldwrWqdlHarNopcD`) and Pin Count (`fld0w7mq9rfixZ5n9`) update automatically from the brief task after pin URL is set
- [ ] Run `AIRTABLE_API_KEY=xxx node _Operations/sync_vocab_to_airtable.js` → Airtable Vocabulary table confirmed in sync
- [ ] Airtable Products table record updated: Workflow Stage → "Live"
- [ ] Cover moved from `Brand Assets/Nonfiction Lesson/TPT Image Cover Pending/` → `TPT Image Covers Uploaded/`
- [ ] Cover Index updated (`Distrubution/Teachers Pay Teachers/CbD_TPT_Cover_Index.md`)
- [ ] Pinterest post live
- [ ] Instagram post live
- [ ] Substack post live or scheduled

### Vocabulary Drift Monitoring

Vocabulary drift = words added to a product during build that were never added to `cbd_unit_vocab.js`, or words removed from the product but still in the source file.

**How to check:**
1. Open `cbd_unit_vocab.js` — find the unit's word array
2. Open the built product docx — find the Vocabulary section
3. Cross-reference word by word
4. Any mismatch → update `cbd_unit_vocab.js` → rebuild explorer → re-sync Airtable

**When to run:** At launch, and any time a product receives a content update (new passage, revised vocabulary section).

### Product Updates and Re-Uploads

When a product is updated after launch (new content, corrected passage, vocabulary revision):

1. Make the change in the build source (unit JS/Python build script)
2. If vocabulary changed → update `cbd_unit_vocab.js` first
3. Rebuild the docx → regenerate PDF (Word → Save As)
4. Re-upload to TPT (replace files — do not create a new listing)
5. If vocabulary changed → run `node _Operations/rebuild_vocab_explorer.js`
6. If vocabulary changed → run `sync_vocab_to_airtable.js`
7. Update Airtable Products record: note the update in the record

**Active re-upload queue:** All 6 nonfiction units need Session 16 content update re-uploaded to TPT (as of 2026-03-29).

### Bundle Management

When a bundle is created from existing live products:
- Create a new Airtable Products record for the bundle
- Create a new Launch Pipeline record
- Build a bundle preview PDF (combine previews from both products)
- New TPT listing — new cover
- Price = individual prices minus discount (see bundle strategy from Phase 2.3)

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

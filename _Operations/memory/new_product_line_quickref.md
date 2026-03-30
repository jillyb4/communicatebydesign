# CbD New Product Line — Quick Reference Checklist
*One page. Use at the start of every build session. Full details: `new_product_line_workflow.md`*

---

## Phase 0 — Concept Validation
- [ ] Instructional gap confirmed (real practitioner problem, evidence exists)
- [ ] ELA/literacy standard identified (one skill, specific codes, grade band)
- [ ] Primary buyer persona defined
- [ ] Competitor gap confirmed (TPT search run)

---

## Phase 1 — Framework Gates *(load each reference file before checking)*

**1.1 Vocabulary** → `vocabulary_selection_reference.md`
- [ ] Vocabulary type confirmed for this product type
- [ ] Word list drafted (core + fringe, Top 5 each, ≤30 fringe)
- [ ] CAP buildable (ARASAAC symbols available)
- [ ] Words added to `_Operations/cbd_unit_vocab.js`

**1.2 Differentiation** → `differentiation_reference.md`
- [ ] V1/V2/V3 Lexile targets confirmed
- [ ] Locked constants defined (standard, EQ, vocab, skill, HLPs)
- [ ] All V3 activities pass IDEA access test (skill demonstrated, not just recalled)
- [ ] V3 vocabulary instruction step planned (Descriptive Teaching Model — not a glossary)

**1.3 Communication Access** → `communication_access_reference.md`
- [ ] Every activity has a non-speech AAC response pathway
- [ ] Core response vocabulary consistent: *because, show, prove, agree, different, same, not, true, wrong*
- [ ] CAP delivery timeline set (1–2 weeks before Day 1)
- [ ] Partner guidance embedded at point of use (not in appendix)

**1.4 Communication Partner** → `communication_partner_reference.md`
- [ ] All 4 behaviors planned for all version levels (Model, Wait, Expand, Offer Choice)
- [ ] At least one callout specifies 5-second wait time
- [ ] All callouts ≤5 lines (Circle 3 test: sub para, no AAC training, 5 minutes)

**1.5 SDI** → `sdi_reference.md`
- [ ] SDI components identified and labeled (V2/V3 text, Vocab Preview Routine, CAP + SLP, AAC pathway)
- [ ] Accommodation components listed separately (symbol cards, extended time, etc.)
- [ ] SDI vs. accommodation distinction in teacher guidance

**1.6 IEP Goals** → `iep_goal_ecosystem_reference.md`
- [ ] Academic goal stem drafted (condition + observable verb + standard + measure + criterion + date)
- [ ] Goal passes accommodation test (same standard, different access)
- [ ] AAC communication goal stem drafted and separate from academic goal

**1.7 Assessment & Data** → `assessment_data_reference.md`
- [ ] Rubric designed for every scored activity (3-level, behavioral, identical across V1/V2/V3)
- [ ] Rubric on student response document (not separate sheet)
- [ ] Default mastery criteria applied (minimum 70%; 2+ partners for generalization)
- [ ] Data roles assigned (educator = rubrics; para = Session Tracker; SLP = CAP confirmation)

**1.8 Research Foundation**
- [ ] Research file exists in `Research/` (create from template if not)
- [ ] Minimum 2 HLPs mapped

**1.9 Product Architecture**
- [ ] Files defined: main docx/PDF, CAP, symbol cards, IEP goal stems, Session Tracker
- [ ] Line-specific files planned (Printable Packet for fiction, lesson chips for UFLI, etc.)

**1.10 Build System**
- [ ] Airtable Products record created (Workflow Stage = "Building")
- [ ] Airtable Launch Pipeline record created
- [ ] Build scripts identified (never start cover from scratch — `build_covers_v2.py` only)

**1.11 Brand & Identity**
- [ ] Product line color confirmed
- [ ] Cover direction confirmed (background + hero concept)
- [ ] Footer Line 2 text confirmed

---

## Phase 2 — Ecosystem Check
- [ ] Core response vocabulary carries over from other products in this line
- [ ] Trading card companion assessed (fringe vocabulary → `cbd_trading_cards.py`)
- [ ] Bundle strategy identified
- [ ] Substack angle identified (Pillar color + seasonal hook)
- [ ] Freebie/entry point planned for this line

---

## Phase 3 — Pre-Build Gates
- [ ] All Phase 1 framework gates passed
- [ ] Research foundation document confirmed in `Research/`
- [ ] Pricing decided
- [ ] Cover direction locked
- [ ] TASKS.md updated with build steps

**Vocabulary Pipeline (lock before build)**
- [ ] Words in `cbd_unit_vocab.js`
- [ ] Product entry added to `rebuild_vocab_explorer.js` with `status: 'In Production'`
- [ ] Run `node _Operations/rebuild_vocab_explorer.js` → explorer shows "In Production"
- [ ] Run `sync_vocab_to_airtable.js` → Airtable updated

---

## Phase 4 — Build Completion
- [ ] All framework QC gates passed (use checklist from each reference file)
- [ ] 22 sections present (nonfiction) or equivalent structure (fiction/picture book)
- [ ] Rubric on student response document
- [ ] CAP complete (vocab, symbols, Session Tracker, SLP handoff)
- [ ] IEP goal stems included (academic + AAC, full IDEA structure)
- [ ] End matter in order: Accessibility Statement → About the Creator → Terms of Use
- [ ] WCAG check: headings styled, teal = `#006DA0`, contrast passes
- [ ] PDF generated via Word → Save As (not Print to PDF)

---

## Phase 5 — Launch Readiness
- [ ] QC checklist passed
- [ ] Preview PDF built (watermarked, 8–9 pages)
- [ ] Canva cover built → saved to `Brand Assets/.../TPT Image Cover Pending/`
- [ ] Cover Index updated (`Distrubution/Teachers Pay Teachers/CbD_TPT_Cover_Index.md`)
- [ ] Output 0 complete (TPT title ≤80 chars, description ≤180 chars, 7 keyword tags)
- [ ] Airtable Products record: Workflow Stage = "Ready to List"
- [ ] Pinterest, Instagram, Substack planned

**Vocabulary Explorer Launch Gate**
- [ ] Update `rebuild_vocab_explorer.js`: `status: 'Live'` + TPT URL
- [ ] Run `node _Operations/rebuild_vocab_explorer.js` → Live badge active
- [ ] Run `sync_vocab_to_airtable.js` → Airtable confirmed
- [ ] Open explorer → select a unit word → confirm Live badge + correct product count

---

## Phase 6 — Post-Launch (within 48 hours)
- [ ] Cover moved to `TPT Image Covers Uploaded/`
- [ ] Cover Index updated (status = Uploaded)
- [ ] Airtable Products: Workflow Stage = "Live"
- [ ] Pinterest post live
- [ ] Instagram post live
- [ ] Substack post live or scheduled
- [ ] GitHub Desktop → commit → Push Origin

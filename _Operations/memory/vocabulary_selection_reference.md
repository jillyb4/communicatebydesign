# CbD Vocabulary Selection — Operational Reference
*Added: 2026-03-29 | Full research: `Research/CbD_Vocabulary_Selection_Framework.md`*

**Load this file when:** building or QC-checking any CbD product vocabulary, starting a new product line, or reviewing a Communication Access Packet.

---

## The Two-Dimension Classification

Every vocabulary word gets TWO tags.

### Dimension 1: AAC Access Layer

| Tag | Meaning | Required Action |
|-----|---------|----------------|
| **Core** | Already on most robust AAC systems | Model during activities; include on communication board |
| **Fringe** | NOT pre-programmed; must be added before instruction | Symbol card + CAP flag; SLP 1–2 week lead time |
| **Heart** | Irregular high-frequency word (phonics exception) | UFLI context only; note phonics connection |

### Dimension 2: Instructional Layer

| Tag | Meaning | Product Treatment |
|-----|---------|------------------|
| **Explicit instruction target** | Student is learning THIS word for the standard | Vocabulary Preview + Word Bank + sentence frames + 3+ activities + Top 5 candidate |
| **Background knowledge** | Needed to understand the text; not the teaching focus | Brief definition in Vocabulary Reference table only |
| **Generative / response** | Student needs this word to PRODUCE their response | Sentence frames + communication board + partner modeling |

**The critical distinction:** A word can be Fringe (AAC Access) AND an Explicit Instruction Target (Instructional). *Protest* in 504 Sit-In is both. *Federal* is Fringe but Background Knowledge only. These require completely different treatment in the unit.

---

## 6-Step Word Selection

1. **Start with the standard, not the text** — what concepts must the student demonstrate?
2. **Tier 2 first** — high-utility academic words that transfer across units (*evidence, advocate, compare*) → Explicit Instruction Targets, 3+ activities each
3. **Tier 3 second** — text-specific content words (*thalidomide, ADA, boarding school*) → mostly Background Knowledge; some Explicit if thematically central
4. **Apply AAC lens** — core (already programmed) vs. fringe (SLP must add before unit)
5. **Identify response vocabulary** — what words does the student use to BUILD a response? (Almost all core: *because, show, prove, agree, wrong*)
6. **Select Top 5 per layer** — most critical core + most critical fringe = the CAP priority page

---

## Product Line Rules

**UFLI Phonics:**
Words are FIXED in `ufli_lesson_configs.js`. Do not add, remove, or reorder. Core/fringe tags = research-based AAC frequency. The vocabulary is a DECODE target, not an instruction target.

**Nonfiction (Gr 6–10):**
Tier 2 academic words + Tier 3 content words. Max ~20–30 fringe per unit. Every unit shares response core words (*because, show, prove, true, wrong, same, different, agree*) — consistent motor pattern across all 6 units.
⚠️ Capitol Crawl: add *disability* to fringe word list (vocabulary framework gap identified 2026-03-29)

**Fiction Anchor Texts:**
Priority order is LOCKED — do not invert:
1. Emotional/mental state vocabulary (*feel, scared, hope, decide, change, believe*)
2. Relational/causal language (*because, if, then, maybe, probably*)
3. Narrative fringe — description NOT name (*tall, angry, runs, hides, home*)
4. Skill-specific vocabulary (*character, trait, narrator, theme*)
Character names = always fringe. Never design for name recall.

**Picture Book Companions (K–3):**
IRA read-aloud vocabulary + thematic conceptual vocabulary. Max ~15–20 per book. Every word must be ARASAAC-symbolizable and 1–2 touch accessible.

---

## SGD Motor Planning

- Core + Tier 2 academic words used across 3+ lessons → 1-hit accessible (home page)
- Unit-specific fringe content → navigation is acceptable
- Lead time: 2 weeks recommended; 1 week minimum. CAP is the SLP handoff document.
- Vocabulary must stay in the SAME location across all activities in a unit. Consistency = motor automaticity.
- Every teacher doc includes aided language modeling guidance for partners.

---

## Symbol Rules

- Every fringe word = ARASAAC symbol. Check `_Operations/symbol_cache/` first.
- Symbol + printed word always together — never symbol alone.
- Fitzgerald Key border = grammatical category. Green=verbs, orange=adjectives, yellow=pronouns, white/grey=nouns, blue=prepositions, pink=social/feelings.
- Missing symbol → flag before build. Do not substitute a semantically wrong symbol.

---

## QC Gates (required before any product goes live)

**Gate 1: Word Selection**
- [ ] Tier 2 academic vocabulary identified?
- [ ] Tier 3 content vocabulary identified?
- [ ] AAC Access Layer tagged for each word (core/fringe)?
- [ ] Instructional Layer tagged (explicit / background / generative)?
- [ ] Total fringe ≤30?
- [ ] Top 5 Core + Top 5 Fringe selected?

**Gate 2: Symbol Coverage**
- [ ] Every fringe word has ARASAAC symbol in symbol_cache?
- [ ] Missing symbols flagged and resolved before build?
- [ ] Correct Fitzgerald Key border color?

**Gate 3: Motor Planning**
- [ ] Core/response words identified as 1-hit accessible?
- [ ] SLP lead time guidance in CAP?
- [ ] Aided language modeling guidance in teacher document?
- [ ] Vocabulary location consistent across all activities in the unit?

**Gate 4: Instructional Coverage**
- [ ] Each Explicit Instruction Target in 3+ activities?
- [ ] Vocabulary Preview Routine present?
- [ ] Sentence frames use response vocabulary + fringe targets?
- [ ] Multiple response pathways available?

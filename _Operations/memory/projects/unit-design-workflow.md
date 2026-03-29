# CbD Nonfiction Unit Design Workflow — Learnings & Standards

## Build Sequence (Proven Across 4+ Units)

### Phase 0 — Topic Analysis (Do This Before Any Template Decisions)

The topic drives the product — not the other way around. Before committing to a skill number, format, or age range, evaluate what the topic itself can support.

**Step 0a: Read the Master Reference**
Read `CbD_Unit_Design_Master_Reference.md` (ALWAYS first). This grounds you in the design system, skill grid, and existing product inventory.

**Step 0b: Research the Topic**
Gather available resources: primary sources, historical accounts, photographs, court documents, first-person narratives, data sets — whatever exists. Ask:
- What primary and secondary sources are available and accessible?
- How rich is the source material? (A single strong article vs. a deep archive)
- What perspectives are represented? Whose voices are present? Whose are missing?
- Is there existing curriculum coverage? (High competition = less opportunity)

**Step 0c: Determine Best Age Range and Version Strategy**
Let the content complexity decide the audience — don't default to a grade band.
- What reading level does the source material naturally sit at?
- What background knowledge does the topic require?
- Are there age-sensitive themes (violence, injustice, death) that set a floor?
- Where is the strongest classroom fit? (Elementary, middle, high — or cross-age?)

**Version strategy (locked):** V1 is the grade-level anchor for the target audience. V2 and V3 step DOWN from there. The purpose of versioning is to remove the Lexile barrier so students can focus on the target skill. If a student is spending cognitive energy decoding, they can't do the analytical work — text structure, sourcing, CER, perspective analysis. The reading level is the vehicle, not the destination. The skill practice is the hard part.
- V1: On grade level (Lexile range appropriate to target audience)
- V2: One step below — reduced sentence complexity, supported vocabulary
- V3: Two steps below — simplified syntax, key vocabulary highlighted, scaffolded access
- All three versions do the SAME analytical work on the SAME skill. The scaffold varies, the expectation does not.

**Step 0d: Determine the Arc and Scope**
Based on what's available, decide how many passages (1–4) and what shape the product takes:
- **1 passage** — The topic is powerful but contained. A single text with deep comprehension work. (Likely a mini-lesson or freebie.)
- **2 passages** — Two texts that create a comparison, a shift, or a before/after. Natural fit for a lesson. (Model: Capitol Crawl, Zitkala-Ša)
- **3–4 passages** — The topic has a full narrative arc — multiple perspectives, a timeline, cause and consequence. Earns full unit status. (Model: 504 Sit-In, Frances Kelsey)
- Ask: What is the story arc? Does it build, contrast, or reveal? How many texts does it take to get there?

**Step 0e: Select Target Skill**
Choose the target reading skill from the skill grid. The topic research should point toward it, but this is a deliberate decision — the skill shapes the text interaction tool, the graphic organizer, and the comprehension activity design for the entire product.
- What reading skill fits most naturally based on what the sources demand? (Check the skill grid.)
- Confirm: skill number, text interaction tool, and graphic organizer type
- All passage activities and comprehension work build toward this skill — it's the instructional throughline

**Step 0f: Write the Essential Question**
Every unit needs an essential question that gives the reading a purpose beyond the skill itself. This is the "why should I care?" that students carry through every passage.
- The essential question should be arguable, not googleable
- It should connect the topic to something bigger — justice, identity, power, responsibility, voice
- It appears on the title page, in teacher materials, and drives discussion/project work
- Draft it now; refine it during content drafting if needed

**Step 0g: Evaluate Project Potential**
Does the topic support MORE than a targeted reading skill? If so, consider a culminating project:
- Does it connect to a real-world action, discipline, or community?
- Is there enough depth for students to synthesize, create, or take a position?
- Would a project elevate the product from "reading practice" to "learning experience"?
- If yes → design a project component. If no → the comprehension activities are enough.

**Step 0h: Checkpoint — User Approves Topic Analysis**
Before any drafting begins, confirm: essential question, age range, version strategy, number of passages, arc, target skill (with tool and organizer), and whether a project is included. This is the product blueprint.

---

### Phase 1 — Draft and Build

```
1. Draft markdown content (passages × versions, comprehension, teacher materials, project if applicable)
2. Checkpoint: User approves content
3. Write build script (model from Capitol Crawl for 2-part lessons, 504 Sit-In for 4-part units)
4. Run build → debug → verify XML
5. Run Inclusive Design Diagnostic (THE FULL PROMPT — see below)
6. Implement quick wins from diagnostic
7. Rebuild + verify
8. Update Master Reference + CLAUDE.md
```

---

## Inclusive Design Diagnostic Prompt

**MANDATORY: Run this prompt AFTER drafting content, BEFORE building the .docx.** This catches pedagogical gaps early, before they're baked into the build script.

```
Role: You are an expert Curriculum Specialist and Inclusive Instructional Designer. Your expertise is grounded in the Science of Reading, Universal Design for Learning (UDL), and the SETT Framework (Student, Environment, Tasks, Tools).

Task: Perform a high-level diagnostic evaluation of the attached ELA Educational Unit. Your analysis must determine the unit's effectiveness in supporting all learners, including students with complex communication needs (CCN) who utilize Augmentative and Alternative Communication (AAC) and students with specific learning disabilities.

Evaluation Frameworks:

1. CCSS Rigor & Depth of Knowledge (DOK):
   * Identify specific Grade-Level ELA Standards addressed.
   * Rigor Check: Analyze if the tasks reach DOK Level 3 (Strategic Thinking) or 4 (Extended Thinking). If the unit focuses solely on recall, suggest ways to pivot to "sensemaking" and "disciplinary literacy" (e.g., reading like a historian or scientist).

2. High-Leverage Practices (HLPs) & Explicit Instruction:
   * HLP 16 (Explicit Instruction): Evaluate the "I Do, We Do, You Do" sequence. Is there a clear model of metacognitive "self-talk"?
   * HLP 11 (Goal Setting): Are goals specific, measurable, and aligned with grade-level content?
   * HLP 15 (Scaffolded Supports): Identify the presence of "temporary scaffolds" (graphic organizers, sentence frames, or word matrices) and provide a plan for their systematic fading to foster independence.

3. UDL Guidelines 3.0 (Joy & Agency):
   * Engagement: Does the unit provide "low floor/high ceiling" tasks that allow for "productive struggle"?
   * Representation (The "How"): Check for accessibility—is the text compatible with screen readers or text-to-speech? Is there a "picture walk" or background-building phase?
   * Action & Expression: Evaluate options for students with CCN. Can they demonstrate mastery through an AAC device, a digital interactive notebook, or an "alternative pencil"?

4. Evidence-Based Literacy & Vocabulary:
   * Morphology & Tier 2: Is there explicit morphology instruction (prefixes, suffixes, bases) using a word matrix?
   * Text-Dependency: Evaluate if comprehension questions require deep evidence from the text or rely on outside personal experience.
   * Shared Reading/Writing: For students with extensive support needs, does the unit incorporate predictable chart writing or interactive shared reading routines (CAR/CROWD)?

Output Format:
* Executive Summary: A concise synthesis of the unit's pedagogical strengths and its current level of "inclusive readiness."
* Gap Analysis: A targeted list of missing elements specifically regarding AAC integration, morphology instruction, and systematic prompt fading.
* Quick Wins (3-5 Actionable Suggestions): High-impact, evidence-based modifications (e.g., "Incorporate a Tier 2 Word Map" or "Add a Graphic Organizer for Critical Lenses").
* The "SETT" Perspective: A brief concluding thought on what Tools or Environmental changes would further reduce barriers to the identified Tasks.
```

---

## Standard Quick Wins Checklist (Apply to Every Unit)

These emerged from the Zitkala-Ša diagnostic and should be included by default in all future units:

- [ ] **Word Parts morphology handout** — break 3-5 key Tier 2/3 words into prefix/base/suffix with a "Try It" exercise
- [ ] **Student-facing learning targets** on every primary instructional handout (not reference sheets)
- [ ] **Text structure / skill-specific visual reference card** — half-page desk reference with icons, signal words, metaphors
- [ ] **Scaffold fading rationale** — explicit teacher-facing explanation of WHY scaffolds decrease across parts/lessons (cite HLP 15)
- [ ] **V3 DOK 3 MCQ** — at least 1 structure/skill-analysis question per V3 MCQ set so V3 students also practice higher-order reasoning in selected-response format

---

## Build Script Patterns (Proven)

### 2-Part Lesson (model: Capitol Crawl, Zitkala-Ša)
- ~960 lines
- Build script in product folder (not _Operations)
- `require` template via relative path to `_Operations/cbd_docx_template.js`
- Passage extraction via regex from draft markdown
- Teacher materials hardcoded in script
- Comprehension activities manually built (not auto-parsed from markdown)
- Output: `../{Name}_Lesson_COMPLETE.docx`

### 4-Part Full Unit (model: 504 Sit-In, Frances Kelsey)
- ~1,500-2,000+ lines
- Build script in `_Operations/`
- Multi-session work required
- Build in phases: teacher docs → passages → comprehension → answer keys
- Rebuild + validate XML after each phase

### Critical Build Warnings
- **ALWAYS spread array-returning template functions** — missing `...` causes `<0/>` XML corruption
- **`studentHandoutHeader` takes 3 args:** `(unitTitle, title, subtitle)`
- **`titlePage` opts:** match property names exactly (`unitTitle`, `unitSubtitle`, `skillNumber`, `skillName`, `gradeRange`, `versions`, `parts`)
- **`assembleAndWrite` arg order:** `(unitShortTitle, children, outputPath, meta)` — title first
- **Regex en-dash:** Use `.` or the actual `–` character to match en-dashes in Lexile ranges
- **V3 passage extraction:** Strip `**Key Vocabulary**` heading from extracted text — the template's `buildPassageParagraphs` V3 mode adds its own "Key Vocabulary" header. Leaving it in causes a duplicate.
- **V3 passage extraction regex boundary:** Do NOT use `---\s*\n` as end boundary — it matches the `---` separator between V3 Key Vocabulary boxes and the passage text, truncating the extraction to just the vocab. Use `\*Word count:` or `## ` as boundaries instead.
- **V3 MCQ/SA page breaks:** Do NOT pass `isV3=true` to `mcqPageHeader` or `saPageHeader` when each part's MCQ/SA is built in a separate loop. The `isV3` inline mode is for consolidating sections within a single part on one page (e.g., passage + MCQ on same page). When MCQ sections are separate handouts, always use `false` so each gets its own page break.
- **MCQ question spacing:** Use `before: 160` (not 280) for MCQ question stems to keep all 5 questions on one page. The template's `mcqChoice()` uses `before: 60, after: 60, line: 276` which can't be changed from the build script. If questions still split, consider `keepNext: true` on question paragraphs (requires building `new Paragraph()` directly instead of using `T.p()`).
- **Table header text:** Avoid special characters (¶, §, etc.) in table headers — they render literally in Word. Use plain text only.

---

## Skill-Specific Design Notes

### Skill #3 — Text Structure Analysis (Zitkala-Ša)
- **NO annotation codes** — uses Structure Mapping Organizer (3-column graphic organizer)
- Text structures taught: cause → effect and problem → solution
- Structure shift between parts mirrors the subject's life arc — this is a powerful design pattern
- Evidence Sort works well for cause/effect categorization
- Progressive scaffolding: pre-labeled organizer (Part 1 V3) → blank organizer (Part 2 all versions)
- Signal word instruction is central — include a reference card

### Skill #6 — Sourcing / Corroboration (Capitol Crawl)
- Uses Source Tracking Chart (4-column)
- Comprehension: ESR + MCQ (Part 1), CEM + SA (Part 2)

### Skill #4 — Author's Purpose / Perspective (504 Sit-In)
- Uses Perspective Tracking Chart (3-column)
- 4-part unit, not a lesson

### Skill #5 — Claim, Evidence, Reasoning (Frances Kelsey)
- CER framework (McNeill & Krajcik)
- 4-part unit

---

## QC Verification Checklist (Post-Build)

### Structural
- [ ] Zero XML corruption (`<0/>` tags)
- [ ] Heading hierarchy (H1 → H2 → H3, no skips)
- [ ] Table header rows tagged for screen readers
- [ ] Page breaks present (via `pageBreakBefore`)
- [ ] All brand colors correct (Navy #1B1F3B, Teal #006DA0, Amber #FFB703)

### Content
- [ ] All passages present (versions × parts)
- [ ] All comprehension activities present (by version)
- [ ] Answer key complete
- [ ] Accessibility Statement included
- [ ] Essential question appears in multiple locations

### Inclusive Language
- [ ] Zero deficit-framing violations (no "below grade level," "struggling readers," etc.)
- [ ] All "point to" instances paired with inclusive alternatives
- [ ] Strength-based language throughout
- [ ] AAC-inclusive verbs (select, indicate, identify — not just "point to")

---

## Seasonal Hooks by Unit

| Unit | Seasonal Hook | List By |
|------|--------------|---------|
| Zitkala-Ša | Native American Heritage Month (November) | Oct 15 |
| Capitol Crawl + 504 Sit-In | Disability Pride Month (July) | Jun 25 |
| Tommie Smith & John Carlos | Black History Month (February) | Jan 15, 2027 |

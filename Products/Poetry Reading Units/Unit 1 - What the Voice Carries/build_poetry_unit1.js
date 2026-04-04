#!/usr/bin/env node

/**
 * Poetry Reading Unit 1 — What the Voice Carries
 * Communicate by Design
 *
 * Skill: Figurative Language Analysis (RL.6.4 / RL.7.4 / L.5.5a–c)
 * Strategy: NOTICE / FEEL / MEAN / ASK (NFMA)
 * Poems: Dunbar · Dickinson · Markham · CbD Original
 * Grade Band: 6–10 | Price: $9.95
 *
 * Output: What_the_Voice_Carries_COMPLETE.docx
 *
 * Color override: Violet (#6B21A8) replaces Teal for poetry product line
 * Run: node build_poetry_unit1.js
 */

const path = require("path");
const T = require(path.join(__dirname, "..", "..", "..", "_Operations", "Build", "cbd_docx_template"));
// Use the SAME docx instance as the template to ensure class compatibility
const { Paragraph, TextRun, BorderStyle, HeadingLevel, AlignmentType } = T;

const CW = T.CONTENT_WIDTH;
const FONT = "Arial";

// ─────────────────────────────────────────────────────────────────────────
// POETRY LINE COLOR CONSTANTS
// ─────────────────────────────────────────────────────────────────────────
const VIOLET     = "6B21A8";  // Deep Violet — docs/pdf — WCAG AAA on white (~12:1)
const NAVY       = "1B1F3B";  // Deep Ink Navy
const AMBER      = "FFB703";  // Warm Amber

// ─────────────────────────────────────────────────────────────────────────
// COLUMN WIDTH HELPERS
// ─────────────────────────────────────────────────────────────────────────
const col2 = (a, b) => [Math.round(CW * a), Math.round(CW * b)];
const col3 = (a, b, c) => [Math.round(CW * a), Math.round(CW * b), Math.round(CW * c)];
const col4 = (a, b, c, d) => [Math.round(CW * a), Math.round(CW * b), Math.round(CW * c), Math.round(CW * d)];
const col5 = (a, b, c, d, e) => [Math.round(CW * a), Math.round(CW * b), Math.round(CW * c), Math.round(CW * d), Math.round(CW * e)];

// ─────────────────────────────────────────────────────────────────────────
// VIOLET HEADING OVERRIDES (replaces teal borders/text with violet)
// ─────────────────────────────────────────────────────────────────────────
function vh1(text, pageBreak = true) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: pageBreak ? 0 : 360, after: 200 },
    ...(pageBreak ? { pageBreakBefore: true } : {}),
    border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: VIOLET, space: 4 } },
    children: [new TextRun({ text, font: FONT, size: 36, bold: true, color: NAVY })],
  });
}

function vh3(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_3,
    spacing: { before: 200, after: 120 },
    children: [new TextRun({ text, font: FONT, size: 24, bold: true, color: VIOLET })],
  });
}

// ─────────────────────────────────────────────────────────────────────────
// POEM FORMATTING HELPERS
// ─────────────────────────────────────────────────────────────────────────

/** Single line of a poem — italic, indented, tight spacing */
function pLine(text, indent = 720) {
  return new Paragraph({
    spacing: { after: 20, line: 240 },
    indent: { left: indent },
    children: [new TextRun({ text, font: FONT, size: 22, italics: true, color: NAVY })],
  });
}

/** Blank stanza break inside a poem */
function pBreak() {
  return new Paragraph({ spacing: { after: 100 } });
}

/** Poem title + attribution block — violet border left */
function poemBlock(title, author, year, lines) {
  const items = [];
  items.push(new Paragraph({
    spacing: { before: 160, after: 60 },
    border: { left: { style: BorderStyle.SINGLE, size: 8, color: VIOLET, space: 8 } },
    indent: { left: 480 },
    children: [
      new TextRun({ text: title, font: FONT, size: 24, bold: true, color: NAVY }),
      new TextRun({ text: `  —  ${author} (${year})`, font: FONT, size: 20, italics: true, color: "555555" }),
    ],
  }));
  for (const l of lines) {
    if (l === "") {
      items.push(pBreak());
    } else if (l.startsWith("    ")) {
      items.push(pLine(l.trimStart(), 1080));
    } else {
      items.push(pLine(l, 720));
    }
  }
  items.push(T.spacer(120));
  return items;
}

/** Version activity block — V1/V2/V3 scaffold for one NFMA step */
function versionBlock(step, v1, v2, v3) {
  return [
    vh3(`${step}`),
    T.makeTable(
      ["Version", "Activity"],
      [
        ["V1", v1],
        ["V2", v2],
        ["V3", v3],
      ],
      col2(0.12, 0.88),
      { compact: true }
    ),
    T.spacer(),
  ];
}

/** Callout box — amber border, teacher note */
function callout(text) {
  return new Paragraph({
    spacing: { before: 120, after: 120, line: 276 },
    indent: { left: 480, right: 480 },
    border: { left: { style: BorderStyle.SINGLE, size: 8, color: AMBER, space: 8 } },
    children: [new TextRun({ text, font: FONT, size: 20, italics: true, color: NAVY })],
  });
}

// ─────────────────────────────────────────────────────────────────────────
// BUILD CHILDREN ARRAY
// ─────────────────────────────────────────────────────────────────────────
const children = [];

// ═══════════════════════════════════════════════════════════════════════
// TITLE PAGE
// ═══════════════════════════════════════════════════════════════════════

children.push(...T.titlePage({
  unitTitle:    "What the Voice Carries",
  unitSubtitle: "Figurative Language in Poetry",
  skillNumber:  "",
  skillName:    "Figurative Language Analysis",
  gradeRange:   "6–10",
  productLine:  "A Poetry Reading Unit",
  versions:     "Poetry Reading Unit · NFMA Strategy",
  parts:        "4 Poems · V1 / V2 / V3 Access Levels",
}));

// ═══════════════════════════════════════════════════════════════════════
// TABLE OF CONTENTS
// ═══════════════════════════════════════════════════════════════════════

children.push(...T.tocPage());

// ═══════════════════════════════════════════════════════════════════════
// SECTION 1 — ABOUT THIS UNIT
// ═══════════════════════════════════════════════════════════════════════

children.push(vh1("About This Unit"));
children.push(T.teacherRefLabel());

children.push(T.makeTable(
  ["Element", "Detail"],
  [
    ["Unit Title",       "What the Voice Carries — Figurative Language in Poetry"],
    ["Product Line",     "Poetry Reading Units · Communicate by Design"],
    ["Targeted Skill",   "Figurative Language Analysis"],
    ["Standards",        "RL.6.4 · RL.7.4 · L.5.5a–c"],
    ["Grade Band",       "6–10 (differentiated by access level, not by text)"],
    ["Strategy",         "NOTICE / FEEL / MEAN / ASK (NFMA)"],
    ["Poems",            "We Wear the Mask (Dunbar) · I'm Nobody! (Dickinson) · The Man with the Hoe (Markham) · The Words I Carry (CbD Original)"],
    ["Access Levels",    "V1 / V2 / V3 — same poem at all levels; scaffold varies"],
    ["Price",            "$9.95"],
  ],
  col2(0.28, 0.72)
));

children.push(T.spacer());
children.push(T.heading2("What This Unit Is"));
children.push(T.p(
  "This is an access-layer poetry unit for grades 6–10. All four poems are presented at every access level — " +
  "V1, V2, and V3 — using the same text. What changes is the depth of the annotation scaffold, the structure " +
  "of the response frame, and the intensity of communication partner support. The poem itself does not change. " +
  "Simplifying a poem produces a different poem — and that is not differentiation, it is modification."
));
children.push(T.p(
  "The scaffold varies. The expectation does not. Every student engages with the same four poems, " +
  "the same skill (figurative language analysis), and the same standards."
));

children.push(T.heading2("What This Unit Is Not"));
children.push(...T.bulletList([
  "A simplified or rewritten version of any poem",
  "A survey of poetic forms (this unit targets one skill — figurative language — across four poems)",
  "A resource that requires a high-tech AAC device (all activities work with any access method)",
  "An enrichment add-on — this is SDI-level instruction that meets IDEA standards",
]));

children.push(T.heading2("What's Included"));
children.push(...T.bulletList([
  "Teacher reference (this document): all four poems with NFMA activities, vocabulary support, partner guidance, IEP goal stems, and rubric",
  "Student Poetry Packet (separate PDF): student-facing NFMA response pages in V1/V2/V3 format",
  "Communication Access Packet (separate PDF): fringe vocabulary cards, priority vocabulary page, SLP handoff",
  "Session Tracker (separate PDF): para-administered data collection tool",
]));

// ═══════════════════════════════════════════════════════════════════════
// SECTION 2 — STANDARDS ALIGNMENT
// ═══════════════════════════════════════════════════════════════════════

children.push(vh1("Standards Alignment"));
children.push(T.teacherRefLabel());

children.push(T.tableCaption("Table: Primary ELA Standards — what each standard requires and where it appears in this unit"));
children.push(T.makeTable(
  ["Standard", "What It Requires", "Where in This Unit"],
  [
    ["RL.6.4 / RL.7.4",
     "Determine the meaning of words and phrases as used in a text, including figurative and connotative meanings; analyze the cumulative impact of word choices on meaning and tone",
     "NOTICE and MEAN steps of every NFMA activity; Criterion 3 and 4 of rubric"],
    ["L.5.5a",
     "Interpret figurative language, including similes and metaphors, in context",
     "NOTICE step (identify type) and MEAN step (interpret meaning)"],
    ["L.5.5b",
     "Recognize and explain the meaning of common idioms, adages, and proverbs",
     "Background context in Dunbar and Dickinson poem notes"],
    ["L.5.5c",
     "Use the relationship between particular words to better understand each word's meaning",
     "Vocabulary Preview and FEEL step (connotation of emotional vocabulary)"],
    ["RL.6.1 / RL.7.1",
     "Cite textual evidence to support analysis",
     "ASK step of every NFMA activity — evidence identification required"],
  ],
  col3(0.18, 0.44, 0.38),
  { compact: true }
));

children.push(T.spacer());
children.push(T.heading2("Grade-Band Crosswalk"));
children.push(T.p(
  "RL.6.4 and RL.7.4 are the primary anchors. Grades 8–10 extend naturally to RL.8.4 (analyze the impact " +
  "of word choices including analogies or allusions) and RL.9-10.4 (cumulative impact of diction). " +
  "The NFMA strategy and all four poems scale across all five grade levels. Adjust the MEAN and ASK " +
  "response expectations for grades 8–10 to require more precise diction analysis."
));

// ═══════════════════════════════════════════════════════════════════════
// SECTION 3 — THE NFMA STRATEGY
// ═══════════════════════════════════════════════════════════════════════

children.push(vh1("The NFMA Strategy"));
children.push(T.teacherRefLabel());

children.push(T.p(
  "NOTICE / FEEL / MEAN / ASK (NFMA) is Communicate by Design's original poetry analysis strategy. " +
  "It was designed as an AAC-compatible alternative to TPCASTT, which requires extended paraphrasing " +
  "and metacognitive language production that is not accessible to most AAC users. NFMA uses four steps " +
  "built entirely from high-frequency core vocabulary words already on most robust AAC systems."
));

children.push(T.tableCaption("Table: NFMA — Four steps, standard connections, and AAC vocabulary"));
children.push(T.makeTable(
  ["Step", "What the Student Does", "Standard Connection", "AAC Vocabulary"],
  [
    ["N — NOTICE",
     "Identify specific language that stands out — a line, phrase, or word that seems intentional",
     "RL.x.4 — determine the meaning of words and phrases",
     "show, point, find, what, here"],
    ["F — FEEL",
     "Name the mood or feeling the language creates — a gateway step before interpretation",
     "RL.x.4 — connotative meanings; L.5.5c — word relationships",
     "feel, sad, proud, lonely, free, different, alone"],
    ["M — MEAN",
     "Interpret what the figurative language means beyond the literal — what the poet is really saying",
     "RL.x.4 — cumulative impact on meaning and tone",
     "mean, because, really, show, same, not, true"],
    ["A — ASK",
     "Generate a question and identify one line of textual evidence",
     "RL.x.1 — cite textual evidence to support analysis",
     "wonder, why, where, who, find, prove, show"],
  ],
  col4(0.12, 0.32, 0.28, 0.28),
  { compact: true }
));

children.push(T.spacer());
children.push(callout(
  "Research basis: NFMA is grounded in the Self-Regulated Strategy Development (SRSD) framework " +
  "(Harris & Graham, 2008) — a cognitive strategy instruction model with strong evidence for students " +
  "with learning differences. Cognitive strategies that use mnemonic anchors (NOTICE, FEEL, MEAN, ASK) " +
  "reduce cognitive load and support students who benefit from explicit structure, including AAC users."
));

children.push(T.spacer());
children.push(T.heading2("Teaching NFMA — Before You Start"));
children.push(...T.bulletList([
  "Introduce all four NFMA steps explicitly before the first poem — post the strategy chart in the classroom",
  "Model each step with a short, familiar example before applying it to the anchor poems",
  "The FEEL step is a gate — students who cannot name a feeling cannot move to MEAN. Use the feeling vocabulary board before every poem",
  "The MEAN step requires interpretation, not recall. A student who says 'the mask covers a face' has not reached MEAN yet — continue prompting",
  "The ASK step is the hardest — scaffold with the sentence frame 'I wonder _____' before asking for open-ended questions",
]));

// ═══════════════════════════════════════════════════════════════════════
// SECTION 4 — MEET THE POEMS
// ═══════════════════════════════════════════════════════════════════════

children.push(vh1("Meet the Poems"));
children.push(T.teacherRefLabel());

children.push(T.tableCaption("Table: Four poems — themes, primary figurative device, and teaching notes"));
children.push(T.makeTable(
  ["Poem", "Poet / Year", "Primary Device", "Theme Connection", "Teaching Note"],
  [
    ["We Wear the Mask",
     "Paul Laurence Dunbar · 1896",
     "Extended metaphor (mask = hiding pain)",
     "Identity, survival, hidden suffering",
     "The mask is not a choice for pleasure — it is survival. Students must reach this in the MEAN step."],
    ["I'm Nobody! Who are you?",
     "Emily Dickinson · c. 1891",
     "Metaphor (Nobody/Somebody as identity categories) + irony",
     "Identity, community, rejecting public performance",
     "Tone is playful and conspiratorial — not sad. Dickinson celebrates being 'nobody.' Students who identify as sad are reading the surface only."],
    ["The Man with the Hoe",
     "Edwin Markham · 1913",
     "Imagery (exhausted body as evidence of oppression)",
     "Labor, dignity, social responsibility",
     "Most complex poem linguistically. In V3, read one stanza at a time with pause. Define 'hoe' before reading. Do not require knowledge of Millet's painting."],
    ["The Words I Carry",
     "Communicate by Design · 2026",
     "Metaphor (voice = river, words = stones) + imagery",
     "Voice, identity, communication access",
     "The speaker is matter-of-fact — not asking for sympathy. Let students respond to the poem on its terms before discussing AAC connection."],
  ],
  col5(0.22, 0.20, 0.20, 0.20, 0.18),
  { compact: true }
));

children.push(T.spacer());
children.push(T.heading2("Copyright and Source Notes"));
children.push(T.p(
  "All three anchor poems are in the public domain. Dunbar's poem was published in 1896 and " +
  "is freely available through Project Gutenberg (eBook #18338). Dickinson's poem was published " +
  "posthumously circa 1891 and is in the public domain. Markham's poem was published in a 1913 collection " +
  "and is in the public domain. 'The Words I Carry' is an original poem by Communicate by Design — " +
  "all rights reserved; may not be reproduced outside CbD products."
));

// ═══════════════════════════════════════════════════════════════════════
// SECTION 5 — VOCABULARY PREVIEW
// ═══════════════════════════════════════════════════════════════════════

children.push(vh1("Vocabulary Preview"));
children.push(T.teacherRefLabel());

children.push(T.p(
  "This unit uses 10 fringe words that must be pre-programmed before Day 1. All 10 are in the " +
  "Communication Access Packet. The five literary device terms are the primary instruction targets — " +
  "these are the words students will use to demonstrate the standard. The other five are supporting vocabulary."
));

children.push(T.tableCaption("Table: Fringe vocabulary — 10 words to pre-program via CAP (SLP lead time: 2 weeks)"));
children.push(T.makeTable(
  ["Word", "Type", "Instructional Role", "Fitzgerald Key", "Notes"],
  [
    ["figurative language", "Fringe · Tier 3", "Explicit instruction target ★ Top 5", "White/Grey", "Unit overarching term. Teach before Day 1. No ARASAAC symbol — use text label card."],
    ["metaphor",           "Fringe · Tier 3", "Explicit instruction target ★ Top 5", "White/Grey", "Primary device in Dunbar and CbD poem. No ARASAAC symbol — use text label card."],
    ["imagery",            "Fringe · Tier 3", "Explicit instruction target ★ Top 5", "White/Grey", "Primary device in Markham and CbD poem. No ARASAAC symbol — use text label card."],
    ["tone",               "Fringe · Tier 3", "Explicit instruction target ★ Top 5", "White/Grey", "Connects FEEL → MEAN across all 4 poems. No ARASAAC symbol — use text label card."],
    ["speaker",            "Fringe · Tier 3", "Explicit instruction target ★ Top 5", "White/Grey", "Who is talking? Applies to all 4 poems. ARASAAC symbol: arasaac_speaker.png"],
    ["mask",               "Fringe · Tier 3", "Explicit instruction target + Background", "White/Grey", "Literal object first, then metaphor (Dunbar). ARASAAC symbol: arasaac_mask.png"],
    ["pretend",            "Fringe · Tier 2", "Generative (response vocabulary)",    "Green",       "Connects to Dunbar mask theme. No ARASAAC symbol — use text label card."],
    ["voice",              "Fringe · Tier 2", "Generative (unit title concept)",      "White/Grey",  "Generative across all 4 poems. ARASAAC symbol: arasaac_voice.png"],
    ["labor",              "Fringe · Tier 3", "Background (Markham context)",         "White/Grey",  "Theme vocabulary for Markham only. ARASAAC symbol: arasaac_labor.png"],
    ["hoe",                "Fringe · Tier 3", "Background (Markham title)",           "White/Grey",  "Concrete tool. Define before reading. ARASAAC symbol: arasaac_hoe.png"],
  ],
  col5(0.16, 0.16, 0.22, 0.14, 0.32),
  { compact: true }
));

children.push(T.spacer());
children.push(T.heading2("Semi-Core Words — Verify Before Day 1"));
children.push(T.p(
  "These five words carry the FEEL step of every NFMA activity. They are likely already on most robust " +
  "AAC systems, but the team should confirm they are accessible before the unit begins. If absent, add to the CAP fringe list."
));
children.push(T.makeTable(
  ["Word", "Fitzgerald Key", "NFMA Role"],
  [
    ["hide",  "Green (verb)",       "FEEL/MEAN — Dunbar mask theme"],
    ["pain",  "Pink (feeling)",     "FEEL — Dunbar and Markham"],
    ["proud", "Pink (feeling)",     "FEEL — Dickinson and CbD poem"],
    ["alone", "Pink (feeling)",     "FEEL — Dickinson and Dunbar"],
    ["free",  "Pink (feeling)",     "FEEL/MEAN — CbD poem"],
  ],
  col3(0.18, 0.22, 0.60),
  { compact: true }
));

children.push(T.spacer());
children.push(callout(
  "Response Core (already on most robust systems — no pre-programming needed): " +
  "because · show · prove · agree · same · different · not · true · wrong · feel · mean · notice · ask. " +
  "Students who have used CbD nonfiction units already have these words as motor patterns. " +
  "Poetry units use the same response core — intentional design decision."
));

// ═══════════════════════════════════════════════════════════════════════
// SECTION 6 — COMMUNICATION ACCESS
// ═══════════════════════════════════════════════════════════════════════

children.push(vh1("Communication Access"));
children.push(T.teacherRefLabel());

children.push(T.p(
  "All four poems are delivered via partner read-aloud — for every student, at every access level. " +
  "This is not an accommodation. Read-aloud is the instructional delivery method for poetry. " +
  "The text is heard and seen simultaneously. A student who uses an SGD, an e-trans board, symbol cards, " +
  "or any other access method participates fully at V1, V2, or V3."
));

children.push(T.heading2("CAP Vocabulary — Team Coordination"));
children.push(T.p(
  "Share the Communication Access Packet with all team members — including the SLP, if one is on the team — " +
  "at least two weeks before Day 1. The packet includes all 10 fringe words with Fitzgerald Key categories, ARASAAC symbols " +
  "where available, and text label cards for abstract literary terms. The team should confirm " +
  "all five semi-core words (hide, pain, proud, alone, free) are accessible on the student's system before instruction begins."
));

children.push(T.tableCaption("Table: Fitzgerald Key — color categories for vocabulary in this unit"));
children.push(T.makeTable(
  ["Color", "Category", "Words in This Unit"],
  [
    ["Green",      "Verbs",         "hide · pretend"],
    ["Pink",       "Feelings/Social", "pain · proud · alone · free"],
    ["White/Grey", "Nouns/Other",   "figurative language · metaphor · imagery · tone · speaker · mask · voice · labor · hoe"],
  ],
  col3(0.14, 0.22, 0.64),
  { compact: true }
));

children.push(T.spacer());
children.push(T.heading2("Response Modes — All Are Valid and Equivalent"));
children.push(...T.bulletList([
  "AAC device output — selecting symbols on SGD",
  "E-trans board or PECS card selection",
  "Pointing or eye gaze to text, symbol card, or choice field on the student packet",
  "Writing or typing a response",
  "Spoken response",
  "Partner scribing student's indicated response",
]));
children.push(callout(
  "Scoring note: A student who points to a line in the poem has cited textual evidence. " +
  "A student who selects a symbol card has named a vocabulary word. " +
  "Do not require verbal or written output for 'Meets' on the rubric — all valid response modes count equally."
));

// ═══════════════════════════════════════════════════════════════════════
// SECTION 7 — COMMUNICATION PARTNER GUIDANCE
// ═══════════════════════════════════════════════════════════════════════

children.push(vh1("Communication Partner Guidance"));
children.push(T.teacherRefLabel());

children.push(T.p(
  "Every NFMA activity includes partner guidance at the point of use. This section provides " +
  "the foundational four behaviors — written for a Circle 3 partner (paraeducator with no prior " +
  "AAC training). Post this page where the partner can see it during instruction."
));

children.push(T.tableCaption("Table: Four partner behaviors — what each behavior looks like in a poetry lesson"));
children.push(T.makeTable(
  ["Behavior", "What It Looks Like in This Unit"],
  [
    ["Model (ALgS — Aided Language Stimulation)",
     "While reading the poem aloud, point to vocabulary on the student's device or board as the words appear. Model 'metaphor,' 'tone,' and 'feel' during the read-aloud — before asking the student to use them."],
    ["Wait (5 seconds — count silently)",
     "After every NFMA prompt, wait 5 full seconds before repeating or prompting. After each stanza in V3, pause and wait. Count '1-one-thousand, 2-one-thousand...' silently. Do not fill the silence."],
    ["Expand",
     "When the student responds with one symbol, expand it into a sentence. If the student selects 'sad,' say: 'The poem feels sad. The poet uses the mask to show sadness.' Then wait again."],
    ["Offer Choice",
     "If the student does not respond after the wait, offer two choices that include the correct answer. 'Is the poet using a metaphor or a rhyme here?' Never offer a choice without including the correct option."],
  ],
  col2(0.28, 0.72),
  { compact: true }
));

children.push(T.spacer());
children.push(callout(
  "Hard rule: Wait time is named in seconds for V3 activities. '5-second wait' is not optional — " +
  "it is the evidence-based prompt hierarchy. A partner who fills the silence immediately is the primary " +
  "barrier to AAC use. Every V3 activity in this unit specifies the wait explicitly."
));

// ═══════════════════════════════════════════════════════════════════════
// SECTION 8 — VERSION GUIDE
// ═══════════════════════════════════════════════════════════════════════

children.push(vh1("Version Guide"));
children.push(T.teacherRefLabel());

children.push(T.p(
  "This unit uses the CbD access-layer model. The poem does not change across versions. " +
  "What changes is the depth of annotation scaffolding, the response frame structure, and the " +
  "intensity of communication partner support. Version assignment is a reading access and " +
  "vocabulary access decision — not an ability label, not a communication level assignment."
));

children.push(T.tableCaption("Table: V1 / V2 / V3 — what changes and what stays the same"));
children.push(T.makeTable(
  ["Element", "V1", "V2", "V3"],
  [
    ["Poem text",         "Unchanged",            "Unchanged",            "Unchanged"],
    ["NFMA steps",        "All 4 steps",           "All 4 steps",           "All 4 steps"],
    ["Standard",          "RL.6.4/7.4",            "RL.6.4/7.4",            "RL.6.4/7.4"],
    ["Vocabulary",        "Same list, CAP active", "Same list, CAP active", "Same list, CAP + vocabulary taught within unit"],
    ["Rubric",            "Identical",             "Identical",             "Identical"],
    ["NOTICE scaffold",   "Open identification",   "2-choice field",         "Partner indicates; student selects from 3 options"],
    ["FEEL scaffold",     "Open response",          "4-choice feeling field", "Symbol choice board + sentence frame"],
    ["MEAN scaffold",     "Open analysis",          "Partial sentence frame", "3-option selection + 'I chose ___ because ___'"],
    ["ASK scaffold",      "Open question + evidence", "'I wonder ___' frame + evidence", "'I wonder ___' + point to evidence in text"],
    ["Partner role",      "Models AAC; 5-sec wait", "Models fringe; reads prompts aloud", "Reads every line; teaches vocabulary; 5-sec wait named"],
  ],
  col4(0.22, 0.25, 0.25, 0.28),
  { compact: true }
));

children.push(T.spacer());
children.push(callout(
  "IDEA compliance reminder: A student who completes any version of these activities " +
  "has demonstrated the skill — not just recalled facts. All three versions require interpretation " +
  "(MEAN) and evidence (ASK). If a V3 activity is reduced to identification only, it becomes " +
  "a modification. The V3 activities in this unit are designed to prevent that."
));

// ═══════════════════════════════════════════════════════════════════════
// POEM 1 — WE WEAR THE MASK (DUNBAR)
// ═══════════════════════════════════════════════════════════════════════

children.push(vh1("Poem 1 — We Wear the Mask"));

children.push(...poemBlock(
  "We Wear the Mask",
  "Paul Laurence Dunbar",
  "1896",
  [
    "We wear the mask that grins and lies,",
    "It hides our cheeks and shades our eyes,—",
    "This debt we pay to human guile;",
    "With torn and bleeding hearts we smile,",
    "And mouth with myriad subtleties.",
    "",
    "Why should the world be over-wise,",
    "In counting all our tears and sighs?",
    "Nay, let them only see us, while",
    "    We wear the mask.",
    "",
    "We smile, but, O great Christ, our cries",
    "To thee from tortured souls arise.",
    "We sing, but oh the clay is vile",
    "Beneath our feet, and long the mile;",
    "But let the world dream otherwise,",
    "    We wear the mask!",
  ]
));

children.push(T.heading2("Partner Notes — Before You Read"));
children.push(...T.bulletList([
  "Define 'mask' as a literal object first: 'A mask covers your face. It hides what you look like.' Then explain: 'In this poem, the mask is not a real mask — it is hiding how you really feel inside.'",
  "The word 'lies' in line 1 means 'is not true / deceives' — not 'lies down.' Pre-teach this before reading.",
  "Dunbar was a Black American poet writing in 1896. The 'mask' is a survival strategy, not a choice for comfort. Students who reach this in MEAN have understood the poem.",
]));

children.push(T.spacer());
children.push(T.heading2("NFMA Activities — We Wear the Mask"));

children.push(...versionBlock(
  "NOTICE — Identify the Figurative Language",
  "Identify one example of figurative language in this poem. Name the type (metaphor, imagery, or other) and copy the line.",
  "Circle one example of figurative language. Complete the frame: 'The poet uses _______ when they write: _______.'\n[Choice for type: metaphor / imagery / rhyme]",
  "Partner reads each stanza aloud. After each stanza, ask: 'Which line has special language — not the plain meaning?' Student indicates the line (point, gaze, tap). Then: 'What kind is it?' [Select: metaphor / imagery]. 5-second wait after each stanza before offering a choice."
));

children.push(...versionBlock(
  "FEEL — What Feeling Does This Create?",
  "What feeling does the mask metaphor create for the reader? How does it connect to the poem's overall tone? Explain.",
  "Circle the feeling this language creates: [sad · trapped · angry · proud]. Complete: 'This language creates a _______ tone because _______.'",
  "How does this part of the poem make you feel? [Symbol choice board: sad · tired · trapped · angry]. Partner asks: 'Why?' Student responds: 'It feels _______ because _______.' 5-second wait before offering a choice."
));

children.push(...versionBlock(
  "MEAN — What Is the Poet Really Saying?",
  "What is the poet really saying? What does the mask metaphor reveal about the speaker's situation and message?",
  "What does the mask mean in this poem? Complete: 'The poet uses metaphor to show that _______. This is important because _______.'",
  "What is the poet really saying? Choose one:\n  A. The speaker likes wearing masks.\n  B. The speaker hides real feelings to survive.\n  C. The speaker is performing in a play.\nUse your AAC to tell your partner why you chose it. Frame: 'I chose _______ because _______.' 5-second wait before naming the choices."
));

children.push(...versionBlock(
  "ASK — Question + Evidence",
  "What question does this poem raise for you? Find one line in the poem that supports or complicates your answer.",
  "Write one question about this poem: 'I wonder _______.' Then find one line that begins to answer it. Write the line.",
  "Ask your partner one question about the poem. Frame: 'I wonder _______.' Then show your partner one line that answers it. Point to it, tap it, or use your AAC. Partner scribes the student's question."
));

// ═══════════════════════════════════════════════════════════════════════
// POEM 2 — I'M NOBODY! WHO ARE YOU? (DICKINSON)
// ═══════════════════════════════════════════════════════════════════════

children.push(vh1("Poem 2 — I'm Nobody! Who are you?"));

children.push(...poemBlock(
  "I'm Nobody! Who are you?",
  "Emily Dickinson",
  "c. 1891",
  [
    "I'm Nobody! Who are you?",
    "Are you – Nobody – too?",
    "Then there's a pair of us!",
    "Don't tell! they'd advertise – you know!",
    "",
    "How dreary – to be – Somebody!",
    "How public – like a Frog –",
    "To tell one's name – the livelong June –",
    "To an admiring Bog!",
  ]
));

children.push(T.heading2("Partner Notes — Before You Read"));
children.push(...T.bulletList([
  "Dickinson capitalizes Nobody, Somebody, Frog, and Bog — these are figurative categories, not proper names. Explain: 'In this poem, 'Nobody' doesn't mean invisible — it means being yourself without needing everyone to know your name.'",
  "Tone is playful and conspiratorial — not sad. Dickinson is sharing a secret with the reader. Students who identify as sad are reading the surface only.",
  "The Frog/Bog image (stanza 2) is irony — the Frog's loud self-announcement is compared to 'Somebody' who craves attention. This is the hardest figurative move in the poem.",
]));

children.push(T.spacer());
children.push(T.heading2("NFMA Activities — I'm Nobody! Who are you?"));

children.push(...versionBlock(
  "NOTICE — Identify the Figurative Language",
  "Identify one example of figurative language in this poem. Name the type and copy the line. (Consider: the Frog/Bog comparison in stanza 2.)",
  "Circle one example of figurative language. Complete the frame: 'The poet uses _______ when they write: _______.' [Choice: metaphor / comparison / rhyme]",
  "Partner reads each stanza. After stanza 2, ask: 'Which line compares a person to something else?' Student indicates the line. 'What kind of language is this?' [Select: metaphor / comparison]. 5-second wait."
));

children.push(...versionBlock(
  "FEEL — What Feeling Does This Create?",
  "What feeling does Dickinson's use of 'Nobody' and 'Somebody' create? Is the speaker sad, proud, or something else? Support your answer.",
  "Circle the feeling this language creates: [proud · playful · sad · lonely]. Complete: 'Dickinson makes 'Nobody' sound _______ because _______.'",
  "How does the speaker feel about being Nobody? [Symbol choice board: proud · happy · sad · alone]. Partner asks: 'Is the speaker sad or proud?' 5-second wait. Frame: 'The speaker feels _______ because _______.' "
));

children.push(...versionBlock(
  "MEAN — What Is the Poet Really Saying?",
  "What is Dickinson really saying about 'Nobody' and 'Somebody'? What does the Frog/Bog metaphor reveal about people who seek public attention?",
  "What does Dickinson mean by 'Nobody'? Complete: 'The poet uses comparison to show that _______. The Frog means _______.'",
  "What is Dickinson really saying? Choose one:\n  A. Being 'Nobody' is lonely and sad.\n  B. Being 'Nobody' means being real — not performing for attention.\n  C. Dickinson wants to be famous like Somebody.\nFrame: 'I chose _______ because _______.' 5-second wait."
));

children.push(...versionBlock(
  "ASK — Question + Evidence",
  "What question does this poem raise? Who do you think Dickinson is talking to with 'Who are you?' Find evidence in the poem.",
  "Write one question: 'I wonder _______.' Find one line that answers it. Write the line.",
  "Ask one question: 'I wonder _______.' Point to one line that answers it. Partner scribes the question."
));

// ═══════════════════════════════════════════════════════════════════════
// POEM 3 — THE MAN WITH THE HOE (MARKHAM)
// ═══════════════════════════════════════════════════════════════════════

children.push(vh1("Poem 3 — The Man with the Hoe"));

children.push(...poemBlock(
  "The Man with the Hoe",
  "Edwin Markham",
  "1913",
  [
    "Bowed by the weight of centuries he leans",
    "Upon his hoe and gazes on the ground,",
    "The emptiness of ages in his face,",
    "And on his back the burden of the world.",
    "Who made him dead to rapture and despair,",
    "A thing that grieves not and that never hopes,",
    "Stolid and stunned, a brother to the ox?",
    "Who loosened and let down this brutal jaw?",
    "Whose was the hand that slanted back this brow?",
    "Whose breath blew out the light within this brain?",
    "",
    "Is this the Thing the Lord God made and gave",
    "To have dominion over sea and land;",
    "To trace the stars and search the heavens for power;",
    "To feel the passion of Eternity?",
    "Is this the dream He dreamed who shaped the suns",
    "And pillared the blue firmament with light?",
    "Down all the stretch of Hell to its last gulf",
    "There is no shape more terrible than this—",
    "More tongued with censure of the world's blind greed—",
    "More filled with signs and portents for the soul.",
  ]
));

children.push(T.heading2("Partner Notes — Before You Read"));
children.push(...T.bulletList([
  "Define 'hoe' before reading: 'A hoe is a tool for farming — digging and turning soil. This man spends all day bent over, working the earth.'",
  "For V3: read one stanza at a time. Pause completely between stanzas. Do not read the entire poem without pausing.",
  "Markham asks a series of rhetorical questions in stanza 1: 'Who made him...?' These questions are the central figurative move — the poet is accusing someone, not looking for an answer. In MEAN, students should identify who Markham is accusing.",
  "The imagery is physical — a bent body, empty face, heavy back. Students can respond to the FEEL step with physical feeling words (tired, heavy, bent) without knowing any literary terms.",
]));

children.push(T.spacer());
children.push(T.heading2("NFMA Activities — The Man with the Hoe"));

children.push(...versionBlock(
  "NOTICE — Identify the Figurative Language",
  "Identify one example of imagery in this poem. Describe what the image shows and copy the line.",
  "Find one image that shows how the man's body looks or feels. Complete: 'The poet creates an image when they write: _______. I can see/feel _______.'",
  "Partner reads stanza 1 aloud. Ask: 'Which line shows us how this man's body looks?' Student indicates the line. 'What does it make you picture?' 5-second wait. [Symbol options: tired person · heavy back · empty face]. "
));

children.push(...versionBlock(
  "FEEL — What Feeling Does This Create?",
  "What feeling does the physical imagery of the man's body create? What tone does Markham establish in stanza 1?",
  "Circle the feeling the imagery creates: [tired · angry · sad · heavy]. Complete: 'The imagery of _______ makes me feel _______ because _______.'",
  "How does reading about this man make you feel? [Symbol choice board: tired · sad · angry · heavy]. Partner: 'Is Markham angry or sad about this man?' 5-second wait. Frame: 'It feels _______ because _______.' "
));

children.push(...versionBlock(
  "MEAN — What Is the Poet Really Saying?",
  "Markham asks 'Who made him...?' several times. What is he really saying with these questions? Who or what is he accusing?",
  "What do Markham's questions really mean? Complete: 'Markham uses imagery and questions to show that _______. He is accusing _______.'",
  "What is Markham really saying? Choose one:\n  A. He is asking God a question about farming.\n  B. He is accusing society for what hard labor has done to this man.\n  C. He thinks the man made bad choices.\nFrame: 'I chose _______ because _______.' 5-second wait."
));

children.push(...versionBlock(
  "ASK — Question + Evidence",
  "What question does this poem raise about labor, dignity, or social responsibility? Find one line that supports your thinking.",
  "Write: 'I wonder _______.' Find one line that connects to your question. Write it.",
  "Ask: 'I wonder _______.' Point to one line that connects. Partner scribes."
));

// ═══════════════════════════════════════════════════════════════════════
// POEM 4 — THE WORDS I CARRY (CBD ORIGINAL)
// ═══════════════════════════════════════════════════════════════════════

children.push(vh1("Poem 4 — The Words I Carry"));

children.push(...poemBlock(
  "The Words I Carry",
  "Communicate by Design",
  "2026",
  [
    "My voice is a river",
    "that runs in different ways—",
    "sometimes a pointing finger,",
    "sometimes a symbol on a page.",
    "",
    "The words I carry",
    "do not always make a sound.",
    "But I hold them like stones in my pocket,",
    "smooth and real and round.",
    "",
    "Do not listen with your ears alone.",
    "Watch my hands reach for the word.",
    "That is how I speak.",
    "That is how I am heard.",
  ]
));

children.push(T.heading2("Partner Notes — Before You Read"));
children.push(...T.bulletList([
  "This poem is about AAC communication — the speaker communicates using different methods (pointing, symbols, gestures). Read this poem without editorializing. Let students respond to it on its own terms.",
  "The speaker is matter-of-fact, not asking for understanding. The tone is certain, not sad. If students identify 'sad,' ask: 'Is the speaker asking for anything? Or are they telling you something?'",
  "The last stanza ('Do not listen with your ears alone') addresses a listener. In ASK, this is a strong discussion point: 'Who is the speaker talking to?'",
  "This poem works at V3 reading level — short lines, no Tier 3 vocabulary, all lines partner-readable. It is suitable as the anchor poem for V3 students across all four poems.",
]));

children.push(callout(
  "Note: 'The Words I Carry' is an original CbD poem — © Communicate by Design, all rights reserved. " +
  "It may not be reproduced outside of CbD products."
));

children.push(T.spacer());
children.push(T.heading2("NFMA Activities — The Words I Carry"));

children.push(...versionBlock(
  "NOTICE — Identify the Figurative Language",
  "Identify two examples of figurative language in this poem. Name the type of each. (Consider: 'My voice is a river' and 'I hold them like stones.')",
  "Find one example of figurative language. Complete: 'The poet uses _______ when they write: _______.' [Choice: metaphor / simile / imagery]",
  "Partner reads each stanza. After stanza 1: 'Which line compares the speaker's voice to something else?' Student indicates. After stanza 2: 'Which line compares words to something you can hold?' 5-second wait each time. [Select: metaphor / comparison]."
));

children.push(...versionBlock(
  "FEEL — What Feeling Does This Create?",
  "What feeling does 'smooth and real and round' create? How does the poem's tone shift between stanza 2 and stanza 3?",
  "Circle the feeling stanza 2 creates: [real · safe · calm · proud]. Complete: 'The image of stones makes communication feel _______ because _______.'",
  "How does stanza 2 make you feel? [Symbol choice board: real · calm · proud · safe]. Partner: 'Do the stones feel heavy or real?' 5-second wait. Frame: 'It feels _______ because _______.' "
));

children.push(...versionBlock(
  "MEAN — What Is the Poet Really Saying?",
  "What is the speaker really saying about communication? What do the river and stone metaphors reveal about how the speaker experiences their own voice?",
  "What does 'My voice is a river' really mean? Complete: 'The poet uses metaphor to show that _______. The stones mean _______.'",
  "What is the poet really saying? Choose one:\n  A. The speaker's voice doesn't work right.\n  B. The speaker communicates in many different ways — all of them real.\n  C. The speaker wishes they could talk out loud.\nFrame: 'I chose _______ because _______.' 5-second wait."
));

children.push(...versionBlock(
  "ASK — Question + Evidence",
  "Who is the speaker talking to in the last stanza? What question does 'Do not listen with your ears alone' raise about how we receive communication?",
  "Write: 'I wonder _______.' Find one line that connects. Write it.",
  "Ask: 'I wonder _______.' Point to one line that connects. Partner scribes."
));

// ═══════════════════════════════════════════════════════════════════════
// SECTION 9 — SYNTHESIS ACTIVITY
// ═══════════════════════════════════════════════════════════════════════

children.push(vh1("Synthesis — Across the Poems"));
children.push(T.teacherRefLabel());

children.push(T.p(
  "After completing NFMA activities for all four poems, students connect figurative language across texts. " +
  "This activity addresses RL.9-10.9 for grades 9–10 (compare approaches across texts) and serves as " +
  "an extension for grades 6–8. All three access levels are included."
));

children.push(T.heading2("Synthesis Activity — V1"));
children.push(T.p(
  "All four poems use figurative language to express something about identity, voice, or the relationship " +
  "between appearance and reality. Choose two poems and analyze how each poet uses figurative language " +
  "differently to express a similar idea. Use specific examples from each poem."
));

children.push(T.heading2("Synthesis Activity — V2"));
children.push(T.p(
  "Choose two poems from this unit. Complete the frame:"
));
children.push(T.blockquote(
  "Both [Poem 1] and [Poem 2] use figurative language to show _______. " +
  "In [Poem 1], the poet uses _______ when they write: _______. " +
  "In [Poem 2], the poet uses _______ when they write: _______. " +
  "The difference is that _______."
));

children.push(T.heading2("Synthesis Activity — V3"));
children.push(T.p(
  "Choose two poems. Show your partner which poems you chose. Complete with your partner's help:"
));
children.push(T.makeTable(
  ["", "Poem 1: _______", "Poem 2: _______"],
  [
    ["One example of figurative language", "", ""],
    ["What feeling it creates (FEEL)",    "", ""],
    ["What it really means (MEAN)",       "", ""],
  ],
  col3(0.25, 0.375, 0.375),
  { compact: true }
));
children.push(T.p(
  "Then tell your partner: 'Both poems use figurative language to show _______.' " +
  "Point to the words in each poem that support your answer."
));

// ═══════════════════════════════════════════════════════════════════════
// SECTION 10 — IEP GOAL STEMS
// ═══════════════════════════════════════════════════════════════════════

children.push(vh1("IEP Goal Stems"));
children.push(T.teacherRefLabel());

children.push(T.p(
  "These are model goal stems — starting points for the IEP team, not compliance guarantees. " +
  "Adjust the condition, criterion, and measurement tool to match the individual student. " +
  "All goals are written as accommodations (same standard, different access) — not modifications."
));

children.push(T.heading2("Academic Goal — RL.6.4 Figurative Language"));
children.push(T.blockquote(
  "Given a short poem with at least one example of figurative language (metaphor or imagery), " +
  "[student name] will identify the figurative language and explain its effect on meaning or tone " +
  "using a sentence frame and their AAC system, achieving 80% accuracy across 3 consecutive trials " +
  "as measured by the CbD unit rubric, by [IEP date]."
));
children.push(T.p("Observable verbs: identify, explain. Measurement tool: CbD Unit Rubric (3-level). Mastery threshold: Meets on Criteria 3 + 4 across 3 consecutive sessions."));

children.push(T.spacer());
children.push(T.heading2("AAC Communication Goal"));
children.push(T.blockquote(
  "Given a partner-read poem and a NFMA response prompt, [student name] will produce a 2–3 symbol " +
  "utterance that includes at least one fringe literary vocabulary word (e.g., metaphor, tone, imagery) " +
  "and one core connector word (e.g., because, same, feel), with no more than one verbal prompt, across " +
  "2 communication partners, achieving 80% accuracy across 3 consecutive sessions as measured by the " +
  "CbD Session Tracker, by [IEP date]."
));
children.push(T.p("Observable verb: produce. Measurement tool: CbD Session Tracker (para-administered). Generalization: 2+ partners minimum."));

children.push(T.spacer());
children.push(callout(
  "SLP note: Pre-programming due 2 weeks before Day 1. Top 5 CAP priority: " +
  "figurative language · metaphor · imagery · tone · speaker. " +
  "Confirm semi-core words on system: hide · pain · proud · alone · free."
));

// ═══════════════════════════════════════════════════════════════════════
// SECTION 11 — RUBRIC
// ═══════════════════════════════════════════════════════════════════════

children.push(vh1("Rubric — Figurative Language Analysis"));
children.push(T.teacherRefLabel());

children.push(T.p(
  "3-level rubric · 4 criteria · Identical across V1/V2/V3 · All response modes valid and equivalent. " +
  "Score per poem. IEP mastery = Meets on Criteria 3 + 4 across 3 consecutive sessions."
));

children.push(callout(
  "Response Mode Note: 'Indicates' means any of the following: selects on AAC device, points, uses eye gaze, " +
  "writes, or speaks. Do not require one mode over another. All modes count equally for scoring."
));
children.push(T.spacer());

children.push(T.tableCaption("Table: Rubric — RL.6.4 Figurative Language in Poetry · 3 levels × 4 criteria"));
children.push(T.makeTable(
  ["Criterion", "Does Not Yet Meet", "Approaching", "Meets"],
  [
    ["1. Identify Figurative Language (NOTICE)",
     "Does not respond, or indicates a line that does not contain figurative language — even with a 2-option choice field.",
     "Indicates a line with figurative language when the choice field is reduced to 2 options, OR after one direct cue. Responds inconsistently (1–2 of 3 trials).",
     "Independently indicates a line with figurative language without a reduced choice field or direct cue. Responds consistently (3 of 3 trials, or across 2 poems in one session)."],
    ["2. Name the Type (NOTICE)",
     "Does not respond, or names/selects a type that does not match the identified example.",
     "Names/selects the correct type from a 2-choice field, OR after one direct cue. Correct on 2 of 3 trials.",
     "Independently names/selects the correct type from 3+ options without a reduced choice field or direct cue. Correct on 3 of 3 trials."],
    ["3. Interpret the Meaning (MEAN) — IEP mastery criterion",
     "Does not produce an interpretation, OR restates the literal meaning without identifying the figurative meaning — even with a sentence frame.",
     "Identifies the figurative meaning (what the language means beyond the literal) but does not connect it to the speaker's message or theme. Response is partial.",
     "Identifies both (a) what the figurative language means beyond the literal AND (b) what it reveals about the speaker's message, using any valid response mode. No cue beyond wait."],
    ["4. Explain Effect on Tone/Mood with Evidence (FEEL + MEAN) — IEP mastery criterion",
     "Does not name a mood/tone, OR names a mood with no logical connection to the figurative language cited.",
     "Names/selects a logically connected mood/tone but does not provide evidence from the poem (no word or phrase cited).",
     "Names the mood/tone AND provides at least one word or phrase from the poem as evidence. Indicating (pointing, gaze) counts as citing. No cue beyond wait."],
  ],
  col4(0.24, 0.25, 0.25, 0.26),
  { compact: true }
));

children.push(T.spacer());
children.push(T.heading2("Quick-Score Version — Para / Session Tracker"));
children.push(T.makeTable(
  ["Criterion", "DNM", "A", "M"],
  [
    ["1. Identifies figurative language in the poem",          "☐", "☐", "☐"],
    ["2. Names the type of figurative language",               "☐", "☐", "☐"],
    ["3. Interprets what the figurative language means",       "☐", "☐", "☐"],
    ["4. Explains effect on tone/mood with poem evidence",     "☐", "☐", "☐"],
  ],
  col4(0.50, 0.167, 0.167, 0.166),
  { compact: true }
));
children.push(T.p("Poem: ________________________  Date: __________  Response mode: ____________________"));
children.push(T.p("Session notes: _________________________________________________"));

// ═══════════════════════════════════════════════════════════════════════
// SECTION 12 — END MATTER
// ═══════════════════════════════════════════════════════════════════════

children.push(vh1("Accessibility, Creator, and Terms"));
children.push(...T.accessibilityStatement());
children.push(T.spacer());
children.push(...T.aboutTheCreator());
children.push(T.spacer());
children.push(...T.termsOfUse());

// ═══════════════════════════════════════════════════════════════════════
// ASSEMBLE AND WRITE
// ═══════════════════════════════════════════════════════════════════════

const OUTPUT = path.join(__dirname, "What_the_Voice_Carries_COMPLETE.docx");

T.assembleAndWrite(
  "What the Voice Carries",
  children,
  OUTPUT,
  {
    title:       "What the Voice Carries — Figurative Language in Poetry | Communicate by Design",
    description: "Poetry Reading Unit 1 for grades 6–10. NFMA strategy (NOTICE/FEEL/MEAN/ASK). " +
                 "Four poems: Dunbar, Dickinson, Markham, and CbD original. " +
                 "Access levels V1/V2/V3. WCAG 2.2 AA. SDI-designed for AAC users.",
    creator:     "Communicate by Design — Jill McCardel",
  }
);

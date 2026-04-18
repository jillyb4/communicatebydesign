#!/usr/bin/env node

/**
 * The Giver: Theme Analysis — Fiction Anchor Text Unit Builder
 * Communicate by Design
 *
 * Novel: The Giver by Lois Lowry
 * Skill: Theme (RL.7.2) supported by textual evidence (RL.7.1)
 * Scope: Whole book — grades 6–8
 *
 * Unit question: "According to The Giver, what makes us fully human —
 *                 and what happens when those things are taken away?"
 *
 * Text interaction tool: Theme Evidence Chart (not annotation codes)
 * 5-Part SDI sequence across the full novel
 *
 * Output: The_Giver_Theme_Analysis_Teaching_Materials.docx
 *
 * Build rule: whole-book scope is STANDARD for all CbD fiction units.
 * Build rule: student worksheet/response pages → cbd_worksheet_templates.py (not this script).
 */

const path = require("path");
const T = require(path.join(__dirname, "..", "..", "..", "_Operations", "Build", "cbd_docx_template"));

const CW = T.CONTENT_WIDTH; // 10080 DXA

const h2k = T.heading2;

// ─────────────────────────────────────────────────────────────────────────
// COLUMN WIDTH HELPERS
// ─────────────────────────────────────────────────────────────────────────
const col2 = (a, b) => [Math.round(CW * a), Math.round(CW * b)];
const col3 = (a, b, c) => [Math.round(CW * a), Math.round(CW * b), Math.round(CW * c)];
const col4 = (a, b, c, d) => [Math.round(CW * a), Math.round(CW * b), Math.round(CW * c), Math.round(CW * d)];

// ─────────────────────────────────────────────────────────────────────────
// UNIT CONSTANTS
// ─────────────────────────────────────────────────────────────────────────

const UNIT_TITLE    = "The Giver";
const UNIT_SUBTITLE = "Theme Analysis";
const NOVEL_AUTHOR  = "Lois Lowry";
const SKILL_NAME    = "Theme Analysis";
const GRADE_RANGE   = "6–8";
const RL_STANDARDS  = "RL.6.2 · RL.7.2 · RL.8.2 · RL.7.1";
const PRODUCT_LINE  = "Fiction Anchor Text Unit";

// ─────────────────────────────────────────────────────────────────────────
// AAC ACCESS NOTE CONSTANTS
// ─────────────────────────────────────────────────────────────────────────
const AAC_CORE         = "Core — part of most AAC ecosystems";
const AAC_CORE_CONFIRM = "Core — part of most AAC ecosystems";
const AAC_CORE_VERIFY  = "Core — part of most AAC ecosystems";
const AAC_FRINGE_PREP  = "Fringe — SDI target; include in communication packet";
const AAC_FRINGE_SYM   = "Fringe — SDI target; include in communication packet";

// ─────────────────────────────────────────────────────────────────────────
// BUILD CHILDREN ARRAY
// ─────────────────────────────────────────────────────────────────────────

const children = [];

// ═══════════════════════════════════════════════════════════════════════
// TITLE PAGE
// ═══════════════════════════════════════════════════════════════════════

children.push(...T.titlePage({
  unitTitle:    UNIT_TITLE,
  unitSubtitle: UNIT_SUBTITLE,
  skillNumber:  "",
  skillName:    SKILL_NAME,
  gradeRange:   GRADE_RANGE,
  versions:     "Fiction Anchor Text",
  parts:        "5-Part SDI Sequence · Whole Book",
}));

// ═══════════════════════════════════════════════════════════════════════
// TABLE OF CONTENTS
// ═══════════════════════════════════════════════════════════════════════

children.push(...T.tocPage());

// ═══════════════════════════════════════════════════════════════════════
// SECTION 1 — ABOUT THIS UNIT
// ═══════════════════════════════════════════════════════════════════════

children.push(T.heading1("About This Unit"));
children.push(T.teacherRefLabel());

children.push(T.makeTable(
  ["Element", "Detail"],
  [
    ["Novel",              `${UNIT_TITLE} by ${NOVEL_AUTHOR}`],
    ["Product Type",       PRODUCT_LINE],
    ["Targeted Skill",     SKILL_NAME],
    ["Standards",          RL_STANDARDS],
    ["Grade Range",        `${GRADE_RANGE} (differentiated by scaffold, not by text)`],
    ["Scope",              "Whole book — 5-part SDI sequence across the full novel"],
    ["Unit Question",      "According to The Giver, what makes us fully human — and what happens when those things are taken away?"],
    ["Required Materials", "Copy of The Giver (not included) · AAC system (any access method) · Communication boards (included)"],
  ],
  col2(0.28, 0.72)
));

children.push(T.spacer());
children.push(h2k("What This Unit Is"));
children.push(T.p(
  "This is a Specially Designed Instruction (SDI) companion unit for the novel The Giver by Lois Lowry. " +
  "The novel is not included — your class or student already has it. What this unit provides is the instructional and communication access layer: " +
  "the teacher guide, AAC-designed activities, vocabulary supports, and response structures that make theme analysis accessible to students who use alternative and augmentative communication."
));
children.push(T.p(
  "This is not a Lexile differentiation product. The text stays the same. " +
  "The scaffold varies. The expectation does not. " +
  "Every student engages with the same novel, the same skill, and the same standard. " +
  "What differs is how they access vocabulary, how they respond, and how the partner supports participation."
));

children.push(h2k("What This Unit Is Not"));
children.push(...T.bulletList([
  "A simplified or rewritten version of the novel",
  "A replacement for general education instruction",
  "An activity pack that only works with high-tech AAC devices",
  "A unit about dystopia as a genre (The Giver does that — this unit is about the literacy skill of theme)",
]));

children.push(h2k("What's Included"));
children.push(...T.bulletList([
  "Teacher SDI guide with 5-part lesson sequence",
  "Before-reading vocabulary preview with core and fringe word list",
  "Part 1: The Rules of Sameness — what the community takes away and why",
  "Part 2: The First Memories — what Jonas receives and what it reveals about what was lost",
  "Part 3: What Jonas Feels and Realizes — internal change and the emotional cost of truth",
  "Part 4: The Ending — what Lowry leaves unresolved, and why that is the point",
  "Part 5: Whole-Book Synthesis — theme response using the Theme Evidence Chart",
  "Theme Evidence Chart — the primary text interaction tool for this unit",
  "Communication Access quick-reference card (partner pull-out)",
  "Core and fringe vocabulary table with AAC access notes",
  "IEP goal stems for RL.6.2 through RL.8.2",
  "Data collection guidance",
]));

// ═══════════════════════════════════════════════════════════════════════
// SECTION 2 — RESEARCH BASE
// ═══════════════════════════════════════════════════════════════════════

children.push(T.heading1("Research Base"));
children.push(T.teacherRefLabel());

children.push(h2k("Why Theme Is the Right Skill for The Giver"));
children.push(T.p(
  "Theme is one of the most abstract skills in literary analysis — and one of the most meaningful. " +
  "Unlike plot (what happened) or character (who did it), theme asks students to step back from the events of the story and ask: " +
  "What does this mean? What is the author trying to show us about being human? " +
  "The Giver is built for exactly this kind of reading. Lois Lowry structures every chapter around questions the novel refuses to resolve easily — " +
  "questions about memory, choice, loss, and what it means to live a full life."
));
children.push(T.p(
  "For students who use AAC, theme analysis requires a different kind of vocabulary preparation than character analysis or plot recall. " +
  "The hardest words in theme work are not proper nouns or domain-specific content words — they are abstract relational concepts: " +
  "memory, freedom, control, sameness, human, real, feel, choose. " +
  "These words are mostly core vocabulary, already on most AAC systems. This is an advantage, not a limitation: " +
  "theme analysis for AAC users can be built almost entirely on words the student already has."
));

children.push(h2k("Story Grammar and Theme as SDI Evidence"));
children.push(T.p(
  "Story grammar instruction (Spencer & Petersen, 2020) is the primary evidence-based framework for narrative SDI. " +
  "Theme is the most advanced story grammar element — it requires students to integrate character, conflict, and resolution " +
  "into a single statement about meaning. Research shows statistically significant improvements in comprehension " +
  "and story-structure knowledge for students with and without disabilities when explicit narrative structure instruction is provided " +
  "(ERIC EJ871908). " +
  "Teaching theme through story grammar scaffolding is literacy instruction, not a support activity."
));
children.push(T.callout(
  "Theme analysis is recognized SDI practice at RL.6.2–RL.8.2. It adapts the methodology and delivery — not the standard. " +
  "Every student is working toward the same RL standard. The scaffold is how we get them there."
));

children.push(h2k("UDL 3.0 and HLP Alignment"));
children.push(T.p(
  "This unit is designed to CAST Universal Design for Learning Guidelines 3.0 (CAST, 2024). " +
  "Every activity implements multiple means of action and expression (UDL Guideline 4.1: vary and honor all response methods; Guideline 4.2: optimize access to AT/AAC tools) " +
  "and multiple means of representation (Guideline 2.1: clarify vocabulary and language structures; Guideline 2.5: illustrate through multiple media). " +
  "The communication access framework in this unit directly implements Guideline 5.4 — addressing biases related to modes of expression. " +
  "Oral response is not the default or the expectation. Every response opportunity has a non-speech pathway. " +
  "Partner guidance embedded at point of use implements Guideline 6.5: challenging the exclusionary practice of expecting AAC users to participate without trained communication partner support."
));
children.push(T.p(
  "CEC High-Leverage Practice alignment: " +
  "HLP 12 (Systematic and explicit instruction — theme vocabulary and the Theme Evidence Chart taught explicitly before application); " +
  "HLP 13 (Adapt curriculum tasks and materials — Theme Evidence Chart, communication boards, sentence frames, symbol sorts); " +
  "HLP 14 (Teach cognitive and metacognitive strategies — Theme Evidence Chart as cumulative pre-writing scaffold across the whole novel); " +
  "HLP 16 (Use explicit instruction / shared reading — Mode 2 during novel reading is the evidence-based delivery condition for complex communicators)."
));

children.push(h2k("Abstract Language and AAC"));
children.push(T.p(
  "Narrative macrostructure — the quality and organization of how a student processes a story — " +
  "accounts for significant variance in reading comprehension beyond what decoding and basic language measures explain " +
  "(Spencer & Petersen, 2020). " +
  "Theme is the capstone of narrative macrostructure. ASHA identifies narrative intervention as accessible and evidence-supported " +
  "for complex communicators (Perspectives, 2022). " +
  "Aided language stimulation during shared reading has moderate-to-strong evidence — and theme vocabulary " +
  "(because, feel, believe, change, real, human) is almost entirely core vocabulary accessible on most systems."
));

children.push(h2k("The Theme Evidence Chart as Scaffold"));
children.push(T.p(
  "This unit uses a Theme Evidence Chart as its primary text interaction tool. " +
  "Unlike annotation codes (which work well for argument-based texts), theme in a novel like The Giver develops slowly and cumulatively — " +
  "through many small moments that build meaning across the whole book. " +
  "The Theme Evidence Chart gives students a way to collect those moments across five parts of the unit and then synthesize them into a theme statement. " +
  "It is pre-writing scaffolding built into the reading process itself. " +
  "By the time a student reaches Part 5 (Synthesis), the chart is already their outline."
));

children.push(h2k("Visual Scene Displays and Communication Boards"));
children.push(T.p(
  "Research shows that Visual Scene Displays (VSDs) embedded in narrative contexts are more effective than decontextualized symbol cards for fiction comprehension — " +
  "they increase participation, enable faster vocabulary acquisition, and reduce cognitive load by situating vocabulary within the actual scene where meaning was made (Drager et al., 2003; PMC8375490). " +
  "This unit uses communication boards and symbol cards for vocabulary access. " +
  "VSDs for key Giver scenes are planned for a future version of this unit. " +
  "Where possible, pair symbol cards with visual references (scene images, character images) to provide contextual embedding."
));

children.push(h2k("Why The Giver for This Unit"));
children.push(T.p(
  "The Giver is taught in thousands of classrooms because its structure makes abstract ideas concrete. " +
  "Lois Lowry shows us what a world without memory, color, music, and choice looks like — and then shows us one person discovering what was lost. " +
  "That structure — absence made visible — is exactly what makes theme analysis accessible to students who think concretely. " +
  "Jonas does not lecture about freedom. He feels it in a memory of a sled ride. He sees it in a flash of red on a girl's hair. " +
  "He loses it when he learns what 'release' means. Each moment is a window into what it means to be fully human."
));
children.push(T.p(
  "For students who use AAC, The Giver is a strong choice for an additional reason: " +
  "the novel's central question — what happens when you take away a person's ability to choose and feel and remember — " +
  "is not abstract to someone whose communication has ever been dismissed, ignored, or controlled by a system that claimed to know better. " +
  "The theme has direct relevance. This unit does not name that connection explicitly, but the teacher should know it is there."
));

// ═══════════════════════════════════════════════════════════════════════
// SECTION 3 — NOVEL OVERVIEW
// ═══════════════════════════════════════════════════════════════════════

children.push(T.heading1("Novel Overview: The Giver"));
children.push(T.teacherRefLabel());

children.push(T.makeTable(
  ["Element", "Detail"],
  [
    ["Author",             "Lois Lowry"],
    ["Published",          "1993"],
    ["Genre",              "Dystopian Fiction / Middle-Grade / Literary Fiction"],
    ["Typical Grade Use",  "Grades 6–8"],
    ["Lexile",             "760L"],
    ["Narrator Structure", "Third-person limited — Jonas's perspective throughout"],
    ["Central Theme",      "What makes us fully human — memory, choice, emotion, color, pain, and love"],
    ["Awards",             "1994 Newbery Medal"],
  ],
  col2(0.28, 0.72)
));

children.push(T.spacer());
children.push(h2k("Summary (for teacher reference)"));
children.push(T.p(
  "Jonas lives in a highly ordered community where Sameness has eliminated conflict, pain, color, and choice. " +
  "At the Ceremony of Twelve, Jonas is selected as the next Receiver of Memory — the only member of the community " +
  "who will hold the memories of all that existed before Sameness. " +
  "His training is conducted by the previous Receiver, who Jonas calls the Giver. " +
  "As Jonas receives memories of snow, sunshine, color, music, and eventually war and pain, he begins to understand what his community has given up. " +
  "The novel ends ambiguously: Jonas flees the community with a baby scheduled for release, and we are left uncertain whether what he sees from the hilltop is real or a last memory."
));

children.push(h2k("Key Characters"));
children.push(T.makeTable(
  ["Character", "Description (not name-based)", "Role"],
  [
    ["Jonas",    "The twelve-year-old boy selected to receive all memories. Begins to feel things — color, music, pain — that no one else in the community can.", "Narrator / Protagonist"],
    ["The Giver","The old man who holds all the memories. Has carried the weight of everything the community refused to feel. Calls himself the Giver to Jonas.", "Supporting / Mentor"],
    ["Gabriel",  "A baby in Jonas's household — small, reaching, in danger of release. Jonas names him and eventually tries to save him.", "Supporting / Symbolic"],
    ["Fiona",    "Jonas's friend. Kind, caring, precise. Does not yet know what she does not know.", "Supporting"],
    ["Lily",     "Jonas's younger sister. Curious, outspoken, asks the questions children ask before they learn not to.", "Supporting"],
    ["The Chief Elder", "The leader who announces Assignments at the Ceremony of Twelve. Represents institutional order.", "Authority figure"],
  ],
  col3(0.20, 0.55, 0.25)
));
children.push(T.tableCaption("Character names are fringe words. Always pair with a description-first reference when introducing in activities."));

children.push(h2k("Novel Structure: 5-Part Mapping"));
children.push(T.makeTable(
  ["Unit Part", "Novel Section", "Chapters", "Theme Focus"],
  [
    ["Before Reading", "Pre-reading vocabulary and community overview", "—",       "Build vocabulary access: memory, rule, sameness, choose, feel"],
    ["Part 1",         "The Rules of Sameness",                       "1–8",      "What the community controls and why — the cost of Sameness"],
    ["Part 2",         "The First Memories",                          "9–16",     "What Jonas receives — color, snow, family, war — and what they reveal"],
    ["Part 3",         "What Jonas Feels and Realizes",               "17–22",    "The emotional cost of truth — Jonas begins to understand release"],
    ["Part 4",         "The Ending — and What Lowry Leaves Open",     "23–Epilogue", "The ambiguous ending as a statement about hope and the unknown"],
    ["Part 5",         "Whole-Book Synthesis",                        "Full book","Theme statement: what The Giver teaches about being fully human"],
  ],
  col4(0.15, 0.28, 0.12, 0.45)
));

// ═══════════════════════════════════════════════════════════════════════
// SECTION 4 — TARGETED STANDARD
// ═══════════════════════════════════════════════════════════════════════

children.push(T.heading1("Targeted Standard: Theme Analysis"));
children.push(T.teacherRefLabel());

children.push(h2k("Standard Statements"));
children.push(T.makeTable(
  ["Grade", "Standard", "Statement"],
  [
    ["6", "RL.6.2", "Determine a theme or central idea of a text and how it is conveyed through particular details; provide a summary of the text distinct from personal opinions or judgments."],
    ["7", "RL.7.2", "Determine a theme or central idea of a text and analyze its development over the course of the text; provide an objective summary of the text."],
    ["8", "RL.8.2", "Determine a theme or central idea of a text and analyze its development over the course of the text, including its relationship to the characters, setting, and plot."],
    ["Support", "RL.7.1", "Cite several pieces of textual evidence to support analysis of what the text says explicitly as well as inferences drawn from the text."],
  ],
  col3(0.07, 0.13, 0.80)
));
children.push(T.tableCaption("Select the standard anchor that matches the student's IEP and grade placement. All activities address the same theme skill at varying response complexity. RL.7.1 is the evidence-citing standard that supports theme analysis at every grade."));

children.push(T.spacer());
children.push(h2k("Learning Target"));
children.push(T.p(
  "I can determine the theme of The Giver — what the novel teaches about being fully human — and explain how that theme develops through what Jonas experiences, feels, and learns across the whole book."
));
children.push(T.tableCaption("This learning target applies to every student in the room. The access layer varies. The expectation does not."));

children.push(T.makeTable(
  ["Standard", "Grade-Level Anchor"],
  [
    ["RL.6.2", "I can identify the theme of The Giver and explain how specific details from the story support it."],
    ["RL.7.2", "I can determine the theme of The Giver and explain how it develops across the whole novel using evidence."],
    ["RL.8.2", "I can analyze how the theme of The Giver develops over the course of the novel and explain how it connects to Jonas, the community, and the ending."],
  ],
  col2(0.18, 0.82)
));

children.push(T.spacer());
children.push(h2k("What Theme Analysis Requires in The Giver"));
children.push(...T.bulletList([
  "Identifying what the novel is really about — beyond the plot, at the level of meaning",
  "Recognizing moments where Lowry shows (not tells) what human life without memory and choice looks like",
  "Tracing how the theme develops across parts of the novel, not just in one scene",
  "Using evidence from the text to explain how specific moments support the theme statement",
  "Understanding that theme is a statement — not a single word ('family') but an idea ('family is what makes you human')",
  "Writing or constructing a theme statement using textual evidence as support",
]));

children.push(h2k("The Difference Between Topic and Theme"));
children.push(T.makeTable(
  ["Topic (one word — not theme)", "Theme (a statement — what the book teaches)"],
  [
    ["Memory",  "Memory is what makes us human — without it, we cannot feel, choose, or connect to each other."],
    ["Freedom", "Freedom cannot exist without the possibility of pain. Taking away pain means taking away what makes life real."],
    ["Control", "When a society controls everything to eliminate suffering, it also eliminates the things that make life worth living."],
    ["Choice",  "The ability to choose — even to choose wrong — is essential to what it means to be a full person."],
  ],
  col2(0.3, 0.7)
));
children.push(T.tableCaption("Use this table to teach the difference between topic and theme before Part 1. Students should be able to move from a single word to a statement by the end of the unit."));

// ═══════════════════════════════════════════════════════════════════════
// SECTION 5 — COMMUNICATION ACCESS
// ═══════════════════════════════════════════════════════════════════════

children.push(T.heading1("Communication Access"));
children.push(T.teacherRefLabel());

children.push(h2k("Partner Modes — When to Use Each"));
children.push(T.makeTable(
  ["Mode", "When", "What the Partner Does", "What the Partner Does NOT Do"],
  [
    ["Mode 1 — Instructional",  "Focused activities (Theme Evidence Chart, Parts 1–5)", "Uses prompt hierarchy; collects data; scaffolds toward independence", "Interrupt the student; complete responses; skip wait time"],
    ["Mode 2 — Partnership",    "During shared novel reading", "Follows student lead; notes spontaneous communication; models AAC use naturally", "Run prompt hierarchy; make demands; correct responses"],
    ["Mode 3 — Participation",  "Performance tasks; group discussion; read-aloud", "Enables access only (holds book, operates device, manages boards)", "Interpret; speak for student; add communication content"],
  ],
  col4(0.18, 0.18, 0.34, 0.30)
));
children.push(T.tableCaption("Mode 2 during reading is non-negotiable. Running Mode 1 (instructional) during novel reading is the most common partner error in fiction units."));

children.push(T.spacer());
children.push(h2k("5-Level Prompt Hierarchy (Mode 1 Only)"));
children.push(T.makeTable(
  ["Level", "Prompt Type", "What It Looks Like"],
  [
    ["1", "Wait",         "Pause 10–15 seconds. Theme vocabulary is abstract — students need processing time."],
    ["2", "Indirect Cue", "Gesture toward the AAC system without saying anything. Non-directive."],
    ["3", "Direct Cue",   "Point to the specific symbol, location, or area on the board."],
    ["4", "Verbal Model", "Say the response AND demonstrate it on the student's system."],
    ["5", "Reassess",     "Non-response is data. Ask: Is the vocabulary available? Is the activity set up correctly? Is this the right mode?"],
  ],
  col3(0.07, 0.18, 0.75)
));

children.push(T.spacer());
children.push(h2k("Core and Fringe Vocabulary — The Giver: Theme Analysis"));
children.push(T.p(
  "Fringe vocabulary in fiction is descriptive — words that help readers picture and understand what characters experience: " +
  "appearance, action, emotion, and setting. " +
  "This is different from nonfiction fringe vocabulary, which is domain-specific content terms. " +
  "In theme analysis, the most important fringe words are abstract concept words — the language of the novel's central ideas. " +
  "Character names are always fringe words — specific proper nouns rarely pre-programmed on AAC systems. " +
  "Coordinate with the student's AAC team to confirm fringe vocabulary is available before the unit begins."
));

children.push(T.makeTable(
  ["Word", "★ Core / Fringe", "Why It Matters in The Giver", "AAC Access Note"],
  [
    ["feel",      "★ Core", "Central to everything Jonas discovers — he begins to feel things no one else can", AAC_CORE_CONFIRM],
    ["think",     "★ Core", "Jonas's internal process as he questions the community", AAC_CORE],
    ["know",      "★ Core", "The gap between what the community knows and what Jonas learns", AAC_CORE],
    ["change",    "★ Core", "Jonas changes across the novel — and the community refuses to", AAC_CORE],
    ["believe",   "★ Core", "What characters believe vs. what is true — central tension", AAC_CORE_VERIFY],
    ["remember",  "★ Core", "The act of holding memory — Jonas and the Giver's role", AAC_CORE_VERIFY],
    ["choose",    "★ Core", "The capacity for choice — taken away by Sameness", AAC_CORE],
    ["want",      "★ Core", "What Jonas wants shifts as he receives memories", AAC_CORE],
    ["free",      "★ Core", "What Jonas begins to understand as he receives memories of open space, color, choice", AAC_CORE],
    ["because",   "★ Core", "Causal reasoning — essential for theme evidence statements", AAC_CORE],
    ["if",        "★ Core", "Conditional reasoning — 'if you could feel, you would...'", AAC_CORE],
    ["real",      "★ Core", "What is real in the community vs. what Jonas discovers", AAC_CORE_VERIFY],
    ["together",  "★ Core", "Community vs. true connection — what Jonas discovers about love", AAC_CORE],
    ["alone",     "★ Core", "Jonas carries memories alone — isolation of the Receiver", AAC_CORE],
    ["memory",    "Fringe", "The most central concept — memories Jonas receives from the Giver", AAC_FRINGE_PREP],
    ["rule",      "Fringe", "The laws that govern the community; what controls everything", AAC_FRINGE_SYM],
    ["community", "Fringe", "The structured society Jonas lives in", AAC_FRINGE_SYM],
    ["assignment","Fringe", "The job each person receives at the Ceremony of Twelve", AAC_FRINGE_SYM],
    ["release",   "Fringe", "The community's word for death — Jonas learns its true meaning", AAC_FRINGE_PREP],
    ["sameness",  "Fringe", "The community's principle — all differences eliminated", AAC_FRINGE_PREP],
    ["color",     "Fringe", "One of the first things Jonas receives — symbol of what was taken away", "Fringe — SDI target; include in communication packet"],
    ["ceremony",  "Fringe", "The Ceremony of Twelve — where Jonas receives his Assignment", AAC_FRINGE_SYM],
    ["sacrifice", "Fringe", "What the community gave up for peace — and what Jonas realizes that cost", AAC_FRINGE_SYM],
    ["human",     "Fringe", "What Jonas is becoming as he receives memories", "Fringe — SDI target; include in communication packet"],
    ["Jonas",     "Fringe", "The protagonist — proper noun; description-first before name", "Fringe — SDI target; include in communication packet"],
    ["the Giver", "Fringe", "The old man who carries memories — Jonas's teacher", "Fringe — SDI target; include in communication packet"],
  ],
  col4(0.16, 0.16, 0.42, 0.26)
));
children.push(T.tableCaption(
  "★ Core = high-frequency, cross-context words already on most AAC ecosystems. " +
  "Fringe = The Giver-specific vocabulary requiring system preparation. " +
  "Coordinate with the student's AAC team before the unit to confirm vocabulary is available."
));

children.push(T.spacer());
children.push(h2k("Top 5 Priority Vocabulary — Confirm First"));
children.push(T.callout(
  "Before any unit activity begins, confirm these 5 words are accessible on the student's system. " +
  "These carry the most weight in theme analysis for The Giver.\n\n" +
  "  1. memory — the central concept of the unit\n" +
  "  2. choose / choice — what Sameness eliminates\n" +
  "  3. feel — what Jonas begins to experience and the community cannot\n" +
  "  4. release — the word the community uses for death (critical for Part 3)\n" +
  "  5. real — what Jonas begins to question about his world"
));

// ═══════════════════════════════════════════════════════════════════════
// SECTION 6 — BEFORE READING: VOCABULARY PREVIEW
// ═══════════════════════════════════════════════════════════════════════

children.push(T.heading1("Before Reading: Vocabulary Preview"));
children.push(T.teacherRefLabel());

children.push(T.p(
  "Pre-teach vocabulary before beginning the novel. Do not wait until a word appears in a chapter. " +
  "Students who use AAC need time to build familiarity with vocabulary in low-stakes contexts " +
  "before they are asked to use it in an activity. " +
  "The abstract concept vocabulary below is the highest priority — introduce these before Chapter 1."
));

children.push(h2k("Priority Vocabulary: Abstract Concept Words"));
children.push(T.callout(
  "Pre-teach these before Chapter 1. These words carry the theme and are the most abstract. " +
  "Most are core vocabulary — the goal is to connect familiar words to new meanings."
));
children.push(T.makeTable(
  ["Word", "What It Means in The Giver", "How to Pre-Teach It"],
  [
    ["memory",    "A feeling, picture, or experience from the past that you carry inside you.", "Ask: Do you have a memory of something that felt good? Show me on your board. (This is a memory.)"],
    ["sameness",  "When everything is the same — same weather, same houses, same choices — there is no surprise and no difference.", "Show two identical objects. Then show one that is different. Which world is Sameness? Why might someone want everything the same?"],
    ["choose",    "To choose means to pick for yourself — not have someone pick for you.", "Practice: Give the student two options. 'You choose.' Connect: When you chose, you were in charge of that."],
    ["release",   "In this community, release is the word they use when they send someone away — forever. We find out what it really means.", "Introduce carefully. 'In this story, the community has a word that sounds okay but means something hard. We will learn what it really means.'"],
    ["real",      "Something that is real actually exists — it is not just an idea. Jonas starts to wonder what is real in his world.", "Ask: Is that feeling real? (Yes.) Is that memory real? (Yes.) Connect to the story: Jonas will ask those same questions."],
    ["human",     "To be fully human means to feel, to remember, to choose, to love, to hurt — to have all of it.", "Ask: What do people feel? What do people need? What would it mean to have none of that? That is the question this book asks."],
  ],
  col3(0.12, 0.44, 0.44)
));

children.push(T.spacer());
children.push(h2k("The Giver Community Overview"));
children.push(T.p(
  "Before reading, give students a brief overview of the community Jonas lives in. " +
  "The goal is to establish what is unusual about it — what has been removed — so students can track what Jonas discovers about what is missing."
));
children.push(T.makeTable(
  ["In the community...", "Why (what Sameness was supposed to solve)"],
  [
    ["Everyone is assigned their job, spouse, and children",       "To eliminate competition and conflict"],
    ["Weather is controlled — no snow, no rain, no seasons",       "To eliminate inconvenience and danger"],
    ["Color has been eliminated — everything is black and white",  "To eliminate the desire for things other people have"],
    ["Feelings are suppressed — people take pills to stop them",   "To eliminate pain and jealousy"],
    ["Language is controlled — precision is required",             "To eliminate misunderstanding"],
    ["Old people and babies who don't meet standards are released","To keep the community functioning and efficient"],
    ["Only the Receiver holds all memories from before Sameness",  "So no one else has to carry the burden of the past"],
  ],
  col2(0.58, 0.42)
));
children.push(T.tableCaption("This table is a teacher reference. Use it to build background knowledge before reading — it is not a student handout."));

// ═══════════════════════════════════════════════════════════════════════
// SECTION 7 — THE THEME EVIDENCE CHART
// ═══════════════════════════════════════════════════════════════════════

children.push(T.heading1("The Theme Evidence Chart — Your Primary Text Interaction Tool"));
children.push(T.teacherRefLabel());

children.push(T.p(
  "The Theme Evidence Chart is how students collect evidence across the whole novel and build toward a theme statement. " +
  "Unlike annotation codes (which work well for shorter argument-based texts), " +
  "theme in The Giver develops across the entire book through accumulation — one moment at a time. " +
  "The chart gives students a place to capture those moments as they read, " +
  "so that by the time they reach Part 5 (Synthesis), the evidence is already organized."
));

children.push(T.callout(
  "The Theme Evidence Chart is pre-writing scaffolding. Students who complete it across all five parts are building their theme essay outline while they read — without knowing it. " +
  "When they reach Part 5, their job is synthesis, not evidence hunting. The reading was the outline."
));

children.push(h2k("How to Use the Chart"));
children.push(...T.bulletList([
  "Introduce the chart before Part 1. Tell students: This is where we collect evidence across the whole book.",
  "At the end of each Part activity, students add one row to the chart: what happened, what Jonas felt or realized, what it might teach us.",
  "Students complete the chart using any access method: symbol selection, gesture + partner record, verbal, or writing.",
  "The chart does not require writing. A student who indicates three symbols per row is completing the chart.",
  "By Part 5, the chart has 4–5 rows — enough evidence to write or construct a theme statement.",
]));

children.push(h2k("Theme Evidence Chart Template"));
children.push(T.makeTable(
  ["Part", "What Happens in This Scene", "What Jonas Feels or Realizes", "What This Might Teach Us About Being Human"],
  [
    ["Part 1 — Sameness", "(students complete)", "(students complete)", "(students complete)"],
    ["Part 2 — Memories", "(students complete)", "(students complete)", "(students complete)"],
    ["Part 3 — The Cost",  "(students complete)", "(students complete)", "(students complete)"],
    ["Part 4 — The Ending","(students complete)", "(students complete)", "(students complete)"],
  ],
  col4(0.12, 0.30, 0.30, 0.28)
));
children.push(T.tableCaption(
  "Students complete one row per Part using any access method. " +
  "Column 3 (What Jonas Feels or Realizes) uses emotion board vocabulary — core words. " +
  "Column 4 (What This Might Teach Us) is the theme-building column — the hardest, most supported."
));

children.push(h2k("Sentence Frames for Column 4 (Theme Building)"));
children.push(T.makeTable(
  ["Frame", "Example Response"],
  [
    ["This shows that without ___, we cannot ___ .",             "'This shows that without memory, we cannot really feel.'"],
    ["When people cannot ___, they lose part of being human.",   "'When people cannot choose, they lose part of being human.'"],
    ["Lowry is showing us that ___ is important because ___.",   "'Lowry is showing us that feeling pain is important because it is connected to feeling joy.'"],
    ["This might mean that ___ is what makes us fully human.",   "'This might mean that choice is what makes us fully human.'"],
  ],
  col2(0.55, 0.45)
));
children.push(T.tableCaption("These frames use core vocabulary — feel, choose, remember, real, human. Students who cannot write can select the key words and a partner records the frame."));

// ═══════════════════════════════════════════════════════════════════════
// SECTION 8 — PART 1: THE RULES OF SAMENESS
// ═══════════════════════════════════════════════════════════════════════

children.push(T.heading1("Part 1: The Rules of Sameness"));
children.push(T.teacherRefLabel());

children.push(T.makeTable(
  ["Element", "Detail"],
  [
    ["Novel Section",  "Chapters 1–8 — Jonas's community and the Ceremony of Twelve"],
    ["Skill Focus",    "Identifying what the community controls and what that reveals about the theme"],
    ["Standards",      "RL.6.2 · RL.7.2 · RL.7.1 (evidence)"],
    ["Partner Mode",   "Mode 2 during reading · Mode 1 for activity"],
    ["Materials",      "The Giver · Theme Evidence Chart · Community Overview reference"],
  ],
  col2(0.28, 0.72)
));

children.push(T.spacer());
children.push(h2k("Activity Overview"));
children.push(T.p(
  "In Chapters 1–8, students are introduced to Jonas's community — its rules, its structure, its language, and its rituals. " +
  "The Ceremony of Twelve ends the section when Jonas receives his Assignment as the next Receiver of Memory. " +
  "Part 1 asks students to look at the community with fresh eyes: What is being controlled? What is missing? What does that cost?"
));
children.push(T.callout(
  "The key move in Part 1 is noticing absence — not what the community has, but what it does not have. " +
  "Students who cannot access complex explanations can still respond to: What is missing? What do we have that they do not?"
));

children.push(h2k("Community Control Sort"));
children.push(T.p(
  "Present students with a list of things the community controls. " +
  "Students sort them into two categories: What does this control take away? What does it give people instead?"
));
children.push(T.makeTable(
  ["The Community Controls", "What This Takes Away", "What This Gives Instead"],
  [
    ["Job assignments",  "", ""],
    ["Family structure", "", ""],
    ["Weather",          "", ""],
    ["Color",            "", ""],
    ["Feelings",         "", ""],
    ["Language",         "", ""],
  ],
  col3(0.33, 0.33, 0.34)
));
children.push(T.tableCaption("Students complete using symbol selection, pointing, partner-confirmed verbal, or writing. There is no single correct answer — the goal is thinking, not recall."));

children.push(h2k("Key Questions for Part 1"));
children.push(T.makeTable(
  ["Question", "Response Scaffold"],
  [
    ["What does this community control?",                              "Select from: weather / color / feeling / job / family / language / who lives and dies"],
    ["What does Sameness take away?",                                  "Sentence frame: 'Sameness takes away ___.'"],
    ["What might be good about living in this community?",             "Two-column sort: Good / Hard — students indicate which column each idea goes in"],
    ["What is the community afraid of?",                               "Select: pain / difference / surprise / conflict / not being the same"],
    ["What does Jonas learn about himself at the Ceremony of Twelve?", "He is different. He has been chosen for something no one else in his community will do."],
  ],
  col2(0.44, 0.56)
));

children.push(h2k("Partner Guidance — Part 1"));
children.push(T.callout(
  "Wait time: Give 10–15 seconds before prompting. Theme questions are abstract — students need time to form a response.\n\n" +
  "Model AAC use naturally during reading: 'I notice the community controls the weather. That seems strange. I feel uncertain about that.' [Indicate feel + uncertain on system.]\n\n" +
  "If a student cannot access the sort independently: present two options at a time. 'Does this take away something good, or does it give something good?' Accept any indication as a response."
));

children.push(h2k("Theme Evidence Chart — Row 1 (complete at end of Part 1)"));
children.push(T.makeTable(
  ["Column", "Prompt to Student", "Example Response"],
  [
    ["What Happens",          "What does the community control in these chapters?",           "'They control jobs and feelings and color and weather.'"],
    ["What Jonas Feels",      "How does Jonas feel about his Assignment?",                    "'He feels uncertain and scared and chosen.'"],
    ["What This Teaches Us",  "What might Lowry be showing us about what happens when everything is controlled?", "'When people cannot choose, they lose part of what it means to be human.'"],
  ],
  col3(0.22, 0.40, 0.38)
));

// ═══════════════════════════════════════════════════════════════════════
// SECTION 9 — PART 2: THE FIRST MEMORIES
// ═══════════════════════════════════════════════════════════════════════

children.push(T.heading1("Part 2: The First Memories"));
children.push(T.teacherRefLabel());

children.push(T.makeTable(
  ["Element", "Detail"],
  [
    ["Novel Section",  "Chapters 9–16 — Jonas's training begins; first memories received"],
    ["Skill Focus",    "How memories reveal what was taken away — evidence for theme"],
    ["Standards",      "RL.7.2 (theme development) · RL.7.1 (textual evidence)"],
    ["Partner Mode",   "Mode 2 during reading · Mode 1 for activity"],
    ["Key vocabulary", "memory · color · feel · different · real · choose · family"],
  ],
  col2(0.28, 0.72)
));

children.push(T.spacer());
children.push(h2k("Activity Overview"));
children.push(T.p(
  "Jonas's training begins. The Giver transfers memories — a sled ride in snow, sunshine, color, a family holiday, music. " +
  "Each memory is something the community decided to eliminate under Sameness. " +
  "Part 2 asks students to examine these memories not as plot events but as evidence: " +
  "What did each memory give Jonas? What does that reveal about what was taken away? " +
  "What do these experiences have to do with being human?"
));

children.push(h2k("Memory Evidence Table"));
children.push(T.makeTable(
  ["Memory Jonas Receives", "What It Gave Him", "What It Reveals Was Taken Away"],
  [
    ["Snow on a sled (first memory)", "", ""],
    ["Sunshine and warmth",           "", ""],
    ["Color (the girl's red hair)",   "", ""],
    ["A family holiday — joy and love", "", ""],
    ["War — pain and death",          "", ""],
  ],
  col3(0.35, 0.33, 0.32)
));
children.push(T.tableCaption("Students complete using any access method. The third column is the theme-building column — what was taken away is the heart of the unit question."));

children.push(h2k("Key Questions for Part 2"));
children.push(T.makeTable(
  ["Question", "Response Scaffold"],
  [
    ["What does Jonas receive that he has never felt before?",      "Select from: snow / warmth / color / love / pain / surprise / music / belonging"],
    ["What does it feel like to have that for the first time?",     "Emotion board — indicate the feeling"],
    ["What does this memory show us about what Sameness removed?",  "Sentence frame: 'Sameness removed ___ because ___.'" ],
    ["Why did the community decide to give up these things?",       "Select: too painful / too different / not fair / hard to control / too much feeling"],
    ["What do you think Jonas feels about receiving these memories?","Two responses: the good part and the hard part. Students indicate both."],
  ],
  col2(0.44, 0.56)
));

children.push(h2k("Partner Guidance — Part 2"));
children.push(T.callout(
  "Wait time: 10–15 seconds. Students are building connections between abstract concepts.\n\n" +
  "Model AAC use during reading: 'Jonas is feeling something new. I think he feels surprised and happy but also confused — because nobody else can feel this.' [Indicate feel + surprised + confused.]\n\n" +
  "The war memory (Chapter 15) is emotionally significant. Prepare students before reading it. 'Jonas is going to receive a very hard memory. It will be painful. That is the point of this chapter.'"
));

children.push(h2k("Theme Evidence Chart — Row 2 (complete at end of Part 2)"));
children.push(T.makeTable(
  ["Column", "Prompt to Student", "Example Response"],
  [
    ["What Happens",         "What does Jonas receive in his training?",                          "'He receives memories — snow, color, a family, and then war.'"],
    ["What Jonas Feels",     "How does receiving memories change how Jonas feels?",               "'He feels things he has never felt before. He feels more real.'"],
    ["What This Teaches Us", "What might Lowry be showing us about what memories do for us?",    "'Memories make us feel. Without them, we cannot really be human.'"],
  ],
  col3(0.22, 0.40, 0.38)
));

// ═══════════════════════════════════════════════════════════════════════
// SECTION 10 — PART 3: WHAT JONAS FEELS AND REALIZES
// ═══════════════════════════════════════════════════════════════════════

children.push(T.heading1("Part 3: What Jonas Feels and Realizes"));
children.push(T.teacherRefLabel());

children.push(T.makeTable(
  ["Element", "Detail"],
  [
    ["Novel Section",  "Chapters 17–22 — Jonas learns the truth about release; plans to flee"],
    ["Skill Focus",    "How Jonas's internal change develops the theme"],
    ["Standards",      "RL.7.2 · RL.8.2 (theme development through character relationship)"],
    ["Partner Mode",   "Mode 2 during reading · Mode 1 for activity"],
    ["Key vocabulary", "release · feel · real · choose · alone · change · believe"],
  ],
  col2(0.28, 0.72)
));

children.push(T.spacer());
children.push(h2k("Activity Overview"));
children.push(T.p(
  "In Chapters 17–22, Jonas discovers the truth about release: it means death. " +
  "He watches a recording of his father releasing a twin — and sees, for the first time, what his community actually does. " +
  "This is the emotional and thematic climax of the novel. Jonas is changed by what he sees, and he makes a decision: he will flee. " +
  "Part 3 asks students to trace Jonas's internal change and connect it to the theme. " +
  "This is the moment where what the community took away becomes undeniable."
));

children.push(h2k("Jonas's Internal Change Chart"));
children.push(T.makeTable(
  ["", "Before Learning About Release", "After Learning About Release"],
  [
    ["How Jonas feels about his community", "", ""],
    ["What Jonas believes about his father", "", ""],
    ["What Jonas believes about Sameness",   "", ""],
    ["What Jonas decides to do",             "", ""],
  ],
  col3(0.32, 0.34, 0.34)
));
children.push(T.tableCaption("Students complete using any access method. The contrast between the two columns IS the evidence for Jonas's change — and for the theme."));

children.push(h2k("Key Questions for Part 3"));
children.push(T.makeTable(
  ["Question", "Response Scaffold"],
  [
    ["What does Jonas discover about what 'release' really means?", "Select: sent away / death / the community ends their life / a lie / not what everyone thought"],
    ["How does Jonas feel when he watches the recording?",          "Emotion board — indicate the feeling. Sentence frame: 'Jonas feels ___ because ___.'" ],
    ["Why is this moment the most important in the book?",          "Sentence frame: 'This is important because Jonas now knows ___ that he cannot unknow.'"],
    ["What does Jonas decide to do — and why?",                     "He decides to leave. Sentence frame: 'Jonas chooses to leave because ___.'" ],
    ["What does his decision show about what being human means?",   "His decision shows that he has the ability to choose — even when it is dangerous and hard."],
  ],
  col2(0.44, 0.56)
));

children.push(h2k("Partner Guidance — Part 3"));
children.push(T.callout(
  "This is the most emotionally difficult section of the novel. Prepare students before the release recording chapter.\n\n" +
  "Wait time: 15 seconds minimum for 'How does Jonas feel?' questions. This is a layered emotional response.\n\n" +
  "Model AAC use: 'Jonas watched something very hard. I think he feels shocked and angry and alone — because nobody else in his community would even feel that way.' [Indicate on system.]\n\n" +
  "If a student needs more support: 'Jonas now knows something true that his community pretended was different. That knowledge changed him. What changed?'"
));

children.push(h2k("Theme Evidence Chart — Row 3 (complete at end of Part 3)"));
children.push(T.makeTable(
  ["Column", "Prompt to Student", "Example Response"],
  [
    ["What Happens",         "What does Jonas learn in these chapters?",                           "'He learns that release means death. His community has been lying.'"],
    ["What Jonas Feels",     "How does learning the truth about release change Jonas?",            "'He feels angry and alone. He decides to leave because he cannot pretend anymore.'"],
    ["What This Teaches Us", "What might Lowry be showing us about what happens when we take away the truth?", "'When people cannot know the truth, they cannot make real choices. That makes them less than fully human.'"],
  ],
  col3(0.22, 0.40, 0.38)
));

// ═══════════════════════════════════════════════════════════════════════
// SECTION 11 — PART 4: THE ENDING
// ═══════════════════════════════════════════════════════════════════════

children.push(T.heading1("Part 4: The Ending — and What Lowry Leaves Open"));
children.push(T.teacherRefLabel());

children.push(T.makeTable(
  ["Element", "Detail"],
  [
    ["Novel Section",  "Chapters 23 and beyond — Jonas and Gabriel flee"],
    ["Skill Focus",    "How the ambiguous ending develops the theme; author's deliberate craft choice"],
    ["Standards",      "RL.7.2 · RL.8.2 (theme through plot and ending)"],
    ["Partner Mode",   "Mode 2 during reading · Mode 1 for activity"],
    ["Key vocabulary", "hope · maybe · real · choose · believe · together · ahead"],
  ],
  col2(0.28, 0.72)
));

children.push(T.spacer());
children.push(h2k("Activity Overview"));
children.push(T.p(
  "The ending of The Giver is deliberately ambiguous. " +
  "Jonas reaches a hill. He sees lights and hears music. He believes he is reaching a place called Elsewhere. " +
  "But Lowry does not confirm this. We do not know if Jonas and Gabriel survive. " +
  "The question is not a mistake or an omission — the ambiguity IS the point. " +
  "Part 4 asks students to sit with that uncertainty and ask: Why would Lowry end the book this way? What does that choice teach us?"
));
children.push(T.callout(
  "Ambiguous endings are hard for every reader — and may be harder for students who rely on certainty and predictability. " +
  "Frame the ambiguity as a deliberate author choice, not a mistake or a gap in understanding. " +
  "'Lowry does not tell us what happens. That is on purpose. We have to decide what we believe.'"
));

children.push(h2k("The Ending: Two Interpretations"));
children.push(T.makeTable(
  ["Interpretation", "Evidence That Supports It", "What It Might Mean for the Theme"],
  [
    ["Jonas and Gabriel survive — they reach Elsewhere", "The lights and music feel real; Lowry allows hope", "Hope exists. Even when a system takes everything, humans can still reach toward something better."],
    ["What Jonas sees is a final memory — he is dying",  "Jonas is cold, starving, almost unconscious; the sled memory echoes the first memory", "Even at the end, Jonas is fully human — he feels, he imagines, he hopes. That is what was always worth fighting for."],
  ],
  col3(0.30, 0.36, 0.34)
));
children.push(T.tableCaption("Both interpretations are valid. Students should select the one they believe and explain why using evidence. 'I think ___ because ___.'" ));

children.push(h2k("Key Questions for Part 4"));
children.push(T.makeTable(
  ["Question", "Response Scaffold"],
  [
    ["What does Jonas see and hear at the end?",                       "He sees lights. He hears music. He feels like he has been there before."],
    ["Do you think Jonas and Gabriel survive?",                        "I think yes / I think no / I am not sure — because ___."],
    ["Why do you think Lowry chose to end the story without telling us what happens?", "Sentence frame: 'Lowry leaves this open because ___.'" ],
    ["What does the ending make you feel?",                            "Emotion board — indicate the feeling."],
    ["Does Jonas have hope at the end of the story?",                  "Yes / No / Maybe — indicate and explain."],
  ],
  col2(0.50, 0.50)
));

children.push(h2k("Theme Evidence Chart — Row 4 (complete at end of Part 4)"));
children.push(T.makeTable(
  ["Column", "Prompt to Student", "Example Response"],
  [
    ["What Happens",         "What happens at the very end of the book?",                                 "'Jonas and Gabriel go over the hill. He sees lights and hears music. We do not know if they survive.'"],
    ["What Jonas Feels",     "What does Jonas feel at the end of the story?",                            "'He feels hope — even though he is cold and scared and maybe dying.'"],
    ["What This Teaches Us", "What might Lowry be showing us about what humans do — even at the hardest moment?", "'Even at the end, Jonas still hopes. That is what it means to be human — to keep hoping and choosing, even when it is hard.'"],
  ],
  col3(0.22, 0.40, 0.38)
));

// ═══════════════════════════════════════════════════════════════════════
// SECTION 12 — PART 5: WHOLE-BOOK SYNTHESIS
// ═══════════════════════════════════════════════════════════════════════

children.push(T.heading1("Part 5: Whole-Book Synthesis — What Does The Giver Teach?"));
children.push(T.teacherRefLabel());

children.push(T.makeTable(
  ["Element", "Detail"],
  [
    ["Novel Section",    "Full book — synthesis activity"],
    ["Skill Focus",      "Constructing a theme statement supported by evidence from across the novel"],
    ["Standards",        "RL.6.2 · RL.7.2 · RL.8.2 (theme) + RL.7.1 (evidence)"],
    ["Text tool",        "Theme Evidence Chart (completed across Parts 1–4)"],
    ["Format",           "Theme statement + evidence from Chart + synthesis response"],
    ["Response Access",  "All three pathways: symbol selection, verbal/gestural, generative construction"],
  ],
  col2(0.28, 0.72)
));

children.push(T.spacer());
children.push(h2k("Activity Overview"));
children.push(T.p(
  "By the time students reach Part 5, their Theme Evidence Chart has four rows — one from each part of the novel. " +
  "Part 5 asks them to look across the chart and build a theme statement: " +
  "one clear idea about what The Giver teaches about being fully human. " +
  "That statement is supported by evidence from the chart. " +
  "The chart was the pre-writing scaffold; the synthesis is the outcome."
));

children.push(h2k("Build the Theme Statement: Three Steps"));
children.push(T.makeTable(
  ["Step", "What to Do", "Example"],
  [
    ["Step 1 — Review the Chart",  "Look at Column 4 of your completed Theme Evidence Chart. What ideas appear more than once? What does the story keep showing us?", "'Memory, choice, and feeling keep appearing. The story keeps showing us what happens when you take those away.'"],
    ["Step 2 — Draft the Statement", "Use a sentence frame to build the theme statement. The statement must say what The Giver teaches — not just what happens in the plot.", "'The Giver teaches us that memory, choice, and feeling are what make us fully human — and that taking them away does not create peace. It creates emptiness.'"],
    ["Step 3 — Add Evidence",      "Choose two rows from your chart as evidence. Which scenes show your theme most clearly?", "'Part 2 — when Jonas receives color and family. Part 3 — when he watches the release recording and chooses to leave.'"],
  ],
  col3(0.22, 0.44, 0.34)
));

children.push(h2k("Theme Statement Frames (Core Vocabulary Construction)"));
children.push(T.makeTable(
  ["Frame", "Core Words Available", "Sample Completed Statement"],
  [
    ["According to The Giver, we are fully human when we can ___.",
     "feel · choose · remember · know the truth · love · hope",
     "'According to The Giver, we are fully human when we can feel, choose, and remember.'"],
    ["The Giver teaches us that taking away ___ means taking away ___.",
     "memory · choice · color · pain · love · the truth",
     "'The Giver teaches us that taking away memory means taking away everything that makes life real.'"],
    ["Lowry shows that a world without ___ is not peaceful — it is ___.",
     "feeling · memory · choice · color · love / empty · less · not human · not real",
     "'Lowry shows that a world without feeling is not peaceful — it is empty.'"],
    ["The most important thing The Giver teaches is that ___ because ___.",
     "All core vocabulary available",
     "'The most important thing The Giver teaches is that humans need to feel — because feeling is what makes choices matter.'"],
  ],
  col3(0.35, 0.30, 0.35)
));

children.push(h2k("Alternative Response: Symbol Sort for Theme"));
children.push(T.p(
  "For students who need a more structured response option, provide a symbol sort. " +
  "Give the student 8–10 symbols representing ideas from The Giver: memory, choose, feel, real, together, alone, human, empty, hope, truth. " +
  "Ask: Which ones are what this story is really about? Sort into: Yes, the story is about this / No / Maybe. " +
  "Ask the student to select their top 3 and explain one using a sentence frame. " +
  "The sort IS the theme statement — the student has identified the central ideas of the novel."
));

children.push(h2k("Whole-Book Discussion: Open Questions"));
children.push(...T.bulletList([
  "What would you give up to live in a world with no pain? What would you keep?",
  "Is it possible to feel happy if you have never felt sad? Why or why not?",
  "Jonas is the only person in his community who knows what everyone else is missing. What is it like to know something that nobody around you knows?",
  "The ending is not answered. Is that okay with you? Why or why not?",
  "What does The Giver teach that you will remember — not as a plot event, but as an idea?",
]));

// ═══════════════════════════════════════════════════════════════════════
// SECTION 13 — IEP GOALS + DATA COLLECTION
// ═══════════════════════════════════════════════════════════════════════

children.push(T.heading1("IEP Goal Stems and Data Collection"));
children.push(T.teacherRefLabel());

children.push(T.p(
  "CbD units ship with two goal stem types per unit: one academic ELA goal and one AAC communication goal. " +
  "These are starting points for the IEP team — not final language. Edit to match the student's baseline, access method, IEP review date, and team decisions. " +
  "Academic progress and communication progress are separate. Both need separate goals and separate data."
));
children.push(T.callout(
  "All goal stems follow IDEA's measurability requirement: Given [condition] → will [observable verb + skill] → as measured by [data tool] → achieving [criterion] → across [consistency] → by [date].\n" +
  "Never use 'understand,' 'know,' or 'learn' — these are not observable behaviors."
));

children.push(h2k("Academic Goal Stems — Theme Analysis (RL)"));
children.push(T.makeTable(
  ["Standard", "Goal Stem"],
  [
    ["RL.6.2",
     "Given The Giver by Lois Lowry read aloud by a partner, a Theme Evidence Chart, and theme sentence frames, [student] will identify the central theme of the novel and cite at least one piece of textual evidence to support it as measured by rubric scoring on Part 5 (Synthesis), achieving a score of Approaching or Meets on 4 of 5 trials across 3 consecutive sessions by [IEP date]."],
    ["RL.7.2",
     "Given The Giver by Lois Lowry read aloud by a partner and a completed Theme Evidence Chart, [student] will construct a theme statement explaining what the novel teaches about being fully human and cite at least two pieces of textual evidence from across the novel, as measured by rubric scoring on Part 5 (Synthesis), achieving a complete theme statement with two evidence citations on 4 of 5 trials across 3 consecutive sessions by [IEP date]."],
    ["RL.8.2",
     "Given The Giver by Lois Lowry read aloud by a partner and a completed Theme Evidence Chart, [student] will construct a theme statement and analyze how it develops across the novel by explaining its connection to Jonas's character, the community's structure, and the ending, as measured by rubric scoring on Part 5 (Synthesis) and Part 4 (Ending) activities, achieving a complete analysis with multi-part evidence on 4 of 5 trials across 3 consecutive sessions by [IEP date]."],
  ],
  col2(0.10, 0.90)
));
children.push(T.tableCaption("Select the standard anchor that matches the student's IEP and grade placement. Adjust condition (access method), criterion (from baseline data), and date to match the individual student."));

children.push(T.spacer());
children.push(h2k("AAC Communication Goal Stem — Theme Analysis Context"));
children.push(T.p(
  "This goal targets communication development within The Giver unit context — separate from the academic ELA skill. " +
  "Data is collected on the Communication Session Tracker by the paraprofessional, not on the academic rubric."
));
children.push(T.makeTable(
  ["Goal Type", "Goal Stem"],
  [
    ["Multi-symbol utterance",
     "Given The Giver by Lois Lowry shared reading with a communication partner using Aided Language Stimulation, [student] will produce a 2+ symbol utterance in response to theme evidence questions (e.g., 'What does this show us?') as measured by Communication Session Tracker data, achieving 4 of 5 response opportunities across 2 consecutive sessions with 2 different partners by [IEP date]."],
    ["Abstract vocabulary use in context",
     "Given The Giver unit with pre-confirmed theme vocabulary (memory, choose, feel, real) and partner Aided Language Stimulation, [student] will use at least one theme-related fringe vocabulary word in a contextually appropriate response during a Part 1–5 activity as measured by Communication Session Tracker data, achieving 4 of 5 opportunities across 2 consecutive sessions by [IEP date]."],
  ],
  col2(0.22, 0.78)
));
children.push(T.tableCaption(
  "Academic progress ≠ communication progress. A student can meet the rubric criterion using a sentence frame and still be building toward spontaneous AAC output — track both separately. " +
  "Generalization criterion: 2+ different partners. AAC skills that only appear with one partner have not generalized."
));

children.push(T.spacer());
children.push(h2k("Data Collection Guidance"));
children.push(T.p(
  "Collect data during Mode 1 activities only (Parts 1–5 Theme Evidence Chart and synthesis activities). Do not collect data during shared reading in Mode 2. " +
  "Record the student's response, the prompt level used, and whether the response was independent, prompted, or modeled. " +
  "Non-response is data — record the prompt level reached and the environmental factors."
));
children.push(T.makeTable(
  ["Data Point", "Record", "Why"],
  [
    ["Response type",      "Symbol / gesture / verbal / partner-confirmed / no response", "Shows access method, not just accuracy"],
    ["Prompt level used",  "1 (wait) through 5 (reassess)",                               "Shows instructional level and growth over time"],
    ["Vocabulary access",  "Yes — on device / No — not programmed / Partial — board only", "Critical for AAC team communication"],
    ["Activity condition", "Read aloud / chart available / sentence frame provided / independent", "Context matters for interpreting data"],
  ],
  col3(0.22, 0.42, 0.36)
));

// ═══════════════════════════════════════════════════════════════════════
// SECTION 14 — COMMUNICATION ACCESS QUICK REFERENCE
// ═══════════════════════════════════════════════════════════════════════

children.push(T.heading1("Communication Access Quick Reference"));
children.push(T.p("Pull out and laminate this page for the partner. This is the one-page summary for anyone working alongside the student during this unit."));

children.push(T.callout(
  "THE GIVER — Theme Analysis | Fiction Anchor Text Unit | Communicate by Design\n" +
  "The text stays the same. The scaffold varies. The expectation does not."
));

children.push(h2k("During Reading: Mode 2"));
children.push(...T.bulletList([
  "Follow the student's lead. Do NOT run prompt hierarchy during the read.",
  "Note spontaneous communication — write it down, do not redirect it.",
  "Model AAC use naturally during reading: 'Jonas is discovering something. I think he feels confused and surprised.' [Indicate on system.]",
  "No demands. No correct/incorrect. Partnership only.",
]));

children.push(h2k("During Activities: Mode 1"));
children.push(...T.bulletList([
  "Wait 10–15 seconds before prompting. Theme vocabulary is abstract — processing time is essential.",
  "Start with the least intrusive prompt (gesture toward system).",
  "Accept: symbol, gaze, gesture, pointing, verbal, partner-confirmed — all valid.",
  "Never complete the response for the student.",
  "If no response: Is the vocabulary available? Is this the right mode? Is the environment set up correctly?",
]));

children.push(h2k("Top 5 Vocabulary Words — Confirm Before Starting"));
children.push(T.makeTable(
  ["Word", "Check"],
  [
    ["memory",  "☐ On device / board"],
    ["choose",  "☐ On device / board"],
    ["feel",    "☐ On device / board"],
    ["release", "☐ On device / board"],
    ["real",    "☐ On device / board"],
  ],
  col2(0.5, 0.5)
));
children.push(T.tableCaption("If a word is not available on the device, prepare a physical symbol or board card before the activity. Do not skip the pre-check."));

children.push(h2k("Theme Evidence Chart Quick Guide"));
children.push(T.makeTable(
  ["Part", "Add a row to the chart for...", "Key prompt"],
  [
    ["Part 1", "What the community controls + how Jonas feels about his Assignment",          "'What is missing in this community?'"],
    ["Part 2", "A memory Jonas receives + what it reveals about what was taken away",         "'What did that memory give him?'"],
    ["Part 3", "What Jonas learns about release + why he decides to leave",                   "'What does Jonas know now that he cannot unknow?'"],
    ["Part 4", "What Jonas sees at the end + whether you think he survives",                  "'Does Jonas have hope at the end?'"],
  ],
  col3(0.12, 0.52, 0.36)
));

// ═══════════════════════════════════════════════════════════════════════
// END MATTER
// ═══════════════════════════════════════════════════════════════════════

// NOTE: About the Creator, Terms of Use, and Accessibility Statement are NOT included
// in the fiction unit Teaching Materials docx. They live in the Welcome to the Product PDF only.
// See fiction_reference.md for this rule.

// ─────────────────────────────────────────────────────────────────────────
// ASSEMBLE AND WRITE
// ─────────────────────────────────────────────────────────────────────────

const outputPath = path.join(__dirname, "The_Giver_Theme_Analysis_Teaching_Materials.docx");

T.assembleAndWrite(
  `${UNIT_TITLE}: ${UNIT_SUBTITLE}`,
  children,
  outputPath,
  {
    title: `The Giver: Theme Analysis — Fiction Anchor Text Unit`,
    description: `SDI companion unit for The Giver by Lois Lowry. Theme Analysis · Grades ${GRADE_RANGE} · Communicate by Design`,
  }
);

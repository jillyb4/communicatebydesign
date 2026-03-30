#!/usr/bin/env node

/**
 * Wonder: Character Analysis — Fiction Anchor Text Unit Builder
 * Communicate by Design
 *
 * Novel: Wonder by R.J. Palacio
 * Skill: Character Analysis (RL.6.3 / RL.7.3)
 * Scope: Whole book — grades 3–8
 *
 * Output: Wonder_Character_Analysis_COMPLETE.docx
 */

const path = require("path");
const T = require(path.join(__dirname, "..", "..", "..", "_Operations", "cbd_docx_template"));

const CW = T.CONTENT_WIDTH; // 10080 DXA

// Alias for clean code — uses template's own heading2
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

const UNIT_TITLE    = "Wonder";
const UNIT_SUBTITLE = "Character Analysis";
const NOVEL_AUTHOR  = "R.J. Palacio";
const SKILL_NAME    = "Character Analysis";
const GRADE_RANGE   = "3–8";
const RL_STANDARDS  = "RL.3.3 · RL.5.3 · RL.6.3 · RL.7.3";
const PRODUCT_LINE  = "Fiction Anchor Text Unit";

// ─────────────────────────────────────────────────────────────────────────
// AAC ACCESS NOTE CONSTANTS
// Single source of truth for vocab table AAC access language.
// Update here → updates everywhere. Do not inline these strings.
// ─────────────────────────────────────────────────────────────────────────
const AAC_CORE          = "Part of most AAC ecosystems";
const AAC_CORE_CONFIRM  = "Part of most AAC ecosystems — confirm location before unit";
const AAC_CORE_VERIFY   = "Part of most AAC ecosystems — verify location";
const AAC_CORE_KIND     = "Part of most AAC ecosystems — confirm 'kind' vs 'kindness'";

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
    ["Required Materials", "Copy of Wonder (not included) · AAC system (any access method) · Communication boards (included)"],
  ],
  col2(0.28, 0.72)
));

children.push(T.spacer());
children.push(h2k("What This Unit Is"));
children.push(T.p(
  "This is a Specially Designed Instruction (SDI) companion unit for the novel Wonder by R.J. Palacio. " +
  "The novel is not included — your class or student already has it. What this unit provides is the instructional and communication access layer: " +
  "the teacher guide, AAC-designed activities, vocabulary supports, and response structures that make the novel accessible to students who use alternative and augmentative communication."
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
  "A unit about disability awareness (Wonder does that — this unit is about the literacy skill)",
]));

children.push(h2k("What's Included"));
children.push(...T.bulletList([
  "Teacher SDI guide with 5-part lesson sequence",
  "Before-reading vocabulary preview with core and fringe word list",
  "Part 1: Describe to Draw — building character description without name-recall",
  "Part 2: Character Comparison — symbol-supported comparison structure",
  "Part 3: Character Motivation — inferencing with because/maybe/probably scaffold",
  "Part 4: Character Change — before/after story arc",
  "Part 5: Whole-book synthesis — theme through character, Write-Ables format",
  "Communication Access quick-reference card (partner pull-out)",
  "Core and fringe vocabulary table with AAC access notes",
  "IEP goal stems for RL.3.3 through RL.7.3",
  "Data collection guidance",
]));

// ═══════════════════════════════════════════════════════════════════════
// SECTION 2 — RESEARCH BASE
// ═══════════════════════════════════════════════════════════════════════

children.push(T.heading1("Research Base"));
children.push(T.teacherRefLabel());

children.push(h2k("Why Fiction Requires a Different SDI Framework"));
children.push(T.p(
  "Narrative comprehension draws on a different cognitive and linguistic skill set than informational text. " +
  "Where nonfiction asks students to evaluate evidence and trace argument structure, fiction asks students to track character motivation, infer emotional states, " +
  "understand theme as an abstraction, and follow the inner lives of people they cannot see or verify. " +
  "For students who use AAC, this creates a specific challenge: the hardest vocabulary in fiction is not domain-specific content words — " +
  "it is the language of minds and feelings."
));

children.push(h2k("Story Grammar as SDI Evidence Base"));
children.push(T.p(
  "Story Grammar instruction (Spencer & Petersen, 2020) is the primary evidence-based framework for narrative SDI. " +
  "Story grammar gives students an organizational schema for any narrative: character, setting, problem/conflict, events, resolution, theme. " +
  "Research shows statistically significant improvements in comprehension strategy use and story-structure knowledge for students with and without disabilities " +
  "when explicit story grammar instruction is provided (ERIC EJ871908)."
));
children.push(T.callout(
  "Story grammar is recognized SDI practice. It adapts the methodology and delivery — not the standard. " +
  "Every student is working toward the same RL standard. The story grammar scaffold is how we get them there."
));

children.push(h2k("Narrative Language and AAC"));
children.push(T.p(
  "Narrative macrostructure — the quality and organization of how a student processes a story — accounts for significant variance in reading comprehension " +
  "beyond what decoding and basic language measures explain (Spencer & Petersen, 2020). " +
  "Teaching story structure is literacy instruction, not a support activity. " +
  "ASHA identifies narrative intervention as accessible and evidence-supported for complex communicators (Perspectives, 2022), " +
  "and aided language stimulation during shared reading has moderate-to-strong evidence."
));

children.push(h2k("Mental State Language Is the Core Challenge"));
children.push(T.p(
  "For students with complex communication needs, emotional and mental state language is the hardest domain — and it is also the heart of literary analysis. " +
  `Words like because, maybe, believe, decide, and wonder are core vocabulary words, ${AAC_CORE.toLowerCase()}, ` +
  "but they are rarely targeted explicitly in fiction instruction. " +
  "Pre-teaching emotional vocabulary before each part of Wonder is a non-negotiable step in this unit."
));

children.push(h2k("Description-First Activity Design"));
children.push(T.p(
  "A central principle of this unit is that activities are designed around description, action, and attribute — not name-recall. " +
  "Character names are fringe words: specific proper nouns that are often not programmed on a student's device. " +
  "A student who cannot say or select 'Auggie' may be fully able to indicate: small, boy, face looks different, feels scared, wants a friend. " +
  "That is comprehension. This unit is designed so that description is always the access point."
));

children.push(h2k("Visual Scene Displays in Narrative Contexts"));
children.push(T.p(
  "Visual Scene Displays (VSDs) embedded in narrative contexts increase participation of complex communicators, " +
  "enable rapid vocabulary acquisition, and reduce cognitive load by situating vocabulary within the actual scene (Drager et al., 2003). " +
  "This unit uses VSDs for key scenes in Wonder rather than decontextualized symbol cards."
));

// ═══════════════════════════════════════════════════════════════════════
// SECTION 3 — NOVEL OVERVIEW
// ═══════════════════════════════════════════════════════════════════════

children.push(T.heading1("Novel Overview: Wonder"));
children.push(T.teacherRefLabel());

children.push(T.makeTable(
  ["Element", "Detail"],
  [
    ["Author",             "R.J. Palacio"],
    ["Published",          "2012"],
    ["Genre",              "Middle-Grade Fiction / Contemporary Realistic Fiction"],
    ["Typical Grade Use",  "Grades 3–8"],
    ["Lexile",             "790L"],
    ["Narrator Structure", "6 narrators: Auggie, Via, Jack, Julian, Miranda, and August again"],
    ["Central Theme",      "Belonging, kindness, identity, and what it means to be seen"],
    ["Disability Rep.",    "Auggie has mandibulofacial dysostosis — a craniofacial difference that affects his appearance"],
  ],
  col2(0.28, 0.72)
));

children.push(T.spacer());
children.push(h2k("Why Wonder for This Unit"));
children.push(T.p(
  "Wonder is taught in thousands of classrooms because its structure invites exactly the kind of thinking that character analysis requires. " +
  "Six narrators recount the same year from six different vantage points. " +
  "Students must track who is speaking, what each person knows, what they want, why they act the way they do, and how they change. " +
  "Every one of those tasks is a character analysis skill."
));
children.push(T.p(
  "For students who use AAC, Wonder is an especially strong choice because Auggie's experience of being seen — or not seen — as a full person " +
  "is directly relevant to the experience of many complex communicators. " +
  "The book's central message (choose kind; see the person inside, not just the outside) reflects the same framework " +
  "that guides every Communication Access design decision in this unit."
));

children.push(h2k("Characters Referenced in This Unit"));
children.push(T.makeTable(
  ["Character", "Description (not name-based)", "Role"],
  [
    ["Auggie (Augustus)",  "Boy with a craniofacial difference; faces his first year of school", "Narrator / Protagonist"],
    ["Via (Olivia)",       "Auggie's older sister; navigates her own identity in his shadow", "Narrator / Supporting"],
    ["Jack Will",          "Student who becomes Auggie's friend — then betrays him — then chooses him again", "Narrator / Supporting"],
    ["Summer Dawson",      "Student who befriends Auggie without hesitation on the first day", "Supporting"],
    ["Julian Albans",      "Student who leads the social exclusion of Auggie; eventually shown to have his own struggles", "Antagonist → Complex"],
    ["Mr. Tushman",        "Principal; supportive authority figure who sees Auggie as a full person", "Supporting"],
  ],
  col3(0.22, 0.58, 0.20)
));
children.push(T.tableCaption("Character names are fringe words. Always pair with a visual reference when introducing in activities."));

// ═══════════════════════════════════════════════════════════════════════
// SECTION 4 — TARGETED STANDARD
// ═══════════════════════════════════════════════════════════════════════

children.push(T.heading1("Targeted Standard: Character Analysis"));
children.push(T.teacherRefLabel());

children.push(h2k("Standard Statements"));
children.push(T.makeTable(
  ["Grade", "Standard", "Anchor Text"],
  [
    ["3", "RL.3.3", "Describe characters in a story and explain how their actions contribute to the sequence of events."],
    ["5", "RL.5.3", "Compare and contrast two or more characters, settings, or events in a story."],
    ["6", "RL.6.3", "Describe how a particular story's plot unfolds in a series of episodes as well as how the characters respond or change as the plot moves toward a resolution."],
    ["7", "RL.7.3", "Analyze how particular elements of a story or drama interact — how setting shapes the characters or plot."],
  ],
  col3(0.07, 0.13, 0.80)
));
children.push(T.tableCaption("Select the standard anchor that matches the student's IEP and grade placement. All activities in this unit address the same skill at varying response complexity."));

children.push(T.spacer());
children.push(h2k("What Character Analysis Requires in Wonder"));
children.push(...T.bulletList([
  "Identifying the character the story is about in each narrator section",
  "Describing a character's appearance, personality traits, and actions using evidence from the text",
  "Explaining why a character acts the way they do (motivation)",
  "Tracking how a character changes from the beginning to the end of the story",
  "Comparing two characters: how are they similar? How are they different? How do they see the same event?",
  "Connecting character behavior to the theme: what does each character's journey show us about kindness, belonging, or being seen?",
]));

children.push(h2k("Why Description-First Matters for This Standard"));
children.push(T.p(
  "Character analysis depends on description. It is not a name-recall task — it is a description task. " +
  "The standard asks students to describe, compare, analyze, and explain. " +
  "None of those verbs require a student to produce or select a character's proper name. " +
  "This unit is built on that principle. Every activity begins with: What do you know about this person? What do they do? How do they feel? " +
  "Name-recall is available but never the only path."
));

// ═══════════════════════════════════════════════════════════════════════
// SECTION 5 — COMMUNICATION ACCESS
// ═══════════════════════════════════════════════════════════════════════

children.push(T.heading1("Communication Access"));
children.push(T.teacherRefLabel());

children.push(h2k("Partner Modes — When to Use Each"));
children.push(T.makeTable(
  ["Mode", "When", "What the Partner Does", "What the Partner Does NOT Do"],
  [
    ["Mode 1 — Instructional",  "Focused activities (Parts 1–5 of this unit)", "Uses prompt hierarchy; collects data; scaffolds toward independence", "Interrupt the student; complete responses; skip wait time"],
    ["Mode 2 — Partnership",    "During shared novel reading", "Follows student lead; notes spontaneous communication; models AAC use naturally", "Run prompt hierarchy; make demands; correct responses"],
    ["Mode 3 — Participation",  "Performance tasks; group discussion; read-aloud", "Enables access only (holds book, operates device, manages boards)", "Interpret; speak for student; add communication content"],
  ],
  col4(0.18, 0.18, 0.34, 0.30)
));
children.push(T.tableCaption("Mode 2 during reading is non-negotiable. Running Mode 1 (instructional) during novel reading is the most common partner error."));

children.push(T.spacer());
children.push(h2k("5-Level Prompt Hierarchy (Mode 1 Only)"));
children.push(T.makeTable(
  ["Level", "Prompt Type", "What It Looks Like"],
  [
    ["1", "Wait",         "Pause 10–15 seconds. Many students need extended processing time."],
    ["2", "Indirect Cue", "Gesture toward the AAC system without saying anything. Non-directive."],
    ["3", "Direct Cue",   "Point to the specific symbol, location, or area on the board."],
    ["4", "Verbal Model", "Say the response AND demonstrate it on the student's system."],
    ["5", "Reassess",     "Non-response is data. Ask: Is the vocabulary available? Is the activity set up correctly? Is this the right mode?"],
  ],
  col3(0.07, 0.18, 0.75)
));

children.push(T.spacer());
children.push(h2k("Core and Fringe Vocabulary for Wonder — Character Analysis"));

children.push(T.makeTable(
  ["Word", "★ Core / Fringe", "Why It Matters in Wonder", "AAC Access Note"],
  [
    ["feel",                 "★ Core",  "The primary question in every character activity: How does this person feel?", AAC_CORE_CONFIRM],
    ["want",                 "★ Core",  "Character motivation — what does each person want?", AAC_CORE],
    ["think",                "★ Core",  "Internal monologue; narrator perspective", AAC_CORE],
    ["know",                 "★ Core",  "What each narrator knows (and doesn't)", AAC_CORE],
    ["change",               "★ Core",  "Central to character arc across whole book", AAC_CORE],
    ["because",              "★ Core",  "Causal reasoning — essential for motivation questions", AAC_CORE],
    ["maybe",                "★ Core",  "Inference scaffold — 'maybe he feels...'", AAC_CORE],
    ["sad",                  "★ Core",  "Auggie's emotional arc; also Via and Jack", AAC_CORE],
    ["scared",               "★ Core",  "Auggie entering school; any new situation", AAC_CORE],
    ["happy",                "★ Core",  "Resolution; Summer scenes; end of book", AAC_CORE],
    ["alone",                "★ Core",  "Auggie's experience; also Via's isolation", AAC_CORE],
    ["kind",                 "★ Core",  "The central moral theme of the novel", AAC_CORE_KIND],
    ["different",            "Fringe",  "Auggie looks different — THE central descriptor", "Symbol needed"],
    ["belong",               "Fringe",  "Auggie's journey; belonging to a group", "Symbol needed"],
    ["invisible",            "Fringe",  "Auggie's wish; metaphor throughout", "Symbol needed"],
    ["brave",                "Fringe",  "Auggie's trait; also Summer's act of sitting with him", "Symbol needed"],
    ["loyal",                "Fringe",  "Jack's defining trait; tested and restored", "May be core combo: 'always friend'"],
    ["bully",                "Fringe",  "Julian's behavior; important for plot", "Symbol needed"],
    ["face looks different", "Fringe",  "Description of Auggie without using his name", "Visual reference — pair with illustration"],
    ["ordinary",             "Fringe",  "Theme: everyone is ordinary in their own way", "Symbol or core combo"],
    ["friend",               "Fringe",  "Central goal; Summer; Jack", AAC_CORE_VERIFY],
    ["helmet",               "Fringe",  "Early plot point; symbol of hiding and protection", "Symbol needed — specific object"],
    ["school",               "Fringe",  "Primary setting", AAC_CORE],
    ["choose",               "Fringe",  "Precept: 'When given the choice, choose kind'", "Core combo: 'choose' + 'kind'"],
  ],
  col4(0.16, 0.16, 0.40, 0.28)
));
children.push(T.tableCaption(
  "★ Core = high-frequency, cross-context words, part of most AAC ecosystems. " +
  "Fringe = Wonder-specific vocabulary requiring system preparation. " +
  "Coordinate with the student's SLP or AAC team before the unit to confirm vocabulary is available. This is a team responsibility, not an SLP-only task."
));

// ═══════════════════════════════════════════════════════════════════════
// SECTION 6 — BEFORE READING: VOCABULARY PREVIEW
// ═══════════════════════════════════════════════════════════════════════

children.push(T.heading1("Before Reading: Vocabulary Preview"));
children.push(T.teacherRefLabel());

children.push(T.p(
  "Pre-teach vocabulary before beginning the novel. Do not wait until a word appears. " +
  "Students who use AAC need time to build familiarity with vocabulary in low-stakes contexts before they are asked to use it in an activity. " +
  "The emotional vocabulary list below is the highest priority — introduce these first."
));

children.push(h2k("Priority Vocabulary: Emotional and Mental State Words"));
children.push(T.callout(
  "Pre-teach these before Chapter 1. These words carry the most weight in Wonder and are the hardest for students with disabilities to access without explicit instruction."
));
children.push(T.makeTable(
  ["Word", "What It Means in Wonder", "How to Pre-Teach It"],
  [
    ["feel",      "The story is about how people feel — on the inside, where you can't always see it", "Ask: How do you feel right now? Find it on your board."],
    ["different", "Auggie looks different from other people. That is the first thing people notice about him.", "Show two objects: same vs. different. Then: How does it feel to be different?"],
    ["belong",    "To belong means to feel like you fit in — like you are wanted where you are.", "Ask: Where do you belong? Where do you feel like you fit?"],
    ["invisible", "Auggie sometimes wishes he could be invisible — that nobody would see him.", "Act it out: hide your face. 'If you were invisible, nobody would see you.' Why might someone want that?"],
    ["brave",     "Being brave means doing something even when it scares you.", "Ask: Can you think of something brave? Find brave on your board."],
    ["kind",      "Being kind means caring about how other people feel.", "Ask: When has someone been kind to you? What did they do?"],
    ["choose",    "In this book, characters have to choose — be kind or be mean.", "Practice: Give two options. Ask the student to choose. Connect to: they chose that."],
  ],
  col3(0.12, 0.44, 0.44)
));

children.push(T.spacer());
children.push(h2k("Character Introduction: Description Before Name"));
children.push(T.p(
  "Before introducing character names, build descriptions. " +
  "Present each character using their attributes and role — not their name. " +
  "Use a visual reference (image or simplified illustration) alongside the description."
));
children.push(T.makeTable(
  ["Description (introduce first)", "Then introduce name", "Visual reference needed?"],
  [
    ["The boy whose face looks different. He is going to school for the first time. He feels scared and brave at the same time.", "Auggie / August", "Yes — provide illustrated reference"],
    ["His older sister. She loves him but sometimes feels invisible herself. She is kind and worried.", "Via / Olivia", "Yes"],
    ["A student at the school who becomes his friend — then stops — then chooses to be his friend again.", "Jack", "Yes"],
    ["A student who sits with him at lunch on the first day without being asked to. She is brave and kind.", "Summer", "Yes"],
    ["A student who is mean to him. He is popular and powerful and chooses unkindness.", "Julian", "Yes"],
  ],
  col3(0.55, 0.25, 0.20)
));
children.push(T.tableCaption("Description-first introduction is always required. Never lead with a name that may not be on the student's device."));

// ═══════════════════════════════════════════════════════════════════════
// SECTION 7 — PART 1: DESCRIBE TO DRAW
// ═══════════════════════════════════════════════════════════════════════

children.push(T.heading1("Part 1: Describe to Draw — Building Character Description"));
children.push(T.teacherRefLabel());

children.push(T.makeTable(
  ["Element", "Detail"],
  [
    ["Novel Section",   "Part 1: August (Chapters 1–9)"],
    ["Skill Focus",     "Character description — appearance, traits, emotional state"],
    ["Standards",       "RL.3.3 · RL.5.3 · RL.6.3"],
    ["Partner Mode",    "Mode 2 during reading · Mode 1 for the activity"],
    ["Materials",       "Wonder · Character description board · Drawing paper or digital canvas"],
  ],
  col2(0.28, 0.72)
));

children.push(T.spacer());
children.push(h2k("Activity Overview"));
children.push(T.p(
  "Describe to Draw is the core activity for Part 1. " +
  "The student builds a description of the main character using vocabulary from their AAC system and the character description board. " +
  "That description is then used to instruct a partner — or the student themselves — to draw the character. " +
  "The drawing becomes evidence of comprehension through generation: the student demonstrated what they understood by describing it precisely enough to create a visual representation."
));
children.push(T.callout(
  "This is not a workaround. Describe to Draw is comprehension demonstrated through generation — the highest-level evidence of understanding. " +
  "A student who builds an accurate character description has met the standard."
));

children.push(h2k("Step-by-Step: Describe to Draw"));
children.push(...T.bulletList([
  "Read Part 1: August (Chapters 1–9) in shared reading — partner in Mode 2. Note spontaneous communication about the character during reading.",
  "After reading Part 1, transition to Mode 1 for the activity.",
  "Present the Character Description Board. Tell the student: We are going to describe this character so well that someone could draw him.",
  "Move through the description categories in order: What does he look like? What does he do? How does he feel? What does he want?",
  "Record each piece of the description as the student indicates it (symbol, gesture, verbal, gaze). Build the written description in the student's words.",
  "Use the description to instruct a drawing. The partner draws what the student described. Do NOT draw a pre-made image of Auggie — the drawing must come from the description.",
  "Review: Does the drawing match? Did the description work? What would you add?",
]));

children.push(h2k("Response Pathways"));
children.push(T.makeTable(
  ["Pathway", "How Student Responds", "What It Looks Like"],
  [
    ["Symbolic / AAC",           "Selects symbols on device, board, or gaze display", "Student selects: 'small' + 'boy' + 'face looks different' + 'scared'"],
    ["Verbal / Gestural",        "Points, nods, gestures, or uses partner-confirmed verbal", "Student points to images on description board; partner records"],
    ["Generative / Constructive","Arranges symbols, completes sentence frames, adds to a list", "'He is ___ and ___. He feels ___ because ___.'" ],
  ],
  col3(0.24, 0.38, 0.38)
));
children.push(T.tableCaption("All three pathways lead to the same evidence: a description the student built. Never close off pathways mid-activity."));

children.push(h2k("Discussion Prompts for Part 1 (Description-First)"));
children.push(T.makeTable(
  ["Do not lead with", "Lead with instead"],
  [
    ["Who is the main character?",                       "Describe the person this story is mostly about. What do you know about him?"],
    ["What is his name?",                                "What does he look like? What does he do? How does he feel?"],
    ["Why does Auggie feel nervous?",                    "Find the person who feels scared. What is happening to him? Why might he feel scared?"],
    ["Who does Auggie want to be friends with?",         "This person wants something. What does he want? How do you know?"],
  ],
  col2(0.42, 0.58)
));

// ═══════════════════════════════════════════════════════════════════════
// SECTION 8 — PART 2: CHARACTER COMPARISON
// ═══════════════════════════════════════════════════════════════════════

children.push(T.heading1("Part 2: Character Comparison"));
children.push(T.teacherRefLabel());

children.push(T.makeTable(
  ["Element", "Detail"],
  [
    ["Novel Section",  "Parts 2–3: Via + Jack (Chapters 10–29)"],
    ["Skill Focus",    "Compare and contrast two characters — perspective, traits, relationship to Auggie"],
    ["Standards",      "RL.5.3 · RL.6.3 · RL.7.3"],
    ["Partner Mode",   "Mode 2 during reading · Mode 1 for activity"],
    ["Materials",      "Wonder · Comparison boards (AAC-accessible 2-column structure)"],
  ],
  col2(0.28, 0.72)
));

children.push(T.spacer());
children.push(h2k("Activity Overview"));
children.push(T.p(
  "Parts 2 and 3 of Wonder shift the narrator. Via tells her story. Jack tells his. " +
  "Each character has a relationship with the main character (Auggie) that looks different from the inside than it did from the outside. " +
  "This part of the unit uses a symbol-supported comparison structure — two character boards side by side — " +
  "to examine how Via and Jack are similar, how they are different, and how each of them feels about the same events."
));

children.push(h2k("Key Questions for Part 2"));
children.push(T.makeTable(
  ["Question", "Response Scaffold"],
  [
    ["How does this character feel about the main character?",                                    "Select: loves / protects / worries about / feels jealous of / is loyal to"],
    ["What does this character want that the main character doesn't know about?",                 "Sentence frame: 'She/He wants ___ but the main character doesn't know.'"],
    ["What does this character do that is kind? What do they do that is hard?",                  "Two-column sort: Kind / Hard"],
    ["How does seeing from this character's point of view change what you know?",                 "'I learned ___ that I didn't know before.'"],
  ],
  col2(0.5, 0.5)
));

children.push(h2k("Comparison Structure (Use for any two characters)"));
children.push(T.makeTable(
  ["", "Character A (describe, don't name)", "Both", "Character B (describe, don't name)"],
  [
    ["Looks like",   "", "", ""],
    ["Acts like",    "", "", ""],
    ["Feels",        "", "", ""],
    ["Wants",        "", "", ""],
    ["Relationship", "", "", ""],
  ],
  col4(0.16, 0.34, 0.16, 0.34)
));
children.push(T.tableCaption("Students complete using any access method: symbol selection, gesture + partner record, verbal, or writing. Character names go in the header ONLY after descriptions are established."));

// ═══════════════════════════════════════════════════════════════════════
// SECTION 9 — PART 3: CHARACTER MOTIVATION
// ═══════════════════════════════════════════════════════════════════════

children.push(T.heading1("Part 3: Character Motivation — Why Do They Act That Way?"));
children.push(T.teacherRefLabel());

children.push(T.makeTable(
  ["Element", "Detail"],
  [
    ["Novel Section",  "Parts 4–5: Julian + Others (Chapters 30–45)"],
    ["Skill Focus",    "Inferencing — character motivation, unstated feelings, cause and effect"],
    ["Standards",      "RL.6.3 · RL.7.3 (motivation and interaction)"],
    ["Partner Mode",   "Mode 2 during reading · Mode 1 for activity"],
    ["Key vocabulary", "because · maybe · probably · choose · want · feel · know"],
  ],
  col2(0.28, 0.72)
));

children.push(T.spacer());
children.push(T.p(
  "Parts 4 and 5 of Wonder give voice to the student who has been unkind — Julian — " +
  "and to Miranda, who has her own complicated relationship with Via and identity. " +
  "These sections shift the unit's skill focus from description to motivation: " +
  "Why does a person act the way they do? What do they feel inside that doesn't match what they show outside?"
));

children.push(h2k("Motivation Scaffold: Because / Maybe / Probably"));
children.push(T.p(
  "The three most powerful inferencing words in fiction are because, maybe, and probably. " +
  "They are core vocabulary words on most AAC devices. " +
  "This scaffold teaches students to use them as reasoning connectors, not just transition words."
));
children.push(T.makeTable(
  ["Sentence Frame", "Example", "Response Access"],
  [
    ["This character acts mean because ___.",              "'...because he is scared of being different too.'",       "Symbol + core vocab combo"],
    ["Maybe this character feels ___ on the inside.",      "'Maybe he feels alone.'",                                 "Select from emotion board"],
    ["This character probably chose to do that because ___.", "'...probably because he wanted to feel powerful.'",   "Generative frame"],
    ["I think this character really wants ___.",           "'I think he really wants to belong.'",                    "Core vocab: want + fringe: belong"],
  ],
  col3(0.40, 0.38, 0.22)
));

children.push(h2k("Key Motivation Questions for Parts 4–5"));
children.push(...T.bulletList([
  "Find the student who is unkind to the main character. Why might he act that way? What might he be feeling on the inside?",
  "This character seems confident. Do you think he is? What evidence shows how he might really feel?",
  "Why does this person stop being kind? What changed for them?",
  "What does this character want that they are not saying out loud?",
]));

// ═══════════════════════════════════════════════════════════════════════
// SECTION 10 — PART 4: CHARACTER CHANGE
// ═══════════════════════════════════════════════════════════════════════

children.push(T.heading1("Part 4: Character Change — Before and After"));
children.push(T.teacherRefLabel());

children.push(T.makeTable(
  ["Element", "Detail"],
  [
    ["Novel Section",  "Part 6: August (Chapters 46–52) + Epilogue"],
    ["Skill Focus",    "Character change — how a character transforms across the arc of the whole story"],
    ["Standards",      "RL.6.3 (responds or changes) · RL.7.3 (how elements interact)"],
    ["Materials",      "Before/After story strip · Core vocabulary"],
  ],
  col2(0.28, 0.72)
));

children.push(T.spacer());
children.push(T.p(
  "The final section of Wonder returns to Auggie's voice. " +
  "By the end of the book, something has shifted — for Auggie, for Jack, even for Julian. " +
  "Character change is a key component of RL.6.3 and the capstone skill of this unit."
));

children.push(h2k("Before/After Strip: Character Change Evidence"));
children.push(T.makeTable(
  ["", "At the Beginning", "Something Changes When...", "At the End"],
  [
    ["How they feel",            "", "", ""],
    ["What they want",           "", "", ""],
    ["How others see them",      "", "", ""],
    ["What they do",             "", "", ""],
    ["What we know about them",  "", "", ""],
  ],
  col4(0.22, 0.26, 0.26, 0.26)
));
children.push(T.tableCaption("Students complete one row per character being tracked. Can be done for Auggie, Jack, or Julian depending on grade and standard focus."));

children.push(h2k("Change Discussion Prompts"));
children.push(...T.bulletList([
  "How is this character different at the end of the story from how they were at the beginning?",
  "What happened that made them change? Was it one thing or many things?",
  "Did the character choose to change, or did something force them to change?",
  "Is the change good? How do you know?",
  "Is there anything about this character that did NOT change?",
]));

// ═══════════════════════════════════════════════════════════════════════
// SECTION 11 — PART 5: WHOLE-BOOK SYNTHESIS
// ═══════════════════════════════════════════════════════════════════════

children.push(T.heading1("Part 5: Whole-Book Synthesis — Theme Through Character"));
children.push(T.teacherRefLabel());

children.push(T.makeTable(
  ["Element", "Detail"],
  [
    ["Novel Section",    "Full book — synthesis activity"],
    ["Skill Focus",      "Connecting character journey to theme — what the story teaches"],
    ["Standards",        "RL.3.2 · RL.5.2 · RL.6.2 · RL.7.2 (theme) + character standards"],
    ["Format",           "Write-Ables — sentence frame + core vocabulary construction"],
    ["Response Access",  "All three pathways: symbol, verbal, generative"],
  ],
  col2(0.28, 0.72)
));

children.push(T.spacer());
children.push(h2k("Write-Ables Frames: Theme Through Character"));
children.push(T.p(
  "Write-Ables are generative sentence frames that use core vocabulary as the construction material. " +
  "Students build a response by selecting or indicating the words that complete each frame. " +
  "The frame structure reduces cognitive load while maintaining the expectation of a constructed, evidence-based response."
));

children.push(T.makeTable(
  ["Frame", "Core Words Available", "Sample Completed Response"],
  [
    ["The main character changes because ___.",
     "feel · want · choose · brave · kind · different · belong",
     "'The main character changes because he learns that he belongs.'"],
    ["The character who is unkind acts that way because ___.",
     "scared · want · feel · know · different · alone",
     "'The character who is unkind acts that way because he is scared of being different.'"],
    ["The most important thing this story teaches is ___.",
     "kind · choose · see · belong · together · inside · real",
     "'The most important thing this story teaches is to choose kind.'"],
    ["I think the character who is bravest is the one who ___.",
     "choose · help · friend · sit · see · different · kind · belong",
     "'I think the character who is bravest is the one who sat with the main character at lunch.'"],
  ],
  col3(0.35, 0.32, 0.33)
));

children.push(h2k("Alternative Response: Symbol Sort for Theme"));
children.push(T.p(
  "For students who need a more structured response option, provide a symbol sort: " +
  "Give the student 6–8 symbols representing ideas from the book (kind, belong, different, choose, invisible, brave, together, see). " +
  "Ask: Which ones are what this story is really about? Sort into: Yes, the story is about this / No, the story is not about this / Maybe. " +
  "The student's sort is their evidence-based response about theme."
));

// ═══════════════════════════════════════════════════════════════════════
// SECTION 12 — IEP GOALS + DATA COLLECTION
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

children.push(h2k("Academic Goal Stems — Character Analysis (RL)"));
children.push(T.makeTable(
  ["Standard", "Goal Stem"],
  [
    ["RL.3.3",
     "Given Wonder by R.J. Palacio read aloud by a partner and a character description board, [student] will describe a character's traits or actions using descriptive vocabulary as measured by rubric scoring on Part 1 and Part 2 response activities, achieving a score of Approaching or Meets on 4 of 5 trials across 3 consecutive sessions by [IEP date]."],
    ["RL.5.3",
     "Given Wonder by R.J. Palacio read aloud by a partner and a visual comparison structure, [student] will identify at least two similarities and two differences between two characters, citing evidence from the text as measured by rubric scoring on Part 2 (Character Comparison) activities, achieving correct comparison with evidence on 3 of 4 trials across 2 consecutive sessions by [IEP date]."],
    ["RL.6.3",
     "Given Wonder by R.J. Palacio read aloud by a partner and a character change graphic organizer, [student] will describe how a character responds or changes as the plot moves toward resolution using core and fringe vocabulary as measured by rubric scoring on Part 4 (Character Change) activities, achieving a complete before/after arc with evidence on 4 of 5 trials across 3 consecutive sessions by [IEP date]."],
    ["RL.7.3",
     "Given Wonder by R.J. Palacio read aloud by a partner and inference scaffolds (because / maybe / probably), [student] will explain a character's motivation for an action using a sentence frame and cited text evidence as measured by rubric scoring on Part 3 (Character Motivation) activities, achieving claim + motivation with evidence on 4 of 5 trials across 3 consecutive sessions by [IEP date]."],
  ],
  col2(0.10, 0.90)
));
children.push(T.tableCaption("Select the standard anchor that matches the student's IEP and grade placement. Adjust condition (access method), criterion (from baseline data), and date to match the individual student."));

children.push(T.spacer());
children.push(h2k("AAC Communication Goal Stem — Character Analysis Context"));
children.push(T.p(
  "This goal targets communication development within the Wonder unit context — separate from the academic ELA skill. " +
  "Data is collected on the Communication Session Tracker by the paraprofessional, not on the academic rubric."
));
children.push(T.makeTable(
  ["Goal Type", "Goal Stem"],
  [
    ["Multi-symbol utterance",
     "Given Wonder by R.J. Palacio shared reading with a communication partner using Aided Language Stimulation, [student] will produce a 2+ symbol utterance in response to comprehension prompts about character as measured by Communication Session Tracker data, achieving 4 of 5 response opportunities across 2 consecutive sessions with 2 different partners by [IEP date]."],
    ["Fringe vocabulary use in context",
     "Given Wonder by R.J. Palacio unit with pre-programmed character vocabulary and partner Aided Language Stimulation, [student] will use at least one pre-programmed fringe vocabulary word (e.g., different, belong, brave, change) in a contextually appropriate response during a character activity as measured by Communication Session Tracker data, achieving 4 of 5 opportunities across 2 consecutive sessions by [IEP date]."],
  ],
  col2(0.22, 0.78)
));
children.push(T.tableCaption(
  "Academic progress ≠ communication progress. Both are reportable at IEP review. A student can meet the rubric criterion using a sentence frame and still be building toward spontaneous AAC output — track both. " +
  "Generalization criterion: 2+ different partners. AAC skills that only appear with one partner have not generalized."
));

children.push(T.spacer());
children.push(h2k("Data Collection Guidance"));
children.push(T.p(
  "Collect data during Mode 1 activities only (Parts 1–5 of this unit). Do not collect data during shared reading in Mode 2. " +
  "Record the student's response, the prompt level used, and whether the response was independent, prompted, or modeled. " +
  "Non-response is data — record the prompt level reached and the environmental factors (vocabulary available? activity set up correctly? correct mode?)."
));
children.push(T.makeTable(
  ["Data Point", "Record", "Why"],
  [
    ["Response type",      "Symbol / gesture / verbal / partner-confirmed / no response", "Shows access method, not just accuracy"],
    ["Prompt level used",  "1 (wait) through 5 (reassess)",                              "Shows instructional level and growth over time"],
    ["Vocabulary access",  "Yes — on device / No — not programmed / Partial — board only", "Critical for AT/AAC team communication"],
    ["Activity condition", "Read aloud / visual board available / sentence frame provided / independent", "Context matters for interpreting data"],
  ],
  col3(0.22, 0.42, 0.36)
));

// ═══════════════════════════════════════════════════════════════════════
// SECTION 13 — COMMUNICATION ACCESS QUICK REFERENCE
// ═══════════════════════════════════════════════════════════════════════

children.push(T.heading1("Communication Access Quick Reference"));
children.push(T.p("Pull out and laminate this page for the partner. This is the one-page summary for anyone working alongside the student during this unit."));

children.push(T.callout(
  "WONDER — Character Analysis | Fiction Anchor Text Unit | Communicate by Design\n" +
  "The text stays the same. The scaffold varies. The expectation does not."
));

children.push(h2k("During Reading: Mode 2"));
children.push(...T.bulletList([
  "Follow the student's lead. Do NOT run prompt hierarchy during the read.",
  "Note spontaneous communication — write it down, do not redirect it.",
  "Model AAC use naturally: 'I think he feels scared.' [Indicate scared on the system.]",
  "No demands. No correct/incorrect. Partnership only.",
]));

children.push(h2k("During Activities: Mode 1"));
children.push(...T.bulletList([
  "Wait 10–15 seconds before prompting.",
  "Start with the least intrusive prompt (gesture toward system).",
  "Accept: symbol, gaze, gesture, pointing, verbal, partner-confirmed — all valid.",
  "Never complete the response for the student.",
  "If no response: Is the vocabulary available? Is this the right mode? Is the environment set up correctly?",
]));

children.push(h2k("Top 10 Vocabulary Words — Confirm Before Starting"));
children.push(T.makeTable(
  ["Word", "Check"],
  [
    ["feel",      "☐ On device / board"],
    ["different", "☐ On device / board"],
    ["belong",    "☐ On device / board"],
    ["brave",     "☐ On device / board"],
    ["kind",      "☐ On device / board"],
    ["because",   "☐ On device / board"],
    ["change",    "☐ On device / board"],
    ["want",      "☐ On device / board"],
    ["maybe",     "☐ On device / board"],
    ["alone",     "☐ On device / board"],
  ],
  col2(0.5, 0.5)
));
children.push(T.tableCaption("If a word is not available, prepare a physical symbol or board card before the activity. Do not skip the pre-check."));

// ═══════════════════════════════════════════════════════════════════════
// END MATTER
// ═══════════════════════════════════════════════════════════════════════

children.push(T.heading1("Accessibility Statement"));
children.push(...T.accessibilityStatement());

children.push(T.heading1("About the Creator"));
children.push(...T.aboutTheCreator());

children.push(T.heading1("Terms of Use"));
children.push(...T.termsOfUse());

// ─────────────────────────────────────────────────────────────────────────
// ASSEMBLE AND WRITE
// ─────────────────────────────────────────────────────────────────────────

const outputPath = path.join(__dirname, "Wonder_Character_Analysis_COMPLETE.docx");

T.assembleAndWrite(
  `${UNIT_TITLE}: ${UNIT_SUBTITLE}`,
  children,
  outputPath,
  {
    title: `Wonder: Character Analysis — Fiction Anchor Text Unit`,
    description: `SDI companion unit for Wonder by R.J. Palacio. Character Analysis · Grades ${GRADE_RANGE} · Communicate by Design`,
  }
);

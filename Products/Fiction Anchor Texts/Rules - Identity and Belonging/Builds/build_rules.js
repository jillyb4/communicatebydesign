#!/usr/bin/env node

/**
 * Rules: Identity and Belonging — Fiction Anchor Text Unit Builder
 * Communicate by Design
 *
 * Novel: Rules by Cynthia Lord (2006)
 * Skill: Character Analysis + Identity & Belonging (RL.4.3 / RL.4.6)
 * Scope: Whole book — grades 4–6
 *
 * Unit question: "What does Rules teaches us about what it means to belong —
 *                 and who gets to decide the rules of belonging?"
 *
 * Text interaction tool: Annotation codes [RULE] / [BELONG] / [CHANGE]
 * 5-Part SDI sequence across the full novel
 *
 * CbD note: This novel features a character who uses AAC (word cards / a
 * communication book) as a central element of the plot. This is a CbD
 * flagship title — the AAC representation is not incidental but central.
 * Activities should honor and deepen that representation, not treat it as
 * a "disability topic." Jason IS a communicator. His access to language
 * is the heart of the book's second storyline.
 *
 * Output: Rules_Identity_and_Belonging_Teaching_Materials.docx
 *
 * Build rule: whole-book scope is STANDARD for all CbD fiction units.
 * Build rule: student worksheet/response pages → cbd_worksheet_templates.py (not this script).
 * Build rule: About, Terms of Use, Accessibility Statement → Welcome PDF only (not this file).
 */

const path = require("path");
const T = require(path.join(__dirname, "..", "..", "..", "..", "_Operations", "Build", "cbd_docx_template"));

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

const UNIT_TITLE    = "Rules";
const UNIT_SUBTITLE = "Identity and Belonging";
const NOVEL_AUTHOR  = "Cynthia Lord";
const SKILL_NAME    = "Character Analysis · Identity and Belonging";
const GRADE_RANGE   = "4–6";
const RL_STANDARDS  = "RL.4.3 · RL.4.6 · RL.5.3";
const PRODUCT_LINE  = "Fiction Anchor Text Unit";

// ─────────────────────────────────────────────────────────────────────────
// AAC ACCESS NOTE CONSTANTS
// ─────────────────────────────────────────────────────────────────────────
const AAC_CORE        = "Core — part of most AAC ecosystems";
const AAC_FRINGE_PREP = "Fringe — SDI target; include in communication packet";

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
    ["Unit Question",      "What does Rules teach us about what it means to belong — and who gets to decide the rules of belonging?"],
    ["Required Materials", "Copy of Rules (not included) · AAC system (any access method) · Communication boards (included)"],
  ],
  col2(0.28, 0.72)
));

children.push(T.spacer());
children.push(h2k("What This Unit Is"));
children.push(T.p(
  "This is a Specially Designed Instruction (SDI) companion unit for the novel Rules by Cynthia Lord. " +
  "The novel is not included — your class or student already has it. What this unit provides is the instructional and communication access layer: " +
  "the teacher guide, AAC-designed activities, vocabulary supports, and response structures that make character analysis and identity exploration accessible " +
  "to students who use alternative and augmentative communication."
));
children.push(T.p(
  "This is not a Lexile differentiation product. The text stays the same. " +
  "The scaffold varies. The expectation does not. " +
  "Every student engages with the same novel, the same skill, and the same standard. " +
  "What differs is how they access vocabulary, how they respond, and how the partner supports participation."
));
children.push(T.p(
  "A note on this particular novel: Rules features a character — Jason — who uses a communication book made of word cards. " +
  "His communication system is not a plot device. It is central to how the novel explores belonging, voice, and what it means to be heard. " +
  "For students who use AAC, this representation is significant. This unit treats Jason as a communicator — " +
  "not as a symbol of disability, not as a lesson about inclusion, but as a full character with perspective, humor, preferences, and something important to say."
));

children.push(h2k("What This Unit Is Not"));
children.push(...T.bulletList([
  "A simplified or rewritten version of the novel",
  "A replacement for general education instruction",
  "An activity pack that only works with high-tech AAC devices",
  "A unit about autism or disability as a topic (Rules is a story about belonging — that theme applies to every student in the room)",
  "A unit that positions disability-related characters as objects of empathy rather than agents with perspective",
]));

children.push(h2k("What's Included"));
children.push(...T.bulletList([
  "Teacher SDI guide with 5-part lesson sequence",
  "Before-reading vocabulary preview with core and fringe word list",
  "Part 1: The Rules — how Catherine's rules reveal what she believes about belonging",
  "Part 2: Meeting Jason — how Jason's communication changes what Catherine (and the reader) understands about belonging",
  "Part 3: Catherine's Rules Start to Break Down — what happens when belonging and honesty conflict",
  "Part 4: What Catherine Learns — her change across the arc of the novel",
  "Part 5: Whole-Book Synthesis — character analysis and identity response using the Belonging Evidence Chart",
  "Belonging Evidence Chart — the primary text interaction tool for this unit",
  "Annotation codes: [RULE] / [BELONG] / [CHANGE]",
  "Communication Access quick-reference card (partner pull-out)",
  "Core and fringe vocabulary table with AAC access notes",
  "IEP goal stems for RL.4.3 and RL.4.6 / RL.5.3",
  "Data collection guidance",
]));

// ═══════════════════════════════════════════════════════════════════════
// SECTION 2 — RESEARCH BASE
// ═══════════════════════════════════════════════════════════════════════

children.push(T.heading1("Research Base"));
children.push(T.teacherRefLabel());

children.push(h2k("Why Character Analysis and Identity Are the Right Skills for Rules"));
children.push(T.p(
  "Rules is structured around two parallel character arcs: Catherine, who creates rules to manage the unpredictability of her life, " +
  "and Jason, who uses a communication book to connect across the assumption that he cannot. " +
  "The novel asks its readers to notice how characters understand belonging — what they think the rules of belonging are, " +
  "and what happens when those rules turn out to be incomplete."
));
children.push(T.p(
  "For students who use AAC, this novel offers something most fiction does not: a central character who communicates using a system like theirs. " +
  "Jason's communication book is not treated as a deficit. It is how he participates, builds relationships, and makes his perspective known. " +
  "The character analysis skill this unit targets — how characters respond to challenges, how they change, how they understand themselves — " +
  "is the same skill for every student in the room, and it is easier to access in a novel where a character already knows what it is like " +
  "to not be heard the way you want to be heard."
));

children.push(h2k("Story Grammar Instruction as SDI Evidence"));
children.push(T.p(
  "Story grammar instruction (Spencer & Petersen, 2020) is the primary evidence-based framework for narrative SDI. " +
  "Character analysis is a core story grammar element — students identify traits, motivations, relationships, and change over time. " +
  "Research shows statistically significant improvements in comprehension and story-structure knowledge for students with and without disabilities " +
  "when explicit narrative structure instruction is provided (ERIC EJ871908). " +
  "Teaching character through story grammar scaffolding is literacy instruction, not a support activity."
));

children.push(h2k("Description-First Activity Design"));
children.push(T.p(
  "Fiction activities designed for complex communicators must lead with description, action, and attribute — not name recall. " +
  "A student who cannot indicate 'Catherine' may absolutely be able to indicate: " +
  "the girl who makes the rules, the one who feels embarrassed, who wants everything to be normal, who changes by the end. " +
  "Every activity in this unit is built to meet students where their vocabulary is — description is the access point, not the workaround."
));

children.push(h2k("AAC Representation in Fiction — Why It Matters for Instruction"));
children.push(T.p(
  "Research on disability representation in children's literature (Dyches & Prater, 2005; Wopperer, 2011) consistently shows that " +
  "when characters with disabilities are portrayed as full agents — with preferences, humor, opinions, and relationships — " +
  "readers are more likely to engage with complex characterization. " +
  "Jason's communication book in Rules creates a natural entry point for every student to understand that communication happens in many forms — " +
  "and that what someone has to say matters more than how they say it."
));
children.push(T.callout(
  "Jason uses a communication book. That is his AAC system. " +
  "This unit does not treat Jason's system as a plot device or a lesson about disability. " +
  "It treats his communication as communication — and Catherine's response to it as the character evidence the unit targets."
));

children.push(h2k("UDL 3.0 and HLP Alignment"));
children.push(T.p(
  "This unit is designed to CAST Universal Design for Learning Guidelines 3.0 (CAST, 2024). " +
  "Every activity implements multiple means of action and expression (UDL Guideline 4.1: vary and honor all response methods; Guideline 4.2: optimize access to AT/AAC tools) " +
  "and multiple means of representation (Guideline 2.1: clarify vocabulary and language structures; Guideline 1.3: represent diversity of identities — this unit foregrounds communication diversity as a represented identity). " +
  "Partner guidance embedded at point of use implements Guideline 6.5: challenging the exclusionary practice of expecting AAC users to participate without trained communication partner support."
));
children.push(T.p(
  "CEC High-Leverage Practice alignment: " +
  "HLP 12 (Systematic and explicit instruction — character vocabulary and annotation codes taught explicitly before application); " +
  "HLP 13 (Adapt curriculum tasks and materials — Belonging Evidence Chart, communication boards, sentence frames, symbol sorts); " +
  "HLP 14 (Predictive Chart Writing / Write-Ables — group identity construction around key scenes); " +
  "HLP 16 (Use explicit instruction / shared reading — Mode 2 during novel reading is the evidence-based delivery condition for complex communicators)."
));

// ═══════════════════════════════════════════════════════════════════════
// SECTION 3 — NOVEL OVERVIEW
// ═══════════════════════════════════════════════════════════════════════

children.push(T.heading1("Novel Overview: Rules"));
children.push(T.teacherRefLabel());

children.push(T.makeTable(
  ["Element", "Detail"],
  [
    ["Author",             "Cynthia Lord"],
    ["Published",          "2006"],
    ["Genre",              "Realistic Fiction / Middle-Grade"],
    ["Typical Grade Use",  "Grades 4–6"],
    ["Lexile",             "820L"],
    ["Narrator Structure", "First-person — Catherine's perspective throughout"],
    ["Central Theme",      "What it means to belong — and how rules can help or hurt our ability to connect"],
    ["Awards",             "2007 Newbery Honor"],
  ],
  col2(0.28, 0.72)
));

children.push(T.spacer());
children.push(h2k("Summary (for teacher reference)"));
children.push(T.p(
  "Twelve-year-old Catherine spends her summer wishing her life were more normal — that her younger brother David, who has autism, " +
  "did not require so much of her family's attention, and that her new neighbor Kristi would see her as a regular girl, not someone whose brother embarrasses her. " +
  "At the therapy clinic where David receives occupational therapy, Catherine meets Jason, a boy who uses a communication book of word cards. " +
  "Catherine begins making word cards for Jason — adding words he doesn't have, words that are funny or surprising or just his. " +
  "Across the summer, her relationships with David, Jason, and Kristi challenge every rule she has made about how belonging works. " +
  "By the end, Catherine must decide whether belonging means fitting in or being known — and those are not the same thing."
));

children.push(h2k("Key Characters"));
children.push(T.makeTable(
  ["Character", "Description (not name-based)", "Role"],
  [
    ["Catherine", "The twelve-year-old narrator. Makes rules to manage what she cannot control. Wants a normal life. Slowly learns that 'normal' is not the goal.", "Narrator / Protagonist"],
    ["David",     "Catherine's younger brother who has autism. He follows rules carefully and literally. Loves videos and fish and specific, predictable things.", "Supporting / Sibling"],
    ["Jason",     "A boy at the therapy clinic who uses a communication book of word cards. Direct, funny, with strong opinions and a full inner life.", "Supporting / Central relationship"],
    ["Kristi",    "Catherine's new neighbor. The girl Catherine wants to impress. Friendly, uncomplicated — does not know Catherine the way Catherine hopes.", "Supporting / Friend figure"],
    ["Ryan",      "A boy from school who Catherine sees at the clinic. His presence there unsettles Catherine's ideas about who belongs where.", "Supporting"],
  ],
  col3(0.18, 0.55, 0.27)
));
children.push(T.tableCaption("Character names are fringe words. Always pair with a description-first reference when introducing in activities."));

children.push(h2k("Novel Structure: 5-Part Mapping"));
children.push(T.makeTable(
  ["Unit Part", "Novel Focus", "Chapters (approx.)", "Skill Focus"],
  [
    ["Before Reading", "Pre-reading vocabulary and 'rules' overview",       "—",      "Build vocabulary: belong, rule, normal, different, choose, fair, hide"],
    ["Part 1",         "The Rules — Catherine's system for belonging",       "1–5",    "What the rules reveal about what Catherine believes"],
    ["Part 2",         "Meeting Jason — a new kind of belonging",            "6–12",   "How Jason's communication challenges Catherine's rules"],
    ["Part 3",         "When the Rules Break Down",                          "13–19",  "What happens when belonging and honesty conflict"],
    ["Part 4",         "What Catherine Learns",                              "20–end", "How Catherine changes — and what she understands about belonging"],
    ["Part 5",         "Whole-Book Synthesis",                               "Full book", "Character analysis: What does Rules teach about belonging?"],
  ],
  col4(0.15, 0.28, 0.17, 0.40)
));

// ═══════════════════════════════════════════════════════════════════════
// SECTION 4 — TARGETED STANDARD
// ═══════════════════════════════════════════════════════════════════════

children.push(T.heading1("Targeted Standard: Character Analysis · Identity and Belonging"));
children.push(T.teacherRefLabel());

children.push(h2k("Standard Statements"));
children.push(T.makeTable(
  ["Grade", "Standard", "Statement"],
  [
    ["4", "RL.4.3", "Describe in depth a character, setting, or event in a story or drama, drawing on specific details in the text (e.g., a character's thoughts, words, or actions)."],
    ["4", "RL.4.6", "Compare and contrast the point of view from which different stories are narrated, including the difference between first- and third-person narrations."],
    ["5", "RL.5.3", "Compare and contrast two or more characters, settings, or events in a story or drama, drawing on specific details in the text (e.g., how characters interact)."],
  ],
  col3(0.07, 0.13, 0.80)
));
children.push(T.tableCaption(
  "Select the standard anchor that matches the student's IEP and grade placement. " +
  "All activities address the same character analysis skill at varying response complexity. " +
  "RL.4.3 is the entry standard for students building toward deeper character description. " +
  "RL.4.6 extends to Catherine's point of view as narrator — and what she cannot see. " +
  "RL.5.3 targets character comparison: Catherine vs. Jason, Catherine vs. David, or Catherine at start vs. end."
));

children.push(T.spacer());
children.push(h2k("Learning Target"));
children.push(T.p(
  "I can describe Catherine's character — what she believes, how she acts, and how she changes — " +
  "using specific details from the novel to explain how her ideas about belonging shift across the story."
));
children.push(T.tableCaption("This learning target applies to every student in the room. The access layer varies. The expectation does not."));

children.push(T.makeTable(
  ["Standard", "Grade-Level Anchor"],
  [
    ["RL.4.3", "I can describe what Catherine is like using specific details about her thoughts, words, and actions."],
    ["RL.4.6", "I can explain how Catherine's point of view as narrator shapes what we know — and what she cannot see clearly about herself."],
    ["RL.5.3", "I can compare Catherine and Jason, explaining how their different ways of seeing belonging shape how they interact throughout the novel."],
  ],
  col2(0.18, 0.82)
));

children.push(T.spacer());
children.push(h2k("Annotation Codes for This Unit (LOCKED)"));
children.push(T.p(
  "Rules uses three annotation codes. Each maps to one body paragraph of the final character analysis response " +
  "AND to one or more parts of the SDI sequence. Codes are single words for AAC accessibility."
));
children.push(T.makeTable(
  ["Code", "What It Marks", "SDI Part", "Body Paragraph"],
  [
    ["[RULE]",   "Evidence of what Catherine believes about belonging — her rules, her thinking, her judgment of others", "Part 1 + Part 3",     "P1: What Catherine Believes"],
    ["[BELONG]", "Evidence of how belonging happens — or doesn't — for Catherine, Jason, or David",                      "Part 2 + Part 3",     "P2: What Belonging Looks Like"],
    ["[CHANGE]", "Evidence of how Catherine changes — before/after, what she does or says differently",                  "Part 4 + Part 5",     "P3: How Catherine Changes"],
  ],
  col4(0.12, 0.44, 0.22, 0.22)
));
children.push(T.tableCaption(
  "Codes are used during activities — not as margin codes on the published novel. " +
  "Students mark evidence in the Belonging Evidence Chart using these codes. " +
  "By Part 5, each code maps to one paragraph of the synthesis response."
));

children.push(T.spacer());
children.push(h2k("What Character Analysis Requires in Rules"));
children.push(...T.bulletList([
  "Identifying what Catherine believes about belonging — and where those beliefs come from",
  "Recognizing specific details in her thoughts, words, and actions that reveal her character",
  "Noticing how her rules function — as protection, as control, and as barriers",
  "Tracking how Catherine's understanding of belonging changes across the novel",
  "Comparing how different characters (Catherine, Jason, David) experience belonging differently",
  "Using evidence from the text to support a character analysis statement",
]));

// ═══════════════════════════════════════════════════════════════════════
// SECTION 5 — COMMUNICATION ACCESS
// ═══════════════════════════════════════════════════════════════════════

children.push(T.heading1("Communication Access"));
children.push(T.teacherRefLabel());

children.push(h2k("Partner Modes — When to Use Each"));
children.push(T.makeTable(
  ["Mode", "When", "What the Partner Does", "What the Partner Does NOT Do"],
  [
    ["Mode 1 — Instructional", "Focused activities (Belonging Evidence Chart, Parts 1–5)", "Uses prompt hierarchy; collects data; scaffolds toward independence", "Interrupt the student; complete responses; skip wait time"],
    ["Mode 2 — Partnership",   "During shared novel reading",                              "Follows student lead; notes spontaneous communication; models AAC use naturally", "Run prompt hierarchy; make demands; correct responses"],
    ["Mode 3 — Participation", "Performance tasks; group discussion; read-aloud",          "Enables access only (holds book, operates device, manages boards)", "Interpret; speak for student; add communication content"],
  ],
  col4(0.18, 0.18, 0.34, 0.30)
));
children.push(T.tableCaption(
  "Mode 2 during reading is non-negotiable. Running Mode 1 (instructional) during novel reading is the most common partner error in fiction units. " +
  "Note: Because Rules includes Jason's communication book as a plot element, Mode 2 reading may produce more spontaneous communication than usual — " +
  "students who use AAC may comment, react, or initiate. Follow their lead. Record. Do not redirect."
));

children.push(T.spacer());
children.push(h2k("5-Level Prompt Hierarchy (Mode 1 Only)"));
children.push(T.makeTable(
  ["Level", "Prompt Type", "What It Looks Like"],
  [
    ["1", "Wait",         "Pause 10–15 seconds. Character motivation is abstract — students need processing time."],
    ["2", "Indirect Cue", "Gesture toward the AAC system without saying anything. Non-directive."],
    ["3", "Direct Cue",   "Point to the specific symbol, location, or area on the board."],
    ["4", "Verbal Model", "Say the response AND demonstrate it on the student's system."],
    ["5", "Reassess",     "Non-response is data. Ask: Is the vocabulary available? Is the activity set up correctly? Is this the right mode?"],
  ],
  col3(0.07, 0.18, 0.75)
));

children.push(T.spacer());
children.push(h2k("Core and Fringe Vocabulary — Rules: Identity and Belonging"));
children.push(T.p(
  "Fringe vocabulary in fiction is descriptive — words that help readers picture and understand what characters experience: " +
  "appearance, action, emotion, and setting. " +
  "In character analysis, the most important fringe words are words that describe the character's internal experience and the specific world of the novel. " +
  "Character names are always fringe words — specific proper nouns rarely pre-programmed on AAC systems. " +
  "Coordinate with the student's AAC team to confirm fringe vocabulary is available before the unit begins."
));

children.push(T.makeTable(
  ["Word", "★ Core / Fringe", "Why It Matters in Rules", "AAC Access Note"],
  [
    ["belong",     "★ Core", "The central concept of the novel — what every character wants", AAC_CORE],
    ["want",       "★ Core", "What Catherine wants vs. what she does — the gap is the character", AAC_CORE],
    ["feel",       "★ Core", "Catherine's internal emotional life drives every plot decision", AAC_CORE],
    ["think",      "★ Core", "How Catherine reasons about her rules and her relationships", AAC_CORE],
    ["know",       "★ Core", "What Catherine knows vs. what she refuses to know — the tension of the novel", AAC_CORE],
    ["change",     "★ Core", "Catherine's arc across the novel — what she learns to do differently", AAC_CORE],
    ["choose",     "★ Core", "Catherine has to choose between fitting in and being honest", AAC_CORE],
    ["same",       "★ Core", "What Catherine wants her life to be — and what it is not", AAC_CORE],
    ["different",  "★ Core", "How David and Jason are different — and why Catherine is uncomfortable", AAC_CORE],
    ["hide",       "★ Core", "What Catherine does with things she is ashamed of — and what that costs her", AAC_CORE],
    ["fair",       "★ Core", "What Catherine thinks is fair — and what Jason shows her about fairness", AAC_CORE],
    ["because",    "★ Core", "Causal reasoning — essential for character analysis evidence statements", AAC_CORE],
    ["normal",     "Fringe", "What Catherine wants her life to be — the story's central problem word", AAC_FRINGE_PREP],
    ["rule",       "Fringe", "The rules Catherine makes — the central metaphor of the novel", AAC_FRINGE_PREP],
    ["autism",     "Fringe", "David's diagnosis — appears in the novel; use with care and context", AAC_FRINGE_PREP],
    ["clinic",     "Fringe", "The therapy clinic where Catherine meets Jason", AAC_FRINGE_PREP],
    ["word card",  "Fringe", "Jason's communication system — the cards Catherine adds to his book", AAC_FRINGE_PREP],
    ["embarrassed","Fringe", "How Catherine often feels about David in public", AAC_FRINGE_PREP],
    ["honest",     "Fringe", "What Jason requires of Catherine — and what she struggles to give", AAC_FRINGE_PREP],
    ["Catherine",  "Fringe", "The protagonist and narrator — proper noun; description-first before name", AAC_FRINGE_PREP],
    ["Jason",      "Fringe", "The boy at the clinic who uses a communication book", AAC_FRINGE_PREP],
    ["David",      "Fringe", "Catherine's younger brother who has autism", AAC_FRINGE_PREP],
    ["Kristi",     "Fringe", "The new neighbor Catherine wants to impress", AAC_FRINGE_PREP],
  ],
  col4(0.16, 0.16, 0.42, 0.26)
));
children.push(T.tableCaption(
  "★ Core = high-frequency, cross-context words already on most AAC ecosystems. " +
  "Fringe = Rules-specific vocabulary requiring system preparation. " +
  "Coordinate with the student's AAC team before the unit to confirm vocabulary is available."
));

children.push(T.spacer());
children.push(h2k("Top 5 Priority Vocabulary — Confirm First"));
children.push(T.callout(
  "Before any unit activity begins, confirm these 5 words are accessible on the student's system. " +
  "These carry the most weight in character analysis for Rules.\n\n" +
  "  1. belong — the central concept of the novel\n" +
  "  2. rule — what Catherine creates and why (the novel's title and central metaphor)\n" +
  "  3. feel — what Catherine hides and what she finally lets herself feel\n" +
  "  4. change — Catherine's arc across the whole novel\n" +
  "  5. honest — what Jason demands and what Catherine struggles to give"
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
  "The vocabulary below is organized by concept cluster — introduce clusters 1 and 2 before Chapter 1."
));

children.push(h2k("Priority Vocabulary: Belonging and Identity Words"));
children.push(T.callout(
  "Pre-teach these before Chapter 1. These words carry the theme and connect to students' own experience. " +
  "Most are core vocabulary — the goal is to connect familiar words to the specific ideas in this novel."
));
children.push(T.makeTable(
  ["Word", "What It Means in Rules", "How to Pre-Teach It"],
  [
    ["belong",     "To feel like you are part of something — like you fit in and are wanted.", "Ask: Have you ever felt like you belonged somewhere? What made you feel that way? Show me on your board."],
    ["rule",       "A rule tells you what to do or how to act. Catherine makes lots of rules — rules for her brother, rules for herself.", "Name a rule you know. Why does that rule exist? What happens if someone breaks it?"],
    ["normal",     "What people think is regular or expected — the way things are 'supposed to be.' Catherine wants her life to feel normal.", "Ask: What feels normal to you? What feels unusual? Is normal the same for everyone?"],
    ["hide",       "To keep something out of sight — to not let others see it. Catherine hides parts of her life that feel embarrassing.", "Ask: Have you ever hidden something you felt embarrassed about? What made you want to hide it?"],
    ["honest",     "Telling the truth — even when it is hard or uncomfortable.", "Ask: When is it hard to be honest? Is it always the right thing to do, even when it is uncomfortable?"],
  ],
  col3(0.12, 0.44, 0.44)
));

children.push(T.spacer());
children.push(h2k("Jason's Communication Book — Before Reading"));
children.push(T.p(
  "Before students encounter Jason in the novel, introduce the idea of a communication book as a communication system. " +
  "Do not treat this as a 'disability lesson' — treat it as background knowledge about one character's way of communicating."
));
children.push(T.makeTable(
  ["About Jason's Communication Book", "How It Works in the Novel"],
  [
    ["A book of word cards — printed words that he selects to communicate", "Catherine adds new words to his book across the story"],
    ["He uses it the way any communicator uses language — to ask, to comment, to joke, to have opinions", "He chooses words that are specific and sometimes surprising"],
    ["Some words he has. Some words he does not have yet.", "The words that are missing are a problem — and Catherine tries to solve it"],
    ["His communication is complete, even when it is not what others expect", "What he says with his cards matters — even when others are not ready to hear it"],
  ],
  col2(0.45, 0.55)
));
children.push(T.tableCaption(
  "This table is a teacher reference. Use it to frame Jason before students meet him in the novel. " +
  "For students who use AAC: this is an opportunity to name what they already know from the inside."
));

// ═══════════════════════════════════════════════════════════════════════
// SECTION 7 — THE BELONGING EVIDENCE CHART
// ═══════════════════════════════════════════════════════════════════════

children.push(T.heading1("The Belonging Evidence Chart — Your Primary Text Interaction Tool"));
children.push(T.teacherRefLabel());

children.push(T.p(
  "The Belonging Evidence Chart is how students collect evidence across the whole novel and build toward a character analysis response. " +
  "Like The Giver's Theme Evidence Chart, this tool allows students to capture evidence as they read — one part at a time — " +
  "so that by Part 5 (Synthesis), the evidence is already organized. " +
  "Students complete the chart using any access method."
));

children.push(T.callout(
  "The Belonging Evidence Chart is pre-writing scaffolding. Students who complete it across all five parts are building their character analysis while they read — " +
  "one piece of evidence at a time. By Part 5, the chart is already their outline. The reading was the thinking."
));

children.push(h2k("How to Use the Chart"));
children.push(...T.bulletList([
  "Introduce the chart before Part 1. Tell students: This is where we collect evidence about Catherine across the whole book.",
  "At the end of each Part activity, students add one row: what Catherine did or thought, what code it gets, and what it reveals about belonging.",
  "Students complete the chart using any access method: symbol selection, gesture + partner record, verbal, or writing.",
  "The chart does not require writing. A student who indicates three symbols per row is completing the chart.",
  "By Part 5, the chart has 4–5 rows — enough evidence to write or construct a character analysis response.",
]));

children.push(h2k("Belonging Evidence Chart Template"));
children.push(T.makeTable(
  ["Part", "What Catherine Does or Thinks", "Code", "What This Reveals About Belonging"],
  [
    ["Part 1 — The Rules",             "(students complete)", "[RULE]",   "(students complete)"],
    ["Part 2 — Meeting Jason",         "(students complete)", "[BELONG]", "(students complete)"],
    ["Part 3 — Rules Break Down",      "(students complete)", "[BELONG]", "(students complete)"],
    ["Part 4 — What Catherine Learns", "(students complete)", "[CHANGE]", "(students complete)"],
  ],
  col4(0.18, 0.30, 0.12, 0.40)
));
children.push(T.tableCaption(
  "Students complete one row per Part using any access method. " +
  "Column 3 (Code) uses annotation codes [RULE] / [BELONG] / [CHANGE]. " +
  "Column 4 (What This Reveals) is the character analysis column — the most supported, highest-level thinking."
));

children.push(h2k("Sentence Frames for Column 4 (Character Analysis)"));
children.push(T.makeTable(
  ["Frame", "Example Response"],
  [
    ["This shows that Catherine believes ___.",                              "'This shows that Catherine believes belonging means acting normal.'"],
    ["Catherine does ___ because she is afraid of ___.",                    "'Catherine does this because she is afraid of being embarrassed.'"],
    ["This reveals that belonging, for Catherine, means ___.",              "'This reveals that belonging, for Catherine, means fitting in without drawing attention.'"],
    ["By the end, Catherine understands that belonging means ___ not ___.", "'By the end, Catherine understands that belonging means being known, not just fitting in.'"],
  ],
  col2(0.55, 0.45)
));
children.push(T.tableCaption("These frames use core vocabulary — belong, feel, choose, know, because, change. Students who cannot write can select the key words and a partner records the frame."));

// ═══════════════════════════════════════════════════════════════════════
// SECTION 8 — PART 1: THE RULES
// ═══════════════════════════════════════════════════════════════════════

children.push(T.heading1("Part 1: The Rules"));
children.push(T.teacherRefLabel());

children.push(T.makeTable(
  ["Element", "Detail"],
  [
    ["Novel Section",  "Chapters 1–5 — Catherine's world and the rules she has made"],
    ["Skill Focus",    "What the rules reveal about what Catherine believes about belonging"],
    ["Standards",      "RL.4.3 (describe character using details) · RL.4.6 (first-person narrator limitations)"],
    ["Annotation Code","[RULE]"],
    ["Partner Mode",   "Mode 2 during reading · Mode 1 for activity"],
    ["Materials",      "Rules · Belonging Evidence Chart · Character Description Board"],
  ],
  col2(0.28, 0.72)
));

children.push(T.spacer());
children.push(h2k("Activity Overview"));
children.push(T.p(
  "The novel opens with Catherine's rules — a list of things she has decided are important for living with David and fitting into the world around her. " +
  "These rules are not arbitrary. They reveal what Catherine believes: that belonging is something you earn by following the right behaviors, " +
  "that difference is a problem to be managed, and that normal is the goal worth protecting. " +
  "Part 1 asks students to look at the rules closely: What is Catherine afraid of? What does she think belonging requires?"
));
children.push(T.callout(
  "The key move in Part 1 is reading the rules as character evidence — not as a list of dos and don'ts, but as a window into what Catherine believes about herself and others. " +
  "Students who cannot access complex analysis can still respond to: What does Catherine want? What is she afraid of? What would break a rule?"
));

children.push(h2k("Catherine's Rules — Character Evidence Sort"));
children.push(T.p(
  "Present students with examples of Catherine's rules from the novel. " +
  "Students sort them: What does this rule protect? What does it assume about belonging?"
));
children.push(T.makeTable(
  ["Catherine's Rule (examples)", "What This Rule Protects", "What This Rule Assumes About Belonging"],
  [
    ["'No toys in the fish tank.'",                           "", ""],
    ["'A boy can take his shirt off outside but not inside.'","", ""],
    ["'Grownups go first.'",                                  "", ""],
    ["'Don't stand in front of the TV when others are watching.'", "", ""],
  ],
  col3(0.35, 0.33, 0.32)
));
children.push(T.tableCaption("Students complete using symbol selection, pointing, partner-confirmed verbal, or writing. The goal is to notice that rules = beliefs about belonging."));

children.push(h2k("Key Questions for Part 1"));
children.push(T.makeTable(
  ["Question", "Response Scaffold"],
  [
    ["Why does Catherine make so many rules?",                        "Select from: she wants to help David / she wants things to be normal / she is worried about what people think / she is trying to stay in control"],
    ["What does Catherine want her life to be like?",                 "Sentence frame: 'Catherine wants her life to be ___.'" ],
    ["What is Catherine most afraid of?",                             "Select from: being embarrassed / people staring / David acting different in public / not fitting in / losing Kristi as a friend"],
    ["Who are the rules really for — David or Catherine?",            "Both / more for David / more for Catherine / I'm not sure — explain."],
    ["What does this tell us about what Catherine thinks 'belonging' means?", "Sentence frame: 'I think Catherine believes belonging means ___.'" ],
  ],
  col2(0.44, 0.56)
));

children.push(h2k("Partner Guidance — Part 1"));
children.push(T.callout(
  "Wait time: Give 10–15 seconds before prompting. Character motivation requires time to process.\n\n" +
  "Model AAC use naturally during reading: 'Catherine made another rule. I wonder why. I think she feels worried when things are unpredictable.' [Indicate feel + worried on system.]\n\n" +
  "If a student cannot access the sort independently: present two options at a time. 'Does this rule help Catherine feel safe, or does it help David know what to do?' Accept any indication as a response.\n\n" +
  "Note: Some students may have strong feelings about rules — particularly students whose own behaviors have been rule-managed by adults. Honor that experience without derailing the activity."
));

children.push(h2k("Belonging Evidence Chart — Row 1 (complete at end of Part 1)"));
children.push(T.makeTable(
  ["Column", "Prompt to Student", "Example Response"],
  [
    ["What Catherine Does",      "What does Catherine do in these chapters that shows what she believes?", "'She makes rules for David to follow everywhere they go.'"],
    ["Code",                     "What code fits?",                                                        "[RULE]"],
    ["What It Reveals",          "What does this tell us about what Catherine thinks belonging means?",    "'Catherine thinks belonging means acting normal and not standing out.'"],
  ],
  col3(0.22, 0.10, 0.68)
));

// ═══════════════════════════════════════════════════════════════════════
// SECTION 9 — PART 2: MEETING JASON
// ═══════════════════════════════════════════════════════════════════════

children.push(T.heading1("Part 2: Meeting Jason"));
children.push(T.teacherRefLabel());

children.push(T.makeTable(
  ["Element", "Detail"],
  [
    ["Novel Section",  "Chapters 6–12 — Catherine meets Jason at the clinic; begins making word cards"],
    ["Skill Focus",    "How Jason's communication challenges and expands Catherine's ideas about belonging"],
    ["Standards",      "RL.4.3 · RL.4.6 (how narrator's limited perspective affects what we see)"],
    ["Annotation Code","[BELONG]"],
    ["Partner Mode",   "Mode 2 during reading · Mode 1 for activity"],
    ["Key vocabulary", "word card · honest · choose · belong · different · fair"],
  ],
  col2(0.28, 0.72)
));

children.push(T.spacer());
children.push(h2k("Activity Overview"));
children.push(T.p(
  "Catherine meets Jason in the waiting area at David's therapy clinic. He uses a communication book of word cards. " +
  "At first, Catherine relates to him mostly as someone to feel sorry for — or someone whose difference makes her uncomfortable. " +
  "But Jason has opinions. He is funny. He knows what he wants to say and chooses his words carefully. " +
  "Part 2 asks students to pay attention to what Jason communicates — not just how — " +
  "and to notice what changes in Catherine when she starts actually listening."
));
children.push(T.callout(
  "The key move in Part 2 is recognizing Jason as a full communicator — not as a character who needs to be pitied or fixed. " +
  "Catherine's job (and ours as readers) is to listen. What is he actually saying? What does he want? " +
  "Students who use AAC may have particularly clear insight here. Honor that."
));

children.push(h2k("What Jason Communicates — Evidence Chart"));
children.push(T.makeTable(
  ["Scene / Moment", "What Jason Communicates", "How Catherine Responds"],
  [
    ["Jason selects words from his book for the first time", "", ""],
    ["Jason asks for a word that is missing",                "", ""],
    ["Jason chooses a word that surprises Catherine",         "", ""],
    ["Jason says something Catherine does not want to hear",  "", ""],
  ],
  col3(0.32, 0.34, 0.34)
));
children.push(T.tableCaption("Students complete using any access method. Column 3 (How Catherine Responds) is the character analysis column — her response reveals what she believes about belonging."));

children.push(h2k("Key Questions for Part 2"));
children.push(T.makeTable(
  ["Question", "Response Scaffold"],
  [
    ["What is Jason trying to tell Catherine with his word cards?",           "Select from: what he wants / how he feels / what he thinks is funny / what he needs / what is unfair"],
    ["What word does Catherine add to Jason's book? Why?",                    "She adds ___. She adds it because ___."],
    ["What does Jason communicate that surprises Catherine?",                  "Describe to Draw: What kind of person would say this? What does this tell us about him?"],
    ["How does Catherine feel when she listens to Jason?",                     "Emotion board — indicate the feeling. Sentence frame: 'Catherine feels ___ because ___.'" ],
    ["What does Jason's communication show us about belonging?",               "Sentence frame: 'Jason shows that belonging means ___ — not just ___.'" ],
  ],
  col2(0.44, 0.56)
));

children.push(h2k("Describe to Draw — Jason"));
children.push(T.p(
  "Lead students through a 'Describe to Draw' activity for Jason. " +
  "Using the Character Description Board, students build a description of Jason using attributes, actions, and what he communicates — not his name or diagnosis."
));
children.push(T.makeTable(
  ["Category", "What Students Can Select"],
  [
    ["LOOKS LIKE", "a boy at the clinic / uses a wheelchair / has a communication book / looks at you directly when he communicates"],
    ["DOES",       "selects words / chooses what to say / waits for others to listen / asks for words he does not have / makes Catherine laugh"],
    ["FEELS",      "determined / honest / frustrated sometimes / clear about what he wants"],
    ["WANTS",      "to be heard / to communicate freely / to have the words he needs / for Catherine to be honest with him"],
  ],
  col2(0.22, 0.78)
));
children.push(T.tableCaption("The description built here IS evidence. A student who constructs this description has demonstrated character analysis at RL.4.3 level."));

children.push(h2k("Partner Guidance — Part 2"));
children.push(T.callout(
  "Wait time: 10–15 seconds. Students are processing a new kind of character — one who communicates differently.\n\n" +
  "Model AAC use during reading: 'Jason is choosing a word. He wants to say something specific. I think he feels determined.' [Indicate feel + determined on system.]\n\n" +
  "For students who use AAC: pay attention. This part of the novel may produce spontaneous communication — reactions, comments, recognition. Document it. This is Mode 2 data that belongs in the session tracker.\n\n" +
  "Do not rush through Jason's scenes. These are the scenes where the novel does its most important work."
));

children.push(h2k("Belonging Evidence Chart — Row 2 (complete at end of Part 2)"));
children.push(T.makeTable(
  ["Column", "Prompt to Student", "Example Response"],
  [
    ["What Catherine Does",  "What does Catherine do when she meets Jason?",                             "'She listens to him — and starts adding words to his book.'"],
    ["Code",                 "What code fits?",                                                          "[BELONG]"],
    ["What It Reveals",      "What does this tell us about a different way belonging can happen?",       "'Belonging can happen when someone listens and adds what you need — not when everyone acts the same.'"],
  ],
  col3(0.22, 0.10, 0.68)
));

// ═══════════════════════════════════════════════════════════════════════
// SECTION 10 — PART 3: WHEN THE RULES BREAK DOWN
// ═══════════════════════════════════════════════════════════════════════

children.push(T.heading1("Part 3: When the Rules Break Down"));
children.push(T.teacherRefLabel());

children.push(T.makeTable(
  ["Element", "Detail"],
  [
    ["Novel Section",  "Chapters 13–19 — Catherine's conflict between fitting in and being honest"],
    ["Skill Focus",    "How belonging and honesty conflict — and what Catherine chooses"],
    ["Standards",      "RL.4.3 · RL.5.3 (compare how Catherine and Jason navigate belonging differently)"],
    ["Annotation Code","[BELONG] + [RULE]"],
    ["Partner Mode",   "Mode 2 during reading · Mode 1 for activity"],
    ["Key vocabulary", "embarrassed · honest · choose · hide · belong · fair"],
  ],
  col2(0.28, 0.72)
));

children.push(T.spacer());
children.push(h2k("Activity Overview"));
children.push(T.p(
  "In the middle section of the novel, Catherine's two worlds begin to collide. " +
  "Kristi sees Jason. David shows up unexpectedly. The rules Catherine made stop working — " +
  "because the people around her do not follow them, and because following them requires Catherine to hide things that matter. " +
  "Jason asks for a word Catherine does not want to give him. " +
  "Part 3 asks students to notice: What does Catherine choose when belonging and honesty pull in different directions?"
));

children.push(h2k("Catherine's Conflict Chart"));
children.push(T.makeTable(
  ["Moment", "What Belonging (Fitting In) Requires", "What Honesty Requires", "What Catherine Chooses"],
  [
    ["Kristi asks about Jason",         "", "", ""],
    ["Jason asks for a word Catherine doesn't want to give", "", "", ""],
    ["David appears when Kristi is around", "", "", ""],
  ],
  col4(0.28, 0.24, 0.24, 0.24)
));
children.push(T.tableCaption("Students complete using any access method. Column 4 (What Catherine Chooses) is the character analysis column — the gap between what she wants to do and what she does reveals her character."));

children.push(h2k("Key Questions for Part 3"));
children.push(T.makeTable(
  ["Question", "Response Scaffold"],
  [
    ["What word does Jason ask for that Catherine struggles with?",             "He asks for ___. This is hard for Catherine because ___."],
    ["Why is it hard for Catherine to be honest with Jason in this section?",  "Sentence frame: 'It is hard because Catherine is afraid ___ will happen if she is honest.'"],
    ["What does Catherine do that she is not proud of?",                       "Select from: she hides Jason from Kristi / she does not add the word Jason needs / she pretends not to know someone / she acts differently in front of Kristi"],
    ["Who does Catherine treat differently in front of others — and why?",     "Sentence frame: 'Catherine treats ___ differently because she is worried about ___.'" ],
    ["What do Jason and David have in common in this section?",                "Both: are treated as problems to manage / are honest / are not trying to fit in / are showing Catherine something she does not want to see"],
  ],
  col2(0.44, 0.56)
));

children.push(h2k("Compare: Catherine and Jason"));
children.push(T.makeTable(
  ["", "How does belonging work for them?", "What are they afraid of?", "What do they need from others?"],
  [
    ["Catherine", "", "", ""],
    ["Jason",     "", "", ""],
  ],
  col4(0.15, 0.30, 0.28, 0.27)
));
children.push(T.tableCaption("Students who are working toward RL.5.3 (character comparison) use this table as their evidence source for the synthesis in Part 5."));

children.push(h2k("Partner Guidance — Part 3"));
children.push(T.callout(
  "This is the most emotionally complex section for students. Catherine does things that are not admirable. That is the point.\n\n" +
  "Wait time: 15 seconds minimum for questions about Catherine's choices. These are not easy answers.\n\n" +
  "Model AAC use: 'Catherine made a choice I feel uncertain about. I think she feels ashamed — but also like she wants to protect herself.' [Indicate on system.]\n\n" +
  "If a student seems troubled by Catherine's choices: 'It is okay to disagree with a character. That means you are reading closely. What would you want Catherine to do instead?'"
));

children.push(h2k("Belonging Evidence Chart — Row 3 (complete at end of Part 3)"));
children.push(T.makeTable(
  ["Column", "Prompt to Student", "Example Response"],
  [
    ["What Catherine Does",  "What does Catherine choose when belonging and honesty conflict?",             "'She chooses fitting in — she hides Jason from Kristi and does not give him the word he needs.'"],
    ["Code",                 "What code fits?",                                                            "[BELONG] or [RULE]"],
    ["What It Reveals",      "What does this tell us about what Catherine still believes about belonging?","'She still believes belonging means protecting her image — even if it hurts someone she cares about.'"],
  ],
  col3(0.22, 0.10, 0.68)
));

// ═══════════════════════════════════════════════════════════════════════
// SECTION 11 — PART 4: WHAT CATHERINE LEARNS
// ═══════════════════════════════════════════════════════════════════════

children.push(T.heading1("Part 4: What Catherine Learns"));
children.push(T.teacherRefLabel());

children.push(T.makeTable(
  ["Element", "Detail"],
  [
    ["Novel Section",  "Chapters 20–end — the resolution; Catherine changes"],
    ["Skill Focus",    "How Catherine changes and what she now understands about belonging"],
    ["Standards",      "RL.4.3 · RL.5.3 (character change as evidence of theme)"],
    ["Annotation Code","[CHANGE]"],
    ["Partner Mode",   "Mode 2 during reading · Mode 1 for activity"],
    ["Key vocabulary", "change · honest · belong · choose · sorry · know · accept"],
  ],
  col2(0.28, 0.72)
));

children.push(T.spacer());
children.push(h2k("Activity Overview"));
children.push(T.p(
  "In the final section of the novel, Catherine's rules begin to fall away — not because she abandons them all at once, " +
  "but because the relationships she has built (with Jason, with David, even with Kristi) show her that fitting in was never the same as belonging. " +
  "Part 4 asks students to trace Catherine's change: What does she do differently at the end? What does she understand now that she did not before?"
));

children.push(h2k("Catherine's Before/After Chart"));
children.push(T.makeTable(
  ["", "At the Start of the Novel", "At the End of the Novel"],
  [
    ["What Catherine wants",                          "", ""],
    ["What Catherine believes belonging means",        "", ""],
    ["How Catherine treats Jason",                     "", ""],
    ["How Catherine feels about David",                "", ""],
    ["What rule Catherine breaks — or stops needing", "", ""],
  ],
  col3(0.36, 0.32, 0.32)
));
children.push(T.tableCaption("Students complete using any access method. The contrast between the two columns IS the character change — this is the evidence for RL.4.3 character development."));

children.push(h2k("Key Questions for Part 4"));
children.push(T.makeTable(
  ["Question", "Response Scaffold"],
  [
    ["What does Catherine do at the end that she could not do at the beginning?", "Sentence frame: 'Catherine is now able to ___ — she could not do this at the start because ___.'" ],
    ["What does Catherine finally give Jason?",                                   "She gives him ___. This matters because ___."],
    ["How has Catherine's idea of 'belonging' changed?",                          "Sentence frame: 'At first, Catherine thought belonging meant ___. Now she understands it means ___.'" ],
    ["What did Catherine have to give up to let herself belong?",                 "Select from: the need to be normal / hiding David / pretending Jason wasn't her friend / trying to impress Kristi / her rules"],
    ["What does Catherine's change teach us about belonging?",                    "Sentence frame: 'Catherine shows us that real belonging requires ___, not just ___.'" ],
  ],
  col2(0.44, 0.56)
));

children.push(h2k("Partner Guidance — Part 4"));
children.push(T.callout(
  "This section often produces strong reactions — some students feel relief, some feel uncertain about the ending.\n\n" +
  "Wait time: 10–15 seconds. These questions ask students to compare across the whole novel.\n\n" +
  "Model AAC use: 'Catherine did something different at the end. I think she feels scared — but also more like herself.' [Indicate on system.]\n\n" +
  "If a student is not satisfied with how things end: 'What would you want to happen next? What does Catherine still need to do?' Those questions are great synthesis starters."
));

children.push(h2k("Belonging Evidence Chart — Row 4 (complete at end of Part 4)"));
children.push(T.makeTable(
  ["Column", "Prompt to Student", "Example Response"],
  [
    ["What Catherine Does",  "What does Catherine do at the end that shows she has changed?",             "'She gives Jason the word he needed. She stops hiding him from Kristi.'"],
    ["Code",                 "What code fits?",                                                           "[CHANGE]"],
    ["What It Reveals",      "What does Catherine's change tell us about what belonging really means?",   "'Belonging means letting people see you — and letting yourself see them — honestly.'"],
  ],
  col3(0.22, 0.10, 0.68)
));

// ═══════════════════════════════════════════════════════════════════════
// SECTION 12 — PART 5: WHOLE-BOOK SYNTHESIS
// ═══════════════════════════════════════════════════════════════════════

children.push(T.heading1("Part 5: Whole-Book Synthesis — What Does Rules Teach About Belonging?"));
children.push(T.teacherRefLabel());

children.push(T.makeTable(
  ["Element", "Detail"],
  [
    ["Novel Section",    "Full book — synthesis activity"],
    ["Skill Focus",      "Constructing a character analysis response supported by evidence from across the novel"],
    ["Standards",        "RL.4.3 (describe character using specific details) + RL.4.6 (narrator perspective) + RL.5.3 (character comparison)"],
    ["Text tool",        "Belonging Evidence Chart (completed across Parts 1–4)"],
    ["Format",           "Character analysis statement + evidence from Chart + synthesis response"],
    ["Response Access",  "All three pathways: symbol selection, verbal/gestural, generative construction"],
  ],
  col2(0.28, 0.72)
));

children.push(T.spacer());
children.push(h2k("Activity Overview"));
children.push(T.p(
  "By the time students reach Part 5, their Belonging Evidence Chart has four rows — one from each part of the novel. " +
  "Part 5 asks them to look across the chart and build a character analysis response: " +
  "Who is Catherine at the start? Who is she at the end? What did she have to learn? " +
  "What does her change teach us about what belonging really means?"
));

children.push(h2k("Build the Character Analysis Response: Three Steps"));
children.push(T.makeTable(
  ["Step", "What to Do", "Example"],
  [
    ["Step 1 — Review the Chart",         "Look at your completed Belonging Evidence Chart. What patterns do you see? What does Catherine keep doing until she finally stops?", "'Catherine keeps hiding things — David, Jason, how she really feels — and it keeps making belonging harder, not easier.'"],
    ["Step 2 — Draft the Statement",      "Use a sentence frame to build the character analysis statement. The statement must say what Catherine learns — not just what she does.", "'At the start of Rules, Catherine believes belonging means fitting in. By the end, she learns that real belonging means being known — and knowing others — honestly.'"],
    ["Step 3 — Add Evidence",             "Choose two rows from your chart as evidence. Which moments show Catherine's character most clearly?", "'Part 1 — when she makes rules for David. Part 4 — when she gives Jason the word he needed.'"],
  ],
  col3(0.22, 0.44, 0.34)
));

children.push(h2k("Character Analysis Statement Frames (Core Vocabulary Construction)"));
children.push(T.makeTable(
  ["Frame", "Core Words Available", "Sample Completed Statement"],
  [
    ["At the start of Rules, Catherine believes belonging means ___. By the end, she understands ___.",
     "normal · same · hide · fit in / honest · known · choose · real",
     "'At the start, Catherine believes belonging means fitting in and acting normal. By the end, she understands that belonging means letting people know the real you.'"],
    ["Catherine changes when ___. Before, she ___. After, she ___.",
     "All core vocabulary available",
     "'Catherine changes when she stops hiding Jason. Before, she was embarrassed. After, she chooses to be honest.'"],
    ["Rules teaches us that belonging is not about being ___. It is about being ___.",
     "same · normal · perfect / honest · known · chosen · seen",
     "'Rules teaches us that belonging is not about being normal. It is about being honest — even when it is hard.'"],
  ],
  col3(0.38, 0.28, 0.34)
));

children.push(h2k("Alternative Response: Word Sort for Belonging"));
children.push(T.p(
  "For students who need a more structured response option, provide a word sort. " +
  "Give the student 8–10 words: belong, normal, hide, honest, choose, real, known, same, seen, different. " +
  "Ask: Which of these words describes what Catherine learns belonging really means? Sort into: Yes / No / Maybe. " +
  "Ask the student to select their top 3 'Yes' words and explain one using a sentence frame. " +
  "The sort IS the character analysis — the student has identified what Catherine's change reveals about belonging."
));

children.push(h2k("Whole-Book Discussion: Open Questions"));
children.push(...T.bulletList([
  "Catherine makes rules at the start because she is trying to feel in control. What do you do when things feel unpredictable?",
  "Jason knows exactly what he wants to say, but sometimes does not have the word for it. What happens when you have something to say and cannot find the right way to say it?",
  "Is there a rule in your life that does not actually help anyone belong? What would happen if that rule changed?",
  "Catherine eventually gives Jason a word he had been missing. What does it mean to give someone the language they need?",
  "At the end of the novel, has Catherine fixed everything? What would you still want her to do?",
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

children.push(h2k("Academic Goal Stems — Character Analysis (RL)"));
children.push(T.makeTable(
  ["Standard", "Goal Stem"],
  [
    ["RL.4.3",
     "Given Rules by Cynthia Lord read aloud by a partner, a Belonging Evidence Chart, and character analysis sentence frames, [student] will describe Catherine's character using at least two specific details from the text (thoughts, words, or actions) as measured by rubric scoring on the Part 5 (Synthesis) activity, achieving a score of Approaching or Meets on 4 of 5 trials across 3 consecutive sessions by [IEP date]."],
    ["RL.4.6",
     "Given Rules by Cynthia Lord read aloud by a partner and a completed Belonging Evidence Chart, [student] will explain how Catherine's first-person point of view affects what the reader knows, citing at least one example of something Catherine cannot see clearly about herself, as measured by rubric scoring on the Part 3 activity and Part 5 synthesis, achieving a complete response on 4 of 5 trials across 3 consecutive sessions by [IEP date]."],
    ["RL.5.3",
     "Given Rules by Cynthia Lord read aloud by a partner, a completed Belonging Evidence Chart, and a character comparison chart, [student] will compare how Catherine and Jason each experience belonging, citing at least two specific details from the text that show the contrast, as measured by rubric scoring on the Part 3 comparison activity and Part 5 synthesis, achieving a complete comparison with evidence on 4 of 5 trials across 3 consecutive sessions by [IEP date]."],
  ],
  col2(0.10, 0.90)
));
children.push(T.tableCaption("Select the standard anchor that matches the student's IEP and grade placement. Adjust condition (access method), criterion (from baseline data), and date to match the individual student."));

children.push(T.spacer());
children.push(h2k("AAC Communication Goal Stem — Rules Unit Context"));
children.push(T.p(
  "This goal targets communication development within the Rules unit context — separate from the academic ELA skill. " +
  "Data is collected on the Communication Session Tracker by the paraprofessional, not on the academic rubric."
));
children.push(T.makeTable(
  ["Goal Type", "Goal Stem"],
  [
    ["Multi-symbol utterance",
     "Given Rules by Cynthia Lord shared reading with a communication partner using Aided Language Stimulation, [student] will produce a 2+ symbol utterance in response to character analysis questions (e.g., 'What does Catherine believe?' / 'How does Jason feel?') as measured by Communication Session Tracker data, achieving 4 of 5 response opportunities across 2 consecutive sessions with 2 different partners by [IEP date]."],
    ["Fringe vocabulary use in context",
     "Given the Rules unit with pre-confirmed fringe vocabulary (belong, rule, change, honest, hide) and partner Aided Language Stimulation, [student] will use at least one unit fringe vocabulary word in a contextually appropriate response during a Part 1–5 activity as measured by Communication Session Tracker data, achieving 4 of 5 opportunities across 2 consecutive sessions by [IEP date]."],
    ["Spontaneous initiation",
     "Given Rules by Cynthia Lord read aloud in a Mode 2 (Partnership) context, [student] will produce at least one spontaneous communicative act (comment, question, reaction) without a partner prompt during each 20-minute reading session as measured by Communication Session Tracker tally, achieving spontaneous initiation in 4 of 5 sessions across 2 consecutive weeks by [IEP date]."],
  ],
  col2(0.22, 0.78)
));
children.push(T.tableCaption(
  "Academic progress ≠ communication progress. A student can meet the rubric criterion using a sentence frame and still be building toward spontaneous AAC output — track both separately. " +
  "Note: This novel features an AAC user as a character. It may produce higher-than-expected spontaneous communication from students who use AAC — document this carefully."
));

children.push(T.spacer());
children.push(h2k("Data Collection Guidance"));
children.push(T.p(
  "Collect data during Mode 1 activities only (Parts 1–5 Belonging Evidence Chart and synthesis activities). Do not collect data during shared reading in Mode 2. " +
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
    ["Spontaneous comms",  "Yes (tally + brief description) / No",                        "Essential in this unit — document AAC-user-initiated responses separately"],
  ],
  col3(0.22, 0.42, 0.36)
));

// ═══════════════════════════════════════════════════════════════════════
// SECTION 14 — COMMUNICATION ACCESS QUICK REFERENCE
// ═══════════════════════════════════════════════════════════════════════

children.push(T.heading1("Communication Access Quick Reference"));
children.push(T.p("Pull out and laminate this page for the partner. This is the one-page summary for anyone working alongside the student during this unit."));

children.push(T.callout(
  "RULES — Identity and Belonging | Fiction Anchor Text Unit | Communicate by Design\n" +
  "The text stays the same. The scaffold varies. The expectation does not."
));

children.push(h2k("During Reading: Mode 2"));
children.push(...T.bulletList([
  "Follow the student's lead. Do NOT run prompt hierarchy during the read.",
  "Note spontaneous communication — especially during Jason's scenes. Write it down immediately, do not redirect it.",
  "Model AAC use naturally during reading: 'Jason is choosing a word. I think he feels determined to say something important.' [Indicate on system.]",
  "No demands. No correct/incorrect. Partnership only.",
  "This novel may produce stronger spontaneous communication from students who use AAC. That is expected and significant — document it.",
]));

children.push(h2k("During Activities: Mode 1"));
children.push(...T.bulletList([
  "Wait 10–15 seconds before prompting. Character motivation requires processing time.",
  "Start with the least intrusive prompt (gesture toward system).",
  "Accept: symbol, gaze, gesture, pointing, verbal, partner-confirmed — all valid.",
  "Never complete the response for the student.",
  "If no response: Is the vocabulary available? Is this the right mode? Is the environment set up correctly?",
]));

children.push(h2k("Top 5 Vocabulary Words — Confirm Before Starting"));
children.push(T.makeTable(
  ["Word", "Check"],
  [
    ["belong",  "☐ On device / board"],
    ["rule",    "☐ On device / board"],
    ["feel",    "☐ On device / board"],
    ["change",  "☐ On device / board"],
    ["honest",  "☐ On device / board"],
  ],
  col2(0.5, 0.5)
));
children.push(T.tableCaption("If a word is not available on the device, prepare a physical symbol or board card before the activity. Do not skip the pre-check."));

children.push(h2k("Annotation Codes — Quick Reference"));
children.push(T.makeTable(
  ["Code", "Marks", "Used in"],
  [
    ["[RULE]",   "What Catherine believes about belonging — her rules, her judgments", "Parts 1 and 3"],
    ["[BELONG]", "Evidence of how belonging happens (or doesn't) in the novel",        "Parts 2 and 3"],
    ["[CHANGE]", "Evidence of Catherine's change — what she does differently",          "Parts 4 and 5"],
  ],
  col3(0.14, 0.56, 0.30)
));

children.push(h2k("Belonging Evidence Chart Quick Guide"));
children.push(T.makeTable(
  ["Part", "Add a row to the chart for...", "Key prompt"],
  [
    ["Part 1", "A rule Catherine makes and what it reveals about belonging",      "'What does this rule tell us about what Catherine believes?'"],
    ["Part 2", "Something Jason communicates and how Catherine responds",          "'What does Jason say — and does Catherine really hear him?'"],
    ["Part 3", "A moment Catherine chooses fitting in over honesty",               "'What does Catherine choose — and what does that cost?'"],
    ["Part 4", "Something Catherine does differently at the end",                  "'How is Catherine different at the end? What changed?'"],
  ],
  col3(0.12, 0.52, 0.36)
));

// ═══════════════════════════════════════════════════════════════════════
// END MATTER NOTE
// ═══════════════════════════════════════════════════════════════════════

// NOTE: About the Creator, Terms of Use, and Accessibility Statement are NOT included
// in the fiction unit Teaching Materials docx. They live in the Welcome to the Product PDF only.
// See fiction_reference.md for this rule.

// ─────────────────────────────────────────────────────────────────────────
// ASSEMBLE AND WRITE
// ─────────────────────────────────────────────────────────────────────────

const outputPath = path.join(__dirname, "..", "Product Files", "Rules_Identity_and_Belonging_Teaching_Materials.docx");

T.assembleAndWrite(
  `${UNIT_TITLE}: ${UNIT_SUBTITLE}`,
  children,
  outputPath,
  {
    title: `Rules: Identity and Belonging — Fiction Anchor Text Unit`,
    description: `SDI companion unit for Rules by Cynthia Lord. Character Analysis · Identity and Belonging · Grades ${GRADE_RANGE} · Communicate by Design`,
  }
);

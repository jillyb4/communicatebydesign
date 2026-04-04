/**
 * cbd_aac_support.js — Shared AAC Support Section Generator
 * Communicate by Design — _Operations/
 *
 * SOURCE OF TRUTH for all CbD AAC framework language.
 * When the framework changes, change it here — propagates to all products.
 *
 * FRAMEWORK: CbD 5-Level Prompt Hierarchy (LOCKED March 2026)
 * Codes: I / G– / G+ / VM / RA
 * Replaces CTD/Ahern frameworks. System-agnostic.
 *
 * USAGE (nonfiction units — pass T from cbd_docx_template):
 *   const AAC = require('../../../_Operations/cbd_aac_support');
 *
 *   // Individual blocks:
 *   children.push(AAC.fringeAccessPara(T));
 *   children.push(AAC.vocabTable(T, { coreWords: "...", fringeWords: "..." }));
 *   children.push(AAC.partnerModesPara(T));
 *
 *   // Or full section (Keiko / Radium Girls pattern):
 *   children.push(...AAC.aacSupportSection(T, {
 *     coreWords: "**think, feel...**",
 *     fringeWords: "**whale, ocean...**",
 *     participationRows: [["Annotation", "Select H/P/D card..."], ...],
 *     iepGoalRows: [["Annotation", "Given informational text..."], ...],
 *   }));
 *
 * HARD RULES (never violate):
 *   - No SLP gatekeeping: teachers, paras, families CAN add vocabulary
 *   - No "point to" as sole interaction verb: always include gaze + indicate
 *   - No "coordinate with the SLP/AAC team": capacity-building model only
 *   - Strength-based language only: no deficit framing
 */

'use strict';

// ─────────────────────────────────────────────────────────────────────────────
// FRAMEWORK CONSTANTS
// These strings are the canonical CbD framework language.
// ─────────────────────────────────────────────────────────────────────────────

const OPENING_STATEMENT_TEXT =
  "This unit is designed for students who use AAC to communicate. That is the starting " +
  "assumption \u2014 not an accommodation. The symbol cards in this packet are part of the " +
  "communication system for this lesson: print, cut, and use them alongside whatever " +
  "system the student already uses.";

const FRINGE_ACCESS_TEXT =
  "Before Lesson 1, confirm each fringe word is accessible in the format that works best " +
  "for this student \u2014 cards in a field, added to a low-tech board, or included in a " +
  "PECS set. Any team member can set this up: teacher, communication partner, family, or SLP.";

const PARTNER_MODES_TEXT =
  "Partner modes during instruction: Not every moment is a prompting opportunity. " +
  "Communication partners shift between three modes \u2014 Instructional (hierarchy active, " +
  "appropriate during structured response tasks), Partnership (no demands, follow the " +
  "student\u2019s lead during discussion and transitions), and Facilitated Participation " +
  "(physical access support only during whole-group activities). For full partner scripts " +
  "and prompting guidance, see the Communicate by Design Communication Partner Guide.";

const IEP_CONFIRM_TEXT =
  "Before Lesson 1: confirm fringe vocabulary is accessible. Who adds it depends on your " +
  "setup \u2014 teacher, communication partner, SLP, or family can all do this.";

const IEP_DATA_TEXT =
  "Lesson 2 checkpoint data can document SDI delivery and student response for IEP " +
  "progress monitoring.";

const IEP_ARTIFACT_TEXT =
  "Final product and Evidence Recording Sheet can serve as IEP evidence artifacts for " +
  "writing, research, and communication goals.";

const V3_VOCAB_NOTE_TEXT =
  "Version 3 passages use core words and the highest-frequency fringe words from this " +
  "unit \u2014 the vocabulary the student encounters most. The annotation task, the " +
  "argument, the essential question \u2014 all the same. The scaffold is vocabulary " +
  "access, not the expectation.";

// Standard vocab table headers
const VOCAB_TABLE_HEADERS = [
  "Core words \u2014 symbol cards included in this packet",
  "Fringe words (unit-specific) \u2014 symbol cards included. Make accessible before Lesson 1. V3 passages prioritize the highest-frequency words from this column.",
];

const PARTICIPATION_TABLE_HEADERS = ["Component", "AAC access point"];
const IEP_TABLE_HEADERS = ["Skill area", "Sample IEP goal stem"];

// ─────────────────────────────────────────────────────────────────────────────
// INDIVIDUAL BLOCK EXPORTS
// Each function returns a single element (or array of elements) to push into children.
// All accept T (the cbd_docx_template module) so they use consistent document styling.
// ─────────────────────────────────────────────────────────────────────────────

/**
 * Opening statement paragraph — establishes AAC as designed-in, not bolted on.
 * Always appears as first paragraph under "Communication Access" heading.
 * @param {object} T - cbd_docx_template module
 * @param {object} opts - { after: number } paragraph spacing
 */
function openingStatementPara(T, opts = {}) {
  return T.p(OPENING_STATEMENT_TEXT, { after: opts.after ?? 120 });
}

/**
 * Fringe accessibility paragraph.
 * Lists access options low-tech first (index card → low-tech board → PECS → SGD).
 * SGD is framed as conditional ("if the student uses one"), not assumed default.
 * Replaces all "Coordinate with the SLP/AAC team" language.
 * @param {object} T - cbd_docx_template module
 * @param {object} opts - { after: number } paragraph spacing
 */
function fringeAccessPara(T, opts = {}) {
  return T.p(FRINGE_ACCESS_TEXT, { after: opts.after ?? 160 });
}

/**
 * Partner modes reference paragraph.
 * Brief inline reference for nonfiction units.
 * Full dedicated page is partnerModesPage() — used in UFLI packets.
 * @param {object} T - cbd_docx_template module
 * @param {object} opts - { after: number, size: number } paragraph styling
 */
function partnerModesPara(T, opts = {}) {
  return T.p(PARTNER_MODES_TEXT, { after: opts.after ?? 160, size: opts.size });
}

/**
 * IEP confirmation paragraph.
 * Replaces "SLP/AT confirm fringe vocabulary is programmed" language.
 * @param {object} T - cbd_docx_template module
 * @param {object} opts - { after: number }
 */
function iepConfirmPara(T, opts = {}) {
  return T.p(IEP_CONFIRM_TEXT, { after: opts.after ?? 120 });
}

/**
 * Standard IEP data note paragraph.
 * @param {object} T - cbd_docx_template module
 * @param {object} opts - { after: number, customText: string }
 */
function iepDataPara(T, opts = {}) {
  return T.p(opts.customText || IEP_DATA_TEXT, { after: opts.after ?? 120 });
}

/**
 * Standard IEP artifact note paragraph.
 * @param {object} T - cbd_docx_template module
 * @param {object} opts - { after: number, customText: string }
 */
function iepArtifactPara(T, opts = {}) {
  return T.p(opts.customText || IEP_ARTIFACT_TEXT, { after: opts.after ?? 160 });
}

/**
 * Core/fringe vocabulary table.
 * @param {object} T - cbd_docx_template module
 * @param {object} params
 * @param {string} params.coreWords - comma-separated core words (may use **bold**)
 * @param {string} params.fringeWords - comma-separated fringe words (may use **bold**)
 * @param {number[]} params.colWidths - [leftColWidth, rightColWidth] in DXA (default: [5040, 5040])
 */
function vocabTable(T, { coreWords, fringeWords, colWidths = [5040, 5040] }) {
  return T.makeTable(
    VOCAB_TABLE_HEADERS,
    [[coreWords, fringeWords]],
    colWidths
  );
}

/**
 * V3 vocabulary rule note paragraph.
 * Appears after the core/fringe vocab table.
 * Establishes: all vocabulary has symbols, V3 prioritizes core + high-frequency fringe,
 * same expectation across all versions.
 * @param {object} T - cbd_docx_template module
 * @param {object} opts - { after: number }
 */
function v3VocabNote(T, opts = {}) {
  return T.p(V3_VOCAB_NOTE_TEXT, { after: opts.after ?? 160, size: 20, italics: true });
}

/**
 * AAC participation pathway table.
 * @param {object} T - cbd_docx_template module
 * @param {object} params
 * @param {string[][]} params.rows - array of [component, aac_access_point] rows
 * @param {number[]} params.colWidths - default [2160, 7920]
 */
function participationTable(T, { rows, colWidths = [2160, 7920] }) {
  return T.makeTable(PARTICIPATION_TABLE_HEADERS, rows, colWidths);
}

/**
 * IEP goal stems table.
 * @param {object} T - cbd_docx_template module
 * @param {object} params
 * @param {string[][]} params.rows - array of [skill_area, goal_stem] rows
 * @param {number[]} params.colWidths - default [2160, 7920]
 */
function iepGoalTable(T, { rows, colWidths = [2160, 7920] }) {
  return T.makeTable(IEP_TABLE_HEADERS, rows, colWidths);
}

// ─────────────────────────────────────────────────────────────────────────────
// FULL SECTION WRAPPER
// Convenience function for the standard Keiko / Radium Girls / Capitol Crawl pattern.
// Returns an array of elements to spread into children.
// ─────────────────────────────────────────────────────────────────────────────

/**
 * Full Communication Access section for nonfiction units (standard pattern).
 *
 * Generates:
 *   heading3("Communication Access")
 *   openingStatementPara  ("This unit is designed for students who use AAC...")
 *   fringeAccessPara      (low-tech first, SGD conditional)
 *   vocabTable (core / fringe)
 *   heading3("Participation Across the Unit")
 *   participationTable
 *   partnerModesPara
 *   heading3("IEP Coordination and Goal Stems")
 *   iepConfirmPara
 *   iepDataPara
 *   iepArtifactPara
 *   iepGoalTable
 *
 * @param {object} T - cbd_docx_template module
 * @param {object} options
 * @param {string} options.coreWords - bold-formatted core word string
 * @param {string} options.fringeWords - bold-formatted fringe word string
 * @param {string[][]} options.participationRows - rows for participation table
 * @param {string[][]} options.iepGoalRows - rows for IEP goal stems table
 * @param {number[]} [options.vocabColWidths] - vocab table column widths
 * @param {number[]} [options.participationColWidths] - participation table column widths
 * @param {number[]} [options.iepColWidths] - IEP table column widths
 * @param {string} [options.iepDataNote] - custom lesson checkpoint note
 * @param {string} [options.iepArtifactNote] - custom final product note
 */
function aacSupportSection(T, {
  coreWords,
  fringeWords,
  participationRows,
  iepGoalRows,
  vocabColWidths = [5040, 5040],
  participationColWidths = [2160, 7920],
  iepColWidths = [2160, 7920],
  iepDataNote,
  iepArtifactNote,
}) {
  const elements = [];

  elements.push(T.heading3("Communication Access"));
  elements.push(openingStatementPara(T));
  elements.push(fringeAccessPara(T));
  elements.push(vocabTable(T, { coreWords, fringeWords, colWidths: vocabColWidths }));
  elements.push(v3VocabNote(T));

  elements.push(T.heading3("Participation Across the Unit"));
  elements.push(participationTable(T, { rows: participationRows, colWidths: participationColWidths }));
  elements.push(partnerModesPara(T));

  elements.push(T.heading3("IEP Coordination and Goal Stems"));
  elements.push(iepConfirmPara(T));
  elements.push(iepDataPara(T, { customText: iepDataNote }));
  elements.push(iepArtifactPara(T, { customText: iepArtifactNote }));
  elements.push(iepGoalTable(T, { rows: iepGoalRows, colWidths: iepColWidths }));

  return elements;
}

// ─────────────────────────────────────────────────────────────────────────────
// EXPORTS
// ─────────────────────────────────────────────────────────────────────────────

module.exports = {
  // Framework text (for inspection / testing)
  OPENING_STATEMENT_TEXT,
  FRINGE_ACCESS_TEXT,
  V3_VOCAB_NOTE_TEXT,
  PARTNER_MODES_TEXT,
  IEP_CONFIRM_TEXT,
  IEP_DATA_TEXT,
  IEP_ARTIFACT_TEXT,

  // Individual blocks
  openingStatementPara,
  fringeAccessPara,
  v3VocabNote,
  partnerModesPara,
  iepConfirmPara,
  iepDataPara,
  iepArtifactPara,
  vocabTable,
  participationTable,
  iepGoalTable,

  // Full section wrapper (standard nonfiction pattern)
  aacSupportSection,
};

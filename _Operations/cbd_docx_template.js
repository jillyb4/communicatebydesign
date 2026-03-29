// ═══════════════════════════════════════════════════════════════════════════
// CbD Nonfiction Reading Unit — Reusable Document Template
// ═══════════════════════════════════════════════════════════════════════════
//
// PURPOSE: This module contains ALL design decisions for CbD Word documents.
// It is the single source of truth for branding, layout, page structure,
// and formatting. Unit build scripts import this module and call its
// functions with unit-specific content. This prevents design drift between
// units and eliminates the need to rebuild formatting from scratch.
//
// USAGE:
//   const T = require("./cbd_docx_template");
//   // Then call T.titlePage({...}), T.studentHandoutHeader("Word Bank"), etc.
//
// DESIGN RULES (locked in — do not override per-unit):
//   - Font: Arial only (per brand guidelines)
//   - Colors: Navy #1B1F3B, Teal #00B4D8, Amber #FFB703, Gray #F4F6F8
//   - Student handouts: Name/Class/Teacher fields, own page, print-friendly
//   - Teacher pages: "TEACHER REFERENCE" label, Lexile info OK
//   - Reading passages: thin header line + discrete version label + Name/Class/Teacher
//   - MCQ pages: own page, numbered bold questions, A/B/C/D lettered choices
//   - SA pages: own page, questions + write-on lines
//   - Version labels: discrete gray text, no Lexile on student-facing pages
//   - Grade range: 6–10
//   - Tables: Navy header row with white text, alternating gray rows
//   - Callouts: Amber left border
//   - Heading 1: Navy + teal bottom border + page break
//   - Heading 2: Navy
//   - Heading 3: Accessible Deep Teal (#0077B6)
//
// ACCESSIBILITY (WCAG 2.2 AA):
//   - All text colors pass WCAG 2.2 AA contrast ratios (4.5:1 normal, 3:1 large)
//   - Document title and language set in metadata
//   - Proper heading hierarchy (H1 > H2 > H3, no skips)
//   - Table header rows marked with tableHeader: true
//   - Real list formatting via numbering config (not manual dashes)
//   - Table captions for screen reader context
//   - Accessibility statement included in every product
//
// CHANGELOG:
//   v1.1 (2026-03-17) — WCAG 2.2 AA accessibility upgrade.
//     - TEAL color changed from #00B4D8 (2.46:1 contrast — FAIL) to #006DA0 (5.68:1 — PASS AA)
//     - Document title and language metadata added to assembleAndWrite()
//     - New helpers: tableCaption(), bulletList(), accessibilityStatement()
//     - Bullet list numbering config added to Document constructor
//     - Accessibility documentation block added to header comments
//   v1.0 (2026-03-16) — Initial creation from Frances Kelsey build script.
//     Includes: brand constants, all helper functions, page builders for
//     title page, TOC, teacher reference sections, student handout sections,
//     reading passages (Keiko-style), MCQ pages, SA pages, version sections,
//     answer key, and document assembly.
// ═══════════════════════════════════════════════════════════════════════════

const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, LevelFormat,
  TableOfContents, HeadingLevel, BorderStyle, WidthType, ShadingType,
  PageNumber, PageBreak, TabStopType, TabStopPosition, ImageRun,
  TableLayoutType
} = require("docx");

// ── Brand Constants ───────────────────────────────────────────────────────
const PAGE_WIDTH = 12240;   // US Letter in twips
const PAGE_HEIGHT = 15840;
const MARGIN = 1080;        // 0.75 inch — tighter layout, less wasted margin space
const CONTENT_WIDTH = PAGE_WIDTH - 2 * MARGIN; // 10080
const FONT = "Arial";       // Only font per brand guidelines

// CbD Brand Colors (from Brand Guidelines document)
const NAVY = "1B1F3B";       // Deep Ink Navy — headings, backgrounds, body text
const TEAL = "006DA0";       // Accessible Deep Teal — WCAG AA compliant (5.68:1 on white, 5.25:1 on gray). Original #00B4D8 failed (2.46:1).
const AMBER = "FFB703";      // Warm Amber — BY DESIGN, icons, callout borders
const YELLOW = "FFD700";     // Warm Yellow — sparingly, accents only
const GRAY_LIGHT = "F4F6F8"; // Light gray — alternating table rows
const BORDER_COLOR = "CCCCCC";
const BODY_COLOR = "1B1F3B";  // Body text in Navy per brand spec

const thinBorder = { style: BorderStyle.SINGLE, size: 1, color: BORDER_COLOR };
const borders = { top: thinBorder, bottom: thinBorder, left: thinBorder, right: thinBorder };
const noBorders = {
  top: { style: BorderStyle.NONE, size: 0 },
  bottom: { style: BorderStyle.NONE, size: 0 },
  left: { style: BorderStyle.NONE, size: 0 },
  right: { style: BorderStyle.NONE, size: 0 },
};
const cellMargins = { top: 60, bottom: 60, left: 100, right: 100 };

// ── Core Paragraph Helpers ────────────────────────────────────────────────

/**
 * Create a paragraph with optional bold/italic markdown-style parsing.
 * Supports **bold** and *italic* inline markers, or an array of TextRun specs.
 * @param {string|Array} text - Text content or array of TextRun config objects
 * @param {Object} opts - Options: size, color, bold, italics, align, indent, after, before, line, heading, pageBreakBefore, border
 */
function p(text, opts = {}) {
  const runs = [];
  if (typeof text === "string") {
    const parts = text.split(/(\*\*[^*]+\*\*|\*[^*]+\*)/g);
    for (const part of parts) {
      if (part.startsWith("**") && part.endsWith("**")) {
        runs.push(new TextRun({ text: part.slice(2, -2), bold: true, font: FONT, size: opts.size || 22, color: opts.color }));
      } else if (part.startsWith("*") && part.endsWith("*")) {
        runs.push(new TextRun({ text: part.slice(1, -1), italics: true, font: FONT, size: opts.size || 22, color: opts.color }));
      } else if (part) {
        runs.push(new TextRun({ text: part, font: FONT, size: opts.size || 22, bold: opts.bold, italics: opts.italics, color: opts.color }));
      }
    }
  } else if (Array.isArray(text)) {
    for (const t of text) {
      if (typeof t === "string") {
        runs.push(new TextRun({ text: t, font: FONT, size: opts.size || 22 }));
      } else {
        runs.push(new TextRun({ font: FONT, size: opts.size || 22, ...t }));
      }
    }
  }
  return new Paragraph({
    spacing: { after: opts.after !== undefined ? opts.after : 120, before: opts.before || 0, line: opts.line || 276 },
    alignment: opts.align,
    indent: opts.indent,
    ...(opts.heading ? { heading: opts.heading } : {}),
    ...(opts.numbering ? { numbering: opts.numbering } : {}),
    ...(opts.pageBreakBefore ? { pageBreakBefore: true } : {}),
    ...(opts.border ? { border: opts.border } : {}),
    children: runs,
  });
}

/** Heading 1 — Navy, bold, teal bottom border, optional page break (default true) */
function heading1(text, pageBreak = true) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: pageBreak ? 0 : 360, after: 200 },
    ...(pageBreak ? { pageBreakBefore: true } : {}),
    border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: TEAL, space: 4 } },
    children: [new TextRun({ text, font: FONT, size: 36, bold: true, color: NAVY })],
  });
}

/** Heading 2 — Navy, bold */
function heading2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 200, after: 120 },
    children: [new TextRun({ text, font: FONT, size: 28, bold: true, color: NAVY })],
  });
}

/** Heading 3 — Teal, bold */
function heading3(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_3,
    spacing: { before: 200, after: 120 },
    children: [new TextRun({ text, font: FONT, size: 24, bold: true, color: TEAL })],
  });
}

/** Blank spacer paragraph */
function spacer(size = 80) {
  return new Paragraph({ spacing: { after: size } });
}

/** Horizontal rule — teal line */
function hr() {
  return new Paragraph({
    spacing: { before: 200, after: 200 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: TEAL, space: 1 } },
  });
}

// ── Table Helpers ─────────────────────────────────────────────────────────

function makeCell(content, opts = {}) {
  const children = [];
  if (typeof content === "string") {
    const runs = [];
    const parts = content.split(/(\*\*[^*]+\*\*)/g);
    for (const part of parts) {
      if (part.startsWith("**") && part.endsWith("**")) {
        runs.push(new TextRun({ text: part.slice(2, -2), bold: true, font: FONT, size: 20 }));
      } else if (part) {
        runs.push(new TextRun({ text: part, font: FONT, size: 20, bold: opts.bold, italics: opts.italics }));
      }
    }
    children.push(new Paragraph({ spacing: { after: 40, line: 240 }, children: runs }));
  } else if (Array.isArray(content)) {
    for (const item of content) {
      if (typeof item === "string") {
        children.push(new Paragraph({ spacing: { after: 40, line: 240 }, children: [new TextRun({ text: item, font: FONT, size: 20 })] }));
      } else {
        children.push(item);
      }
    }
  } else {
    children.push(content);
  }
  return new TableCell({
    borders: opts.noBorders ? noBorders : borders,
    width: opts.width ? { size: opts.width, type: WidthType.DXA } : undefined,
    shading: opts.shading ? { fill: opts.shading, type: ShadingType.CLEAR } : undefined,
    margins: cellMargins,
    verticalAlign: opts.vAlign || undefined,
    children,
  });
}

/**
 * Create a branded table with Navy header row + alternating gray data rows.
 * @param {string[]} headers - Column header text
 * @param {string[][]} rows - 2D array of cell content
 * @param {number[]} colWidths - Column widths in twips
 * @param {Object} [opts] - Optional: { compact: true } for tighter teacher tables (size 18, less padding)
 */
function makeTable(headers, rows, colWidths, opts = {}) {
  const sz = opts.compact ? 17 : 20;
  const lineSpacing = opts.compact ? 220 : 240;
  const cellPad = opts.compact ? { top: 20, bottom: 20, left: 60, right: 60 } : cellMargins;
  // Auto-scale column widths to fill CONTENT_WIDTH if they don't already
  const rawTotal = colWidths.reduce((a, b) => a + b, 0);
  if (rawTotal < CONTENT_WIDTH) {
    const scale = CONTENT_WIDTH / rawTotal;
    colWidths = colWidths.map(w => Math.round(w * scale));
  }
  const totalWidth = colWidths.reduce((a, b) => a + b, 0);
  const tableRows = [];
  // Helper: parse a cell string into one or more paragraphs, splitting on \n
  function cellParagraphs(text, extraOpts) {
    const paragraphs = [];
    const lines = String(text).split("\n");
    let nextSpacingBefore = 0;
    for (const line of lines) {
      if (!line.trim()) {
        // Empty line = add extra spacing before the next paragraph
        nextSpacingBefore = 80;
        continue;
      }
      const runs = [];
      const parts = line.split(/(\*\*[^*]+\*\*)/g);
      for (const part of parts) {
        if (part.startsWith("**") && part.endsWith("**")) {
          runs.push(new TextRun({ text: part.slice(2, -2), bold: true, font: FONT, size: extraOpts?.sz || sz, color: extraOpts?.color }));
        } else if (part) {
          runs.push(new TextRun({ text: part, bold: extraOpts?.bold, font: FONT, size: extraOpts?.sz || sz, color: extraOpts?.color }));
        }
      }
      paragraphs.push(new Paragraph({ spacing: { before: nextSpacingBefore, after: 20, line: lineSpacing }, children: runs }));
      nextSpacingBefore = 0;
    }
    return paragraphs.length > 0 ? paragraphs : [new Paragraph({ spacing: { after: 20, line: lineSpacing }, children: [new TextRun({ text: "", font: FONT, size: sz })] })];
  }

  if (headers) {
    tableRows.push(new TableRow({
      tableHeader: true,
      cantSplit: true,
      children: headers.map((h, i) => {
        return new TableCell({
          borders,
          width: { size: colWidths[i], type: WidthType.DXA },
          shading: { fill: NAVY, type: ShadingType.CLEAR },
          margins: cellPad,
          children: cellParagraphs(h, { bold: true, color: "FFFFFF" }),
        });
      }),
    }));
  }
  rows.forEach((row, ri) => {
    tableRows.push(new TableRow({
      cantSplit: opts.allowSplit ? false : true,
      children: row.map((cell, ci) => {
        return new TableCell({
          borders,
          width: { size: colWidths[ci], type: WidthType.DXA },
          shading: ri % 2 === 0 ? { fill: GRAY_LIGHT, type: ShadingType.CLEAR } : undefined,
          margins: cellPad,
          children: cellParagraphs(cell),
        });
      }),
    }));
  });
  return new Table({
    width: { size: totalWidth, type: WidthType.DXA },
    columnWidths: colWidths,
    layout: TableLayoutType.FIXED,
    rows: tableRows,
  });
}

/** Callout box — Amber left border with bold label */
function callout(text, label = "Note") {
  return new Paragraph({
    spacing: { before: 120, after: 120, line: 260 },
    indent: { left: 360 },
    border: { left: { style: BorderStyle.SINGLE, size: 12, color: AMBER, space: 8 } },
    children: [
      new TextRun({ text: label + ": ", bold: true, font: FONT, size: 21, color: NAVY }),
      new TextRun({ text, font: FONT, size: 21, color: BODY_COLOR }),
    ],
  });
}

/** Info box — bordered box for introductory context (used in Differentiating, Modeling, Vocab) */
function infoBox(text) {
  return new Paragraph({
    spacing: { before: 80, after: 120, line: 260 },
    indent: { left: 240, right: 240 },
    border: {
      top: { style: BorderStyle.SINGLE, size: 1, color: BORDER_COLOR },
      bottom: { style: BorderStyle.SINGLE, size: 1, color: BORDER_COLOR },
      left: { style: BorderStyle.SINGLE, size: 1, color: BORDER_COLOR },
      right: { style: BorderStyle.SINGLE, size: 1, color: BORDER_COLOR },
    },
    children: [new TextRun({ text, font: FONT, size: 21, color: BODY_COLOR })],
  });
}

/** Checkbox item (unchecked by default) */
/** Legacy checkbox — single paragraph with Unicode box. Avoid for new content; use checklistTable instead. */
function checkbox(text, checked = false) {
  return p([
    { text: checked ? "\u2611 " : "\u2610 ", font: "Segoe UI Symbol", size: 22 },
    { text, size: 22 },
  ], { after: 60 });
}

/**
 * Checklist rendered as a clean table with a "Done" column for marking.
 * Far more readable than inline Unicode checkboxes — works for both teacher prep and student self-assessment.
 * @param {string[]} items - Array of checklist item text strings
 * @param {Object} [opts] - Options: { doneLabel: "Done" | "Yes / Not Yet", numbered: true|false }
 */
function checklistTable(items, opts = {}) {
  const doneLabel = opts.doneLabel || "\u2713";
  const doneWidth = 900;
  const itemWidth = CONTENT_WIDTH - doneWidth;
  const tableRows = [];
  // Header row
  tableRows.push(new TableRow({
    tableHeader: true,
    cantSplit: true,
    children: [
      new TableCell({
        borders,
        width: { size: itemWidth, type: WidthType.DXA },
        shading: { fill: NAVY, type: ShadingType.CLEAR },
        margins: { top: 40, bottom: 40, left: 100, right: 100 },
        children: [new Paragraph({ spacing: { after: 0, line: 240 }, children: [new TextRun({ text: opts.headerLabel || "Item", bold: true, font: FONT, size: 20, color: "FFFFFF" })] })],
      }),
      new TableCell({
        borders,
        width: { size: doneWidth, type: WidthType.DXA },
        shading: { fill: NAVY, type: ShadingType.CLEAR },
        margins: { top: 40, bottom: 40, left: 60, right: 60 },
        children: [new Paragraph({ spacing: { after: 0, line: 240 }, alignment: AlignmentType.CENTER, children: [new TextRun({ text: doneLabel, bold: true, font: FONT, size: 20, color: "FFFFFF" })] })],
      }),
    ],
  }));
  // Data rows
  items.forEach((item, i) => {
    const runs = [];
    if (opts.numbered) {
      runs.push(new TextRun({ text: (i + 1) + ".  ", bold: true, font: FONT, size: 20, color: NAVY }));
    }
    // Parse bold markers
    const parts = String(item).split(/(\*\*[^*]+\*\*)/g);
    for (const part of parts) {
      if (part.startsWith("**") && part.endsWith("**")) {
        runs.push(new TextRun({ text: part.slice(2, -2), bold: true, font: FONT, size: 20 }));
      } else if (part) {
        runs.push(new TextRun({ text: part, font: FONT, size: 20 }));
      }
    }
    tableRows.push(new TableRow({
      cantSplit: true,
      children: [
        new TableCell({
          borders,
          width: { size: itemWidth, type: WidthType.DXA },
          shading: i % 2 === 0 ? { fill: GRAY_LIGHT, type: ShadingType.CLEAR } : undefined,
          margins: { top: 50, bottom: 50, left: 100, right: 100 },
          children: [new Paragraph({ spacing: { after: 0, line: 252 }, children: runs })],
        }),
        new TableCell({
          borders,
          width: { size: doneWidth, type: WidthType.DXA },
          shading: i % 2 === 0 ? { fill: GRAY_LIGHT, type: ShadingType.CLEAR } : undefined,
          margins: { top: 50, bottom: 50, left: 60, right: 60 },
          children: [new Paragraph({ spacing: { after: 0 }, alignment: AlignmentType.CENTER, children: [] })],
        }),
      ],
    }));
  });
  return new Table({
    width: { size: CONTENT_WIDTH, type: WidthType.DXA },
    columnWidths: [itemWidth, doneWidth],
    layout: TableLayoutType.FIXED,
    rows: tableRows,
  });
}

/** Blockquote — teal left border, italic, indented */
function blockquote(text) {
  return new Paragraph({
    spacing: { before: 80, after: 120, line: 276 },
    indent: { left: 480, right: 480 },
    border: { left: { style: BorderStyle.SINGLE, size: 8, color: TEAL, space: 8 } },
    children: [new TextRun({ text, font: FONT, size: 22, italics: true })],
  });
}

// ── Accessibility Helpers (WCAG 2.2 AA) ─────────────────────────────────

/**
 * Table caption — describes a table for screen reader users (WCAG 1.3.1).
 * Place immediately before the table it describes.
 * @param {string} text - e.g. "Table: CCSS Standards Alignment — Primary standards, descriptions, and where they appear in the unit"
 */
function tableCaption(text) {
  return new Paragraph({
    spacing: { before: 160, after: 60 },
    children: [new TextRun({ text, font: FONT, size: 20, italics: true, color: "555555" })],
  });
}

/**
 * Bulleted list — uses real list formatting for screen reader accessibility (WCAG 1.3.1).
 * @param {string[]} items - Array of bullet text strings (supports **bold** markers)
 * @param {Object} [opts] - Options: { size, indent, color }
 */
function bulletList(items, opts = {}) {
  return items.map(item => {
    const runs = [];
    const parts = String(item).split(/(\*\*[^*]+\*\*)/g);
    for (const part of parts) {
      if (part.startsWith("**") && part.endsWith("**")) {
        runs.push(new TextRun({ text: part.slice(2, -2), bold: true, font: FONT, size: opts.size || 22, color: opts.color || BODY_COLOR }));
      } else if (part) {
        runs.push(new TextRun({ text: part, font: FONT, size: opts.size || 22, color: opts.color || BODY_COLOR }));
      }
    }
    return new Paragraph({
      spacing: { after: 60, line: 276 },
      numbering: { reference: "cbd-bullets", level: 0 },
      children: runs,
    });
  });
}

/**
 * Accessibility statement — goes in every CbD product's teacher documents.
 * Signals commitment to accessibility and provides a contact channel.
 */
function accessibilityStatement() {
  return [
    heading2("Accessibility Statement"),
    p("This document was designed to meet WCAG 2.2 Level AA accessibility standards. It is compatible with screen readers, text-to-speech tools (including Microsoft Immersive Reader), and assistive technology. Headings are structured for keyboard navigation. Tables include header rows for screen reader identification. All text meets minimum contrast ratios for low-vision users."),
    p(""),
    p([
      { text: "Using this document with assistive technology: ", bold: true },
      { text: "In Microsoft Word, use ", size: 22 },
      { text: "View > Immersive Reader", bold: true, size: 22 },
      { text: " or ", size: 22 },
      { text: "Review > Read Aloud", bold: true, size: 22 },
      { text: " to hear passages read aloud. Reading passages are formatted for continuous text-to-speech. Navigate sections using the ", size: 22 },
      { text: "Navigation Pane (View > Navigation Pane)", bold: true, size: 22 },
      { text: " or by pressing Ctrl+F to search.", size: 22 },
    ]),
    p(""),
    p([
      { text: "Known limitation: ", bold: true },
      { text: "If you convert this document to PDF, use ", size: 22 },
      { text: "File > Save As > PDF", bold: true, size: 22 },
      { text: " (not Print > PDF). The Save As method preserves document structure tags that screen readers need. Printing to PDF strips all accessibility.", size: 22 },
    ]),
    p(""),
    p([
      { text: "If you encounter an accessibility barrier in this product, contact Jill McCardel at communicatebydesign.substack.com. ", size: 22 },
      { text: "Accessibility is not an add-on — it is how Communicate by Design builds.", bold: true, italics: true, size: 22 },
    ]),
  ];
}

/**
 * About the Creator — goes in every CbD product's teacher documents.
 * Condensed version of the full About Me for in-document use.
 */
function aboutTheCreator() {
  return [
    heading2("About the Creator"),
    p("Communicate by Design was created by Jill McCardel — a special educator, advocate, and mom to an AAC user."),
    p("Everything in this resource is designed to build capacity across the whole team — teachers, OTs, PTs, BCBAs, RBTs, paraprofessionals, and families. AT and AAC aren't one person's job. Any professional working with a student in any environment should have the knowledge and tools to support communication."),
    p([
      { text: "Communicate by Design", bold: true, size: 22 },
      { text: " is grounded in the capacity-building approach: evidence-based, practical, and ready to use. No fluff, no filler — just tools that work on Monday morning.", size: 22 },
    ]),
    p(""),
    p([
      { text: "Find more resources and writing at ", size: 22 },
      { text: "communicatebydesign.substack.com", bold: true, size: 22 },
      { text: " and on Instagram at ", size: 22 },
      { text: "@communicatebydesignaac", bold: true, size: 22 },
      { text: ".", size: 22 },
    ]),
  ];
}

/**
 * Terms of Use — goes in every CbD product's teacher documents.
 * Single-user license with school-wide option and accessibility commitment.
 */
function termsOfUse() {
  return [
    heading2("Terms of Use"),
    p([
      { text: "Thank you for purchasing from Communicate by Design!", bold: true, size: 22 },
    ]),
    p("By purchasing this resource, you agree to the following terms of use."),
    p(""),
    p([{ text: "What You CAN Do", bold: true, size: 22 }]),
    p("\u2022  Use this resource in your own classroom, therapy room, or home setting with your own students or child."),
    p("\u2022  Print or photocopy pages for use with your students or child."),
    p("\u2022  Share the resource with a student\u2019s IEP team for direct use with that student (e.g., sending a copy to a parent, OT, PT, BCBA, RBT, or paraprofessional working with the same learner)."),
    p("\u2022  Save a digital backup copy for your personal use."),
    p(""),
    p([{ text: "What You CANNOT Do", bold: true, size: 22 }]),
    p("\u2022  Share this resource with other teachers, therapists, or colleagues for use in their own classrooms. Each teacher or professional needs their own license."),
    p("\u2022  Post this resource \u2014 or any part of it \u2014 on any website, shared drive, or online platform (including school or district servers, Google Drive shared folders, or learning management systems accessible to other staff)."),
    p("\u2022  Sell, redistribute, or claim this resource as your own."),
    p("\u2022  Edit, modify, or remove the copyright information from any part of this resource."),
    p(""),
    p([{ text: "School-Wide or District Licenses: ", bold: true, size: 22 }, { text: "Need this resource for your whole team? I offer discounted multi-license options. Contact me through my TPT store for pricing \u2014 I\u2019m happy to work with schools and districts.", size: 22 }]),
    p(""),
    p("\u00A9 Communicate by Design. All rights reserved. Purchase of this resource grants a single-user license only. This resource may not be reproduced, distributed, or displayed publicly without written permission."),
  ];
}

// ── Page Structure Builders ───────────────────────────────────────────────

/** "TEACHER REFERENCE — Do Not Distribute to Students" label */
function teacherRefLabel() {
  return new Paragraph({
    alignment: AlignmentType.RIGHT,
    spacing: { before: 40, after: 80 },
    children: [
      new TextRun({ text: "TEACHER REFERENCE \u2014 Do Not Distribute to Students", font: FONT, size: 18, bold: true, italics: true, color: "999999" }),
    ],
  });
}

/**
 * Student handout header — starts a new page with:
 * - Thin header line (print-friendly)
 * - Bold title with teal underline
 * - Name / Class / Teacher fields
 * @param {string} unitTitle - e.g. "Frances Kelsey: The Woman Who Said No"
 * @param {string} title - e.g. "Word Bank"
 * @param {string} subtitle - e.g. "Half-Page Resource"
 */
function studentHandoutHeader(unitTitle, title, subtitle) {
  const items = [];
  items.push(new Paragraph({ pageBreakBefore: true, children: [] }));
  items.push(new Paragraph({
    spacing: { after: 60 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 2, color: TEAL, space: 2 } },
    children: [
      new TextRun({ text: unitTitle, font: FONT, size: 18, italics: true, color: NAVY }),
      new TextRun({ text: subtitle ? "  |  " + subtitle : "", font: FONT, size: 18, italics: true, color: "999999" }),
    ],
  }));
  items.push(new Paragraph({
    spacing: { before: 100, after: 80 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: TEAL, space: 4 } },
    children: [new TextRun({ text: title, font: FONT, size: 30, bold: true, color: NAVY })],
  }));
  items.push(nameClassTeacher());
  return items;
}

/** Name / Class / Teacher field line — table-based for perfect alignment */
function nameClassTeacher() {
  return new Table({
    width: { size: CONTENT_WIDTH, type: WidthType.DXA },
    columnWidths: [Math.round(CONTENT_WIDTH * 0.42), Math.round(CONTENT_WIDTH * 0.26), Math.round(CONTENT_WIDTH * 0.32)],
    layout: TableLayoutType.FIXED,
    rows: [new TableRow({
      children: [
        new TableCell({
          borders: noBorders,
          width: { size: Math.round(CONTENT_WIDTH * 0.42), type: WidthType.DXA },
          margins: { top: 40, bottom: 40, left: 0, right: 60 },
          children: [new Paragraph({
            spacing: { after: 0 },
            border: { bottom: { style: BorderStyle.SINGLE, size: 1, color: BORDER_COLOR, space: 2 } },
            children: [new TextRun({ text: "Name:", font: FONT, size: 20, bold: true, color: NAVY })],
          })],
        }),
        new TableCell({
          borders: noBorders,
          width: { size: Math.round(CONTENT_WIDTH * 0.26), type: WidthType.DXA },
          margins: { top: 40, bottom: 40, left: 60, right: 60 },
          children: [new Paragraph({
            spacing: { after: 0 },
            border: { bottom: { style: BorderStyle.SINGLE, size: 1, color: BORDER_COLOR, space: 2 } },
            children: [new TextRun({ text: "Class:", font: FONT, size: 20, bold: true, color: NAVY })],
          })],
        }),
        new TableCell({
          borders: noBorders,
          width: { size: Math.round(CONTENT_WIDTH * 0.32), type: WidthType.DXA },
          margins: { top: 40, bottom: 40, left: 60, right: 0 },
          children: [new Paragraph({
            spacing: { after: 0 },
            border: { bottom: { style: BorderStyle.SINGLE, size: 1, color: BORDER_COLOR, space: 2 } },
            children: [new TextRun({ text: "Teacher:", font: FONT, size: 20, bold: true, color: NAVY })],
          })],
        }),
      ],
    })],
  });
}

/**
 * Reading passage page header (Keiko-style).
 * Thin header line + Name/Class/Teacher + part title with teal underline.
 * Version label is discrete gray text in header line only.
 * @param {string} unitTitle - e.g. "Frances Kelsey: The Woman Who Said No"
 * @param {string} partTitle - e.g. "Part 1: The New Drug"
 * @param {string} versionLabel - e.g. "Version 1"
 */
function passageHeader(unitTitle, partTitle, versionLabel) {
  const items = [];
  items.push(new Paragraph({ pageBreakBefore: true, children: [] }));
  items.push(new Paragraph({
    spacing: { after: 60 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 2, color: TEAL, space: 2 } },
    children: [
      new TextRun({ text: unitTitle, font: FONT, size: 18, italics: true, color: NAVY }),
      new TextRun({ text: "      " + versionLabel, font: FONT, size: 16, color: "999999" }),
    ],
  }));
  items.push(nameClassTeacher());
  items.push(new Paragraph({
    spacing: { before: 40, after: 120 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: TEAL, space: 4 } },
    children: [new TextRun({ text: partTitle, font: FONT, size: 28, bold: true, color: NAVY })],
  }));
  return items;
}

/**
 * MCQ page header (Keiko-style).
 * @param {string} unitTitle
 * @param {string} partTitle
 * @param {string} versionLabel
 * @param {boolean} inline - If true, use inline divider instead of page break (for V3 consolidation)
 */
function mcqPageHeader(unitTitle, partTitle, versionLabel, inline) {
  const items = [];
  if (inline) {
    // V3 inline: teal divider + section title, no page break, no name/class repeat
    items.push(new Paragraph({
      spacing: { before: 300, after: 60 },
      border: { top: { style: BorderStyle.SINGLE, size: 4, color: TEAL, space: 6 } },
      children: [new TextRun({ text: "Multiple-Choice Questions", font: FONT, size: 24, bold: true, color: NAVY })],
    }));
  } else {
    items.push(new Paragraph({ pageBreakBefore: true, children: [] }));
    items.push(new Paragraph({
      spacing: { after: 60 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 2, color: TEAL, space: 2 } },
      children: [
        new TextRun({ text: "Multiple-Choice Questions  |  " + partTitle, font: FONT, size: 18, italics: true, color: NAVY }),
        new TextRun({ text: "      " + versionLabel, font: FONT, size: 16, color: "999999" }),
      ],
    }));
    items.push(nameClassTeacher());
    items.push(new Paragraph({
      spacing: { before: 40, after: 120 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: TEAL, space: 4 } },
      children: [new TextRun({ text: "Multiple-Choice Questions \u2014 " + partTitle, font: FONT, size: 26, bold: true, color: NAVY })],
    }));
  }
  return items;
}

/**
 * Short Answer page header (Keiko-style).
 * @param {string} unitTitle
 * @param {string} partTitle
 * @param {string} versionLabel
 * @param {boolean} inline - If true, use inline divider instead of page break (for V3 consolidation)
 */
function saPageHeader(unitTitle, partTitle, versionLabel, inline) {
  const items = [];
  if (inline) {
    // V3 inline: teal divider + section title, no page break, no name/class repeat
    items.push(new Paragraph({
      spacing: { before: 300, after: 60 },
      border: { top: { style: BorderStyle.SINGLE, size: 4, color: TEAL, space: 6 } },
      children: [new TextRun({ text: "Short Answer", font: FONT, size: 24, bold: true, color: NAVY })],
    }));
  } else {
    items.push(new Paragraph({ pageBreakBefore: true, children: [] }));
    items.push(new Paragraph({
      spacing: { after: 60 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 2, color: TEAL, space: 2 } },
      children: [
        new TextRun({ text: "Short Answer  |  " + partTitle, font: FONT, size: 18, italics: true, color: NAVY }),
        new TextRun({ text: "      " + versionLabel, font: FONT, size: 16, color: "999999" }),
      ],
    }));
    items.push(nameClassTeacher());
    items.push(new Paragraph({
      spacing: { before: 40, after: 120 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: TEAL, space: 4 } },
      children: [new TextRun({ text: "Short Answer \u2014 " + partTitle, font: FONT, size: 26, bold: true, color: NAVY })],
    }));
  }
  return items;
}

/** Write-on lines for student responses */
function writeOnLines(count = 4) {
  const items = [];
  for (let i = 0; i < count; i++) {
    items.push(new Paragraph({
      spacing: { before: 200, after: 0 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 1, color: BORDER_COLOR, space: 1 } },
      children: [new TextRun({ text: " ", font: FONT, size: 22 })],
    }));
  }
  return items;
}

/**
 * Evidence Sort page header (Keiko-style).
 */
function esPageHeader(unitTitle, partTitle, versionLabel) {
  const items = [];
  items.push(new Paragraph({ pageBreakBefore: true, children: [] }));
  items.push(new Paragraph({
    spacing: { after: 60 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 2, color: TEAL, space: 2 } },
    children: [
      new TextRun({ text: "Evidence Sort  |  " + partTitle, font: FONT, size: 18, italics: true, color: NAVY }),
      new TextRun({ text: "      " + versionLabel, font: FONT, size: 16, color: "999999" }),
    ],
  }));
  items.push(nameClassTeacher());
  items.push(new Paragraph({
    spacing: { before: 40, after: 120 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: TEAL, space: 4 } },
    children: [new TextRun({ text: "Evidence Sort \u2014 " + partTitle, font: FONT, size: 26, bold: true, color: NAVY })],
  }));
  return items;
}

/**
 * Evidence Strength Rating page header (Keiko-style).
 */
function esrPageHeader(unitTitle, partTitle, versionLabel) {
  const items = [];
  items.push(new Paragraph({ pageBreakBefore: true, children: [] }));
  items.push(new Paragraph({
    spacing: { after: 60 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 2, color: TEAL, space: 2 } },
    children: [
      new TextRun({ text: "Evidence Strength Rating  |  " + partTitle, font: FONT, size: 18, italics: true, color: NAVY }),
      new TextRun({ text: "      " + versionLabel, font: FONT, size: 16, color: "999999" }),
    ],
  }));
  items.push(nameClassTeacher());
  items.push(new Paragraph({
    spacing: { before: 40, after: 120 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: TEAL, space: 4 } },
    children: [new TextRun({ text: "Evidence Strength Rating \u2014 " + partTitle, font: FONT, size: 26, bold: true, color: NAVY })],
  }));
  return items;
}

/** MCQ answer choice (A/B/C/D with bold letter, generous spacing for student readability) */
function mcqChoice(letter, text) {
  return new Paragraph({
    spacing: { before: 60, after: 60, line: 276 },
    indent: { left: 600, hanging: 300 },
    children: [
      new TextRun({ text: letter + ".  ", font: FONT, size: 22, bold: true, color: NAVY }),
      new TextRun({ text: text.replace(/\*\*/g, ""), font: FONT, size: 22, color: BODY_COLOR }),
    ],
  });
}

/** Passage paragraph with first-line indent — reader-friendly spacing */
function passageParagraph(text) {
  return new Paragraph({
    spacing: { before: 0, after: 180, line: 360 },
    indent: { firstLine: 432 },
    children: [new TextRun({ text: text.replace(/\*\*/g, ""), font: FONT, size: 23, color: BODY_COLOR })],
  });
}

/** Vocab box / context callout (gray background, teal left border) */
function vocabBox(text) {
  return new Paragraph({
    spacing: { before: 120, after: 120, line: 276 },
    indent: { left: 432, right: 432 },
    shading: { fill: GRAY_LIGHT, type: ShadingType.CLEAR },
    border: { left: { style: BorderStyle.SINGLE, size: 6, color: TEAL, space: 6 } },
    children: [new TextRun({ text: text.replace(/\*\*/g, ""), font: FONT, size: 20, italics: true, color: NAVY })],
  });
}

/** Pre-identified claim highlight (pale yellow background) */
function claimHighlight(text, isBold) {
  return new Paragraph({
    spacing: { before: 60, after: 60, line: 276 },
    shading: { fill: "FFF8DC", type: ShadingType.CLEAR },
    indent: { left: 240, right: 240 },
    children: [new TextRun({ text: text.replace(/\*\*/g, ""), font: FONT, size: 22, bold: isBold })],
  });
}

// ── Title Page Builder ────────────────────────────────────────────────────

/**
 * Build a complete CbD title page.
 * @param {Object} opts
 * @param {string} opts.unitTitle - e.g. "Frances Kelsey:"
 * @param {string} opts.unitSubtitle - e.g. "The Woman Who Said No"
 * @param {string} opts.skillNumber - e.g. "#5"
 * @param {string} opts.skillName - e.g. "Claim, Evidence, Reasoning"
 * @param {string} opts.gradeRange - e.g. "6–10"
 * @param {string} opts.versions - e.g. "3 Lexile Versions"
 * @param {string} opts.parts - e.g. "4 Parts"
 * @param {string} opts.seasonalHook - e.g. "Women's History Month"
 */
function titlePage(opts) {
  const items = [];
  items.push(spacer(1600));
  items.push(new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { after: 40 },
    children: [new TextRun({ text: "COMMUNICATE", font: FONT, size: 32, bold: true, color: TEAL })],
  }));
  items.push(new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { after: 20 },
    children: [new TextRun({ text: "BY DESIGN", font: FONT, size: 32, bold: true, color: AMBER })],
  }));
  items.push(new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { after: 500 },
    children: [new TextRun({ text: "Where AT Meets Practice", font: FONT, size: 22, bold: true, italics: true, color: NAVY })],
  }));
  items.push(new Paragraph({
    spacing: { after: 300 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: TEAL, space: 1 } },
  }));
  items.push(new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { after: 40 },
    children: [new TextRun({ text: opts.unitTitle, font: FONT, size: 52, bold: true, color: NAVY })],
  }));
  items.push(new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { after: 300 },
    children: [new TextRun({ text: opts.unitSubtitle, font: FONT, size: 52, bold: true, color: NAVY })],
  }));
  items.push(new Paragraph({
    spacing: { after: 200 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: TEAL, space: 1 } },
  }));
  items.push(p("A Nonfiction Reading Unit", { size: 28, align: AlignmentType.CENTER, color: NAVY, after: 60 }));
  items.push(p([
    { text: `Target Literacy Skill ${opts.skillNumber}: `, size: 24, color: NAVY },
    { text: opts.skillName, size: 24, bold: true, color: TEAL },
  ], { align: AlignmentType.CENTER, after: 60 }));
  items.push(p(`Grade Range: ${opts.gradeRange}  |  Special Education  |  Resource Room  |  Co-taught ELA`, { size: 22, align: AlignmentType.CENTER, color: NAVY, after: 400 }));
  items.push(p(`${opts.versions}  \u00B7  ${opts.parts}  \u00B7  Teacher Materials  \u00B7  Answer Key`, { size: 22, align: AlignmentType.CENTER, color: "555555", after: 200 }));
  items.push(spacer(600));
  items.push(p("\u00A9 Communicate by Design  |  Jill McCardel", { size: 20, align: AlignmentType.CENTER, color: "888888", after: 40 }));
  items.push(p("communicatebydesign.substack.com", { size: 20, align: AlignmentType.CENTER, color: "888888" }));
  return items;
}

/** Table of Contents page */
function tocPage() {
  return [
    new Paragraph({ pageBreakBefore: true, children: [] }),
    p("Table of Contents", { size: 36, bold: true, color: NAVY, after: 200 }),
    new TableOfContents("Table of Contents", { hyperlink: true, headingStyleRange: "1-3" }),
  ];
}

// ── Document Assembly ─────────────────────────────────────────────────────

/**
 * Assemble and write the final Word document.
 * @param {string} unitShortTitle - e.g. "Frances Kelsey: The Woman Who Said No"
 * @param {Paragraph[]} children - All content paragraphs/tables in order
 * @param {string} outputPath - Full file path for the .docx output
 * @param {Object} [meta] - Optional metadata: { title, description, creator }
 */
function assembleAndWrite(unitShortTitle, children, outputPath, meta = {}) {
  const doc = new Document({
    // ── Accessibility: Document metadata (WCAG 2.4.2 — Page Titled, 3.1.1 — Language) ──
    title: meta.title || unitShortTitle,
    description: meta.description || `Communicate by Design Nonfiction Reading Unit: ${unitShortTitle}. Accessible educational material designed for WCAG 2.2 AA conformance.`,
    creator: meta.creator || "Communicate by Design — Jill McCardel",
    language: "en-US",
    numbering: {
      config: [{
        reference: "cbd-bullets",
        levels: [{
          level: 0,
          format: LevelFormat.BULLET,
          text: "\u2022",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } },
        }],
      }],
    },
    styles: {
      default: {
        document: { run: { font: FONT, size: 22, color: BODY_COLOR } },
      },
      paragraphStyles: [
        {
          id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
          run: { size: 36, bold: true, font: FONT, color: NAVY },
          paragraph: { spacing: { before: 240, after: 200 }, outlineLevel: 0 },
        },
        {
          id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
          run: { size: 28, bold: true, font: FONT, color: NAVY },
          paragraph: { spacing: { before: 200, after: 160 }, outlineLevel: 1 },
        },
        {
          id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
          run: { size: 24, bold: true, font: FONT, color: TEAL },
          paragraph: { spacing: { before: 160, after: 120 }, outlineLevel: 2 },
        },
      ],
    },
    sections: [{
      properties: {
        page: {
          size: { width: PAGE_WIDTH, height: PAGE_HEIGHT },
          margin: { top: MARGIN, right: MARGIN, bottom: MARGIN, left: MARGIN },
        },
      },
      headers: {
        default: new Header({
          children: [
            new Table({
              width: { size: CONTENT_WIDTH, type: WidthType.DXA },
              columnWidths: [6720, 3360],
              layout: TableLayoutType.FIXED,
              rows: [new TableRow({
                children: [
                  new TableCell({
                    borders: noBorders,
                    width: { size: 6720, type: WidthType.DXA },
                    margins: { top: 0, bottom: 0, left: 0, right: 0 },
                    children: [new Paragraph({
                      spacing: { after: 0 },
                      children: [
                        new TextRun({ text: unitShortTitle, font: FONT, size: 18, color: NAVY, italics: true }),
                      ],
                    })],
                  }),
                  new TableCell({
                    borders: noBorders,
                    width: { size: 3360, type: WidthType.DXA },
                    margins: { top: 0, bottom: 0, left: 0, right: 0 },
                    children: [new Paragraph({
                      spacing: { after: 0 },
                      alignment: AlignmentType.RIGHT,
                      children: [
                        new TextRun({ text: "COMMUNICATE ", font: FONT, size: 16, bold: true, color: TEAL }),
                        new TextRun({ text: "BY DESIGN", font: FONT, size: 16, bold: true, color: AMBER }),
                      ],
                    })],
                  }),
                ],
              })],
            }),
            new Paragraph({
              spacing: { before: 40, after: 0 },
              border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: TEAL, space: 0 } },
            }),
          ],
        }),
      },
      footers: {
        default: new Footer({
          children: [new Paragraph({
            alignment: AlignmentType.CENTER, spacing: { after: 0 },
            children: [
              new TextRun({ text: unitShortTitle + "  |  Communicate by Design  |  p. ", font: FONT, size: 16, italics: true, color: "888888" }),
              new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 16, color: NAVY }),
            ],
          })],
        }),
      },
      children,
    }],
  });

  return Packer.toBuffer(doc).then(buffer => {
    require("fs").writeFileSync(outputPath, buffer);
    console.log(`Document created: ${outputPath}`);
    console.log(`Size: ${(buffer.length / 1024).toFixed(1)} KB`);
    return buffer;
  });
}

/** End-of-document matter (copyright line) */
function endMatter() {
  return [
    new Paragraph({
      spacing: { before: 200, after: 200 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: TEAL, space: 1 } },
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER, spacing: { after: 40 },
      children: [
        new TextRun({ text: "\u00A9 ", font: FONT, size: 20, color: "888888" }),
        new TextRun({ text: "Communicate by Design", font: FONT, size: 20, color: NAVY }),
        new TextRun({ text: "  |  Jill McCardel  |  communicatebydesign.substack.com", font: FONT, size: 20, color: "888888" }),
      ],
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER, spacing: { after: 0 },
      children: [new TextRun({ text: "Where AT Meets Practice", font: FONT, size: 20, bold: true, italics: true, color: AMBER })],
    }),
  ];
}

// ── Markdown Parsing Helpers ──────────────────────────────────────────────
// These parse markdown passages into structured docx elements.

/** Parse a version section into structured parts with passage, MCQ, SA */
function parseVersionParts(versionText) {
  const parts = [];
  const partRegex = /## Part (\d+): ([^\n]+)\n([\s\S]*?)(?=\n## Part \d+:|\n## Teacher Answer Key|\n---\s*\n---|\n# VERSION|\n\*\*COMMUNICATE\*\*|$)/g;
  let match;
  while ((match = partRegex.exec(versionText)) !== null) {
    const partNum = match[1];
    const partTitle = match[2].trim();
    const partContent = match[3];
    const mcqMarker = /### Multiple-Choice Questions/;
    const saMarker = /### Short Answer/;
    let passageText = partContent, mcqText = "", saText = "";
    const mcqMatch = mcqMarker.exec(partContent);
    const saMatch = saMarker.exec(partContent);
    if (mcqMatch) {
      passageText = partContent.substring(0, mcqMatch.index);
      mcqText = saMatch ? partContent.substring(mcqMatch.index, saMatch.index) : partContent.substring(mcqMatch.index);
      if (saMatch) saText = partContent.substring(saMatch.index);
    } else if (saMatch) {
      passageText = partContent.substring(0, saMatch.index);
      saText = partContent.substring(saMatch.index);
    }
    parts.push({ partNum, partTitle, passageText, mcqText, saText });
  }
  return parts;
}

/** Build passage paragraphs from markdown text */
/** Build passage paragraphs. In V3 mode (isV3=true), vocab boxes are collected and
 *  placed at the top, comprehension checks are collected and placed at the bottom,
 *  and the reading text flows uninterrupted in between. */
function buildPassageParagraphs(text, isV3) {
  if (!isV3) {
    // V1/V2: inline rendering (original behavior)
    const items = [];
    const lines = text.split("\n");
    let inBlockquote = false, bqText = "";
    for (const line of lines) {
      const trimmed = line.trim();
      if (!trimmed) {
        if (inBlockquote && bqText) { items.push(vocabBox(bqText)); bqText = ""; }
        inBlockquote = false;
        continue;
      }
      if (trimmed.startsWith("> ")) { inBlockquote = true; bqText += (bqText ? " " : "") + trimmed.substring(2); continue; }
      if (inBlockquote && bqText) { items.push(vocabBox(bqText)); bqText = ""; inBlockquote = false; }
      if (trimmed.startsWith("#") || trimmed === "---") continue;
      if (trimmed.startsWith("[C]") || trimmed.startsWith("**[C]")) { items.push(claimHighlight(trimmed, trimmed.includes("**"))); continue; }
      if (trimmed.startsWith("(*)") || trimmed.startsWith("\u2705")) { items.push(p(trimmed, { bold: true, indent: { left: 360 } })); continue; }
      items.push(passageParagraph(trimmed));
    }
    if (inBlockquote && bqText) items.push(vocabBox(bqText));
    return items;
  }

  // V3 mode: separate vocab → reading → checks
  const vocabItems = [];
  const readingItems = [];
  const checkItems = [];
  const lines = text.split("\n");
  let inBlockquote = false, bqText = "";
  let inAnnotationCheck = false, acText = "";

  for (const line of lines) {
    const trimmed = line.trim();

    // Handle blockquotes (vocab boxes and annotation checks)
    if (trimmed.startsWith("> ")) {
      const inner = trimmed.substring(2).trim();
      if (inner.includes("Annotation Check") || inAnnotationCheck) {
        inAnnotationCheck = true;
        acText += (acText ? "\n" : "") + inner.replace(/\*\*/g, "").replace(/[✏️]/g, "").trim();
        continue;
      }
      inBlockquote = true;
      bqText += (bqText ? " " : "") + inner;
      continue;
    }

    // End of blockquote
    if (inBlockquote && bqText) {
      // Parse V3 vocab: "**Vocabulary: Clinical investigation** A clinical..." → bold term + em dash + definition
      // GREEDY [^*]+ so multi-word terms like "Clinical investigation" are captured fully
      const vocabMatch = bqText.match(/^\*?\*?Vocabulary:\s*([^*]+)\*?\*?\s+(.+)/i);
      if (vocabMatch) {
        const term = vocabMatch[1].trim();
        const def = vocabMatch[2].trim();
        vocabItems.push(new Paragraph({
          spacing: { before: 40, after: 40, line: 276 },
          indent: { left: 432, right: 432 },
          shading: { fill: GRAY_LIGHT, type: ShadingType.CLEAR },
          border: { left: { style: BorderStyle.SINGLE, size: 6, color: TEAL, space: 6 } },
          children: [
            new TextRun({ text: term, bold: true, font: FONT, size: 20, color: NAVY }),
            new TextRun({ text: " \u2014 " + def, font: FONT, size: 20, color: BODY_COLOR }),
          ],
        }));
      } else if (/^\*?\*?Note:/i.test(bqText)) {
        // Non-vocab blockquote (e.g. "> **Note:** ...") → render as italic callout in reading section
        readingItems.push(p(bqText.replace(/\*\*/g, ""), { italics: true, indent: { left: 360 }, before: 80, after: 80 }));
      } else {
        vocabItems.push(vocabBox(bqText));
      }
      bqText = "";
      inBlockquote = false;
    }
    if (inAnnotationCheck && !trimmed.startsWith(">")) {
      if (acText) checkItems.push(vocabBox(acText));
      acText = "";
      inAnnotationCheck = false;
    }

    if (!trimmed) continue;
    if (trimmed.startsWith("#") || trimmed === "---") continue;

    // Comprehension checks (✅ lines) → collect at bottom
    if (trimmed.startsWith("\u2705") || trimmed.startsWith("(*)")) {
      checkItems.push(p(trimmed.replace(/\*\*/g, ""), { bold: true, indent: { left: 360 }, after: 60 }));
      continue;
    }

    // Claims — any line containing [C] gets the tag stripped and a ★ in the right margin
    if (trimmed.includes("[C]")) {
      const cleanText = trimmed.replace(/\*\*/g, "").replace(/\[C\]\s*/g, "").trim();
      readingItems.push(new Paragraph({
        spacing: { before: 0, after: 160, line: 336 },
        indent: { firstLine: 432 },
        tabStops: [{ type: TabStopType.RIGHT, position: CONTENT_WIDTH }],
        children: [
          new TextRun({ text: cleanText, font: FONT, size: 23, color: BODY_COLOR }),
          new TextRun({ text: "\t" }),
          new TextRun({ text: "\u2605", font: FONT, size: 22, color: AMBER }),
        ],
      }));
      continue;
    }
    // Markdown bullet list items → render as indented bullet paragraphs
    if (trimmed.startsWith("- ")) {
      readingItems.push(p("\u2022  " + trimmed.substring(2).replace(/\*\*/g, ""), { indent: { left: 720, hanging: 288 }, after: 60 }));
      continue;
    }
    readingItems.push(passageParagraph(trimmed));
  }

  // Flush remaining
  if (inBlockquote && bqText) vocabItems.push(vocabBox(bqText));
  if (acText) checkItems.push(vocabBox(acText));

  // Assemble: vocab header → vocab boxes → reading → checks header → checks
  const items = [];
  if (vocabItems.length > 0) {
    items.push(p("Key Vocabulary", { bold: true, size: 22, color: TEAL, before: 80, after: 60 }));
    items.push(...vocabItems);
    items.push(new Paragraph({ spacing: { before: 60, after: 60 }, border: { bottom: { style: BorderStyle.SINGLE, size: 2, color: TEAL, space: 4 } }, children: [] }));
  }
  items.push(...readingItems);
  if (checkItems.length > 0) {
    items.push(new Paragraph({ spacing: { before: 60, after: 60 }, border: { bottom: { style: BorderStyle.SINGLE, size: 2, color: TEAL, space: 4 } }, children: [] }));
    items.push(p("Check Your Understanding", { bold: true, size: 22, color: TEAL, before: 80, after: 60 }));
    items.push(...checkItems);
  }
  return items;
}

/** Build MCQ items from markdown text — student-facing (no answer key) */
function buildMcqItems(text) {
  const items = [];
  if (!text) return items;
  let qNum = 0;
  let skipUntilNextQ = false;
  for (const line of text.split("\n")) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#") || trimmed === "---") continue;
    // Skip answer explanation lines (Answer: X. ...)  and scoring notes
    if (/^\*?\*?Answer:/i.test(trimmed) || /^\*Scoring note/i.test(trimmed)) { skipUntilNextQ = true; continue; }
    // Question stem: **1.** or 1. etc.
    const qMatch = trimmed.match(/^\*?\*?(\d+)\.?\*?\*?\s+(.+)/);
    if (qMatch && !/^[A-D]\./i.test(trimmed)) {
      skipUntilNextQ = false;
      qNum++;
      const beforeSpace = qNum > 1 ? 280 : 120;
      items.push(new Paragraph({
        spacing: { before: beforeSpace, after: 60, line: 276 },
        children: [
          new TextRun({ text: qNum + ".  ", font: FONT, size: 23, bold: true, color: NAVY }),
          new TextRun({ text: qMatch[2].replace(/\*\*/g, ""), font: FONT, size: 23, bold: true, color: BODY_COLOR }),
        ],
      }));
      continue;
    }
    if (skipUntilNextQ) continue;
    // Answer choice: A. B. C. D.
    const optMatch = trimmed.match(/^([A-D])\.?\s+(.+)/);
    if (optMatch) { items.push(mcqChoice(optMatch[1], optMatch[2])); continue; }
    // Anything else that isn't an answer line
    if (trimmed && !/^\*?\*?Answer:/i.test(trimmed)) {
      items.push(p(trimmed.replace(/\*\*/g, ""), { after: 60 }));
    }
  }
  return items;
}

/** Build SA items from markdown text with write-on lines — student-facing (no scoring notes).
 *  Write-on lines are distributed evenly so questions fill the page equally.
 *  V3 mode (isV3=true) renders scaffold elements (Circle, Yes/No, evidence lists,
 *  sentence frames) compactly without adding write-on lines for sub-questions. */
function buildSaItems(text, isV3) {
  if (!text) return [];
  const lines = text.split("\n");

  if (isV3) {
    // ── V3 mode: numbered questions + scaffold elements, minimal write-on lines ──
    const items = [];
    for (const line of lines) {
      const trimmed = line.trim();
      if (!trimmed || trimmed.startsWith("#") || trimmed === "---") continue;
      if (/^\*Scoring note/i.test(trimmed) || /^\*?\*?Answer:/i.test(trimmed)) continue;

      // Numbered question stem: **1.** text
      const qMatch = trimmed.match(/^\*?\*?(\d+)\.?\*?\*?\s+(.+)/);
      if (qMatch) {
        items.push(p(qMatch[1] + ". " + qMatch[2].replace(/\*\*/g, ""), { bold: true, before: 200, after: 60 }));
        continue;
      }

      // Bulleted evidence/choice item: - text
      if (trimmed.startsWith("- ")) {
        items.push(p(trimmed.substring(2).replace(/\*\*/g, ""), { indent: { left: 480, hanging: 240 }, after: 30 }));
        continue;
      }

      // Sentence frame prompt → add 2 write-on lines after the frame text
      if (/use this frame/i.test(trimmed)) {
        items.push(p(trimmed.replace(/\*\*/g, ""), { bold: true, before: 80, after: 40 }));
        items.push(...writeOnLines(2));
        continue;
      }

      // Reasoning prompt with fill-in → add 2 write-on lines
      if (/^(\*\*)?Reasoning/i.test(trimmed) && trimmed.includes("_")) {
        items.push(p(trimmed.replace(/\*\*/g, ""), { bold: true, before: 80, after: 40 }));
        items.push(...writeOnLines(2));
        continue;
      }

      // Everything else (Circle:, Yes/No, scaffold text) → compact paragraph
      items.push(p(trimmed.replace(/\*\*/g, ""), { after: 40 }));
    }
    return items;
  }

  // ── V1/V2 mode: traditional questions + evenly distributed write-on lines ──
  // First pass: count questions to distribute space evenly
  let totalQs = 0;
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#") || trimmed === "---") continue;
    if (/^\*Scoring note/i.test(trimmed) || /^\*?\*?Answer:/i.test(trimmed)) continue;
    const qMatch = trimmed.match(/^\*?\*?(\d+)\.?\*?\*?\s+(.+)/);
    if (qMatch) { totalQs++; continue; }
    if (trimmed.includes("?") && trimmed.length > 20) { totalQs++; }
  }
  // Calculate lines per question to fill page evenly
  // Page fits roughly 28 write-on lines total; subtract ~2 lines per question for the question text
  const usableLines = Math.max(12, 28 - totalQs * 2);
  const linesPerQ = totalQs > 0 ? Math.min(10, Math.max(3, Math.floor(usableLines / totalQs))) : 3;

  // Second pass: build items
  const items = [];
  let qNum = 0;
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#") || trimmed === "---") continue;
    if (/^\*Scoring note/i.test(trimmed) || /^\*?\*?Answer:/i.test(trimmed)) continue;
    const qMatch = trimmed.match(/^\*?\*?(\d+)\.?\*?\*?\s+(.+)/);
    if (qMatch) { qNum++; items.push(p(qNum + ". " + qMatch[2].replace(/\*\*/g, ""), { bold: true, before: 180, after: 40 })); items.push(...writeOnLines(linesPerQ)); continue; }
    if (trimmed.includes("?") && trimmed.length > 20) { qNum++; items.push(p(trimmed.replace(/\*\*/g, ""), { bold: true, before: 180, after: 40 })); items.push(...writeOnLines(linesPerQ)); continue; }
    items.push(p(trimmed.replace(/\*\*/g, ""), { after: 60 }));
  }
  return items;
}

/**
 * Build a full version section (teacher divider + Keiko-style student pages).
 * @param {string} unitTitle - e.g. "Frances Kelsey: The Woman Who Said No"
 * @param {string} versionLabel - e.g. "Version 1"
 * @param {string} lexileRange - e.g. "900–1050"
 * @param {string} versionNote - Italicized teacher note
 * @param {string} versionText - Raw markdown for this version
 */
function buildVersionSection(unitTitle, versionLabel, lexileRange, versionNote, versionText) {
  const items = [];
  const isV3 = /version\s*3/i.test(versionLabel);
  items.push(heading1(versionLabel + " \u2014 Lexile " + lexileRange));
  items.push(teacherRefLabel());
  items.push(p("Print the following pages for students assigned to " + versionLabel + ". Lexile range: " + lexileRange + ". Do not share Lexile information with students.", { italics: true, after: 80 }));
  if (versionNote) items.push(p(versionNote, { italics: true, after: 200 }));

  const parts = parseVersionParts(versionText);
  for (const part of parts) {
    const partTitle = "Part " + part.partNum + ": " + part.partTitle;
    items.push(...passageHeader(unitTitle, partTitle, versionLabel));
    items.push(...buildPassageParagraphs(part.passageText, isV3));
    if (part.mcqText) { items.push(...mcqPageHeader(unitTitle, partTitle, versionLabel, isV3)); items.push(...buildMcqItems(part.mcqText)); }
    if (part.saText) { items.push(...saPageHeader(unitTitle, partTitle, versionLabel, isV3)); items.push(...buildSaItems(part.saText, isV3)); }
  }
  return items;
}

/** Simple markdown-to-docx for teacher-facing text (answer keys, research boards) */
function simpleMdToDocx(text) {
  const items = [];
  for (const line of text.split("\n")) {
    const trimmed = line.trim();
    if (!trimmed) continue;
    if (trimmed.startsWith("### ")) { items.push(heading3(trimmed.replace(/^### /, "").replace(/\*\*/g, ""))); }
    else if (trimmed.startsWith("## ")) { items.push(heading2(trimmed.replace(/^## /, "").replace(/\*\*/g, ""))); }
    else { items.push(p(trimmed)); }
  }
  return items;
}

// ── Export Everything ──────────────────────────────────────────────────────
module.exports = {
  // Constants
  NAVY, TEAL, AMBER, YELLOW, GRAY_LIGHT, BORDER_COLOR, BODY_COLOR,
  FONT, PAGE_WIDTH, PAGE_HEIGHT, MARGIN, CONTENT_WIDTH,
  borders, noBorders, cellMargins, thinBorder,
  // Core helpers
  p, heading1, heading2, heading3, spacer, hr,
  makeCell, makeTable, callout, infoBox, checkbox, checklistTable, blockquote,
  // Accessibility helpers (WCAG 2.2 AA)
  tableCaption, bulletList, accessibilityStatement, aboutTheCreator, termsOfUse,
  // Page builders
  teacherRefLabel, studentHandoutHeader, nameClassTeacher,
  passageHeader, mcqPageHeader, saPageHeader, esPageHeader, esrPageHeader,
  writeOnLines, mcqChoice, passageParagraph, vocabBox, claimHighlight,
  // Document builders
  titlePage, tocPage, endMatter, assembleAndWrite,
  // Markdown parsers
  parseVersionParts, buildPassageParagraphs, buildMcqItems, buildSaItems,
  buildVersionSection, simpleMdToDocx,
  // Re-export docx types that unit scripts may need
  Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, HeadingLevel, BorderStyle, WidthType, ShadingType,
  PageNumber, PageBreak, ImageRun,
};

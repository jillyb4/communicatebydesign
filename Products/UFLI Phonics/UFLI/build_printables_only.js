#!/usr/bin/env node
/**
 * UFLI Printables-Only Builder — Communicate by Design
 *
 * Generates a single .docx with ONLY the physical manipulatives
 * that need to be printed in color, cut, and used:
 *   1. Symbol cards (labeled: word + ARASAAC image + core/fringe tag)
 *   2. Symbol-only reading practice cards (image only, no labels)
 *   3. Heart word cards
 *
 * EXCLUDES: cover pages, lesson info tables, step tables, review word
 * binder lists, morphology notes, data trackers, attribution pages.
 *
 * These are the COLOR PRINT pages. Everything else lives in the spiral notebook.
 *
 * Usage:
 *   node build_printables_only.js
 */

const path = require('path');
const fs = require('fs');
const { getFitzgeraldCategory } = require('./fitzgerald_key');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  WidthType, AlignmentType, BorderStyle, PageBreak, ImageRun,
  ShadingType, HeadingLevel, Header, Footer, PageNumber,
} = require('docx');

// ── CbD Brand ────────────────────────────────────────────────
const NAVY  = '1B1F3B';
const TEAL  = '006DA0';
const AMBER = 'FFB703';
const FONT  = 'Arial';
const PAGE_W = 12240;
const PAGE_H = 15840;
const MARGIN = 1080;
const CW = PAGE_W - 2 * MARGIN;

const thinBorder = { style: BorderStyle.SINGLE, size: 1, color: 'CCCCCC' };
const borders = { top: thinBorder, bottom: thinBorder, left: thinBorder, right: thinBorder };
const noBorders = { top: { style: BorderStyle.NONE, size: 0 }, bottom: { style: BorderStyle.NONE, size: 0 }, left: { style: BorderStyle.NONE, size: 0 }, right: { style: BorderStyle.NONE, size: 0 } };

// Fitzgerald Key colors for left border
const FITZ_COLORS = {
  'People/Pronouns': 'FFD700',   // Yellow
  'Verbs/Actions':   '00B050',   // Green
  'Descriptions':    'FF8C00',   // Orange
  'Nouns':           'FFFFFF',   // White
  'Little Words':    '5B9BD5',   // Blue
  'Social/Feelings': 'FF69B4',   // Pink
};

const SYMBOL_SIZE = 110;
const WORD_LABEL_SIZE = 36;
const COLS = 4;
const colW = Math.floor(CW / COLS);

// ── Helpers ──────────────────────────────────────────────────
function p(text, opts = {}) {
  const runs = [];
  if (typeof text === 'string') {
    runs.push(new TextRun({ text, font: FONT, size: opts.size || 22, bold: opts.bold, italics: opts.italics, color: opts.color || NAVY }));
  } else if (Array.isArray(text)) {
    for (const r of text) runs.push(new TextRun({ font: FONT, size: 22, color: NAVY, ...r }));
  }
  return new Paragraph({
    children: runs,
    spacing: { after: opts.after !== undefined ? opts.after : 120, before: opts.before || 0 },
    alignment: opts.align,
    ...(opts.heading ? { heading: opts.heading } : {}),
  });
}

function h1(text) {
  return new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun({ text, font: FONT, size: 36, bold: true, color: NAVY })], spacing: { after: 60 }, border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: TEAL, space: 4 } } });
}
function spacer(n = 120) { return new Paragraph({ spacing: { after: n } }); }
function pageBreak() { return new Paragraph({ children: [new PageBreak()] }); }
function rule(color = TEAL, size = 3) { return new Paragraph({ border: { bottom: { style: BorderStyle.SINGLE, size, color, space: 1 } }, spacing: { after: 120 } }); }

function getSymbolPath(word, cacheDir) {
  return path.join(cacheDir, `arasaac_${word}.png`);
}

// ── Build symbol card grid for one lesson ────────────────────
function buildSymbolCards(lesson, cacheDir) {
  const children = [];

  if (lesson.newWords.length === 0) return children; // Skip empty lessons

  // Lesson divider
  children.push(pageBreak());
  children.push(h1(`Lesson ${lesson.number} — Symbol Cards: ${lesson.phoneme}`));
  children.push(p('Print in color. Cut along borders. Add to student binder.', { size: 16, color: '666666', italics: true, after: 60 }));
  children.push(rule(TEAL));

  // ── LABELED SYMBOL CARDS (word + image + visual coding) ──
  // Visual coding: ★ top-right = core, no mark = fringe
  // Fitzgerald Key left border = category color (matches device)
  const symRows = [];
  for (let i = 0; i < lesson.newWords.length; i += COLS) {
    const rowItems = lesson.newWords.slice(i, i + COLS);
    const cells = rowItems.map(item => {
      const fp = getSymbolPath(item.word, cacheDir);
      const fitzCat = getFitzgeraldCategory(item.word);
      const fitzColor = FITZ_COLORS[fitzCat] || 'CCCCCC';
      const c = [];

      // Visual marker: ★ for core (top-right)
      if (item.type === 'core') {
        c.push(new Paragraph({ children: [new TextRun({ text: '★', font: FONT, size: 16, color: TEAL })], alignment: AlignmentType.RIGHT, spacing: { after: 0 } }));
      } else {
        c.push(new Paragraph({ spacing: { after: 10 } }));
      }

      if (fs.existsSync(fp)) {
        c.push(new Paragraph({ children: [new ImageRun({ type: 'png', data: fs.readFileSync(fp), transformation: { width: SYMBOL_SIZE, height: SYMBOL_SIZE }, altText: { title: item.word, description: `Symbol for ${item.word}`, name: item.word } })], alignment: AlignmentType.CENTER, spacing: { after: 0 } }));
      } else {
        c.push(new Paragraph({ children: [new TextRun({ text: '✏️ Draw it!', font: FONT, size: 14, color: AMBER, bold: true })], alignment: AlignmentType.CENTER, spacing: { after: 20 } }));
        c.push(new Paragraph({ spacing: { after: 60 } }));
        c.push(new Paragraph({ spacing: { after: 60 } }));
      }
      c.push(new Paragraph({ children: [new TextRun({ text: item.word, bold: true, font: FONT, size: WORD_LABEL_SIZE, color: NAVY })], alignment: AlignmentType.CENTER, spacing: { before: 60, after: 0 } }));
      return new TableCell({ children: c, width: { size: colW, type: WidthType.DXA }, borders: {
        top: thinBorder, bottom: thinBorder, right: thinBorder,
        left: { style: BorderStyle.SINGLE, size: 12, color: fitzColor },
      }, margins: { top: 100, bottom: 80, left: 60, right: 60 } });
    });
    while (cells.length < COLS) cells.push(new TableCell({ children: [new Paragraph({ spacing: { after: 0 } })], width: { size: colW, type: WidthType.DXA }, borders: noBorders }));
    symRows.push(new TableRow({ children: cells }));
  }
  children.push(new Table({ rows: symRows, width: { size: CW, type: WidthType.DXA }, columnWidths: Array(COLS).fill(colW) }));

  // ── SYMBOL-ONLY READING PRACTICE CARDS (no labels) ──
  children.push(pageBreak());
  children.push(p(`Lesson ${lesson.number} — Reading Practice (No Labels)`, { bold: true, size: 28, color: NAVY, after: 60 }));
  children.push(p('Cut these out. Student reads the word, then selects the matching symbol.', { size: 16, color: '666666', italics: true, after: 60 }));
  children.push(rule(TEAL));

  const allSymbolWords = [
    ...lesson.newWords.map(w => ({ word: w.word, type: w.type })),
    ...(lesson.heartWords || []).map(hw => ({ word: hw, type: 'heart' })),
  ];

  const soRows = [];
  for (let i = 0; i < allSymbolWords.length; i += COLS) {
    const rowItems = allSymbolWords.slice(i, i + COLS);
    const cells = rowItems.map(item => {
      const fp = getSymbolPath(item.word, cacheDir);
      const fitzCat = getFitzgeraldCategory(item.word);
      const fitzColor = FITZ_COLORS[fitzCat] || 'CCCCCC';
      const c = [];
      if (fs.existsSync(fp)) {
        c.push(new Paragraph({ children: [new ImageRun({ type: 'png', data: fs.readFileSync(fp), transformation: { width: SYMBOL_SIZE + 20, height: SYMBOL_SIZE + 20 }, altText: { title: item.word, description: `Symbol for ${item.word}`, name: item.word } })], alignment: AlignmentType.CENTER, spacing: { after: 0 } }));
      } else {
        c.push(new Paragraph({ children: [new TextRun({ text: '✏️', font: FONT, size: 20 })], alignment: AlignmentType.CENTER, spacing: { after: 20 } }));
        c.push(new Paragraph({ spacing: { after: 60 } }));
        c.push(new Paragraph({ spacing: { after: 40 } }));
      }
      c.push(new Paragraph({ children: [new TextRun({ text: '________________', font: FONT, size: 16, color: 'CCCCCC' })], alignment: AlignmentType.CENTER, spacing: { before: 40, after: 0 } }));
      return new TableCell({ children: c, width: { size: colW, type: WidthType.DXA }, borders: {
        top: thinBorder, bottom: thinBorder, right: thinBorder,
        left: { style: BorderStyle.SINGLE, size: 12, color: fitzColor },
      }, margins: { top: 100, bottom: 80, left: 60, right: 60 } });
    });
    while (cells.length < COLS) cells.push(new TableCell({ children: [new Paragraph({ spacing: { after: 0 } })], width: { size: colW, type: WidthType.DXA }, borders: noBorders }));
    soRows.push(new TableRow({ children: cells }));
  }
  children.push(new Table({ rows: soRows, width: { size: CW, type: WidthType.DXA }, columnWidths: Array(COLS).fill(colW) }));

  // ── HEART WORD CARDS ──
  if (lesson.heartWords && lesson.heartWords.length > 0) {
    children.push(pageBreak());
    children.push(p(`Lesson ${lesson.number} — Heart Word Cards`, { bold: true, size: 28, color: NAVY, after: 60 }));
    children.push(p('Irregular words. The "heart part" must be memorized.', { size: 16, color: '666666', italics: true, after: 60 }));
    children.push(rule(TEAL));

    // Heart word cards use consistent 4-column grid (same as symbol cards)
    const hwRows = [];
    for (let i = 0; i < lesson.heartWords.length; i += COLS) {
      const rowItems = lesson.heartWords.slice(i, i + COLS);
      const cells = rowItems.map(hw => {
        const fp = getSymbolPath(hw, cacheDir);
        const fitzCat = getFitzgeraldCategory(hw);
        const fitzColor = FITZ_COLORS[fitzCat] || 'CCCCCC';
        const c = [];
        // ♥ marker top-right for heart words
        c.push(new Paragraph({ children: [new TextRun({ text: '♥', font: FONT, size: 16, color: 'CC3333' })], alignment: AlignmentType.RIGHT, spacing: { after: 0 } }));
        if (fs.existsSync(fp)) {
          c.push(new Paragraph({ children: [new ImageRun({ type: 'png', data: fs.readFileSync(fp), transformation: { width: SYMBOL_SIZE, height: SYMBOL_SIZE }, altText: { title: hw, description: `Symbol for ${hw}`, name: hw } })], alignment: AlignmentType.CENTER, spacing: { after: 0 } }));
        } else {
          c.push(new Paragraph({ children: [new TextRun({ text: '✏️ Draw it!', font: FONT, size: 14, color: AMBER, bold: true })], alignment: AlignmentType.CENTER, spacing: { after: 20 } }));
          c.push(new Paragraph({ spacing: { after: 60 } }));
          c.push(new Paragraph({ spacing: { after: 60 } }));
        }
        c.push(new Paragraph({ children: [new TextRun({ text: hw, bold: true, font: FONT, size: WORD_LABEL_SIZE, color: NAVY })], alignment: AlignmentType.CENTER, spacing: { before: 60, after: 0 } }));
        return new TableCell({ children: c, width: { size: colW, type: WidthType.DXA }, borders: {
          top: thinBorder, bottom: thinBorder, right: thinBorder,
          left: { style: BorderStyle.SINGLE, size: 12, color: fitzColor },
        }, margins: { top: 100, bottom: 80, left: 60, right: 60 } });
      });
      while (cells.length < COLS) cells.push(new TableCell({ children: [new Paragraph({ spacing: { after: 0 } })], width: { size: colW, type: WidthType.DXA }, borders: noBorders }));
      hwRows.push(new TableRow({ children: cells }));
    }
    children.push(new Table({ rows: hwRows, width: { size: CW, type: WidthType.DXA }, columnWidths: Array(COLS).fill(colW) }));
  }

  return children;
}

// ── MAIN BUILD ──────────────────────────────────────────────
async function build() {
  console.log('═══════════════════════════════════════════════════');
  console.log('  COMMUNICATE BY DESIGN — Printables Only Builder');
  console.log('  Color print → cut → use as manipulatives');
  console.log('═══════════════════════════════════════════════════\n');

  const configs = require('./ufli_lesson_configs');
  const cacheDir = path.join(__dirname, 'symbol_library');

  const children = [];

  // Cover page
  children.push(spacer(1200));
  children.push(p([
    { text: 'COMMUNICATE ', bold: true, size: 52, color: TEAL },
    { text: 'BY DESIGN', bold: true, size: 52, color: AMBER },
  ], { align: AlignmentType.CENTER, after: 200 }));
  children.push(rule(NAVY, 4));
  children.push(spacer(200));
  children.push(p('UFLI Foundations — Printable Symbol Cards', { bold: true, size: 40, align: AlignmentType.CENTER, after: 80 }));
  children.push(p('Lessons 5–34', { size: 28, color: TEAL, align: AlignmentType.CENTER, after: 200 }));
  children.push(rule(NAVY, 4));
  children.push(spacer(200));
  children.push(p('🖨️ PRINT IN COLOR — ONE-SIDED', { bold: true, size: 24, color: AMBER, align: AlignmentType.CENTER, after: 120 }));
  children.push(p('These pages contain only the materials that need to be printed, cut, and used as physical manipulatives.', { size: 20, color: '444444', align: AlignmentType.CENTER, after: 80 }));
  children.push(p('Symbol cards go in the student\'s binder. Reading practice cards go on the e-trans board.', { size: 20, color: '444444', align: AlignmentType.CENTER, after: 200 }));
  children.push(spacer(200));
  children.push(p('Where AT Meets Practice', { size: 20, color: TEAL, italics: true, align: AlignmentType.CENTER }));

  // Build printables for each lesson with words
  let lessonCount = 0;
  let cardCount = 0;
  for (const config of configs) {
    if (config.newWords.length === 0) continue; // Skip lessons 1-4
    const lessonChildren = buildSymbolCards(config, cacheDir);
    children.push(...lessonChildren);
    lessonCount++;
    cardCount += config.newWords.length;
    console.log(`  Lesson ${String(config.number).padStart(2)}: ${config.newWords.length} symbol cards + ${config.newWords.length} reading practice cards${config.heartWords.length ? ' + ' + config.heartWords.length + ' heart word cards' : ''}`);
  }

  // Attribution page
  children.push(pageBreak());
  children.push(spacer(400));
  children.push(p('Pictographic symbols © Government of Aragón. ARASAAC (arasaac.org). Licensed under CC BY-NC-SA 4.0.', { size: 16, color: '777777', italics: true, after: 80 }));
  children.push(p('Use symbols from your student\'s own AAC system first. These open-source symbols are provided as a universal reference when system-specific symbols are not available.', { size: 16, color: '777777', italics: true, after: 80 }));
  children.push(p('© Communicate by Design. All rights reserved. communicatebydesign.substack.com', { size: 16, color: '777777', italics: true }));

  // Assemble document
  const doc = new Document({
    title: 'UFLI Foundations — Printable Symbol Cards (Lessons 5–34)',
    description: 'Communicate by Design — Color printables only: symbol cards, reading practice cards, heart word cards',
    creator: 'Communicate by Design',
    styles: {
      default: { document: { run: { font: FONT, size: 22 } } },
      paragraphStyles: [
        { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { size: 36, bold: true, font: FONT, color: NAVY }, paragraph: { spacing: { before: 120, after: 120 }, outlineLevel: 0 } },
      ],
    },
    sections: [{
      properties: { page: { size: { width: PAGE_W, height: PAGE_H }, margin: { top: MARGIN, bottom: MARGIN, left: MARGIN, right: MARGIN } } },
      headers: { default: new Header({ children: [new Paragraph({ children: [
        new TextRun({ text: 'Communicate by Design', font: FONT, size: 16, color: TEAL, italics: true }),
        new TextRun({ text: '  |  UFLI Printable Symbol Cards — PRINT IN COLOR', font: FONT, size: 16, color: AMBER }),
      ], border: { bottom: { style: BorderStyle.SINGLE, size: 1, color: 'CCCCCC', space: 4 } }, spacing: { after: 0 } })] }) },
      footers: { default: new Footer({ children: [new Paragraph({ children: [
        new TextRun({ text: 'Where AT Meets Practice', font: FONT, size: 14, color: TEAL, italics: true }),
        new TextRun({ text: '  |  Page ', font: FONT, size: 14, color: '999999' }),
        new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 14, color: '999999' }),
      ], alignment: AlignmentType.CENTER, border: { top: { style: BorderStyle.SINGLE, size: 1, color: 'CCCCCC', space: 4 } }, spacing: { before: 0 } })] }) },
      children,
    }],
  });

  const outputDir = path.join(__dirname, '..', '..');
  const outputPath = path.join(outputDir, 'UFLI_Printables_Symbol_Cards_ONLY.docx');
  const buffer = await Packer.toBuffer(doc);
  fs.writeFileSync(outputPath, buffer);

  console.log(`\n═══════════════════════════════════════════════════`);
  console.log(`  ✅ ${lessonCount} lessons, ${cardCount} labeled cards + ${cardCount} practice cards`);
  console.log(`  ✅ ${path.basename(outputPath)} (${(buffer.length / 1024).toFixed(1)} KB)`);
  console.log(`  📂 ${outputPath}`);
  console.log(`═══════════════════════════════════════════════════\n`);
}

build().catch(err => { console.error('❌ Fatal:', err.message); process.exit(1); });

#!/usr/bin/env node
/**
 * UFLI Word-Only Cards Builder — Communicate by Design
 *
 * Generates a single .docx with WORD-ONLY cards (no symbols).
 * Same grid size as symbol cards (4 columns) for matching activities.
 *
 * Activity: Student matches word cards to symbol-only cards.
 *   - Symbol cards (picture only) on one side
 *   - Word cards (text only) on the other
 *   - Student picks up a word card, reads it, places next to correct symbol
 *   - OR student picks up a symbol, selects the matching word card
 *
 * Also usable for: labeling, sorting (core/fringe), Fitzgerald Key sorting,
 *   pocket chart activities, sentence building with word cards.
 *
 * Usage:
 *   node build_word_cards.js
 */

const path = require('path');
const fs = require('fs');
const { groupByFitzgerald, getFitzgeraldCategory } = require('./fitzgerald_key');
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

// Match symbol card grid exactly
const COLS = 4;
const colW = Math.floor(CW / COLS);
const WORD_SIZE = 44;  // Large readable text (22pt) for matching

// Fitzgerald Key colors for the category strip
const FITZ_COLORS = {
  'People/Pronouns': 'FFD700',   // Yellow
  'Verbs/Actions':   '00B050',   // Green
  'Descriptions':    'FF8C00',   // Orange
  'Nouns':           'FFFFFF',   // White (with border)
  'Little Words':    '5B9BD5',   // Blue
  'Social/Feelings': 'FF69B4',   // Pink
};

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


// ── Build word-only card grid for one lesson ─────────────────
function buildWordCards(lesson) {
  const children = [];
  if (lesson.newWords.length === 0) return children;

  // Lesson divider
  children.push(pageBreak());
  children.push(h1(`Lesson ${lesson.number} — Word Cards: ${lesson.phoneme}`));
  children.push(p('Print, cut, and use for matching activities. Match word cards to symbol cards.', { size: 16, color: '666666', italics: true, after: 60 }));
  children.push(rule(TEAL));

  // All words for this lesson: new words + heart words
  const allWords = [
    ...lesson.newWords.map(w => ({ word: w.word, type: w.type })),
    ...(lesson.heartWords || []).map(hw => ({ word: hw, type: 'heart' })),
  ];

  const rows = [];
  for (let i = 0; i < allWords.length; i += COLS) {
    const rowItems = allWords.slice(i, i + COLS);
    const cells = rowItems.map(item => {
      const c = [];

      // Visual type indicator — top-right: ★ for core, ♥ for heart, nothing for fringe
      let marker = '';
      let markerColor = NAVY;
      if (item.type === 'core') { marker = '★'; markerColor = TEAL; }
      else if (item.type === 'heart') { marker = '♥'; markerColor = 'CC3333'; }

      if (marker) {
        c.push(new Paragraph({
          children: [new TextRun({ text: marker, font: FONT, size: 16, color: markerColor })],
          alignment: AlignmentType.RIGHT,
          spacing: { after: 0 },
        }));
      } else {
        c.push(new Paragraph({ spacing: { after: 10 } }));
      }

      // Spacer before word
      c.push(new Paragraph({ spacing: { after: 60 } }));

      // Large word text — centered, bold
      c.push(new Paragraph({
        children: [new TextRun({ text: item.word, bold: true, font: FONT, size: WORD_SIZE, color: NAVY })],
        alignment: AlignmentType.CENTER,
        spacing: { before: 60, after: 60 },
      }));

      // Bottom spacer for consistent card height
      c.push(new Paragraph({ spacing: { after: 80 } }));

      // Fitzgerald Key left border for category color coding
      const fitzCat = getFitzgeraldCategory(item.word);
      const fitzColor = FITZ_COLORS[fitzCat] || 'CCCCCC';

      return new TableCell({
        children: c,
        width: { size: colW, type: WidthType.DXA },
        borders: {
          top: thinBorder,
          bottom: thinBorder,
          right: thinBorder,
          left: { style: BorderStyle.SINGLE, size: 12, color: fitzColor },
        },
        margins: { top: 100, bottom: 80, left: 60, right: 60 },
        verticalAlign: 'center',
      });
    });

    // Pad row to COLS
    while (cells.length < COLS) {
      cells.push(new TableCell({
        children: [new Paragraph({ spacing: { after: 0 } })],
        width: { size: colW, type: WidthType.DXA },
        borders: noBorders,
      }));
    }
    rows.push(new TableRow({ children: cells }));
  }

  children.push(new Table({
    rows,
    width: { size: CW, type: WidthType.DXA },
    columnWidths: Array(COLS).fill(colW),
  }));

  return children;
}


// ── MAIN BUILD ──────────────────────────────────────────────
async function build() {
  console.log('═══════════════════════════════════════════════════');
  console.log('  COMMUNICATE BY DESIGN — Word-Only Cards Builder');
  console.log('  Match to symbol cards for literacy activities');
  console.log('═══════════════════════════════════════════════════\n');

  const configs = require('./ufli_lesson_configs');

  const children = [];

  // Cover page
  children.push(spacer(1200));
  children.push(p([
    { text: 'COMMUNICATE ', bold: true, size: 52, color: TEAL },
    { text: 'BY DESIGN', bold: true, size: 52, color: AMBER },
  ], { align: AlignmentType.CENTER, after: 200 }));
  children.push(rule(NAVY, 4));
  children.push(spacer(200));
  children.push(p('UFLI Foundations — Word Cards for Matching', { bold: true, size: 40, align: AlignmentType.CENTER, after: 80 }));
  children.push(p('Lessons 5–34', { size: 28, color: TEAL, align: AlignmentType.CENTER, after: 200 }));
  children.push(rule(NAVY, 4));
  children.push(spacer(200));
  children.push(p('🖨️ PRINT — CAN BE B&W OR COLOR', { bold: true, size: 24, color: AMBER, align: AlignmentType.CENTER, after: 120 }));
  children.push(p('These word-only cards match the symbol card grid. Use for word-to-symbol matching, labeling, sorting, and reading activities.', { size: 20, color: '444444', align: AlignmentType.CENTER, after: 80 }));
  children.push(spacer(120));

  // Activity instructions
  children.push(p('MATCHING ACTIVITIES', { bold: true, size: 28, color: NAVY, align: AlignmentType.CENTER, after: 80 }));
  children.push(rule(TEAL, 2));
  children.push(p([
    { text: 'Activity 1 — Word to Symbol: ', bold: true, size: 20, color: NAVY },
    { text: 'Lay symbol-only cards on the table. Student selects, points to, or uses gaze to indicate the matching word card for each symbol.', size: 20, color: '444444' },
  ], { after: 80 }));
  children.push(p([
    { text: 'Activity 2 — Symbol to Word: ', bold: true, size: 20, color: NAVY },
    { text: 'Lay word cards on the table. Student selects, points to, or uses gaze to indicate the matching symbol card for each word.', size: 20, color: '444444' },
  ], { after: 80 }));
  children.push(p([
    { text: 'Activity 3 — Label It: ', bold: true, size: 20, color: NAVY },
    { text: 'Place symbol cards in a row. Student places word card below each symbol to label it. Communication partner provides the auditory loop.', size: 20, color: '444444' },
  ], { after: 80 }));
  children.push(p([
    { text: 'Activity 4 — Sort It: ', bold: true, size: 20, color: NAVY },
    { text: 'Sort word cards by Fitzgerald Key color (matches the colored strip at top of each card). Builds categorization skills and mirrors device organization.', size: 20, color: '444444' },
  ], { after: 80 }));
  children.push(p([
    { text: 'Activity 5 — Pocket Chart: ', bold: true, size: 20, color: NAVY },
    { text: 'Use word cards and symbol cards together in a pocket chart for sentence building. Add core words for connected phrases.', size: 20, color: '444444' },
  ], { after: 120 }));
  children.push(spacer(80));
  children.push(p('Fitzgerald Key Color Legend:', { bold: true, size: 20, color: NAVY, after: 40 }));
  children.push(p('Yellow = People/Pronouns  •  Green = Verbs/Actions  •  Orange = Descriptions  •  White = Nouns  •  Blue = Little Words  •  Pink = Social/Feelings', { size: 18, color: '666666', italics: true, after: 120 }));

  // Build word cards for each lesson
  let lessonCount = 0;
  let cardCount = 0;
  for (const config of configs) {
    if (config.newWords.length === 0) continue;
    const lessonChildren = buildWordCards(config);
    children.push(...lessonChildren);
    lessonCount++;
    cardCount += config.newWords.length + (config.heartWords ? config.heartWords.length : 0);
    console.log(`  Lesson ${String(config.number).padStart(2)}: ${config.newWords.length} word cards${config.heartWords && config.heartWords.length ? ' + ' + config.heartWords.length + ' heart word cards' : ''}`);
  }

  // Attribution page
  children.push(pageBreak());
  children.push(spacer(400));
  children.push(p('Fitzgerald Key categorization based on: Fitzgerald (1949), adapted by Goossens\', Crain, & Elder (1992). Color-coding matches standard AAC device conventions.', { size: 16, color: '777777', italics: true, after: 80 }));
  children.push(p('Core/fringe classification based on: Banajee et al. (2003), Van Tatenhove (2009).', { size: 16, color: '777777', italics: true, after: 80 }));
  children.push(p('© Communicate by Design. All rights reserved. communicatebydesign.substack.com', { size: 16, color: '777777', italics: true }));

  // Assemble document
  const doc = new Document({
    title: 'UFLI Foundations — Word Cards for Matching (Lessons 5–34)',
    description: 'Communicate by Design — Word-only cards for matching, labeling, and sorting activities',
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
        new TextRun({ text: '  |  UFLI Word Cards — MATCHING ACTIVITY', font: FONT, size: 16, color: AMBER }),
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
  const outputPath = path.join(outputDir, 'UFLI_Word_Cards_Matching.docx');
  const buffer = await Packer.toBuffer(doc);
  fs.writeFileSync(outputPath, buffer);

  console.log(`\n═══════════════════════════════════════════════════`);
  console.log(`  ✅ ${lessonCount} lessons, ${cardCount} total word cards`);
  console.log(`  ✅ ${path.basename(outputPath)} (${(buffer.length / 1024).toFixed(1)} KB)`);
  console.log(`  📂 ${outputPath}`);
  console.log(`═══════════════════════════════════════════════════\n`);
}

build().catch(err => { console.error('❌ Fatal:', err.message); process.exit(1); });

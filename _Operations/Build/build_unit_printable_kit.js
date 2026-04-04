#!/usr/bin/env node
/**
 * CbD Standard Unit Printable Kit Builder
 *
 * Generates the COMPLETE printable package for any CbD unit:
 *   1. Communication Partner Word List (reference page with Fitzgerald Key categories)
 *   2. Symbol Cards (ARASAAC + Fitzgerald Key color borders, 2.5"×3.5" trading card size)
 *   3. Word Cards (text-only, Fitzgerald Key color strips)
 *   4. Unit Communication Board (compact grid by Fitzgerald Key sections)
 *
 * All four components generate from the SAME vocabulary data —
 * the lesson config's newWords, reviewWords, and heartWords arrays
 * plus the Fitzgerald Key classification.
 *
 * DESIGN ASSUMPTIONS (from CbD Master Reference):
 *   - Student is a complex communicator, mostly nonspeaking
 *   - Student has NOTHING unless we provide it or list it
 *   - Core/fringe from AAC research (Banajee et al., 2003; Van Tatenhove, 2009)
 *   - Fitzgerald Key color coding matches device conventions
 *   - One-sided printing for all card pages
 *   - Symbol normalization: 400×400px canvas, 340px content area
 *   - Access Level 2 default for communication boards (eye gaze / direct selection)
 *
 * USAGE:
 *   // Build kit for a single UFLI lesson
 *   node build_unit_printable_kit.js --lesson 7
 *
 *   // Build kit for a range of lessons
 *   node build_unit_printable_kit.js --range 5 10
 *
 *   // Build kit for all lessons with words
 *   node build_unit_printable_kit.js --all
 *
 *   // Programmatic use from any unit builder
 *   const { buildUnitKit } = require('./build_unit_printable_kit');
 *   await buildUnitKit({
 *     unitTitle: 'Lesson 7 — /n/ n',
 *     unitNumber: 7,
 *     coreWords: [{ word: 'an', type: 'core' }, ...],
 *     fringeWords: [{ word: 'nap', type: 'fringe' }, ...],
 *     heartWords: ['the'],
 *     reviewWords: [{ word: 'at', from: 'Lesson 5', type: 'core' }, ...],
 *     symbolDir: './symbol_library',
 *     outputDir: './Output',
 *     accessLevel: 'level2',
 *   });
 */

const path = require('path');
const fs = require('fs');
const { getFitzgeraldCategory, groupByFitzgerald } = require('./fitzgerald_key');
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
const PAGE_W = 12240;  // 8.5" in twips
const PAGE_H = 15840;  // 11" in twips
const MARGIN = 1080;   // 0.75" in twips
const CW = PAGE_W - 2 * MARGIN;

const thinBorder = { style: BorderStyle.SINGLE, size: 1, color: 'CCCCCC' };
const borders = { top: thinBorder, bottom: thinBorder, left: thinBorder, right: thinBorder };
const noBorders = { top: { style: BorderStyle.NONE, size: 0 }, bottom: { style: BorderStyle.NONE, size: 0 }, left: { style: BorderStyle.NONE, size: 0 }, right: { style: BorderStyle.NONE, size: 0 } };

// ── Fitzgerald Key color palette (matches device conventions) ─
const FITZ = {
  People:       { color: 'D4A800', bg: 'FFF8DC', label: 'People / Pronouns' },
  Actions:      { color: '00A86B', bg: 'E8F5E9', label: 'Verbs / Actions' },
  Descriptions: { color: 'FF8C00', bg: 'FFF3E0', label: 'Descriptions' },
  Nouns:        { color: '8B6914', bg: 'FFF5D6', label: 'Nouns' },
  Prepositions: { color: '4A90D9', bg: 'E3F2FD', label: 'Little Words' },
  Social:       { color: 'E88CA5', bg: 'FCE4EC', label: 'Social / Feelings' },
};

// Display order for Fitzgerald Key categories
const FITZ_ORDER = ['People', 'Actions', 'Descriptions', 'Nouns', 'Prepositions', 'Social'];

// ── Access Level Sizing (from cbd_symbol_fetcher.js) ─────────
const ACCESS_LEVELS = {
  level1: { imageWidth: 126, imageHeight: 126, labelSize: 24, maxPerRow: 3, borderWidth: 3, desc: 'Partner-assisted / beginning eye gaze' },
  level2: { imageWidth: 90,  imageHeight: 90,  labelSize: 22, maxPerRow: 4, borderWidth: 2, desc: 'Eye gaze / direct selection' },
  level3: { imageWidth: 72,  imageHeight: 72,  labelSize: 20, maxPerRow: 5, borderWidth: 1, desc: 'Independent device / reference' },
};

// ── Trading Card sizing (2.5" × 3.5" — binder ecosystem) ────
// Evidence: exceeds AAC field standard 2"×2" minimum.
// Fits standard 9-pocket trading card binder pages (900 card capacity).
// 3 cards per row on letter paper with 0.75" margins.
const CARD_W_INCHES = 2.5;
const CARD_H_INCHES = 3.5;
const CARD_W = Math.floor(CARD_W_INCHES * 1440);  // twips (1 inch = 1440 twips)
const CARD_H = Math.floor(CARD_H_INCHES * 1440);
const CARD_SYMBOL_SIZE = 140;  // Larger symbol for trading card size
const CARD_WORD_SIZE = 36;     // Word label on symbol cards (18pt)
const CARD_COLS = 3;           // 3 trading cards per row on letter paper
const CARD_COL_W = Math.floor(CW / CARD_COLS);
const CARD_CAT_BAR_H = 300;   // Category bar height (twips) — Zone 1 for binder sorting

// ── Legacy sizing for word cards (text-only, still 4 per row) ──
const WORD_CARD_COLS = 4;
const WORD_CARD_COL_W = Math.floor(CW / WORD_CARD_COLS);

/**
 * Get display label for a unit/lesson.
 * Supports both UFLI format (Lesson 7 — /f/ f) and nonfiction format (Radium Girls).
 */
function getUnitLabel(config) {
  if (config.unitTitle) return config.unitTitle;
  return `Lesson ${config.number}` + (config.phoneme ? ` — ${config.phoneme} ${config.grapheme}` : config.grapheme ? ` — ${config.grapheme}` : '');
}

// ══════════════════════════════════════════════════════════════
// HELPERS
// ══════════════════════════════════════════════════════════════

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
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    children: [new TextRun({ text, font: FONT, size: 36, bold: true, color: NAVY })],
    spacing: { after: 60 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: TEAL, space: 4 } },
  });
}

function h2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    children: [new TextRun({ text, font: FONT, size: 28, bold: true, color: NAVY })],
    spacing: { before: 200, after: 100 },
  });
}

function spacer(n = 120) { return new Paragraph({ spacing: { after: n } }); }
function pageBreak() { return new Paragraph({ children: [new PageBreak()] }); }
function rule(color = TEAL, size = 3) {
  return new Paragraph({
    border: { bottom: { style: BorderStyle.SINGLE, size, color, space: 1 } },
    spacing: { after: 120 },
  });
}

function getSymbolPath(word, cacheDir) {
  return path.join(cacheDir, `arasaac_${word}.png`);
}

/**
 * Get all unique words from a lesson config, categorized
 */
function getUnitVocabulary(config) {
  const core = [];
  const fringe = [];
  const heart = [];
  const seen = new Set();

  for (const w of config.newWords || []) {
    if (seen.has(w.word)) continue;
    seen.add(w.word);
    if (w.type === 'core') core.push(w);
    else fringe.push(w);
  }
  for (const hw of config.heartWords || []) {
    if (seen.has(hw)) continue;
    seen.add(hw);
    heart.push({ word: hw, type: 'heart' });
  }
  return { core, fringe, heart, all: [...core, ...fringe, ...heart] };
}


// ══════════════════════════════════════════════════════════════
// COMPONENT 1: Communication Partner Word List
// ══════════════════════════════════════════════════════════════

function buildPartnerWordList(config, vocab) {
  const children = [];
  const unitLabel = getUnitLabel(config);

  children.push(h1(`${unitLabel}: Communication Partner Word List`));
  children.push(p('Vocabulary targets for this unit. Use this list to prepare symbol cards, e-trans boards, and communication boards before starting the unit.', { size: 18, color: '666666', italics: true, after: 60 }));
  children.push(rule(TEAL));

  // Group all words by Fitzgerald Key category
  const allTagged = vocab.all.map(w => ({ word: w.word, type: w.type, from: '' }));
  for (const rw of config.reviewWords || []) {
    if (!allTagged.find(a => a.word === rw.word)) {
      allTagged.push({ word: rw.word, type: rw.type, from: rw.from });
    }
  }

  const grouped = {};
  for (const w of allTagged) {
    const fitz = getFitzgeraldCategory(w.word);
    if (!grouped[fitz.label]) grouped[fitz.label] = [];
    grouped[fitz.label].push(w);
  }

  // Build table: one section per Fitzgerald category
  for (const cat of FITZ_ORDER) {
    if (!grouped[cat] || grouped[cat].length === 0) continue;

    const fitzInfo = FITZ[cat];
    const words = grouped[cat].sort((a, b) => {
      // Core first, then fringe, then alphabetical
      if (a.type !== b.type) return a.type === 'core' ? -1 : 1;
      return a.word.localeCompare(b.word);
    });

    // Category header with Fitzgerald color bar
    children.push(new Paragraph({
      children: [new TextRun({ text: `  ${fitzInfo.label}`, font: FONT, size: 22, bold: true, color: NAVY })],
      spacing: { before: 160, after: 40 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: fitzInfo.color, space: 2 } },
    }));

    // 3-column table: Word | Type | How the Student Uses It
    const rows = [];
    const headerCells = [
      new TableCell({
        children: [p('Word', { bold: true, size: 18, after: 0 })],
        width: { size: Math.floor(CW * 0.30), type: WidthType.DXA },
        shading: { type: ShadingType.CLEAR, fill: fitzInfo.bg },
        borders: { ...borders, left: { style: BorderStyle.SINGLE, size: 4, color: fitzInfo.color } },
        margins: { top: 40, bottom: 40, left: 80, right: 80 },
      }),
      new TableCell({
        children: [p('Type', { bold: true, size: 18, after: 0 })],
        width: { size: Math.floor(CW * 0.20), type: WidthType.DXA },
        shading: { type: ShadingType.CLEAR, fill: fitzInfo.bg },
        borders,
        margins: { top: 40, bottom: 40, left: 80, right: 80 },
      }),
      new TableCell({
        children: [p('V3 Activity Use', { bold: true, size: 18, after: 0 })],
        width: { size: Math.floor(CW * 0.50), type: WidthType.DXA },
        shading: { type: ShadingType.CLEAR, fill: fitzInfo.bg },
        borders,
        margins: { top: 40, bottom: 40, left: 80, right: 80 },
      }),
    ];
    rows.push(new TableRow({ children: headerCells, cantSplit: true }));

    for (const w of words) {
      let typeLabel, typeColor;
      if (w.type === 'core') { typeLabel = '★ core'; typeColor = TEAL; }
      else if (w.type === 'heart') { typeLabel = '♥ heart'; typeColor = 'CC3333'; }
      else { typeLabel = 'fringe'; typeColor = AMBER; }

      // Activity use note based on Fitzgerald category + type
      let activityNote;
      const fitz = getFitzgeraldCategory(w.word);
      if (fitz.label === 'Actions') activityNote = 'Annotation, sentence frames, discussion';
      else if (fitz.label === 'Descriptions') activityNote = 'Annotation responses, evidence citing';
      else if (fitz.label === 'Prepositions') activityNote = 'Sentence frames, connecting ideas';
      else if (fitz.label === 'Social') activityNote = 'Discussion, comprehension responses';
      else if (fitz.label === 'People') activityNote = 'Discussion, identifying perspectives';
      else activityNote = 'Vocabulary preview, passage comprehension';

      const dataCells = [
        new TableCell({
          children: [p(w.word, { bold: true, size: 20, after: 0 })],
          width: { size: Math.floor(CW * 0.30), type: WidthType.DXA },
          borders: { ...borders, left: { style: BorderStyle.SINGLE, size: 4, color: fitzInfo.color } },
          margins: { top: 30, bottom: 30, left: 80, right: 80 },
        }),
        new TableCell({
          children: [p(typeLabel, { size: 18, color: typeColor, italics: true, after: 0 })],
          width: { size: Math.floor(CW * 0.20), type: WidthType.DXA },
          borders,
          margins: { top: 30, bottom: 30, left: 80, right: 80 },
        }),
        new TableCell({
          children: [p(activityNote, { size: 16, color: '666666', italics: true, after: 0 })],
          width: { size: Math.floor(CW * 0.50), type: WidthType.DXA },
          borders,
          margins: { top: 30, bottom: 30, left: 80, right: 80 },
        }),
      ];
      rows.push(new TableRow({ children: dataCells, cantSplit: true }));
    }

    children.push(new Table({
      rows,
      width: { size: CW, type: WidthType.DXA },
    }));
  }

  // Partner guidance — full AAC continuum
  children.push(spacer(200));
  children.push(rule(AMBER, 2));
  children.push(p([
    { text: 'How to use these words during the unit:', bold: true, size: 20, color: TEAL },
  ], { after: 80 }));
  children.push(p([
    { text: 'Model ', bold: true, size: 20, color: '444444' },
    { text: 'these words throughout instruction. Point to the symbol on the communication board, e-trans board, symbol cards, or device as you say the word. Use it in context during reading, discussion, and activities.', size: 20, color: '444444' },
  ], { after: 60 }));
  children.push(p([
    { text: 'Core words (★) ', bold: true, size: 20, color: TEAL },
    { text: 'are high-frequency words used across many contexts. Model these and support adding them to the student\'s device appropriately. The student will encounter these across units.', size: 20, color: '444444' },
  ], { after: 60 }));
  children.push(p([
    { text: 'Fringe words ', bold: true, size: 20, color: AMBER },
    { text: 'are topic-specific vocabulary for this unit. Introduce during vocabulary preview before reading the passage. Consider adding fringe words to the student\'s device and developing a topic board to support access during the unit.', size: 20, color: '444444' },
  ], { after: 80 }));
  children.push(p([
    { text: 'This kit provides ready-made symbols for immediate use with e-trans boards, symbol exchange, partner-assisted scanning, or any access method. If the student has a device, use these symbols alongside device vocabulary to support participation across all V3 activities.', size: 18, color: '666666', italics: true },
  ]));

  return children;
}


// ══════════════════════════════════════════════════════════════
// COMPONENT 2: Symbol Cards (Trading Card — 2.5" × 3.5")
//
// 3-ZONE DESIGN for 9-pocket binder ecosystem:
//   Zone 1 (top): Category bar — Fitzgerald Key color + label for binder sorting
//   Zone 2 (center): ARASAAC symbol with Fitzgerald Key colored border
//   Zone 3 (bottom): Bold word label + part-of-speech sublabel
//
// Cards accumulate across ALL CbD units into a student's binder,
// organized by Modified Fitzgerald Key tab colors.
// ══════════════════════════════════════════════════════════════

function buildSymbolCards(config, vocab, symbolDir) {
  const children = [];
  if (vocab.all.length === 0) return children;

  const unitLabel = getUnitLabel(config);

  children.push(h1(`${unitLabel}: Symbol Cards`));
  children.push(p('Print in color. Cut along borders. ONE-SIDED PRINTING ONLY.', { size: 18, color: AMBER, bold: true, after: 40 }));
  children.push(p('Cards are 2.5" × 3.5" (trading card size). Store in a 9-pocket trading card binder organized by Fitzgerald Key category tabs.', { size: 16, color: '666666', italics: true, after: 60 }));
  children.push(rule(TEAL));

  // Build card grid — core first, then fringe, then heart
  const allCards = [
    ...vocab.core.map(w => ({ ...w })),
    ...vocab.fringe.map(w => ({ ...w })),
    ...vocab.heart.map(w => ({ ...w })),
  ];

  const rows = [];
  for (let i = 0; i < allCards.length; i += CARD_COLS) {
    const rowItems = allCards.slice(i, i + CARD_COLS);
    const cells = rowItems.map(item => {
      const fitz = getFitzgeraldCategory(item.word);
      const fitzInfo = FITZ[fitz.label] || FITZ.Nouns;
      const fp = getSymbolPath(item.word, symbolDir);
      const c = [];

      // ── ZONE 1: Category bar (Fitzgerald Key color + label) ──
      // Solid color background with white text for binder sorting
      c.push(new Paragraph({
        children: [
          new TextRun({ text: fitzInfo.label.toUpperCase(), font: FONT, size: 16, bold: true, color: 'FFFFFF' }),
          ...(item.type === 'core' ? [new TextRun({ text: '  ★', font: FONT, size: 16, color: 'FFFFFF' })] : []),
          ...(item.type === 'heart' ? [new TextRun({ text: '  ♥', font: FONT, size: 16, color: 'FFFFFF' })] : []),
        ],
        alignment: AlignmentType.CENTER,
        spacing: { before: 0, after: 0 },
        shading: { type: ShadingType.CLEAR, fill: fitzInfo.color },
      }));

      // ── ZONE 2: Symbol area (largest zone — center of card) ──
      if (fs.existsSync(fp)) {
        c.push(new Paragraph({
          children: [new ImageRun({
            type: 'png',
            data: fs.readFileSync(fp),
            transformation: { width: CARD_SYMBOL_SIZE, height: CARD_SYMBOL_SIZE },
            altText: { title: item.word, description: `Symbol for ${item.word}`, name: item.word },
          })],
          alignment: AlignmentType.CENTER,
          spacing: { before: 80, after: 40 },
        }));
      } else {
        // Draw It! activity for words without ARASAAC symbols
        c.push(new Paragraph({
          children: [new TextRun({ text: '✏️ Draw It!', font: FONT, size: 20, color: AMBER, bold: true })],
          alignment: AlignmentType.CENTER,
          spacing: { before: 60, after: 20 },
        }));
        // Empty space for drawing
        c.push(spacer(200));
      }

      // ── ZONE 3: Word label + part-of-speech sublabel ──
      c.push(new Paragraph({
        children: [new TextRun({ text: item.word, bold: true, font: FONT, size: CARD_WORD_SIZE, color: NAVY })],
        alignment: AlignmentType.CENTER,
        spacing: { before: 20, after: 0 },
      }));
      // Part-of-speech sublabel (from Fitzgerald category)
      c.push(new Paragraph({
        children: [new TextRun({ text: fitzInfo.label.toLowerCase(), font: FONT, size: 14, color: fitzInfo.color, italics: true })],
        alignment: AlignmentType.CENTER,
        spacing: { before: 0, after: 0 },
      }));

      // Card cell: Fitzgerald Key colored border + category bar shading
      // Using nested table to get solid color category bar at top
      return new TableCell({
        children: c,
        width: { size: CARD_COL_W, type: WidthType.DXA },
        shading: { type: ShadingType.CLEAR, fill: 'FFFFFF' },
        borders: {
          top: { style: BorderStyle.SINGLE, size: 8, color: fitzInfo.color },
          bottom: { style: BorderStyle.SINGLE, size: 8, color: fitzInfo.color },
          left: { style: BorderStyle.SINGLE, size: 8, color: fitzInfo.color },
          right: { style: BorderStyle.SINGLE, size: 8, color: fitzInfo.color },
        },
        margins: { top: 40, bottom: 60, left: 60, right: 60 },
      });
    });

    // Pad row with empty cells
    while (cells.length < CARD_COLS) {
      cells.push(new TableCell({
        children: [spacer(0)],
        width: { size: CARD_COL_W, type: WidthType.DXA },
        borders: noBorders,
      }));
    }
    rows.push(new TableRow({ children: cells, cantSplit: true, height: { value: CARD_H, rule: 'atLeast' } }));
  }

  children.push(new Table({
    rows,
    width: { size: CW, type: WidthType.DXA },
    columnWidths: Array(CARD_COLS).fill(CARD_COL_W),
  }));

  // Legend
  children.push(spacer(80));
  const legendItems = FITZ_ORDER.map(cat => {
    const f = FITZ[cat];
    return f.label;
  });
  children.push(p(`Fitzgerald Key: ${legendItems.join('  •  ')}  |  ★ = core  ♥ = heart  |  Card size: 2.5" × 3.5"`, { size: 14, color: '888888', italics: true, align: AlignmentType.CENTER }));
  children.push(p('Store cards in a 9-pocket trading card binder organized by category tabs.', { size: 14, color: '888888', italics: true, align: AlignmentType.CENTER }));

  return children;
}


// ══════════════════════════════════════════════════════════════
// COMPONENT 3: Word Cards (text-only, Fitzgerald Key color strips)
// ══════════════════════════════════════════════════════════════

function buildWordCards(config, vocab) {
  const children = [];
  if (vocab.all.length === 0) return children;

  const unitLabel = getUnitLabel(config);

  children.push(h1(`${unitLabel}: Word Cards`));
  children.push(p('Print, cut, and use for matching, sorting, and vocabulary activities.', { size: 16, color: '666666', italics: true, after: 60 }));
  children.push(rule(TEAL));

  const allCards = [...vocab.core, ...vocab.fringe, ...vocab.heart];
  const WORD_DISPLAY_SIZE = 44;

  const rows = [];
  for (let i = 0; i < allCards.length; i += WORD_CARD_COLS) {
    const rowItems = allCards.slice(i, i + WORD_CARD_COLS);
    const cells = rowItems.map(item => {
      const fitz = getFitzgeraldCategory(item.word);
      const fitzInfo = FITZ[fitz.label] || FITZ.Nouns;
      const c = [];

      // Core/heart indicator in top-left corner
      let tagText = '';
      let tagColor = NAVY;
      if (item.type === 'core') { tagText = '★'; tagColor = TEAL; }
      else if (item.type === 'heart') { tagText = '♥'; tagColor = 'CC3333'; }

      c.push(new Paragraph({
        children: [new TextRun({ text: tagText || ' ', font: FONT, size: tagText ? 20 : 4, color: tagColor })],
        spacing: { after: 0 },
      }));

      // Large word text (centered vertically)
      c.push(spacer(60));
      c.push(new Paragraph({
        children: [new TextRun({ text: item.word, bold: true, font: FONT, size: WORD_DISPLAY_SIZE, color: NAVY })],
        alignment: AlignmentType.CENTER,
        spacing: { before: 40, after: 40 },
      }));
      c.push(spacer(40));

      return new TableCell({
        children: c,
        width: { size: WORD_CARD_COL_W, type: WidthType.DXA },
        shading: { type: ShadingType.CLEAR, fill: fitzInfo.bg },
        borders: {
          top: { style: BorderStyle.SINGLE, size: 6, color: fitzInfo.color },
          bottom: { style: BorderStyle.SINGLE, size: 6, color: fitzInfo.color },
          left: { style: BorderStyle.SINGLE, size: 6, color: fitzInfo.color },
          right: { style: BorderStyle.SINGLE, size: 6, color: fitzInfo.color },
        },
        margins: { top: 80, bottom: 80, left: 60, right: 60 },
      });
    });

    while (cells.length < WORD_CARD_COLS) {
      cells.push(new TableCell({
        children: [spacer(0)],
        width: { size: WORD_CARD_COL_W, type: WidthType.DXA },
        borders: noBorders,
      }));
    }
    rows.push(new TableRow({ children: cells, cantSplit: true }));
  }

  children.push(new Table({
    rows,
    width: { size: CW, type: WidthType.DXA },
    columnWidths: Array(WORD_CARD_COLS).fill(WORD_CARD_COL_W),
  }));

  // Legend
  children.push(spacer(80));
  const legendItems = FITZ_ORDER.map(cat => FITZ[cat].label);
  children.push(p(`Fitzgerald Key colors: ${legendItems.join('  •  ')}  |  ★ = core  ♥ = heart`, { size: 14, color: '888888', italics: true, align: AlignmentType.CENTER }));

  return children;
}


// ══════════════════════════════════════════════════════════════
// COMPONENT 4: Unit Communication Board (Single Printable Grid)
// ══════════════════════════════════════════════════════════════
//
// One continuous grid — no category header breaks. Fitzgerald Key
// color on each cell via background tint + thick left border.
// Words sorted by category so colors naturally group together.
// Compact symbols + word labels. Prints as a usable e-trans board.

function buildCommunicationBoard(config, vocab, symbolDir, accessLevel = 'level2') {
  const children = [];
  if (vocab.all.length === 0) return children;

  const level = ACCESS_LEVELS[accessLevel] || ACCESS_LEVELS.level2;
  const unitLabel = getUnitLabel(config);
  const BOARD_COLS = level.maxPerRow;

  children.push(h1(`${unitLabel}: Communication Board`));
  children.push(p(`Print in color. Use for aided language input, e-trans, and student responses during all activities.`, { size: 16, color: '666666', italics: true, after: 40 }));
  children.push(rule(TEAL));

  // Collect all words
  const allWords = new Map();
  for (const w of vocab.all) allWords.set(w.word, { ...w });
  for (const rw of config.reviewWords || []) {
    if (!allWords.has(rw.word)) allWords.set(rw.word, { word: rw.word, type: rw.type });
  }

  // Sort all words by Fitzgerald category order, then core first, then alphabetical
  const sortedWords = [...allWords.values()].sort((a, b) => {
    const fitzA = getFitzgeraldCategory(a.word);
    const fitzB = getFitzgeraldCategory(b.word);
    const orderA = FITZ_ORDER.indexOf(fitzA.label);
    const orderB = FITZ_ORDER.indexOf(fitzB.label);
    if (orderA !== orderB) return orderA - orderB;
    if (a.type !== b.type) return a.type === 'core' ? -1 : 1;
    return a.word.localeCompare(b.word);
  });

  const boardColW = Math.floor(CW / BOARD_COLS);
  const imgSize = Math.min(level.imageWidth, 72);

  // One continuous table — all words in grid
  const gridRows = [];
  for (let i = 0; i < sortedWords.length; i += BOARD_COLS) {
    const rowItems = sortedWords.slice(i, i + BOARD_COLS);
    const cells = rowItems.map(w => {
      const fitz = getFitzgeraldCategory(w.word);
      const fitzInfo = FITZ[fitz.label] || FITZ.Nouns;
      const fp = getSymbolPath(w.word, symbolDir);
      const cellChildren = [];

      // Symbol
      if (fs.existsSync(fp)) {
        cellChildren.push(new Paragraph({
          children: [new ImageRun({
            type: 'png',
            data: fs.readFileSync(fp),
            transformation: { width: imgSize, height: imgSize },
            altText: { title: w.word, description: `Symbol for ${w.word}`, name: w.word },
          })],
          alignment: AlignmentType.CENTER,
          spacing: { before: 10, after: 0 },
        }));
      } else {
        cellChildren.push(new Paragraph({
          children: [new TextRun({ text: '✏️', font: FONT, size: 14 })],
          alignment: AlignmentType.CENTER,
          spacing: { before: 10, after: 10 },
        }));
      }

      // Word label with core star
      cellChildren.push(new Paragraph({
        children: [
          new TextRun({ text: w.word, bold: true, font: FONT, size: level.labelSize, color: NAVY }),
        ],
        alignment: AlignmentType.CENTER,
        spacing: { before: 4, after: 0 },
      }));

      return new TableCell({
        children: cellChildren,
        width: { size: boardColW, type: WidthType.DXA },
        shading: { type: ShadingType.CLEAR, fill: fitzInfo.bg },
        borders: {
          top: { style: BorderStyle.SINGLE, size: 6, color: fitzInfo.color },
          bottom: { style: BorderStyle.SINGLE, size: 6, color: fitzInfo.color },
          left: { style: BorderStyle.SINGLE, size: 6, color: fitzInfo.color },
          right: { style: BorderStyle.SINGLE, size: 6, color: fitzInfo.color },
        },
        margins: { top: 20, bottom: 20, left: 10, right: 10 },
      });
    });

    // Pad row
    while (cells.length < BOARD_COLS) {
      cells.push(new TableCell({
        children: [spacer(0)],
        width: { size: boardColW, type: WidthType.DXA },
        borders: noBorders,
      }));
    }
    gridRows.push(new TableRow({ children: cells, cantSplit: true }));
  }

  children.push(new Table({
    rows: gridRows,
    width: { size: CW, type: WidthType.DXA },
    columnWidths: Array(BOARD_COLS).fill(boardColW),
  }));

  // Fitzgerald Key legend at bottom
  children.push(spacer(80));
  const legendItems = FITZ_ORDER.map(cat => FITZ[cat].label);
  children.push(p(`Fitzgerald Key: ${legendItems.join('  •  ')}  |  ★ = core`, { size: 14, color: '888888', italics: true, align: AlignmentType.CENTER }));

  return children;
}


// ══════════════════════════════════════════════════════════════
// MAIN: Build Unit Kit
// ══════════════════════════════════════════════════════════════

/**
 * Build the complete printable kit for a unit/lesson.
 * @param {Object} config - Lesson config from ufli_lesson_configs.js (or any unit config with the same shape)
 * @param {Object} options
 * @param {string} options.symbolDir - Path to symbol library directory
 * @param {string} options.outputDir - Output directory for generated .docx
 * @param {string} [options.accessLevel='level2'] - Communication board access level
 * @param {string} [options.productLine='UFLI'] - Product line name for headers
 */
async function buildUnitKit(config, options = {}) {
  const {
    symbolDir = path.join(__dirname, '..', 'Symbols', 'symbol_library'),
    outputDir = path.join(__dirname, 'Output'),
    accessLevel = 'level2',
    productLine = 'UFLI Foundations',
  } = options;

  const vocab = getUnitVocabulary(config);
  if (vocab.all.length === 0) {
    console.log(`  Lesson ${config.number}: No words — skipping kit`);
    return null;
  }

  const unitLabel = getUnitLabel(config);
  console.log(`\n  Building kit for ${unitLabel}...`);
  console.log(`    ${vocab.core.length} core + ${vocab.fringe.length} fringe + ${vocab.heart.length} heart = ${vocab.all.length} words`);

  const children = [];

  // ── Cover Page ──
  children.push(spacer(800));
  children.push(p([
    { text: 'COMMUNICATE ', bold: true, size: 52, color: TEAL },
    { text: 'BY DESIGN', bold: true, size: 52, color: AMBER },
  ], { align: AlignmentType.CENTER, after: 200 }));
  children.push(rule(NAVY, 4));
  children.push(spacer(200));
  children.push(p(`${productLine} — Unit Printable Kit`, { bold: true, size: 36, align: AlignmentType.CENTER, after: 80 }));
  children.push(p(unitLabel, { bold: true, size: 28, color: TEAL, align: AlignmentType.CENTER, after: 120 }));
  children.push(rule(NAVY, 4));
  children.push(spacer(120));

  // Kit contents summary
  children.push(p('This kit contains:', { bold: true, size: 22, after: 60 }));
  children.push(p([
    { text: '1. ', bold: true, size: 20, color: TEAL },
    { text: 'Communication Partner Word List — ', bold: true, size: 20 },
    { text: 'vocabulary reference with Fitzgerald Key categories and device checklist', size: 20, color: '444444' },
  ], { after: 40 }));
  children.push(p([
    { text: '2. ', bold: true, size: 20, color: TEAL },
    { text: 'Symbol Cards (2.5" × 3.5") — ', bold: true, size: 20 },
    { text: 'ARASAAC symbols, 3-zone trading card layout for 9-pocket binder (PRINT IN COLOR)', size: 20, color: '444444' },
  ], { after: 40 }));
  children.push(p([
    { text: '3. ', bold: true, size: 20, color: TEAL },
    { text: 'Word Cards — ', bold: true, size: 20 },
    { text: 'text-only cards with Fitzgerald Key color strips for matching and sorting', size: 20, color: '444444' },
  ], { after: 40 }));
  children.push(p([
    { text: '4. ', bold: true, size: 20, color: TEAL },
    { text: 'Communication Board — ', bold: true, size: 20 },
    { text: 'compact grid organized by Fitzgerald Key for aided language input during lessons', size: 20, color: '444444' },
  ], { after: 120 }));

  children.push(spacer(120));
  children.push(p('These symbols support communication and participation across V3 activities: vocabulary preview, passage reading, annotation, comprehension responses, evidence citing, and discussion.', { size: 18, color: '666666', align: AlignmentType.CENTER, after: 80 }));
  children.push(p('Use with e-trans boards, symbol exchange, partner-assisted scanning, direct selection, or alongside the student\'s device.', { size: 18, color: '666666', align: AlignmentType.CENTER, after: 120 }));
  children.push(rule(NAVY, 2));
  children.push(spacer(80));
  children.push(p('🖨️ SYMBOL CARDS & COMMUNICATION BOARD: Print in color, one-sided', { bold: true, size: 20, color: AMBER, align: AlignmentType.CENTER, after: 40 }));
  children.push(p('WORD LIST & WORD CARDS: Can be printed B&W', { size: 18, color: '666666', align: AlignmentType.CENTER, after: 200 }));
  children.push(p('Where AT Meets Practice', { size: 20, color: TEAL, italics: true, align: AlignmentType.CENTER }));

  // ── Component 1: Communication Partner Word List ──
  children.push(pageBreak());
  children.push(...buildPartnerWordList(config, vocab));

  // ── Component 2: Symbol Cards ──
  children.push(pageBreak());
  children.push(...buildSymbolCards(config, vocab, symbolDir));

  // ── Component 3: Word Cards ──
  children.push(pageBreak());
  children.push(...buildWordCards(config, vocab));

  // ── Component 4: Communication Board ──
  children.push(pageBreak());
  children.push(...buildCommunicationBoard(config, vocab, symbolDir, accessLevel));

  // ── Attribution ──
  children.push(pageBreak());
  children.push(spacer(400));
  children.push(p('Pictographic symbols © Government of Aragón. ARASAAC (arasaac.org). Licensed under CC BY-NC-SA 4.0.', { size: 16, color: '777777', italics: true, after: 80 }));
  children.push(p('Use symbols from your student\'s own AAC system first. These open-source symbols are provided as a universal reference when system-specific symbols are not available.', { size: 16, color: '777777', italics: true, after: 80 }));
  children.push(p('Fitzgerald Key categorization based on: Fitzgerald (1949), adapted by Goossens\', Crain, & Elder (1992). Color-coding matches standard AAC device conventions.', { size: 16, color: '777777', italics: true, after: 80 }));
  children.push(p('Core/fringe classification based on: Banajee et al. (2003), Van Tatenhove (2009).', { size: 16, color: '777777', italics: true, after: 80 }));
  children.push(p('© Communicate by Design. All rights reserved. communicatebydesign.substack.com', { size: 16, color: '777777', italics: true }));

  // ── Assemble Document ──
  const doc = new Document({
    title: `${productLine} — Unit Printable Kit: ${unitLabel}`,
    description: `Communicate by Design — Complete printable kit: word list, symbol cards, word cards, communication board`,
    creator: 'Communicate by Design',
    styles: {
      default: { document: { run: { font: FONT, size: 22 } } },
      paragraphStyles: [
        { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { size: 36, bold: true, font: FONT, color: NAVY }, paragraph: { spacing: { before: 120, after: 120 }, outlineLevel: 0 } },
        { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { size: 28, bold: true, font: FONT, color: NAVY }, paragraph: { spacing: { before: 200, after: 100 }, outlineLevel: 1 } },
      ],
    },
    sections: [{
      properties: {
        page: {
          size: { width: PAGE_W, height: PAGE_H },
          margin: { top: MARGIN, bottom: MARGIN, left: MARGIN, right: MARGIN },
        },
      },
      headers: {
        default: new Header({
          children: [new Paragraph({
            children: [
              new TextRun({ text: 'Communicate by Design', font: FONT, size: 16, color: TEAL, italics: true }),
              new TextRun({ text: `  |  ${productLine} Unit Printable Kit`, font: FONT, size: 16, color: AMBER }),
            ],
            border: { bottom: { style: BorderStyle.SINGLE, size: 1, color: 'CCCCCC', space: 4 } },
            spacing: { after: 0 },
          })],
        }),
      },
      footers: {
        default: new Footer({
          children: [new Paragraph({
            children: [
              new TextRun({ text: 'Where AT Meets Practice', font: FONT, size: 14, color: TEAL, italics: true }),
              new TextRun({ text: '  |  Page ', font: FONT, size: 14, color: '999999' }),
              new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 14, color: '999999' }),
            ],
            alignment: AlignmentType.CENTER,
            border: { top: { style: BorderStyle.SINGLE, size: 1, color: 'CCCCCC', space: 4 } },
            spacing: { before: 0 },
          })],
        }),
      },
      children,
    }],
  });

  fs.mkdirSync(outputDir, { recursive: true });
  let fileName;
  if (config.unitTitle) {
    const safeTitle = config.unitTitle.replace(/[^a-zA-Z0-9_-]/g, '_').replace(/_+/g, '_');
    fileName = `${safeTitle}_Printable_Kit.docx`;
  } else {
    fileName = `UFLI_L${String(config.number).padStart(2, '0')}_Printable_Kit.docx`;
  }
  const outputPath = path.join(outputDir, fileName);
  const buffer = await Packer.toBuffer(doc);
  fs.writeFileSync(outputPath, buffer);

  console.log(`    ✅ ${fileName} (${(buffer.length / 1024).toFixed(1)} KB)`);
  console.log(`    📄 4 components: Word List + Symbol Cards + Word Cards + Comm Board`);

  return { path: outputPath, size: buffer.length, wordCount: vocab.all.length };
}


// ══════════════════════════════════════════════════════════════
// CLI
// ══════════════════════════════════════════════════════════════

async function main() {
  console.log('═══════════════════════════════════════════════════');
  console.log('  COMMUNICATE BY DESIGN — Unit Printable Kit Builder');
  console.log('  Standard 5-component kit for any CbD unit');
  console.log('═══════════════════════════════════════════════════\n');

  const args = process.argv.slice(2);
  const configs = require('./ufli_lesson_configs');
  const symbolDir = path.join(__dirname, '..', 'Symbols', 'symbol_library');
  const outputDir = path.join(__dirname, 'Output', 'Printable_Kits');

  let toBuild = [];

  if (args.includes('--lesson')) {
    const num = parseInt(args[args.indexOf('--lesson') + 1]);
    const config = configs.find(c => c.number === num);
    if (!config) { console.error(`❌ Lesson ${num} not found`); process.exit(1); }
    toBuild = [config];
  } else if (args.includes('--range')) {
    const start = parseInt(args[args.indexOf('--range') + 1]);
    const end = parseInt(args[args.indexOf('--range') + 2]);
    toBuild = configs.filter(c => c.number >= start && c.number <= end && c.newWords.length > 0);
  } else if (args.includes('--all')) {
    toBuild = configs.filter(c => c.newWords.length > 0);
  } else {
    console.log('Usage:');
    console.log('  node build_unit_printable_kit.js --lesson 7');
    console.log('  node build_unit_printable_kit.js --range 5 10');
    console.log('  node build_unit_printable_kit.js --all');
    process.exit(0);
  }

  let totalKits = 0;
  let totalWords = 0;

  for (const config of toBuild) {
    const result = await buildUnitKit(config, { symbolDir, outputDir });
    if (result) {
      totalKits++;
      totalWords += result.wordCount;
    }
  }

  console.log(`\n═══════════════════════════════════════════════════`);
  console.log(`  ✅ ${totalKits} unit kits built (${totalWords} total words)`);
  console.log(`  📂 ${outputDir}`);
  console.log(`═══════════════════════════════════════════════════\n`);
}

// Export for programmatic use + run CLI
module.exports = { buildUnitKit, getUnitVocabulary };

if (require.main === module) {
  main().catch(err => { console.error('❌ Fatal:', err.message); process.exit(1); });
}

#!/usr/bin/env node
/**
 * UFLI Per-Lesson Packet Builder — Communicate by Design
 *
 * Generates a single per-lesson packet .docx from a lesson config.
 * Usage:
 *   node build_ufli_packet.js --lesson 1
 *   node build_ufli_packet.js --config path/to/config.json
 *   require('./build_ufli_packet').buildPacket(lessonConfig, outputDir)
 *
 * DESIGN ASSUMPTIONS (NEVER VIOLATE):
 *   - Student is a complex communicator, mostly nonspeaking
 *   - Student has NOTHING unless we provide it or list it
 *   - Words come from UFLI only — we don't add words
 *   - Core/fringe from AAC research (Banajee et al., 2003; Van Tatenhove, 2009)
 *   - No SLP gatekeeping — capacity-building model
 *   - Auditory confirmation loop: produce the PHONEME SOUND
 *   - Pacing flexes, scope doesn't
 *   - SGD is part of robust AAC, not required for phonics
 */

const path = require('path');
const fs = require('fs');
const https = require('https');
const sharp = require('sharp');
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
const cellMar = { top: 80, bottom: 80, left: 120, right: 120 };

const SYMBOL_PX = 180;
const SYMBOL_SIZE = 110;  // Larger symbols for literacy product
const WORD_LABEL_SIZE = 36;  // Big, readable word labels (18pt) — this is a reading product

// ── Symbol Normalization ─────────────────────────────────────
// Every ARASAAC symbol gets normalized to a standard square canvas
// so the library is consistent across all lessons and products.
const NORM_CANVAS = 400;   // Standard square canvas size (px)
const NORM_CONTENT = 340;  // Max content area within canvas (px) — leaves 30px padding each side
const NORM_BG = { r: 255, g: 255, b: 255, alpha: 1 };  // White background

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
    ...(opts.border ? { border: opts.border } : {}),
  });
}

function h1(text) {
  return new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun({ text, font: FONT, size: 36, bold: true, color: NAVY })], spacing: { after: 60 }, border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: TEAL, space: 4 } } });
}
function h2(text) {
  return new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun({ text, font: FONT, size: 28, bold: true, color: NAVY })], spacing: { before: 200, after: 100 } });
}
function spacer(n = 120) { return new Paragraph({ spacing: { after: n } }); }
function pageBreak() { return new Paragraph({ children: [new PageBreak()] }); }
function rule(color = TEAL, size = 3) { return new Paragraph({ border: { bottom: { style: BorderStyle.SINGLE, size, color, space: 1 } }, spacing: { after: 120 } }); }

function guidanceBox(title, paragraphs, accent) {
  const fill = accent === TEAL ? 'EBF5FB' : 'FFF8E7';
  const content = [];
  content.push(new Paragraph({ children: [new TextRun({ text: title, bold: true, font: FONT, size: 24, color: NAVY })], spacing: { after: 100 }, border: { bottom: { style: BorderStyle.SINGLE, size: 2, color: accent, space: 4 } } }));
  for (const para of paragraphs) {
    if (typeof para === 'string') content.push(new Paragraph({ children: [new TextRun({ text: para, font: FONT, size: 20, color: '333333' })], spacing: { after: 100 } }));
    else content.push(new Paragraph({ children: para.map(r => new TextRun({ font: FONT, size: 20, color: '333333', ...r })), spacing: { after: 100 } }));
  }
  return new Table({ width: { size: CW, type: WidthType.DXA }, columnWidths: [CW], rows: [new TableRow({ children: [new TableCell({
    children: content, width: { size: CW, type: WidthType.DXA },
    borders: { top: { style: BorderStyle.SINGLE, size: 1, color: accent }, bottom: { style: BorderStyle.SINGLE, size: 1, color: accent }, left: { style: BorderStyle.SINGLE, size: 12, color: accent }, right: { style: BorderStyle.SINGLE, size: 1, color: accent } },
    shading: { fill, type: ShadingType.CLEAR }, margins: { top: 200, bottom: 200, left: 250, right: 200 },
  })] })] });
}

// ── ARASAAC Symbol Fetcher ───────────────────────────────────
// Fetches real AAC pictograms from the ARASAAC API (same approach
// as the Alternative Pencil products). Falls back to placeholder
// if the API is unreachable.
const ARASAAC_SEARCH = 'https://api.arasaac.org/v1/pictograms/en/search/';
const ARASAAC_IMAGE  = 'https://static.arasaac.org/pictograms/';

function httpsGet(url) {
  return new Promise((resolve, reject) => {
    const req = https.get(url, { headers: { 'User-Agent': 'CommunicateByDesign/1.0' } }, res => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        return httpsGet(res.headers.location).then(resolve).catch(reject);
      }
      const chunks = [];
      res.on('data', c => chunks.push(c));
      res.on('end', () => resolve({ status: res.statusCode, data: Buffer.concat(chunks) }));
    });
    req.on('error', reject);
    req.setTimeout(12000, () => { req.destroy(); reject(new Error('timeout')); });
  });
}

/**
 * Normalize a symbol image to a standard square canvas.
 * Trims whitespace, resizes content to fit within NORM_CONTENT area,
 * then centers on a NORM_CANVAS × NORM_CANVAS white square.
 * This ensures every symbol in the CbD library looks the same size.
 */
async function normalizeSymbol(inputBuffer) {
  // Step 1: Trim whitespace/transparency from the source image
  const trimmed = sharp(inputBuffer).trim();
  const trimMeta = await trimmed.toBuffer({ resolveWithObject: true });

  // Step 2: Resize trimmed content to fit within NORM_CONTENT box (preserve aspect ratio)
  const resized = await sharp(trimMeta.data)
    .resize(NORM_CONTENT, NORM_CONTENT, { fit: 'inside', withoutEnlargement: false })
    .toBuffer({ resolveWithObject: true });

  // Step 3: Center on standard white canvas
  const rInfo = resized.info;
  const left = Math.floor((NORM_CANVAS - rInfo.width) / 2);
  const top = Math.floor((NORM_CANVAS - rInfo.height) / 2);

  const normalized = await sharp({
    create: { width: NORM_CANVAS, height: NORM_CANVAS, channels: 4, background: NORM_BG }
  })
    .composite([{ input: resized.data, left, top }])
    .png()
    .toBuffer();

  return normalized;
}

async function fetchArasaacSymbol(word, cacheDir) {
  const cachedPath = path.join(cacheDir, `arasaac_${word}.png`);
  if (fs.existsSync(cachedPath)) return cachedPath;

  try {
    const searchRes = await httpsGet(ARASAAC_SEARCH + encodeURIComponent(word));
    if (searchRes.status !== 200) return null;
    const results = JSON.parse(searchRes.data.toString());
    if (!results || results.length === 0) return null;

    const id = results[0]._id;
    const imgRes = await httpsGet(`${ARASAAC_IMAGE}${id}/${id}_500.png`);
    if (imgRes.status !== 200) return null;

    // Normalize to standard canvas before caching
    const normalized = await normalizeSymbol(imgRes.data);
    fs.writeFileSync(cachedPath, normalized);
    return cachedPath;
  } catch (e) {
    return null;
  }
}

async function fetchAllSymbols(words, cacheDir) {
  fs.mkdirSync(cacheDir, { recursive: true });
  const symbolMap = {};
  for (const word of words) {
    const filePath = await fetchArasaacSymbol(word, cacheDir);
    symbolMap[word] = filePath;
    if (filePath) {
      // Rate limit: 200ms between requests (only if we actually hit the API)
      if (!fs.existsSync(path.join(cacheDir, `arasaac_${word}.png`))) {
        await new Promise(r => setTimeout(r, 200));
      }
    }
  }
  return symbolMap;
}

function getSymbolPath(word, cacheDir) {
  return path.join(cacheDir, `arasaac_${word}.png`);
}

// ── Build Packet ─────────────────────────────────────────────
async function buildPacket(LESSON, outputDir) {
  // Normalized symbol library — every symbol is a standardized 400×400 canvas
  const cacheDir = path.join(__dirname, 'symbol_library');
  const allWords = [
    ...LESSON.newWords.map(w => w.word),
    ...LESSON.reviewWords.map(w => w.word),
    ...(LESSON.heartWords || []),
  ];

  console.log(`  Fetching ARASAAC symbols for ${allWords.length} words...`);
  const symbolMap = await fetchAllSymbols(allWords, cacheDir);
  const fetched = Object.values(symbolMap).filter(v => v !== null).length;
  console.log(`  ${fetched}/${allWords.length} symbols fetched from ARASAAC`);

  const children = [];

  // ════════════════════════════════════════════════════════════
  // COVER / LESSON INFO PAGE
  // ════════════════════════════════════════════════════════════
  children.push(spacer(1200));
  children.push(p([
    {text: 'COMMUNICATE ', bold: true, size: 52, color: TEAL},
    {text: 'BY DESIGN', bold: true, size: 52, color: AMBER},
  ], {align: AlignmentType.CENTER, after: 200}));
  children.push(rule(NAVY, 4));
  children.push(spacer(200));

  // Lesson number and phoneme
  const phonemeLabel = LESSON.phoneme;
  const graphemeLabel = LESSON.grapheme;
  children.push(p(`UFLI Lesson ${LESSON.number}`, {bold: true, size: 44, align: AlignmentType.CENTER, after: 80, color: NAVY}));
  children.push(p(`Consonant ${phonemeLabel}  ·  Grapheme: ${graphemeLabel}`, {size: 28, color: TEAL, align: AlignmentType.CENTER, after: 200}));
  children.push(rule(NAVY, 4));
  children.push(spacer(200));

  children.push(p('Complex Communicator Access Layer \u2014 Per-Lesson Packet', {size: 22, color: '555555', align: AlignmentType.CENTER, after: 120}));
  children.push(p('Symbol Cards  \u00b7  Review Words  \u00b7  Heart Words  \u00b7  Morphology Notes', {size: 20, color: '777777', align: AlignmentType.CENTER, after: 200}));

  // ── ACCESS METHOD COMPATIBILITY STATEMENT ──
  children.push(rule(TEAL, 2));
  children.push(spacer(60));
  children.push(p('ACCESS METHODS SUPPORTED', {bold: true, size: 18, color: NAVY, align: AlignmentType.CENTER, after: 60}));
  children.push(p([
    {text: 'Direct selection', size: 16, color: '444444'},
    {text: '  \u2022  ', size: 16, color: TEAL},
    {text: 'Eye gaze', size: 16, color: '444444'},
    {text: '  \u2022  ', size: 16, color: TEAL},
    {text: 'Partner-assisted scanning', size: 16, color: '444444'},
    {text: '  \u2022  ', size: 16, color: TEAL},
    {text: 'Switch scanning', size: 16, color: '444444'},
  ], {align: AlignmentType.CENTER, after: 30}));
  children.push(p([
    {text: 'Head pointer', size: 16, color: '444444'},
    {text: '  \u2022  ', size: 16, color: TEAL},
    {text: 'Adapted keyboard', size: 16, color: '444444'},
    {text: '  \u2022  ', size: 16, color: TEAL},
    {text: 'SGD (any system)', size: 16, color: '444444'},
    {text: '  \u2022  ', size: 16, color: TEAL},
    {text: 'Low-tech AAC (PECS, e-trans)', size: 16, color: '444444'},
    {text: '  \u2022  ', size: 16, color: TEAL},
    {text: 'No-tech', size: 16, color: '444444'},
  ], {align: AlignmentType.CENTER, after: 60}));
  children.push(rule(TEAL, 2));
  children.push(spacer(120));

  // Prerequisite note — capacity-building framing
  children.push(guidanceBox('USING THIS PACKET', [
    'This packet is part of the Communicate by Design UFLI + AAC Literacy Series. Use it alongside the Teacher Guide, which covers the adapted 8-step routine, access options, prompting framework, and pacing guidance.',
    [
      {text: '4 tools for every lesson: ', bold: true, color: NAVY},
      {text: '(1) alternative pencil for encoding, (2) e-trans board for decoding, (3) symbol cards from this packet, (4) phoneme sound access. If any of these are not yet in place, see the Teacher Guide for how to develop them alongside instruction.'},
    ],
  ], TEAL));

  children.push(spacer(120));
  children.push(guidanceBox('🖨️ PRINTING NOTES', [
    [
      {text: 'Print symbol card pages ONE-SIDED. ', bold: true, color: NAVY},
      {text: 'Symbol cards need to be cut out and used individually on e-trans boards, in binders, or as PECS exchange cards. Double-sided printing makes them unusable.'},
    ],
    'The data tracker on the last page can be printed separately or photocopied as needed.',
  ], AMBER));

  children.push(spacer(120));
  children.push(rule('CCCCCC', 1));
  children.push(p('Where AT Meets Practice', {size: 18, color: TEAL, italics: true, align: AlignmentType.CENTER}));

  // ════════════════════════════════════════════════════════════
  // PARTNER MODES & PROMPT HIERARCHY PAGE
  // Separate page — before Lesson At a Glance
  // CbD 5-Level Framework (LOCKED March 2026)
  // Codes: I / G– / G+ / VM / RA
  // ════════════════════════════════════════════════════════════
  children.push(pageBreak()); // end cover page

  children.push(h1('Partner Modes & Prompt Hierarchy'));
  children.push(p([
    {text: 'Quick reference for communication partners. The prompt hierarchy applies only in ', size: 19, color: '444444'},
    {text: 'Mode 1 \u2014 Instructional.', bold: true, size: 19, color: NAVY},
    {text: ' Always check preconditions first.', size: 19, color: '444444'},
  ], {after: 140}));

  // PRECONDITIONS
  children.push(guidanceBox('PRECONDITIONS (Always Active \u2014 Every Mode)', [
    [
      {text: 'ALI (Aided Language Input): ', bold: true, color: NAVY},
      {text: 'Partner models on the student\u2019s own communication system during natural activity. Not a prompt \u2014 a demonstration.'},
    ],
    [
      {text: 'Communication Environment: ', bold: true, color: NAVY},
      {text: 'Student\u2019s system is present, charged, accessible, and positioned. Vocabulary is programmed. Activity has something worth saying. Check these before starting any mode.'},
    ],
  ], TEAL));
  children.push(spacer(140));

  // THREE PARTNER MODES
  children.push(p([{text: 'Three Partner Modes', bold: true, size: 24, color: NAVY}], {after: 80}));
  const modeColW = Math.floor(CW / 3);
  const modeWidths3 = [modeColW, modeColW, CW - modeColW * 2];
  const modeDefs3 = [
    { num: 'Mode 1', name: 'Instructional', bullets: ['Prompt hierarchy active', 'Data collection running', 'Correct / incorrect applies'], note: 'Hierarchy is for this mode only \u2193', bg: NAVY, fg: 'FFFFFF' },
    { num: 'Mode 2', name: 'Partnership', bullets: ['No demands, no hierarchy', 'Partner follows student lead', 'Note spontaneous communication'], note: 'Transitions, breaks, free choice', bg: '005F8A', fg: 'FFFFFF' },
    { num: 'Mode 3', name: 'Facilitated Participation', bullets: ['Physical access support only', 'No interpretation, no editorializing', 'Partner enables \u2014 does not direct'], note: 'Group activities and routines', bg: 'EBF5FB', fg: NAVY },
  ];
  const modeCells3 = modeDefs3.map((m, i) => {
    const mContent = [
      new Paragraph({ children: [new TextRun({ text: m.num, bold: true, font: FONT, size: 20, color: m.fg })], spacing: { after: 10 } }),
      new Paragraph({ children: [new TextRun({ text: m.name, bold: true, font: FONT, size: 22, color: m.fg })], spacing: { after: 80 }, border: { bottom: { style: BorderStyle.SINGLE, size: 2, color: m.fg === 'FFFFFF' ? '4A8AAA' : 'BBBBBB', space: 4 } } }),
    ];
    for (const b of m.bullets) {
      mContent.push(new Paragraph({ children: [new TextRun({ text: '\u2022 ', font: FONT, size: 17, color: m.fg }), new TextRun({ text: b, font: FONT, size: 17, color: m.fg })], spacing: { after: 30 } }));
    }
    mContent.push(new Paragraph({ children: [new TextRun({ text: m.note, font: FONT, size: 14, color: m.fg, italics: true })], spacing: { after: 0, before: 60 } }));
    return new TableCell({ children: mContent, width: { size: modeWidths3[i], type: WidthType.DXA }, borders, margins: { top: 140, bottom: 140, left: 140, right: 140 }, shading: { fill: m.bg, type: ShadingType.CLEAR } });
  });
  children.push(new Table({ rows: [new TableRow({ children: modeCells3 })], width: { size: CW, type: WidthType.DXA }, columnWidths: modeWidths3 }));
  children.push(spacer(160));

  // MODE 1 PROMPT HIERARCHY LADDER
  children.push(p([
    {text: 'Mode 1 \u2014 Prompt Hierarchy', bold: true, size: 24, color: NAVY},
    {text: '   Tracker codes: ', size: 18, color: '666666'},
    {text: 'I  /  G\u2013  /  G+  /  VM  /  RA', bold: true, size: 18, color: TEAL},
    {text: '  (record highest level of support needed)', size: 15, color: '888888'},
  ], {after: 70}));
  children.push(p([
    {text: 'Para defaulting to Mode 1 in all contexts is the most common AAC barrier. ', bold: true, size: 17, color: NAVY},
    {text: 'Non-response = ask why, not stop.', size: 17, color: '444444', italics: true},
  ], {after: 110}));

  const colBadgeH = 1700;
  const colDetailH = CW - colBadgeH;
  const ladderItems = [
    { code: 'I',     label: 'INDEPENDENT',       subLabel: '\u2605 Goal',         subColor: 'FFD700', bg: NAVY,     fg: 'FFFFFF', desc: 'Student communicates without any prompting needed.', note: 'This is the goal. Respond naturally and with enthusiasm.' },
    { code: 'G\u2013', label: 'INDIRECT CUE',   subLabel: null,                   bg: '005F8A', fg: 'FFFFFF', desc: 'Gesture toward the student\u2019s communication system as a whole.', note: 'Do NOT point to a specific symbol or page. Gesture to the system, then wait.' },
    { code: 'G+',    label: 'DIRECT CUE',         subLabel: null,                   bg: '006DA0', fg: 'FFFFFF', desc: 'Point to a specific symbol, location, or page on the student\u2019s system.', note: 'Narrows the field. Use when G\u2013 produced no response after a full wait.' },
    { code: 'VM',    label: 'VERBAL MODEL',        subLabel: null,                   bg: '4A9EC0', fg: 'FFFFFF', desc: 'Say the message aloud and demonstrate it on the student\u2019s own system.', note: '"You can say \u2018more\u2019 \u2014 here." [touch symbol] Then re-present the opportunity.' },
    { code: 'RA',    label: 'REASSESS ACCESS',     subLabel: '\u26a0 Stop & Check', subColor: AMBER, bg: 'FFF8E7', fg: NAVY,    desc: 'Non-response is data about the environment \u2014 not the student.', note: 'Stop. Check: positioning \u2219 system accessible \u2219 vocabulary present \u2219 activity worth saying something \u2219 partner behavior.' },
  ];
  const ladderRows = [];
  ladderItems.forEach((lv, idx) => {
    const badgeContent = [
      new Paragraph({ children: [new TextRun({ text: lv.code, bold: true, font: FONT, size: 38, color: lv.fg })], spacing: { after: 10 }, alignment: AlignmentType.CENTER }),
      new Paragraph({ children: [new TextRun({ text: lv.label, bold: true, font: FONT, size: 13, color: lv.fg })], spacing: { after: lv.subLabel ? 10 : 0 }, alignment: AlignmentType.CENTER }),
    ];
    if (lv.subLabel) {
      badgeContent.push(new Paragraph({ children: [new TextRun({ text: lv.subLabel, font: FONT, size: 13, color: lv.subColor || lv.fg, italics: true })], spacing: { after: 0 }, alignment: AlignmentType.CENTER }));
    }
    ladderRows.push(new TableRow({ children: [
      new TableCell({ children: badgeContent, width: { size: colBadgeH, type: WidthType.DXA }, borders, margins: { top: 120, bottom: 120, left: 80, right: 80 }, shading: { fill: lv.bg, type: ShadingType.CLEAR } }),
      new TableCell({ children: [
        new Paragraph({ children: [new TextRun({ text: lv.desc, font: FONT, size: 19, color: lv.fg })], spacing: { after: 50 } }),
        new Paragraph({ children: [new TextRun({ text: lv.note, font: FONT, size: 15, color: lv.fg, italics: true })], spacing: { after: 0 } }),
      ], width: { size: colDetailH, type: WidthType.DXA }, borders, margins: { top: 100, bottom: 100, left: 160, right: 160 }, shading: { fill: lv.bg, type: ShadingType.CLEAR } }),
    ]}));
    if (idx < ladderItems.length - 1) {
      ladderRows.push(new TableRow({ children: [
        new TableCell({ children: [new Paragraph({ spacing: { after: 0 } })], width: { size: colBadgeH, type: WidthType.DXA }, borders: noBorders, margins: { top: 20, bottom: 20, left: 0, right: 0 }, shading: { fill: 'FFF8E7', type: ShadingType.CLEAR } }),
        new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: 'WAIT \u2014 minimum 10 seconds before moving to the next level', bold: true, font: FONT, size: 14, color: AMBER })], spacing: { after: 0 } })], width: { size: colDetailH, type: WidthType.DXA }, borders: noBorders, margins: { top: 40, bottom: 40, left: 160, right: 160 }, shading: { fill: 'FFF8E7', type: ShadingType.CLEAR } }),
      ]}));
    }
  });
  children.push(new Table({ rows: ladderRows, width: { size: CW, type: WidthType.DXA }, columnWidths: [colBadgeH, colDetailH] }));

  // ════════════════════════════════════════════════════════════
  // LESSON INFO TABLE
  // ════════════════════════════════════════════════════════════
  children.push(pageBreak());
  children.push(h1(`Lesson ${LESSON.number} — At a Glance`));
  children.push(spacer(100));

  const infoLabelW = 2800;
  const infoValW = CW - infoLabelW;
  const infoRows = [];

  const addInfoRow = (label, value, shade) => {
    infoRows.push(new TableRow({ children: [
      new TableCell({ children: [new Paragraph({children: [new TextRun({text: label, bold: true, font: FONT, size: 22, color: 'FFFFFF'})], spacing: {after: 0}})], width: {size: infoLabelW, type: WidthType.DXA}, borders, margins: cellMar, shading: {fill: NAVY, type: ShadingType.CLEAR} }),
      new TableCell({ children: [new Paragraph({children: [new TextRun({text: value, font: FONT, size: 22, color: NAVY})], spacing: {after: 0}})], width: {size: infoValW, type: WidthType.DXA}, borders, margins: cellMar, shading: shade ? {fill: shade, type: ShadingType.CLEAR} : undefined }),
    ]}));
  };

  addInfoRow('Lesson', String(LESSON.number));
  addInfoRow('Phoneme', LESSON.phoneme, 'F4F6F8');
  addInfoRow('Grapheme', LESSON.grapheme);

  // New words split by type — clean, scannable
  const coreWords = LESSON.newWords.filter(w => w.type === 'core').map(w => w.word);
  const fringeWords = LESSON.newWords.filter(w => w.type === 'fringe').map(w => w.word);
  addInfoRow('New Words (core)', coreWords.join(', ') || 'None this lesson', 'F4F6F8');
  addInfoRow('New Words (fringe)', fringeWords.join(', ') || 'None this lesson');
  addInfoRow('Review Words', LESSON.reviewWords.map(w => w.word).join(', ') || 'None this lesson', 'F4F6F8');
  addInfoRow('Heart Words', LESSON.heartWords.join(', ') || 'None this lesson');

  children.push(new Table({ rows: infoRows, width: {size: CW, type: WidthType.DXA}, columnWidths: [infoLabelW, infoValW] }));

  // Word use by step
  children.push(spacer(250));
  children.push(h2('Words Used at Each Step'));
  children.push(p('Reference for which words to prepare at each UFLI step. See the Teacher Guide for full communication partner scripts and access options.', {size: 18, color: '666666', italics: true, after: 120}));

  const stepLabelW = 2600;
  const stepWordsW = CW - stepLabelW;
  const stepRows = [];

  const stepHeader = new TableRow({ children: [
    new TableCell({ children: [new Paragraph({children: [new TextRun({text: 'UFLI Step', bold: true, font: FONT, size: 20, color: 'FFFFFF'})], spacing: {after: 0}})], width: {size: stepLabelW, type: WidthType.DXA}, borders, margins: cellMar, shading: {fill: NAVY, type: ShadingType.CLEAR} }),
    new TableCell({ children: [new Paragraph({children: [new TextRun({text: 'Words / Materials', bold: true, font: FONT, size: 20, color: 'FFFFFF'})], spacing: {after: 0}})], width: {size: stepWordsW, type: WidthType.DXA}, borders, margins: cellMar, shading: {fill: NAVY, type: ShadingType.CLEAR} }),
  ]});
  stepRows.push(stepHeader);

  const newWordStr = LESSON.newWords.map(w => w.word).join(', ');
  const reviewWordStr = LESSON.reviewWords.map(w => w.word).join(', ');
  const allWordStr = [...LESSON.newWords.map(w => w.word), ...LESSON.reviewWords.map(w => w.word)].join(', ');
  const heartWordStr = LESSON.heartWords.join(', ');

  const steps = [
    ['Step 1: Phonemic Awareness', `E-trans board with symbol cards: ${newWordStr || 'new words'}`, 'F4F6F8'],
    ['Step 2: Visual Drill', `Phoneme cards for review + new: ${LESSON.phoneme}`, ''],
    ['Step 3: Auditory Drill', `Alternative pencil — student selects "${LESSON.grapheme}" from full alphabet`, 'F4F6F8'],
    ['Step 4: Blending Drill', `E-trans board: ${newWordStr || 'new words'} (use phonetically similar distractors)`, ''],
    ['Step 5: New Concept', `New words only: ${newWordStr || 'new words'}. Start with 2–3 on e-trans, expand to 4.`, 'F4F6F8'],
    ['Step 6: Word Chain', `New + review words on e-trans board. Alternative pencil for letter swap.`, ''],
    ['Step 7: Heart Words', heartWordStr ? `Heart words: ${heartWordStr}. E-trans + alternative pencil.` : 'No heart words this lesson.', 'F4F6F8'],
    ['Step 8: Connected Text', `All symbol cards on e-trans board. Preview 3–5 target words before reading.`, ''],
  ];

  steps.forEach(([label, words, shade]) => {
    stepRows.push(new TableRow({ children: [
      new TableCell({ children: [new Paragraph({children: [new TextRun({text: label, bold: true, font: FONT, size: 20, color: NAVY})], spacing: {after: 0}})], width: {size: stepLabelW, type: WidthType.DXA}, borders, margins: cellMar, shading: shade ? {fill: shade, type: ShadingType.CLEAR} : undefined }),
      new TableCell({ children: [new Paragraph({children: [new TextRun({text: words, font: FONT, size: 20, color: '333333'})], spacing: {after: 0}})], width: {size: stepWordsW, type: WidthType.DXA}, borders, margins: cellMar, shading: shade ? {fill: shade, type: ShadingType.CLEAR} : undefined }),
    ]}));
  });

  children.push(new Table({ rows: stepRows, width: {size: CW, type: WidthType.DXA}, columnWidths: [stepLabelW, stepWordsW] }));

  // ════════════════════════════════════════════════════════════
  // SYMBOL CARDS — new words, labeled core/fringe
  // ════════════════════════════════════════════════════════════
  children.push(pageBreak());
  children.push(h1(`Symbol Cards — Lesson ${LESSON.number}: ${LESSON.phoneme}`));
  children.push(p('Print, cut, and add to the student\'s binder. Each word is labeled as core (high-frequency, used across all contexts) or fringe (lesson-specific vocabulary).', {size: 18, color: '666666', italics: true, after: 60}));
  children.push(p([
    {text: 'Eye gaze users: ', bold: true, color: NAVY, size: 18},
    {text: 'When placing cards on an e-trans board, space them at least 3 inches apart for reliable gaze discrimination. Use a maximum of 4 cards per e-trans board. Cards should be at least 1 inch square for gaze access at 18 inches.', size: 18, color: '666666', italics: true},
  ], {after: 60}));
  children.push(p([
    {text: '✏️ Draw It! ', bold: true, color: AMBER, size: 18},
    {text: 'Some cards have a drawing box instead of a symbol — these words don\'t have a pictogram in the symbol library. Before the lesson, draw a quick picture together! For real words, draw what it means. For made-up or silly words (like "plog" or "squib"), let the student make up the drawing. This is a fun warm-up that builds word ownership.', size: 18, color: '666666', italics: true},
  ], {after: 100}));
  children.push(rule(TEAL));

  // Build symbol card grid
  const COLS = 4;
  const colW = Math.floor(CW / COLS);
  const symRows = [];

  for (let i = 0; i < LESSON.newWords.length; i += COLS) {
    const rowItems = LESSON.newWords.slice(i, i + COLS);
    const cells = rowItems.map(item => {
      const fp = getSymbolPath(item.word, cacheDir);
      const c = [];
      if (fs.existsSync(fp)) {
        c.push(new Paragraph({ children: [new ImageRun({ type: 'png', data: fs.readFileSync(fp), transformation: {width: SYMBOL_SIZE, height: SYMBOL_SIZE}, altText: {title: item.word, description: `Symbol for ${item.word}`, name: item.word} })], alignment: AlignmentType.CENTER, spacing: {after: 0} }));
      } else {
        // Drawing box — fun warm-up activity for words without symbols
        c.push(new Paragraph({ children: [new TextRun({ text: '✏️ Draw it!', font: FONT, size: 14, color: AMBER, bold: true })], alignment: AlignmentType.CENTER, spacing: {after: 20} }));
        // Empty space for drawing (using underscores as a visual box frame)
        c.push(new Paragraph({ spacing: {after: 60} }));
        c.push(new Paragraph({ spacing: {after: 60} }));
      }
      c.push(new Paragraph({ children: [new TextRun({ text: item.word, bold: true, font: FONT, size: WORD_LABEL_SIZE, color: NAVY })], alignment: AlignmentType.CENTER, spacing: {before: 60, after: 0} }));
      const tagColor = item.type === 'core' ? TEAL : AMBER;
      const tagText = item.type === 'core' ? 'core' : 'fringe';
      c.push(new Paragraph({ children: [new TextRun({ text: tagText, font: FONT, size: 18, color: tagColor, italics: true })], alignment: AlignmentType.CENTER, spacing: {before: 20, after: 0} }));
      return new TableCell({ children: c, width: {size: colW, type: WidthType.DXA}, borders, margins: {top: 100, bottom: 80, left: 60, right: 60} });
    });
    while (cells.length < COLS) cells.push(new TableCell({ children: [new Paragraph({spacing: {after: 0}})], width: {size: colW, type: WidthType.DXA}, borders: noBorders }));
    symRows.push(new TableRow({ children: cells }));
  }

  children.push(new Table({ rows: symRows, width: {size: CW, type: WidthType.DXA}, columnWidths: Array(COLS).fill(colW) }));

  // ════════════════════════════════════════════════════════════
  // SYMBOL-ONLY CARDS — for reading practice (after symbols taught)
  // Student reads the word, then finds the matching symbol.
  // ════════════════════════════════════════════════════════════
  children.push(pageBreak());
  children.push(h1(`Reading Practice Cards — Lesson ${LESSON.number}`));
  children.push(guidanceBox('WHEN TO USE THESE', [
    'Use these AFTER the student has learned the labeled symbol cards above. The student reads a word from the word list, then selects, points to, or uses gaze to indicate the matching symbol. This is the comprehension check — the student is reading, not just matching text to text.',
    [
      {text: 'How to present: ', bold: true, color: NAVY},
      {text: 'Place 2–4 symbol-only cards on the e-trans board. Show or say a word. The student indicates the correct symbol. Increase the field size as the student demonstrates mastery.'},
    ],
  ], TEAL));
  children.push(spacer(100));

  // Symbol-only grid (no word labels)
  children.push(p('Symbol Cards (No Labels)', {bold: true, size: 26, color: NAVY, after: 80}));
  children.push(rule(TEAL));
  const soRows = [];
  // Combine new words + heart words for symbol-only cards
  const allSymbolWords = [
    ...LESSON.newWords.map(w => ({ word: w.word, type: w.type })),
    ...(LESSON.heartWords || []).map(hw => ({ word: hw, type: 'heart' })),
  ];

  for (let i = 0; i < allSymbolWords.length; i += COLS) {
    const rowItems = allSymbolWords.slice(i, i + COLS);
    const cells = rowItems.map(item => {
      const fp = getSymbolPath(item.word, cacheDir);
      const c = [];
      if (fs.existsSync(fp)) {
        c.push(new Paragraph({ children: [new ImageRun({ type: 'png', data: fs.readFileSync(fp), transformation: {width: SYMBOL_SIZE + 20, height: SYMBOL_SIZE + 20}, altText: {title: item.word, description: `Symbol for ${item.word}`, name: item.word} })], alignment: AlignmentType.CENTER, spacing: {after: 0} }));
      } else {
        // Student's drawing goes here — their version of the word
        c.push(new Paragraph({ children: [new TextRun({ text: '✏️', font: FONT, size: 20 })], alignment: AlignmentType.CENTER, spacing: {after: 20} }));
        c.push(new Paragraph({ spacing: {after: 60} }));
        c.push(new Paragraph({ spacing: {after: 40} }));
      }
      // Thin line at bottom for teacher to write word after student identifies it (optional)
      c.push(new Paragraph({ children: [new TextRun({ text: '________________', font: FONT, size: 16, color: 'CCCCCC' })], alignment: AlignmentType.CENTER, spacing: {before: 40, after: 0} }));
      return new TableCell({ children: c, width: {size: colW, type: WidthType.DXA}, borders, margins: {top: 100, bottom: 80, left: 60, right: 60} });
    });
    while (cells.length < COLS) cells.push(new TableCell({ children: [new Paragraph({spacing: {after: 0}})], width: {size: colW, type: WidthType.DXA}, borders: noBorders }));
    soRows.push(new TableRow({ children: cells }));
  }
  children.push(new Table({ rows: soRows, width: {size: CW, type: WidthType.DXA}, columnWidths: Array(COLS).fill(colW) }));

  // Word list for matching
  children.push(spacer(200));
  children.push(p('Word List — Read and Match', {bold: true, size: 26, color: NAVY, after: 80}));
  children.push(rule(TEAL));
  children.push(p('Present these words one at a time. The student reads the word, then indicates the matching symbol above.', {size: 18, color: '666666', italics: true, after: 120}));

  const wlCols = Math.min(allSymbolWords.length, 4);
  const wlColW = Math.floor(CW / wlCols);
  const wlRows = [];
  for (let i = 0; i < allSymbolWords.length; i += wlCols) {
    const rowItems = allSymbolWords.slice(i, i + wlCols);
    const cells = rowItems.map(item => {
      return new TableCell({
        children: [
          new Paragraph({ children: [new TextRun({ text: item.word, bold: true, font: FONT, size: 44, color: NAVY })], alignment: AlignmentType.CENTER, spacing: {after: 0} }),
        ],
        width: {size: wlColW, type: WidthType.DXA}, borders, margins: {top: 120, bottom: 120, left: 60, right: 60},
      });
    });
    while (cells.length < wlCols) cells.push(new TableCell({ children: [new Paragraph({spacing: {after: 0}})], width: {size: wlColW, type: WidthType.DXA}, borders: noBorders }));
    wlRows.push(new TableRow({ children: cells }));
  }
  children.push(new Table({ rows: wlRows, width: {size: CW, type: WidthType.DXA}, columnWidths: Array(wlCols).fill(wlColW) }));

  // ════════════════════════════════════════════════════════════
  // REVIEW WORDS, HEART WORDS, MORPHOLOGY — grouped on one page
  // ════════════════════════════════════════════════════════════
  children.push(pageBreak());
  children.push(h1(`Lesson ${LESSON.number} — Reference Materials`));
  children.push(spacer(80));

  if (LESSON.reviewWords.length > 0) {
    children.push(h2('Review Words — Pull From Binder'));
    children.push(p([
      {text: 'Pull these cards from the student\'s binder. Words are grouped by ', size: 18, color: '666666', italics: true},
      {text: 'Fitzgerald Key', size: 18, color: NAVY, bold: true, italics: true},
      {text: ' categories — the same color-coding system used on most AAC devices. Organize your binder the same way for consistency.', size: 18, color: '666666', italics: true},
    ], {after: 100}));

    // Group review words by Fitzgerald Key category
    const fitzGroups = groupByFitzgerald(LESSON.reviewWords);
    const fitzBorder = { style: BorderStyle.SINGLE, size: 1, color: 'DDDDDD' };
    const fitzBorders = { top: fitzBorder, bottom: fitzBorder, left: fitzBorder, right: fitzBorder };

    for (const group of fitzGroups) {
      // Category header with color strip
      const stripW = 300;
      const labelW = CW - stripW;
      children.push(new Table({ rows: [new TableRow({ children: [
        new TableCell({ children: [new Paragraph({spacing: {after: 0}})], width: {size: stripW, type: WidthType.DXA}, borders: noBorders, shading: {fill: group.color, type: ShadingType.CLEAR} }),
        new TableCell({ children: [new Paragraph({children: [
          new TextRun({text: `${group.label}`, bold: true, font: FONT, size: 22, color: NAVY}),
          new TextRun({text: `  (${group.words.length} word${group.words.length > 1 ? 's' : ''})`, font: FONT, size: 18, color: '999999'}),
        ], spacing: {after: 0}})], width: {size: labelW, type: WidthType.DXA}, borders: noBorders, margins: {top: 60, bottom: 60, left: 120, right: 60} }),
      ]})], width: {size: CW, type: WidthType.DXA} }));

      // Word chips — compact inline layout, 5 per row
      const CHIPS_PER_ROW = 5;
      const chipW = Math.floor(CW / CHIPS_PER_ROW);
      for (let i = 0; i < group.words.length; i += CHIPS_PER_ROW) {
        const rowWords = group.words.slice(i, i + CHIPS_PER_ROW);
        const cells = rowWords.map(rw => {
          const tagColor = rw.type === 'core' ? TEAL : AMBER;
          return new TableCell({ children: [
            new Paragraph({children: [new TextRun({text: rw.word, bold: true, font: FONT, size: 22, color: NAVY})], alignment: AlignmentType.CENTER, spacing: {after: 0}}),
            new Paragraph({children: [new TextRun({text: rw.type, font: FONT, size: 14, color: tagColor, italics: true})], alignment: AlignmentType.CENTER, spacing: {after: 0}}),
          ], width: {size: chipW, type: WidthType.DXA}, borders: fitzBorders, margins: {top: 40, bottom: 40, left: 30, right: 30} });
        });
        while (cells.length < CHIPS_PER_ROW) cells.push(new TableCell({ children: [new Paragraph({spacing: {after: 0}})], width: {size: chipW, type: WidthType.DXA}, borders: noBorders }));
        children.push(new Table({ rows: [new TableRow({ children: cells })], width: {size: CW, type: WidthType.DXA}, columnWidths: Array(CHIPS_PER_ROW).fill(chipW) }));
      }
      children.push(spacer(60));
    }

    // Fitzgerald Key legend
    children.push(spacer(40));
    children.push(p([
      {text: 'Fitzgerald Key: ', bold: true, size: 16, color: NAVY},
      {text: '■', size: 16, color: 'FFD700'}, {text: ' People  ', size: 14, color: '666666'},
      {text: '■', size: 16, color: '00A86B'}, {text: ' Actions  ', size: 14, color: '666666'},
      {text: '■', size: 16, color: 'FF8C00'}, {text: ' Descriptions  ', size: 14, color: '666666'},
      {text: '■', size: 16, color: 'CCCCCC'}, {text: ' Nouns  ', size: 14, color: '666666'},
      {text: '■', size: 16, color: '4A90D9'}, {text: ' Prepositions  ', size: 14, color: '666666'},
      {text: '■', size: 16, color: 'E88CA5'}, {text: ' Social', size: 14, color: '666666'},
    ], {after: 40}));
    children.push(p('This matches the color-coding on most AAC devices (TD Snap, LAMP, Proloquo2Go, TouchChat). Organize binder dividers by these colors for quick access during lessons.', {size: 14, color: '999999', italics: true, after: 60}));
  }

  // ════════════════════════════════════════════════════════════
  // HEART WORDS
  // ════════════════════════════════════════════════════════════
  if (LESSON.heartWords && LESSON.heartWords.length > 0) {
    children.push(spacer(200));
    children.push(h2('Heart Words'));
    children.push(p('These words don\'t follow regular phonics rules. The "heart part" must be memorized.', {size: 18, color: '666666', italics: true, after: 100}));

    // Heart words get the same symbol card layout as new words
    const hwCols = Math.min(LESSON.heartWords.length, 4);
    const hwColW = Math.floor(CW / hwCols);
    const hwRows = [];

    for (let i = 0; i < LESSON.heartWords.length; i += hwCols) {
      const rowItems = LESSON.heartWords.slice(i, i + hwCols);
      const cells = rowItems.map(hw => {
        const fp = getSymbolPath(hw, cacheDir);
        const c = [];
        if (fs.existsSync(fp)) {
          c.push(new Paragraph({ children: [new ImageRun({ type: 'png', data: fs.readFileSync(fp), transformation: {width: SYMBOL_SIZE, height: SYMBOL_SIZE}, altText: {title: hw, description: `Symbol for ${hw}`, name: hw} })], alignment: AlignmentType.CENTER, spacing: {after: 0} }));
        } else {
          c.push(new Paragraph({ children: [new TextRun({ text: '✏️ Draw it!', font: FONT, size: 14, color: AMBER, bold: true })], alignment: AlignmentType.CENTER, spacing: {after: 20} }));
          c.push(new Paragraph({ spacing: {after: 60} }));
          c.push(new Paragraph({ spacing: {after: 60} }));
        }
        c.push(new Paragraph({ children: [new TextRun({ text: hw, bold: true, font: FONT, size: WORD_LABEL_SIZE, color: NAVY })], alignment: AlignmentType.CENTER, spacing: {before: 60, after: 0} }));
        c.push(new Paragraph({ children: [new TextRun({ text: '♥ heart word', font: FONT, size: 18, color: 'CC3333', italics: true })], alignment: AlignmentType.CENTER, spacing: {before: 20, after: 0} }));
        return new TableCell({ children: c, width: {size: hwColW, type: WidthType.DXA}, borders, margins: {top: 100, bottom: 80, left: 60, right: 60} });
      });
      while (cells.length < hwCols) cells.push(new TableCell({ children: [new Paragraph({spacing: {after: 0}})], width: {size: hwColW, type: WidthType.DXA}, borders: noBorders }));
      hwRows.push(new TableRow({ children: cells }));
    }

    children.push(new Table({ rows: hwRows, width: {size: CW, type: WidthType.DXA}, columnWidths: Array(hwCols).fill(hwColW) }));
  }

  // ════════════════════════════════════════════════════════════
  // MORPHOLOGY NOTES
  // ════════════════════════════════════════════════════════════
  if (LESSON.morphologyNotes && LESSON.morphologyNotes.length > 0) {
    children.push(spacer(200));
    children.push(h2('Teaching Moment: Word Forms'));
    children.push(p('Some words in this lesson are related to words the student may already know. These are good opportunities to talk through how words change form.', {size: 20, color: '444444', after: 120}));
    for (const note of LESSON.morphologyNotes) {
      children.push(p([
        {text: `${note.word} `, bold: true, color: NAVY, size: 22},
        {text: `← ${note.base}: `, bold: true, color: TEAL, size: 20},
        {text: note.note, size: 20, color: '444444'},
      ], {after: 80}));
    }
  }

  // (Word Location Map removed — now a standalone team tool in the Teacher Guide)

  // ════════════════════════════════════════════════════════════
  // SESSION DATA TRACKER — printable, fill-in-after-each-session
  // ════════════════════════════════════════════════════════════
  children.push(pageBreak());
  children.push(h1(`Session Data Tracker — Lesson ${LESSON.number}`));
  children.push(p('Fill in after each session. Transfer totals to the compilation spreadsheet in the Teacher Guide.', {size: 18, color: '666666', italics: true, after: 80}));

  // Student info row
  const infoFieldW = Math.floor(CW / 3);
  children.push(new Table({ rows: [new TableRow({ children: [
    new TableCell({ children: [p([{text: 'Student: ', bold: true, size: 18, color: NAVY}, {text: '________________________', size: 18, color: 'CCCCCC'}])], width: {size: infoFieldW, type: WidthType.DXA}, borders: noBorders, margins: cellMar }),
    new TableCell({ children: [p([{text: 'Date: ', bold: true, size: 18, color: NAVY}, {text: '_______________', size: 18, color: 'CCCCCC'}])], width: {size: infoFieldW, type: WidthType.DXA}, borders: noBorders, margins: cellMar }),
    new TableCell({ children: [p([{text: 'Session #: ', bold: true, size: 18, color: NAVY}, {text: '________', size: 18, color: 'CCCCCC'}])], width: {size: infoFieldW, type: WidthType.DXA}, borders: noBorders, margins: cellMar }),
  ]})], width: {size: CW, type: WidthType.DXA} }));
  children.push(spacer(40));

  // SECTION 1: Prompt levels by step
  children.push(p([{text: '1. Prompt Level by UFLI Step', bold: true, size: 22, color: NAVY}], {after: 40}));
  children.push(p('Circle the highest level of support needed:  I = Independent  |  G\u2013 = Indirect Cue  |  G+ = Direct Cue  |  VM = Verbal Model  |  RA = Reassess Access', {size: 14, color: '666666', italics: true, after: 60}));

  const dtSteps = ['Step 1: Phonemic Awareness', 'Step 2: Visual Drill', 'Step 3: Auditory Drill', 'Step 4: Blending Drill', 'Step 5: New Concept', 'Step 6: Word Work', 'Step 7: Heart Words', 'Step 8: Connected Text'];
  const dtLevels = ['I', 'G\u2013', 'G+', 'VM', 'RA'];
  const dtStepW = 3200; const dtLvlW = Math.floor((CW - dtStepW - 1500) / 5); const dtNotesW = 1500;

  // Header
  const dtHeaderCells = [
    new TableCell({ children: [p('Step', {bold: true, size: 16, color: 'FFFFFF'})], width: {size: dtStepW, type: WidthType.DXA}, borders, margins: cellMar, shading: {fill: NAVY, type: ShadingType.CLEAR} }),
  ];
  for (const lv of dtLevels) {
    dtHeaderCells.push(new TableCell({ children: [p(lv, {bold: true, size: 18, color: 'FFFFFF', align: AlignmentType.CENTER})], width: {size: dtLvlW, type: WidthType.DXA}, borders, margins: cellMar, shading: {fill: NAVY, type: ShadingType.CLEAR} }));
  }
  dtHeaderCells.push(new TableCell({ children: [p('Notes', {bold: true, size: 16, color: 'FFFFFF'})], width: {size: dtNotesW, type: WidthType.DXA}, borders, margins: cellMar, shading: {fill: NAVY, type: ShadingType.CLEAR} }));

  const dtRows = [new TableRow({ children: dtHeaderCells })];
  dtSteps.forEach((step, i) => {
    const sh = i % 2 === 0 ? 'F4F6F8' : 'FFFFFF';
    const cells = [
      new TableCell({ children: [p(step, {bold: true, size: 16, color: NAVY})], width: {size: dtStepW, type: WidthType.DXA}, borders, margins: cellMar, shading: {fill: sh, type: ShadingType.CLEAR} }),
    ];
    for (const lv of dtLevels) {
      cells.push(new TableCell({ children: [p(lv, {size: 18, color: NAVY, align: AlignmentType.CENTER})], width: {size: dtLvlW, type: WidthType.DXA}, borders, margins: cellMar, shading: {fill: sh, type: ShadingType.CLEAR} }));
    }
    cells.push(new TableCell({ children: [new Paragraph({spacing: {after: 0}})], width: {size: dtNotesW, type: WidthType.DXA}, borders, margins: cellMar, shading: {fill: sh, type: ShadingType.CLEAR} }));
    dtRows.push(new TableRow({ children: cells }));
  });
  children.push(new Table({ rows: dtRows, width: {size: CW, type: WidthType.DXA} }));
  children.push(spacer(80));

  // SECTION 2: Core word tracking
  children.push(p([{text: '2. Core Word Use', bold: true, size: 22, color: NAVY}], {after: 40}));
  children.push(p('Write core words. Mark:  ✓ = used independently  |  M = with model  |  — = not observed  |  ★ = generalized', {size: 14, color: '666666', italics: true, after: 60}));

  const cwCols = 5; const cwColW = Math.floor(CW / cwCols);
  const cwTrackerRows = [];
  for (let r = 0; r < 2; r++) {
    const cells = [];
    for (let c = 0; c < cwCols; c++) {
      cells.push(new TableCell({ children: [
        p('✓  M  —  ★', {size: 12, color: '999999', align: AlignmentType.RIGHT}),
        p('________________', {size: 16, color: 'CCCCCC', align: AlignmentType.CENTER}),
      ], width: {size: cwColW, type: WidthType.DXA}, borders, margins: {top: 40, bottom: 40, left: 40, right: 40} }));
    }
    cwTrackerRows.push(new TableRow({ children: cells }));
  }
  children.push(new Table({ rows: cwTrackerRows, width: {size: CW, type: WidthType.DXA}, columnWidths: Array(cwCols).fill(cwColW) }));
  children.push(spacer(80));

  // SECTION 3: Reading
  children.push(p([{text: '3. Reading & Connected Text', bold: true, size: 22, color: NAVY}], {after: 40}));
  children.push(p([
    {text: 'Decodable passage: ', bold: true, size: 16, color: NAVY},
    {text: '☐ Attempted   ☐ Not attempted   |   Word accuracy: ____ / ____ total   |   Accuracy %: ______', size: 16, color: '444444'},
  ], {after: 40}));
  children.push(p([
    {text: 'Support: ', bold: true, size: 16, color: NAVY},
    {text: '☐ Independent   ☐ Finger tracking   ☐ Partner read-along   ☐ Symbol support   ☐ Re-read needed', size: 16, color: '444444'},
  ], {after: 40}));
  children.push(p([
    {text: 'Behaviors: ', bold: true, size: 16, color: NAVY},
    {text: '☐ Tracked L→R   ☐ Self-corrected   ☐ Blended independently   ☐ Used picture cues', size: 16, color: '444444'},
  ], {after: 60}));

  // SECTION 4: Mastery decision + notes
  children.push(p([{text: '4. Notes & Mastery Decision', bold: true, size: 22, color: NAVY}], {after: 40}));
  // Notes lines
  for (let i = 0; i < 3; i++) {
    children.push(p('________________________________________________________________________________________________________', {size: 14, color: 'DDDDDD', after: 20}));
  }
  children.push(spacer(40));
  children.push(p([
    {text: 'Mastery Decision: ', bold: true, size: 16, color: NAVY},
    {text: '☐ Move to next lesson   ☐ Reteach (same lesson)   ☐ Adjust access method   ☐ Consult with team', size: 16, color: '444444'},
  ]));

  // ════════════════════════════════════════════════════════════
  // FINAL PAGE — attribution & copyright
  // ════════════════════════════════════════════════════════════
  children.push(pageBreak());
  children.push(spacer(600));
  children.push(p([
    {text: 'COMMUNICATE ', bold: true, size: 36, color: TEAL},
    {text: 'BY DESIGN', bold: true, size: 36, color: AMBER},
  ], {align: AlignmentType.CENTER, after: 80}));
  children.push(p('Where AT Meets Practice', {size: 22, color: TEAL, italics: true, align: AlignmentType.CENTER, after: 300}));
  children.push(rule(NAVY, 2));
  children.push(spacer(200));
  children.push(p('Pictographic symbols © Government of Aragón. ARASAAC (arasaac.org). Licensed under CC BY-NC-SA 4.0.', {size: 16, color: '777777', italics: true, after: 80}));
  children.push(p('Use symbols from your student\'s own AAC system first. These open-source symbols are provided as a universal reference when system-specific symbols are not available.', {size: 16, color: '777777', italics: true, after: 80}));
  children.push(p('© Communicate by Design. All rights reserved. communicatebydesign.substack.com', {size: 16, color: '777777', italics: true, after: 80}));
  children.push(p('This product aligns to the UFLI Foundations scope and sequence but is not affiliated with, endorsed by, or produced by UFLI or the University of Florida.', {size: 14, color: '999999', italics: true}));

  // ════════════════════════════════════════════════════════════
  // ASSEMBLE DOCUMENT
  // ════════════════════════════════════════════════════════════
  const doc = new Document({
    title: `UFLI Lesson ${LESSON.number} — Per-Lesson Packet`,
    description: `Communicate by Design — UFLI Lesson ${LESSON.number}: ${LESSON.phoneme}`,
    creator: 'Communicate by Design',
    styles: {
      default: { document: { run: { font: FONT, size: 22 } } },
      paragraphStyles: [
        { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: {size: 36, bold: true, font: FONT, color: NAVY}, paragraph: {spacing: {before: 120, after: 120}, outlineLevel: 0} },
        { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: {size: 28, bold: true, font: FONT, color: NAVY}, paragraph: {spacing: {before: 160, after: 100}, outlineLevel: 1} },
      ],
    },
    sections: [{
      properties: { page: { size: {width: PAGE_W, height: PAGE_H}, margin: {top: MARGIN, bottom: MARGIN, left: MARGIN, right: MARGIN} } },
      headers: { default: new Header({ children: [new Paragraph({ children: [
        new TextRun({text: 'Communicate by Design', font: FONT, size: 16, color: TEAL, italics: true}),
        new TextRun({text: `  |  UFLI Lesson ${LESSON.number}: ${LESSON.phoneme}`, font: FONT, size: 16, color: '999999'}),
      ], border: { bottom: { style: BorderStyle.SINGLE, size: 1, color: 'CCCCCC', space: 4 } }, spacing: { after: 0 } })] }) },
      footers: { default: new Footer({ children: [new Paragraph({ children: [
        new TextRun({text: 'Where AT Meets Practice', font: FONT, size: 14, color: TEAL, italics: true}),
        new TextRun({text: '  |  Page ', font: FONT, size: 14, color: '999999'}),
        new TextRun({children: [PageNumber.CURRENT], font: FONT, size: 14, color: '999999'}),
      ], alignment: AlignmentType.CENTER, border: { top: { style: BorderStyle.SINGLE, size: 1, color: 'CCCCCC', space: 4 } }, spacing: { before: 0 } })] }) },
      children,
    }],
  });

  const paddedNum = String(LESSON.number).padStart(2, '0');
  const filename = `UFLI_Lesson${paddedNum}_${LESSON.grapheme}_Packet.docx`;
  const outputPath = path.join(outputDir, filename);

  const buffer = await Packer.toBuffer(doc);
  fs.writeFileSync(outputPath, buffer);
  console.log(`  ✅ ${filename} (${(buffer.length/1024).toFixed(1)} KB)`);
  return outputPath;
}

// ── CLI ──────────────────────────────────────────────────────
if (require.main === module) {
  const args = process.argv.slice(2);
  const lessonFlag = args.indexOf('--lesson');
  const configFlag = args.indexOf('--config');

  if (lessonFlag !== -1) {
    const lessonNum = parseInt(args[lessonFlag + 1]);
    const configs = require('./ufli_lesson_configs');
    const config = configs.find(c => c.number === lessonNum);
    if (!config) { console.error(`No config found for lesson ${lessonNum}`); process.exit(1); }
    const outDir = path.join(__dirname, 'Output');
    fs.mkdirSync(outDir, { recursive: true });
    buildPacket(config, outDir).catch(e => { console.error('❌', e.message); process.exit(1); });
  } else if (configFlag !== -1) {
    const config = JSON.parse(fs.readFileSync(args[configFlag + 1], 'utf8'));
    const outDir = path.join(__dirname, 'Output');
    fs.mkdirSync(outDir, { recursive: true });
    buildPacket(config, outDir).catch(e => { console.error('❌', e.message); process.exit(1); });
  } else {
    console.log('Usage:');
    console.log('  node build_ufli_packet.js --lesson 1');
    console.log('  node build_ufli_packet.js --config lesson_config.json');
  }
}

module.exports = { buildPacket };

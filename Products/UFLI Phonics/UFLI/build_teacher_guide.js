#!/usr/bin/env node
/**
 * UFLI Teacher Guide + Communication Partner Guide
 * Communicate by Design
 *
 * The "buy once" standalone product. Covers:
 *   SECTION A: Teacher Guide
 *     - Philosophy & design assumptions
 *     - The 4 tools
 *     - The 8 UFLI steps adapted for complex communicators
 *     - Prompting framework (System of Least Prompts + CTD)
 *     - Pacing guidance
 *     - AAC integration
 *     - IEP goal stems
 *   SECTION B: Communication Partner Guide
 *     - Step-by-step para scripts for all 8 UFLI steps
 *     - Quick-reference laminate card (1-page front/back)
 *     - Data collection sheet
 *     - Troubleshooting guide
 *
 * DESIGN ASSUMPTIONS (NEVER VIOLATE):
 *   - Student is a complex communicator, mostly nonspeaking
 *   - Meet the student wherever they are — develop tools alongside literacy instruction
 *   - Words come from UFLI only — we don't add words
 *   - Core/fringe from AAC research (Banajee et al., 2003; Van Tatenhove, 2009)
 *   - No SLP gatekeeping — capacity-building model
 *   - Auditory confirmation loop: produce the PHONEME SOUND
 *   - Pacing flexes, scope doesn't
 *   - SGD is part of robust AAC, not required for phonics
 */

const path = require('path');
const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  WidthType, AlignmentType, BorderStyle, PageBreak, ImageRun,
  ShadingType, HeadingLevel, Header, Footer, PageNumber,
  TableOfContents, LevelFormat,
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
function h3(text) {
  return new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun({ text, font: FONT, size: 24, bold: true, color: TEAL })], spacing: { before: 160, after: 80 } });
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

function infoTable(rows, labelW = 3200) {
  const valW = CW - labelW;
  const tRows = rows.map(([label, value], i) => {
    const shade = i % 2 === 0 ? 'F4F6F8' : 'FFFFFF';
    return new TableRow({ children: [
      new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: label, bold: true, font: FONT, size: 20, color: 'FFFFFF' })], spacing: { after: 0 } })], width: { size: labelW, type: WidthType.DXA }, borders, margins: cellMar, shading: { fill: NAVY, type: ShadingType.CLEAR } }),
      new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: value, font: FONT, size: 20, color: '333333' })], spacing: { after: 0 } })], width: { size: valW, type: WidthType.DXA }, borders, margins: cellMar, shading: { fill: shade, type: ShadingType.CLEAR } }),
    ] });
  });
  return new Table({ rows: tRows, width: { size: CW, type: WidthType.DXA }, columnWidths: [labelW, valW] });
}

// Two-column step table (left = UFLI step, right = complex communicator)
function stepTable(leftContent, rightContent) {
  const leftW = 3200; const rightW = CW - leftW;
  const mkCells = (arr) => arr.map(t => {
    if (typeof t === 'string') return new Paragraph({ children: [new TextRun({ text: t, font: FONT, size: 20, color: '333333' })], spacing: { after: 60 } });
    return new Paragraph({ children: t.map(r => new TextRun({ font: FONT, size: 20, color: '333333', ...r })), spacing: { after: 60 } });
  });
  return new Table({ width: { size: CW, type: WidthType.DXA }, columnWidths: [leftW, rightW], rows: [new TableRow({ children: [
    new TableCell({ children: mkCells(leftContent), width: { size: leftW, type: WidthType.DXA }, borders, margins: cellMar, shading: { fill: 'F4F6F8', type: ShadingType.CLEAR } }),
    new TableCell({ children: mkCells(rightContent), width: { size: rightW, type: WidthType.DXA }, borders, margins: cellMar }),
  ] })] });
}

// ── BUILD ────────────────────────────────────────────────────
async function build() {
  console.log('=== Building UFLI Teacher Guide + Communication Partner Guide ===\n');
  const children = [];

  // ════════════════════════════════════════════════════════════
  // COVER PAGE
  // ════════════════════════════════════════════════════════════
  children.push(spacer(1600));
  children.push(p([
    { text: 'COMMUNICATE ', bold: true, size: 64, color: TEAL },
    { text: 'BY DESIGN', bold: true, size: 64, color: AMBER },
  ], { align: AlignmentType.CENTER, after: 120 }));
  children.push(rule(NAVY, 6));

  // ── ACCESS METHOD COMPATIBILITY STATEMENT (under the name) ──
  children.push(spacer(80));
  children.push(p('ACCESS METHODS SUPPORTED', { bold: true, size: 20, color: NAVY, align: AlignmentType.CENTER, after: 80 }));
  children.push(p([
    { text: 'Direct selection (touch)', size: 18, color: '444444' },
    { text: '  \u2022  ', size: 18, color: TEAL },
    { text: 'Eye gaze', size: 18, color: '444444' },
    { text: '  \u2022  ', size: 18, color: TEAL },
    { text: 'Partner-assisted scanning', size: 18, color: '444444' },
  ], { align: AlignmentType.CENTER, after: 40 }));
  children.push(p([
    { text: 'Switch scanning', size: 18, color: '444444' },
    { text: '  \u2022  ', size: 18, color: TEAL },
    { text: 'Head pointer', size: 18, color: '444444' },
    { text: '  \u2022  ', size: 18, color: TEAL },
    { text: 'Adapted keyboard', size: 18, color: '444444' },
  ], { align: AlignmentType.CENTER, after: 40 }));
  children.push(p([
    { text: 'SGD (any system)', size: 18, color: '444444' },
    { text: '  \u2022  ', size: 18, color: TEAL },
    { text: 'Low-tech AAC (e-trans, symbol cards, PECS)', size: 18, color: '444444' },
    { text: '  \u2022  ', size: 18, color: TEAL },
    { text: 'No-tech (partner voice)', size: 18, color: '444444' },
  ], { align: AlignmentType.CENTER, after: 80 }));
  children.push(rule(NAVY, 6));

  children.push(spacer(200));
  children.push(p('UFLI Foundations', { bold: true, size: 48, align: AlignmentType.CENTER, after: 80 }));
  children.push(p('Teacher Guide + Communication Partner Guide', { size: 28, color: TEAL, align: AlignmentType.CENTER, after: 120 }));
  children.push(p('Complex Communicator Access Layer', { size: 24, color: '555555', align: AlignmentType.CENTER, after: 300 }));

  children.push(p('This guide covers all 8 UFLI lesson steps adapted for complex communicators.', { size: 20, color: '444444', align: AlignmentType.CENTER, after: 80 }));
  children.push(p('Buy once. Use with every per-lesson packet.', { size: 20, color: '444444', align: AlignmentType.CENTER, after: 200 }));

  children.push(p('Where AT Meets Practice', { size: 20, color: TEAL, italics: true, align: AlignmentType.CENTER }));

  // ════════════════════════════════════════════════════════════
  // TABLE OF CONTENTS
  // ════════════════════════════════════════════════════════════
  children.push(pageBreak());
  children.push(h1('Contents'));
  children.push(new TableOfContents('Table of Contents', { hyperlink: true, headingStyleRange: '1-3' }));

  // ════════════════════════════════════════════════════════════
  // SECTION A: TEACHER GUIDE
  // ════════════════════════════════════════════════════════════
  children.push(pageBreak());
  children.push(spacer(1500));
  children.push(p('SECTION A', { bold: true, size: 48, color: TEAL, align: AlignmentType.CENTER, after: 200 }));
  children.push(p('Teacher Guide', { bold: true, size: 40, align: AlignmentType.CENTER, after: 200 }));
  children.push(rule(NAVY, 4));
  children.push(p('For the SPED teacher, co-teacher, or instructional lead', { size: 22, color: '555555', align: AlignmentType.CENTER }));

  // ── HOW TO USE THIS GUIDE ──
  children.push(pageBreak());
  children.push(h1('How to Use This Guide'));
  children.push(p('This guide is the companion to every Communicate by Design UFLI per-lesson packet. The per-lesson packets contain the lesson-specific materials (symbol cards, review words, heart words, morphology notes). This guide contains everything that stays the same across all lessons: the adapted 8-step routine, access options, prompting framework, communication partner scripts, and data collection tools.', { size: 20, color: '333333', after: 200 }));

  children.push(guidanceBox('PRODUCT STRUCTURE', [
    [
      { text: 'This Teacher Guide (buy once): ', bold: true, color: NAVY },
      { text: 'The 8 UFLI steps adapted for complex communicators, communication partner scripts, prompting framework, pacing guidance, data collection sheets, quick-reference laminate card, and troubleshooting guide. Use this with every lesson.' },
    ],
    [
      { text: 'Per-Lesson Packets (one per lesson): ', bold: true, color: NAVY },
      { text: 'Lesson-specific symbol cards with ARASAAC pictograms, review words, heart words, morphology notes, and a reading practice page. These change every lesson.' },
    ],
    'Together, these give a complex communicator full access to UFLI Foundations without requiring a speech generating device.',
  ], TEAL));

  children.push(spacer(200));
  children.push(p('This product does not replace UFLI Foundations. You need the UFLI manual. This product provides the access layer that makes UFLI work for a student who does not speak.', { size: 20, color: '444444', after: 200 }));

  // ── KEY TERMS ──
  children.push(pageBreak());
  children.push(h1('Key Terms'));
  children.push(p('These terms are used throughout this guide. If you are new to AAC or assistive technology, start here.', { size: 20, color: '444444', after: 200 }));
  children.push(infoTable([
    ['AAC', 'Augmentative and Alternative Communication \u2014 any tool, strategy, or system that supplements or replaces speech. Includes low-tech (symbol cards, communication boards) and high-tech (speech generating devices).'],
    ['SGD', 'Speech Generating Device \u2014 a high-tech AAC device that produces spoken output when the user selects symbols, words, or letters. Examples: Tobii Dynavox, TouchChat, LAMP Words for Life. Not required for this product.'],
    ['E-Trans Board', 'Eye Transfer Board \u2014 a clear or opaque frame used to present choices. The communication partner holds up symbol cards in quadrants; the student indicates by gaze, pointing, or other access method.'],
    ['Alternative Pencil', 'Any tool that allows a student to select letters for spelling and writing without a standard pencil. Examples: eye gaze alphabet board, flip alphabet chart, adapted letter tiles, adapted keyboard, SGD keyboard.'],
    ['Communication Partner', 'The person running the UFLI lesson 1:1 with the student. Could be a para, RBT, teacher, parent, tutor, or any trained team member. This is a research-based term from AAC literature (Light, 1988).'],
    ['Core Words', 'High-frequency words that make up approximately 80% of daily communication across all contexts (Banajee et al., 2003). Examples: I, want, go, more, help, it, that. Core words are used by everyone, every day.'],
    ['Fringe Words', 'Topic-specific or lesson-specific vocabulary. Examples: hat, mop, ship. Fringe words are important for the lesson but are not used as frequently across all communication contexts.'],
    ['CTD', 'Constant Time Delay \u2014 a prompting strategy where the communication partner waits a set number of seconds (3, 5, or 7) before providing a model. Builds independence by giving the student time to respond before help is offered.'],
    ['SDI', 'Specially Designed Instruction \u2014 instruction adapted in content, methodology, or delivery to meet the unique needs of a student with a disability. Written into the IEP.'],
    ['ARASAAC', 'Aragonese Portal of Augmentative and Alternative Communication \u2014 a free, open-source library of over 13,000 pictographic symbols used in the per-lesson packets. Licensed under CC BY-NC-SA 4.0.'],
  ]));

  // ── PHILOSOPHY & DESIGN ASSUMPTIONS ──
  children.push(pageBreak());
  children.push(h1('Philosophy and Design Assumptions'));

  children.push(h2('Who This Is For'));
  children.push(p('A complex communicator learning to read. Any age. Any setting. The student is mostly nonspeaking and uses or will use augmentative and alternative communication (AAC). They may already have a robust AAC system, or they may have nothing in place yet. Either way, literacy instruction starts now.', { size: 20, color: '333333', after: 200 }));

  children.push(h2('Start Where the Student Is'));
  children.push(guidanceBox('THIS IS A CAPACITY-BUILDING TOOL', [
    'This product meets the complex communicator wherever they are \u2014 regardless of age, regardless of what systems or tools are currently in place. If the student already has an AAC system, use it. If they do not, this guide helps the team identify what tools are needed and develop them while literacy instruction begins.',
    [
      { text: 'Literacy instruction does not wait for the perfect setup. ', bold: true, color: NAVY },
      { text: 'The team identifies and develops 4 tools alongside instruction: (1) an alternative pencil for encoding, (2) an e-trans board for decoding, (3) symbol cards from the per-lesson packet, and (4) phoneme sound access through partner voice, a phoneme sound device, or an SGD if available.' },
    ],
    [
      { text: 'What about the alternative pencil? ', bold: true, color: NAVY },
      { text: 'Ideally, the student develops their alternative pencil during the free Pre-Alphabet A\u2013Z resource before starting numbered lessons. But do not hold a student out of curriculum waiting for that to happen. If the student has not yet established their access method, download the free Pre-Alphabet A\u2013Z resource and begin developing the alternative pencil alongside these lessons. Access method development and literacy instruction run in parallel \u2014 the student stays in sync with their peers while the team builds the tools they need.' },
    ],
  ], TEAL));

  children.push(pageBreak());
  children.push(h2('Core Beliefs'));

  children.push(p([
    { text: 'The scope does not change. The pace flexes. ', bold: true, color: NAVY, size: 22 },
    { text: 'Complex communicators learn the same phonemes, in the same order, with the same cognitive demand as every other student. The output mode changes. The thinking does not.', size: 20, color: '333333' },
  ], { after: 120 }));

  children.push(p([
    { text: 'The student does not need to speak to learn to read. ', bold: true, color: NAVY, size: 22 },
    { text: 'Research demonstrates that individuals with congenital anarthria (no speech from birth) can perform phonological coding of printed words without ever having produced speech (Foley & Pollatsek, 1999; Bishop, 1985). The internal reading voice develops through hearing sounds, not producing them.', size: 20, color: '333333' },
  ], { after: 120 }));

  children.push(p([
    { text: 'SGD is part of robust AAC, not required for phonics. ', bold: true, color: NAVY, size: 22 },
    { text: 'Every student should be considered for a speech generating device. But for learning to read, the alternative pencil, e-trans board, symbol cards, and phoneme sound access are what teach reading. The SGD supports communication alongside the literacy work.', size: 20, color: '333333' },
  ], { after: 120 }));

  children.push(p([
    { text: 'Wait time is instruction. ', bold: true, color: NAVY, size: 22 },
    { text: '5\u201310 seconds of silence after a prompt is not wasted time. The student is processing, navigating their access method, and formulating a response. Paras who fill silence are stealing learning.', size: 20, color: '333333' },
  ], { after: 120 }));

  children.push(p([
    { text: 'We build the whole team. ', bold: true, color: NAVY, size: 22 },
    { text: 'Teachers, paras, and families can manage vocabulary, add pages, and run phonics instruction. The SLP is part of the team, not the gatekeeper. This is the capacity-building model (RESNA).', size: 20, color: '333333' },
  ], { after: 200 }));

  // ── THE 4 TOOLS ──
  children.push(pageBreak());
  children.push(h1('The 4 Tools'));
  children.push(p('Every lesson, the student uses these four tools. The per-lesson packet provides the symbol cards. If the other three are not yet in place, work with your team to develop them. Literacy instruction and tool development happen at the same time \u2014 you do not wait for one to start the other.', { size: 20, color: '444444', after: 200 }));

  const toolRows = [
    ['Alternative Pencil', 'How the student writes and spells (encoding). Could be an eye gaze alphabet board, flip alphabet chart, adapted letter tiles, adapted keyboard, or SGD keyboard. Ideally developed in the free Pre-Alphabet A\u2013Z resource. If the student does not yet have one, begin developing it alongside these lessons \u2014 do not hold the student out of curriculum.'],
    ['E-Trans Board', 'How the student selects and indicates during decoding tasks. Hold up symbol cards in quadrants. Student gazes at their answer. Also used for yes/no, forced choice, and comprehension. Space cards at least 3 inches apart for reliable gaze discrimination.'],
    ['Symbol Cards', 'Provided in the per-lesson packets. Print, cut, and add to the student\u2019s growing binder. These are the UFLI words for each lesson. New words get symbol cards; review words are pulled from the binder.'],
    ['Phoneme Sounds', 'The student must hear the sound when they select a letter. Three options: (1) Partner voice \u2014 simplest, always available. (2) Hand2Mind Talking Mirror My Sounds Phoneme Set \u2014 44 phoneme sound cards for independent access. (3) SGD with phoneme sounds programmed, if available.'],
  ];
  children.push(infoTable(toolRows));

  children.push(spacer(200));
  children.push(guidanceBox('SGD AND THIS PRODUCT', [
    'An SGD is part of a robust AAC system, and every student should be considered for one. However, for learning phoneme sounds and spelling, the SGD is not what teaches reading. The alternative pencil, e-trans board, symbol cards, and phoneme sound access are what teach reading. The SGD supports communication alongside the literacy work.',
    'If the student has an SGD: use it for communication during instruction. The keyboard can support spelling practice. The device may have phoneme sounds that can be customized. But this product works with or without a device.',
    [
      { text: 'Turn predictive text OFF during phonics instruction. ', bold: true, color: NAVY },
      { text: 'Word prediction short-circuits phonemic processing \u2014 the student learns "type H and HAT appears" instead of blending /h/ /\u00E6/ /t/. Research confirms prediction has no lasting impact on independent spelling skills (ASHA Leader, 2025; EDC/NCIP). Introduce prediction later as a WRITING efficiency tool once the student demonstrates independent decoding and encoding. Prediction is for writing, not reading.' },
    ],
  ], AMBER));

  // ── PHONEME SOUND ACCESS ──
  children.push(pageBreak());
  children.push(h1('Phoneme Sound Access'));
  children.push(p('UFLI is phonics. The student must hear the sounds.', { size: 20, color: '444444', after: 200 }));

  children.push(guidanceBox('THE INTERNAL READING VOICE', [
    'When a speaking student reads, they hear an internal voice sounding out the words. This is the phonological loop \u2014 the brain\u2019s system for holding and rehearsing sounds during reading (Baddeley, 1986). It is the foundation of decoding.',
    'Complex communicators who do not speak still develop this internal phonological representation. Research demonstrates that individuals with congenital anarthria can perform phonological coding of printed words \u2014 including judging whether made-up words "sound" the same \u2014 without ever having produced speech (Foley & Pollatsek, 1999).',
    [
      { text: 'The internal voice develops through hearing sounds, not producing them. ', bold: true, color: NAVY },
      { text: 'External sound access during phonics instruction feeds the student\u2019s phonological loop. Every time the student selects a letter and hears the sound, they are building the internal grapheme-phoneme connection that drives reading.' },
    ],
  ], TEAL));

  children.push(spacer(200));
  children.push(guidanceBox('THREE OPTIONS FOR SOUND ACCESS', [
    [
      { text: '1. Partner voice: ', bold: true, color: NAVY },
      { text: 'The communication partner produces the sound when the student selects a letter. Say the sound whether the selection is correct or not. The student needs to hear what they selected so they can self-correct. Always available.' },
    ],
    [
      { text: '2. Phoneme sound device: ', bold: true, color: NAVY },
      { text: 'A product like the Hand2Mind Talking Mirror My Sounds Phoneme Set provides all 44 phoneme sounds on individual cards. Gives the student independent sound access without relying on a partner.' },
    ],
    [
      { text: '3. SGD (if available): ', bold: true, color: NAVY },
      { text: 'Some SGDs can be customized to include phoneme-level sound buttons. Check with your team on who manages device programming. This is a bonus, not a requirement.' },
    ],
  ], AMBER));

  // ── THE 8 UFLI STEPS ──
  children.push(pageBreak());
  children.push(h1('The 8 UFLI Steps \u2014 Adapted for Complex Communicators'));
  children.push(p('The left column shows the UFLI step and cognitive goal. The right column shows what the complex communicator does. The cognitive work is identical for all students. Only the output mode changes.', { size: 20, color: '444444', after: 100 }));
  children.push(p([
    { text: 'Tools used throughout: ', bold: true, color: NAVY, size: 20 },
    { text: 'alternative pencil (encoding), e-trans board with symbol cards (decoding), phoneme sounds (partner/device).', size: 20, color: '444444' },
  ], { after: 200 }));

  // STEP 1
  children.push(h2('Step 1: Phonemic Awareness'));
  children.push(p('Blending + Segmenting  |  ~2 min', { size: 18, color: '666666', italics: true, after: 120 }));
  children.push(stepTable(
    [
      [{ text: 'COGNITIVE GOAL', bold: true, color: NAVY }],
      'Hear individual phonemes, blend them into a word. Or hear a word, break it into phonemes.',
      [{ text: 'GEN ED', bold: true, color: NAVY }],
      'Teacher says phonemes. Students blend aloud.',
    ],
    [
      [{ text: 'COMPLEX COMMUNICATOR', bold: true, color: TEAL }],
      'Hears the same phonemes. Blends internally. Selects the target word from symbol cards on the e-trans board. For segmenting: indicates the number of sounds or selects phoneme cards in sequence.',
      [{ text: 'ACCESS OPTIONS: ', bold: true, color: NAVY }, { text: 'E-trans board (2\u20134 symbol cards in quadrants, student gazes), direct selection (student touches card), partner-assisted scanning (partner says each option, student signals YES), switch scanning.' }],
      [{ text: 'AUDITORY LOOP: ', bold: true, color: AMBER }, { text: 'When the student selects a word, PRODUCE THE WORD, then segment it back into phonemes. The student hears the blended word AND the individual phonemes confirmed. This closes the loop.' }],
    ]
  ));

  // STEP 2
  children.push(pageBreak());
  children.push(h2('Step 2: Visual Drill'));
  children.push(p('Grapheme to phoneme  |  ~3 min', { size: 18, color: '666666', italics: true, after: 120 }));
  children.push(stepTable(
    [
      [{ text: 'COGNITIVE GOAL', bold: true, color: NAVY }],
      'See a grapheme, retrieve the corresponding phoneme. Automatic recognition.',
      [{ text: 'GEN ED', bold: true, color: NAVY }],
      'Teacher displays grapheme. Students say the sound. Rapid fire.',
    ],
    [
      [{ text: 'COMPLEX COMMUNICATOR', bold: true, color: TEAL }],
      'Sees the same grapheme. Selects the matching phoneme using phoneme sound cards or partner voice.',
      [{ text: 'ACCESS OPTIONS: ', bold: true, color: NAVY }, { text: 'E-trans board (phoneme cards in quadrants), direct selection, partner-assisted scanning (partner says phonemes, student signals YES), phoneme sound device (student presses card to hear independently).' }],
      [{ text: 'AUDITORY LOOP: ', bold: true, color: AMBER }, { text: 'PRODUCE THE SOUND for whatever the student selects \u2014 right or wrong. Say the phoneme, not the letter name. The student needs to hear what they selected to self-correct.' }],
    ]
  ));

  // STEP 3
  children.push(pageBreak());
  children.push(h2('Step 3: Auditory Drill'));
  children.push(p('Phoneme to grapheme (encoding)  |  ~5 min', { size: 18, color: '666666', italics: true, after: 120 }));
  children.push(stepTable(
    [
      [{ text: 'COGNITIVE GOAL', bold: true, color: NAVY }],
      'Hear a phoneme, write the corresponding grapheme. Encoding.',
      [{ text: 'GEN ED', bold: true, color: NAVY }],
      'Teacher says a phoneme. Students write the grapheme on their whiteboard.',
    ],
    [
      [{ text: 'COMPLEX COMMUNICATOR', bold: true, color: TEAL }],
      [{ text: 'This is an ALTERNATIVE PENCIL step. ', bold: true, color: TEAL }, { text: 'The student hears the phoneme and uses their alternative pencil to select the grapheme from the full alphabet. Just like a gen ed student writing on their whiteboard.' }],
      [{ text: 'ACCESS OPTIONS: ', bold: true, color: NAVY }, { text: 'Eye gaze alphabet board, flip alphabet chart, adapted letter tiles, partner-assisted scanning alphabet, SGD keyboard.' }],
      [{ text: 'AUDITORY LOOP: ', bold: true, color: AMBER }, { text: 'When the student selects a letter, PRODUCE THE SOUND that letter makes \u2014 not the letter name. Whether correct or incorrect, the student hears the sound to self-monitor.' }],
    ]
  ));

  // STEP 4
  children.push(pageBreak());
  children.push(h2('Step 4: Blending Drill'));
  children.push(p('Graphemes to word (decoding)  |  ~5 min', { size: 18, color: '666666', italics: true, after: 120 }));
  children.push(stepTable(
    [
      [{ text: 'COGNITIVE GOAL', bold: true, color: NAVY }],
      'See graphemes in sequence, blend into a word, read the word.',
      [{ text: 'GEN ED', bold: true, color: NAVY }],
      'Teacher displays graphemes. Students blend aloud.',
    ],
    [
      [{ text: 'COMPLEX COMMUNICATOR', bold: true, color: TEAL }],
      'Sees the same graphemes. Blends internally. Selects the word from symbol cards on the e-trans board. Use phonetically similar distractors so the student proves they actually blended.',
      [{ text: 'ACCESS OPTIONS: ', bold: true, color: NAVY }, { text: 'E-trans board (symbol cards), direct selection, partner-assisted scanning, switch scanning.' }],
      [{ text: 'AUDITORY LOOP: ', bold: true, color: AMBER }, { text: 'As each grapheme is revealed, PRODUCE THE SOUND. When student selects a word: sound it out phoneme by phoneme, then say the whole word. Confirm by blending AND saying the whole word.' }],
    ]
  ));

  // STEP 5
  children.push(pageBreak());
  children.push(h2('Step 5: New Concept'));
  children.push(p('Explicit instruction + guided practice  |  ~15 min', { size: 18, color: '666666', italics: true, after: 120 }));
  children.push(stepTable(
    [
      [{ text: 'COGNITIVE GOAL', bold: true, color: NAVY }],
      'Learn the new grapheme-phoneme correspondence. Guided decoding and encoding practice.',
      [{ text: 'GEN ED', bold: true, color: NAVY }],
      'Teacher introduces the new phoneme. Students practice reading and spelling words with it.',
    ],
    [
      [{ text: 'COMPLEX COMMUNICATOR', bold: true, color: TEAL }],
      'Highest-support phase. Scaffold heavily.',
      [{ text: 'Introduction: ', bold: true, color: NAVY }, { text: 'Student watches and listens. Communication partner points to the grapheme card and produces the sound. Student explores the grapheme through multi-sensory interaction: tracing a sandpaper letter, forming it in playdough, sketching in sand or on a light box, tracing with a finger or adapted pointer. While exploring the letter form, the student can press the phoneme sound card (e.g., Hand2Mind Talking Mirror set) to hear the sound \u2014 building the grapheme-phoneme connection through touch AND hearing at the same time. The goal is active, multi-channel engagement, not passive viewing.' }],
      [{ text: 'Decoding practice: ', bold: true, color: NAVY }, { text: 'Same as blending drill but with new-concept words only. Start with 2\u20133 symbol cards on the e-trans board. Expand to 4 as the student shows competence.' }],
      [{ text: 'Encoding practice: ', bold: true, color: NAVY }, { text: 'Teacher says a word. Student spells it using their alternative pencil. One letter at a time.' }],
      [{ text: 'AUDITORY LOOP: ', bold: true, color: AMBER }, { text: 'Decoding: confirm by sounding out phoneme by phoneme, then saying the whole word. Encoding: produce the sound for each letter the student selects. After spelling: blend the sounds and say the word.' }],
    ]
  ));

  // STEP 6
  children.push(pageBreak());
  children.push(h2('Step 6: Word Work / Word Chain'));
  children.push(p('Phonemic manipulation  |  ~5 min', { size: 18, color: '666666', italics: true, after: 120 }));
  children.push(stepTable(
    [
      [{ text: 'COGNITIVE GOAL', bold: true, color: NAVY }],
      'Change one phoneme at a time (hat \u2192 hot \u2192 hop). Notice what changed.',
      [{ text: 'GEN ED', bold: true, color: NAVY }],
      'Teacher says the change. Students erase and rewrite.',
    ],
    [
      [{ text: 'COMPLEX COMMUNICATOR', bold: true, color: TEAL }],
      'Identifies what changed. Selects the new word from symbol cards on the e-trans board. Can also use alternative pencil or adapted letter tiles to physically make the letter swap.',
      [{ text: 'ACCESS OPTIONS: ', bold: true, color: NAVY }, { text: 'E-trans board (symbol cards + phoneme cards), adapted letter tiles (Velcro/magnetic for letter swap), alternative pencil (spell the new word), partner-assisted scanning.' }],
      [{ text: 'AUDITORY LOOP: ', bold: true, color: AMBER }, { text: 'When the change is announced, produce BOTH sounds clearly. When student selects the new word: sound it out phoneme by phoneme. The student hears what changed AND hears the new word confirmed.' }],
    ]
  ));

  // STEP 7
  children.push(pageBreak());
  children.push(h2('Step 7: Heart Words'));
  children.push(p('Irregular words  |  ~6 min', { size: 18, color: '666666', italics: true, after: 120 }));
  children.push(stepTable(
    [
      [{ text: 'COGNITIVE GOAL', bold: true, color: NAVY }],
      'Learn words that don\u2019t follow regular rules. Identify the "regular part" and the "heart part."',
      [{ text: 'GEN ED', bold: true, color: NAVY }],
      'Teacher introduces. Students practice reading and spelling.',
    ],
    [
      [{ text: 'COMPLEX COMMUNICATOR', bold: true, color: TEAL }],
      'Selects the heart word from similar-looking options on the e-trans board (visual discrimination). Identifies the "heart part" by indicating which letters are irregular \u2014 communication partner points to each letter group, student signals YES/NO.',
      'Spelling practice: student uses alternative pencil. The irregular part is the challenge \u2014 they have to remember it, just like every other student.',
      [{ text: 'AUDITORY LOOP: ', bold: true, color: AMBER }, { text: 'Heart words have a mismatch between sound and spelling. Make this explicit: sound out each part of the word. Identify the regular part and the heart part. The student needs to HEAR the mismatch to internalize it.' }],
    ]
  ));

  // STEP 8
  children.push(pageBreak());
  children.push(h2('Step 8: Connected Text'));
  children.push(p('Decodable passage  |  ~15 min', { size: 18, color: '666666', italics: true, after: 120 }));
  children.push(stepTable(
    [
      [{ text: 'COGNITIVE GOAL', bold: true, color: NAVY }],
      'Read a passage with previously taught patterns plus the new phoneme. Apply decoding in context.',
      [{ text: 'GEN ED', bold: true, color: NAVY }],
      'Students read the decodable passage aloud.',
    ],
    [
      [{ text: 'COMPLEX COMMUNICATOR', bold: true, color: TEAL }],
      [{ text: 'This is where the symbol cards get used most. ', bold: true, color: NAVY }, { text: 'The student demonstrates they are reading by selecting the correct word.' }],
      [{ text: 'Shared reading: ', bold: true, color: NAVY }, { text: 'Communication partner reads the passage. Target words are highlighted. When a target word appears, the reader PAUSES and the student indicates the word using symbol cards on the e-trans board.' }],
      [{ text: 'Comprehension: ', bold: true, color: NAVY }, { text: 'After reading, ask 2\u20133 questions. Student indicates using symbol cards.' }],
      [{ text: 'AUDITORY LOOP: ', bold: true, color: AMBER }, { text: 'During shared reading, confirm each target word naturally (not phoneme by phoneme \u2014 this is fluency context). For comprehension, confirm responses in full sentences.' }],
      'Do NOT skip this phase. Complex communicators need connected text as much as anyone.',
    ]
  ));

  // ── AIDED LANGUAGE INPUT MAP ──
  children.push(pageBreak());
  children.push(h1('Aided Language Input Map'));
  children.push(p([
    { text: 'When to model on the device during phonics instruction.', bold: true, color: NAVY, size: 22 },
  ], { after: 80 }));
  children.push(p('Aided language input during phonics is almost never done. Teachers model phonics orally but don\u2019t model on the device. This map tells the partner exactly when to touch the device, what to model, and why. Modeling on the device is not prompting \u2014 it is showing the student how their communication system connects to the literacy work.', { size: 20, color: '444444', after: 200 }));

  children.push(infoTable([
    ['Step 1: Phonemic Awareness', 'AFTER the student indicates the blended word, touch that word on the device and say it. "Yes \u2014 ship!" (touch SHIP). This connects the phonemic task to real communication. Do NOT model before the student responds \u2014 that\u2019s prompting, not modeling.'],
    ['Step 2: Visual Drill', 'When the student correctly identifies the phoneme for a grapheme, model a word that starts with that sound on the device. Grapheme "sh" \u2192 touch SHIP or SHE on the device. Quick, 2 seconds. Builds the bridge from isolated sounds to real words on their system.'],
    ['Step 3: Auditory Drill', 'After the student selects the correct grapheme, model the grapheme on the device keyboard (if available) or model a word starting with that sound. This is where you connect encoding to the device keyboard layout \u2014 "S-H, that\u2019s where SH lives on your keyboard."'],
    ['Step 4: Blending Drill', 'BEFORE presenting the choice array, model the target word on the device. "Watch: /sh/ /\u012d/ /p/ \u2014 ship." Touch SHIP. Then present the choices. This is aided language input \u2014 the student sees HOW to find the word before they are asked to demonstrate.'],
    ['Step 5: New Concept', 'During introduction: touch the new grapheme on the device keyboard while producing the sound. During decoding practice: model the target word BEFORE asking the student. During encoding: touch each letter on the device keyboard as the student builds the word on their alternative pencil. Heavy modeling \u2014 this is new learning.'],
    ['Step 6: Word Work', 'When the word chain changes, model BOTH the old word and the new word on the device: "We had HOP (touch HOP). Now it\u2019s HOT (touch HOT). What changed?" Modeling the word pair on the device reinforces the phonemic manipulation.'],
    ['Step 7: Heart Words', 'This is the highest-value modeling step. Touch the heart word on the device and show the student WHERE it lives. "This is THE (touch THE). It\u2019s right here on your main page." Practice navigation: student finds and selects the word independently. Heart words on the device = real communication words.'],
    ['Step 8: Connected Text', 'During shared reading: model key content words on the device as they appear in the text. After reading: model your comprehension question on the device before asking it \u2014 touch WHO, touch IN, touch STORY. Then ask: "Who was in the story?" The student sees the question modeled before they answer.'],
  ]));

  children.push(pageBreak());
  children.push(guidanceBox('MODELING IS NOT PROMPTING', [
    [
      { text: 'Modeling: ', bold: true, color: NAVY },
      { text: 'The adult touches the device to SHOW the student how the communication system connects to the literacy work. The student watches. No response expected.' },
    ],
    [
      { text: 'Prompting: ', bold: true, color: NAVY },
      { text: 'The adult cues the student to make a specific response. A response IS expected.' },
    ],
    'When you model on the device BEFORE asking the student to respond, that is aided language input. When you model on the device AFTER the student fails to respond, that is a prompt. The timing matters.',
    [
      { text: 'General rule: ', bold: true, color: NAVY },
      { text: 'Model first, then ask. Not the other way around. The student sees it done, then does it themselves.' },
    ],
    [
      { text: 'No device? ', bold: true, color: NAVY },
      { text: 'Aided language input still applies. Point to the symbol card, point to the e-trans board option, or point to the alternative pencil letter while saying the sound. Modeling happens on whatever system the student uses.' },
    ],
  ], TEAL));

  // ── PROMPTING FRAMEWORK ──
  children.push(pageBreak());
  children.push(h1('Prompting Framework'));
  children.push(p('System of Least Prompts + Constant Time Delay \u2014 the evidence-based instructional spine running from Pre-Alphabet through independent reading.', { size: 20, color: '444444', after: 200 }));

  children.push(h2('Progression'));
  children.push(infoTable([
    ['Pre-Alphabet', 'Simultaneous prompting (0-second delay). Heavy modeling. Student is learning the access method, not phonemic knowledge.'],
    ['Early UFLI (Lessons 1\u201310)', 'Shift to 0\u21923-second constant time delay. Student has motor access, now building grapheme-phoneme connections. Field size grows: 2-choice \u2192 4-quadrant.'],
    ['Mid UFLI (Lessons 11\u201330)', 'Time delay increases 3\u21925\u21927 seconds. System of least prompts for review skills. CTD still for new phonemes.'],
    ['Later UFLI (30+)', 'Review at independent level. New patterns get CTD. Connected text with decreasing pause time.'],
  ]));

  children.push(spacer(200));
  children.push(guidanceBox('PROMPT DEPENDENCE IS THE #1 BARRIER', [
    'Communication partners who fill silence are stealing learning. Every script in this guide includes specific wait times. If the communication partner gives the answer before the wait time is up, the student learns that waiting works better than thinking.',
    [
      { text: 'The rule: ', bold: true, color: NAVY },
      { text: 'Present the task. Start the timer. Silence. If the student responds correctly: confirm. If the student responds incorrectly: produce the sound/word they selected (auditory loop), then model the correct answer, then present again. If no response after the specified wait time: model, then present again.' },
    ],
    'Never repeat the prompt during the wait time. Never add hints during the wait time. The wait IS the instruction.',
  ], AMBER));

  // ── PACING ──
  children.push(pageBreak());
  children.push(h1('Pacing Guidance'));
  children.push(p('UFLI is designed for daily lessons. A complex communicator may spend 2\u20133 days on a single lesson. That is responsive teaching, not modification.', { size: 20, color: '333333', after: 200 }));

  children.push(h2('When to Move On'));
  children.push(p('The student can identify 3 out of 4 new words independently on the e-trans board (no prompting needed). The student can produce the target grapheme on their alternative pencil when hearing the phoneme. Heart words are recognized on sight at least 2 out of 3 times.', { size: 20, color: '333333', after: 200 }));

  children.push(h2('When to Stay'));
  children.push(p('The student needs more than 2 prompts per word during blending drill. The student cannot find the target grapheme on their alternative pencil after CTD. The student confuses the new phoneme with a recently taught one. Stay, review, re-teach. Mastery over pace.', { size: 20, color: '333333', after: 200 }));

  children.push(h2('Recommended Schedule'));
  children.push(p('Evidence supports approximately 2 hours per day of structured literacy instruction for complex communicators (Erickson & Koppenhaver, 2020). This is Specially Designed Instruction (SDI) \u2014 it should be written into the IEP.', { size: 20, color: '333333', after: 120 }));
  children.push(infoTable([
    ['Daily phonics block', '30\u201345 minutes dedicated to the UFLI lesson. Steps 1\u20138.'],
    ['Additional literacy time', 'Shared reading, independent reading with adapted texts, writing with alternative pencil. Separate from the phonics block.'],
    ['Review cycles', 'Pull symbol cards from the binder. Re-run blending drills with earlier words. Re-read decodable passages. At least 5 minutes per session.'],
    ['Who delivers', '1:1 communication partner under SPED teacher supervision. This could be a para, RBT, co-teacher, parent, or tutor. The communication partner runs the daily routine; the teacher monitors data and adjusts.'],
  ]));

  // ── IEP GOAL STEMS ──
  children.push(pageBreak());
  children.push(h1('IEP Goal Stems'));
  children.push(p('Sample goals for requesting structured literacy support. Adapt to your student and district language.', { size: 20, color: '444444', after: 200 }));

  const goalStems = [
    ['Phoneme-grapheme', 'Given a phoneme sound, [student] will select the corresponding grapheme on their alternative pencil with [X]% accuracy across [Y] consecutive sessions.'],
    ['Decoding (blending)', 'Given graphemes presented in sequence, [student] will select the correct CVC word from a field of [2/4] symbol cards on an e-trans board with [X]% accuracy.'],
    ['Encoding (spelling)', 'Given a spoken CVC word, [student] will spell the word using their alternative pencil, selecting the correct grapheme for each phoneme with [X]% accuracy.'],
    ['Heart words', '[Student] will identify [N] heart words on sight by selecting the correct word from a field of [2/4] options with [X]% accuracy.'],
    ['Connected text', 'During shared reading of decodable text, [student] will indicate [N] target words using symbol cards with [X]% accuracy across [Y] sessions.'],
    ['Phonemic awareness', 'Given 3 phonemes blended orally, [student] will select the corresponding word from a field of [2/4] symbol cards with [X]% accuracy.'],
  ];
  children.push(infoTable(goalStems, 2800));

  // ════════════════════════════════════════════════════════════
  // SECTION B: COMMUNICATION PARTNER GUIDE
  // ════════════════════════════════════════════════════════════
  children.push(pageBreak());
  children.push(spacer(1500));
  children.push(p('SECTION B', { bold: true, size: 48, color: AMBER, align: AlignmentType.CENTER, after: 200 }));
  children.push(p('Communication Partner Guide', { bold: true, size: 40, align: AlignmentType.CENTER, after: 200 }));
  children.push(rule(NAVY, 4));
  children.push(p('For any communication partner running the daily UFLI lesson 1:1', { size: 22, color: '555555', align: AlignmentType.CENTER }));

  // ── PARA SCRIPTS ──
  children.push(pageBreak());
  children.push(h1('Step-by-Step Scripts'));
  children.push(p('Use these scripts during every UFLI lesson. The words change (check the per-lesson packet). The routine stays the same.', { size: 20, color: '444444', after: 200 }));

  // Para Script — Step 1
  children.push(h2('Step 1: Phonemic Awareness'));
  children.push(p('~2 min  |  E-trans board + symbol cards', { size: 18, color: '666666', italics: true, after: 120 }));
  children.push(guidanceBox('WHAT TO DO', [
    'Place 2\u20134 symbol cards on the e-trans board.',
    'After teacher says the phonemes: "Which word do those sounds make? Show me."',
    'WAIT 5\u20137 seconds. Silence.',
    'When student selects: say the word, then segment it back into phonemes.',
    'If no response: model by pointing to the correct card. Say the word. Present again.',
    [{ text: 'Accept any correct indication: ', bold: true, color: NAVY }, { text: 'gaze, touch, switch, card exchange.' }],
  ], TEAL));
  children.push(spacer(80));
  children.push(guidanceBox('WHAT NOT TO DO', [
    'Do not repeat the prompt during the wait time.',
    'Do not say "Look at me" or redirect gaze \u2014 the student may be scanning options.',
    'Do not say the word for the student before they select.',
    'Do not skip this step because the student is "not ready."',
  ], AMBER));

  // Para Script — Steps 2, 3, 4 (short steps — grouped to avoid mostly-empty pages)
  children.push(pageBreak());
  children.push(h2('Step 2: Visual Drill'));
  children.push(p('~3 min  |  Phoneme cards or partner voice', { size: 18, color: '666666', italics: true, after: 120 }));
  children.push(guidanceBox('WHAT TO DO', [
    'Point to grapheme: "What sound?"',
    'Student selects a phoneme.',
    'PRODUCE THE SOUND for whatever they select (right or wrong).',
    'WAIT 3\u20135 seconds.',
    'If correct: move on. If incorrect: say the correct sound, move on.',
    [{ text: 'Do not drill errors during visual drill. ', bold: true, color: NAVY }, { text: 'Keep it moving.' }],
  ], TEAL));

  // Para Script — Step 3
  children.push(spacer(200));
  children.push(h2('Step 3: Auditory Drill'));
  children.push(p('~5 min  |  Alternative pencil', { size: 18, color: '666666', italics: true, after: 120 }));
  children.push(guidanceBox('WHAT TO DO', [
    '"Which letter makes that sound? Show me on your alphabet."',
    'Student uses their alternative pencil.',
    'WAIT 5\u20137 seconds.',
    'When student selects: produce the sound that letter makes (not the letter name).',
    'If correct: confirm. If incorrect: say the correct sound, point to the correct letter on their alphabet.',
  ], TEAL));

  // Para Script — Step 4
  children.push(spacer(200));
  children.push(h2('Step 4: Blending Drill'));
  children.push(p('~5 min  |  E-trans board + symbol cards', { size: 18, color: '666666', italics: true, after: 120 }));
  children.push(guidanceBox('WHAT TO DO', [
    'Place 2\u20134 symbol cards on the e-trans board (include phonetically similar words as distractors).',
    'As teacher reveals each grapheme, produce the sound.',
    'After all shown: "Blend them. What word? Show me."',
    'WAIT 5\u20137 seconds.',
    'When student selects: say each sound, then the whole word.',
    'If incorrect: sound out the correct word phoneme by phoneme. Model. Present again.',
  ], TEAL));

  // Para Script — Step 5
  children.push(pageBreak());
  children.push(h2('Step 5: New Concept'));
  children.push(p('~15 min  |  E-trans board + alternative pencil', { size: 18, color: '666666', italics: true, after: 120 }));
  children.push(guidanceBox('WHAT TO DO', [
    'Set up the grapheme for multi-sensory exploration before the teacher introduces the new concept.',
    [{ text: 'Introduction: ', bold: true, color: NAVY }, { text: 'Point to the grapheme, produce the sound. Let the student explore the letter form: sandpaper letter, playdough, sand tray, light box, finger tracing on textured surface. Place the phoneme sound card nearby \u2014 student presses it to hear the sound while they trace or form the letter. Sound + touch at the same time. Use whatever the student can access.' }],
    [{ text: 'Decoding: ', bold: true, color: NAVY }, { text: 'E-trans board with 2\u20133 symbol cards. "What word? Show me." WAIT 7\u201310 seconds. Sound it out, say the word.' }],
    [{ text: 'Encoding: ', bold: true, color: NAVY }, { text: '"Spell it on your alphabet." Produce the sound for each letter the student selects. After spelling: blend and say the whole word.' }],
    [{ text: 'DO NOT do it for the student. ', bold: true, color: NAVY }, { text: 'If stuck >15 seconds, model ONE letter, then wait.' }],
  ], TEAL));
  children.push(spacer(80));
  children.push(guidanceBox('WHAT NOT TO DO', [
    'Do not hand the student a card and move on. A card to hold is passive. The student needs to interact with the letter form.',
    'Do not assume the student can grip, hold, or manipulate standard materials. Offer options: sandpaper letters, playdough, sand tray, light box, finger tracing on a textured surface, adapted stamp.',
    'Do not skip multi-sensory exploration because of time. This is where the grapheme gets into the student\u2019s body. 2\u20133 minutes of active engagement with the letter form is worth more than 10 minutes of looking at flashcards.',
    'Do not say the letter NAME during this phase. Produce the SOUND every time the student traces or forms the letter. If the student has a phoneme sound card, let them press it themselves \u2014 that\u2019s independent sound access.',
  ], AMBER));

  // Para Script — Step 6
  children.push(pageBreak());
  children.push(h2('Step 6: Word Work / Word Chain'));
  children.push(p('~5 min  |  E-trans board + letter tiles (optional)', { size: 18, color: '666666', italics: true, after: 120 }));
  children.push(guidanceBox('WHAT TO DO', [
    'Display the word chain visually.',
    'When teacher says the change: produce both sounds \u2014 "Taking out [old sound], putting in [new sound]."',
    '"What sound changes? Show me." Then: "What\u2019s the new word? Show me."',
    'WAIT 5\u20137 seconds.',
    'When student selects: sound out the new word.',
    'If student needs more than 2 attempts, move on and circle back.',
  ], TEAL));

  // Para Script — Step 7 (grouped with Step 6 — both short)
  children.push(spacer(200));
  children.push(h2('Step 7: Heart Words'));
  children.push(p('~6 min  |  E-trans board + alternative pencil', { size: 18, color: '666666', italics: true, after: 120 }));
  children.push(guidanceBox('WHAT TO DO', [
    'Show the heart word card. Say the word, then sound it out letter by letter.',
    'Identify the regular and heart parts aloud.',
    '"What word is this?" Student indicates.',
    'Point to each letter group: "Regular or heart part?" Produce the sound for each part.',
    'WAIT 5 seconds per response.',
    'Practice spelling with alternative pencil. Practice 3 times during the lesson.',
  ], TEAL));

  // Para Script — Step 8
  children.push(pageBreak());
  children.push(h2('Step 8: Connected Text'));
  children.push(p('~15 min  |  E-trans board + symbol cards + decodable passage', { size: 18, color: '666666', italics: true, after: 120 }));
  children.push(guidanceBox('WHAT TO DO', [
    [{ text: 'BEFORE reading: ', bold: true, color: NAVY }, { text: 'Preview 3\u20135 target words with the student. Sound out each one. "You\u2019re going to help me read these words." Place target symbol cards on the e-trans board.' }],
    [{ text: 'DURING reading: ', bold: true, color: NAVY }, { text: 'Slow pace. PAUSE before each target word. WAIT 5\u201310 seconds. When student indicates: read the word naturally (not phoneme by phoneme \u2014 this is fluency context).' }],
    [{ text: 'AFTER reading: ', bold: true, color: NAVY }, { text: 'Comprehension questions using symbol cards. Confirm responses in full sentences. If time: reread with more target words.' }],
    'Do NOT skip this phase.',
  ], TEAL));

  // ── QUICK-REFERENCE LAMINATE CARD ──
  children.push(pageBreak());
  children.push(h1('Quick-Reference Card'));
  children.push(p('Print this page and laminate it. Keep it with the e-trans board.', { size: 20, color: '444444', italics: true, after: 200 }));

  // Front side
  children.push(guidanceBox('THE 4 TOOLS', [
    [{ text: '1. Alternative Pencil ', bold: true, color: NAVY }, { text: '\u2014 for spelling and writing (encoding)' }],
    [{ text: '2. E-Trans Board ', bold: true, color: NAVY }, { text: '\u2014 for selecting and indicating (decoding)' }],
    [{ text: '3. Symbol Cards ', bold: true, color: NAVY }, { text: '\u2014 print from per-lesson packet, add to binder' }],
    [{ text: '4. Phoneme Sounds ', bold: true, color: NAVY }, { text: '\u2014 partner voice, phoneme cards, or SGD' }],
  ], TEAL));
  children.push(spacer(120));

  children.push(guidanceBox('AUDITORY CONFIRMATION LOOP', [
    [{ text: 'Student selects something \u2192 YOU PRODUCE THE SOUND.', bold: true, color: NAVY }],
    'Right or wrong. Always. Immediately.',
    'Decoding (e-trans): say the word, then sound it out.',
    'Encoding (alt pencil): say the sound that letter makes.',
    'Heart words: say the word, identify regular vs. heart parts.',
    'Connected text: say the word naturally (fluency context).',
  ], AMBER));
  children.push(spacer(120));

  children.push(guidanceBox('WAIT TIME', [
    [{ text: 'Steps 1\u20134: ', bold: true, color: NAVY }, { text: '5\u20137 seconds' }],
    [{ text: 'Step 5 (New Concept): ', bold: true, color: NAVY }, { text: '7\u201310 seconds' }],
    [{ text: 'Step 8 (Connected Text): ', bold: true, color: NAVY }, { text: '5\u201310 seconds' }],
    [{ text: 'Silence during wait time. ', bold: true, color: NAVY }, { text: 'No hints. No redirections. No repeated prompts. The wait IS the instruction.' }],
  ], TEAL));
  children.push(spacer(120));

  children.push(guidanceBox('WHAT NOT TO DO', [
    'Do not say the answer before the wait time is up.',
    'Do not say "look at me" \u2014 the student may be scanning.',
    'Do not add extra words to the UFLI lesson.',
    'Do not skip connected text (Step 8).',
    'Do not turn off prediction \u2014 it should already be off during phonics.',
  ], AMBER));

  // ── DATA COLLECTION SHEET ──
  children.push(pageBreak());
  children.push(h1('Data Collection Sheet'));
  children.push(p('Copy this page for each lesson. Track tools in use and prompt level per step. Use this to monitor progress and inform pacing decisions.', { size: 20, color: '444444', after: 120 }));

  // ── LESSON INFO + TOOLS IN USE ──
  children.push(p('Lesson #: ________    Phoneme: ________    Grapheme: ________    Date started: ________', { size: 18, color: '666666', after: 120 }));
  children.push(p([
    { text: 'Tools in Use', bold: true, color: NAVY, size: 22 },
    { text: '  (circle or write in what the student is using this lesson)', size: 16, color: '666666', italics: true },
  ], { after: 60 }));

  const toolsLabelW = 3200;
  const toolsFillW = CW - toolsLabelW;
  const toolItems = [
    ['Alternative Pencil:', 'eye gaze alphabet board  /  flip chart  /  adapted tiles  /  partner-assisted scanning  /  SGD keyboard  /  other: ________'],
    ['Decoding Tool:', 'e-trans board  /  symbol cards  /  SGD  /  other: ________'],
    ['Sound Access:', 'partner voice  /  Talking Mirror set  /  SGD phoneme page  /  other: ________'],
    ['Field Size:', '2-choice  /  4-quadrant  /  6–8 field  /  other: ________'],
  ];
  const tiuRows = toolItems.map((item, i) => {
    const shade = i % 2 === 0 ? 'F4F6F8' : 'FFFFFF';
    return new TableRow({ children: [
      new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: item[0], bold: true, font: FONT, size: 18, color: NAVY })], spacing: { after: 0 } })], width: { size: toolsLabelW, type: WidthType.DXA }, borders, margins: cellMar, shading: { fill: shade, type: ShadingType.CLEAR } }),
      new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: item[1], font: FONT, size: 16, color: '666666', italics: true })], spacing: { after: 0 } })], width: { size: toolsFillW, type: WidthType.DXA }, borders, margins: cellMar, shading: { fill: shade, type: ShadingType.CLEAR } }),
    ] });
  });
  children.push(new Table({ rows: tiuRows, width: { size: CW, type: WidthType.DXA }, columnWidths: [toolsLabelW, toolsFillW] }));

  children.push(spacer(200));
  children.push(p([
    { text: 'Prompt levels: ', bold: true, color: NAVY, size: 20 },
    { text: 'I = Independent  |  CTD-3 = Correct after 3-second delay  |  CTD-5 = Correct after 5-second delay  |  M = Needed model  |  NR = No response  |  N/A = Not introduced', size: 18, color: '444444' },
  ], { after: 200 }));

  // Data collection table
  const dcLabelW = 3000;
  const dcDataW = Math.floor((CW - dcLabelW) / 3);
  const dcHeader = new TableRow({ children: [
    new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: 'UFLI Step', bold: true, font: FONT, size: 18, color: 'FFFFFF' })], spacing: { after: 0 } })], width: { size: dcLabelW, type: WidthType.DXA }, borders, margins: cellMar, shading: { fill: NAVY, type: ShadingType.CLEAR } }),
    new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: 'Day 1', bold: true, font: FONT, size: 18, color: 'FFFFFF' })], spacing: { after: 0 }, alignment: AlignmentType.CENTER })], width: { size: dcDataW, type: WidthType.DXA }, borders, margins: cellMar, shading: { fill: NAVY, type: ShadingType.CLEAR } }),
    new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: 'Day 2', bold: true, font: FONT, size: 18, color: 'FFFFFF' })], spacing: { after: 0 }, alignment: AlignmentType.CENTER })], width: { size: dcDataW, type: WidthType.DXA }, borders, margins: cellMar, shading: { fill: NAVY, type: ShadingType.CLEAR } }),
    new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: 'Day 3', bold: true, font: FONT, size: 18, color: 'FFFFFF' })], spacing: { after: 0 }, alignment: AlignmentType.CENTER })], width: { size: dcDataW, type: WidthType.DXA }, borders, margins: cellMar, shading: { fill: NAVY, type: ShadingType.CLEAR } }),
  ] });

  const dcSteps = [
    '1. Phonemic Awareness',
    '2. Visual Drill',
    '3. Auditory Drill',
    '4. Blending Drill',
    '5. New Concept \u2014 Decoding',
    '5. New Concept \u2014 Encoding',
    '6. Word Chain',
    '7. Heart Words \u2014 Recognition',
    '7. Heart Words \u2014 Spelling',
    '8. Connected Text \u2014 Word ID',
    '8. Connected Text \u2014 Comprehension',
  ];

  const dcRows = [dcHeader];
  dcSteps.forEach((step, i) => {
    const shade = i % 2 === 0 ? 'F4F6F8' : 'FFFFFF';
    dcRows.push(new TableRow({ children: [
      new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: step, font: FONT, size: 18, color: NAVY })], spacing: { after: 0 } })], width: { size: dcLabelW, type: WidthType.DXA }, borders, margins: cellMar, shading: { fill: shade, type: ShadingType.CLEAR } }),
      new TableCell({ children: [new Paragraph({ spacing: { after: 0 } })], width: { size: dcDataW, type: WidthType.DXA }, borders, margins: { top: 200, bottom: 200, left: 120, right: 120 }, shading: { fill: shade, type: ShadingType.CLEAR } }),
      new TableCell({ children: [new Paragraph({ spacing: { after: 0 } })], width: { size: dcDataW, type: WidthType.DXA }, borders, margins: { top: 200, bottom: 200, left: 120, right: 120 }, shading: { fill: shade, type: ShadingType.CLEAR } }),
      new TableCell({ children: [new Paragraph({ spacing: { after: 0 } })], width: { size: dcDataW, type: WidthType.DXA }, borders, margins: { top: 200, bottom: 200, left: 120, right: 120 }, shading: { fill: shade, type: ShadingType.CLEAR } }),
    ] }));
  });

  children.push(new Table({ rows: dcRows, width: { size: CW, type: WidthType.DXA }, columnWidths: [dcLabelW, dcDataW, dcDataW, dcDataW] }));

  children.push(spacer(200));
  children.push(p('Notes: ________________________________________________________________________________', { size: 18, color: '666666' }));

  // ── WORDS TO ADD TO THE DEVICE ──
  children.push(pageBreak());
  children.push(h1('Words to Add to the Device'));
  children.push(p([
    { text: 'A team planning tool. ', bold: true, color: NAVY, size: 22 },
    { text: 'Before the next unit starts, review the word list from the per-lesson packets. Identify words that need to be added to the student\u2019s device. Send this sheet to whoever adds words on your team.', size: 20, color: '444444' },
  ], { after: 120 }));
  children.push(p('Student: ________________    Device/System: ________________', { size: 18, color: '666666', after: 40 }));
  children.push(p('Lessons covered: ________    Assigned to: ________________    Due by: ________', { size: 18, color: '666666', after: 120 }));

  // Simple, clean 3-column table: Word, Where to put it, Done
  const waWordW = 2400;
  const waWhereW = CW - waWordW - 1200;
  const waDoneW = 1200;

  const waHeaderRow = new TableRow({ children: [
    new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: 'Word to Add', bold: true, font: FONT, size: 20, color: 'FFFFFF' })], spacing: { after: 0 } })], width: { size: waWordW, type: WidthType.DXA }, borders, margins: cellMar, shading: { fill: NAVY, type: ShadingType.CLEAR } }),
    new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: 'Where on the Device', bold: true, font: FONT, size: 20, color: 'FFFFFF' })], spacing: { after: 0 } })], width: { size: waWhereW, type: WidthType.DXA }, borders, margins: cellMar, shading: { fill: NAVY, type: ShadingType.CLEAR } }),
    new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: 'Done', bold: true, font: FONT, size: 20, color: 'FFFFFF' })], spacing: { after: 0 }, alignment: AlignmentType.CENTER })], width: { size: waDoneW, type: WidthType.DXA }, borders, margins: cellMar, shading: { fill: NAVY, type: ShadingType.CLEAR } }),
  ] });

  const waTableRows = [waHeaderRow];
  for (let r = 0; r < 10; r++) {
    const shade = r % 2 === 0 ? 'F4F6F8' : 'FFFFFF';
    waTableRows.push(new TableRow({ children: [
      new TableCell({ children: [new Paragraph({ spacing: { after: 0 } })], width: { size: waWordW, type: WidthType.DXA }, borders, margins: { top: 160, bottom: 160, left: 100, right: 100 }, shading: { fill: shade, type: ShadingType.CLEAR } }),
      new TableCell({ children: [new Paragraph({ spacing: { after: 0 } })], width: { size: waWhereW, type: WidthType.DXA }, borders, margins: { top: 160, bottom: 160, left: 100, right: 100 }, shading: { fill: shade, type: ShadingType.CLEAR } }),
      new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: '\u2610', font: FONT, size: 22, color: '999999' })], spacing: { after: 0 }, alignment: AlignmentType.CENTER })], width: { size: waDoneW, type: WidthType.DXA }, borders, margins: cellMar, shading: { fill: shade, type: ShadingType.CLEAR } }),
    ] }));
  }

  children.push(new Table({ rows: waTableRows, width: { size: CW, type: WidthType.DXA }, columnWidths: [waWordW, waWhereW, waDoneW] }));

  children.push(spacer(200));
  children.push(guidanceBox('WHO ADDS WORDS?', [
    'Anyone on the team: the student, the communication partner, the teacher, a family member, or the SLP. The team decides who handles device programming for this student.',
    [
      { text: 'Does this word need to go on the device? ', bold: true, color: NAVY },
      { text: 'Core words and heart words \u2192 yes. Fringe words \u2192 team decision. If the student will use the word beyond phonics, add it. If not, the symbol card from the packet is enough.' },
    ],
    'When a word needs to be added, it gets added. This sheet is the action plan. Confirm everything is done before instruction starts.',
    [
      { text: 'No SGD? ', bold: true, color: NAVY },
      { text: 'Skip this page. The lessons work with alternative pencils, e-trans boards, and symbol cards without a device.' },
    ],
  ], TEAL));

  // ── TROUBLESHOOTING GUIDE ──
  children.push(pageBreak());
  children.push(h1('Troubleshooting Guide'));
  children.push(p('Common scenarios and what to do about them.', { size: 20, color: '444444', after: 200 }));

  const troubleRows = [
    ['Student is not responding', 'Check positioning first \u2014 can the student see the cards? Are cards within gaze/reach range? Reduce the field size to 2. Use simultaneous prompting (model, then present). If still no response: take a break, try again in 5 minutes. Document and discuss with the teacher.'],
    ['Student seems to guess randomly', 'Reduce to 2 choices (target + 1 distractor). Make the distractor very different from the target. If the student gets 50/50, they are guessing. Go back to simultaneous prompting for this phoneme. Check that the student understands the e-trans board itself \u2014 do they know gaze/point = selection?'],
    ['Student is prompt dependent', 'The student waits for you to give the answer. Increase wait time. Do not model until the wait time is fully elapsed. Use constant time delay \u2014 start at 0 seconds (simultaneous), then increase to 3, 5, 7. If the student looks at you expectantly: look at the cards, not back at the student.'],
    ['Student gets frustrated', 'Switch to a review task they can do independently. Success builds motivation. Then return to the new concept with more scaffolding (2-choice, simultaneous prompting). Never force through frustration \u2014 but also don\u2019t avoid the task permanently. Come back to it.'],
    ['Student is fatigued', 'Shorten the session. Prioritize Steps 3 (auditory drill) and 5 (new concept) \u2014 these have the highest instructional value. Steps 1 and 2 can be brief. Connected text can wait for the next session if needed.'],
    ['Pacing feels too slow', 'That\u2019s okay. Mastery over pace. A complex communicator may spend 2\u20133 days on one lesson. Review the data sheet: if prompt levels are improving, the student is learning. If prompt levels are flat across 3+ days, discuss with the teacher \u2014 the student may need the access method reassessed.'],
    ['Communication partner and teacher disagree on readiness', 'The data decides. If the student is at Independent or CTD-3 for 3 out of 4 new words across 2 days, they are ready to move on. If not, they stay. The data collection sheet removes opinion from the decision.'],
  ];

  troubleRows.forEach(([scenario, response], i) => {
    if (i === 4) children.push(pageBreak()); // keep sections to ~1 page
    children.push(h3(scenario));
    children.push(p(response, { size: 20, color: '333333', after: 120 }));
  });

  // ── RESEARCH BASE ──
  children.push(pageBreak());
  children.push(h1('References'));
  children.push(p('Key citations supporting the instructional design of this product.', { size: 20, color: '444444', after: 200 }));

  const citations = [
    ['Foley & Pollatsek (1999)', 'Phonological processing and reading abilities in adolescents and adults with severe congenital speech impairments. AAC, 15(3). All participants demonstrated phonological coding of printed text without intelligible speech.'],
    ['Bishop (1985)', 'Spelling ability in congenital dysarthria. Cognitive Neuropsychology, 2, 229\u2013251. Children who cannot articulate speech can develop phonological representations sufficient for spelling.'],
    ['Erickson & Koppenhaver (2020)', 'Comprehensive Literacy for All. Brookes Publishing. Literacy instruction for students with significant disabilities should follow the same evidence base as general education.'],
    ['Vandervelden & Siegel (1999)', 'Phonological processing and literacy in AAC users. AAC, 15(3). Phonological recoding and awareness exist in individuals who use AAC, even those with no speech.'],
    ['Hudler, Hurlburt & Brock (2025)', 'System of least prompts and constant time delay research for AAC users in structured literacy.'],
    ['Banajee, Dicarlo & Stricklin (2003)', 'Core vocabulary determination for toddlers. AAC, 19(2). Established the concept of high-frequency core words comprising ~80% of daily communication.'],
    ['Van Tatenhove (2009)', 'Normal language development, generative language, and AAC. Perspectives on AAC. Core/fringe framework for vocabulary organization in AAC systems.'],
  ];

  for (const [cite, desc] of citations) {
    children.push(p([
      { text: cite + ': ', bold: true, color: NAVY, size: 20 },
      { text: desc, size: 18, color: '444444' },
    ], { after: 120 }));
  }

  // ── FINAL PAGE ──
  children.push(pageBreak());
  children.push(spacer(600));
  children.push(p([
    { text: 'COMMUNICATE ', bold: true, size: 36, color: TEAL },
    { text: 'BY DESIGN', bold: true, size: 36, color: AMBER },
  ], { align: AlignmentType.CENTER, after: 80 }));
  children.push(p('Where AT Meets Practice', { size: 22, color: TEAL, italics: true, align: AlignmentType.CENTER, after: 300 }));
  children.push(rule(NAVY, 2));
  children.push(spacer(200));
  children.push(p('Pictographic symbols \u00A9 Government of Arag\u00F3n. ARASAAC (arasaac.org). Licensed under CC BY-NC-SA 4.0.', { size: 16, color: '777777', italics: true, after: 80 }));
  children.push(p('Use symbols from your student\u2019s own AAC system first. These open-source symbols are provided as a universal reference when system-specific symbols are not available.', { size: 16, color: '777777', italics: true, after: 80 }));
  children.push(p('\u00A9 Communicate by Design. All rights reserved. communicatebydesign.substack.com', { size: 16, color: '777777', italics: true, after: 80 }));
  children.push(p('This product aligns to the UFLI Foundations scope and sequence but is not affiliated with, endorsed by, or produced by UFLI or the University of Florida.', { size: 14, color: '999999', italics: true }));

  // ════════════════════════════════════════════════════════════
  // ASSEMBLE DOCUMENT
  // ════════════════════════════════════════════════════════════
  const doc = new Document({
    title: 'UFLI Teacher Guide + Communication Partner Guide',
    description: 'Communicate by Design \u2014 UFLI Foundations: Teacher Guide + Communication Partner Guide',
    creator: 'Communicate by Design',
    styles: {
      default: { document: { run: { font: FONT, size: 22 } } },
      paragraphStyles: [
        { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { size: 36, bold: true, font: FONT, color: NAVY }, paragraph: { spacing: { before: 120, after: 120 }, outlineLevel: 0 } },
        { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { size: 28, bold: true, font: FONT, color: NAVY }, paragraph: { spacing: { before: 160, after: 100 }, outlineLevel: 1 } },
        { id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { size: 24, bold: true, font: FONT, color: TEAL }, paragraph: { spacing: { before: 140, after: 80 }, outlineLevel: 2 } },
      ],
    },
    sections: [{
      properties: { page: { size: { width: PAGE_W, height: PAGE_H }, margin: { top: MARGIN, bottom: MARGIN, left: MARGIN, right: MARGIN } } },
      headers: { default: new Header({ children: [new Paragraph({ children: [
        new TextRun({ text: 'Communicate by Design', font: FONT, size: 16, color: TEAL, italics: true }),
        new TextRun({ text: '  |  UFLI Teacher Guide + Communication Partner Guide', font: FONT, size: 16, color: '999999' }),
      ], border: { bottom: { style: BorderStyle.SINGLE, size: 1, color: 'CCCCCC', space: 4 } }, spacing: { after: 0 } })] }) },
      footers: { default: new Footer({ children: [new Paragraph({ children: [
        new TextRun({ text: 'Where AT Meets Practice', font: FONT, size: 14, color: TEAL, italics: true }),
        new TextRun({ text: '  |  Page ', font: FONT, size: 14, color: '999999' }),
        new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 14, color: '999999' }),
      ], alignment: AlignmentType.CENTER, border: { top: { style: BorderStyle.SINGLE, size: 1, color: 'CCCCCC', space: 4 } }, spacing: { before: 0 } })] }) },
      children,
    }],
  });

  const outputDir = path.join(__dirname, 'Output');
  fs.mkdirSync(outputDir, { recursive: true });
  const outputPath = path.join(outputDir, 'UFLI_Teacher_Guide_and_Communication_Partner_Guide.docx');
  const buffer = await Packer.toBuffer(doc);
  fs.writeFileSync(outputPath, buffer);
  console.log(`\u2705 ${path.basename(outputPath)} (${(buffer.length / 1024).toFixed(1)} KB)`);
  return outputPath;
}

// ── CLI ──────────────────────────────────────────────────────
build().catch(e => { console.error('\u274C', e.message); process.exit(1); });

/**
 * rebuild_vocab_explorer.js — Communicate by Design
 * ===================================================
 * Regenerates the embedded VOCAB dataset inside cbd-vocabulary-explorer.html
 * from the authoritative source files.
 *
 * RUN AFTER:
 *   - Editing cbd_unit_vocab.js (any word change, new unit added)
 *   - Editing ufli_lesson_configs.js
 *   - Adding a new product line to the explorer
 *
 * USAGE:
 *   node _Operations/rebuild_vocab_explorer.js
 *
 * OUTPUT:
 *   Overwrites Products/UFLI Phonics/cbd-vocabulary-explorer.html in-place.
 *   Prints a summary of what changed.
 */

'use strict';

const path = require('path');
const fs   = require('fs');

const OPS       = path.join(__dirname);
const HTML_PATH = path.join(__dirname, '..', 'Products', 'UFLI Phonics', 'cbd-vocabulary-explorer.html');
const UFLI_PATH = path.join(__dirname, '..', 'Products', 'UFLI Phonics', 'UFLI', 'ufli_lesson_configs.js');

const nonfictionUnits           = require(path.join(OPS, 'cbd_unit_vocab.js'));
const ufliLessons               = require(UFLI_PATH);
const { getFitzgeraldCategory } = require(path.join(OPS, 'fitzgerald_key.js'));

// ── Unit title → short key used in PRODUCTS and nu[] arrays ──────────────────
const UNIT_KEY = {
  'Radium Girls'                           : 'Radium Girls',
  "Keiko: A Whale's Journey"               : 'Keiko',
  'Frances Kelsey and the Thalidomide Crisis': 'Frances Kelsey',
  '504 Sit-In 1977'                        : '504 Sit-In',
  'Capitol Crawl 1990'                     : 'Capitol Crawl',
  'Zitkala-Ša'                             : 'Zitkala-Ša',
  'Wonder: Character Analysis'             : 'Wonder',
};

// Is this unit a fiction unit (not shown in nonfiction filter)?
const FICTION_UNITS = new Set(['Wonder']);

// ── Build master VOCAB array ──────────────────────────────────────────────────

function buildVocab() {
  const map = new Map(); // lowercase word → entry

  function entry(word) {
    const key = word.toLowerCase();
    if (!map.has(key)) {
      const fitz = getFitzgeraldCategory(key);
      map.set(key, {
        w   : key,
        t   : null,       // C / F / H / CU
        f   : fitz.category,
        fl  : fitz.label,
        ul  : [],         // UFLI lesson numbers
        nu  : [],         // nonfiction unit short keys
        pl  : new Set(),  // product line strings
        p5  : false,
      });
    }
    return map.get(key);
  }

  // 1. Nonfiction + fiction units (all in cbd_unit_vocab.js)
  for (const unit of nonfictionUnits) {
    const shortKey = UNIT_KEY[unit.unitTitle] || unit.unitTitle;
    const isFiction = FICTION_UNITS.has(shortKey);
    const productLine = isFiction ? 'Fiction Anchor Texts' : 'Nonfiction Reading Units';

    for (const w of unit.newWords) {
      const e = entry(w.word);
      if (!e.t || (e.t === 'C' && w.type === 'fringe')) e.t = w.type === 'core' ? 'C' : 'F';
      if (!e.nu.includes(shortKey)) e.nu.push(shortKey); // includes fiction units
      e.pl.add(productLine);
      if (w.top5) e.p5 = true;
    }
  }

  // 2. UFLI lessons
  for (const lesson of ufliLessons) {
    for (const w of (lesson.newWords || [])) {
      const e = entry(w.word);
      if (!e.t) e.t = w.type === 'core' ? 'C' : 'F';
      if (!e.ul.includes(lesson.number)) e.ul.push(lesson.number);
      e.pl.add('UFLI Phonics');
    }
    for (const hw of (lesson.heartWords || [])) {
      const wordStr = typeof hw === 'string' ? hw : hw.word;
      if (!wordStr) continue;
      const e = entry(wordStr);
      e.t = 'H';
      if (!e.ul.includes(lesson.number)) e.ul.push(lesson.number);
      e.pl.add('UFLI Phonics');
    }
  }

  // 3. Post-process
  const vocab = [];
  for (const [, e] of map) {
    e.ul.sort((a, b) => a - b);
    e.nu.sort();
    e.pl = [...e.pl].sort();
    if (!e.t) e.t = 'F';

    // Upgrade to CU if appears in both UFLI and a nonfiction/fiction line
    if (e.t === 'C' && e.pl.includes('UFLI Phonics') && e.pl.some(p => p !== 'UFLI Phonics')) {
      e.t = 'CU';
    }

    vocab.push({
      w  : e.w,
      t  : e.t,
      f  : e.f,
      fl : e.fl,
      ul : e.ul,
      nu : e.nu,
      pl : e.pl,
      // Count individual products: one card per nonfiction/fiction unit + 1 if in UFLI
      pc : e.nu.length + (e.ul.length > 0 ? 1 : 0),
      p5 : e.p5,
    });
  }

  vocab.sort((a, b) => a.w.localeCompare(b.w));
  return vocab;
}

// ── Stats ─────────────────────────────────────────────────────────────────────

function stats(vocab) {
  const core   = vocab.filter(v => v.t === 'C' || v.t === 'CU').length;
  const fringe = vocab.filter(v => v.t === 'F').length;
  const units  = new Set(vocab.flatMap(v => v.nu)).size;
  const ufli   = new Set(vocab.flatMap(v => v.ul)).size;
  return { total: vocab.length, core, fringe, units, ufli };
}

// ── PRODUCTS block to inject (includes Wonder) ───────────────────────────────

const PRODUCTS_BLOCK = `const PRODUCTS = {
  'UFLI Phonics': {
    label: 'UFLI Phonics Lesson Packets (Lessons 5–34)',
    icon: '🔤',
    productLine: 'UFLI Supplemental',
    status: 'In Production',
    estimatedDate: 'May 2026',
    desc: '30 adapted lesson packets with AAC access layers, auditory confirmation loop, and Communication Access one-sheets.',
    cardClass: '',
  },
  'Keiko': {
    label: 'Keiko: A Whale\\'s Journey',
    icon: '🐋',
    productLine: 'Nonfiction',
    status: 'Live',
    platforms: [{ name: 'TPT', url: 'https://www.teacherspayteachers.com/store/communicate-by-design' }],
    desc: 'Grades 6–10 | RI standards | V1–V3 Lexile | Skill #1: Close Reading & Annotation',
    cardClass: 'nonfiction',
  },
  'Radium Girls': {
    label: 'Radium Girls: Labor, Science & Justice',
    icon: '⚗️',
    productLine: 'Nonfiction',
    status: 'Live',
    platforms: [{ name: 'TPT', url: 'https://www.teacherspayteachers.com/store/communicate-by-design' }],
    desc: 'Grades 6–10 | RI standards | V1–V3 Lexile | Skill #1: Close Reading & Annotation',
    cardClass: 'nonfiction',
  },
  'Frances Kelsey': {
    label: 'Frances Kelsey: Science, Evidence & Power',
    icon: '🔬',
    productLine: 'Nonfiction',
    status: 'Live',
    platforms: [{ name: 'TPT', url: 'https://www.teacherspayteachers.com/store/communicate-by-design' }],
    desc: 'Grades 6–10 | RI standards | V1–V3 Lexile | Skill #5',
    cardClass: 'nonfiction',
  },
  '504 Sit-In': {
    label: '504 Sit-In: Disability Rights & Advocacy',
    icon: '✊',
    productLine: 'Nonfiction',
    status: 'Live',
    platforms: [{ name: 'TPT', url: 'https://www.teacherspayteachers.com/store/communicate-by-design' }],
    desc: 'Grades 6–10 | RI standards | V1–V3 Lexile | Skill #4',
    cardClass: 'nonfiction',
  },
  'Capitol Crawl': {
    label: 'Capitol Crawl 1990: Source Analysis & Argumentation',
    icon: '🏛️',
    productLine: 'Nonfiction',
    status: 'Live',
    platforms: [{ name: 'TPT', url: 'https://www.teacherspayteachers.com/store/communicate-by-design' }],
    desc: 'Grades 6–10 | RI standards | V1–V3 Lexile | Skill #6',
    cardClass: 'nonfiction',
  },
  'Zitkala-Ša': {
    label: 'Zitkala-Ša: Voice, Identity & Resistance',
    icon: '🪶',
    productLine: 'Nonfiction',
    status: 'Live',
    platforms: [{ name: 'TPT', url: 'https://www.teacherspayteachers.com/store/communicate-by-design' }],
    desc: 'Grades 6–10 | RI standards | V1–V3 Lexile | Skill #3',
    cardClass: 'nonfiction',
  },
  'Wonder': {
    label: 'Wonder: Character Analysis',
    icon: '📖',
    productLine: 'Fiction',
    status: 'In Production',
    estimatedDate: 'TBD',
    desc: 'Grades 3–8 | RL.3.3–RL.7.3 | V1–V3 Lexile | Skill: Character Analysis',
    cardClass: 'fiction',
  },
};`;

// ── Inject into HTML ──────────────────────────────────────────────────────────

function inject(html, vocab) {
  const s = stats(vocab);
  const vocabJson = JSON.stringify(vocab);

  // Replace VOCAB array
  html = html.replace(
    /const VOCAB = \n?\[[\s\S]*?\];/,
    `const VOCAB = \n${vocabJson};`
  );

  // Replace PRODUCTS block
  html = html.replace(
    /const PRODUCTS = \{[\s\S]*?\};/,
    PRODUCTS_BLOCK
  );

  // Replace LINE filter buttons (keep in sync with product lines present in VOCAB)
  const LINE_BUTTONS = `<button class="line-btn active" data-line="all">All</button>
    <button class="line-btn" data-line="UFLI Phonics">UFLI</button>
    <button class="line-btn" data-line="Nonfiction Reading Units">Nonfiction</button>
    <button class="line-btn" data-line="Fiction Anchor Texts">Fiction</button>`;
  html = html.replace(
    /<button class="line-btn active"[\s\S]*?<\/button>[\s\S]*?<\/div>/,
    LINE_BUTTONS + '\n  </div>'
  );

  // Update stat numbers in HTML
  html = html.replace(/(<div class="stat-num" id="stat-total">)\d+(<\/div>)/, `$1${s.total}$2`);
  html = html.replace(/(<div class="stat-num" id="stat-core">)\d+(<\/div>)/,  `$1${s.core}$2`);
  html = html.replace(/(<div class="stat-num" id="stat-fringe">)\d+(<\/div>)/, `$1${s.fringe}$2`);
  html = html.replace(/(<div class="stat-num" id="stat-units">)\d+(<\/div>)/, `$1${s.units}$2`);
  html = html.replace(/(<div class="stat-num" id="stat-ufli">)\d+(<\/div>)/,  `$1${s.ufli}$2`);

  // Update hardcoded 476 / result-count line (fallback)
  html = html.replace(
    /(<div class="result-count" id="result-count">)\d+ words(<\/div>)/,
    `$1${s.total} words$2`
  );

  return { html, stats: s };
}

// ── Main ──────────────────────────────────────────────────────────────────────

function main() {
  console.log('\n' + '─'.repeat(60));
  console.log('CbD Vocabulary Explorer — Rebuild');
  console.log('─'.repeat(60) + '\n');

  console.log('Building vocab from source files...');
  const vocab = buildVocab();
  const s     = stats(vocab);

  console.log(`  ${s.total} total words  (${s.core} core · ${s.fringe} fringe)`);
  console.log(`  ${s.units} nonfiction units · ${s.ufli} UFLI lessons\n`);

  console.log('Reading HTML...');
  const original = fs.readFileSync(HTML_PATH, 'utf8');

  const { html, stats: newStats } = inject(original, vocab);

  if (html === original) {
    console.log('  No changes detected — already up to date.\n');
    return;
  }

  fs.writeFileSync(HTML_PATH, html, 'utf8');

  console.log('  Written: cbd-vocabulary-explorer.html');
  console.log('\n─'.repeat(60));
  console.log('DONE');
  console.log(`  Total words : ${newStats.total}`);
  console.log(`  Core        : ${newStats.core}`);
  console.log(`  Fringe      : ${newStats.fringe}`);
  console.log(`  Units       : ${newStats.units}`);
  console.log(`  UFLI lessons: ${newStats.ufli}`);
  console.log('─'.repeat(60) + '\n');
}

main();

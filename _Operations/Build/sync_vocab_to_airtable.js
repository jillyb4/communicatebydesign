/**
 * sync_vocab_to_airtable.js — Communicate by Design
 * ===================================================
 * Syncs the master vocabulary data (cbd_unit_vocab.js + ufli_lesson_configs.js)
 * to the Airtable Vocabulary table (tblL2KH04WijW8XUb).
 *
 * RUN AFTER:
 *   - Editing cbd_unit_vocab.js (any unit change, new unit added)
 *   - Editing ufli_lesson_configs.js (word changes to UFLI lessons)
 *
 * USAGE:
 *   AIRTABLE_API_KEY=patXXXXXXXXXXXXXX node sync_vocab_to_airtable.js
 *
 *   Dry run (shows diff, makes no changes):
 *   AIRTABLE_API_KEY=patXXXXXXXXXXXXXX DRY_RUN=true node sync_vocab_to_airtable.js
 *
 * HOW IT WORKS:
 *   1. Reads both source files — builds master word map
 *   2. Reads all current Airtable records
 *   3. Compares field by field (diff)
 *   4. Creates new records + updates changed records in batches of 10
 *   5. Prints a change report
 *
 * DOES NOT DELETE records — removal is manual to prevent accidental data loss.
 */

'use strict';

const path = require('path');

// ── Config ────────────────────────────────────────────────────────────────────

const AIRTABLE_API_KEY = process.env.AIRTABLE_API_KEY;
const DRY_RUN          = process.env.DRY_RUN === 'true';
const BASE_ID          = 'appeaT8hkeXWqQKIj';
const TABLE_ID         = 'tblL2KH04WijW8XUb';

// ── Field IDs (do not rename these without updating Airtable schema) ──────────

const F = {
  WORD          : 'fld1QN7hpfdjCTtS2',
  WORD_TYPE     : 'fldRKp7t0RQlLDgjf',
  FITZ_CATEGORY : 'fldGOhcGmVHvEpth6',
  FITZ_COLOR    : 'fldpr07ErXvfGXX4K',
  UFLI_LESSONS  : 'fldyGwwn8AwUeY2gj',
  FIRST_LESSON  : 'fldXkX1JgtnE49Tfl',
  NONFICTION    : 'fldMBgyzPpdcAp4pZ',
  PRODUCT_LINES : 'fldvahgolI8nTsbKw',
  PRODUCT_COUNT : 'fldQS3tOYjfNfXBSW',
  BOTH_LINES    : 'flddpJR7hsqJcVyzn',
  PRIORITY      : 'fldV9kgi0k3IF4x9C',
  NOTES         : 'fldrwJdR2Bn7XR0nd',
};

// ── Data sources ──────────────────────────────────────────────────────────────

const OPS = path.join(__dirname);
const UFLI_PATH = path.join(__dirname, '..', 'Products', 'UFLI Phonics', 'UFLI', 'ufli_lesson_configs.js');

const nonfictionUnits   = require(path.join(OPS, 'cbd_unit_vocab.js'));
const ufliLessons       = require(UFLI_PATH);
const { getFitzgeraldCategory } = require(path.join(OPS, 'fitzgerald_key.js'));

// ── Airtable REST helpers ─────────────────────────────────────────────────────

const AT_BASE = `https://api.airtable.com/v0/${BASE_ID}/${TABLE_ID}`;

async function atFetch(url, opts = {}) {
  const res = await fetch(url, {
    ...opts,
    headers: {
      'Authorization': `Bearer ${AIRTABLE_API_KEY}`,
      'Content-Type': 'application/json',
      ...(opts.headers || {}),
    },
  });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`Airtable error ${res.status}: ${body}`);
  }
  return res.json();
}

async function fetchAllRecords() {
  const records = [];
  let offset;
  do {
    const url = new URL(AT_BASE);
    url.searchParams.set('returnFieldsByFieldId', 'true');
    if (offset) url.searchParams.set('offset', offset);
    const data = await atFetch(url.toString());
    records.push(...data.records);
    offset = data.offset;
  } while (offset);
  return records;
}

async function createRecords(batch) {
  return atFetch(AT_BASE, {
    method: 'POST',
    body: JSON.stringify({ records: batch }),
  });
}

async function updateRecords(batch) {
  return atFetch(AT_BASE, {
    method: 'PATCH',
    body: JSON.stringify({ records: batch }),
  });
}

// ── Airtable value normalization ──────────────────────────────────────────────

// Map source wordType strings to Airtable single-select option names
const WORD_TYPE_LABELS = { core: 'Core', fringe: 'Fringe', heart: 'Heart Word' };
function wordTypeLabel(t) { return WORD_TYPE_LABELS[t] || 'Fringe'; }

// Map full unit titles (from cbd_unit_vocab.js) to Airtable multiselect option names
const UNIT_TITLE_MAP = {
  // Nonfiction (6 live units)
  'Radium Girls'                             : 'Radium Girls',
  "Keiko: A Whale's Journey"                 : 'Keiko',
  'Frances Kelsey and the Thalidomide Crisis': 'Frances Kelsey',
  '504 Sit-In 1977'                          : '504 Sit-In',
  'Capitol Crawl 1990'                       : 'Capitol Crawl',
  'Zitkala-Ša'                               : 'Zitkala-Ša',
  // Fiction Anchor Texts
  'Wonder: Character Analysis'               : 'Wonder',
  // Poetry Reading Units
  'What the Voice Carries'                   : 'What the Voice Carries',
  // Picture Book Companions
  'All the Way to the Top'                   : 'All the Way to the Top',
};
function unitLabel(title) { return UNIT_TITLE_MAP[title] || title; }

// Extract string value from Airtable single-select (may be object or string)
function selectName(v) { return v && typeof v === 'object' ? v.name : v; }

// ── Build master vocabulary map from source files ─────────────────────────────
// Key: lowercase word. Value: aggregated data across all product lines.

function buildMasterMap() {
  const map = new Map(); // word (lowercase) → data object

  // ── Helper: get or init a word entry ──
  function entry(word) {
    const key = word.toLowerCase();
    if (!map.has(key)) {
      const fitz = getFitzgeraldCategory(key);
      map.set(key, {
        word: key,
        wordType: null,       // set on first encounter
        fitzCategory: fitz.label,
        fitzColor: fitz.color,
        ufliLessons: [],      // lesson numbers (int)
        firstLesson: null,
        nonfictionUnits: [],  // unit titles
        productLines: new Set(),
        priority: false,
        notes: [],
      });
    }
    return map.get(key);
  }

  // ── 1. Nonfiction units ────────────────────────────────────────────────────
  for (const unit of nonfictionUnits) {
    // Separate fiction units (unit 7+, unitTitle contains ':') from nonfiction (1–6)
    // unitTitle check: nonfiction units are the first 6; Wonder is fiction.
    // Use productLine field to distinguish.
    // Skip pending-build stubs — no words to sync yet
    if (unit.pendingBuild) continue;

    const isNonfiction  = unit.productLine === 'Nonfiction Reading Unit';
    const isFiction     = unit.productLine === 'Fiction Anchor Text Unit' ||
                          unit.unitTitle.includes('Character Analysis');
    const isPoetry      = unit.productLine === 'Poetry Reading Unit';
    const isPictureBook = unit.productLine === 'Picture Book Companion';
    const productLine   = isFiction     ? 'Fiction Anchor Texts'      :
                          isPoetry      ? 'Poetry Reading Units'       :
                          isPictureBook ? 'Picture Book Companions'    :
                                         'Nonfiction Reading Units';

    for (const w of unit.newWords) {
      const e = entry(w.word);
      // Word type: fringe takes priority over core if ever mixed across units
      if (!e.wordType || (e.wordType === 'core' && w.type === 'fringe')) {
        e.wordType = w.type;
      }
      const mappedTitle = unitLabel(unit.unitTitle);
      if (isNonfiction && !e.nonfictionUnits.includes(mappedTitle)) {
        e.nonfictionUnits.push(mappedTitle);
      }
      e.productLines.add(productLine);
      if (w.top5) e.priority = true;
      if (w.instructional) {
        const note = `${mappedTitle}: ${w.instructional}`;
        if (!e.notes.includes(note)) e.notes.push(note);
      }
      if (w.notes && typeof w.notes === 'string') {
        const noteKey = `${mappedTitle} — ${w.notes}`;
        if (!e.notes.includes(noteKey)) e.notes.push(noteKey);
      }
    }
  }

  // ── 2. UFLI lessons ───────────────────────────────────────────────────────
  for (const lesson of ufliLessons) {
    if (!lesson.newWords || lesson.newWords.length === 0) continue;

    for (const w of lesson.newWords) {
      const e = entry(w.word);
      if (!e.wordType) e.wordType = w.type;
      if (!e.ufliLessons.includes(lesson.number)) {
        e.ufliLessons.push(lesson.number);
      }
      e.productLines.add('UFLI Phonics');
    }

    // heart words
    for (const hw of (lesson.heartWords || [])) {
      const wordStr = typeof hw === 'string' ? hw : hw.word;
      if (!wordStr) continue;
      const e = entry(wordStr);
      if (!e.wordType) e.wordType = 'heart';
      if (!e.ufliLessons.includes(lesson.number)) {
        e.ufliLessons.push(lesson.number);
      }
      e.productLines.add('UFLI Phonics');
    }
  }

  // ── 3. Post-process ───────────────────────────────────────────────────────
  for (const [, e] of map) {
    // Sort UFLI lessons, set firstLesson
    e.ufliLessons.sort((a, b) => a - b);
    e.firstLesson = e.ufliLessons.length > 0 ? String(e.ufliLessons[0]) : null;
    e.ufliLessonsStr = e.ufliLessons.length > 0 ? e.ufliLessons.join(', ') : null;

    // Product count = number of distinct product lines
    e.productLines = [...e.productLines].sort();
    e.productCount = e.productLines.length;
    e.appearsInBoth = e.productLines.includes('UFLI Phonics') &&
                      e.productLines.some(p => p !== 'UFLI Phonics');

    // Nonfiction units: sorted
    e.nonfictionUnits.sort();

    // Notes: join
    e.notesStr = e.notes.join(' | ') || null;

    // Default type if still null
    if (!e.wordType) e.wordType = 'fringe';
  }

  return map;
}

// ── Diff helpers ──────────────────────────────────────────────────────────────

function multiSelectVal(arr) {
  // Airtable returns multipleSelects as array of strings or objects {id, name}
  if (!arr) return '';
  return arr.map(x => (x && typeof x === 'object' ? x.name : x)).sort().join('|');
}

function fieldsDiffer(current, desired) {
  // Returns true if any mapped field has changed
  // Single-select fields may return {id, name} objects — extract .name before comparing
  const checks = [
    [F.WORD_TYPE,     selectName(current[F.WORD_TYPE]),                   wordTypeLabel(desired.wordType)],
    [F.FITZ_CATEGORY, selectName(current[F.FITZ_CATEGORY]),               desired.fitzCategory],
    [F.FITZ_COLOR,    current[F.FITZ_COLOR],                             desired.fitzColor],
    [F.UFLI_LESSONS,  current[F.UFLI_LESSONS]  ?? null,                  desired.ufliLessonsStr],
    [F.FIRST_LESSON,  current[F.FIRST_LESSON]  ?? null,                  desired.firstLesson],
    [F.PRODUCT_COUNT, current[F.PRODUCT_COUNT] ?? 0,                     desired.productCount],
    [F.BOTH_LINES,    current[F.BOTH_LINES]    ?? false,                  desired.appearsInBoth],
    [F.PRIORITY,      current[F.PRIORITY]      ?? false,                  desired.priority],
    [F.NOTES,         current[F.NOTES]         ?? null,                  desired.notesStr],
  ];

  const multiChecks = [
    [F.NONFICTION,    multiSelectVal(current[F.NONFICTION]),    multiSelectVal(desired.nonfictionUnits)],
    [F.PRODUCT_LINES, multiSelectVal(current[F.PRODUCT_LINES]), multiSelectVal(desired.productLines)],
  ];

  for (const [, cur, des] of [...checks, ...multiChecks]) {
    if (cur !== des) return true;
  }
  return false;
}

function buildFields(e) {
  const fields = {
    [F.WORD]         : e.word,
    [F.WORD_TYPE]    : wordTypeLabel(e.wordType),
    [F.FITZ_CATEGORY]: e.fitzCategory,
    [F.FITZ_COLOR]   : e.fitzColor,
    [F.PRODUCT_COUNT]: e.productCount,
    [F.BOTH_LINES]   : e.appearsInBoth,
    [F.PRIORITY]     : e.priority,
    [F.PRODUCT_LINES]: e.productLines,
    [F.NONFICTION]   : e.nonfictionUnits,
  };
  if (e.ufliLessonsStr) fields[F.UFLI_LESSONS] = e.ufliLessonsStr;
  if (e.firstLesson)    fields[F.FIRST_LESSON]  = e.firstLesson;
  if (e.notesStr)       fields[F.NOTES]         = e.notesStr;
  return fields;
}

// ── Batch helper (10 records max per Airtable call) ───────────────────────────

function chunk(arr, size) {
  const out = [];
  for (let i = 0; i < arr.length; i += size) out.push(arr.slice(i, i + size));
  return out;
}

// ── Main ──────────────────────────────────────────────────────────────────────

async function main() {
  if (!AIRTABLE_API_KEY) {
    console.error('ERROR: Set AIRTABLE_API_KEY env variable before running.');
    console.error('  AIRTABLE_API_KEY=patXXXX node sync_vocab_to_airtable.js');
    process.exit(1);
  }

  console.log(`\n${'─'.repeat(60)}`);
  console.log('CbD Vocabulary → Airtable Sync');
  console.log(DRY_RUN ? '  MODE: DRY RUN (no changes will be written)' : '  MODE: LIVE');
  console.log(`${'─'.repeat(60)}\n`);

  // 1. Build source map
  console.log('Building master vocabulary map from source files...');
  const masterMap = buildMasterMap();
  console.log(`  ${masterMap.size} words in source\n`);

  // 2. Fetch current Airtable records
  console.log('Fetching current Airtable records...');
  const existing = await fetchAllRecords();
  console.log(`  ${existing.size ?? existing.length} records in Airtable\n`);

  // Index existing by lowercase word
  const existingByWord = new Map();
  for (const rec of existing) {
    const w = rec.fields[F.WORD];
    if (w) existingByWord.set(w.toLowerCase(), rec);
  }

  // 3. Diff
  const toCreate = [];
  const toUpdate = [];

  for (const [word, desired] of masterMap) {
    if (!existingByWord.has(word)) {
      toCreate.push({ fields: buildFields(desired) });
    } else {
      const rec = existingByWord.get(word);
      if (fieldsDiffer(rec.fields, desired)) {
        toUpdate.push({ id: rec.id, fields: buildFields(desired) });
      }
    }
  }

  // 4. Report
  console.log('─'.repeat(60));
  console.log(`DIFF SUMMARY`);
  console.log(`  New words to create : ${toCreate.length}`);
  console.log(`  Changed words to update: ${toUpdate.length}`);
  console.log(`  Unchanged           : ${masterMap.size - toCreate.length - toUpdate.length}`);

  if (toCreate.length > 0) {
    console.log('\n  NEW WORDS:');
    for (const r of toCreate) console.log(`    + ${r.fields[F.WORD]}  (${r.fields[F.WORD_TYPE]})`);
  }

  if (toUpdate.length > 0) {
    console.log('\n  UPDATED WORDS:');
    for (const r of toUpdate) {
      const src = masterMap.get(r.fields[F.WORD]);
      console.log(`    ~ ${r.fields[F.WORD]}  (${r.fields[F.WORD_TYPE]}) — product lines: ${src.productLines.join(', ')}`);
    }
  }

  if (DRY_RUN) {
    console.log('\n  DRY RUN — no changes written. Remove DRY_RUN=true to apply.');
    return;
  }

  if (toCreate.length === 0 && toUpdate.length === 0) {
    console.log('\n  Airtable is already in sync. Nothing to do.');
    return;
  }

  // 5. Write
  console.log('\n─'.repeat(60));
  let created = 0, updated = 0;

  for (const batch of chunk(toCreate, 10)) {
    await createRecords(batch);
    created += batch.length;
    process.stdout.write(`\r  Created: ${created}/${toCreate.length}`);
  }
  if (created > 0) console.log();

  for (const batch of chunk(toUpdate, 10)) {
    await updateRecords(batch);
    updated += batch.length;
    process.stdout.write(`\r  Updated: ${updated}/${toUpdate.length}`);
  }
  if (updated > 0) console.log();

  console.log('\n─'.repeat(60));
  console.log(`DONE: ${created} created, ${updated} updated.`);
  console.log('─'.repeat(60) + '\n');
}

main().catch(err => {
  console.error('\nSync failed:', err.message);
  process.exit(1);
});

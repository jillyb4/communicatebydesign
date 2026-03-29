#!/usr/bin/env node
/**
 * Nonfiction Unit Printable Kit Builder — Communicate by Design
 *
 * Fetches ARASAAC symbols for all nonfiction unit vocabulary,
 * then generates the standard 5-component printable kit for each unit.
 *
 * Usage:
 *   node build_nonfiction_kits.js              # Build all units
 *   node build_nonfiction_kits.js --unit 1     # Build Radium Girls only
 *   node build_nonfiction_kits.js --fetch-only # Just fetch symbols, don't build
 */

const path = require('path');
const fs = require('fs');
const https = require('https');

// ── Paths ─────────────────────────────────────────────────────
const SYMBOL_DIR = path.join(__dirname, 'symbol_cache');
const OUTPUT_DIR = path.join(__dirname, '..', 'Products', 'Nonfiction Units', 'Printable_Kits_v6');
const VOCAB_FILE = path.join(__dirname, 'nonfiction_unit_vocab.js');

// The unit kit builder is in the UFLI folder — require it
const KIT_BUILDER_PATH = path.join(__dirname, 'build_unit_printable_kit.js');

// ── Symbol Fetcher (simplified — just ARASAAC) ───────────────

const ARASAAC_SEARCH = 'https://api.arasaac.org/v1/pictograms/en/search/';
const ARASAAC_IMAGE = 'https://static.arasaac.org/pictograms/';

function fetchJson(url) {
  return new Promise((resolve, reject) => {
    https.get(url, { headers: { 'User-Agent': 'CbD-SymbolFetcher/1.0' } }, res => {
      if (res.statusCode === 301 || res.statusCode === 302) {
        return fetchJson(res.headers.location).then(resolve).catch(reject);
      }
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); }
        catch(e) { reject(new Error(`JSON parse failed for ${url}`)); }
      });
    }).on('error', reject);
  });
}

function fetchImage(url) {
  return new Promise((resolve, reject) => {
    https.get(url, { headers: { 'User-Agent': 'CbD-SymbolFetcher/1.0' } }, res => {
      if (res.statusCode === 301 || res.statusCode === 302) {
        return fetchImage(res.headers.location).then(resolve).catch(reject);
      }
      const chunks = [];
      res.on('data', chunk => chunks.push(chunk));
      res.on('end', () => resolve(Buffer.concat(chunks)));
    }).on('error', reject);
  });
}

async function fetchSymbolForWord(word) {
  // Skip multi-word phrases and abbreviations that won't have symbols
  const cleanWord = word.toLowerCase().trim();
  if (cleanWord.includes(' ')) {
    // Try each word separately for multi-word terms
    console.log(`    ⚠️  "${word}" is multi-word — skipping ARASAAC (draw-it candidate)`);
    return null;
  }

  const cachePath = path.join(SYMBOL_DIR, `arasaac_${cleanWord}.png`);
  if (fs.existsSync(cachePath)) {
    return cachePath; // Already cached
  }

  try {
    const results = await fetchJson(ARASAAC_SEARCH + encodeURIComponent(cleanWord));
    if (!Array.isArray(results) || results.length === 0) {
      console.log(`    ⚠️  "${word}" — no ARASAAC symbol found (draw-it candidate)`);
      return null;
    }

    // Pick first result
    const id = results[0]._id;
    const imageUrl = `${ARASAAC_IMAGE}${id}/${id}_500.png`;
    const imageBuffer = await fetchImage(imageUrl);
    fs.writeFileSync(cachePath, imageBuffer);
    console.log(`    ✅ "${word}" — fetched (ID: ${id})`);
    return cachePath;
  } catch (e) {
    console.log(`    ❌ "${word}" — fetch error: ${e.message}`);
    return null;
  }
}

async function fetchAllSymbols(units) {
  fs.mkdirSync(SYMBOL_DIR, { recursive: true });

  // Collect all unique words across all units
  const allWords = new Set();
  for (const unit of units) {
    for (const w of unit.newWords) {
      allWords.add(w.word);
    }
  }

  console.log(`\n  Fetching symbols for ${allWords.size} unique words across ${units.length} units...\n`);

  let fetched = 0, cached = 0, missing = 0;
  for (const word of allWords) {
    const cachePath = path.join(SYMBOL_DIR, `arasaac_${word.toLowerCase().trim()}.png`);
    if (fs.existsSync(cachePath)) {
      cached++;
      continue;
    }
    const result = await fetchSymbolForWord(word);
    if (result) fetched++;
    else missing++;

    // Rate limit — be nice to ARASAAC
    await new Promise(r => setTimeout(r, 200));
  }

  console.log(`\n  Symbol fetch complete: ${cached} cached, ${fetched} new, ${missing} missing`);
  return { cached, fetched, missing };
}


// ── Build Kits ───────────────────────────────────────────────

async function buildKits(units, fetchOnly = false) {
  // Step 1: Fetch all symbols
  const stats = await fetchAllSymbols(units);

  if (fetchOnly) {
    console.log('\n  --fetch-only mode. Symbols cached. Exiting.');
    return;
  }

  // Step 2: Load the kit builder
  const { buildUnitKit } = require(KIT_BUILDER_PATH);

  // Step 3: Build each unit's kit
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });

  console.log(`\n  Building printable kits...\n`);

  for (const unit of units) {
    // Override the config to use unitTitle for display
    const displayConfig = {
      ...unit,
      // Override the number-based display in the kit builder
      // The kit builder uses `Lesson ${config.number}` — we need to patch this
    };

    const result = await buildUnitKit(displayConfig, {
      symbolDir: SYMBOL_DIR,
      outputDir: OUTPUT_DIR,
      accessLevel: 'level2',
      productLine: unit.productLine || 'Nonfiction Reading Unit',
    });

    if (result) {
      // Rename the output file to use the unit title instead of lesson number
      const safeTitle = unit.unitTitle.replace(/[^a-zA-Z0-9_-]/g, '_').replace(/_+/g, '_');
      const newName = `${safeTitle}_Printable_Kit.docx`;
      const newPath = path.join(OUTPUT_DIR, newName);
      if (result.path !== newPath) {
        fs.renameSync(result.path, newPath);
        console.log(`    → Renamed to: ${newName}`);
      }
    }
  }
}


// ── Main ─────────────────────────────────────────────────────

async function main() {
  console.log('═══════════════════════════════════════════════════');
  console.log('  COMMUNICATE BY DESIGN');
  console.log('  Nonfiction Unit Printable Kit Builder');
  console.log('═══════════════════════════════════════════════════\n');

  const args = process.argv.slice(2);
  const units = require(VOCAB_FILE);
  const fetchOnly = args.includes('--fetch-only');

  let toBuild;
  if (args.includes('--unit')) {
    const num = parseInt(args[args.indexOf('--unit') + 1]);
    toBuild = units.filter(u => u.number === num);
    if (toBuild.length === 0) {
      console.error(`❌ Unit ${num} not found. Available: ${units.map(u => `${u.number} (${u.unitTitle})`).join(', ')}`);
      process.exit(1);
    }
  } else {
    toBuild = units;
  }

  console.log(`  Units to process: ${toBuild.map(u => u.unitTitle).join(', ')}`);

  await buildKits(toBuild, fetchOnly);

  console.log(`\n═══════════════════════════════════════════════════`);
  console.log(`  ✅ Done!`);
  console.log(`  📂 ${OUTPUT_DIR}`);
  console.log(`═══════════════════════════════════════════════════\n`);
}

main().catch(err => { console.error('❌ Fatal:', err.message, err.stack); process.exit(1); });

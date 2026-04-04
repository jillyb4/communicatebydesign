/**
 * Communicate by Design — AAC Symbol Fetcher
 *
 * Fetches open-source AAC pictograms for use in CbD products (UFLI units,
 * nonfiction units, AT/AAC tools). Symbols are sourced from ARASAAC
 * (primary) and Mulberry (fallback).
 *
 * USAGE:
 *   const { fetchSymbols, buildSymbolPage } = require('./cbd_symbol_fetcher');
 *
 *   // Fetch symbols for a word list
 *   const symbols = await fetchSymbols(['read', 'help', 'want', 'more', 'stop']);
 *
 *   // Build a printable symbol support page for a unit
 *   const docxChildren = await buildSymbolPage({
 *     unitTitle: 'UFLI Unit 4: Digraphs',
 *     coreWords: ['read', 'help', 'want', 'more', 'stop', 'go', 'like', 'not'],
 *     fringeWords: ['digraph', 'blend', 'phoneme', 'ship', 'chin', 'thin'],
 *     includeTeacherNote: true,
 *     includeQRCode: true,
 *   });
 *
 * LICENSE NOTES:
 *   - ARASAAC: CC BY-NC-SA 4.0 (Government of Aragón). Free for educational
 *     use. Attribution required. Non-commercial — CbD products sold on TPT
 *     are EDUCATIONAL MATERIALS, which ARASAAC explicitly permits. Their
 *     FAQ states: "You can use them in educational materials, therapeutic
 *     materials, and adapted materials." BUT: check their current terms at
 *     https://arasaac.org/terms-of-use before each product launch.
 *   - Mulberry: CC BY-SA 4.0. Permits commercial use with attribution.
 *     More permissive license. Fewer symbols (~3,000 vs ARASAAC's ~13,000).
 *   - OpenSymbols API: aggregates both + others. Requires API token.
 *
 * RECOMMENDATION FOR CbD:
 *   Use ARASAAC as primary (largest library, best AAC coverage).
 *   Use Mulberry as fallback for words ARASAAC doesn't have.
 *   Always include attribution per license requirements.
 *   Always include teacher note: "Use your student's own system symbols first."
 */

const https = require('https');
const fs = require('fs');
const path = require('path');
let sharp;
try { sharp = require('sharp'); } catch(e) {
  console.warn('sharp not installed — symbols will not be normalized. Run: npm install sharp');
}

// ============================================================
// CONFIGURATION
// ============================================================

const CONFIG = {
  // ARASAAC API (no authentication required for basic search + image retrieval)
  arasaac: {
    searchUrl: 'https://api.arasaac.org/v1/pictograms/en/search/',
    imageUrl: 'https://static.arasaac.org/pictograms/',
    // Image URL pattern: {imageUrl}/{id}/{id}_500.png (500px) or {id}_2500.png (high res)
    imageSize: 500,  // 500px default, 2500px for high-res
    attribution: 'Pictographic symbols © Government of Aragón. ARASAAC (https://arasaac.org). Licensed under CC BY-NC-SA 4.0.',
  },

  // Mulberry fallback (download full set from GitHub, search locally)
  mulberry: {
    csvUrl: 'https://raw.githubusercontent.com/mulberrysymbols/mulberry-symbols/master/categories.csv',
    svgBaseUrl: 'https://raw.githubusercontent.com/mulberrysymbols/mulberry-symbols/master/EN/',
    attribution: 'Mulberry Symbols (https://mulberrysymbols.org). Licensed under CC BY-SA 4.0.',
  },

  // OpenSymbols API (requires free API token — register at opensymbols.org)
  openSymbols: {
    searchUrl: 'https://www.opensymbols.org/api/v2/symbols',
    // Requires: ?access_token=YOUR_TOKEN&q=search_term
    // Get token: POST https://www.opensymbols.org/api/v2/token
  },

  // Local cache directory for downloaded symbols
  cacheDir: path.join(__dirname, '..', 'Symbols', 'symbol_cache'),

  // Master symbol library (cumulative across all units)
  libraryFile: path.join(__dirname, '..', 'Symbols', 'symbol_cache', '_symbol_library.json'),

  // QR code for free symbol resource
  symbolResourceUrl: 'https://arasaac.org/pictograms/search',
  symbolResourceLabel: 'Free AAC Symbol Search (ARASAAC)',

  // ============================================================
  // SYMBOL SIZING STANDARDS (AT/AAC best practices)
  // ============================================================
  //
  // These sizes are based on:
  //   - TD Snap grid layouts: 30-position (largest targets, eye gaze/
  //     limited motor), 40-position (mid), 66-position (smallest, fine motor)
  //   - Low-tech communication board standards: minimum 2.5cm (1 inch) for
  //     direct selection, 3.5cm+ (1.5 inch) for eye gaze boards
  //   - WCAG 2.2 SC 2.5.8: minimum 24×24 CSS px target size
  //   - Speak for Yourself research: smaller buttons with consistent motor
  //     planning outperform larger buttons with navigation demands
  //   - Print at 300 DPI: 1 inch = 300px, 1.5 inch = 450px, 2 inch = 600px
  //
  // CbD products are PRINT materials (not screen). All sizing is in
  // points (1/72 inch) for docx, which translates to print dimensions.
  //
  // The symbol IMAGE is always fetched at 500px from ARASAAC.
  // The DISPLAY SIZE in the document varies by access level.
  //
  symbolSizing: {
    // Level 1: Partner-assisted scanning / beginning eye gaze
    // Largest targets. Max 4 per row on letter-size paper.
    // Print size: ~1.75 inches (126pt) — allows thick borders + spacing
    level1: {
      imageWidth: 126,   // points (1.75 inches)
      imageHeight: 126,
      cellPadding: 150,  // twips (generous spacing between targets)
      labelSize: 24,     // font size in half-points (12pt)
      maxPerRow: 3,      // max symbols per row at this size
      borderWidth: 3,    // thick border for visual separation
      description: 'Level 1: Partner-assisted / beginning eye gaze (3 per row, ~1.75" each)',
    },
    // Level 2: Eye gaze / direct selection with motor challenges
    // Mid-size targets. Max 4 per row.
    // Print size: ~1.25 inches (90pt)
    level2: {
      imageWidth: 90,
      imageHeight: 90,
      cellPadding: 100,
      labelSize: 22,     // 11pt
      maxPerRow: 4,
      borderWidth: 2,
      description: 'Level 2: Eye gaze / direct selection with motor support (4 per row, ~1.25" each)',
    },
    // Level 3: Independent device users / adapted keyboard
    // Standard reference size. 5-6 per row.
    // Print size: ~1 inch (72pt) — standard visual reference
    level3: {
      imageWidth: 72,
      imageHeight: 72,
      cellPadding: 75,
      labelSize: 20,     // 10pt
      maxPerRow: 5,
      borderWidth: 1,
      description: 'Level 3: Independent device users / reference (5 per row, ~1" each)',
    },
  },
};

// ============================================================
// SYMBOL NORMALIZATION
// ============================================================
// Every symbol gets normalized to a standard square canvas so the
// CbD symbol library is consistent across ALL products and lessons.
// Trim whitespace → resize to content area → center on white square.
const NORM_CANVAS = 400;   // Standard square canvas size (px)
const NORM_CONTENT = 340;  // Max content area within canvas (30px padding each side)
const NORM_BG = { r: 255, g: 255, b: 255, alpha: 1 };

async function normalizeSymbol(inputBuffer) {
  if (!sharp) return inputBuffer;  // Pass through if sharp not available
  try {
    // Step 1: Trim whitespace/transparency
    const trimMeta = await sharp(inputBuffer).trim().toBuffer({ resolveWithObject: true });
    // Step 2: Resize trimmed content to fit standard box (preserve aspect ratio)
    const resized = await sharp(trimMeta.data)
      .resize(NORM_CONTENT, NORM_CONTENT, { fit: 'inside', withoutEnlargement: false })
      .toBuffer({ resolveWithObject: true });
    // Step 3: Center on standard white canvas
    const rInfo = resized.info;
    const left = Math.floor((NORM_CANVAS - rInfo.width) / 2);
    const top = Math.floor((NORM_CANVAS - rInfo.height) / 2);
    return await sharp({
      create: { width: NORM_CANVAS, height: NORM_CANVAS, channels: 4, background: NORM_BG }
    }).composite([{ input: resized.data, left, top }]).png().toBuffer();
  } catch(e) {
    console.warn(`Normalization failed, using original: ${e.message}`);
    return inputBuffer;
  }
}

// ============================================================
// CORE FUNCTIONS
// ============================================================

// ============================================================
// CUMULATIVE SYMBOL LIBRARY
// ============================================================
// The library grows across units. Core words (read, help, want, more,
// stop, go, like, not, yes, no) appear in EVERY unit — they get fetched
// once and reused. Fringe words are unit-specific but still get added
// to the master library so we have a complete record of every symbol
// CbD has ever used, which unit introduced it, and whether it's core
// or fringe.
//
// Library structure (_symbol_library.json):
// {
//   "words": {
//     "read": {
//       "arasaacId": 6009,
//       "localFile": "arasaac_read_6009.png",
//       "type": "core",
//       "firstUsedIn": "UFLI Unit 1: Getting Ready",
//       "usedIn": ["UFLI Unit 1", "UFLI Unit 2", ...],
//       "dateAdded": "2026-03-18"
//     }
//   },
//   "stats": { "totalWords": 47, "core": 15, "fringe": 32, "notFound": 3 }
// }

/**
 * Load the master symbol library (or create empty if none exists)
 */
function loadLibrary() {
  ensureCache();
  if (fs.existsSync(CONFIG.libraryFile)) {
    try {
      return JSON.parse(fs.readFileSync(CONFIG.libraryFile, 'utf8'));
    } catch (e) {
      console.warn('Library file corrupted, starting fresh.');
    }
  }
  return { words: {}, stats: { totalWords: 0, core: 0, fringe: 0, notFound: 0 } };
}

/**
 * Save the master symbol library
 */
function saveLibrary(library) {
  ensureCache();
  // Recount stats
  const words = Object.values(library.words);
  library.stats = {
    totalWords: words.length,
    core: words.filter(w => w.type === 'core').length,
    fringe: words.filter(w => w.type === 'fringe').length,
    notFound: words.filter(w => w.arasaacId === null).length,
  };
  fs.writeFileSync(CONFIG.libraryFile, JSON.stringify(library, null, 2));
}

/**
 * Register a word in the library. If it already exists, just add
 * the new unit to its usedIn list.
 */
function registerWord(library, word, symbolResult, type, unitName) {
  const existing = library.words[word];
  if (existing) {
    if (!existing.usedIn.includes(unitName)) {
      existing.usedIn.push(unitName);
    }
    return existing;
  }
  library.words[word] = {
    arasaacId: symbolResult ? symbolResult.id : null,
    localFile: symbolResult ? path.basename(symbolResult.localPath || '') : null,
    type: type,  // 'core' or 'fringe'
    firstUsedIn: unitName,
    usedIn: [unitName],
    dateAdded: new Date().toISOString().split('T')[0],
  };
  return library.words[word];
}

/**
 * Check if a word is already in the library with a cached image
 * Returns the symbol info if cached, null if needs fetching
 */
function getCachedSymbol(library, word) {
  const entry = library.words[word];
  if (!entry || !entry.localFile) return null;
  const filepath = path.join(CONFIG.cacheDir, entry.localFile);
  if (!fs.existsSync(filepath)) return null;
  return {
    id: entry.arasaacId,
    keyword: word,
    localPath: filepath,
    source: 'arasaac',
    cached: true,
  };
}

/**
 * Print a library summary
 */
function printLibrarySummary() {
  const lib = loadLibrary();
  console.log('\n=== CbD Symbol Library Summary ===');
  console.log(`Total words: ${lib.stats.totalWords}`);
  console.log(`Core words: ${lib.stats.core}`);
  console.log(`Fringe words: ${lib.stats.fringe}`);
  console.log(`Not found in ARASAAC: ${lib.stats.notFound}`);

  // Show which units have contributed
  const units = new Set();
  for (const w of Object.values(lib.words)) {
    w.usedIn.forEach(u => units.add(u));
  }
  if (units.size > 0) {
    console.log(`\nUnits using symbols: ${units.size}`);
    for (const u of units) console.log(`  - ${u}`);
  }

  // Show words that appear in the most units (most reused)
  const sorted = Object.entries(lib.words)
    .sort((a, b) => b[1].usedIn.length - a[1].usedIn.length)
    .slice(0, 10);
  if (sorted.length > 0) {
    console.log(`\nMost reused words:`);
    for (const [word, info] of sorted) {
      console.log(`  ${word} (${info.type}) — used in ${info.usedIn.length} unit(s)`);
    }
  }
}

/**
 * Fetch a URL and return JSON or buffer
 */
function httpGet(url, returnBuffer = false) {
  return new Promise((resolve, reject) => {
    const handler = (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        return httpGet(res.headers.location, returnBuffer).then(resolve).catch(reject);
      }
      if (returnBuffer) {
        const chunks = [];
        res.on('data', chunk => chunks.push(chunk));
        res.on('end', () => resolve(Buffer.concat(chunks)));
      } else {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          try { resolve(JSON.parse(data)); }
          catch(e) { resolve(data); }
        });
      }
    };
    const mod = url.startsWith('https') ? https : require('http');
    mod.get(url, handler).on('error', reject);
  });
}

/**
 * Ensure cache directory exists
 */
function ensureCache() {
  if (!fs.existsSync(CONFIG.cacheDir)) {
    fs.mkdirSync(CONFIG.cacheDir, { recursive: true });
  }
}

/**
 * Search ARASAAC for a word and return the best pictogram match
 * Returns: { id, keyword, imageUrl, source: 'arasaac' } or null
 */
async function searchArasaac(word) {
  try {
    const results = await httpGet(CONFIG.arasaac.searchUrl + encodeURIComponent(word.toLowerCase()));
    if (!Array.isArray(results) || results.length === 0) return null;

    // Find best match: prefer exact keyword match
    let best = results[0];
    for (const r of results) {
      if (r.keywords) {
        const exactMatch = r.keywords.find(k =>
          k.keyword && k.keyword.toLowerCase() === word.toLowerCase()
        );
        if (exactMatch) { best = r; break; }
      }
    }

    const id = best._id;
    const size = CONFIG.arasaac.imageSize;
    return {
      id,
      keyword: word,
      imageUrl: `${CONFIG.arasaac.imageUrl}${id}/${id}_${size}.png`,
      source: 'arasaac',
    };
  } catch (e) {
    console.warn(`ARASAAC search failed for "${word}": ${e.message}`);
    return null;
  }
}

/**
 * Download a symbol image to cache and return the local file path
 */
async function downloadSymbol(symbol) {
  ensureCache();
  const ext = symbol.imageUrl.endsWith('.svg') ? 'svg' : 'png';
  const filename = `${symbol.source}_${symbol.keyword.replace(/\s+/g, '_')}_${symbol.id}.${ext}`;
  const filepath = path.join(CONFIG.cacheDir, filename);

  if (fs.existsSync(filepath)) {
    return filepath; // Already cached
  }

  try {
    const buffer = await httpGet(symbol.imageUrl, true);
    // Normalize to standard 400×400 canvas before caching
    const normalized = await normalizeSymbol(buffer);
    fs.writeFileSync(filepath, normalized);
    return filepath;
  } catch (e) {
    console.warn(`Failed to download symbol for "${symbol.keyword}": ${e.message}`);
    return null;
  }
}

/**
 * Fetch symbols for a list of words
 * Returns: Map<word, { id, keyword, imageUrl, localPath, source }>
 */
async function fetchSymbols(words, options = {}) {
  const { downloadImages = true, verbose = false, unitName = '', wordTypes = {} } = options;
  // wordTypes: optional map of word → 'core'|'fringe' for library registration
  const results = new Map();
  const library = loadLibrary();
  let cacheHits = 0;

  for (const word of words) {
    if (verbose) process.stdout.write(`Fetching symbol for "${word}"...`);

    // Check cumulative library cache first
    const cached = getCachedSymbol(library, word);
    if (cached) {
      results.set(word, cached);
      if (unitName) registerWord(library, word, cached, wordTypes[word] || 'fringe', unitName);
      cacheHits++;
      if (verbose) console.log(` ✓ cached (${cached.source} #${cached.id})`);
      continue;
    }

    // Try ARASAAC first
    let symbol = await searchArasaac(word);

    // TODO: Mulberry fallback could be added here
    // if (!symbol) symbol = await searchMulberry(word);

    if (symbol) {
      if (downloadImages) {
        symbol.localPath = await downloadSymbol(symbol);
      }
      results.set(word, symbol);
      if (unitName) registerWord(library, word, symbol, wordTypes[word] || 'fringe', unitName);
      if (verbose) console.log(` ✓ (${symbol.source} #${symbol.id})`);
    } else {
      results.set(word, null);
      if (unitName) registerWord(library, word, null, wordTypes[word] || 'fringe', unitName);
      if (verbose) console.log(' ✗ not found');
    }

    // Rate limiting: 200ms between requests
    await new Promise(r => setTimeout(r, 200));
  }

  // Save updated library
  if (unitName) saveLibrary(library);
  if (verbose && cacheHits > 0) {
    console.log(`\nLibrary cache: ${cacheHits}/${words.length} words already cached`);
  }

  return results;
}

// ============================================================
// DOCX INTEGRATION (for use with cbd_docx_template.js)
// ============================================================

/**
 * Build a symbol support page for a CbD unit document.
 * Returns an array of docx elements (Paragraph, Table) ready to spread
 * into a docx document using docx library.
 *
 * This function is designed to work with the existing cbd_docx_template.js
 * design system. Import it alongside your template functions.
 *
 * Usage in a build script:
 *   const { buildSymbolPage } = require('./cbd_symbol_fetcher');
 *   const symbolChildren = await buildSymbolPage({ ... });
 *   // Then in your document children array:
 *   ...symbolChildren,
 */
async function buildSymbolPage(options) {
  const {
    unitTitle = 'Unit',
    unitName = '',          // for library registration (e.g., 'UFLI Unit 4')
    coreWords = [],
    fringeWords = [],
    accessLevel = 'all',    // 'level1', 'level2', 'level3', or 'all' (generates all 3)
    includeTeacherNote = true,
    includeQRCode = true,
  } = options;

  // Lazy-load docx library (same one used by cbd_docx_template.js)
  let docx;
  try {
    docx = require('docx');
  } catch (e) {
    throw new Error('docx package not found. Run: npm install docx');
  }

  const { Paragraph, TextRun, Table, TableRow, TableCell,
          WidthType, AlignmentType, BorderStyle, ImageRun,
          PageBreak, HeadingLevel } = docx;

  // CbD brand colors
  const NAVY = '1B1F3B';
  const TEAL = '006DA0';
  const AMBER = 'FFB703';

  const children = [];

  // Page break before symbol page
  children.push(new Paragraph({ children: [new PageBreak()] }));

  // Title
  children.push(new Paragraph({
    children: [new TextRun({
      text: `Symbol Support — ${unitTitle}`,
      bold: true, font: 'Arial', size: 28, color: TEAL,
    })],
    spacing: { after: 200 },
  }));

  // Teacher Note
  if (includeTeacherNote) {
    children.push(new Paragraph({
      children: [
        new TextRun({
          text: '📋 Teacher Note: ',
          bold: true, font: 'Arial', size: 20, color: NAVY,
        }),
        new TextRun({
          text: 'These are reading response symbols. Print, cut, and use with an e-trans board, choice array, or flip cards so the student can demonstrate reading comprehension. ',
          font: 'Arial', size: 20, color: '333333',
        }),
        new TextRun({
          text: 'If the student has a dedicated AAC system, use those familiar symbols first when possible. ',
          bold: true, font: 'Arial', size: 20, color: NAVY,
        }),
        new TextRun({
          text: 'These open-source symbols (ARASAAC) are a universal backup and work for any student regardless of whether they have a device.',
          font: 'Arial', size: 20, color: '333333',
        }),
      ],
      spacing: { after: 200 },
      border: {
        top: { style: BorderStyle.SINGLE, size: 1, color: AMBER },
        bottom: { style: BorderStyle.SINGLE, size: 1, color: AMBER },
        left: { style: BorderStyle.SINGLE, size: 6, color: AMBER },
        right: { style: BorderStyle.SINGLE, size: 1, color: AMBER },
      },
      indent: { left: 200, right: 200 },
    }));

    children.push(new Paragraph({ spacing: { after: 100 } }));
  }

  // Build word type map for library registration
  const wordTypes = {};
  coreWords.forEach(w => { wordTypes[w] = 'core'; });
  fringeWords.forEach(w => { wordTypes[w] = 'fringe'; });

  // Fetch all symbols (uses cumulative library cache when available)
  const allWords = [...coreWords, ...fringeWords];
  const symbols = await fetchSymbols(allWords, {
    downloadImages: true, verbose: true, unitName, wordTypes,
  });

  // Determine which access levels to generate
  const levels = accessLevel === 'all'
    ? ['level1', 'level2', 'level3']
    : [accessLevel];

  // Content width in DXA (twips) — US Letter with 0.5" margins
  const CONTENT_WIDTH_DXA = 10080;

  // Reusable border style (matches cbd_docx_template.js pattern)
  const thinBorder = { style: BorderStyle.SINGLE, size: 1, color: 'CCCCCC' };
  const cellBorders = { top: thinBorder, bottom: thinBorder, left: thinBorder, right: thinBorder };
  const noBorders = {
    top: { style: BorderStyle.NONE, size: 0 },
    bottom: { style: BorderStyle.NONE, size: 0 },
    left: { style: BorderStyle.NONE, size: 0 },
    right: { style: BorderStyle.NONE, size: 0 },
  };

  // Helper: build a symbol table for a specific access level
  function buildSymbolTable(wordList, sectionTitle, sectionColor, sizing) {
    const sectionChildren = [];
    const { imageWidth, imageHeight, cellPadding, labelSize, maxPerRow } = sizing;
    const colWidthDXA = Math.floor(CONTENT_WIDTH_DXA / maxPerRow);

    sectionChildren.push(new Paragraph({
      children: [new TextRun({
        text: sectionTitle,
        bold: true, font: 'Arial', size: 24, color: sectionColor,
      })],
      spacing: { before: 200, after: 100 },
    }));

    const rows = [];
    for (let i = 0; i < wordList.length; i += maxPerRow) {
      const rowWords = wordList.slice(i, i + maxPerRow);

      const imageCells = rowWords.map(word => {
        const sym = symbols.get(word);
        const cellContent = [];

        if (sym && sym.localPath && fs.existsSync(sym.localPath)) {
          try {
            const imgData = fs.readFileSync(sym.localPath);
            cellContent.push(new Paragraph({
              children: [new ImageRun({
                data: imgData,
                transformation: { width: imageWidth, height: imageHeight },
                type: 'png',
              })],
              alignment: AlignmentType.CENTER,
              spacing: { after: 0 },
            }));
          } catch (e) {
            cellContent.push(new Paragraph({
              children: [new TextRun({ text: '[symbol]', font: 'Arial', size: 18, color: '999999' })],
              alignment: AlignmentType.CENTER,
              spacing: { after: 0 },
            }));
          }
        } else {
          cellContent.push(new Paragraph({
            children: [new TextRun({ text: '[symbol]', font: 'Arial', size: 16, color: '999999', italics: true })],
            alignment: AlignmentType.CENTER,
            spacing: { after: 0 },
          }));
        }

        // Word label below image (size varies by access level)
        cellContent.push(new Paragraph({
          children: [new TextRun({
            text: word,
            bold: true, font: 'Arial', size: labelSize, color: NAVY,
          })],
          alignment: AlignmentType.CENTER,
          spacing: { before: 40, after: 0 },
        }));

        return new TableCell({
          children: cellContent,
          width: { size: colWidthDXA, type: WidthType.DXA },
          borders: cellBorders,
          margins: { top: cellPadding, bottom: cellPadding, left: 50, right: 50 },
        });
      });

      // Pad remaining cells if row is not full
      while (imageCells.length < maxPerRow) {
        imageCells.push(new TableCell({
          children: [new Paragraph({ spacing: { after: 0 } })],
          width: { size: colWidthDXA, type: WidthType.DXA },
          borders: noBorders,
        }));
      }

      rows.push(new TableRow({ children: imageCells }));
    }

    if (rows.length > 0) {
      sectionChildren.push(new Table({
        rows,
        width: { size: CONTENT_WIDTH_DXA, type: WidthType.DXA },
      }));
    } else {
      sectionChildren.push(new Paragraph({
        children: [new TextRun({ text: 'No words in this category.', font: 'Arial', size: 18, italics: true })],
      }));
    }

    return sectionChildren;
  }

  // Generate symbol pages for each access level
  for (const level of levels) {
    const sizing = CONFIG.symbolSizing[level];

    // Level header (only when generating multiple levels)
    if (levels.length > 1) {
      children.push(new Paragraph({
        children: [new TextRun({
          text: sizing.description,
          bold: true, font: 'Arial', size: 22, color: NAVY,
        })],
        spacing: { before: 300, after: 100 },
        border: {
          bottom: { style: BorderStyle.SINGLE, size: 2, color: TEAL },
        },
      }));
    }

    // Core Words section
    if (coreWords.length > 0) {
      children.push(...buildSymbolTable(coreWords,
        'Core Words (high-frequency, used across all contexts)', TEAL, sizing));
    }

    children.push(new Paragraph({ spacing: { after: 200 } }));

    // Fringe Words section
    if (fringeWords.length > 0) {
      children.push(...buildSymbolTable(fringeWords,
        'Fringe Words (lesson-specific vocabulary)', AMBER, sizing));
    }

    // Page break between access levels (when generating all 3)
    if (levels.length > 1 && level !== levels[levels.length - 1]) {
      children.push(new Paragraph({ children: [new PageBreak()] }));
    }
  }

  // QR Code + Resource Link
  if (includeQRCode) {
    children.push(new Paragraph({ spacing: { after: 200 } }));
    children.push(new Paragraph({
      children: [
        new TextRun({
          text: '🔗 Free Symbol Resource: ',
          bold: true, font: 'Arial', size: 18, color: TEAL,
        }),
        new TextRun({
          text: 'Search for additional symbols at ',
          font: 'Arial', size: 18, color: '333333',
        }),
        new TextRun({
          text: 'arasaac.org/pictograms/search',
          font: 'Arial', size: 18, color: TEAL, underline: {},
        }),
        new TextRun({
          text: ' — free, open-source AAC pictograms in 30+ languages. Use these to create custom choice boards, visual supports, or low-tech communication pages.',
          font: 'Arial', size: 18, color: '333333',
        }),
      ],
      spacing: { after: 100 },
    }));

    // QR code generation note
    children.push(new Paragraph({
      children: [new TextRun({
        text: '[QR Code: Scan to open free AAC symbol search]',
        font: 'Arial', size: 16, color: '999999', italics: true,
      })],
      alignment: AlignmentType.CENTER,
      spacing: { after: 100 },
    }));

    // Note: To generate actual QR codes, use the 'qrcode' npm package:
    //   npm install qrcode
    //   const QRCode = require('qrcode');
    //   const qrBuffer = await QRCode.toBuffer(CONFIG.symbolResourceUrl, { width: 150 });
    //   Then use ImageRun with the buffer.
  }

  // Attribution (required by license)
  children.push(new Paragraph({ spacing: { after: 200 } }));
  children.push(new Paragraph({
    children: [new TextRun({
      text: CONFIG.arasaac.attribution,
      font: 'Arial', size: 14, color: '777777', italics: true,
    })],
    spacing: { after: 50 },
  }));
  children.push(new Paragraph({
    children: [new TextRun({
      text: CONFIG.mulberry.attribution,
      font: 'Arial', size: 14, color: '777777', italics: true,
    })],
  }));

  return children;
}

// ============================================================
// STANDALONE QR CODE GENERATOR (for any URL)
// ============================================================

/**
 * Generate a QR code image buffer for embedding in documents.
 * Requires: npm install qrcode
 *
 * Usage:
 *   const qrBuffer = await generateQR('https://arasaac.org/pictograms/search');
 *   // Use with ImageRun in docx
 */
async function generateQR(url, size = 200) {
  try {
    const QRCode = require('qrcode');
    return await QRCode.toBuffer(url, {
      width: size,
      margin: 1,
      color: { dark: '#1B1F3B', light: '#FFFFFF' }, // CbD navy QR codes
    });
  } catch (e) {
    if (e.code === 'MODULE_NOT_FOUND') {
      console.warn('QR code generation requires: npm install qrcode');
      return null;
    }
    throw e;
  }
}

// ============================================================
// CLI TOOL: Fetch symbols for a word list from command line
// ============================================================

async function cli() {
  const args = process.argv.slice(2);

  if (args.length === 0 || args[0] === '--help') {
    console.log(`
Communicate by Design — AAC Symbol Fetcher

Usage:
  node cbd_symbol_fetcher.js <word1> <word2> <word3> ...
  node cbd_symbol_fetcher.js --file wordlist.txt
  node cbd_symbol_fetcher.js --test
  node cbd_symbol_fetcher.js --library

Options:
  --file <path>   Read words from a text file (one per line)
  --test          Test with sample UFLI digraph words
  --library       Show cumulative symbol library summary
  --no-download   Search only, don't download images
  --verbose       Show detailed output
  --unit <name>   Register fetched words under this unit name in the library

Examples:
  node cbd_symbol_fetcher.js read help want more stop go like not
  node cbd_symbol_fetcher.js --unit "UFLI Unit 4" --file ufli_unit4_words.txt
  node cbd_symbol_fetcher.js --library
  node cbd_symbol_fetcher.js --test
`);
    return;
  }

  if (args[0] === '--library') {
    printLibrarySummary();
    return;
  }

  let words;
  const verbose = args.includes('--verbose');
  const download = !args.includes('--no-download');

  if (args[0] === '--test') {
    words = [
      // Core words for UFLI
      'read', 'help', 'want', 'more', 'stop', 'go', 'like', 'not',
      'yes', 'no', 'look', 'this', 'that', 'good', 'again',
      // Fringe words for digraphs unit
      'ship', 'shop', 'fish', 'chin', 'think', 'white', 'phone',
    ];
    console.log('Testing with sample UFLI digraph words...\n');
  } else if (args[0] === '--file') {
    const filepath = args[1];
    if (!filepath || !fs.existsSync(filepath)) {
      console.error('File not found:', filepath);
      process.exit(1);
    }
    words = fs.readFileSync(filepath, 'utf8')
      .split('\n')
      .map(w => w.trim())
      .filter(w => w.length > 0 && !w.startsWith('#'));
  } else {
    words = args.filter(a => !a.startsWith('--'));
  }

  // Check for --unit flag
  const unitIdx = args.indexOf('--unit');
  const unitName = unitIdx !== -1 && args[unitIdx + 1] ? args[unitIdx + 1] : '';

  console.log(`Fetching symbols for ${words.length} words...`);
  if (unitName) console.log(`Registering under unit: ${unitName}`);
  console.log(`Cache directory: ${CONFIG.cacheDir}\n`);

  const results = await fetchSymbols(words, { downloadImages: download, verbose: true, unitName });

  // Summary
  const found = [...results.values()].filter(v => v !== null).length;
  const notFound = [...results.entries()].filter(([k, v]) => v === null).map(([k]) => k);

  console.log(`\n=== Summary ===`);
  console.log(`Found: ${found}/${words.length}`);
  if (notFound.length > 0) {
    console.log(`Not found: ${notFound.join(', ')}`);
  }
  if (download) {
    console.log(`Images cached in: ${CONFIG.cacheDir}`);
  }

  console.log(`\nAttribution (include in all products):`);
  console.log(CONFIG.arasaac.attribution);
}

// Run CLI if called directly
if (require.main === module) {
  cli().catch(console.error);
}

// ============================================================
// EXPORTS
// ============================================================

module.exports = {
  fetchSymbols,
  buildSymbolPage,
  searchArasaac,
  downloadSymbol,
  normalizeSymbol,
  generateQR,
  loadLibrary,
  saveLibrary,
  registerWord,
  getCachedSymbol,
  printLibrarySummary,
  CONFIG,
  NORM_CANVAS,
  NORM_CONTENT,
};

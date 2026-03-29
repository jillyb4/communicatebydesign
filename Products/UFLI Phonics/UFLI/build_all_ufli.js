#!/usr/bin/env node
/**
 * UFLI Batch Builder — Communicate by Design
 *
 * Generates all per-lesson packets from ufli_lesson_configs.js.
 *
 * Usage:
 *   node build_all_ufli.js              # Build all lessons with word lists
 *   node build_all_ufli.js --all        # Build ALL lessons (including empty configs — for testing)
 *   node build_all_ufli.js --range 1 10 # Build lessons 1–10 only
 *   node build_all_ufli.js --lesson 23  # Build a single lesson
 */

const path = require('path');
const fs = require('fs');
const { buildPacket } = require('./build_ufli_packet');

const OUTPUT_DIR = path.join(__dirname, 'Output');

async function main() {
  const args = process.argv.slice(2);
  const configs = require('./ufli_lesson_configs');

  fs.mkdirSync(OUTPUT_DIR, { recursive: true });

  let toBuild = [];

  if (args.includes('--all')) {
    // Build everything, even empty configs (for testing layout)
    toBuild = configs;
  } else if (args.includes('--range')) {
    const rangeIdx = args.indexOf('--range');
    const start = parseInt(args[rangeIdx + 1]);
    const end = parseInt(args[rangeIdx + 2]);
    toBuild = configs.filter(c => c.number >= start && c.number <= end);
  } else if (args.includes('--lesson')) {
    const lessonIdx = args.indexOf('--lesson');
    const num = parseInt(args[lessonIdx + 1]);
    toBuild = configs.filter(c => c.number === num);
  } else {
    // Default: only build lessons that have word lists populated
    toBuild = configs.filter(c => c.newWords.length > 0);
  }

  if (toBuild.length === 0) {
    console.log('No lessons to build.');
    console.log('  - Use --all to build all lessons (including empty configs)');
    console.log('  - Use --lesson 23 to build a specific lesson');
    console.log('  - Or populate word lists in ufli_lesson_configs.js');
    return;
  }

  console.log(`\n═══════════════════════════════════════════════════`);
  console.log(`  COMMUNICATE BY DESIGN — UFLI Batch Builder`);
  console.log(`  Building ${toBuild.length} lesson packet(s)...`);
  console.log(`  Output: ${OUTPUT_DIR}`);
  console.log(`═══════════════════════════════════════════════════\n`);

  const results = { success: [], skipped: [], failed: [] };

  for (const config of toBuild) {
    const hasWords = config.newWords.length > 0;
    console.log(`\nLesson ${config.number}: ${config.phoneme} (${config.grapheme})${hasWords ? '' : ' [empty config — layout only]'}`);

    try {
      await buildPacket(config, OUTPUT_DIR);
      results.success.push(config.number);
    } catch (err) {
      console.error(`  ❌ FAILED: ${err.message}`);
      results.failed.push({ number: config.number, error: err.message });
    }
  }

  // ── Summary ──────────────────────────────────────────────
  console.log(`\n═══════════════════════════════════════════════════`);
  console.log(`  BUILD SUMMARY`);
  console.log(`═══════════════════════════════════════════════════`);
  console.log(`  ✅ Success: ${results.success.length} lessons`);
  if (results.failed.length > 0) {
    console.log(`  ❌ Failed:  ${results.failed.length} lessons`);
    results.failed.forEach(f => console.log(`     Lesson ${f.number}: ${f.error}`));
  }

  // Count populated vs empty
  const populated = configs.filter(c => c.newWords.length > 0).length;
  const empty = configs.length - populated;
  console.log(`\n  Config status: ${populated}/34 lessons have word lists`);
  if (empty > 0) console.log(`  ⬜ ${empty} lessons still need word lists from UFLI manual`);

  console.log(`\n  Output directory: ${OUTPUT_DIR}`);
  console.log(`═══════════════════════════════════════════════════\n`);
}

main().catch(err => { console.error('❌ Fatal:', err.message); process.exit(1); });

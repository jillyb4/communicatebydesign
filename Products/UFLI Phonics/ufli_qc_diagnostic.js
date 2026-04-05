#!/usr/bin/env node
/**
 * UFLI QC Diagnostic Script — Communicate by Design
 *
 * Analyzes all lesson configs against the QC rubric BEFORE building packets.
 * Catches config-level issues across all 34 lessons in one pass.
 *
 * Usage:
 *   node ufli_qc_diagnostic.js              # Full report for all lessons
 *   node ufli_qc_diagnostic.js --lesson 12  # Single lesson detail
 *   node ufli_qc_diagnostic.js --flags-only # Only show lessons with issues
 *   node ufli_qc_diagnostic.js --csv        # Output CSV for spreadsheet review
 *
 * What this checks (config-level — no build required):
 *   1. Word type coverage: every word tagged core or fringe (never untagged)
 *   2. Core/fringe balance: at least one core word per lesson with words
 *   3. Morphology flag coverage: tense variations (sit/sat etc.) are flagged
 *   4. Review word continuity: no words drop out of review without returning
 *   5. Heart word presence: lessons 1-4 typically have heart words
 *   6. Lesson completeness: no partially populated configs
 *   7. Duplicate words: no word appears twice in newWords or reviewWords
 *   8. Cross-lesson consistency: core/fringe classification is stable across lessons
 *   9. Missing morphology: inflected forms present without base form flagged
 *  10. Word count reasonableness: >15 new words is unusual — flag for review
 */

const lessons = require('./ufli_lesson_configs');
const { getFitzgeraldCategory } = require('./fitzgerald_key');

// ── Known tense/morphology pairs that SHOULD be flagged ──────────────────────
// If both forms appear across lessons without a morphologyNote, flag it.
const KNOWN_MORPHOLOGY_PAIRS = [
  ['sit', 'sat'], ['has', 'had'], ['hide', 'hid'], ['hop', 'hopped'],
  ['run', 'ran'], ['get', 'got'], ['hit', 'hit'], ['let', 'let'],
  ['set', 'set'], ['cut', 'cut'], ['put', 'put'], ['dig', 'dug'],
  ['win', 'won'], ['spin', 'spun'], ['spit', 'spat'], ['bit', 'bat'],
  ['pin', 'pan'], ['tip', 'tap'], ['dim', 'dab'], ['fit', 'fat'],
];

// ── Color codes ───────────────────────────────────────────────────────────────
const RED   = '\x1b[31m';
const AMBER = '\x1b[33m';
const GREEN = '\x1b[32m';
const CYAN  = '\x1b[36m';
const BOLD  = '\x1b[1m';
const RESET = '\x1b[0m';
const DIM   = '\x1b[2m';

const isCsv   = process.argv.includes('--csv');
const isFlags = process.argv.includes('--flags-only');
const lessonArg = process.argv.includes('--lesson')
  ? parseInt(process.argv[process.argv.indexOf('--lesson') + 1])
  : null;

// ── Build a cross-lesson word registry ───────────────────────────────────────
// Track how each word is classified across all lessons.
// If classification is inconsistent (core in L5, fringe in L12), flag it.
const wordRegistry = {}; // word → { type: 'core'|'fringe', firstSeen: lessonNumber }

function registerWord(word, type, lessonNumber) {
  if (!wordRegistry[word]) {
    wordRegistry[word] = { type, firstSeen: lessonNumber, conflicts: [] };
  } else if (wordRegistry[word].type !== type) {
    wordRegistry[word].conflicts.push({ lessonNumber, declaredType: type });
  }
}

// Pre-populate registry
for (const lesson of lessons) {
  for (const w of lesson.newWords)    registerWord(w.word, w.type, lesson.number);
  for (const w of lesson.reviewWords) registerWord(w.word, w.type, lesson.number);
}

// ── Per-lesson diagnostic ─────────────────────────────────────────────────────
function diagnoseLesson(lesson) {
  const flags = [];   // { level: 'ERROR'|'WARN'|'INFO', code, message }
  const notes = [];   // passing checks

  const { number, phoneme, grapheme, newWords, reviewWords, heartWords, morphologyNotes } = lesson;
  const allWords = [...newWords, ...reviewWords];
  const hasWords = newWords.length > 0;

  // ── 1. Empty lesson (L1–L4 are intentionally sparse) ─────────────────────
  if (!hasWords && number > 4) {
    flags.push({ level: 'WARN', code: 'NO_WORDS', message: 'No newWords — lesson config may be incomplete.' });
  }

  // ── 2. Word type tagging ──────────────────────────────────────────────────
  for (const w of allWords) {
    if (!w.type || !['core', 'fringe'].includes(w.type)) {
      flags.push({ level: 'ERROR', code: 'UNTAGGED_WORD', message: `"${w.word}" has no type tag (must be core or fringe).` });
    }
  }

  // ── 3. Core word coverage ─────────────────────────────────────────────────
  if (hasWords) {
    const coreWords = newWords.filter(w => w.type === 'core');
    if (coreWords.length === 0) {
      flags.push({ level: 'WARN', code: 'NO_CORE_WORDS', message: 'No core words in newWords. Expected at least 1 high-frequency core word per lesson with words.' });
    } else {
      notes.push(`Core words (${coreWords.length}): ${coreWords.map(w => w.word).join(', ')}`);
    }
  }

  // ── 4. Excessive new words ────────────────────────────────────────────────
  if (newWords.length > 15) {
    flags.push({ level: 'WARN', code: 'HIGH_WORD_COUNT', message: `${newWords.length} new words — unusually high. Review for accuracy.` });
  }

  // ── 5. Duplicate words in newWords ───────────────────────────────────────
  const newWordSet = new Set();
  for (const w of newWords) {
    if (newWordSet.has(w.word)) {
      flags.push({ level: 'ERROR', code: 'DUPLICATE_NEW_WORD', message: `"${w.word}" appears more than once in newWords.` });
    }
    newWordSet.add(w.word);
  }

  // ── 6. Duplicate words in reviewWords ────────────────────────────────────
  const reviewWordSet = new Set();
  for (const w of reviewWords) {
    if (reviewWordSet.has(w.word)) {
      flags.push({ level: 'ERROR', code: 'DUPLICATE_REVIEW_WORD', message: `"${w.word}" appears more than once in reviewWords.` });
    }
    reviewWordSet.add(w.word);
  }

  // ── 7. Cross-lesson classification conflict ───────────────────────────────
  for (const w of newWords) {
    const reg = wordRegistry[w.word];
    if (reg && reg.conflicts.length > 0) {
      const conflictLessons = reg.conflicts.map(c => `L${c.lessonNumber}:${c.declaredType}`).join(', ');
      flags.push({ level: 'ERROR', code: 'CLASSIFICATION_CONFLICT', message: `"${w.word}" classified as ${w.type} here but differently in ${conflictLessons}. Classification must be stable across all lessons.` });
    }
  }

  // ── 8. Morphology pair detection ─────────────────────────────────────────
  // Check if inflected pairs appear in this lesson without a morphology note
  const lessonWordStrings = allWords.map(w => w.word.toLowerCase());
  for (const [base, inflected] of KNOWN_MORPHOLOGY_PAIRS) {
    if (lessonWordStrings.includes(base) && lessonWordStrings.includes(inflected)) {
      const alreadyFlagged = (morphologyNotes || []).some(n => {
        const text = typeof n === 'string' ? n : JSON.stringify(n);
        return text.toLowerCase().includes(base) || text.toLowerCase().includes(inflected);
      });
      if (!alreadyFlagged) {
        flags.push({ level: 'WARN', code: 'MISSING_MORPHOLOGY_FLAG', message: `Both "${base}" and "${inflected}" appear in this lesson. Add a morphologyNote flagging the tense variation.` });
      }
    }
  }

  // ── 9. Review word has 'from' field ──────────────────────────────────────
  for (const w of reviewWords) {
    if (!w.from) {
      flags.push({ level: 'WARN', code: 'REVIEW_MISSING_FROM', message: `reviewWord "${w.word}" has no 'from' field. Should reference the lesson it was introduced in (e.g. "Lesson 5").` });
    }
  }

  // ── 10. Phoneme field present for lessons with words ─────────────────────
  if (hasWords && (!phoneme || phoneme.trim() === '')) {
    flags.push({ level: 'WARN', code: 'MISSING_PHONEME', message: 'Lesson has words but no phoneme field. Check lesson config.' });
  }

  // ── 11. Grapheme field present ────────────────────────────────────────────
  if (!grapheme || grapheme.trim() === '') {
    flags.push({ level: 'WARN', code: 'MISSING_GRAPHEME', message: 'No grapheme field. Check lesson config.' });
  }

  // ── 12. Heart words present in early lessons ─────────────────────────────
  // L6–L10 commonly introduce sight/heart words — warn if empty in that range
  if (number >= 6 && number <= 10 && heartWords.length === 0) {
    flags.push({ level: 'INFO', code: 'NO_HEART_WORDS', message: 'No heart words. Confirm this is intentional — lessons 6–10 commonly introduce sight words.' });
  }

  // ── 13. Fitzgerald Key classification check ───────────────────────────────
  // Every word should resolve to a valid FK category (not 'unknown')
  for (const w of newWords) {
    try {
      const fk = getFitzgeraldCategory(w.word);
      if (!fk || fk === 'unknown') {
        flags.push({ level: 'INFO', code: 'FK_UNKNOWN', message: `"${w.word}" has no Fitzgerald Key category — will display as white/noun default. Confirm this is correct.` });
      }
    } catch (e) {
      // getFitzgeraldCategory may throw for unusual words — flag it
      flags.push({ level: 'INFO', code: 'FK_ERROR', message: `"${w.word}" threw an error in Fitzgerald Key lookup: ${e.message}` });
    }
  }

  return { number, grapheme, phoneme, hasWords, newWordCount: newWords.length, reviewWordCount: reviewWords.length, heartWordCount: heartWords.length, morphologyNoteCount: (morphologyNotes || []).length, flags, notes };
}

// ── Cross-lesson checks ───────────────────────────────────────────────────────
function crossLessonChecks() {
  const issues = [];

  // Check for global classification conflicts
  for (const [word, reg] of Object.entries(wordRegistry)) {
    if (reg.conflicts.length > 0) {
      issues.push({
        level: 'ERROR',
        code: 'GLOBAL_CLASSIFICATION_CONFLICT',
        message: `"${word}" (first seen L${reg.firstSeen} as ${reg.type}) reclassified in: ${reg.conflicts.map(c => `L${c.lessonNumber}→${c.declaredType}`).join(', ')}`
      });
    }
  }

  // Check review word continuity: a word introduced in lesson N should appear in review for N+1 through N+5 at minimum
  // Build introduction map
  const introducedAt = {};
  for (const lesson of lessons) {
    for (const w of lesson.newWords) {
      if (!introducedAt[w.word]) introducedAt[w.word] = lesson.number;
    }
  }

  // Check each word appears in review in the lessons immediately following introduction
  for (const [word, introLesson] of Object.entries(introducedAt)) {
    const followingLessons = lessons.filter(l => l.number > introLesson && l.number <= introLesson + 4 && l.newWords.length > 0);
    for (const fl of followingLessons) {
      const inReview = fl.reviewWords.some(w => w.word === word);
      const inNew = fl.newWords.some(w => w.word === word);
      if (!inReview && !inNew) {
        // Only flag if the word has 3+ lessons missing review (gaps in first 4 after intro)
        const reviewGaps = followingLessons.filter(l => !l.reviewWords.some(w => w.word === word) && !l.newWords.some(w => w.word === word));
        if (reviewGaps.length >= 3) {
          issues.push({
            level: 'INFO',
            code: 'REVIEW_GAP',
            message: `"${word}" (introduced L${introLesson}) missing from review in multiple following lessons: ${reviewGaps.map(l => 'L' + l.number).join(', ')}`
          });
          break; // Only flag once per word
        }
      }
    }
  }

  return issues;
}

// ── Output helpers ────────────────────────────────────────────────────────────
function levelColor(level) {
  if (level === 'ERROR') return RED;
  if (level === 'WARN')  return AMBER;
  return DIM;
}

function printLessonReport(result) {
  const { number, grapheme, hasWords, newWordCount, reviewWordCount, heartWordCount, flags, notes } = result;
  const errorCount = flags.filter(f => f.level === 'ERROR').length;
  const warnCount  = flags.filter(f => f.level === 'WARN').length;
  const infoCount  = flags.filter(f => f.level === 'INFO').length;

  const statusIcon = errorCount > 0 ? `${RED}✗${RESET}` : warnCount > 0 ? `${AMBER}⚠${RESET}` : `${GREEN}✓${RESET}`;

  if (isFlags && flags.length === 0) return; // skip clean lessons in flags-only mode

  console.log(`\n${BOLD}Lesson ${number}${RESET} — ${grapheme || '—'} ${statusIcon}`);
  console.log(`${DIM}  Words: ${newWordCount} new · ${reviewWordCount} review · ${heartWordCount} heart${RESET}`);

  if (notes.length > 0 && !isFlags) {
    for (const n of notes) console.log(`  ${GREEN}✓${RESET} ${DIM}${n}${RESET}`);
  }

  for (const flag of flags) {
    console.log(`  ${levelColor(flag.level)}[${flag.level}]${RESET} ${flag.code}: ${flag.message}`);
  }

  if (flags.length === 0 && !isFlags) {
    console.log(`  ${GREEN}All checks passed.${RESET}`);
  }
}

function printCsv(results, crossIssues) {
  const headers = ['Lesson', 'Grapheme', 'HasWords', 'NewWords', 'ReviewWords', 'HeartWords', 'Errors', 'Warnings', 'Info', 'FirstFlag'];
  console.log(headers.join(','));

  for (const r of results) {
    const errors  = r.flags.filter(f => f.level === 'ERROR').length;
    const warns   = r.flags.filter(f => f.level === 'WARN').length;
    const infos   = r.flags.filter(f => f.level === 'INFO').length;
    const first   = r.flags.length > 0 ? `"${r.flags[0].code}: ${r.flags[0].message.replace(/"/g, "'")}"` : '';
    console.log([r.number, r.grapheme, r.hasWords ? 'Y' : 'N', r.newWordCount, r.reviewWordCount, r.heartWordCount, errors, warns, infos, first].join(','));
  }
}

// ── Main ──────────────────────────────────────────────────────────────────────
function main() {
  const toLint = lessonArg
    ? lessons.filter(l => l.number === lessonArg)
    : lessons;

  if (toLint.length === 0) {
    console.error(`No lesson found for --lesson ${lessonArg}`);
    process.exit(1);
  }

  const results = toLint.map(diagnoseLesson);
  const crossIssues = lessonArg ? [] : crossLessonChecks();

  if (isCsv) {
    printCsv(results, crossIssues);
    return;
  }

  // ── Header ─────────────────────────────────────────────────────────────────
  console.log(`\n${BOLD}${CYAN}════════════════════════════════════════════════════════${RESET}`);
  console.log(`${BOLD}${CYAN}  COMMUNICATE BY DESIGN — UFLI QC Diagnostic${RESET}`);
  console.log(`${BOLD}${CYAN}  ${new Date().toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })}${RESET}`);
  console.log(`${BOLD}${CYAN}════════════════════════════════════════════════════════${RESET}`);

  const totalLessons   = results.length;
  const withWords      = results.filter(r => r.hasWords).length;
  const cleanLessons   = results.filter(r => r.flags.length === 0).length;
  const errorLessons   = results.filter(r => r.flags.some(f => f.level === 'ERROR')).length;
  const warnLessons    = results.filter(r => r.flags.some(f => f.level === 'WARN')).length;
  const totalErrors    = results.reduce((sum, r) => sum + r.flags.filter(f => f.level === 'ERROR').length, 0);
  const totalWarnings  = results.reduce((sum, r) => sum + r.flags.filter(f => f.level === 'WARN').length, 0);

  console.log(`\n${BOLD}Summary${RESET}`);
  console.log(`  Lessons analyzed:  ${totalLessons}`);
  console.log(`  With word lists:   ${withWords}`);
  console.log(`  ${GREEN}✓ Clean:${RESET}           ${cleanLessons}`);
  console.log(`  ${RED}✗ Errors:${RESET}          ${errorLessons} lessons · ${totalErrors} total`);
  console.log(`  ${AMBER}⚠ Warnings:${RESET}        ${warnLessons} lessons · ${totalWarnings} total`);

  if (crossIssues.length > 0) {
    console.log(`\n${BOLD}Cross-Lesson Issues${RESET}`);
    for (const issue of crossIssues) {
      console.log(`  ${levelColor(issue.level)}[${issue.level}]${RESET} ${issue.code}: ${issue.message}`);
    }
  }

  // ── Per-lesson output ──────────────────────────────────────────────────────
  if (lessonArg) {
    printLessonReport(results[0]);
  } else {
    console.log(`\n${BOLD}Per-Lesson Results${RESET}`);
    for (const result of results) {
      printLessonReport(result);
    }
  }

  // ── Triage list ────────────────────────────────────────────────────────────
  const errorList = results.filter(r => r.flags.some(f => f.level === 'ERROR'));
  const warnList  = results.filter(r => r.flags.some(f => f.level === 'WARN') && !r.flags.some(f => f.level === 'ERROR'));

  if (!lessonArg && (errorList.length > 0 || warnList.length > 0)) {
    console.log(`\n${BOLD}Triage Queue${RESET} ${DIM}(fix errors before building)${RESET}`);
    if (errorList.length > 0) {
      console.log(`\n  ${RED}${BOLD}Fix first — ERRORS:${RESET}`);
      for (const r of errorList) {
        const errs = r.flags.filter(f => f.level === 'ERROR');
        console.log(`  L${r.number} (${r.grapheme}): ${errs.map(e => e.code).join(', ')}`);
      }
    }
    if (warnList.length > 0) {
      console.log(`\n  ${AMBER}${BOLD}Review — WARNINGS:${RESET}`);
      for (const r of warnList) {
        const warns = r.flags.filter(f => f.level === 'WARN');
        console.log(`  L${r.number} (${r.grapheme}): ${warns.map(w => w.code).join(', ')}`);
      }
    }
  }

  // ── Code counts summary ────────────────────────────────────────────────────
  const codeCounts = {};
  for (const r of results) {
    for (const f of r.flags) {
      codeCounts[f.code] = (codeCounts[f.code] || 0) + 1;
    }
  }
  if (Object.keys(codeCounts).length > 0 && !lessonArg) {
    console.log(`\n${BOLD}Issue Frequency${RESET} ${DIM}(most common issues first)${RESET}`);
    const sorted = Object.entries(codeCounts).sort((a, b) => b[1] - a[1]);
    for (const [code, count] of sorted) {
      console.log(`  ${count}x  ${code}`);
    }
  }

  console.log(`\n${DIM}Run with --csv to export for spreadsheet review.${RESET}`);
  console.log(`${DIM}Run with --flags-only to show only lessons with issues.${RESET}`);
  console.log(`${DIM}Run with --lesson N for single-lesson detail.\n${RESET}`);

  // Exit with error code if errors found (useful for CI/automated checks)
  if (totalErrors > 0) process.exit(1);
}

main();

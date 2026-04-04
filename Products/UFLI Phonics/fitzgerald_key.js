/**
 * Fitzgerald Key Classification — UFLI Words
 *
 * Standard AAC color-coding system for grammatical function.
 * Used by TD Snap, LAMP/Unity, Proloquo2Go, TouchChat, and most AAC systems.
 *
 * Categories:
 *   yellow  — People / Pronouns (I, you, he, she, we, they, it)
 *   green   — Verbs / Actions (go, want, sit, run, hit)
 *   orange  — Adjectives / Descriptions (big, hot, wet, more)
 *   blue    — Prepositions / Time / Places (in, on, at, up)
 *   pink    — Questions / Social / Feelings (hi, yes, no, what)
 *   white   — Nouns (cat, cup, bed, map) — DEFAULT for unclassified words
 *
 * Source: Fitzgerald (1949), adapted by Goossens', Crain, & Elder (1992)
 * Standard in U.S. AAC practice. Matches device color-coding.
 *
 * Words with dual function (e.g., "tap" = verb or noun) are classified
 * by most common AAC usage for complex communicators.
 */

const FITZGERALD = {
  // ── YELLOW: People / Pronouns / Names ──
  yellow: new Set([
    'him', 'his', 'us', 'it', 'me',
    // Names from UFLI (proper nouns used as people references)
    'pam', 'dan', 'ben', 'sam', 'nat', 'jan', 'jim', 'jon', 'tim', 'tom',
    'kim', 'ken', 'meg', 'lex', 'wes', 'vin', 'ed', 'zak', 'pim', 'quin',
  ]),

  // ── GREEN: Verbs / Actions ──
  green: new Set([
    'am', 'ask', 'ban', 'bat', 'beg', 'bet', 'bid', 'bit', 'bled', 'brag',
    'bud', 'can', 'cap', 'clap', 'clog', 'clop', 'clot', 'con', 'cop', 'crab',
    'crop', 'cut', 'dab', 'did', 'dig', 'digs', 'dim', 'dip', 'drip', 'drips',
    'drop', 'dub', 'dug', 'end', 'fad', 'fan', 'fed', 'fend', 'fib', 'fit',
    'fix', 'flag', 'fled', 'flip', 'flop', 'fun', 'gab', 'gag', 'get', 'gets',
    'got', 'grab', 'grip', 'grips', 'had', 'has', 'held', 'help', 'hid', 'hint',
    'hit', 'hop', 'hug', 'hum', 'hunt', 'jab', 'jabs', 'jam', 'jest', 'jig',
    'jilt', 'jog', 'jot', 'jots', 'jut', 'kept', 'kid', 'kip', 'lag', 'lap',
    'led', 'lend', 'let', 'lift', 'limp', 'lit', 'log', 'lug', 'lump', 'met',
    'mix', 'mob', 'mop', 'mops', 'nab', 'nag', 'nags', 'nap', 'naps', 'nip',
    'nix', 'nod', 'pad', 'pan', 'pat', 'pats', 'peg', 'pet', 'pin', 'pins',
    'pit', 'pled', 'plop', 'plot', 'plug', 'pop', 'pops', 'prep', 'prod',
    'prop', 'pun', 'puns', 'quit', 'quits', 'quiz', 'ram', 'ramp', 'ran',
    'rant', 'rap', 'raps', 'rest', 'rid', 'rim', 'rip', 'run', 'runs', 'rut',
    'sag', 'sags', 'sat', 'scan', 'set', 'sets', 'sip', 'sit', 'skid', 'skim',
    'skin', 'skip', 'skit', 'slap', 'sled', 'slid', 'slip', 'slot', 'snub',
    'sob', 'sop', 'spam', 'span', 'stub', 'sub', 'sum', 'swag', 'swig',
    'tag', 'tags', 'tan', 'tap', 'taps', 'tend', 'tip', 'top', 'tops', 'tot',
    'tots', 'trap', 'trim', 'trip', 'trips', 'tug', 'tugs', 'wag', 'wax',
    'wed', 'weld', 'welt', 'went', 'wept', 'wilt', 'win', 'yap', 'yelp',
    'yip', 'zap', 'zaps', 'zip', 'zips',
  ]),

  // ── ORANGE: Adjectives / Descriptions ──
  orange: new Set([
    'bad', 'best', 'big', 'fat', 'flat', 'grim', 'hot', 'just', 'lax', 'left',
    'mad', 'max', 'mod', 'next', 'not', 'odd', 'prim', 'red', 'sad', 'six',
    'slim', 'snug', 'vast', 'wet',
  ]),

  // ── BLUE: Prepositions / Time / Location ──
  blue: new Set([
    'an', 'as', 'at', 'but', 'if', 'in', 'on', 'up', 'un', 'um', 'yet',
  ]),

  // ── PINK: Social / Questions / Feelings / Interjections ──
  pink: new Set([
    'yes', 'yep', 'yup', 'yum',
  ]),
};

// Everything not classified above defaults to 'white' (Noun)

// ── GENERAL ENGLISH VOCABULARY (extends UFLI sets for nonfiction/fiction) ──
// Common AAC vocabulary that appears across CbD product lines.
// Same Fitzgerald Key categories, broader word coverage.
const GENERAL = {
  yellow: new Set([
    // Pronouns and people-reference words
    'i', 'you', 'he', 'she', 'we', 'they', 'my', 'your', 'our', 'their',
    'who', 'someone', 'everyone', 'people', 'human',
  ]),
  green: new Set([
    // Common verbs across nonfiction units
    'think', 'feel', 'know', 'want', 'need', 'help', 'stop', 'fight', 'change',
    'show', 'prove', 'mean', 'say', 'tell', 'believe', 'make', 'do', 'go', 'get',
    'give', 'like', 'live', 'care', 'move', 'swim', 'learn', 'die', 'protect',
    'paint', 'lie', 'approve', 'deny', 'claim', 'review', 'test', 'occupy',
    'demand', 'sign', 'agree', 'disagree', 'crawl', 'protest', 'verify',
    'corroborate', 'organize', 'contradict', 'cause', 'read', 'write',
    'work', 'use', 'find', 'try', 'put', 'take', 'see', 'look', 'hear',
    'play', 'come', 'turn', 'open', 'close', 'start', 'begin', 'finish',
    'keep', 'bring', 'send', 'build', 'break', 'grow', 'eat', 'drink',
    'sleep', 'walk', 'stand', 'sit', 'wait', 'watch', 'listen', 'talk',
    'speak', 'ask', 'answer', 'explain', 'describe', 'compare', 'analyze',
    'evaluate', 'identify', 'observe', 'support', 'include', 'follow',
    'choose', 'decide', 'create', 'share', 'connect', 'push', 'pull',
  ]),
  orange: new Set([
    // Adjectives/descriptions across nonfiction units
    'good', 'bad', 'right', 'wrong', 'different', 'same', 'more', 'less',
    'true', 'false', 'strong', 'weak', 'big', 'small', 'little', 'free',
    'safe', 'sick', 'healthy', 'wild', 'dangerous', 'reliable', 'accessible',
    'new', 'old', 'important', 'best', 'hard', 'easy', 'long', 'short',
    'fast', 'slow', 'happy', 'sad', 'angry', 'afraid', 'sure', 'ready',
    'able', 'enough', 'many', 'few', 'all', 'some', 'every', 'each',
  ]),
  blue: new Set([
    // Prepositions, time, location, conjunctions
    'because', 'before', 'after', 'then', 'first', 'last', 'but', 'if',
    'about', 'and', 'that', 'which', 'when', 'where', 'today', 'now',
    'here', 'there', 'in', 'on', 'at', 'up', 'down', 'to', 'from',
    'with', 'for', 'of', 'by', 'into', 'out', 'over', 'under', 'between',
    'through', 'during', 'until', 'while', 'also', 'too', 'next', 'again',
    'still', 'already', 'always', 'never', 'sometimes', 'or', 'so',
  ]),
  pink: new Set([
    // Social, feelings, questions, interjections
    'yes', 'no', 'please', 'thank', 'sorry', 'hi', 'hello', 'bye',
    'why', 'what', 'how', 'question', 'okay', 'wow',
  ]),
};

/**
 * Get the Fitzgerald Key category for a word.
 * Checks UFLI-specific sets first, then general English vocabulary.
 * @param {string} word
 * @returns {{ category: string, color: string, label: string }}
 */
function getFitzgeraldCategory(word) {
  const w = word.toLowerCase();
  // Check UFLI-specific sets first (curated for those 458 words)
  if (FITZGERALD.yellow.has(w)) return { category: 'yellow', color: 'FFD700', label: 'People' };
  if (FITZGERALD.green.has(w))  return { category: 'green',  color: '00A86B', label: 'Actions' };
  if (FITZGERALD.orange.has(w)) return { category: 'orange', color: 'FF8C00', label: 'Descriptions' };
  if (FITZGERALD.blue.has(w))   return { category: 'blue',   color: '4A90D9', label: 'Prepositions' };
  if (FITZGERALD.pink.has(w))   return { category: 'pink',   color: 'E88CA5', label: 'Social' };
  // Check general English vocabulary (for nonfiction/fiction units)
  if (GENERAL.yellow.has(w)) return { category: 'yellow', color: 'FFD700', label: 'People' };
  if (GENERAL.green.has(w))  return { category: 'green',  color: '00A86B', label: 'Actions' };
  if (GENERAL.orange.has(w)) return { category: 'orange', color: 'FF8C00', label: 'Descriptions' };
  if (GENERAL.blue.has(w))   return { category: 'blue',   color: '4A90D9', label: 'Prepositions' };
  if (GENERAL.pink.has(w))   return { category: 'pink',   color: 'E88CA5', label: 'Social' };
  return { category: 'white', color: '8B6914', label: 'Nouns' };
}

/**
 * Group an array of review word objects by Fitzgerald category.
 * @param {Array<{word: string, from: string, type: string}>} reviewWords
 * @returns {Object} Grouped by category label, sorted by display order
 */
function groupByFitzgerald(reviewWords) {
  const order = ['People', 'Actions', 'Descriptions', 'Nouns', 'Prepositions', 'Social'];
  const groups = {};
  for (const rw of reviewWords) {
    const fitz = getFitzgeraldCategory(rw.word);
    if (!groups[fitz.label]) groups[fitz.label] = { color: fitz.color, category: fitz.category, words: [] };
    groups[fitz.label].words.push(rw);
  }
  // Sort groups by display order, only include non-empty groups
  const result = [];
  for (const label of order) {
    if (groups[label]) {
      groups[label].words.sort((a, b) => a.word.localeCompare(b.word));
      result.push({ label, ...groups[label] });
    }
  }
  return result;
}

module.exports = { getFitzgeraldCategory, groupByFitzgerald, FITZGERALD };

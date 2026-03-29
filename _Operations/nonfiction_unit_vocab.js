/**
 * Nonfiction Unit Vocabulary Configs — Communicate by Design
 * Updated: 2026-03-29 (Vocabulary Framework v1.0 alignment)
 *
 * TWO-DIMENSION CLASSIFICATION (required on every word):
 *   type:          'core' | 'fringe' | 'heart'
 *                  AAC Access Layer — does the student already have this word?
 *                  core   = already on most robust AAC systems
 *                  fringe = NOT pre-programmed; SLP must add 1–2 weeks before unit
 *                  heart  = irregular high-frequency phonics word (UFLI context only)
 *
 *   instructional: 'explicit' | 'background' | 'generative'
 *                  Instructional Layer — what role does this word play in the lesson?
 *                  explicit    = Tier 2 academic word OR thematically central Tier 3;
 *                                taught directly; appears in 3+ activities; Word Bank target
 *                  background  = needed to access the text but not the instructional focus;
 *                                brief definition in Vocabulary Reference only
 *                  generative  = student uses this word to BUILD a response (sentence frames,
 *                                communication board, evidence statements)
 *
 *   top5:          true | false
 *                  Marks Top 5 Core (highest-priority response/generative core words) OR
 *                  Top 5 Fringe (fringe words that are both explicit targets AND critical
 *                  for student response). Used by build_all_units.py Top 5 callout page.
 *
 * SELECTION RULES (per vocabulary framework):
 *   - Tier 2 academic words → explicit + generative (often both)
 *   - Tier 3 content words (thematically central) → explicit
 *   - Tier 3 context words (text access only) → background
 *   - Core response vocabulary → generative
 *   - Max ~20–30 fringe per unit (pre-programming burden threshold)
 *   - Shared response core across all 6 units: because, show, prove, true, wrong,
 *     same, different, agree — consistent motor pattern builds automaticity
 *
 * SYMBOL RULE: Every fringe word must have ARASAAC symbol in symbol_cache.
 *              Missing symbols flagged in comments below.
 *
 * NONFICTION UNIT SKILL ASSIGNMENTS (LOCKED):
 *   Keiko        #1  Close Reading / Annotation (annotation codes: F / R / C)
 *   Radium Girls #1  Close Reading / Annotation (annotation codes: H / Ha / D)
 *   Zitkala-Ša   #3  Text Structure (cause-effect, problem-solution)
 *   504 Sit-In   #4  Author's Purpose / Perspective
 *   Frances Kelsey #5  Claim-Evidence-Reasoning
 *   Capitol Crawl  #6  Sourcing / Corroboration
 */

const units = [

  // ──────────────────────────────────────────────────────────────────────────────
  // RADIUM GIRLS — LIVE on TPT
  // Skill #1: Close Reading / Annotation | Annotation codes: H / Ha / D
  // Standard: RI.6.6 / RI.8.6 — Author perspective + conflicting information
  // 27 core + 17 fringe = 44 words
  // Top 5 Core: prove, wrong, stop, fight, show
  // Top 5 Fringe: radium, factory, safe, danger, lie
  // ──────────────────────────────────────────────────────────────────────────────
  {
    number: 1,
    unitTitle: 'Radium Girls',
    productLine: 'Nonfiction Reading Unit',
    phoneme: '',
    grapheme: '',
    newWords: [
      // ── Core words (27) ──
      // Generative: used to express ideas, judgments, and evidence
      { word: 'think',     type: 'core', instructional: 'generative', top5: false },
      { word: 'feel',      type: 'core', instructional: 'generative', top5: false },
      { word: 'know',      type: 'core', instructional: 'generative', top5: false },
      { word: 'good',      type: 'core', instructional: 'generative', top5: false },
      { word: 'bad',       type: 'core', instructional: 'generative', top5: false },
      { word: 'right',     type: 'core', instructional: 'generative', top5: false },
      { word: 'wrong',     type: 'core', instructional: 'generative', top5: true  }, // Top 5 Core
      { word: 'because',   type: 'core', instructional: 'generative', top5: false },
      { word: 'why',       type: 'core', instructional: 'generative', top5: false },
      { word: 'help',      type: 'core', instructional: 'generative', top5: false },
      { word: 'stop',      type: 'core', instructional: 'generative', top5: true  }, // Top 5 Core
      { word: 'fight',     type: 'core', instructional: 'generative', top5: true  }, // Top 5 Core — thematically central
      { word: 'change',    type: 'core', instructional: 'generative', top5: false },
      { word: 'same',      type: 'core', instructional: 'generative', top5: false },
      { word: 'different', type: 'core', instructional: 'generative', top5: false },
      { word: 'more',      type: 'core', instructional: 'generative', top5: false },
      { word: 'less',      type: 'core', instructional: 'generative', top5: false },
      { word: 'before',    type: 'core', instructional: 'generative', top5: false },
      { word: 'after',     type: 'core', instructional: 'generative', top5: false },
      { word: 'true',      type: 'core', instructional: 'generative', top5: false },
      { word: 'false',     type: 'core', instructional: 'generative', top5: false },
      // Explicit + generative: Tier 2 evidence/argument verbs — directly taught
      { word: 'show',      type: 'core', instructional: 'explicit',   top5: true  }, // Top 5 Core — Tier 2 evidence verb
      { word: 'mean',      type: 'core', instructional: 'explicit',   top5: false },
      { word: 'prove',     type: 'core', instructional: 'explicit',   top5: true  }, // Top 5 Core — Tier 2 evidence verb
      { word: 'first',     type: 'core', instructional: 'generative', top5: false },
      { word: 'then',      type: 'core', instructional: 'generative', top5: false },
      { word: 'last',      type: 'core', instructional: 'generative', top5: false },
      // ── Fringe words (17) ──
      // Background: context/content words needed to access text but not instructional focus
      { word: 'radium',    type: 'fringe', instructional: 'background', top5: true  }, // Top 5 Fringe — central topic noun
      { word: 'factory',   type: 'fringe', instructional: 'background', top5: true  }, // Top 5 Fringe — setting
      { word: 'worker',    type: 'fringe', instructional: 'background', top5: false },
      { word: 'paint',     type: 'fringe', instructional: 'background', top5: false },
      { word: 'sick',      type: 'fringe', instructional: 'background', top5: false },
      { word: 'law',       type: 'fringe', instructional: 'background', top5: false },
      { word: 'court',     type: 'fringe', instructional: 'background', top5: false },
      // Explicit: thematically central fringe — tied to H / Ha / D annotation codes
      { word: 'safe',      type: 'fringe', instructional: 'explicit',   top5: true  }, // Top 5 Fringe — annotation H code
      { word: 'danger',    type: 'fringe', instructional: 'explicit',   top5: true  }, // Top 5 Fringe — annotation H code
      { word: 'company',   type: 'fringe', instructional: 'background', top5: false },
      { word: 'money',     type: 'fringe', instructional: 'background', top5: false },
      { word: 'protect',   type: 'fringe', instructional: 'background', top5: false },
      { word: 'today',     type: 'fringe', instructional: 'background', top5: false },
      { word: 'bone',      type: 'fringe', instructional: 'background', top5: false },
      { word: 'doctor',    type: 'fringe', instructional: 'background', top5: false },
      { word: 'lie',       type: 'fringe', instructional: 'explicit',   top5: true  }, // Top 5 Fringe — annotation D code; Tier 2
      { word: 'proof',     type: 'fringe', instructional: 'explicit',   top5: false }, // Tier 2 evidence word
    ],
    reviewWords: [],
    heartWords: [],
    morphologyNotes: [],
  },

  // ──────────────────────────────────────────────────────────────────────────────
  // KEIKO: A WHALE'S JOURNEY — LIVE on TPT
  // Skill #1: Close Reading / Annotation | Annotation codes: F / R / C
  // Standard: RI.6.6 / RI.8.6 — Author perspective; captivity vs. freedom debate
  // 28 core + 21 fringe = 49 words
  // Top 5 Core: free, because, help, show, true
  // Top 5 Fringe: captivity, whale, ocean, wild, freedom
  // ──────────────────────────────────────────────────────────────────────────────
  {
    number: 2,
    unitTitle: 'Keiko: A Whale\'s Journey',
    productLine: 'Nonfiction Reading Unit',
    phoneme: '',
    grapheme: '',
    newWords: [
      // ── Core words (28) ──
      { word: 'think',     type: 'core', instructional: 'generative', top5: false },
      { word: 'feel',      type: 'core', instructional: 'generative', top5: false },
      { word: 'know',      type: 'core', instructional: 'generative', top5: false },
      { word: 'good',      type: 'core', instructional: 'generative', top5: false },
      { word: 'bad',       type: 'core', instructional: 'generative', top5: false },
      { word: 'best',      type: 'core', instructional: 'generative', top5: false },
      // Explicit: "free" is both a Tier 2 concept AND core — Freedom is the unit's big idea
      { word: 'free',      type: 'core', instructional: 'explicit',   top5: true  }, // Top 5 Core — thematic core word
      { word: 'live',      type: 'core', instructional: 'generative', top5: false },
      { word: 'place',     type: 'core', instructional: 'generative', top5: false },
      { word: 'because',   type: 'core', instructional: 'generative', top5: true  }, // Top 5 Core — reasoning connector
      { word: 'why',       type: 'core', instructional: 'generative', top5: false },
      { word: 'help',      type: 'core', instructional: 'generative', top5: true  }, // Top 5 Core
      { word: 'care',      type: 'core', instructional: 'generative', top5: false },
      { word: 'same',      type: 'core', instructional: 'generative', top5: false },
      { word: 'different', type: 'core', instructional: 'generative', top5: false },
      { word: 'more',      type: 'core', instructional: 'generative', top5: false },
      { word: 'less',      type: 'core', instructional: 'generative', top5: false },
      { word: 'before',    type: 'core', instructional: 'generative', top5: false },
      { word: 'after',     type: 'core', instructional: 'generative', top5: false },
      { word: 'true',      type: 'core', instructional: 'generative', top5: true  }, // Top 5 Core
      { word: 'false',     type: 'core', instructional: 'generative', top5: false },
      // Explicit + generative: Tier 2 evidence verbs
      { word: 'show',      type: 'core', instructional: 'explicit',   top5: true  }, // Top 5 Core — Tier 2 evidence verb
      { word: 'mean',      type: 'core', instructional: 'explicit',   top5: false },
      { word: 'prove',     type: 'core', instructional: 'explicit',   top5: false },
      { word: 'first',     type: 'core', instructional: 'generative', top5: false },
      { word: 'then',      type: 'core', instructional: 'generative', top5: false },
      { word: 'last',      type: 'core', instructional: 'generative', top5: false },
      { word: 'which',     type: 'core', instructional: 'generative', top5: false },
      // ── Fringe words (21) ──
      // Explicit: thematically central — F / R / C annotation + captivity-freedom debate
      { word: 'captivity', type: 'fringe', instructional: 'explicit',   top5: true  }, // Top 5 Fringe — opposes "freedom"
      { word: 'wild',      type: 'fringe', instructional: 'explicit',   top5: true  }, // Top 5 Fringe — annotation F code
      { word: 'freedom',   type: 'fringe', instructional: 'explicit',   top5: true  }, // Top 5 Fringe — unit's central concept
      // Background: setting and context words
      { word: 'ocean',     type: 'fringe', instructional: 'background', top5: true  }, // Top 5 Fringe — setting
      { word: 'whale',     type: 'fringe', instructional: 'background', top5: true  }, // Top 5 Fringe — subject noun
      { word: 'park',      type: 'fringe', instructional: 'background', top5: false },
      { word: 'sick',      type: 'fringe', instructional: 'background', top5: false },
      { word: 'healthy',   type: 'fringe', instructional: 'background', top5: false },
      { word: 'home',      type: 'fringe', instructional: 'background', top5: false },
      { word: 'family',    type: 'fringe', instructional: 'background', top5: false },
      { word: 'pod',       type: 'fringe', instructional: 'background', top5: false },
      { word: 'human',     type: 'fringe', instructional: 'background', top5: false },
      { word: 'move',      type: 'fringe', instructional: 'background', top5: false },
      { word: 'swim',      type: 'fringe', instructional: 'background', top5: false },
      { word: 'learn',     type: 'fringe', instructional: 'background', top5: false },
      { word: 'die',       type: 'fringe', instructional: 'background', top5: false },
      { word: 'safe',      type: 'fringe', instructional: 'explicit',   top5: false },
      { word: 'danger',    type: 'fringe', instructional: 'explicit',   top5: false },
      { word: 'company',   type: 'fringe', instructional: 'background', top5: false },
      { word: 'protect',   type: 'fringe', instructional: 'explicit',   top5: false },
      { word: 'today',     type: 'fringe', instructional: 'background', top5: false },
    ],
    reviewWords: [],
    heartWords: [],
    morphologyNotes: [],
  },

  // ──────────────────────────────────────────────────────────────────────────────
  // FRANCES KELSEY: THE WOMAN WHO SAID NO — BUILT; pending live
  // Skill #5: Claim-Evidence-Reasoning
  // Standard: RI.6.8 / RI.8.8 — Evaluate evidence; identify claims vs. reasoning
  // 27 core + 17 fringe = 44 words
  // Top 5 Core: not, show, wrong, because, strong
  // Top 5 Fringe: safe, test, deny, pressure, claim
  // ──────────────────────────────────────────────────────────────────────────────
  {
    number: 3,
    unitTitle: 'Frances Kelsey and the Thalidomide Crisis',
    productLine: 'Nonfiction Reading Unit',
    phoneme: '',
    grapheme: '',
    newWords: [
      // ── Core words (27) ──
      { word: 'say',       type: 'core', instructional: 'generative', top5: false },
      { word: 'think',     type: 'core', instructional: 'generative', top5: false },
      { word: 'know',      type: 'core', instructional: 'generative', top5: false },
      { word: 'want',      type: 'core', instructional: 'generative', top5: false },
      // Explicit + generative: "not" is the CER pivot word — rejection IS the story
      { word: 'not',       type: 'core', instructional: 'explicit',   top5: true  }, // Top 5 Core — Kelsey's answer was "not approved"
      { word: 'good',      type: 'core', instructional: 'generative', top5: false },
      { word: 'bad',       type: 'core', instructional: 'generative', top5: false },
      { word: 'wrong',     type: 'core', instructional: 'generative', top5: true  }, // Top 5 Core
      { word: 'right',     type: 'core', instructional: 'generative', top5: false },
      { word: 'help',      type: 'core', instructional: 'generative', top5: false },
      { word: 'stop',      type: 'core', instructional: 'generative', top5: false },
      { word: 'go',        type: 'core', instructional: 'generative', top5: false },
      { word: 'more',      type: 'core', instructional: 'generative', top5: false },
      { word: 'different', type: 'core', instructional: 'generative', top5: false },
      { word: 'same',      type: 'core', instructional: 'generative', top5: false },
      // Explicit + generative: CER reasoning connectors — directly taught
      { word: 'because',   type: 'core', instructional: 'explicit',   top5: true  }, // Top 5 Core — CER connector
      { word: 'but',       type: 'core', instructional: 'generative', top5: false },
      { word: 'if',        type: 'core', instructional: 'generative', top5: false },
      { word: 'true',      type: 'core', instructional: 'generative', top5: false },
      // Explicit: CER meta-cognitive vocabulary — Tier 2 academic
      { word: 'question',  type: 'core', instructional: 'explicit',   top5: false }, // Tier 2 — CER structure
      { word: 'answer',    type: 'core', instructional: 'explicit',   top5: false }, // Tier 2 — CER structure
      { word: 'prove',     type: 'core', instructional: 'explicit',   top5: false }, // Tier 2 evidence verb
      { word: 'show',      type: 'core', instructional: 'explicit',   top5: true  }, // Top 5 Core — Tier 2 evidence verb
      { word: 'tell',      type: 'core', instructional: 'generative', top5: false },
      { word: 'believe',   type: 'core', instructional: 'generative', top5: false },
      // Explicit: evaluating evidence strength — directly taught for CER
      { word: 'strong',    type: 'core', instructional: 'explicit',   top5: true  }, // Top 5 Core — evidence evaluation
      { word: 'weak',      type: 'core', instructional: 'explicit',   top5: false },
      // ── Fringe words (17) ──
      { word: 'FDA',         type: 'fringe', instructional: 'background', top5: false }, // acronym context
      { word: 'drug',        type: 'fringe', instructional: 'background', top5: false },
      // Explicit: CER-central fringe — the act of testing = the unit's argument
      { word: 'safe',        type: 'fringe', instructional: 'explicit',   top5: true  }, // Top 5 Fringe — CER question
      { word: 'test',        type: 'fringe', instructional: 'explicit',   top5: true  }, // Top 5 Fringe — CER action
      { word: 'approve',     type: 'fringe', instructional: 'explicit',   top5: false }, // Tier 2 — Kelsey's power
      { word: 'deny',        type: 'fringe', instructional: 'explicit',   top5: true  }, // Top 5 Fringe — what Kelsey did; Tier 2
      // CER Tier 2 skill vocabulary — explicitly taught as unit's analytical framework
      { word: 'claim',       type: 'fringe', instructional: 'explicit',   top5: true  }, // Top 5 Fringe — CER pillar
      { word: 'evidence',    type: 'fringe', instructional: 'explicit',   top5: false }, // Tier 2 — CER pillar
      { word: 'reasoning',   type: 'fringe', instructional: 'explicit',   top5: false }, // Tier 2 — CER pillar
      { word: 'thalidomide', type: 'fringe', instructional: 'background', top5: false },
      { word: 'birth defect',type: 'fringe', instructional: 'background', top5: false }, // ⚠ multi-word; may need two symbols
      { word: 'company',     type: 'fringe', instructional: 'background', top5: false },
      { word: 'pressure',    type: 'fringe', instructional: 'explicit',   top5: true  }, // Top 5 Fringe — Tier 2; Kelsey resisted company pressure
      { word: 'review',      type: 'fringe', instructional: 'explicit',   top5: false }, // Tier 2 — FDA review process
      { word: 'scientist',   type: 'fringe', instructional: 'background', top5: false },
      { word: 'law',         type: 'fringe', instructional: 'background', top5: false },
      { word: 'protect',     type: 'fringe', instructional: 'explicit',   top5: false }, // Tier 2 — Kelsey's goal
    ],
    reviewWords: [],
    heartWords: [],
    morphologyNotes: [],
  },

  // ──────────────────────────────────────────────────────────────────────────────
  // 504 SIT-IN 1977 — LIVE on TPT
  // Skill #4: Author's Purpose / Perspective
  // Standard: RI.6.6 / RI.8.6 — Analyze how authors present perspectives
  //           on the same event differently
  // 23 core + 22 fringe = 45 words
  // Top 5 Core: fight, show, stop, right, change
  // Top 5 Fringe: protest, law, disability, equal, rights
  // ──────────────────────────────────────────────────────────────────────────────
  {
    number: 4,
    unitTitle: '504 Sit-In 1977',
    productLine: 'Nonfiction Reading Unit',
    phoneme: '',
    grapheme: '',
    newWords: [
      // ── Core words (23) — sourced from unit DRAFT + confirmed in build reference ──
      // Generative response vocabulary
      { word: 'people',    type: 'core', instructional: 'generative', top5: false },
      { word: 'change',    type: 'core', instructional: 'generative', top5: true  }, // Top 5 Core
      { word: 'feel',      type: 'core', instructional: 'generative', top5: false },
      { word: 'fight',     type: 'core', instructional: 'generative', top5: true  }, // Top 5 Core — thematically central
      { word: 'help',      type: 'core', instructional: 'generative', top5: false },
      { word: 'make',      type: 'core', instructional: 'generative', top5: false },
      { word: 'need',      type: 'core', instructional: 'generative', top5: false },
      // Explicit + generative: Tier 2 evidence verb
      { word: 'show',      type: 'core', instructional: 'explicit',   top5: true  }, // Top 5 Core
      { word: 'sit',       type: 'core', instructional: 'generative', top5: false }, // the sit-in action
      { word: 'stop',      type: 'core', instructional: 'generative', top5: true  }, // Top 5 Core
      { word: 'tell',      type: 'core', instructional: 'generative', top5: false },
      { word: 'think',     type: 'core', instructional: 'generative', top5: false },
      { word: 'want',      type: 'core', instructional: 'generative', top5: false },
      // Explicit: Tier 2 concepts central to Author's Purpose / Perspective skill
      { word: 'brave',     type: 'core', instructional: 'explicit',   top5: false }, // character/author purpose analysis
      { word: 'different', type: 'core', instructional: 'generative', top5: false },
      { word: 'fair',      type: 'core', instructional: 'explicit',   top5: false }, // Tier 2 equity concept
      { word: 'free',      type: 'core', instructional: 'generative', top5: false },
      { word: 'important', type: 'core', instructional: 'generative', top5: false },
      { word: 'right',     type: 'core', instructional: 'generative', top5: true  }, // Top 5 Core
      { word: 'safe',      type: 'core', instructional: 'generative', top5: false },
      { word: 'same',      type: 'core', instructional: 'generative', top5: false },
      { word: 'strong',    type: 'core', instructional: 'generative', top5: false },
      { word: 'wrong',     type: 'core', instructional: 'generative', top5: false },
      // ── Fringe words (22) — sourced from unit DRAFT + confirmed in build reference ──
      { word: 'approve',        type: 'fringe', instructional: 'background', top5: false },
      { word: 'crawl',          type: 'fringe', instructional: 'background', top5: false }, // protest imagery
      { word: 'demand',         type: 'fringe', instructional: 'explicit',   top5: false }, // Tier 2 — protest vocabulary
      { word: 'deny',           type: 'fringe', instructional: 'explicit',   top5: false }, // Tier 2 — government response
      { word: 'occupy',         type: 'fringe', instructional: 'explicit',   top5: false }, // Tier 2 — the sit-in IS an occupation
      { word: 'organize',       type: 'fringe', instructional: 'explicit',   top5: false }, // Tier 2 — advocacy skill
      { word: 'protest',        type: 'fringe', instructional: 'explicit',   top5: true  }, // Top 5 Fringe — thematically central
      { word: 'prove',          type: 'fringe', instructional: 'explicit',   top5: false }, // Tier 2 evidence verb
      { word: 'sign',           type: 'fringe', instructional: 'background', top5: false },
      // Access + disability rights vocabulary — Author's Purpose fringe targets
      { word: 'access',         type: 'fringe', instructional: 'explicit',   top5: false }, // Tier 2 — disability rights
      { word: 'advocate',       type: 'fringe', instructional: 'explicit',   top5: false }, // Tier 2 — key role
      { word: 'barrier',        type: 'fringe', instructional: 'explicit',   top5: false }, // Tier 2 — access concept
      { word: 'building',       type: 'fringe', instructional: 'background', top5: false },
      { word: 'community',      type: 'fringe', instructional: 'background', top5: false },
      { word: 'disability',     type: 'fringe', instructional: 'explicit',   top5: true  }, // Top 5 Fringe — thematically central
      { word: 'discrimination', type: 'fringe', instructional: 'explicit',   top5: false }, // Tier 2
      { word: 'equal',          type: 'fringe', instructional: 'explicit',   top5: true  }, // Top 5 Fringe — central concept
      { word: 'federal',        type: 'fringe', instructional: 'background', top5: false },
      { word: 'government',     type: 'fringe', instructional: 'background', top5: false },
      { word: 'law',            type: 'fringe', instructional: 'background', top5: true  }, // Top 5 Fringe — Section 504
      { word: 'rights',         type: 'fringe', instructional: 'explicit',   top5: true  }, // Top 5 Fringe — thematically central
      { word: 'section',        type: 'fringe', instructional: 'background', top5: false }, // Section 504 reference
    ],
    reviewWords: [],
    heartWords: [],
    morphologyNotes: [],
  },

  // ──────────────────────────────────────────────────────────────────────────────
  // CAPITOL CRAWL 1990 — BUILT; pending live
  // Skill #6: Sourcing / Corroboration
  // Standard: RI.6.8 / RI.8.8 — Evaluate sources; corroborate claims across sources
  // 19 core + 15 fringe = 34 words (added "disability" per framework gap 2026-03-29)
  // Top 5 Core: because, agree, strong, true, same
  // Top 5 Fringe: disability, ADA, evidence, claim, corroborate
  // NOTE: "disability" added to fringe — identified as vocabulary framework gap 2026-03-29.
  //       Previous Top 5 Fringe was: protest, law, evidence, claim, ADA.
  //       Updated to center disability as thematically central per ADA / Jennifer Keelan context.
  // ──────────────────────────────────────────────────────────────────────────────
  {
    number: 5,
    unitTitle: 'Capitol Crawl 1990',
    productLine: 'Nonfiction Reading Unit',
    phoneme: '',
    grapheme: '',
    newWords: [
      // ── Core words (19) ──
      { word: 'think',     type: 'core', instructional: 'generative', top5: false },
      { word: 'know',      type: 'core', instructional: 'generative', top5: false },
      { word: 'true',      type: 'core', instructional: 'generative', top5: true  }, // Top 5 Core
      { word: 'false',     type: 'core', instructional: 'generative', top5: false },
      { word: 'same',      type: 'core', instructional: 'generative', top5: true  }, // Top 5 Core — corroboration
      { word: 'different', type: 'core', instructional: 'generative', top5: false },
      { word: 'good',      type: 'core', instructional: 'generative', top5: false },
      { word: 'bad',       type: 'core', instructional: 'generative', top5: false },
      // Explicit: evidence evaluation vocabulary — directly tied to sourcing skill
      { word: 'strong',    type: 'core', instructional: 'explicit',   top5: true  }, // Top 5 Core — source evaluation
      { word: 'weak',      type: 'core', instructional: 'explicit',   top5: false },
      { word: 'because',   type: 'core', instructional: 'generative', top5: true  }, // Top 5 Core — reasoning connector
      { word: 'but',       type: 'core', instructional: 'generative', top5: false },
      // Explicit: sourcing/corroboration response vocabulary — directly taught
      { word: 'agree',     type: 'core', instructional: 'explicit',   top5: true  }, // Top 5 Core — corroboration response
      { word: 'disagree',  type: 'core', instructional: 'explicit',   top5: false },
      // Question words for source analysis
      { word: 'why',       type: 'core', instructional: 'generative', top5: false },
      { word: 'who',       type: 'core', instructional: 'generative', top5: false },
      { word: 'what',      type: 'core', instructional: 'generative', top5: false },
      { word: 'where',     type: 'core', instructional: 'generative', top5: false },
      { word: 'when',      type: 'core', instructional: 'generative', top5: false },
      // ── Fringe words (15 — includes "disability" added 2026-03-29) ──
      // Background: event context
      { word: 'crawl',         type: 'fringe', instructional: 'background', top5: false },
      { word: 'Capitol',       type: 'fringe', instructional: 'background', top5: false },
      { word: 'steps',         type: 'fringe', instructional: 'background', top5: false },
      { word: 'protest',       type: 'fringe', instructional: 'background', top5: false },
      { word: 'law',           type: 'fringe', instructional: 'background', top5: false },
      // Explicit + Top 5: thematically central disability rights vocabulary
      { word: 'disability',    type: 'fringe', instructional: 'explicit',   top5: true  }, // ADDED 2026-03-29 — framework gap; ADA/Keelan context
      { word: 'ADA',           type: 'fringe', instructional: 'explicit',   top5: true  }, // Top 5 Fringe — Americans with Disabilities Act
      { word: 'ADAPT',         type: 'fringe', instructional: 'background', top5: false }, // activist group context
      // Explicit: Sourcing/Corroboration Skill #6 Tier 2 vocabulary — core of the unit
      { word: 'source',        type: 'fringe', instructional: 'explicit',   top5: false }, // Tier 2 — skill word
      { word: 'reliable',      type: 'fringe', instructional: 'explicit',   top5: false }, // Tier 2 — skill word
      { word: 'corroborate',   type: 'fringe', instructional: 'explicit',   top5: true  }, // Top 5 Fringe — unit's analytical skill
      { word: 'evidence',      type: 'fringe', instructional: 'explicit',   top5: true  }, // Top 5 Fringe — Tier 2
      { word: 'claim',         type: 'fringe', instructional: 'explicit',   top5: true  }, // Top 5 Fringe — Tier 2
      { word: 'verify',        type: 'fringe', instructional: 'explicit',   top5: false }, // Tier 2 — skill word
      { word: 'contradict',    type: 'fringe', instructional: 'explicit',   top5: false }, // Tier 2 — skill word
    ],
    reviewWords: [],
    heartWords: [],
    morphologyNotes: [],
  },

  // ──────────────────────────────────────────────────────────────────────────────
  // ZITKALA-ŠA — BUILT; pending live
  // Skill #3: Text Structure (cause-effect, problem-solution)
  // Standard: RI.6.5 / RI.8.5 — Analyze text structure; how structure conveys meaning
  // 20 core + 16 fringe = 36 words
  // Top 5 Core: change, need, right, stop, because
  // Top 5 Fringe: assimilation, boarding school, spirit, testimony, cause
  // NOTE: Word list reconciled 2026-03-29.
  //   build_reference (authoritative) had 9 fringe: zitkala, boarding, assimilation, dakota,
  //   reservation, hair, spirit, testimony, organize
  //   nonfiction_unit_vocab.js had 12 fringe including structural Skill #3 terms:
  //   cause, effect, problem, solution, structure, identity, culture
  //   RECONCILED: combined both lists; structural terms (cause/effect/problem/solution/structure)
  //   are Tier 2 explicit targets for Skill #3 and BELONG in fringe for AAC access.
  //   Identity + culture added as Tier 2 thematic vocabulary.
  //   ⚠ Symbol check needed: 'zitkala', 'dakota' — may not have ARASAAC symbols.
  //     Use custom text card if not in symbol_cache.
  // ──────────────────────────────────────────────────────────────────────────────
  {
    number: 6,
    unitTitle: 'Zitkala-Ša',
    productLine: 'Nonfiction Reading Unit',
    phoneme: '',
    grapheme: '',
    newWords: [
      // ── Core words (20) — from confirmed build reference ──
      { word: 'think',     type: 'core', instructional: 'generative', top5: false },
      { word: 'know',      type: 'core', instructional: 'generative', top5: false },
      { word: 'feel',      type: 'core', instructional: 'generative', top5: false },
      { word: 'why',       type: 'core', instructional: 'generative', top5: false },
      { word: 'because',   type: 'core', instructional: 'generative', top5: true  }, // Top 5 Core — cause-effect connector
      { word: 'but',       type: 'core', instructional: 'generative', top5: false },
      { word: 'and',       type: 'core', instructional: 'generative', top5: false },
      { word: 'same',      type: 'core', instructional: 'generative', top5: false },
      { word: 'different', type: 'core', instructional: 'generative', top5: false },
      // Explicit: "change" is both a Tier 2 academic concept AND the unit's central question
      { word: 'change',    type: 'core', instructional: 'explicit',   top5: true  }, // Top 5 Core — text structure + theme
      { word: 'make',      type: 'core', instructional: 'generative', top5: false },
      { word: 'do',        type: 'core', instructional: 'generative', top5: false },
      { word: 'help',      type: 'core', instructional: 'generative', top5: false },
      { word: 'stop',      type: 'core', instructional: 'generative', top5: true  }, // Top 5 Core
      { word: 'want',      type: 'core', instructional: 'generative', top5: false },
      // Explicit: Tier 2 concepts central to the unit's ethical question
      { word: 'need',      type: 'core', instructional: 'explicit',   top5: true  }, // Top 5 Core
      { word: 'right',     type: 'core', instructional: 'explicit',   top5: true  }, // Top 5 Core — rights / right-wrong
      { word: 'wrong',     type: 'core', instructional: 'generative', top5: false },
      { word: 'good',      type: 'core', instructional: 'generative', top5: false },
      { word: 'bad',       type: 'core', instructional: 'generative', top5: false },
      // ── Fringe words (16) — reconciled from build_reference + vocab.js 2026-03-29 ──
      // Background: proper noun / cultural context — from build_reference
      { word: 'zitkala',         type: 'fringe', instructional: 'background', top5: false }, // ⚠ no ARASAAC symbol — use text card
      { word: 'dakota',          type: 'fringe', instructional: 'background', top5: false }, // ⚠ no ARASAAC symbol — use text card
      { word: 'hair',            type: 'fringe', instructional: 'background', top5: false }, // specific cultural symbol in text
      // Explicit: thematically central fringe — from both sources
      { word: 'boarding school', type: 'fringe', instructional: 'explicit',   top5: true  }, // Top 5 Fringe — the institutional force; ⚠ multi-word
      { word: 'assimilation',    type: 'fringe', instructional: 'explicit',   top5: true  }, // Top 5 Fringe — Tier 2/3 central concept
      { word: 'reservation',     type: 'fringe', instructional: 'explicit',   top5: true  }, // Top 5 Fringe
      { word: 'spirit',          type: 'fringe', instructional: 'explicit',   top5: true  }, // Top 5 Fringe — what was taken
      { word: 'testimony',       type: 'fringe', instructional: 'explicit',   top5: true  }, // Top 5 Fringe — Tier 2 text type for this unit
      { word: 'organize',        type: 'fringe', instructional: 'explicit',   top5: false }, // Tier 2 advocacy action
      // Explicit: Skill #3 (Text Structure) Tier 2 analytical vocabulary — directly taught
      { word: 'cause',           type: 'fringe', instructional: 'explicit',   top5: false }, // Tier 2 — text structure skill word
      { word: 'effect',          type: 'fringe', instructional: 'explicit',   top5: false }, // Tier 2 — text structure skill word
      { word: 'problem',         type: 'fringe', instructional: 'explicit',   top5: false }, // Tier 2 — text structure skill word
      { word: 'solution',        type: 'fringe', instructional: 'explicit',   top5: false }, // Tier 2 — text structure skill word
      { word: 'structure',       type: 'fringe', instructional: 'explicit',   top5: false }, // Tier 2 — meta-skill word
      // Explicit: Tier 2 thematic vocabulary
      { word: 'identity',        type: 'fringe', instructional: 'explicit',   top5: false }, // Tier 2 — central theme
      { word: 'culture',         type: 'fringe', instructional: 'explicit',   top5: false }, // Tier 2 — central theme
    ],
    reviewWords: [],
    heartWords: [],
    morphologyNotes: [],
  },

  // ──────────────────────────────────────────────────────────────────────────────
  // WONDER: CHARACTER ANALYSIS — Fiction Anchor Text Unit #1
  // RL.6.3 / RL.7.3 | Grades 3–8
  // Annotation codes: [TRAIT] / [WHY] / [CHANGE]
  // 12 core + 12 fringe = 24 words
  // ⚠ Missing ARASAAC symbols: alone, belong, invisible, loyal, bully, ordinary,
  //   helmet, face looks different — flag before build
  // ──────────────────────────────────────────────────────────────────────────────
  {
    number: 7,
    unitTitle: 'Wonder: Character Analysis',
    productLine: 'Fiction Anchor Text Unit',
    phoneme: '',
    grapheme: '',
    newWords: [
      // ── Core words (12) — Fiction priority: emotional/mental state first ──
      // Layer 1: Emotional/mental state vocabulary (primary access gap for fiction)
      { word: 'feel',    type: 'core', instructional: 'explicit',   top5: false },
      { word: 'want',    type: 'core', instructional: 'explicit',   top5: false },
      { word: 'think',   type: 'core', instructional: 'explicit',   top5: false },
      { word: 'know',    type: 'core', instructional: 'explicit',   top5: false },
      { word: 'change',  type: 'core', instructional: 'explicit',   top5: false },
      { word: 'sad',     type: 'core', instructional: 'explicit',   top5: false },
      { word: 'scared',  type: 'core', instructional: 'explicit',   top5: false },
      { word: 'happy',   type: 'core', instructional: 'explicit',   top5: false },
      { word: 'alone',   type: 'core', instructional: 'explicit',   top5: false }, // ⚠ check symbol_cache
      { word: 'kind',    type: 'core', instructional: 'explicit',   top5: false },
      // Layer 2: Relational/causal language
      { word: 'because', type: 'core', instructional: 'generative', top5: false },
      { word: 'maybe',   type: 'core', instructional: 'generative', top5: false },
      // ── Fringe words (12) — Character/narrative vocabulary specific to Wonder ──
      // Layer 3: Narrative fringe — description, not name
      { word: 'different',          type: 'fringe', instructional: 'explicit',   top5: false },
      { word: 'belong',             type: 'fringe', instructional: 'explicit',   top5: false }, // ⚠ missing symbol
      { word: 'invisible',          type: 'fringe', instructional: 'explicit',   top5: false }, // ⚠ missing symbol
      { word: 'brave',              type: 'fringe', instructional: 'explicit',   top5: false },
      { word: 'loyal',              type: 'fringe', instructional: 'explicit',   top5: false }, // ⚠ missing symbol
      { word: 'bully',              type: 'fringe', instructional: 'explicit',   top5: false }, // ⚠ missing symbol
      { word: 'ordinary',           type: 'fringe', instructional: 'explicit',   top5: false }, // ⚠ missing symbol
      // Layer 4: Skill-specific vocabulary
      { word: 'friend',             type: 'fringe', instructional: 'explicit',   top5: false },
      { word: 'helmet',             type: 'fringe', instructional: 'background', top5: false }, // ⚠ missing symbol — Auggie's mask
      { word: 'school',             type: 'fringe', instructional: 'background', top5: false },
      { word: 'choose',             type: 'fringe', instructional: 'explicit',   top5: false },
      { word: 'face looks different',type:'fringe', instructional: 'background', top5: false }, // ⚠ missing symbol — multi-word
    ],
    reviewWords: [],
    heartWords: [],
    morphologyNotes: [],
  },

];

module.exports = units;

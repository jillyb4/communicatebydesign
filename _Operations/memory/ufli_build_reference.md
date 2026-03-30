# UFLI Build Reference

Deep reference for UFLI Phonics product builds. Pull this file for UFLI build sessions.

## UFLI Product Design Principles

- **Assume nothing.** Student is a complex communicator, mostly nonspeaking. They have a teacher willing to learn. We provide everything else.
- **Four tools per lesson:** alternative pencil (encoding), e-trans board (decoding), symbol cards (this packet), phoneme sounds (partner/device).
- **Alternative pencil established in Pre-Alphabet A-Z lessons.** By numbered UFLI lessons, it is an assumed tool.
- **Symbol cards are reading response tools, not SGD programming.** Print, cut, use with e-trans board.
- **Decoding steps → symbol cards + e-trans board. Encoding steps → alternative pencil.**
- **Sound access is non-negotiable.** Student must hear the phoneme. Partner voice, Hand2Mind Talking Mirror Phoneme Set, or SGD if available.
- **The internal reading voice develops through hearing, not speaking.** (Foley & Pollatsek 1999, Bishop 1985, Erickson & Koppenhaver 2020, Vandervelden & Siegel 1999)
- **Hybrid word lists:** new words get symbol cards, review words get a "pull from binder" text list.
- **Morphology flags:** when UFLI words are tense variations (sit/sat, has/had), flag as a teaching moment.
- **Teacher decides how many choices to present.** No fixed "levels." 2-choice, 4-quadrant e-trans, field of 6-8 — based on the student.
- **Pacing flexes, scope doesn't.** Complex communicators may spend 2-3 days on one lesson. Wait time is instruction (5-10 seconds).
- **Product split: Teacher Guide + Per-Lesson Packets.** The 8 UFLI steps, access options, auditory loop, para scripts, pacing guidance do NOT change lesson to lesson — they go in the Teacher Guide (buy once). Per-lesson packets: lesson info page, symbol cards, review words, heart words, morphology notes. ~2-3 pages per lesson.

## Lesson Config Pattern
```js
{ number, phoneme, grapheme, newWords, reviewWords, heartWords, morphologyNotes }
```

## Lessons 1–4 Note
UFLI Lessons 1–4 introduce letters — no new phoneme-grapheme words yet, but students DO have work to do from Lesson 1. Packets for Lessons 1–4 focus on: alternative pencil access for letter recognition, e-trans board setup, symbol-to-letter correspondence, and partner scripting for the auditory confirmation loop. These ARE $1 individual products. Students should not wait until Lesson 5 to begin. The Teacher Guide covers the 8-step structure; Lesson 1–4 packets carry the letter-specific access content for each lesson.

## Ready for TPT Folder
`Products/UFLI Phonics/Ready for TPT v3/` — 34 final files:
- 34 lesson packets (.docx, Lessons 1–34)
- `UFLI_Teacher_Guide_and_Communication_Partner_Guide.docx`
- `UFLI_Letter_Cards_Lowercase.pdf`
- `UFLI_Session_Data_Tracker.pdf`
- `UFLI_Symbol_Binder_Guide.pdf`

## UFLI Packet Features

### Fitzgerald Key Categorization
- Standard: Fitzgerald Key (1949), adapted Goossens', Crain, & Elder (1992). Matches TD Snap, LAMP/Unity, Proloquo2Go, TouchChat device color-coding.
- Categories: Yellow=People/Pronouns, Green=Verbs/Actions, Orange=Adjectives/Descriptions, White=Nouns (default), Blue=Prepositions/Time/Location, Pink=Social/Questions/Feelings
- Module: `fitzgerald_key.js` — classifies all 458 UFLI words. Review words grouped by category with color strips, 5 words per row.

### Drawing Activity for Missing Symbols
- 29 of 508 UFLI words have no ARASAAC symbol (mostly CVC nonsense/rare words).
- `✏️ Draw It!` activity replaces blank `[symbol]` placeholders. Drawing box on card.
- Real words = draw meaning. Made-up/silly words = student invents the picture.
- Note at top of symbol cards section explains the activity to the communication partner.

### Embedded Session Data Tracker
- **Placement:** Last page of every lesson packet (before final attribution).
- **4 sections:** (1) Prompt Level by UFLI Step — table with I/G–/G+/VM/RA columns for all 8 steps. (2) Core Word Use — 10 write-in slots with ✓/M/—/★ markers. (3) Reading & Connected Text — checkboxes for passage attempt, accuracy, support, behaviors. (4) Notes & Mastery Decision — write-in area + mastery checkboxes.
- Standalone PDF: `UFLI_Session_Data_Tracker.pdf` (4 copies).

### One-Sided Printing Note
All symbol card pages MUST be printed one-sided. Cards are cut out for e-trans boards, binders, PECS exchange. Amber-accented guidance box on cover page of every packet.

### Letter Card Library
- Lowercase only. NO keywords, NO phonemes, NO mixed case. 2.5"×2.5" cards, 3×3 grid per page.
- White background, navy letter (Helvetica-Bold 120pt), teal rounded borders, dashed cut lines.
- `UFLI_Letter_Cards_Lowercase.pdf` (3 pages, 26 cards)

### "Communication Partner" Terminology
Standard term throughout all UFLI products (Light 1988, Beukelman & Mirenda). Covers paras, RBTs, teachers, parents, tutors, siblings — anyone supporting the student.

## Prompting Framework — LOCKED (March 2026)

### Three Partner Modes
| Mode | Name | Key Features |
|------|------|-------------|
| Mode 1 | Instructional | Hierarchy active · Data running · Correct/incorrect applies · **Hierarchy applies HERE only** |
| Mode 2 | Partnership | No demands · Partner follows student lead · Note spontaneous communication |
| Mode 3 | Facilitated Participation | Physical access support only · No interpretation or editorializing |

**Critical rule:** Para defaulting to Mode 1 in ALL contexts is the most common AAC barrier.

### Preconditions (Always Active — Every Mode)
- **ALI (Aided Language Input):** Partner models on student's own system during natural interaction. Not a prompt — a demonstration.
- **Communication Environment:** System present, charged, accessible, positioned. Vocabulary programmed. Activity has something worth saying.

### 5-Level Prompt Hierarchy (Mode 1 Only)
| Code | Level | What Partner Does |
|------|-------|------------------|
| I | Independent | Student communicates without any prompt. Respond naturally. |
| — | **WAIT** | Full pause — **minimum 10 seconds** — between EVERY level. |
| G– | Indirect Cue | Gesture toward the system as a whole. NOT a specific symbol. |
| G+ | Direct Cue | Point to a specific symbol, location, or page. |
| VM | Verbal Model | Say message + demonstrate on student's own system. |
| RA | Reassess Access | Non-response = data about environment, NOT the student. Check: positioning · system · vocabulary · activity · partner. |

Tracker codes: I / G– / G+ / VM / RA — record highest level of support needed.
Non-response principle: Non-response = ask why, not stop.

## Pre-Alphabet A-Z Design Principles

- **Pre-Alphabet = letters, not sounds.** Avoid phoneme-grapheme instruction in this phase. Focus on letter recognition and developing the alternative pencil.
- **Alternative pencil is exploratory.** Student tries different access methods to find what works.
- **Frequency keyboard layout, not QWERTY.** Letters organized by frequency (ETAOIN SHRDLU). Color-coded bands: red (E,T,A), yellow (S,H,R,D), green (M,W,F), teal (O,I,N,B,V,K), purple (J,X,Q,Z).
- **Map with eyes before device.** Student maps UFLI lessons on frequency keyboard with gaze BEFORE getting the SGD. Builds motor planning for letter location.
- **Progressive letter reveal.** Start with letters hidden. As each is introduced in A-Z lessons, unhide it. Prevents overwhelm.
- **Predictive text OFF during phonics.** Word prediction has no lasting impact on independent spelling skills (ASHA Leader 2025, EDC/NCIP). Prediction short-circuits phonemic processing. Turn off during all phonics instruction. Introduce prediction later as a WRITING efficiency tool.

## Audience & Delivery

- **Any age.** Complex communicators who need phonics instruction may be any age. Access determines readiness, not age.
- **Any setting.** Primary: classroom with 1:1 para. Also: home with parent using YouTube UFLI lesson videos, therapy, tutoring.
- **This is SDI.** Phonics instruction for a complex communicator requires dedicated 1:1 support. Evidence supports ~2 hours/day of literacy instruction.
- **IEP advocacy.** Families need to know how to request 1:1 SDI for structured literacy in the IEP: what to request, sample IEP goal stems, how much time (daily, 2 hours), who delivers it, what to say when district pushes back.

## TPT Listing Files
- `Products/UFLI Phonics/TPT_Listing_Teacher_Guide.md`
- `Products/UFLI Phonics/TPT_Listing_Per_Lesson_Packets.md`
- `Products/UFLI Phonics/UFLI_Cover_Design_Notes.md`

## Competitive Positioning
Only product on TPT providing a complete access layer for all 8 UFLI steps for AAC users. All competitors are supplemental worksheets or adapted manipulatives — none provide communication partner scripts, alternative response pathways across all AAC modalities, or the auditory confirmation loop.

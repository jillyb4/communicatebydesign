# Symbol Cards & Binder Ecosystem Reference

Deep reference for AAC symbol cards, trading cards, and the binder ecosystem. Pull this file for symbol/card build sessions.

## AAC Symbol System

- **Primary source:** ARASAAC (arasaac.org) — 13,000+ pictograms, CC BY-NC-SA 4.0, free API, no auth required
- **API:** `https://api.arasaac.org/v1/pictograms/en/search/{word}` → image at `https://static.arasaac.org/pictograms/{id}/{id}_500.png`
- **Fallback:** Mulberry Symbols (mulberrysymbols.org) — 3,000+ SVGs, CC BY-SA 4.0
- **Aggregator:** OpenSymbols (opensymbols.org) — searches across ARASAAC + Mulberry + Sclera + Tawasol, requires API token
- **License compliance (required in every document):** "Pictographic symbols © Government of Aragón. ARASAAC. Licensed under CC BY-NC-SA 4.0."
- **Teacher note (include in every product with symbols):** "Use symbols from your student's own AAC system first. These open-source symbols are provided as a universal reference when system-specific symbols are not available."
- **QR code link:** arasaac.org/pictograms/search

## Symbol Sizing (3 Access Levels)
Based on TD Snap grid layouts, low-tech board standards, WCAG 2.2 SC 2.5.8, and print DPI.

| Level | Size | Per Row | Borders | Use |
|-------|------|---------|---------|-----|
| Level 1 | ~1.75" / 126pt | 3 | Thick | Partner-assisted/beginning eye gaze |
| Level 2 | ~1.25" / 90pt | 4 | Standard | Eye gaze/direct selection (DEFAULT) |
| Level 3 | ~1" / 72pt | 5 | Standard | Independent device/reference |

`buildSymbolPage({ accessLevel: 'all' })` generates all 3 levels; use `'level1'`/`'level2'`/`'level3'` for specific level.

## Symbol Fetcher
`_Operations/cbd_symbol_fetcher.js` — fetches ARASAAC symbols, caches in `_Operations/symbol_cache/`.
CLI: `node cbd_symbol_fetcher.js read help want more`
Library cache: `_Operations/symbol_cache/_symbol_library.json` — 741 cached PNGs, tracks every word fetched. CLI: `node cbd_symbol_fetcher.js --library`

## ARASAAC Symbol Backfill Strategy
For plurals missing symbols, fetch base form (digs→dig, cops→cop). Recovers ~26% of missing symbols. Remaining → Draw It! activity.

---

## Symbol Card Binder Ecosystem

### Core Product Differentiator
Every CbD lesson ships with trading card–sized AAC symbol cards that accumulate into a student's personal vocabulary library, organized in a 9-pocket trading card binder by Modified Fitzgerald Key categories.

### Card Design — 3-Zone Layout (2.5" × 3.5")
| Zone | Content | Purpose |
|------|---------|---------|
| **Zone 1 (top)** | Fitzgerald Key category bar — solid color + white label text | Binder sorting |
| **Zone 2 (center)** | ARASAAC symbol with Fitzgerald Key colored border | Visual vocabulary (~60% of card) |
| **Zone 3 (bottom)** | Bold word label + part-of-speech sublabel | Word identification |

### Modified Fitzgerald Key Colors
| Category | Color | Hex |
|----------|-------|-----|
| People / Pronouns | Yellow | #D4A800 |
| Verbs / Actions | Green | #00A86B |
| Descriptions | Orange | #FF8C00 |
| Nouns | Brown/Gold | #8B6914 |
| Little Words (Prepositions) | Blue | #4A90D9 |
| Social / Feelings | Pink | #E88CA5 |

### Visual Coding on Cards
- ★ star = core word (high frequency, likely on device already)
- ♥ heart = heart word (irregular, memorize)
- No mark = fringe word (unit-specific, pre-program before lesson)

### Ecosystem Components
1. Symbol Cards — 2.5"×3.5" trading cards (Component 2 of Unit Printable Kit)
2. 9-Pocket Binder — organized by Fitzgerald Key category tabs
3. Word Tracker — `UFLI_AAC_Phonics_Data_Tracker_FREE.xlsx`
4. Communication Board — unit-level grid layout using same Fitzgerald Key columns
5. Alternative Pencil + E-Trans Board — part of broader AAC ecosystem

### Production Rule
**Every CbD lesson MUST include:**
- Symbol card set (trading card size, 3-zone layout)
- Word tracker for accumulated vocabulary

These are STANDARD resources, not optional add-ons.

---

## 9 Cent Copy Print Specification (CONFIRMED by Nicole, March 2026)

| Setting | Value |
|---------|-------|
| Product type | Multi-Page Documents (NOT booklets) |
| Page size | 2.5" × 3.5" (one card per page — NO multiple-up) |
| Printed on | Both Sides (odd = front, even = back) |
| Color | Full Color |
| Paper | 80# Matte Cover Paper - Heavy Flyer Weight |
| Bleed | White Margin (No Bleed) |
| Margins | 0.25" white margin built into artwork on all four edges. Art area = 2.0" × 3.0" centered. |

**CRITICAL:** 9 Cent Copy does NOT accept multiple-up layouts. Each page must be exactly one card at 2.5"×3.5". Without the 0.25" margin built in, 9CC scales artwork down and cards end up smaller than binder sleeves.

### Card Backs
- Default: `card_back_default.png` (florals/butterflies, white bg, bleed-safe) — Canva ID DAHEmP8Ai3o page 1
- Alternate: `card_back_pink_rainbow.png` (Kylee music theme) — Canva ID DAHEmP8Ai3o page 2

### Build Scripts
- Standalone decks: `_Operations/build_trading_card_decks.py --deck all`
- Per-product companion: `from cbd_trading_cards import build_product_deck; build_product_deck("Unit Name", words, output_path)`
- Print spec files auto-generated per deck: `[Deck_Name]_Print_Spec.txt`

### Per-Product Companion Decks (MANDATORY for all AAC products)
Every product with AAC symbol cards MUST also generate a companion trading card deck PDF. Same word list as in-document symbol cards. Module: `_Operations/cbd_trading_cards.py`. Add this step to every build script AFTER the printable kit build.

---

## Word Tracker Adaptation Needed
Source file: `Products/UFLI Phonics/UFLI/UFLI_AAC_Phonics_Data_Tracker_FREE.xlsx`
**Add/change:**
- Fitzgerald Key Category column (dropdown: People/Pronouns, Verbs/Actions, Descriptions, Nouns, Little Words, Social/Feelings)
- In Binder? column (✓ / —)
- Source Unit/Lesson column
- Summary dashboard with COUNTIF per Fitzgerald category
- Units Completed tab — log of units/lessons done + running total
- Binder Guide tab — printable reference page
Keep existing UFLI prompt-level tracking intact.
This tracker ships with EVERY CbD product — not UFLI-only.

---

## Competitive Advantage
No other TPT store in the AAC/SPED space offers a cumulative symbol card binder system. Competitors sell isolated worksheets. CbD's ecosystem means every purchase adds to the student's growing vocabulary library — creating lock-in and cross-product value.

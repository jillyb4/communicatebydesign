# Symbol Card Sheet Generator — Reference

**File:** `_Operations/Tools/cbd-pecs-sheet-generator.html`
**Built:** Session 26 (Sep 2026) · Branch `claude/pecs-sheet-generator-lp7uox`
**Status:** Working, classroom-ready. NOT yet an official product — see Open Decisions.

A standalone browser tool, separate from the product build system. Type words or
phrases → pull symbols → print a sheet of cards at a true physical size. Built for
quick classroom needs by Jill, paras, RBTs and BCBAs — not for a TPT product build.

---

## Why it is a browser tool and not a Python build

The docx/ReportLab build system exists to turn vocabulary data into *products*, run
by Jill, versioned, shipped. This is a *utility*: someone needs six cards before
lunch. A double-clicked HTML file needs no terminal, no install, and no repo. That
is the whole reason it works for a para.

It lives in `_Operations/Tools/` — a category added this session for standalone
classroom utilities. Not a product, not a dashboard. The symbol cache path is
relative (`../Symbols/symbol_cache/`), so the file must stay in that folder to use
the cache. It still works anywhere without it.

---

## How symbols resolve

Three sources, in order:

1. **Local cache** — `../Symbols/symbol_cache/arasaac_{word}.png`, same filename
   convention the Python builds use (`word.lower().replace(' ','_')`). Works offline
   and is faster than the network.
2. **ARASAAC live search** — `api.arasaac.org/v1/pictograms/en/search/{term}`,
   images from `static.arasaac.org`.
3. **Draw-it box** — a blank bordered card when nothing is found. Never a guessed
   picture.

### Multi-word fallback chain — the thing that makes it usable

ARASAAC has no pictogram for "back stretch". The search walks a chain and keeps the
label the user typed:

| Typed | Chain tried |
|---|---|
| `back stretch` | back stretch → stretch → back |
| `hand rub` | hand rub → rub → hand |
| `squeezes` | squeezes → squeeze |
| `a break` | a break → break (stopword dropped) |

Singularisation is deliberately conservative. **`squeezes` must singularise to
`squeeze`, not `squeez`** — an early rule stripped "es" from anything ending in
`zes` and broke one of the first three words ever tested. Only strip "es" where the
base genuinely ends in s/z/x/ch/sh (glasses→glass, boxes→box, watches→watch).

---

## Card spec

Matches the locked Communicate by Design symbol card standard: symbol + word label
+ Fitzgerald Key colored border only. No category bar, no star, no part-of-speech
label.

- **Sizes** 1" / 1.5" (default) / 2" / 2.5" / 3", true measured size
- **Cutting space** tight 1/16" / **standard 3/16" (default)** / wide 5/16"
- **Label** ALL CAPS (default), lowercase, or Title Case
- **Border** Fitzgerald Key color (default), black, light gray, or none
- Per-word copy counts, alternate-symbol picker, per-card search override

### Print rules that are load-bearing

- `orphans: 1; widows: 1` on `.cards` — the browser default of 2 silently throws
  away a whole printable row whenever the last row does not fit. This cost a row
  per page until it was found.
- Cards are `inline-flex` with margins, **not** flex-wrap with `gap`. Inline-level
  boxes fragment across printed pages reliably; flex containers do not.
- No hard-coded symbol/label heights — flexbox absorbs padding and border, so every
  border style and card size lays out correctly.
- The ARASAAC attribution is `position: fixed` in print. In flow it took a page of
  its own whenever cards filled the last page exactly. Fixed, it costs no flow
  space and prints on every page, with `padding-bottom` on `.cards` keeping cards
  clear of it.
- **Users must print at 100%, not "Fit to page."** Said in the tool's own help.

---

## Google Docs export

Drive converts an uploaded `.html` file into a Doc and fetches every remote image
into it, so a sheet can be handed to a team as an ordinary shared Doc. Verified by
round trip: uploaded, converted, read back — 108pt cells (1.5in exactly), each card
keeping its own embedded image, Fitzgerald borders and attribution intact.

Two things the export must do differently from the screen sheet:

1. **Tables, not inline-flex.** Google converts tables reliably; the on-screen card
   layout does not survive. The export serialises its own table.
2. **Spacer columns and rows for the cutting gap.** Google *discards*
   `border-spacing` outright — it rewrites the table to `border-collapse: collapse`
   and mashes the cells together. Empty spacer cells do survive. Google also floors
   a cell at about 20pt, so the Doc gap is at least 0.28in (wider than the printed
   sheet) and the column count accounts for it — 3 per row at 1.5in, not 4.

Symbols resolved from the local cache are file paths Google cannot reach, so the
export looks those up on ARASAAC first to get a public URL; anything still
unresolved exports as a draw-it box and the count is reported to the user.

---

## Fitzgerald Key classification

Ported from `_Operations/Build/fitzgerald_key.js` (GENERAL sets), plus a
movement/sensory/regulation extension so break-menu words classify correctly:
stretch, rub, squeeze, press, breathe, jump, march, roll, wiggle, shake, swing,
bounce, hug, tap, lift, carry, climb, rock, spin, crash, massage, brush, scratch,
tickle, pat, poke, squish, knead, compress, sway, wrap, hold, rest, relax, calm.

`scratch` was falling through to the noun default and printing a gray border on a
sensory menu. Anything added to a break or regulation board should be checked
against the green set before use.

The classification runs on the whole phrase first, then the head word — so
`back stretch` and `squeezes` both resolve to Action.

---

## Handing it to someone who does not code

**Email them the file. That is the whole handoff.** Verified by test: opened as a
plain double-clicked file in a folder with no symbol cache, calling a live
cross-origin API — all words resolved, zero CORS failures, cards rendered.

They need a browser, internet, and a printer. They do **not** need Claude Code, a
Claude account, any AI subscription, Node, Python, a terminal, GitHub, or any
install. The file never contacts Claude or Anthropic at runtime; its only outbound
request is to ARASAAC for a picture.

Instructions live **inside the file** — a "How to use this" panel, open for a
first-time visitor, remembered once collapsed, hidden when printing. A separate
instruction document is a thing to lose when the file gets forwarded.

---

## Licensing

- **ARASAAC** — CC BY-NC-SA 4.0. Non-commercial. Fine for a free tool; would block
  a paid version. Attribution prints on every sheet and must not be removed.
- **Mulberry Symbols** — CC BY-SA, permits commercial use. Reachable at
  `raw.githubusercontent.com/mulberrysymbols/mulberry-symbols/master/EN/{name}.svg`.
  Full index at `scripts/data/symbol-info-en.csv` (3,435 symbols with grammar and
  category). **Naming convention is `stretch_,_to`, not `stretch`** — guessing
  filenames without the index returns wrong symbols (a palm tree for "hands", a
  bottle of squash for "squeeze"). The index exists; use it.

**Do not mix symbol sets on one student's board.** A student learning symbols should
see one consistent set. If a second source is ever added to the tool, it must be a
per-sheet choice, never a silent per-card fallback.

---

## Open Decisions — before this becomes an official free product

Nothing below is decided. See CLAUDE.md → New Product Line Workflow (Phase 0).

1. **Name.** Currently "Symbol Card Sheet Generator"; file is
   `cbd-pecs-sheet-generator.html`. Two problems for an outward-facing download:
   "CbD" in a public filename breaks the spell-it-out rule, and PECS is a
   trademarked protocol (Pyramid Educational Consultants). Suggested approach —
   name it something like *Symbol Card Maker*, and capture the PECS search traffic
   in TPT tags and description instead of the product name.
2. **No links out.** Zero references to the TPT store or Substack. For a free
   product whose job is funnel-building, that is the point missing — and the file
   travels without Jill once it is emailed.
3. **No end matter.** No Accessibility Statement, About the Creator, or Terms of
   Use. Required in that order on teacher-facing materials.
4. **Distribution.** Recommendation: both, TPT first. TPT sells files and this is a
   file, so a free download works natively and drives follower growth before the
   May UFLI launch. Then host it (Netlify Drop or similar) so updates do not need a
   re-upload, and put that link in Substack, the Instagram bio, and Pinterest.
5. **Support burden.** A free public tool generates questions. Real cost on a
   one-person operation.

---

## Testing notes

Logic is covered by a throwaway Node harness (search chain, singularisation, slug,
Fitzgerald classification, label casing). Layout and print geometry were verified by
driving a real browser, generating PDFs and measuring the drawn boxes — that is how
the widows bug, the attribution page and the `squeez` bug were all caught. Anything
touching print layout should be re-verified the same way, not eyeballed.

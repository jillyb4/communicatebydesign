# Tasks
> ⚠️ **Primary tracking has moved to Airtable** — Base: `appeaT8hkeXWqQKIj`, table: Work Items. This file is a backup reference. At session start, read Airtable for current state.


## Active

- [ ] **Weekly TPT Traffic Check** — Every Saturday, pull Traffic tab on TPT dashboard (This week vs. Last week). Watch: (1) Facebook click-throughs — goal is 15+ sustained after Mar 28 surge driven by "That Statistic Is 33 Years Old" post; (2) Direct traffic trend — flag if drops below 80/week for 3+ consecutive weeks; (3) Conversion rate — currently 0.00%, needs product page optimization pass. Report template saved: `Marketing/TPT_Traffic_Report_2026-03-28.html`. *(Added 2026-03-28)*
- [ ] **Product page conversion audit** — 373 click-throughs this month, $0.00 earned = 0% conversion. Review top-traffic product listings: cover image, description opener (first 180 chars), pricing display, and thumbnail. Start with AT Checklist + AT Toolkit (highest direct traffic products). *(Added 2026-03-28)*

- [x] **Capitol Crawl** — LIVE on TPT ✓ $9.95 (confirmed 2026-03-26). Pin created on Pinterest ✓. Bundle with 504 Sit-In for Disability Pride Month (Jul). Launch Calendar updated to 🟢 Live ✓.
- [x] **CLAUDE.md status** — Zitkala-Ša + Frances Kelsey updated to LIVE ✓ (2026-03-27)
- [x] **AAC Trading Cards — resubmit 1-up format** — Done ✓ (confirmed 2026-03-27)
- [x] **Capitol Crawl preview PDF** — Uploaded to TPT ✓ (2026-03-26).
- [ ] **TPT audit** — Fill in TPT Zip, Thumbnails, and Preview PDF columns on Master Pipeline tab (`CbD_TPT_Launch_Calendar.xlsx`). 5 nonfiction previews uploaded ✓. Capitol Crawl pending. AT/AAC products need checking.
- [ ] **Preview PDFs — AT/AAC products** — Build preview PDFs for AT Checklist + AT Toolkit (highest traffic products). Include one page of symbol cards in every nonfiction/UFLI preview (shows the Fitzgerald Key trading card design — instant visual differentiator).
- [ ] **Re-upload nonfiction zips to TPT** — All 6 units have new `_Complete.zip` files with Symbol Cards + Printable Kit add-ons. Replace old uploads. Add note to listings: "Includes Word (.docx) and PDF formats. To use in Google Docs, upload the .docx to your Google Drive."
- [ ] **Substack: First TPT Drop post** — READY to publish. All TPT URLs + prices inserted. Just needs Canva thumbnails + publish. File: `Substack/Substack-FirstTPTDrop-Post.md`
- [ ] **TPT cross-linking audit** — Confirm freebies (Checklist, Finding Symbols) link TO paid products. Confirm Toolkit links FROM Checklist.
- [ ] **TPT Awards section** — Manual entry needed (content drafted).
- [ ] **AT certification** — Working toward; not yet started.
- [ ] **Nonfiction bundle** — Create Keiko + Radium Girls bundle listing on TPT.
- [x] **Earth Day keyword push** — Update Keiko listing with Earth Day keywords ✓ (completed 2026-03-26)
- [ ] **Add tag gold mines to TPT listings** — "aactivities" (all AAC products), "ulfi" (all UFLI products), "drawn to aac" (AAC tags), "special education lesson plans template" (nonfiction descriptions). Free wins — just paste into TPT tag fields.
- [ ] **Daily SellerSpy searches** — 5 free/day. Next batch: "core vocabulary", "adapted reading", "IEP tools", "phonics AAC", "disability history". Add results to `CbD_SEO_Keyword_Research.xlsx`.
- [ ] **Airtable: Link Work Items → Products table** — Products table (`tbl2YSRQiW7RHEPY5`) created with 32 records. Manually link Work Items tasks to their specific Product records in Airtable UI (or do in a future session).
- [ ] **Airtable: Delete 3 blank Work Items records** — Cannot delete via MCP. Do manually in Airtable: recacRAoUpf2Pm7K6, reccV2W1OY0Z4xHgI, recm3WsrttywsUP6p.
- [ ] **Airtable: Review "Operations" as Product Line** — "Operations" was added as a Product Line option but it's a rollup category, not a swim lane. Consider adding a separate "Rollup To" field to Work Items.
- [ ] **Rebuild CbD Dashboard** — Dashboard (`CbD_Dashboard_2026-03-27.html`) does not yet show Products table or Operations grouping. Rebuild when Airtable linking is done.
- [ ] **Archive Launch Calendar Excel** — `CbD_TPT_Launch_Calendar.xlsx` has been fully migrated to Airtable (Session 17). Move to `_Operations/Archive/` or delete. Do NOT use as a reference — Airtable Launch Pipeline table (`tblKDEYyrRdPOtbhX`) is now authoritative.
- [ ] **Ahrefs 7-day trial** — Start April 27. Run 7-day competitor research plan (see SEO spreadsheet → Ahrefs tab). CANCEL by May 2 at 9am PT.
- [x] **TPT title rewrites** — All 6 DONE ✓ (Radium Girls, Keiko, Frances Kelsey, 504 Sit-In, AT Checklist, Visual Schedule). Implemented March 24.

## Fiction Line — Active

- [ ] **Wonder: Character Analysis — fix Word open error** — Build script complete (`Products/Fiction Anchor Texts/Wonder - Character Analysis/build_wonder_character_analysis.js`). File builds (33KB) but Word throws "error opening file." File is structurally valid ZIP with valid XML. Removing secondary docx require() import didn't fix it. Next: test opening from iCloud path directly (not outputs folder); try libreoffice conversion as fallback; investigate if macOS quarantine attribute is blocking Word.
- [ ] **Wonder: DELETE wrong kit file** — `Wonder_Character_Analysis_Printable_Kit.docx` in Wonder folder is the wrong format (UFLI trading card size, built with build_unit_printable_kit.js). Delete manually — iCloud mount is read-only from sandbox.
- [ ] **Wonder: Fetch 8 missing ARASAAC symbols** — alone, belong, invisible, loyal, bully, ordinary, helmet, face looks different → fetch from ARASAAC API before building Printable Packet. Save to `_Operations/symbol_cache/`.
- [ ] **Wonder: Build Printable Packet** — Build `build_wonder_printable_packet.py` using fiction_printable_packet_spec.md. 9-page PDF: Layer 1 (partner setup) + Layer 2 (symbol cards — Set A 24 words) + Layer 3 (3 boards: Description A + Emotion B + Literary Moves C) + Layer 4a (vocab map) + Layer 4b (Session Tracker appended). Annotation codes LOCKED: [TRAIT] / [WHY] / [CHANGE]. Build AFTER Word open error is resolved.
- [ ] **Wonder: Character Analysis — decide pricing** — Nonfiction passage-count table doesn't apply. Whole-book fiction unit. Decide before listing. Candidates: $8.95 (aligns with 1-passage nonfiction), $9.95, or new tiered structure.
- [ ] **Fiction cover color — lock before building** — Direction: bright/light background (NOT dark navy), navy footer only. Hero color TBD — leading candidates: Electric Teal (#00B4D8) on white, or split treatment. Decide before building any cover. See `_Operations/memory/fiction_reference.md` Cover Design section.
- [ ] **Wonder: Character Analysis — add to Airtable** — Add product record to Products table and Launch Pipeline once pricing and cover are decided.
- [ ] **Fiction Visual Supports V2** — Visual Scene Displays for 4 Wonder scenes (first day / lunch scene / Halloween / graduation). Requires: original illustration source decision + file format decision (print PDF vs. interactive). Deferred to V2 — unit is launchable without them.

## Next Up (Build Queue)

- [ ] **Re-upload all 6 nonfiction units to TPT** — Session 16 updates: Communication Access section (new heading, opening statement, fringe para low-tech-first, V3 vocab rule note), hang-over pages fixed in Keiko, partner modes note, access verb language. New .docx files built. Replace existing TPT downloads.
- [ ] **V3 passage audit — all 6 units** — NEW RULE (Session 16): V3 passages must use core words + highest-frequency fringe only. Review V3 text in each unit against its fringe word list. Flag any V3-exclusive vocabulary that doesn't have a symbol. Priority: Keiko, then Radium Girls.
- [ ] **`cbd_aac_support.js` shared module** — BUILT ✓ (Session 16). Keiko + Radium Girls use it. Capitol Crawl, Zitkala-Sa, Frances Kelsey, 504 Sit-In still have inline framework text — migrate on next rebuild of those units.
- [ ] **Fix nonfiction build script require paths** — 5 of 6 scripts had `../../../../_Operations` (4 levels up) instead of `../../../_Operations` (3 levels). FIXED in Session 16, but note this for any new scripts — always 3 levels up from unit folder to `Communicate by Design/_Operations/`.
- [ ] **All the Way to the Top Companion** — NEW. Picture Book Companions sub-line, K–3. Plan DONE (`Products/Picture Book Companions/All the Way to the Top/AllTheWayToTheTop_Unit_PLAN.md`). Next: draft unit content section by section. Target: Disability Pride Month July 2026 (ADA anniversary July 26). Price: $5.
- [ ] **Jennifer Keelan bundle** — Pair "All the Way to the Top Companion" (K–3, $5) + Capitol Crawl 1990 ($9.95) = disability rights across grade bands. Create bundle listing once both are live.
- [ ] **Substack: "The Capitol Crawl Was a Child's Act of Resistance"** — Jennifer Keelan was 9 years old. Advocacy pillar post. Ties to both Capitol Crawl unit and All the Way to the Top companion. Target: July 2026 (ADA anniversary timing).
- [ ] **Haben Girma unit** — Completes Disability Rights triple bundle (504 + Capitol Crawl + Haben). Zero TPT competition.
- [ ] **Alternative Pencil Guide** — Jill actively building. Prerequisite for UFLI product line.
- [ ] **UFLI Teacher Guide** — Build first before per-lesson packets. July 2026 target.
- [ ] **Family sub-line F0 (freebie)** — Your AAC Quick-Start: 5 Things I Wish Someone Had Told Me. Lead magnet for family funnel.

## Someday

- [ ] Tommie Smith & John Carlos unit — BHM Feb 2027.
- [ ] Fiction line — Wonder: Character Analysis is Unit 1. See Active tasks.

## Completed

- [x] Nonfiction grade range 5–12 → 6–10 (Session 15) — All 6 build scripts, template, Master Reference, 12 listing/draft .md files updated. Step 0d added to nonfiction workflow. Zero stale refs remain.
- [x] Nonfiction preview PDFs (Session 15) — 6 branded 10-page watermarked previews built via `build_preview_pdfs.py`. 5 uploaded to TPT (Keiko, Radium Girls, Frances Kelsey, 504 Sit-In, Zitkala-Ša). Capitol Crawl built but pending listing.
- [x] TPT audit columns (Session 15) — Added TPT Zip, Thumbnails, Preview PDF columns to Master Pipeline tab in Launch Calendar.
- [x] File cleanup & reorganization (Session 15) — Downloads cleared (46 files sorted/deleted), Desktop cleared (53 files sorted), CbD internal cleanup (merged 504 folders, moved COMPLETE docs into units, removed duplicates, new Print References + Pinterest Pin Images folders).
- [x] CbD brand launch — Substack, TPT banner, Instagram all live.
- [x] IEP AT Consideration Toolkit — LIVE on TPT ($4, ID 15795702).
- [x] IEP AT Consideration Checklist (Freebie) — LIVE on TPT (ID 15796344).
- [x] AAC Communication Partner Quick Guide — LIVE on TPT ($3).
- [x] AAC Data Collection Forms — LIVE on TPT ($3).
- [x] Visual Schedule Template Pack — LIVE on TPT ($4).
- [x] AT & AAC Toolkit Bundle — LIVE on TPT ($10).
- [x] Finding Symbols (Freebie) — LIVE on TPT.
- [x] Keiko Part 1 Free Example — LIVE on TPT.
- [x] Keiko: A Whale's Journey — LIVE on TPT ($11.95).
- [x] Radium Girls — LIVE on TPT ($11.95).
- [x] Frances Kelsey — LIVE on TPT ($11.95).
- [x] Zitkala-Ša — LIVE on TPT ($9.95).
- [x] 504 Sit-In — LIVE on TPT ($11.95).
- [x] Zitkala-Ša .docx build — BUILT.
- [x] Capitol Crawl .docx build — BUILT.
- [x] 504 Sit-In .docx build — BUILT.
- [x] Frances Kelsey .docx build — BUILT.
- [x] Substack: First TPT Drop post — URLs + prices updated (2026-03-19).
- [x] Workflow reorganization — All workflows consolidated into `CbD_Production_Workflows.xlsx`. Preview PDF phase added to all 4 workflows.
- [x] Launch Calendar rebuild — Master Pipeline (one tab, all products), Frameworks tab, Fiction Line tab. Old 7-tab structure replaced.
- [x] **Launch Calendar → Airtable migration (Session 17)** — All content from `CbD_TPT_Launch_Calendar.xlsx` migrated to Airtable: Launch Pipeline table (68 records, `tblKDEYyrRdPOtbhX`), Instructional Activities table (6 records, `tblHJlkbCF7c4tCNP`), 16 Substack pipeline posts added to Work Items, 10 live-product action items added to Work Items. Excel is deprecated.
- [x] TPT price update — Toolkit $4, Comm Partner $3, Data Collection $3, Visual Schedule $4, Bundle $10.

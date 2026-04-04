# QC Report — What the Voice Carries (Poetry Reading Unit 1)
**Date:** April 3, 2026
**Reviewer:** Claude (Cowork)
**Files checked:** COMPLETE.pdf · COMPLETE.docx · Student Packet PDF · CAP PDF · Session Tracker PDF

---

## Summary

| File | Status |
|------|--------|
| COMPLETE.docx | ✅ PASS (rebuilt with fixes applied) |
| COMPLETE.pdf | ⚠️ NEEDS RE-EXPORT FROM WORD (see below) |
| Student Packet PDF | ✅ PASS (rebuilt with fixes applied) |
| CAP PDF | ✅ PASS |
| Session Tracker PDF | ✅ PASS |

---

## Issues Found and Resolved

### 🔴 FIXED — Cover Page: Wrong Product Line Label
**File:** COMPLETE.pdf / COMPLETE.docx
**Issue:** Cover page read "A Nonfiction Reading Unit" — must say "A Poetry Reading Unit"
**Root cause:** `titlePage()` in `cbd_docx_template.js` had "A Nonfiction Reading Unit" hardcoded
**Fix applied:** Added `opts.productLine` parameter to `titlePage()` in template (falls back to "A Nonfiction Reading Unit" for all existing nonfiction units — no breakage). Added `productLine: "A Poetry Reading Unit"` to `build_poetry_unit1.js`. COMPLETE.docx rebuilt.

### 🔴 FIXED — Student Packet PDF: Missing Metadata
**File:** What_the_Voice_Carries_Student_Packet.pdf
**Issue:** `Author: anonymous`, `Title: untitled` — violates accessibility and brand standards
**Fix applied:** Added `setTitle()`, `setAuthor()`, `setSubject()`, `setCreator()` calls to `build_poetry_student_packet.py`. PDF rebuilt. Verified metadata now correct.

### 🔴 FIXED — Student Packet: "Point to" as Sole Interaction Verb on Cover NFMA Guide
**File:** What_the_Voice_Carries_Student_Packet.pdf
**Issue:** A — ASK step on cover page read "Point to evidence from the poem" with no AAC alternative
**CbD rule:** "point to" must never be the sole interaction verb — add "select, point to, or indicate"
**Fix applied:** Updated to "Point to, select, or indicate evidence from the poem." in `build_poetry_student_packet.py`. PDF rebuilt.

### 🔴 FIXED — SLP Gatekeeping Language
**File:** COMPLETE.docx (Sections 5–6 of build script)
**Issues found:**
1. Section heading: "Semi-Core Words — Verify with SLP Before Day 1" → SLP listed as sole responsible party
2. Body text: "confirm with the SLP before the unit begins" → frames SLP as gatekeeper
3. Section heading: "CAP Vocabulary — SLP Handoff" → implies the SLP alone receives the CAP
4. Body text: "Send the Communication Access Packet to the SLP at least two weeks before Day 1" + "The SLP should confirm..." → SLP-only framing

**Fixes applied to `build_poetry_unit1.js`:**
1. Heading → "Semi-Core Words — Verify Before Day 1"
2. Body → "the team should confirm they are accessible before the unit begins"
3. Heading → "CAP Vocabulary — Team Coordination"
4. Body → "Share the Communication Access Packet with all team members — including the SLP, if one is on the team" + "The team should confirm..."

COMPLETE.docx rebuilt.

---

## ⚠️ Jill Action Required — Re-Export COMPLETE.pdf from Word

**Issue:** The existing `What_the_Voice_Carries_COMPLETE.pdf` was produced by LibreOffice 26.2.2.2
**CbD rule:** All PDFs must be exported via Word → File → Save As → PDF (not Print to PDF, not LibreOffice)
**Status:** COMPLETE.docx has been rebuilt with all fixes above. You must re-export from Word.

**Steps:**
1. Open `What_the_Voice_Carries_COMPLETE.docx` in Microsoft Word
2. File → Save As → PDF
3. Save as `What_the_Voice_Carries_COMPLETE.pdf` (overwrite existing)
4. Verify the cover page reads "A Poetry Reading Unit" ✓

---

## Checks That Passed

| Check | Result |
|-------|--------|
| End matter order (Accessibility → About → Terms) | ✅ PASS |
| "The scaffold varies. The expectation does not." present | ✅ PASS |
| No banned terms: nonverbal, AT Specialist, AAC Specialist | ✅ PASS |
| No "above/below grade level," "struggling readers" | ✅ PASS |
| Section heading: "Communication Access" (not "AAC Support") | ✅ PASS |
| "point to" in COMPLETE.pdf always accompanied by other AAC modalities (except Student Packet — FIXED) | ✅ PASS |
| CAP section heading: "Communication Access Packet" (not "AAC Support") | ✅ PASS |
| CAP metadata: Title, Author, Subject correct | ✅ PASS |
| Session Tracker metadata: Title, Author, Subject correct | ✅ PASS |
| Page counts: COMPLETE 13pp · Student Packet 13pp · CAP 12pp · Session Tracker 6pp | ✅ PASS |
| Build script has 12 sections: About · Standards · NFMA Strategy · Meet the Poems · Vocab Preview · Comm Access · Partner Guidance · Version Guide · 4 Poem NFMA Activities · Synthesis · IEP Goals · Rubric · End Matter | ✅ PASS |
| NFMA framework (NOTICE/FEEL/MEAN/ASK) present and explained | ✅ PASS |
| IEP goal stems present (academic ELA + AAC communication goal) | ✅ PASS |
| Rubric present (4-criterion, behavioral descriptors) | ✅ PASS |
| Versions field on cover: "Poetry Reading Unit · NFMA Strategy" | ✅ PASS (after fix) |

---

## Sections Present in COMPLETE.docx

The poetry unit uses a 12-section architecture (different from nonfiction's 22-section spec — poetry line has its own spec):

1. About This Unit
2. Standards Alignment
3. The NFMA Strategy
4. Meet the Poems
5. Vocabulary Preview
6. Communication Access
7. Communication Partner Guidance
8. Version Guide
9–12. Poem NFMA Activities (× 4 poems)
13. Synthesis Activity
14. IEP Goal Stems
15. Rubric
16. End Matter (Accessibility → About → Terms)

**Note:** Pacing Guide, UDL Teacher Notes, Differentiating section, Modeling (HLP 16), and Checkpoint Protocol sections are present in nonfiction units but were not included in this poetry unit build spec. Confirm with Jill whether these are needed for the poetry line before marking QC fully passed.

---

## Files Modified This Session

| File | Change |
|------|--------|
| `cbd_docx_template.js` | `titlePage()` now accepts `opts.productLine` — defaults to "A Nonfiction Reading Unit" for backward compat |
| `build_poetry_unit1.js` | Added `productLine: "A Poetry Reading Unit"` to `titlePage()` call; fixed SLP gatekeeping in Sections 5–6 |
| `build_poetry_student_packet.py` | Added PDF metadata (Title, Author, Subject, Creator); fixed "Point to" → "Point to, select, or indicate" on cover |
| `What_the_Voice_Carries_COMPLETE.docx` | Rebuilt — all build script fixes applied |
| `What_the_Voice_Carries_Student_Packet.pdf` | Rebuilt — metadata + AAC language fixes applied |

---

## GitHub Push

Code changes pending push:
- `_Operations/cbd_docx_template.js`
- `Products/Poetry Reading Units/Unit 1 - What the Voice Carries/build_poetry_unit1.js`
- `Products/Poetry Reading Units/Unit 1 - What the Voice Carries/build_poetry_student_packet.py`

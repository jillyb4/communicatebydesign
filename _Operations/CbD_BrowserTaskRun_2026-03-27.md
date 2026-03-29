# Communicate by Design — Browser Task Run Report
**Date:** March 27, 2026
**Run Type:** Scheduled automated task
**Triggered by:** CbD scheduled task queue (Airtable base `appeaT8hkeXWqQKIj`)

---

## Summary

7 tasks were in the Ready queue. 2 were completed fully. 1 produced actionable findings. 4 were blocked and documented.

---

## ✅ COMPLETED

### 1. Nonfiction Bundle — Keiko + Radium Girls
**Task:** Create bundle listing on TPT
**Result:** Bundle created and saved as **INACTIVE DRAFT** (not live).

- **Title:** Nonfiction Bundle | Keiko + Radium Girls | Adapted Reading | SPED Grades 6-10
- **Product ID:** 15922531
- **Edit URL:** https://www.teacherspayteachers.com/itemsBundle/editNext/15922531
- **Price:** $18.00 discount (list: $21.90 — saves $3.90)
- **Products included:** Keiko ($9.95) + Radium Girls ($11.95)
- **Grades:** 6th–9th (TPT max 4; 10th grade needs to be added manually)
- **Subject Area:** Reading
- **Tags:** AAC, Neurodiversity, Women's History Month
- **Tax Code:** Digital books sold to an end user with rights for permanent use
- **Status:** INACTIVE — will not appear in search or notify followers until Jill activates

**Jill needs to:**
- [ ] Add thumbnail (upload from Canva)
- [ ] Verify description and price
- [ ] Add 10th Grade to grade levels (currently maxed at 4: 6–9)
- [ ] Activate listing when ready

---

### 2. Already-Done Record Cleanup *(completed in previous session)*
3 Airtable records had Status=Done but Ready to Pick Up=true. All unchecked.

---

## 🔍 AUDIT COMPLETE — ACTION NEEDED BY JILL

### 3. TPT Cross-Linking Audit
**Task:** Confirm AT Checklist and AT Toolkit link to each other
**Result:** **Both cross-links are MISSING.**

Findings:
- **AT Consideration Checklist** (ID: 15796344) — description does NOT contain a link to the AT Consideration Toolkit
- **AT Consideration Toolkit** (ID: 15795702) — description does NOT contain a link to the AT Consideration Checklist
- Also confirmed: "Finding Symbols for AAC Visual Supports" (free, $0.00) exists in store

**Jill needs to:**
- [ ] Edit AT Checklist description → add link to the Toolkit
- [ ] Edit AT Toolkit description → add link to the Checklist
- Both edits are manual (TPT description editor required)

**Airtable Next Action updated** with specific instructions.

---

## ❌ BLOCKED — Cannot Execute in Automated Session

### 4. Add Tag Gold Mines to All TPT Listings
**Reason:** TPT no longer supports free-form custom tags. The Tag field is a **structured dropdown only** (Theme, Audience, Language — preset options only). Tags `aactivities`, `drawn to aac`, `ulfi`, and `special education lesson plans template` are **not valid options** in the current TPT interface.
**Recommendation:** Delete or rewrite this task. The old tag strategy is obsolete. Jill should use the structured Tag dropdown when editing listings (e.g., select "AAC" under Speech Therapy, "Special Education" under Supports, etc.).
**Airtable:** Status → Done, Ready → unchecked, Notes updated.

---

### 5. First TPT Drop — Substack Post
**Reason:** Post content is ready (`Substack/Substack-FirstTPTDrop-Post.md`), but it contains 5 `[Insert thumbnail: ...]` placeholders requiring phone photos of each product. Cannot publish without images.
**Jill needs to:**
- [ ] Take phone photos of each product printout (5 photos)
- [ ] Insert photos into the Substack draft
- [ ] Publish
**Airtable:** Status remains Ready. No change.

---

### 6. Daily SellerSpy Searches (5 keywords)
**Reason:** SellerSpy requires an active authenticated browser session. Automated scheduled tasks cannot log in.
**Keywords to run when logged in:** `core vocabulary`, `adapted reading`, `IEP tools`, `phonics AAC`, `disability history`
**Log results to:** `_Operations/TPT/CbD_SEO_Keyword_Research.xlsx`
**Airtable:** Notes updated with blocked status and keyword list. Ready to Pick Up remains checked for next manual session.

---

### 7. TPT Awards Section
**Reason:** Airtable notes say "content already drafted" but no content was provided in the Notes field or linked document. Cannot enter content that doesn't exist in a known location.
**Jill needs to:**
- [ ] Paste the drafted awards content into the Notes field in Airtable, OR
- [ ] Share the document where it lives so it can be located and entered
**Airtable:** No change.

---

### 8. Re-upload Nonfiction Zips — 6 Units
**Reason:** Requires uploading local files from Jill's computer to TPT. Scheduled tasks run in a sandboxed environment without access to local file paths.
**Jill needs to:**
- [ ] Use Cowork mode (with folder access) to upload the 6 `_Complete.zip` files to each TPT product
- [ ] Units: Keiko, Radium Girls, Zitkala-Ša, 504 Sit-In, Frances Kelsey, Capitol Crawl
**Airtable:** No change. Flag for a Cowork session.

---

## Airtable Changes Made This Session

| Record | Task | Change |
|--------|------|--------|
| recZZeS91lf1oQpVT | Nonfiction bundle | Status → Done, Ready → false, Notes updated |
| reclD4uVJEu58meJ8 | Tag gold mines | Status → Done, Ready → false, Notes updated (blocked, TPT changed) |
| recjIg47gn3GVrren | Cross-linking audit | Next Action updated with specific instructions, Notes updated |
| recoww6Woq018Nzyq | SellerSpy searches | Notes updated (blocked, manual only) |

---

## Platform Discovery (New Information)

- **TPT Tag system changed:** Free-form custom tags are no longer supported. The Tag field is now a structured dropdown (preset options only). All future tag tasks must reference valid preset options.
- **"Finding Symbols for AAC Visual Supports"** exists as a free product in the CbD TPT store (confirmed during bundle product selector review).
- **Bundle product count:** Store now has **15 items** (14 active + 1 new inactive bundle draft).

---

*Report generated by scheduled CbD browser task run — March 27, 2026*

# CbD Accessible Document Research & Implementation Plan

**Date:** March 17, 2026
**Purpose:** Research the legal landscape for digital document accessibility, audit CbD's current build system, and create a plan to make every CbD product meet the highest accessibility bar — not just because the law requires it, but because a brand that teaches disability rights curriculum in inaccessible formats isn't walking the talk.

---

## Part 1: The Legal Landscape

### Federal Law — What Applies to CbD

**Three federal laws create the accessibility floor for educational documents:**

**1. ADA Title II (Updated April 2024, Compliance Deadline April 24, 2026)**

The Department of Justice finalized new ADA Title II regulations requiring state and local government entities — including public K-12 schools — to make all digital content conform to WCAG 2.1 Level AA. This is the first time the ADA has explicitly named a technical standard for digital accessibility.

What it means for CbD: When a school district purchases CbD materials and distributes them to students, those materials become part of the district's digital ecosystem. If a district is audited for ADA Title II compliance and a CbD PDF or Word document fails accessibility checks, the district bears the legal liability — but CbD bears the reputational damage. Districts with sophisticated accessibility coordinators will start vetting purchased materials before adoption. An accessible product is a competitive advantage right now. Within two years, it will be table stakes.

Deadline by district size: Population 50,000+ must comply by April 24, 2026. Under 50,000 by April 26, 2027.

**2. Section 508 of the Rehabilitation Act (Refreshed 2017, WCAG 2.2 incorporated 2024)**

Section 508 requires all electronic and information technology developed, procured, or used by federal agencies to be accessible. The 2017 refresh explicitly incorporated WCAG 2.0 Level AA. The 2024 update incorporated WCAG 2.2.

What it means for CbD: Section 508 doesn't directly regulate TPT sellers. But it sets the standard that cascades into state procurement rules. When a federally-funded school uses IDEA money to buy instructional materials, the spirit of Section 508 follows the dollars. More practically: Section 508 defines what "accessible" means in government procurement, and school districts increasingly mirror these requirements.

The key Section 508 rule for documents: Electronic documents must meet WCAG 2.0 Level A and AA success criteria. The term "document" replaces "web page" — every WCAG requirement that applies to a web page also applies to a PDF or Word file. A document that fails even one of the 38 applicable success criteria does not conform.

**3. IDEA — Accessible Educational Materials (AEM)**

IDEA requires schools to provide accessible educational materials (AEM) to students with disabilities so they can access the general education curriculum. The four accessible formats specified are braille, large print, audio, and digital text. When a student's IEP requires AEM, the district must provide it without delay.

What it means for CbD: CbD's entire audience is SPED teams serving students who need AEM. If a CbD product arrives as a flat PDF (no tags, no reading order, no alt text), the SLP or resource teacher has to rebuild it before it can be used with their students. That's not a product — it's a burden. An AEM-ready product saves the team hours and signals that CbD understands their world.

### Washington State Law

**WaTech Policy USER-01 (Digital Accessibility Policy)**

Washington requires all state agency digital services to meet WCAG 2.1 Level AA at minimum. By July 1, 2026, the standard rises to WCAG 2.2 AA. By July 1, 2029, all tools necessary for job performance or public access must be accessible. Agencies must designate an accessibility coordinator, develop IT Accessibility Plans, and conduct annual training.

What it means for CbD: Washington school districts are state entities. As they build compliance infrastructure for the 2026 and 2029 deadlines, they will scrutinize every digital product in their ecosystem — including purchased curriculum. CbD is based in Washington. The optics of a Washington-based disability-focused brand selling inaccessible documents to Washington schools are not great.

### Summary: What Standard Should CbD Meet?

| Standard | Required By | Level | CbD Decision |
|----------|------------|-------|-------------|
| WCAG 2.1 AA | ADA Title II (2026 deadline) | Legal floor for public schools | **Minimum** |
| WCAG 2.2 AA | Section 508 (2024), WA State (July 2026) | Federal + state floor | **Target** |
| WCAG 2.2 AAA (selected criteria) | Best practice, not legally required | Gold standard | **Aspiration for key criteria** |
| AEM readiness | IDEA | Functional requirement for SPED | **Non-negotiable** |

**CbD's standard: WCAG 2.2 AA conformance for every product, with AEM readiness built in.** This means every document — PDF and DOCX — must pass every applicable WCAG 2.2 AA success criterion. No exceptions.

---

## Part 2: What WCAG 2.2 AA Requires for Documents

### The Checklist — Every Applicable Criterion for DOCX and PDF

**Structure & Navigation**

| Requirement | WCAG Criterion | What It Means for CbD Documents |
|-------------|---------------|--------------------------------|
| Heading hierarchy | 1.3.1 (Info & Relationships) | Use Heading 1, 2, 3 in order. Never skip levels. Every section must be navigable by heading. |
| Reading order | 1.3.2 (Meaningful Sequence) | Screen readers must encounter content in the correct order. Tables, sidebars, and multi-column layouts are high-risk areas. |
| Lists as lists | 1.3.1 | Bulleted and numbered content must use real list formatting, not manually typed dashes or numbers. |
| Tables with headers | 1.3.1 | Every data table must have a defined header row. Screen readers use headers to describe relationships between cells. |
| No tables for layout | 1.3.1 | Tables used purely for visual layout (e.g., side-by-side boxes) must be avoided or tagged as presentational. |
| Document language | 3.1.1 (Language of Page) | The document's primary language must be set (English). |
| Document title | 2.4.2 (Page Titled) | The document must have a meaningful title in its properties (not "Document1"). |
| Bookmarks / TOC | 2.4.1 (Bypass Blocks) | Long documents must provide a way to skip to sections. A generated Table of Contents with hyperlinks satisfies this. |

**Text & Color**

| Requirement | WCAG Criterion | What It Means for CbD Documents |
|-------------|---------------|--------------------------------|
| Color contrast (normal text) | 1.4.3 (Contrast Minimum) | 4.5:1 ratio minimum for text smaller than 18pt (or 14pt bold). |
| Color contrast (large text) | 1.4.3 | 3:1 ratio minimum for text 18pt+ (or 14pt+ bold). |
| Don't use color alone | 1.4.1 (Use of Color) | If color conveys meaning (e.g., red = wrong), add text or a symbol too. |
| Resizable text | 1.4.4 (Resize Text) | Text must be resizable to 200% without loss of content. For DOCX, this is inherent. For PDF, avoid image-based text. |
| Real text, not images of text | 1.4.5 (Images of Text) | Never use a screenshot or image of text. All text must be selectable, searchable, and readable by screen readers. |

**Images & Media**

| Requirement | WCAG Criterion | What It Means for CbD Documents |
|-------------|---------------|--------------------------------|
| Alt text for informational images | 1.1.1 (Non-text Content) | Every image that conveys information must have concise, meaningful alt text. |
| Decorative images marked decorative | 1.1.1 | Images that are purely decorative (borders, spacers) must be marked as artifacts/decorative so screen readers skip them. |

**Links & Navigation**

| Requirement | WCAG Criterion | What It Means for CbD Documents |
|-------------|---------------|--------------------------------|
| Descriptive link text | 2.4.4 (Link Purpose in Context) | "Click here" is not accessible. Links must describe their destination. |
| Consistent navigation | 3.2.3 | Repeated navigation elements (headers, footers) should appear consistently. |

**Forms & Interactivity** (for Google Docs / fillable PDFs)

| Requirement | WCAG Criterion | What It Means for CbD Documents |
|-------------|---------------|--------------------------------|
| Form field labels | 1.3.1 / 4.1.2 | Every fillable field must have a visible label and a programmatic label (tooltip). |
| Error identification | 3.3.1 | If validation exists, errors must be described in text. |

---

## Part 3: Auditing the Current CbD Build System

### What `cbd_docx_template.js` Does Right

The template system uses the `docx` npm library to generate Word documents programmatically. Several things are already working for accessibility:

| Element | Current State | Assessment |
|---------|--------------|------------|
| **Heading hierarchy** | Uses `HeadingLevel.HEADING_1`, `HEADING_2`, `HEADING_3` correctly | **PASS** — proper semantic headings are generated |
| **Table header rows** | Sets `tableHeader: true` on first row | **PASS** — screen readers will identify header rows |
| **Table row splitting** | Uses `cantSplit: true` to prevent rows from breaking across pages | **PASS** — improves readability for all users |
| **Font consistency** | Single font (Arial) throughout | **PASS** — consistent, readable sans-serif |
| **Navy body text on white** | Contrast ratio 16.08:1 | **PASS AAA** — excellent |
| **White on Navy headers** | Contrast ratio 16.08:1 | **PASS AAA** — excellent |
| **Navy on light gray rows** | Contrast ratio 14.85:1 | **PASS AAA** — excellent |
| **Navy on amber callout** | Contrast ratio 9.21:1 | **PASS AAA** — excellent |

### What Fails or Is Missing

| Element | Current State | Assessment | Impact |
|---------|--------------|------------|--------|
| **Teal (#00B4D8) headings on white** | Contrast ratio **2.46:1** | **FAIL AA — CRITICAL** | Every H3 heading in the document is invisible to low-vision users. This is a WCAG 1.4.3 violation. |
| **Teal on light gray** | Contrast ratio **2.28:1** | **FAIL AA — CRITICAL** | Teal text on alternating gray table rows fails even worse. |
| **Amber on white** | Contrast ratio **1.75:1** | **FAIL AA** | Amber text directly on white would fail, though the template currently uses Amber only for borders and on navy backgrounds (which passes). Verify no amber text appears on white. |
| **Document title** | Not set in document properties | **FAIL** | `docx` library supports `title` in Document constructor but it's not being set. Screen readers announce "Document1" instead of "The 504 Sit-In: Who Tells the Story?" |
| **Document language** | Not set | **FAIL** | No `language` property set. Screen readers may mispronounce words or use wrong pronunciation rules. |
| **Alt text for images** | No images currently, but no system exists | **GAP** | If CbD adds logos, icons, or diagrams, there's no alt text infrastructure. The title page likely needs a brand logo at some point. |
| **List formatting** | Uses manual paragraphs with bold prefixes instead of real lists | **FAIL** | Bulleted content (MLL strategies, intervention strategies, AAC access pathways) is rendered as indented paragraphs. Screen readers cannot identify them as list items. |
| **Reading order in complex layouts** | No explicit reading order management | **GAP** | The template generates content sequentially, which naturally creates correct reading order. But multi-column layouts or sidebars would break this. Currently safe; needs attention if layout complexity increases. |
| **Table alt text / captions** | No table descriptions | **FAIL** | Data tables (pacing guide, standards alignment, vocabulary) have no summary or caption. Screen reader users encounter tables without context. |
| **Bookmark / TOC hyperlinks** | `TableOfContents` is generated but may not create clickable hyperlinks in all contexts | **VERIFY** | Need to test whether the generated TOC actually allows navigation in assistive technology. |
| **Color-only meaning** | Version labels may rely on gray color to indicate "discrete" status | **VERIFY** | If version labels are only distinguished by color (gray vs. black), this fails WCAG 1.4.1. |

### The Teal Problem — This Is the Big One

The Teal heading color (#00B4D8) on white background has a contrast ratio of **2.46:1**. WCAG AA requires **4.5:1** for normal text and **3:1** for large text. CbD's H3 headings are 12pt (24 half-points), which is NOT large text under WCAG (large = 18pt+ or 14pt+ bold). So H3 headings need the full 4.5:1 ratio and fail at 2.46:1.

**This means every Heading 3 in every CbD document is a WCAG violation.**

Options for fixing teal:

| Option | New Color | Contrast on White | Contrast on Gray | Notes |
|--------|-----------|-------------------|-------------------|-------|
| Darken teal to pass AA | #007A94 | ~5.2:1 | ~4.8:1 | Still recognizably "teal," darker and more saturated. Maintains brand identity. |
| Darken teal to pass AAA | #006478 | ~7.1:1 | ~6.5:1 | Deeper teal, close to dark cyan. Very readable. |
| Use navy for all text, teal for borders/accents only | N/A | N/A | N/A | Eliminates the problem entirely. Teal appears as decorative borders, not text. |
| Increase H3 font size to 18pt+ (large text threshold) | #00B4D8 | 2.46:1 | 2.28:1 | Still fails even at the 3:1 large-text threshold. Not viable. |

**Recommendation:** Darken teal to **#0077B6** (a deeper ocean teal that lands at ~5.5:1 on white). This passes AA for normal text, stays visually in the teal family, and differentiates from navy. Alternatively, use the current teal ONLY for decorative borders (which have no contrast requirement) and switch all teal text to navy.

---

## Part 4: The Format Question — PDF vs. DOCX vs. Google Docs

### Accessibility Comparison

| Factor | DOCX | PDF | Google Docs |
|--------|------|-----|-------------|
| **Screen reader support** | Excellent — native heading navigation, list detection, table header support | Excellent IF properly tagged; broken if not | Good but inconsistent across screen readers; requires keyboard shortcut knowledge |
| **Heading navigation** | Full support | Full support if tagged | Full support |
| **Table accessibility** | Header rows propagate to AT | Requires TH/TD tags with scope | **Tables lose proper formatting when exported to PDF** — cells convert to paragraph tags |
| **Alt text** | Supported natively | Supported if tagged | Supported |
| **Editability for teachers** | High — teachers can modify for their students | Low (without Acrobat Pro) | High |
| **AEM adaptability** | Can be easily converted to large print, read aloud by built-in tools, or converted to other formats | Locked format — hard to adapt | Easy to adapt |
| **Text-to-speech** | Built-in Read Aloud (Word, OneNote, Immersive Reader) | Requires tagged PDF + external TTS | Built-in (Read Aloud in Google Docs) |
| **TPT delivery format** | Accepted | Standard for TPT | Link-based (Google Drive) |
| **PDF export quality** | "Save As PDF" preserves tags if done correctly | N/A | **Exports lose table structure** — critical failure |

### Recommendation for CbD

**Primary format: DOCX (accessible Word document).**
Reasons: SPED teachers need to adapt materials. Word's built-in accessibility tools (Read Aloud, Immersive Reader, Accessibility Checker) are already on most school devices. The `docx` npm library gives us programmatic control over every accessibility feature. A properly built DOCX passes accessibility checkers out of the box.

**Secondary format: Tagged PDF (generated from the accessible DOCX).**
Reasons: TPT customers expect PDFs. Many teachers print and distribute. The key: generate the PDF FROM the accessible DOCX using Word's "Save As PDF" with the "Document structure tags for accessibility" checkbox enabled. Never print to PDF. Never use a PDF library that strips tags.

**Google Docs: Provide as optional editable version only.**
Reasons: Google Docs loses table structure on export and has inconsistent screen reader behavior. It's useful for teachers who want to edit, but it should not be the primary accessible format. Include a note: "For the most accessible version, use the Word document with Microsoft's Immersive Reader."

---

## Part 5: Implementation Plan for `cbd_docx_template.js`

### Priority 1 — Fix What's Broken (WCAG Violations)

| Change | What to Do | Where in Template | Difficulty |
|--------|-----------|-------------------|-----------|
| **Fix teal contrast** | Change `TEAL` constant from `00B4D8` to `0077B6` (or chosen accessible teal). Test against white AND gray backgrounds. | Line 55: `const TEAL = "00B4D8"` → `"0077B6"` | Easy — single line change, but needs brand approval |
| **Set document title** | Add `title` property to Document constructor. Pass unit title from build script. | Document constructor in assembly function | Easy |
| **Set document language** | Add `language` property to styles/document. | Document constructor | Easy |
| **Fix list formatting** | Create a `bulletList(items)` helper that uses real `numbering` configuration instead of indented paragraphs. | New helper function | Medium |
| **Add table captions** | Add a paragraph before each data table with a brief description (e.g., "Table: CCSS Standards Alignment — Primary standards, descriptions, and where they appear in the unit"). | New `tableCaption(text)` helper | Easy |

### Priority 2 — Add What's Missing (WCAG Gaps)

| Change | What to Do | Where in Template | Difficulty |
|--------|-----------|-------------------|-----------|
| **Alt text infrastructure** | Add `altText` parameter to any function that inserts images. Even if no images exist yet, build the pipeline so it's impossible to add an image without alt text. | Image-related functions (currently none — build proactively) | Easy |
| **Decorative image marking** | When brand elements (borders, dividers) are added as images, mark them as decorative (empty alt text, artifact tagging). | Future image functions | Easy |
| **Verify TOC navigation** | Test generated TOC in NVDA and Word's Accessibility Checker. Ensure links are functional. | Test — no code change unless broken | Medium |
| **Verify color-only meaning** | Audit all version labels, callout boxes, and status indicators. If any use color alone, add text labels. | Audit pass across all helper functions | Easy |

### Priority 3 — Reach the Highest Bar (Beyond Compliance)

| Change | What to Do | Why | Difficulty |
|--------|-----------|-----|-----------|
| **Add Accessibility Statement to every product** | Include a brief statement in the teacher documents: "This document was designed to meet WCAG 2.2 AA accessibility standards. It is compatible with screen readers, text-to-speech tools, and assistive technology. If you encounter an accessibility barrier, contact communicatebydesign@[email]." | Signals commitment. Normalizes accessibility as a quality standard. Gives users a way to report issues. | Easy |
| **Add "Using This Document with Assistive Technology" section** | Brief teacher note: how to use Read Aloud, Immersive Reader, or screen reader with this document. Specific instructions for text-to-speech with the reading passages. | Most SPED teachers don't know their school's AT tools can read Word docs aloud. This section activates tools they already have. | Medium |
| **Test with actual screen reader** | Run NVDA (free) on the generated DOCX. Navigate by heading. Read a table. Verify reading order. Document any failures. | Automated checkers catch ~30% of issues. Manual testing catches the rest. | Medium |
| **Offer text-only version** | Provide a clean, unformatted text version (.txt or .md) of reading passages for teachers who need to reformat for specific AT systems (e.g., refreshable braille displays). | Maximum AEM flexibility. Costs nothing to generate since the content already exists in markdown. | Easy |
| **AAA contrast where possible** | Aim for 7:1 contrast ratio on body text (already achieved with Navy on white at 16.08:1). Apply the same standard to all text elements. | Exceeding the minimum costs nothing and benefits everyone. | Already done for most elements |

### Priority 4 — Brand Decision Required

| Decision | Options | Who Decides | Impact |
|----------|---------|------------|--------|
| **Teal color adjustment** | (A) Darken to #0077B6 across all brand materials, (B) Keep #00B4D8 for decorative/border use only and use navy for all text, (C) Use a two-teal system — dark teal for text, bright teal for non-text accents | Jill | Affects every CbD product and platform. Needs to happen before the .docx build. |
| **Accessibility statement wording** | Draft provided above — needs Jill's voice | Jill | Goes in every product going forward. |
| **Format delivery strategy** | DOCX primary + tagged PDF secondary + optional Google Docs link | Jill + TPT store requirements | Affects TPT listings, file preparation workflow. |

---

## Part 6: The "Walking the Talk" Standard

CbD is a brand built on the premise that every learner deserves access. The unit we just drafted includes 26 core words, 19 fringe words, AAC access pathways for every activity, and IEP goal stems. It would be incoherent to deliver that content in a document that a screen reader can't navigate.

The legal minimum is WCAG 2.1 AA by April 2026. CbD should exceed it — not because of legal exposure (TPT sellers are not direct targets of ADA Title II enforcement), but because:

1. **CbD's customers are the people who enforce accessibility in schools.** They will notice.
2. **CbD's content is about disability rights.** The 504 Sit-In unit literally teaches students that the government's refusal to enforce accessibility law was a civil rights violation. The irony of delivering that lesson in an inaccessible document would not be subtle.
3. **Accessible documents are better documents for everyone.** Proper heading structure, reading order, and contrast benefit sighted users, printability, and searchability.
4. **It's a competitive differentiator.** No TPT seller in the SPED nonfiction space is marketing WCAG-conformant products. Being first to say "Accessible by design" — and mean it — positions CbD as the professional-grade option.

The tagline is *Where AT Meets Practice.* This is the practice.

---

## Sources

### Federal Laws & Standards
- [Section 508 Laws and Policies](https://www.section508.gov/manage/laws-and-policies/)
- [Section 508 Applicability & Conformance Requirements](https://www.section508.gov/develop/applicability-conformance/)
- [U.S. Access Board — Revised 508 Standards](https://www.access-board.gov/ict/)
- [Access Board Updates ICT Requirements](https://www.section508.gov/blog/access-board-updates-ict-requirements/)
- [Section 508 Compliance: 2026 Requirements Guide](https://www.levelaccess.com/compliance-overview/section-508-compliance/)
- [Understanding Digital Accessibility Before the ADA Title II Deadline](https://www.astho.org/communications/blog/2025/understanding-digital-accessibility-before-ada-title-ii-deadline/)
- [ADA Title II: What K-12 Schools Need to Know](https://www.k12dive.com/news/schools-colleges-title-ii-digital-accessibility/715184/)
- [Public School ADA Website Compliance](https://www.accessibility.works/blog/k-as-public-school-digital-web-accessibility-compliance/)

### Washington State
- [WaTech Digital Accessibility Policy](https://watech.wa.gov/policies/digital-accessibility-policy)
- [WaTech Digital Accessibility Standard](https://watech.wa.gov/policies/digital-accessibility-standard)
- [Washington Digital Accessibility Requirements](https://equidox.co/resources/accessibility-education-tools/accessibility-regulations/usa-washington/)

### WCAG Standards & Document Accessibility
- [W3C WCAG 2 Documents](https://www.w3.org/WAI/standards-guidelines/wcag/docs/)
- [WebAIM WCAG 2 Checklist](https://webaim.org/standards/wcag/checklist)
- [How to Make Word Documents Accessible (ADA & WCAG Guide)](https://accessabilityofficer.com/blog/how-to-make-your-word-documents-accessible)
- [10 Best Practices for Accessible PDFs — University of Iowa](https://accessibility.uiowa.edu/news/2025/11/10-best-practices-accessible-pdfs)
- [Creating Accessible PDFs — Harvard](https://accessibility.huit.harvard.edu/pdf)
- [WCAG 2.2 AA Compliance for PDFs and Word Documents](https://parish-council.website/wcag-2-2-aa-compliance-how-to-make-pdfs-and-word-documents-accessible/)
- [Canada Microsoft Document Compliance Checklist](https://a11y.canada.ca/en/microsoft-document-compliance-checklist/)

### AEM & Education
- [NCADEMI: AEM in the AT Guidance](https://ncademi.org/aem-guide)
- [AEM: A Parent's Guide — NCADEMI](https://ncademi.org/audiences/parent-centers/parents-aem/)
- [Accessible Educational Materials — Iowa](https://educate.iowa.gov/pk-12/special-education/programs-services/aem)

### Google Docs
- [Google Docs Accessibility Review](https://theaccessibilityguy.com/google-docs-accessibility-a-comprehensive-review/)
- [Google Docs and Accessibility — CU Boulder](https://www.colorado.edu/digital-accessibility/google-docs-and-accessibility)

### Contrast Checking
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)

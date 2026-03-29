# Digital Accessibility Laws & Requirements for Communicate by Design

**Date compiled:** March 20, 2026  
**Source conversation:** Research session on digital accessibility legal landscape, what laws apply to CbD as a small educational content business, and what practical changes are required across products, platforms, and workflow.

---

## Key Findings & Evidence

### 1. ADA Title III Applies to CbD's Website and Digital Storefront

**Claim:** ADA Title III (Americans with Disabilities Act) covers "places of public accommodation," and federal courts have increasingly interpreted this to include commercial websites and digital storefronts — not just physical spaces.

**Source:** Americans with Disabilities Act Title III, 42 U.S.C. § 12181 et seq. Discussed in conversation; no formal case citation provided — follow-up sourcing recommended (see Gaps section).

**Why it matters:** CbD's website, TPT store, and social media presence are likely covered. Failure to meet baseline accessibility standards creates legal exposure and, more critically, actively excludes the exact population CbD exists to serve.

---

### 2. Section 508 Does Not Directly Apply — But Indirectly Shapes the Market

**Claim:** Section 508 of the Rehabilitation Act applies to federal agencies and their direct contractors. CbD is not a federal contractor. However, public school districts receiving federal funding occupy a gray zone where procurement requirements may include Section 508-aligned specifications.

**Source:** Rehabilitation Act of 1973, Section 508, as amended by the Workforce Innovation and Opportunity Act (2018). Discussed in conversation; no formal procurement case cited.

**Why it matters:** Districts buying CbD resources may be required to confirm those resources meet Section 508 / WCAG standards before approving purchases. Accessibility compliance is a procurement advantage, not just a legal obligation.

---

### 3. DOJ Web Accessibility Rule (2024) Governs CbD's Buyers, Not CbD Directly

**Claim:** The Department of Justice finalized a rule in 2024 under Title II of the ADA requiring state and local governments — including public school districts — to meet WCAG 2.1 AA standards for their digital content. Smaller entities have until April 2026 to comply.

**Source:** U.S. Department of Justice, Title II ADA Web Accessibility Final Rule, 28 C.F.R. Part 35 (2024). Discussed in conversation; full regulatory citation should be verified.

**Why it matters for CbD specifically:** The April 2026 deadline means districts are actively auditing their procurement pipelines right now. Resources that are not demonstrably accessible may be rejected or removed from use. CbD's accessibility posture is a direct selling point for district-level buyers under procurement pressure.

---

### 4. WCAG 2.1 AA Is the Universal Safe Harbor Target

**Claim:** WCAG (Web Content Accessibility Guidelines) 2.1 Level AA is not a law but is the technical standard referenced by ADA Title III enforcement, Section 508, the DOJ's 2024 Title II rule, and most state-level accessibility regulations. Achieving WCAG 2.1 AA is the accepted baseline for legal compliance across all frameworks.

**Source:** World Wide Web Consortium (W3C), Web Content Accessibility Guidelines 2.1, June 2018. wcag.org. Discussed in conversation; authoritative source is W3C directly.

**Why it matters:** Rather than tracking multiple regulatory frameworks, CbD can use WCAG 2.1 AA as a single design target that satisfies all relevant law. WCAG 2.2 is the current version (October 2023) and is backward compatible — building to 2.2 AA exceeds all current requirements.

---

### 5. Canva PDF Export Has a Known, Documented Accessibility Gap

**Claim:** Canva's PDF export does not reliably produce fully tagged PDFs. Untagged PDFs are essentially inaccessible to screen readers and other assistive technology — the content may be visually present but structurally invisible to AT.

**Source:** Discussed in conversation based on known Canva platform behavior; no Canva support documentation citation provided — see Gaps section.

**Why it matters:** Every CbD resource that ships as a PDF from Canva carries this risk by default. This is not a minor issue — it is a structural barrier for students and educators who use screen readers, text-to-speech, or other AT to access documents. Workflow remediation or documented limitation disclosure is required.

---

### 6. Color Contrast Requirements Are Specific and Testable

**Claim:** WCAG 2.1 AA requires a minimum contrast ratio of 4.5:1 for normal-sized text against its background, and 3:1 for large text (18pt+ or 14pt+ bold). Color alone cannot be the only means of conveying information (e.g., color-coded tables without labels).

**Source:** WCAG 2.1, Success Criteria 1.4.3 (Contrast Minimum) and 1.4.1 (Use of Color). Discussed in conversation.

**Why it matters for CbD brand:** Navy #1B1F3B as a background color was previously confirmed as CbD's "accessibility superpower" — all brand accent colors (Teal #00B4D8, Amber #FFB703, Yellow #FFD700) pass WCAG 2.1 AA contrast on navy. All accent colors FAIL on white or light backgrounds. This is a non-negotiable layout constraint, not a preference.

---

### 7. Alt Text and Document Tagging Are the Two Highest-Impact Fixes

**Claim:** The two most common and most consequential PDF accessibility failures are (1) missing or poor alt text on images and graphics, and (2) absent or incorrect document structure tags (headings, lists, reading order). Both are required under WCAG and Section 508.

**Source:** Discussed in conversation; aligns with WebAIM annual accessibility report patterns (WebAIM Million, annual). Formal citation recommended.

**Why it matters:** These are the two areas where CbD resources are most likely to currently fail. Both can be audited for free using Adobe Acrobat's built-in accessibility checker before any paid remediation workflow is needed.

---

### 8. Instagram and Social Media Accessibility Is Creator-Controlled

**Claim:** While Instagram's platform has inherent accessibility limitations that creators cannot fix, creators do control: (1) alt text on every image post (via Advanced Settings), (2) captions on all video/Reel content, (3) whether key information is buried in image text only vs. also written in the caption, and (4) hashtag formatting (CamelCase improves screen reader pronunciation).

**Source:** Discussed in conversation; Instagram native alt text feature confirmed available. No formal citation needed — this is platform functionality.

**Why it matters:** CbD's Instagram audience includes AT specialists, SLPs, and special educators — many of whom work daily with students using assistive technology and are acutely aware of accessibility failures. Inaccessible social posts directly undermine CbD's brand credibility.

---

### 9. EU Accessibility Act (June 2025) Is a Watch Item

**Claim:** The European Accessibility Act requires products and services sold in the EU to meet accessibility standards, with enforcement beginning June 2025. This does not currently apply to CbD but becomes relevant if CbD expands distribution internationally.

**Source:** European Accessibility Act, Directive (EU) 2019/882, transposed by EU member states by June 2025. Discussed in conversation.

**Why it matters:** Low-priority now; flag for future planning if TPT or direct sales expand to European markets.

---

## Direct Quotes & Formally Cited Sources

No direct quotations from external publications were included in this conversation. The following sources were named and should be verified at their authoritative locations:

| Source | Location | Relevance |
|---|---|---|
| ADA Title III | 42 U.S.C. § 12181 | Applies to CbD website/storefront |
| Rehabilitation Act §508 | 29 U.S.C. § 794d | Applies indirectly via district procurement |
| DOJ Title II Final Rule (2024) | 28 C.F.R. Part 35 | Governs school district buyers; April 2026 deadline |
| WCAG 2.1 AA | w3.org/TR/WCAG21/ | Universal technical compliance target |
| WCAG 2.2 | w3.org/TR/WCAG22/ | Current version; backward compatible with 2.1 |
| EU Accessibility Act | EUR-Lex Directive 2019/882 | International expansion watch item |
| WebAIM Million Report (annual) | webaim.org/projects/million/ | Annual data on most common accessibility failures |

---

## Practical Implications

### AT/AAC Service Delivery
Accessible resource design is not a bonus feature — it is a prerequisite for use with AT. A PDF that cannot be read by a screen reader, or a document with no logical heading structure, cannot be navigated by a student using a switch interface or eye gaze device. Every CbD resource should function with the same AT tools CbD's content teaches people to use.

### IEP Team Capacity-Building
IEP teams are most likely to adopt resources that remove barriers rather than create them. An SLP or special educator who opens a CbD PDF and finds it is not accessible to the student they are trying to support will not return to that product. Accessible design is also modeling: CbD teaches accessibility practice, so every CbD product is a demonstration of what that practice looks like.

### Instructional Design
The highest-leverage instructional accessibility changes are structural, not cosmetic: logical reading order, proper heading hierarchy, text-based (not image-based) content delivery, and plain language baselines. These decisions happen at the design stage, not the export stage. Retrofitting accessibility is significantly harder than building it in from the start.

### District and Family Procurement
The DOJ's April 2026 Title II compliance deadline creates immediate market urgency. Districts evaluating supplemental resources are increasingly required to verify or document accessibility compliance before approving purchases. CbD resources that include an accessibility statement in the product listing and pass a basic PDF accessibility check will clear procurement filters that competitors without accessible resources will fail.

---

## Terms & Definitions

**WCAG (Web Content Accessibility Guidelines):** The international technical standard for digital accessibility, published by the W3C. Organized into four principles (Perceivable, Operable, Understandable, Robust) and three conformance levels (A, AA, AAA). WCAG 2.1 AA is the current legal safe harbor standard in the US.

**Tagged PDF:** A PDF with embedded structural markup (tags) that identifies headings, paragraphs, lists, tables, figures, and reading order in a way screen readers and AT can interpret. Untagged PDFs are visually readable but structurally invisible to AT.

**Alt text (alternative text):** A written description of an image or graphic, embedded in the file or HTML, that screen readers and text-to-speech tools read aloud. Required for all non-decorative visual elements under WCAG.

**Contrast ratio:** A mathematical comparison of the relative luminance of foreground text against its background color. WCAG 2.1 AA requires 4.5:1 for normal text, 3:1 for large text. Tested with tools like WebAIM Contrast Checker or Coolors.

**ADA Title III:** The section of the Americans with Disabilities Act that governs "places of public accommodation." Courts have extended this to commercial websites; legal interpretation is still evolving but the risk of non-compliance is well-established.

**Section 508:** Federal law requiring that electronic and information technology developed, procured, maintained, or used by federal agencies be accessible. Referenced in school district procurement requirements that flow from federal funding.

**DOJ Title II Rule (2024):** A federal regulation finalized in 2024 that explicitly requires state and local government entities (including public schools) to meet WCAG 2.1 AA for web content and digital services. Smaller entities must comply by April 2026.

**CamelCase hashtags:** Writing hashtags with each word capitalized (#CommunicateByDesign vs. #communicatebydesign). Screen readers parse CamelCase hashtags as individual words; lowercase runs them together as a single unreadable string.

**Plain language:** Writing designed to be understood by the intended audience on first reading. Federal plain language guidelines recommend targeting an 8th grade reading level for general public-facing content. Hemingway App is a free tool for measuring this.

**Safe harbor:** A legal term meaning that meeting a specific standard (WCAG 2.1 AA) provides protection against claims of non-compliance under the broader law (ADA, Section 508). Not absolute immunity, but a recognized standard of reasonable care.

---

## Gaps & Follow-Up Needed

**1. Canva PDF accessibility documentation**  
Need to confirm current Canva PDF export behavior against WCAG tagging requirements — specifically whether Canva's "accessible PDF" export option (if available) produces genuinely tagged output or visual-only PDFs. Check Canva's support documentation and test with Adobe Acrobat Accessibility Checker on a current export.  
*Priority: High — affects every product CbD ships.*

**2. Formal case law on ADA Title III and websites**  
Several federal circuit courts have ruled differently on whether ADA Title III applies to websites independent of a physical location. The current dominant view supports coverage, but the specific circuit governing Oregon (Ninth Circuit) should be confirmed.  
*Priority: Medium — relevant if CbD ever faces a formal complaint.*

**3. TPT platform's own accessibility compliance posture**  
TPT as a platform has its own obligations under ADA Title III and the DOJ rule. CbD's products are delivered through TPT's infrastructure. Understanding where TPT's responsibility ends and the seller's begins affects how CbD frames its own accessibility statement.  
*Priority: Medium — affects product listing language.*

**4. WebAIM Million Report — current year data**  
The WebAIM Million Report is published annually and tracks the most common accessibility failures across the top 1 million websites. Citing current-year data would strengthen any accessibility-related marketing or thought leadership content CbD publishes.  
*Priority: Low — useful for Substack content.*

**5. Adobe Acrobat Pro vs. free checker — remediation workflow**  
Confirmed the free Acrobat accessibility checker exists; did not confirm whether free Acrobat Reader (vs. paid Acrobat Pro) can remediate failures. If remediation requires the paid subscription, that is a cost and workflow consideration.  
*Priority: High — practical workflow decision.*

**6. Oregon state-level digital accessibility requirements**  
Oregon may have state-level digital accessibility requirements that go beyond federal law. This was not researched in this conversation.  
*Priority: Low — CbD operates nationally via TPT, not Oregon-specific.*

---

*Compiled from conversation: Digital accessibility research session, Communicate by Design, March 20, 2026. No formal publications were directly cited in the source conversation; all source attributions above represent the authoritative documents the conversation content was drawn from and should be independently verified before use in formal communications.*

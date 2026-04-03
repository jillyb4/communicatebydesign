"""
build_all_previews.py — Communicate by Design
Builds watermarked 10-page preview PDFs for all 6 nonfiction units.

PREREQUISITE — before running this script:
  1. Open each COMPLETE.docx in Word
  2. File → Save As → PDF (NOT Print to PDF, NOT LibreOffice)
  3. Save the PDF into the unit folder with the filename listed in UNITS below
  4. For 504 Sit-In: first run `node Products/Nonfiction Units/504\ Sit\ In/build_504_sit_in.js`
     to generate the COMPLETE.docx, then export it to PDF

USAGE:
  # Build all 6 units:
  python3 _Operations/build_all_previews.py

  # Build a single unit:
  python3 _Operations/build_all_previews.py --unit keiko

  # Inspect page text to verify page indices (run this before building if PDFs are new):
  python3 _Operations/build_all_previews.py --inspect --unit keiko

DEPENDENCIES:
  pip install pypdf reportlab --break-system-packages

OUTPUT:
  Products/Nonfiction Units/Preview PDFs/[Unit]_TPT_Preview.pdf
"""

import io
import os
import sys
import argparse
from pathlib import Path
from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white, Color
from reportlab.lib.units import inch

# ── Brand Colors ──────────────────────────────────────────────────────────────
NAVY   = HexColor("#1B1F3B")
TEAL   = HexColor("#006DA0")
TEAL_D = HexColor("#00B4D8")
AMBER  = HexColor("#FFB703")
WHITE  = white
GRAY   = HexColor("#CCCCCC")

W, H = letter  # 612 x 792 pts

BASE = Path(__file__).parent.parent  # Communicate by Design root
UNITS_ROOT = BASE / "Products" / "Nonfiction Units"
# Preview PDFs are saved alongside the source PDF in each unit's _TPT/ folder.
# OUTPUT_DIR is kept as a fallback reference only — individual output paths
# are resolved per unit from the source_pdf location.
OUTPUT_DIR = UNITS_ROOT / "Preview PDFs"

# ── Unit Configurations ────────────────────────────────────────────────────────
#
# SOURCE_PAGES: 8 page indices (0-based) pulled from the unit PDF
#   [TOC, overview, v1_passage, v2_passage, v3_passage, v1_activity, v2_activity, v3_activity]
#
# Page indices sourced from nonfiction_build_reference.md.
# V2 passage and V2 activity marked with * are estimates — run --inspect to verify.
#
UNITS = {
    "keiko": {
        "folder":       "Keiko",
        "tpt_folder":   "Keiko_TPT",
        "source_pdf":   "Keiko_TPT/Keiko_COMPLETE.pdf",
        "symbol_pdf":   "Keiko_TPT/Keiko_Communication_Access_Packet.pdf",
        "symbol_page_idx": 2,   # "Priority Vocabulary for Communication Access" page
        "output":       "Keiko_TPT_Preview.pdf",
        # overview · comm-access (AAC unit design) · V1 passage · V1 Short Answer · V2 passage · V2 Short Answer · V3 passage · V3 Short Answer
        # NOTE: MCQ pages omitted — questions are in table format that does not render after watermark merge
        "source_pages": [3, 8, 24, 28, 45, 47, 58, 60],
        "config": {
            "title_line1":   "Keiko: A Whale's Journey",
            "title_line2":   "Argument Writing · Grades 6–10",
            "subtitle":      "A Nonfiction Reading Unit  |  Argument Writing  |  Grades 6–10",
            "skill_badge":   "Skill #1 — Argument Writing (CCSS W.1)",
            "full_pages":    75,
            "price":         "$9.95",
            "preview_items": [
                "✦  Lesson overview and standards alignment",
                "✦  3 Lexile versions — V1 (900–1050)  ·  V2 (650–800)  ·  V3 (400–550)",
                "✦  4-part reading sequence + debate section",
                "✦  Sample passage and argument writing activity",
                "✦  Communication Access section with AAC word table",
                "✦  Annotation codes: H (Health) · P (Happiness) · D (Dependence)",
            ],
            "full_items": [
                "4-part passage sequence  ·  3 Lexile versions  ·  12 passage versions total",
                "Argument writing activities  ·  Answer keys for all versions",
                "Word Bank  ·  Sentence Frames  ·  Modeling Session + Think-Aloud Script",
                "Vocabulary Preview Routine  ·  Teacher Background  ·  Pacing Guide",
                "Communication Access  ·  AAC word table  ·  WCAG 2.2 AA",
                "Supplemental Resources  ·  Accessibility Statement  ·  About the Creator",
            ],
            "seasonal_note1": "Ideal for Environmental Science Units  ·  Animal Rights Topics",
            "seasonal_note2": "Argument Writing  ·  SPED Grades 6–10  ·  AAC-Accessible",
            "bundle_line1":   "Bundle with Radium Girls for a two-unit argument writing sequence",
            "bundle_line2":   "Keiko + Radium Girls Bundle  ·  6–8 days of instruction",
        },
    },

    "radium_girls": {
        "folder":       "Radium Girls",
        "tpt_folder":   "Radium_Girls_TPT",
        "source_pdf":   "Radium_Girls_TPT/Radium_Girls_COMPLETE.pdf",
        "symbol_pdf":   "Radium_Girls_TPT/Radium_Girls_Communication_Access_Packet.pdf",
        "symbol_page_idx": 2,   # "Priority Vocabulary for Communication Access" page
        "output":       "Radium_Girls_TPT_Preview.pdf",
        # overview · MLL/AAC teacher support · V1 passage · V1 Short Answer · V2 passage · V2 Short Answer · V3 passage · V3 Short Answer
        # NOTE: MCQ pages omitted — questions are in table format that does not render after watermark merge
        "source_pages": [3, 8, 23, 25, 44, 46, 63, 65],
        "config": {
            "title_line1":   "Radium Girls:",
            "title_line2":   "Informative Writing · Grades 6–10",
            "subtitle":      "A Nonfiction Reading Unit  |  Informative Writing  |  Grades 6–10",
            "skill_badge":   "Skill #1 — Informative/Explanatory Writing (CCSS W.2)",
            "full_pages":    70,
            "price":         "$11.95",
            "preview_items": [
                "✦  Lesson overview and standards alignment",
                "✦  3 Lexile versions — V1 (900–1050)  ·  V2 (650–800)  ·  V3 (400–550)",
                "✦  5-part reading sequence (The Dial Painters → The Legacy)",
                "✦  Sample passage and informative writing activity",
                "✦  Communication Access section with AAC word table",
                "✦  Annotation codes: F (Failure) · R (Response) · C (Change)",
            ],
            "full_items": [
                "5-part passage sequence  ·  3 Lexile versions  ·  15 passage versions total",
                "Informative writing activities  ·  Answer keys for all versions",
                "Word Bank  ·  Sentence Frames  ·  Modeling Session + Think-Aloud Script",
                "Vocabulary Preview Routine  ·  Teacher Background  ·  Pacing Guide",
                "Communication Access  ·  AAC word table  ·  WCAG 2.2 AA",
                "Supplemental Resources  ·  Accessibility Statement  ·  About the Creator",
            ],
            "seasonal_note1": "Ideal for Women's History Month  ·  Labor History Units",
            "seasonal_note2": "Informative Writing  ·  SPED Grades 6–10  ·  AAC-Accessible",
            "bundle_line1":   "Bundle with Keiko for a two-unit informative/argument writing sequence",
            "bundle_line2":   "Keiko + Radium Girls Bundle  ·  6–8 days of instruction",
        },
    },

    "zitkala_sa": {
        "folder":       "Zitkala-Sa",
        "tpt_folder":   "Zitkala_Sa_TPT",
        "source_pdf":   "Zitkala_Sa_TPT/Zitkala_Sa_COMPLETE.pdf",
        "symbol_pdf":   "Zitkala_Sa_TPT/Zitkala_Sa_Communication_Access_Packet.pdf",
        "symbol_page_idx": 1,   # "Priority Vocabulary for Communication Access" page
        "output":       "Zitkala_Sa_TPT_Preview.pdf",
        # overview · modeling session (teacher guide) · V1 passage · V1 Evidence Sort · V2 passage · V2 Short Answer · V3 passage · V3 Short Answer
        # NOTE: MCQ pages omitted — questions are in table format that does not render after watermark merge
        "source_pages": [3, 9, 16, 21, 29, 35, 40, 44],
        "config": {
            "title_line1":   "Zitkala-Ša:",
            "title_line2":   "Text Structure Analysis · Grades 6–10",
            "subtitle":      "A Nonfiction Reading Lesson  |  Text Structure  |  Grades 6–10",
            "skill_badge":   "Skill #3 — Text Structure Analysis (RI.x.5)",
            "full_pages":    55,
            "price":         "$9.95",
            "preview_items": [
                "✦  Lesson overview and standards alignment",
                "✦  3 Lexile versions — V1 (900–1050)  ·  V2 (650–800)  ·  V3 (400–550)",
                "✦  2-part lesson: cause-and-effect → problem-solution",
                "✦  Sample passage and text structure activity",
                "✦  Communication Access section with AAC word table",
                "✦  Symbol Cards + Communication Access Packet included",
            ],
            "full_items": [
                "2-part lesson  ·  3 Lexile versions  ·  6 passage versions total",
                "Text structure activities  ·  Answer keys for all versions",
                "Word Bank  ·  Sentence Frames  ·  Modeling Session + Think-Aloud Script",
                "Vocabulary Preview Routine  ·  Teacher Background  ·  Pacing Guide",
                "Communication Access  ·  Symbol Cards  ·  AAC word table  ·  WCAG 2.2 AA",
                "Supplemental Resources  ·  Accessibility Statement  ·  About the Creator",
            ],
            "seasonal_note1": "Ideal for Native American Heritage Month  ·  Nov / Indigenous Peoples Day",
            "seasonal_note2": "Text Structure  ·  SPED Grades 6–10  ·  AAC-Accessible",
            "bundle_line1":   "Pairs with other disability history and identity units",
            "bundle_line2":   "Multiple units available  ·  3–5 days of instruction per unit",
        },
    },

    "504_sit_in": {
        "folder":       "504 Sit In",
        "tpt_folder":   None,   # no _TPT subfolder — saves to unit folder root
        "source_pdf":   "504_Sit_In_Unit_COMPLETE.pdf",
        "symbol_pdf":   None,
        "output":       "504_Sit_In_TPT_Preview.pdf",
        # overview · instructional design section · V1 passage · V3 passage · Quote Selection V1 · Quote Selection V3 · Perspective Comparison · Short Answer V3
        # NOTE: MCQ pages omitted — questions are in table format that does not render after watermark merge
        "source_pages": [5, 18, 39, 45, 53, 55, 65, 70],
        "config": {
            "title_line1":   "504 Sit-In:",
            "title_line2":   "Author's Purpose & Perspective · Grades 6–10",
            "subtitle":      "A Nonfiction Reading Unit  |  Author's Purpose  |  Grades 6–10",
            "skill_badge":   "Skill #4 — Author's Purpose / Perspective (RI.x.6)",
            "full_pages":    65,
            "price":         "$11.95",
            "preview_items": [
                "✦  Lesson overview and standards alignment",
                "✦  3 Lexile versions — V1 (900–1050)  ·  V2 (650–800)  ·  V3 (400–550)",
                "✦  4-part sequence: The Promise → The Occupation → The Pressure → The Victory",
                "✦  Sample passage and perspective-tracking activity",
                "✦  Communication Access section with AAC word table",
                "✦  Perspective Tracking Chart student handout",
            ],
            "full_items": [
                "4-part passage sequence  ·  3 Lexile versions  ·  12 passage versions total",
                "Author's purpose activities  ·  Answer keys for all versions",
                "Word Bank  ·  Sentence Frames  ·  Modeling Session + Think-Aloud Script",
                "Vocabulary Preview Routine  ·  Teacher Background  ·  Pacing Guide",
                "Communication Access  ·  AAC word table  ·  WCAG 2.2 AA",
                "Supplemental Resources  ·  Accessibility Statement  ·  About the Creator",
            ],
            "seasonal_note1": "Ideal for Disability History Month (Oct)  ·  Disability Pride Month (July)",
            "seasonal_note2": "Author's Purpose  ·  SPED Grades 6–10  ·  AAC-Accessible",
            "bundle_line1":   "Bundle with Capitol Crawl 1990 for Disability Pride Month",
            "bundle_line2":   "504 Sit-In + Capitol Crawl Bundle  ·  6–8 days of instruction",
        },
    },

    "frances_kelsey": {
        "folder":       "Frances Kelsey",
        "tpt_folder":   "Frances_Kelsey_TPT",
        "source_pdf":   "Frances_Kelsey_TPT/Frances_Kelsey_COMPLETE.pdf",
        "symbol_pdf":   "Frances_Kelsey_TPT/Frances_Kelsey_Symbol_Cards.pdf",
        "symbol_page_idx": 0,   # Symbol Cards PDF — page 0
        "output":       "Frances_Kelsey_TPT_Preview.pdf",
        # overview · MLL/AAC teacher support · V1 passage · V1 Short Answer · V1 Evidence Sort · V3 passage · V3 activity · V3 passage Part 3
        # NOTE: MCQ pages omitted — questions are in table format that does not render after watermark merge
        "source_pages": [3, 8, 27, 38, 44, 65, 66, 70],
        "config": {
            "title_line1":   "Frances Kelsey:",
            "title_line2":   "Claim, Evidence, Reasoning · Grades 6–10",
            "subtitle":      "A Nonfiction Reading Unit  |  Claim · Evidence · Reasoning  |  Grades 6–10",
            "skill_badge":   "Skill #5 — Claim, Evidence, Reasoning (RI.x.8)",
            "full_pages":    72,
            "price":         "$11.95",
            "preview_items": [
                "✦  Lesson overview and standards alignment",
                "✦  3 Lexile versions — V1 (900–1050)  ·  V2 (650–800)  ·  V3 (400–550)",
                "✦  4-part sequence: The New Drug → The Pressure → The Truth → The Legacy",
                "✦  Sample passage and C·E·R annotation activity",
                "✦  Communication Access section with AAC word table + Symbol Cards",
                "✦  Annotation codes: C (Claim) · E (Evidence) · R (Reasoning)",
            ],
            "full_items": [
                "4-part passage sequence  ·  3 Lexile versions  ·  12 passage versions total",
                "C·E·R activities  ·  Answer keys for all versions",
                "Word Bank  ·  Sentence Frames  ·  Modeling Session + Think-Aloud Script",
                "Vocabulary Preview Routine  ·  Teacher Background  ·  Pacing Guide",
                "Communication Access  ·  Symbol Cards  ·  AAC word table  ·  WCAG 2.2 AA",
                "Supplemental Resources  ·  Accessibility Statement  ·  About the Creator",
            ],
            "seasonal_note1": "Ideal for Women's History Month  ·  Science & Society Units",
            "seasonal_note2": "C·E·R Argument Writing  ·  SPED Grades 6–10  ·  AAC-Accessible",
            "bundle_line1":   "Pairs with other argument writing units for a writing sequence",
            "bundle_line2":   "Multiple units available  ·  3–5 days of instruction per unit",
        },
    },

    "capitol_crawl": {
        "folder":       "Capitol Crawl",
        "tpt_folder":   "Capitol_Crawl_TPT",
        "source_pdf":   "Capitol_Crawl_TPT/Capitol_Crawl_COMPLETE.pdf",
        "symbol_pdf":   "Capitol_Crawl_TPT/Capitol_Crawl_Communication_Access_Packet.pdf",
        "symbol_page_idx": 2,   # "Priority Vocabulary for Communication Access" page
        "output":       "Capitol_Crawl_TPT_Preview.pdf",
        # overview · comm-access (AAC pre-loaded responses) · V1 passage Part 1 · V1 passage Part 2 · V3 passage · V3 Evidence Strength Rating · V1 Short Answer · Source Evaluation guide
        # NOTE: MCQ pages omitted — questions are in table format that does not render after watermark merge
        "source_pages": [3, 12, 16, 18, 27, 33, 40, 44],
        "config": {
            "title_line1":   "Capitol Crawl 1990:",
            "title_line2":   "Sourcing & Corroboration · Grades 6–10",
            "subtitle":      "A Nonfiction Reading Lesson  |  Sourcing & Corroboration  |  Grades 6–10",
            "skill_badge":   "Skill #6 — Sourcing / Corroboration (RI.x.9)",
            "full_pages":    55,
            "price":         "$9.95",
            "preview_items": [
                "✦  Lesson overview and standards alignment",
                "✦  3 Lexile versions — V1 (900–1050)  ·  V2 (650–800)  ·  V3 (400–550)",
                "✦  Source Tracking Chart student handout (4-column graphic organizer)",
                "✦  Sample passage and corroboration activity",
                "✦  Communication Access section with AAC word table",
                "✦  Evaluate multiple sources — do they all tell the same story?",
            ],
            "full_items": [
                "2-part passage sequence  ·  3 Lexile versions  ·  6 passage versions total",
                "Sourcing & corroboration activities  ·  Answer keys for all versions",
                "Word Bank  ·  Sentence Frames  ·  Modeling Session + Think-Aloud Script",
                "Vocabulary Preview Routine  ·  Teacher Background  ·  Pacing Guide",
                "Communication Access  ·  AAC word table  ·  WCAG 2.2 AA",
                "Supplemental Resources  ·  Accessibility Statement  ·  About the Creator",
            ],
            "seasonal_note1": "Ideal for Disability Pride Month  ·  ADA Anniversary July 26",
            "seasonal_note2": "Civil Rights Curriculum  ·  Media Literacy  ·  SPED Grades 6–10",
            "bundle_line1":   "Bundle with 504 Sit-In for Disability Pride Month",
            "bundle_line2":   "504 Sit-In + Capitol Crawl Bundle  ·  6–8 days of instruction",
        },
    },
}


# ── Page builder functions (from build_preview_pdf_template.py) ────────────────

def make_cover(cfg):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)

    c.setFillColor(NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    c.setFillColor(TEAL)
    c.rect(0, H - 72, W, 72, fill=1, stroke=0)

    c.setFillColor(TEAL_D)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(W / 2, H - 44, "COMMUNICATE BY DESIGN")
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Oblique", 11)
    c.drawCentredString(W / 2, H - 60, "Where AT Meets Practice")

    badge_w, badge_h = 180, 42
    badge_x = (W - badge_w) / 2
    badge_y = H - 155
    c.setFillColor(AMBER)
    c.roundRect(badge_x, badge_y, badge_w, badge_h, 6, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(W / 2, badge_y + 12, "PREVIEW")

    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(W / 2, H - 240, cfg["title_line1"])
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(W / 2, H - 272, cfg["title_line2"])

    c.setStrokeColor(TEAL_D)
    c.setLineWidth(2)
    c.line(72, H - 295, W - 72, H - 295)

    c.setFillColor(GRAY)
    c.setFont("Helvetica", 14)
    c.drawCentredString(W / 2, H - 322, cfg["subtitle"])

    c.setFillColor(HexColor("#252A4A"))
    c.roundRect(60, H - 540, W - 120, 195, 8, fill=1, stroke=0)

    c.setFillColor(AMBER)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(84, H - 370, "What's Inside This Preview:")

    c.setFillColor(WHITE)
    c.setFont("Helvetica", 11)
    y = H - 392
    for item in cfg["preview_items"]:
        c.drawString(84, y, item)
        y -= 22

    c.setFillColor(AMBER)
    c.rect(0, 0, W, 58, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(W / 2, 36, "communicatebydesign.substack.com  ·  TPT: Communicate by Design")

    c.setFillColor(TEAL)
    c.roundRect(60, H - 600, 220, 30, 5, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(72, H - 590, cfg["skill_badge"])

    c.setFillColor(GRAY)
    c.setFont("Helvetica-Oblique", 10)
    c.drawCentredString(W / 2, H - 640,
        f"Full unit: {cfg['full_pages']} pages  ·  This preview: 10 pages")

    c.save()
    buf.seek(0)
    return buf


def make_watermark():
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    c.saveState()
    c.setFillColor(Color(0.106, 0.122, 0.231, alpha=0.12))
    c.setFont("Helvetica-Bold", 72)
    c.translate(W / 2, H / 2)
    c.rotate(40)
    c.drawCentredString(0, 0, "PREVIEW")
    c.restoreState()

    c.setFillColor(AMBER)
    c.roundRect(W - 115, H - 34, 105, 24, 4, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(W - 62, H - 25, "COMMUNICATE BY DESIGN")

    c.save()
    buf.seek(0)
    return buf


def make_back(cfg):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)

    c.setFillColor(NAVY)
    c.rect(0, H / 2, W, H / 2, fill=1, stroke=0)

    c.setFillColor(TEAL)
    c.rect(0, H - 72, W, 72, fill=1, stroke=0)
    c.setFillColor(TEAL_D)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(W / 2, H - 44, "COMMUNICATE BY DESIGN")
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Oblique", 11)
    c.drawCentredString(W / 2, H - 60, "Where AT Meets Practice")

    c.setFillColor(AMBER)
    c.setFont("Helvetica-Bold", 32)
    c.drawCentredString(W / 2, H - 130, "Get the Full Unit")

    c.setFillColor(AMBER)
    c.circle(W / 2, H - 195, 42, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(W / 2, H - 202, cfg["price"])

    c.setStrokeColor(TEAL_D)
    c.setLineWidth(1.5)
    c.line(72, H - 240, W - 72, H - 240)

    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(W / 2, H - 264, "The full unit includes:")

    c.setFont("Helvetica", 10.5)
    y = H - 288
    for item in cfg["full_items"]:
        c.drawCentredString(W / 2, y, item)
        y -= 18

    c.setFillColor(WHITE)
    c.rect(0, 0, W, H / 2, fill=1, stroke=0)

    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(W / 2, H / 2 - 40, "Find it on Teachers Pay Teachers:")
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(W / 2, H / 2 - 64, "teacherspayteachers.com/store/communicate-by-design")

    c.setFillColor(HexColor("#555555"))
    c.setFont("Helvetica-Oblique", 11)
    c.drawCentredString(W / 2, H / 2 - 100, cfg["seasonal_note1"])
    c.drawCentredString(W / 2, H / 2 - 118, cfg["seasonal_note2"])

    c.setFillColor(HexColor("#F0F4F8"))
    c.roundRect(72, H / 2 - 215, W - 144, 72, 6, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(W / 2, H / 2 - 162, cfg["bundle_line1"])
    c.setFillColor(HexColor("#444444"))
    c.setFont("Helvetica", 10)
    c.drawCentredString(W / 2, H / 2 - 180, cfg["bundle_line2"])

    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(W / 2, H / 2 - 248, "About Communicate by Design")
    c.setFillColor(HexColor("#444444"))
    c.setFont("Helvetica", 10)
    c.drawCentredString(W / 2, H / 2 - 266,
        "Created by a special educator and advocate. Every resource is built on the belief that")
    c.drawCentredString(W / 2, H / 2 - 282,
        "AT must be explicitly taught — not merely provided — to give complex communicators a genuine chance.")

    c.setFillColor(AMBER)
    c.rect(0, 0, W, 48, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(W / 2, 28, "communicatebydesign.substack.com")
    c.setFont("Helvetica", 9)
    c.drawCentredString(W / 2, 14, "@communicatebydesignaac  ·  Where AT Meets Practice")

    c.save()
    buf.seek(0)
    return buf


# ── Inspector: prints page text to verify indices ────────────────────────────

def inspect_unit(unit_key):
    unit = UNITS[unit_key]
    pdf_path = UNITS_ROOT / unit["folder"] / unit["source_pdf"]
    if not pdf_path.exists():
        print(f"❌  Source PDF not found: {pdf_path}")
        print(f"    → Export {unit['source_pdf'].replace('.pdf','.docx')} from Word first.")
        return
    print(f"\n📄  Inspecting: {pdf_path.name}  ({unit_key})")
    print(f"{'─'*70}")
    reader = PdfReader(str(pdf_path))
    print(f"    Total pages: {len(reader.pages)}\n")
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        snippet = text.replace("\n", " ").strip()[:100]
        print(f"  idx {i:3d}  (p{i+1:3d}):  {snippet}")
    print()


# ── Builder ────────────────────────────────────────────────────────────────────

def build_preview(unit_key):
    unit = UNITS[unit_key]
    pdf_path    = UNITS_ROOT / unit["folder"] / unit["source_pdf"]
    output_path     = OUTPUT_DIR / unit["output"]
    # Also save into the unit's _TPT folder so the preview lives with all other TPT files
    tpt_folder = unit.get("tpt_folder")
    tpt_output_path = (
        UNITS_ROOT / unit["folder"] / tpt_folder / unit["output"]
        if tpt_folder
        else UNITS_ROOT / unit["folder"] / unit["output"]
    )

    if not pdf_path.exists():
        print(f"\n⚠️   SKIPPING {unit_key} — source PDF not found:")
        print(f"     {pdf_path}")
        print(f"     → Open {unit['source_pdf'].replace('.pdf', '.docx')} in Word")
        print(f"       and use File → Save As → PDF\n")
        return False

    print(f"\n▶  Building preview: {unit_key}")
    print(f"   Source:  {pdf_path.name}")
    source = PdfReader(str(pdf_path))
    print(f"   Pages in source: {len(source.pages)}")

    # Validate page indices
    max_idx = len(source.pages) - 1
    valid_pages = []
    for idx in unit["source_pages"]:
        if idx <= max_idx:
            valid_pages.append(idx)
        else:
            print(f"   ⚠️  Page index {idx} out of range (max {max_idx}) — skipping")

    if len(valid_pages) < 6:
        print(f"   ❌  Too few valid pages ({len(valid_pages)}). Run --inspect to verify indices.")
        return False

    # Generate branded pages
    cover_page = PdfReader(make_cover(unit["config"])).pages[0]
    wm_page    = PdfReader(make_watermark()).pages[0]
    back_page  = PdfReader(make_back(unit["config"])).pages[0]

    # Assemble
    writer = PdfWriter()
    writer.add_page(cover_page)

    for page_idx in valid_pages:
        page = source.pages[page_idx]
        page.merge_page(wm_page)
        writer.add_page(page)

    # Add symbol / Communication Access vocabulary page if available
    if unit.get("symbol_pdf"):
        sym_path = UNITS_ROOT / unit["folder"] / unit["symbol_pdf"]
        if sym_path.exists():
            sym_reader   = PdfReader(str(sym_path))
            sym_page_idx = unit.get("symbol_page_idx", 0)
            if sym_page_idx < len(sym_reader.pages):
                sym_page = sym_reader.pages[sym_page_idx]
                sym_page.merge_page(wm_page)
                writer.add_page(sym_page)
                print(f"   ✅  Communication Access / symbol page added (p{sym_page_idx + 1} of {sym_path.name})")
            else:
                print(f"   ⚠️   symbol_page_idx {sym_page_idx} out of range for {sym_path.name}")
        else:
            print(f"   ℹ️   Symbol PDF not found (optional): {sym_path.name}")

    writer.add_page(back_page)

    # Write to central Preview PDFs folder
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(str(output_path), "wb") as f:
        writer.write(f)
    print(f"   ✅  Saved ({len(writer.pages)} pages): {output_path.name}")

    # Also write into the unit's TPT folder so the preview lives with all other upload files
    tpt_output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(str(tpt_output_path), "wb") as f:
        writer.write(f)
    print(f"   ✅  Copied to TPT folder: {tpt_output_path.relative_to(UNITS_ROOT)}")

    return True


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Build CbD nonfiction preview PDFs")
    parser.add_argument("--unit", choices=list(UNITS.keys()),
                        help="Build a single unit (default: all)")
    parser.add_argument("--inspect", action="store_true",
                        help="Print page text to verify page indices")
    args = parser.parse_args()

    targets = [args.unit] if args.unit else list(UNITS.keys())

    if args.inspect:
        for key in targets:
            inspect_unit(key)
        return

    print(f"\n{'='*60}")
    print(f"  CbD Nonfiction Preview Builder")
    print(f"  Output: {OUTPUT_DIR}")
    print(f"{'='*60}")

    results = {}
    for key in targets:
        results[key] = build_preview(key)

    print(f"\n{'─'*60}")
    print("  Summary:")
    for key, ok in results.items():
        status = "✅  Built" if ok else "⚠️   Skipped — source PDF missing"
        print(f"  {key:<20} {status}")
    print(f"{'─'*60}\n")

    missing = [k for k, ok in results.items() if not ok]
    if missing:
        print("Next steps for missing units:")
        for key in missing:
            unit = UNITS[key]
            print(f"  • {key}: Open {unit['source_pdf'].replace('.pdf','.docx')} in Word")
            print(f"           → File → Save As → PDF → save to unit folder")
        if "504_sit_in" in missing:
            print(f"\n  ⚠️  504 Sit-In also needs COMPLETE.docx built first:")
            print(f"       cd 'Products/Nonfiction Units/504 Sit In'")
            print(f"       node build_504_sit_in.js")
        print(f"\n  Then re-run:  python3 _Operations/build_all_previews.py\n")


if __name__ == "__main__":
    main()

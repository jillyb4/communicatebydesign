"""
build_preview_pdf_template.py — Communicate by Design
Reusable template for 10-page watermarked nonfiction unit preview PDFs.

Structure: Cover (1) + watermarked content pages (8) + "Get the Full Unit" back (1)

HOW TO USE FOR A NEW UNIT:
1. Copy this file to the unit folder (or run from _Operations with updated paths)
2. Set SOURCE_PDF, OUTPUT_PATH, UNIT_CONFIG, and SOURCE_PAGES
3. Run: python build_preview_pdf_template.py

HOW TO FIND CORRECT PAGE INDICES (run this first):
    from pypdf import PdfReader
    source = PdfReader("path/to/COMPLETE.pdf")
    for i, page in enumerate(source.pages):
        text = page.extract_text()
        if text:
            snippet = text[100:250].strip().replace('\\n', ' ')
            print(f"  idx {i:2d} (p{i+1:2d}): {snippet[:80]}")

PAGE SELECTION STRATEGY (8 content pages):
  1. TOC                        — typically idx 1 (p2)
  2. Lesson Overview/skill page — typically idx 3 (p4)
  3. V1 passage Part 1
  4. V2 passage Part 1
  5. V3 passage Part 1
  6. Activity for V1 (ESR or key comprehension activity)
  7. Activity for V2
  8. Activity for V3

UNIT PAGE SELECTION REFERENCE:
  Capitol Crawl (#6, 55 pages): [1, 3, 16, 21, 26, 30, 32, 33]
  Zitkala-Sa (#3):        TBD — run text extraction
  Frances Kelsey (#5):    TBD — run text extraction
  Radium Girls (#1):      TBD — run text extraction
  Keiko (#1):             TBD — run text extraction
  504 Sit-In (#4):        TBD — run text extraction

DEPENDENCIES:
  pip install pypdf reportlab --break-system-packages
"""

import io
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

# ─────────────────────────────────────────────────────────────────────────────
# UNIT CONFIGURATION — edit this section for each unit
# ─────────────────────────────────────────────────────────────────────────────

SOURCE_PDF  = "/path/to/COMPLETE.pdf"       # Update for each unit
OUTPUT_PATH = "/path/to/Preview PDFs/Unit_Preview.pdf"  # Update for each unit

UNIT_CONFIG = {
    "title_line1":   "Unit Title:",           # e.g. "Capitol Crawl 1990:"
    "title_line2":   "Subtitle",              # e.g. "Sourcing & Corroboration"
    "subtitle":      "A Nonfiction Reading Lesson  |  Topic  |  Grades 6–10",
    "skill_badge":   "Skill #N — Skill Name", # e.g. "Skill #6 — Sourcing & Corroboration"
    "full_pages":    55,                       # Total pages in the complete unit
    "price":         "$9.95",                 # Product price
    "preview_items": [                        # What's inside bullet list
        "✦  Lesson overview and standards alignment",
        "✦  3 Lexile versions — V1 (900–1050)  ·  V2 (650–800)  ·  V3 (400–550)",
        "✦  Source Tracking Chart student handout",
        "✦  Sample reading passage and comprehension activity",
        "✦  Communication Access section with AAC word table",
        "✦  Differentiation and pacing guidance",
    ],
    "full_items": [                           # Full unit contents for back page
        "2-part passage sequence  ·  3 Lexile versions  ·  6 passage versions total",
        "Comprehension activities  ·  Answer Keys for all versions",
        "Word Bank  ·  Sentence Frames  ·  Modeling Session + Think-Aloud Script",
        "Vocabulary Preview Routine  ·  Teacher Background  ·  Pacing Guide",
        "Communication Access  ·  AAC fringe word list  ·  WCAG 2.2 AA",
        "Supplemental Resources  ·  Accessibility Statement  ·  About the Creator",
    ],
    "seasonal_note1": "Ideal for Disability Pride Month  ·  ADA Anniversary July 26",
    "seasonal_note2": "Civil Rights Curriculum  ·  Media Literacy Units",
    "bundle_line1":   "Bundle with related units for a complete teaching sequence",
    "bundle_line2":   "Multiple units  ·  3–5 days of instruction per unit",
}

# Pages to pull from source (0-indexed) — run text extraction script to verify
SOURCE_PAGES = [1, 3, 0, 0, 0, 0, 0, 0]  # Replace zeros with correct indices


# ── 1. Cover Page ─────────────────────────────────────────────────────────────
def make_cover(cfg):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)

    # Navy background
    c.setFillColor(NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # Top teal bar
    c.setFillColor(TEAL)
    c.rect(0, H - 72, W, 72, fill=1, stroke=0)

    # Brand name in teal bar
    c.setFillColor(TEAL_D)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(W / 2, H - 44, "COMMUNICATE BY DESIGN")
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Oblique", 11)
    c.drawCentredString(W / 2, H - 60, "Where AT Meets Practice")

    # PREVIEW badge
    badge_w, badge_h = 180, 42
    badge_x = (W - badge_w) / 2
    badge_y = H - 155
    c.setFillColor(AMBER)
    c.roundRect(badge_x, badge_y, badge_w, badge_h, 6, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(W / 2, badge_y + 12, "PREVIEW")

    # Unit title
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(W / 2, H - 240, cfg["title_line1"])
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(W / 2, H - 272, cfg["title_line2"])

    # Teal divider
    c.setStrokeColor(TEAL_D)
    c.setLineWidth(2)
    c.line(72, H - 295, W - 72, H - 295)

    # Subtitle
    c.setFillColor(GRAY)
    c.setFont("Helvetica", 14)
    c.drawCentredString(W / 2, H - 322, cfg["subtitle"])

    # What's inside block
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

    # Amber footer
    c.setFillColor(AMBER)
    c.rect(0, 0, W, 58, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(W / 2, 36, "communicatebydesign.substack.com  ·  TPT: Communicate by Design")

    # Skill badge
    c.setFillColor(TEAL)
    c.roundRect(60, H - 600, 220, 30, 5, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(72, H - 590, cfg["skill_badge"])

    # Page count note
    c.setFillColor(GRAY)
    c.setFont("Helvetica-Oblique", 10)
    c.drawCentredString(W / 2, H - 640,
        f"Full unit: {cfg['full_pages']} pages  ·  This preview: 10 pages")

    c.save()
    buf.seek(0)
    return buf


# ── 2. Watermark overlay ──────────────────────────────────────────────────────
def make_watermark():
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    c.saveState()
    c.setFillColor(Color(0.106, 0.122, 0.231, alpha=0.12))  # Navy @ 12% opacity
    c.setFont("Helvetica-Bold", 72)
    c.translate(W / 2, H / 2)
    c.rotate(40)
    c.drawCentredString(0, 0, "PREVIEW")
    c.restoreState()

    # Corner stamp
    c.setFillColor(AMBER)
    c.roundRect(W - 115, H - 34, 105, 24, 4, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(W - 62, H - 25, "COMMUNICATE BY DESIGN")

    c.save()
    buf.seek(0)
    return buf


# ── 3. Back page ──────────────────────────────────────────────────────────────
def make_back(cfg):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)

    # Navy background top half
    c.setFillColor(NAVY)
    c.rect(0, H / 2, W, H / 2, fill=1, stroke=0)

    # Top teal bar
    c.setFillColor(TEAL)
    c.rect(0, H - 72, W, 72, fill=1, stroke=0)
    c.setFillColor(TEAL_D)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(W / 2, H - 44, "COMMUNICATE BY DESIGN")
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Oblique", 11)
    c.drawCentredString(W / 2, H - 60, "Where AT Meets Practice")

    # Headline + price
    c.setFillColor(AMBER)
    c.setFont("Helvetica-Bold", 32)
    c.drawCentredString(W / 2, H - 130, "Get the Full Unit")

    c.setFillColor(AMBER)
    c.circle(W / 2, H - 195, 42, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(W / 2, H - 202, cfg["price"])

    # Divider
    c.setStrokeColor(TEAL_D)
    c.setLineWidth(1.5)
    c.line(72, H - 240, W - 72, H - 240)

    # Full unit contents
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(W / 2, H - 264, "The full unit includes:")

    c.setFont("Helvetica", 10.5)
    y = H - 288
    for item in cfg["full_items"]:
        c.drawCentredString(W / 2, y, item)
        y -= 18

    # White bottom half
    c.setFillColor(WHITE)
    c.rect(0, 0, W, H / 2, fill=1, stroke=0)

    # TPT link
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(W / 2, H / 2 - 40, "Find it on Teachers Pay Teachers:")
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(W / 2, H / 2 - 64, "teacherspayteachers.com/store/communicate-by-design")

    # Seasonal notes
    c.setFillColor(HexColor("#555555"))
    c.setFont("Helvetica-Oblique", 11)
    c.drawCentredString(W / 2, H / 2 - 100, cfg["seasonal_note1"])
    c.drawCentredString(W / 2, H / 2 - 118, cfg["seasonal_note2"])

    # Bundle callout
    c.setFillColor(HexColor("#F0F4F8"))
    c.roundRect(72, H / 2 - 215, W - 144, 72, 6, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(W / 2, H / 2 - 162, cfg["bundle_line1"])
    c.setFillColor(HexColor("#444444"))
    c.setFont("Helvetica", 10)
    c.drawCentredString(W / 2, H / 2 - 180, cfg["bundle_line2"])

    # About section
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(W / 2, H / 2 - 248, "About Communicate by Design")
    c.setFillColor(HexColor("#444444"))
    c.setFont("Helvetica", 10)
    c.drawCentredString(W / 2, H / 2 - 266,
        "Created by a special educator and advocate. Every resource is built on the belief that")
    c.drawCentredString(W / 2, H / 2 - 282,
        "AT must be explicitly taught — not merely provided — to give complex communicators a genuine chance.")

    # Bottom amber bar
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


# ── 4. Assemble ───────────────────────────────────────────────────────────────
def build_preview(source_pdf=SOURCE_PDF, output_path=OUTPUT_PATH,
                  source_pages=SOURCE_PAGES, cfg=UNIT_CONFIG):
    print("Reading source PDF...")
    source = PdfReader(source_pdf)
    print(f"  Source: {len(source.pages)} pages")

    print("Generating cover...")
    cover_page = PdfReader(make_cover(cfg)).pages[0]

    print("Generating watermark...")
    wm_page = PdfReader(make_watermark()).pages[0]

    print("Generating back page...")
    back_page = PdfReader(make_back(cfg)).pages[0]

    print(f"Extracting and watermarking pages {[p+1 for p in source_pages]}...")
    writer = PdfWriter()

    writer.add_page(cover_page)

    for page_idx in source_pages:
        page = source.pages[page_idx]
        page.merge_page(wm_page)
        writer.add_page(page)

    writer.add_page(back_page)

    print(f"Writing preview PDF ({len(writer.pages)} pages)...")
    with open(output_path, "wb") as f:
        writer.write(f)
    print(f"✅ Preview saved: {output_path}")


if __name__ == "__main__":
    build_preview()

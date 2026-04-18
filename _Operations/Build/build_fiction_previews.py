"""
build_fiction_previews.py — Communicate by Design
Builds watermarked preview PDFs for Fiction Anchor Text units.

Fiction previews are sourced from the Printable Packet PDF (ReportLab-built,
always available). They show the AAC access layer — the unique value proposition
of the fiction line: communication boards, symbol cards, partner setup, and
student response pages.

Preview page selection (all from Printable Packet):
  Cover       — branded CbD cover (generated)
  p.1  idx 0  — Communication Environment Setup (partner reference)
  p.2  idx 1  — Core Word Symbol Cards
  p.4  idx 3  — Communication Board A (character/theme vocabulary, landscape)
  p.6  idx 5  — Communication Board C (literary discussion moves)
  p.9  idx 8  — Student Activity Part 1
  p.13 idx 12 — Student Activity Part 5 (synthesis)
  Back        — branded CTA with TPT store link (generated)

Total: 8 pages (cover + 6 content + back)

USAGE:
  # Build all units:
  python3 _Operations/Build/build_fiction_previews.py

  # Build a single unit:
  python3 _Operations/Build/build_fiction_previews.py --unit wonder

  # Inspect packet pages to verify indices:
  python3 _Operations/Build/build_fiction_previews.py --inspect --unit wonder

DEPENDENCIES:
  pip install pypdf reportlab pymupdf --break-system-packages

OUTPUT:
  Products/Fiction Anchor Texts/[Unit Folder]/TPT Product Files/[Unit]_TPT_Preview.pdf
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

# ── Brand Colors ───────────────────────────────────────────────────────────────
NAVY   = HexColor("#1B1F3B")
TEAL   = HexColor("#006DA0")
TEAL_D = HexColor("#00B4D8")
AMBER  = HexColor("#FFB703")
WHITE  = white
GRAY   = HexColor("#CCCCCC")

W, H = letter  # 612 x 792 pts

BASE         = Path(__file__).parent.parent.parent   # Communicate by Design root
FICTION_ROOT = BASE / "Products" / "Fiction Anchor Texts"
# No central Preview PDFs folder — preview lives in TPT Product Files/ with all upload files

# ── Unit Configurations ────────────────────────────────────────────────────────
#
# SOURCE_PAGES: page indices (0-based) pulled from the Printable Packet PDF.
# Standard fiction preview set:
#   idx 0  = Communication Environment Setup
#   idx 1  = Core Word Symbol Cards
#   idx 3  = Communication Board A (landscape — character/theme vocab)
#   idx 5  = Communication Board C (literary discussion moves)
#   idx 8  = Student Activity Part 1
#   idx 12 = Student Activity Part 5 (synthesis)
#
UNITS = {
    "wonder": {
        "folder":       "Wonder - Character Analysis",
        "tpt_folder":   "TPT Product Files",
        "packet_pdf":   "Wonder_Character_Analysis_Printable_Packet.pdf",
        "output":       "Wonder_TPT_Preview.pdf",
        "source_pages": [0, 1, 3, 5, 8, 12],
        "config": {
            "title_line1":   "Wonder: Character Analysis",
            "title_line2":   "Fiction Anchor Text Unit · Grades 3–8",
            "subtitle":      "A Fiction Anchor Text Unit  |  Character Analysis  |  SPED Grades 3–8",
            "skill_badge":   "RL.5.3 · RL.5.6  —  Character Traits + Point of View",
            "anchor_text":   "Wonder by R.J. Palacio",
            "full_pages":    55,
            "price":         "$6.00",
            "preview_items": [
                "✦  Communication Environment Setup — partner modes, prompt hierarchy, barrier check",
                "✦  Core word symbol cards (12 words, Fitzgerald Key coded)",
                "✦  Communication Board A: Character Description vocabulary (landscape)",
                "✦  Communication Board C: Literary Discussion Moves + annotation codes",
                "✦  Student Activity — Part 1: Who Is Auggie? (character description)",
                "✦  Student Activity — Part 5: Whole-Book Character Analysis (synthesis)",
            ],
            "full_items": [
                "Teaching Materials  ·  5-part whole-novel unit  ·  Partner guidance at point of use",
                "AAC communication boards (3)  ·  Symbol cards (24 words)  ·  Vocabulary Map",
                "Annotation code system: [TRAIT] · [WHY] · [CHANGE]",
                "IEP goal stems  ·  AAC communication goals  ·  Answer key  ·  Rubric",
                "Communication Access Packet  ·  Session Tracker  ·  WCAG 2.2 AA",
            ],
            "seasonal_note1": "Wonder is already on your reading list — now every student has access",
            "seasonal_note2": "Character Analysis  ·  SPED Grades 3–8  ·  AAC-Accessible",
            "bundle_line1":   "Bundle with The Giver: Theme Analysis when Unit 2 launches (May 2026)",
            "bundle_line2":   "Fiction Anchor Text Bundle · SDI grades 3–8",
        },
    },

    "the_giver": {
        "folder":       "The Giver - Theme Analysis",
        "tpt_folder":   "TPT Product Files",
        "packet_pdf":   "The_Giver_Theme_Analysis_Printable_Packet.pdf",
        "output":       "The_Giver_TPT_Preview.pdf",
        "source_pages": [0, 1, 3, 5, 8, 12],
        "config": {
            "title_line1":   "The Giver: Theme Analysis",
            "title_line2":   "Fiction Anchor Text Unit · Grades 6–8",
            "subtitle":      "A Fiction Anchor Text Unit  |  Theme Analysis  |  SPED Grades 6–8",
            "skill_badge":   "RL.7.1 · RL.7.2  —  Theme + Textual Evidence",
            "anchor_text":   "The Giver by Lois Lowry",
            "full_pages":    43,
            "price":         "$6.00",
            "preview_items": [
                "✦  Communication Environment Setup — partner modes, prompt hierarchy, barrier check",
                "✦  Core word symbol cards (12 words, Fitzgerald Key coded)",
                "✦  Communication Board A: Theme Vocabulary (landscape)",
                "✦  Communication Board C: Literary Discussion Moves + annotation codes",
                "✦  Student Activity — Part 1: Theme Introduction (rules of sameness)",
                "✦  Student Activity — Part 5: Whole-Book Theme Synthesis",
            ],
            "full_items": [
                "Teaching Materials  ·  5-part whole-novel unit  ·  Partner guidance at point of use",
                "AAC communication boards (3)  ·  Symbol cards (24 words)  ·  Vocabulary Map",
                "Annotation code system: [THEME] · [EVIDENCE] · [CHANGE]",
                "IEP goal stems  ·  AAC communication goals  ·  Answer key  ·  Rubric",
                "Communication Access Packet  ·  Session Tracker  ·  WCAG 2.2 AA",
            ],
            "seasonal_note1": "The Giver is already in your classroom — now every student has access",
            "seasonal_note2": "Theme Analysis  ·  SPED Grades 6–8  ·  AAC-Accessible",
            "bundle_line1":   "Bundle with Wonder: Character Analysis — Fiction Anchor Text Units 1 & 2",
            "bundle_line2":   "Fiction Anchor Text Bundle · SDI grades 3–8",
        },
    },
}


# ── Cover page ─────────────────────────────────────────────────────────────────

def make_cover(cfg):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)

    # Navy background
    c.setFillColor(NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # Teal header bar
    c.setFillColor(TEAL)
    c.rect(0, H - 72, W, 72, fill=1, stroke=0)
    c.setFillColor(TEAL_D)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(W / 2, H - 44, "COMMUNICATE BY DESIGN")
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Oblique", 11)
    c.drawCentredString(W / 2, H - 60, "Where SDI & AT Meets Practice")

    # PREVIEW badge
    badge_w, badge_h = 180, 42
    badge_x = (W - badge_w) / 2
    badge_y = H - 155
    c.setFillColor(AMBER)
    c.roundRect(badge_x, badge_y, badge_w, badge_h, 6, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(W / 2, badge_y + 12, "PREVIEW")

    # Title
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(W / 2, H - 240, cfg["title_line1"])
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(W / 2, H - 270, cfg["title_line2"])

    # Divider
    c.setStrokeColor(TEAL_D)
    c.setLineWidth(2)
    c.line(72, H - 290, W - 72, H - 290)

    # Subtitle
    c.setFillColor(GRAY)
    c.setFont("Helvetica", 12)
    c.drawCentredString(W / 2, H - 312, cfg["subtitle"])

    # Anchor text label
    c.setFillColor(AMBER)
    c.setFont("Helvetica-Oblique", 11)
    c.drawCentredString(W / 2, H - 334, f"Companion unit for:  {cfg['anchor_text']}")

    # Preview contents box
    c.setFillColor(HexColor("#252A4A"))
    c.roundRect(60, H - 548, W - 120, 190, 8, fill=1, stroke=0)
    c.setFillColor(AMBER)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(84, H - 374, "What's Inside This Preview:")
    c.setFillColor(WHITE)
    c.setFont("Helvetica", 10.5)
    y = H - 394
    for item in cfg["preview_items"]:
        c.drawString(84, y, item)
        y -= 24

    # Skill badge (bottom of box)
    c.setFillColor(TEAL)
    c.roundRect(60, H - 576, 260, 22, 4, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(72, H - 568, cfg["skill_badge"])

    # Page count line
    c.setFillColor(GRAY)
    c.setFont("Helvetica-Oblique", 10)
    c.drawCentredString(W / 2, H - 608,
        f"Full unit: {cfg['full_pages']} pages  ·  This preview: 8 pages")

    # Footer bar
    c.setFillColor(AMBER)
    c.rect(0, 0, W, 58, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(W / 2, 36, "communicatebydesign.substack.com  ·  TPT: Communicate by Design")

    c.save()
    buf.seek(0)
    return buf


# ── Watermark ──────────────────────────────────────────────────────────────────

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

    # Branding stamp (top right)
    c.setFillColor(AMBER)
    c.roundRect(W - 115, H - 34, 105, 24, 4, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(W - 62, H - 25, "COMMUNICATE BY DESIGN")

    c.save()
    buf.seek(0)
    return buf


# ── Back page ──────────────────────────────────────────────────────────────────

def make_back(cfg):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)

    # Top half — navy
    c.setFillColor(NAVY)
    c.rect(0, H / 2, W, H / 2, fill=1, stroke=0)

    c.setFillColor(TEAL)
    c.rect(0, H - 72, W, 72, fill=1, stroke=0)
    c.setFillColor(TEAL_D)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(W / 2, H - 44, "COMMUNICATE BY DESIGN")
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Oblique", 11)
    c.drawCentredString(W / 2, H - 60, "Where SDI & AT Meets Practice")

    c.setFillColor(AMBER)
    c.setFont("Helvetica-Bold", 32)
    c.drawCentredString(W / 2, H - 130, "Get the Full Unit")

    c.setFillColor(AMBER)
    c.circle(W / 2, H - 192, 42, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(W / 2, H - 199, cfg["price"])

    c.setStrokeColor(TEAL_D)
    c.setLineWidth(1.5)
    c.line(72, H - 238, W - 72, H - 238)

    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(W / 2, H - 260, "The full unit includes:")

    c.setFont("Helvetica", 10.5)
    y = H - 282
    for item in cfg["full_items"]:
        c.drawCentredString(W / 2, y, item)
        y -= 18

    # Bottom half — white
    c.setFillColor(WHITE)
    c.rect(0, 0, W, H / 2, fill=1, stroke=0)

    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(W / 2, H / 2 - 40, "Find it on Teachers Pay Teachers:")
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(W / 2, H / 2 - 62, "teacherspayteachers.com/store/communicate-by-design")

    c.setFillColor(HexColor("#555555"))
    c.setFont("Helvetica-Oblique", 11)
    c.drawCentredString(W / 2, H / 2 - 96, cfg["seasonal_note1"])
    c.drawCentredString(W / 2, H / 2 - 114, cfg["seasonal_note2"])

    # Bundle box
    c.setFillColor(HexColor("#F0F4F8"))
    c.roundRect(72, H / 2 - 210, W - 144, 68, 6, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(W / 2, H / 2 - 158, cfg["bundle_line1"])
    c.setFillColor(HexColor("#444444"))
    c.setFont("Helvetica", 10)
    c.drawCentredString(W / 2, H / 2 - 176, cfg["bundle_line2"])

    # About section
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(W / 2, H / 2 - 242, "About Communicate by Design")
    c.setFillColor(HexColor("#444444"))
    c.setFont("Helvetica", 10)
    c.drawCentredString(W / 2, H / 2 - 258,
        "Created by a special educator and advocate. Every resource is built on the belief that")
    c.drawCentredString(W / 2, H / 2 - 274,
        "access design is not a supplement — it is the instruction. The standard does not change.")

    # Footer
    c.setFillColor(AMBER)
    c.rect(0, 0, W, 48, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(W / 2, 28, "communicatebydesign.substack.com")
    c.setFont("Helvetica", 9)
    c.drawCentredString(W / 2, 14, "@communicatebydesignaac  ·  Where SDI & AT Meets Practice")

    c.save()
    buf.seek(0)
    return buf


# ── Inspector ──────────────────────────────────────────────────────────────────

def inspect_unit(unit_key):
    unit = UNITS[unit_key]
    packet_path = FICTION_ROOT / unit["folder"] / unit["packet_pdf"]
    if not packet_path.exists():
        print(f"❌  Packet PDF not found: {packet_path}")
        return
    print(f"\n📄  Inspecting: {packet_path.name}  ({unit_key})")
    print(f"{'─'*70}")
    reader = PdfReader(str(packet_path))
    print(f"    Total pages: {len(reader.pages)}\n")
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        snippet = text.replace("\n", " ").strip()[:100]
        print(f"  idx {i:3d}  (p{i+1:3d}):  {snippet}")
    print()


# ── Builder ────────────────────────────────────────────────────────────────────

def build_preview(unit_key):
    unit = UNITS[unit_key]
    # Look in Product Files/ first (new structure), then unit root (fallback)
    packet_path = FICTION_ROOT / unit["folder"] / "Product Files" / unit["packet_pdf"]
    if not packet_path.exists():
        packet_path = FICTION_ROOT / unit["folder"] / unit["packet_pdf"]

    if not packet_path.exists():
        print(f"\n⚠️   SKIPPING {unit_key} — Printable Packet PDF not found:")
        print(f"     {packet_path}")
        return False

    print(f"\n▶  Building preview: {unit_key}")
    print(f"   Source:  {packet_path.name}")
    source = PdfReader(str(packet_path))
    print(f"   Pages in source: {len(source.pages)}")

    # Validate page indices
    max_idx = len(source.pages) - 1
    valid_pages = []
    for idx in unit["source_pages"]:
        if idx <= max_idx:
            valid_pages.append(idx)
        else:
            print(f"   ⚠️  Page index {idx} out of range (max {max_idx}) — skipping")

    if len(valid_pages) < 4:
        print(f"   ❌  Too few valid pages ({len(valid_pages)}). Run --inspect to verify.")
        return False

    # Generate branded pages
    cover_page = PdfReader(make_cover(unit["config"])).pages[0]
    wm_page    = PdfReader(make_watermark()).pages[0]
    back_page  = PdfReader(make_back(unit["config"])).pages[0]

    # Assemble: cover + watermarked content pages + back
    writer = PdfWriter()
    writer.add_page(cover_page)

    for page_idx in valid_pages:
        page = source.pages[page_idx]
        page.merge_page(wm_page)
        writer.add_page(page)

    writer.add_page(back_page)

    # Output goes into TPT Product Files/ — with all other upload files
    import shutil
    tpt_folder = unit.get("tpt_folder")
    tpt_output_path = FICTION_ROOT / unit["folder"] / tpt_folder / unit["output"]
    tpt_output_path.parent.mkdir(parents=True, exist_ok=True)

    tmp_path = Path("/tmp") / unit["output"]
    with open(str(tmp_path), "wb") as f:
        writer.write(f)
    shutil.copy2(str(tmp_path), str(tpt_output_path))
    print(f"   ✅  Saved ({len(writer.pages)} pages): {tpt_output_path.relative_to(FICTION_ROOT)}")

    return True


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Build CbD fiction preview PDFs")
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
    print(f"  CbD Fiction Preview Builder")
    print(f"  Source: Product Files/[Unit]_Printable_Packet.pdf")
    print(f"  Output: TPT Product Files/[Unit]_TPT_Preview.pdf")
    print(f"{'='*60}")

    results = {}
    for key in targets:
        results[key] = build_preview(key)

    print(f"\n{'─'*60}")
    print("  Summary:")
    for key, ok in results.items():
        status = "✅  Built" if ok else "⚠️   Skipped — packet PDF missing"
        print(f"  {key:<20} {status}")
    print(f"{'─'*60}\n")

    missing = [k for k, ok in results.items() if not ok]
    if missing:
        print("Next steps for missing units:")
        for key in missing:
            unit = UNITS[key]
            print(f"  • {key}: Build {unit['packet_pdf']} first")
            print(f"           python3 Products/Fiction\\ Anchor\\ Texts/{unit['folder']}/build_*.py")
        print(f"\n  Then re-run:  python3 _Operations/Build/build_fiction_previews.py\n")


if __name__ == "__main__":
    main()

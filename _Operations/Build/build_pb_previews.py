"""
build_pb_previews.py — Communicate by Design
Builds watermarked 5-page preview PDFs for Picture Book Companion products.

PREVIEW PAGE ORDER (5 pages):
  1. Branded cover (generated — title, price, what's inside)
  2. Teacher Quick Start p.1 (vocab routine intro) — watermarked
  3. Student Activities p.1 (first activity) — watermarked
  4. Communication Board p.1 — watermarked
  5. Symbol Pages p.1 (Core Words) — watermarked

USAGE:
  # Build all titles:
  python3 _Operations/Build/build_pb_previews.py

  # Build a single title:
  python3 _Operations/Build/build_pb_previews.py --title henry

DEPENDENCIES:
  pip install pypdf reportlab --break-system-packages

OUTPUT:
  Products/Picture Book Companions/[Title folder]/[Title]_TPT_Preview.pdf
"""

import io
import os
import sys
import argparse
from pathlib import Path
from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader

# ── Brand Colors ─────────────────────────────────────────────────────────────
NAVY   = HexColor("#1B1F3B")
ROSE   = HexColor("#D4614E")   # Dusty Rose-Coral — PB Companion line color
AMBER  = HexColor("#FFB703")
WHITE  = white
GRAY   = HexColor("#94A3B8")
LIGHT  = HexColor("#F1F5F9")

W, H = letter  # 612 × 792 pts

BASE = Path(__file__).parent.parent.parent  # Communicate by Design root
PB_ROOT = BASE / "Products" / "Picture Book Companions"

# ── Title Configurations ──────────────────────────────────────────────────────
TITLES = {
    "henry": {
        "folder":       "A Friend for Henry",
        "tpt_folder":   "TPT A Friend for Henry",
        "prefix":       "AFriendForHenry",
        "output":       "AFriendForHenry_TPT_Preview.pdf",
        "config": {
            "title":        "A Friend for Henry",
            "series":       "A Picture Book Companion  |  AAC Read-Aloud Unit",
            "grade":        "Grades K–1",
            "standard":     "RL.K.3 + RL.1.3  |  Character Feelings + Belonging",
            "price":        "$5",
            "preview_items": [
                "✦  Vocabulary routine with ARASAAC symbol cards",
                "✦  Partner scripts for all 3 readings (before · during · after)",
                "✦  Student activities with sentence frames",
                "✦  Student reading tracker (3 readings)",
                "✦  Communication board + symbol pages",
            ],
            "full_items": [
                "Teacher Packet (complete reference with standards + frameworks)",
                "Teacher Quick Start (print-and-go vocab + partner scripts + answer key)",
                "Student Activities + reading tracker + comm board instructions",
                "Communication Board (core + fringe vocabulary)",
                "Symbol Pages (ARASAAC, Fitzgerald Key borders)",
                "Welcome Packet  ·  AAC Session Tracker",
            ],
            "hook": "Zero TPT competition — first mover in AAC + belonging",
            "skill_badge": "Character Feelings + Belonging",
        },
    },
    "river": {
        "folder":       "I Talk Like a River",
        "tpt_folder":   None,   # files in root of folder (no TPT subfolder)
        "prefix":       "ITalkLikeARiver",
        "output":       "ITalkLikeARiver_TPT_Preview.pdf",
        "config": {
            "title":        "I Talk Like a River",
            "series":       "A Picture Book Companion  |  AAC Read-Aloud Unit",
            "grade":        "Grades K–2",
            "standard":     "RL.K.3 + RL.2.3  |  Communication Identity",
            "price":        "$5",
            "preview_items": [
                "✦  Vocabulary routine with ARASAAC symbol cards",
                "✦  Partner scripts for all 3 readings",
                "✦  Student activities with sentence frames",
                "✦  Student reading tracker (3 readings)",
                "✦  Communication board + symbol pages",
            ],
            "full_items": [
                "Teacher Packet (complete reference with standards + frameworks)",
                "Teacher Quick Start (print-and-go vocab + partner scripts + answer key)",
                "Student Activities + reading tracker + comm board instructions",
                "Communication Board (core + fringe vocabulary)",
                "Symbol Pages (ARASAAC, Fitzgerald Key borders)",
                "Welcome Packet  ·  AAC Session Tracker",
            ],
            "hook": "Communication identity — perfect for early AAC users + stuttering representation",
            "skill_badge": "Communication Identity",
        },
    },
    "ians_walk": {
        "folder":       "Ian's Walk",
        "tpt_folder":   None,
        "prefix":       "IansWalk",
        "output":       "IansWalk_TPT_Preview.pdf",
        "config": {
            "title":        "Ian's Walk",
            "series":       "A Picture Book Companion  |  AAC Read-Aloud Unit",
            "grade":        "Grades K–1",
            "standard":     "RL.K.3 + RL.1.3  |  Character Perspective",
            "price":        "$5",
            "preview_items": [
                "✦  Vocabulary routine with ARASAAC symbol cards",
                "✦  Partner scripts for all 3 readings",
                "✦  Student activities with sentence frames",
                "✦  Student reading tracker (3 readings)",
                "✦  Communication board + symbol pages",
            ],
            "full_items": [
                "Teacher Packet (complete reference with standards + frameworks)",
                "Teacher Quick Start (print-and-go vocab + partner scripts + answer key)",
                "Student Activities + reading tracker + comm board instructions",
                "Communication Board (core + fringe vocabulary)",
                "Symbol Pages (ARASAAC, Fitzgerald Key borders)",
                "Welcome Packet  ·  AAC Session Tracker",
            ],
            "hook": "Perspective-taking + sensory experience — autism + AAC representation",
            "skill_badge": "Character Perspective",
        },
    },
    "emmanuel": {
        "folder":       "Emmanuel's Dream",
        "tpt_folder":   "TPT Emmanuel Dream",
        "prefix":       "EmmanuelsDream",
        "output":       "EmmanuelsDream_TPT_Preview.pdf",
        "config": {
            "title":        "Emmanuel's Dream",
            "series":       "A Picture Book Companion  |  AAC Read-Aloud Unit",
            "grade":        "Grades 1–2",
            "standard":     "RL.1.3 + RI.1.3  |  Character Response + Biography",
            "price":        "$5",
            "preview_items": [
                "✦  Vocabulary routine with ARASAAC symbol cards",
                "✦  Partner scripts for all 3 readings",
                "✦  Student activities with sentence frames",
                "✦  Student reading tracker (3 readings)",
                "✦  Communication board + symbol pages",
            ],
            "full_items": [
                "Teacher Packet (complete reference with standards + frameworks)",
                "Teacher Quick Start (print-and-go vocab + partner scripts + answer key)",
                "Student Activities + reading tracker + comm board instructions",
                "Communication Board (core + fringe vocabulary)",
                "Symbol Pages (ARASAAC, Fitzgerald Key borders)",
                "Welcome Packet  ·  AAC Session Tracker",
            ],
            "hook": "Black History Month + Disability Pride Month — biography + persistence",
            "skill_badge": "Character Response + Biography",
        },
    },
    "isabelle": {
        "folder":       "My Friend Isabelle",
        "tpt_folder":   None,
        "prefix":       "MyFriendIsabelle",
        "output":       "MyFriendIsabelle_TPT_Preview.pdf",
        "config": {
            "title":        "My Friend Isabelle",
            "series":       "A Picture Book Companion  |  AAC Read-Aloud Unit",
            "grade":        "Grades K–1",
            "standard":     "RL.K.3 + RL.1.3  |  Friendship + Celebrating Difference",
            "price":        "$5",
            "preview_items": [
                "✦  Vocabulary routine with ARASAAC symbol cards",
                "✦  Partner scripts for all 3 readings",
                "✦  Student activities with sentence frames",
                "✦  Student reading tracker (3 readings)",
                "✦  Communication board + symbol pages",
            ],
            "full_items": [
                "Teacher Packet (complete reference with standards + frameworks)",
                "Teacher Quick Start (print-and-go vocab + partner scripts + answer key)",
                "Student Activities + reading tracker + comm board instructions",
                "Communication Board (core + fringe vocabulary)",
                "Symbol Pages (ARASAAC, Fitzgerald Key borders)",
                "Welcome Packet  ·  AAC Session Tracker",
            ],
            "hook": "Down syndrome representation — friendship + celebrating difference",
            "skill_badge": "Friendship + Celebrating Difference",
        },
    },
}


# ── Watermark Overlay ─────────────────────────────────────────────────────────
def make_watermark():
    """Return a PDF bytes object with a diagonal PREVIEW watermark."""
    buf = io.BytesIO()
    c = rl_canvas.Canvas(buf, pagesize=letter)
    c.saveState()
    c.setFillColor(HexColor("#1B1F3B"))
    c.setFillAlpha(0.07)
    c.setFont("Helvetica-Bold", 52)
    c.translate(W / 2, H / 2)
    c.rotate(40)
    for dx in [-240, 0, 240]:
        for dy in [-200, 0, 200]:
            c.drawCentredString(dx, dy, "PREVIEW")
    c.restoreState()
    c.save()
    buf.seek(0)
    return PdfReader(buf).pages[0]


# ── Branded Cover Page ────────────────────────────────────────────────────────
def make_cover_page(cfg):
    """Generate a branded cover page for the preview PDF."""
    buf = io.BytesIO()
    c = rl_canvas.Canvas(buf, pagesize=letter)

    # Navy background — full page
    c.setFillColor(NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # Rose accent bar — top
    c.setFillColor(ROSE)
    c.rect(0, H - 8, W, 8, fill=1, stroke=0)

    # Rose accent bar — bottom
    c.rect(0, 0, W, 8, fill=1, stroke=0)

    # PREVIEW stamp — top right
    c.setFillColor(ROSE)
    c.setFont("Helvetica-Bold", 9)
    c.drawRightString(W - 20, H - 22, "PREVIEW")

    # Series label — top
    c.setFillColor(HexColor("#94A3B8"))
    c.setFont("Helvetica", 10)
    c.drawCentredString(W / 2, H - 55, cfg["series"])

    # Title — large
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 28)
    title = cfg["title"]
    # Wrap if long
    if len(title) > 24:
        words = title.split()
        mid = len(words) // 2
        line1 = " ".join(words[:mid])
        line2 = " ".join(words[mid:])
        c.drawCentredString(W / 2, H - 100, line1)
        c.drawCentredString(W / 2, H - 132, line2)
        title_bottom = H - 132
    else:
        c.drawCentredString(W / 2, H - 110, title)
        title_bottom = H - 110

    # Grade + standard
    c.setFillColor(ROSE)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(W / 2, title_bottom - 28, cfg["grade"])
    c.setFillColor(HexColor("#94A3B8"))
    c.setFont("Helvetica", 10)
    c.drawCentredString(W / 2, title_bottom - 44, cfg["standard"])

    # Skill badge pill
    badge_y = title_bottom - 70
    badge_text = f"Skill Focus: {cfg['skill_badge']}"
    c.setFillColor(ROSE)
    c.roundRect(W/2 - 130, badge_y - 10, 260, 22, 6, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(W / 2, badge_y + 2, badge_text)

    # Divider
    div_y = badge_y - 24
    c.setStrokeColor(HexColor("#2d3456"))
    c.setLineWidth(1)
    c.line(40, div_y, W - 40, div_y)

    # "This preview includes" section
    col_x = 52
    col_y = div_y - 18
    c.setFillColor(ROSE)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(col_x, col_y, "THIS PREVIEW INCLUDES:")
    col_y -= 14
    c.setFillColor(WHITE)
    c.setFont("Helvetica", 9)
    for item in cfg["preview_items"]:
        c.drawString(col_x, col_y, item)
        col_y -= 13

    # Divider 2
    col_y -= 6
    c.setStrokeColor(HexColor("#2d3456"))
    c.line(40, col_y, W - 40, col_y)
    col_y -= 16

    # "Full purchase includes" section
    c.setFillColor(AMBER)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(col_x, col_y, "FULL PURCHASE INCLUDES:")
    col_y -= 14
    c.setFillColor(HexColor("#94A3B8"))
    c.setFont("Helvetica", 9)
    for item in cfg["full_items"]:
        c.drawString(col_x, col_y, item)
        col_y -= 13

    # Hook line
    col_y -= 10
    c.setFillColor(HexColor("#60A5FA"))
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(col_x, col_y, cfg["hook"])

    # Price box — bottom right
    price_x = W - 100
    price_y = 80
    c.setFillColor(ROSE)
    c.roundRect(price_x - 10, price_y - 10, 90, 46, 8, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica", 8)
    c.drawCentredString(price_x + 35, price_y + 26, "FULL PURCHASE")
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(price_x + 35, price_y + 4, cfg["price"])

    # CbD brand name — bottom left
    c.setFillColor(ROSE)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(40, 80, "Communicate")
    c.setFillColor(AMBER)
    c.drawString(40, 65, "by Design")
    c.setFillColor(HexColor("#94A3B8"))
    c.setFont("Helvetica", 8)
    c.drawString(40, 52, "Where AT Meets Practice")
    c.drawString(40, 40, "communicatebydesign.substack.com")
    c.drawString(40, 28, "tpt.com/store/communicate-by-design")

    # Page number indicator
    c.setFillColor(HexColor("#94A3B8"))
    c.setFont("Helvetica", 7)
    c.drawCentredString(W / 2, 20, "Page 1 of 5  |  Preview Only — Not for Distribution")

    c.save()
    buf.seek(0)
    return PdfReader(buf).pages[0]


# ── Watermark a single source page ───────────────────────────────────────────
def watermark_page(source_page, watermark_page_obj, page_num, total=5):
    """Merge watermark onto source page and add page number footer."""
    # Merge watermark
    source_page.merge_page(watermark_page_obj)

    # Add page number footer via a small overlay
    buf = io.BytesIO()
    c = rl_canvas.Canvas(buf, pagesize=letter)
    c.setFillColor(HexColor("#94A3B8"))
    c.setFont("Helvetica", 7)
    c.drawCentredString(W / 2, 14,
        f"Page {page_num} of {total}  |  PREVIEW — Communicate by Design  |  tpt.com/store/communicate-by-design")
    c.save()
    buf.seek(0)
    footer_page = PdfReader(buf).pages[0]
    source_page.merge_page(footer_page)
    return source_page


# ── Build one title's preview ─────────────────────────────────────────────────
def build_preview(key, unit):
    cfg = unit["config"]
    folder = PB_ROOT / unit["folder"]
    tpt_sub = unit.get("tpt_folder")
    pfx = unit["prefix"]

    # Resolve file paths — check TPT subfolder first, then root folder
    def find_pdf(filename):
        if tpt_sub:
            p = folder / tpt_sub / filename
            if p.exists() and not p.name.startswith(".~"):
                return p
        p = folder / filename
        if p.exists() and not p.name.startswith(".~"):
            return p
        # Last resort: search entire title folder, skip lock files
        matches = [m for m in folder.rglob(filename)
                   if not m.name.startswith(".~") and m.suffix == ".pdf"]
        if matches:
            return matches[0]
        return None

    qs_path       = find_pdf(f"{pfx}_Teacher_QuickStart.pdf")
    act_path      = find_pdf(f"{pfx}_Student_Activities.pdf")
    board_path    = find_pdf(f"{pfx}_Communication_Board.pdf")
    symbols_path  = find_pdf(f"{pfx}_Symbol_Pages.pdf")

    missing = []
    for label, p in [("Teacher_QuickStart", qs_path), ("Student_Activities", act_path),
                     ("Communication_Board", board_path), ("Symbol_Pages", symbols_path)]:
        if not p:
            missing.append(label)
    if missing:
        print(f"  ⚠️  SKIPPING {cfg['title']} — missing: {missing}")
        return

    # Read source PDFs
    qs_reader      = PdfReader(str(qs_path))
    act_reader     = PdfReader(str(act_path))
    board_reader   = PdfReader(str(board_path))
    symbols_reader = PdfReader(str(symbols_path))

    # Make watermark
    wm = make_watermark()

    # Build writer
    writer = PdfWriter()

    # Page 1: Branded cover
    cover = make_cover_page(cfg)
    writer.add_page(cover)

    # Page 2: Teacher Quick Start p.1 (vocab routine / how-to)
    p2 = qs_reader.pages[0]
    writer.add_page(watermark_page(p2, wm, 2))

    # Page 3: Student Activities p.1 (first activity)
    p3 = act_reader.pages[0]
    writer.add_page(watermark_page(p3, wm, 3))

    # Page 4: Communication Board
    p4 = board_reader.pages[0]
    writer.add_page(watermark_page(p4, wm, 4))

    # Page 5: Symbol Pages p.1 (Core Words)
    p5 = symbols_reader.pages[0]
    writer.add_page(watermark_page(p5, wm, 5))

    # Determine output path — save in root of title folder
    out_path = folder / unit["output"]
    with open(out_path, "wb") as f:
        writer.write(f)

    print(f"  ✓  {cfg['title']} → {out_path.name} (5pp)")
    return out_path


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Build Picture Book Companion preview PDFs")
    parser.add_argument("--title", help="Build one title: henry | river | ians_walk | emmanuel | isabelle")
    args = parser.parse_args()

    if args.title:
        key = args.title.lower()
        if key not in TITLES:
            print(f"Unknown title key '{key}'. Valid: {list(TITLES.keys())}")
            sys.exit(1)
        targets = {key: TITLES[key]}
    else:
        targets = TITLES

    print(f"\nBuilding {len(targets)} Picture Book Companion preview PDF(s)...\n")
    built = []
    for key, unit in targets.items():
        print(f"→ {unit['config']['title']}")
        result = build_preview(key, unit)
        if result:
            built.append(result)

    print(f"\n✅  Done — {len(built)}/{len(targets)} preview(s) built.")
    for p in built:
        print(f"   {p}")


if __name__ == "__main__":
    main()

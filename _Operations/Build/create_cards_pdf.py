"""
create_cards_pdf.py
CbD Symbol Card Binder Ecosystem — PDF card sheet generator

Output spec: 9 Cent Copy local printer
  - Card size:    2.75" x 3.75"  (includes 0.125" bleed on all 4 sides)
  - Trim size:    2.5"  x 3.5"   (final card after cutting)
  - Safe zone:    2.25" x 3.25"  (content must stay inside this)
  - Layout:       3 cards across x 2 cards down = 6 cards per letter page
  - Paper:        US Letter 8.5" x 11"
  - DPI:          300

Card 3-zone layout (within trim area):
  Zone 1 — Top bar:    Fitzgerald Key category color + category name (white bold text)
  Zone 2 — Center:     ARASAAC symbol image
  Zone 3 — Bottom:     Word label (bold) + part-of-speech sublabel
  Border:              8pt Fitzgerald Key color border around full card

Visual coding (printed in corner of top bar):
  ★  = core word
  ♥  = heart word
  (none) = fringe word

Usage:
  python3 create_cards_pdf.py --input words.csv --output cards.pdf
  python3 create_cards_pdf.py --demo --output demo_cards.pdf

CSV format:
  word, pos, category, fitzgerald_color, symbol_path, coding
  Example: go, verb, Actions, #2D6A2D, /path/to/go.png, core
"""

import argparse
import csv
import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ─── Dimensions ───────────────────────────────────────────────────────────────

BLEED       = 0.125 * inch   # 0.125" bleed on each side
CARD_W      = 2.5   * inch   # trim width
CARD_H      = 3.5   * inch   # trim height
CARD_W_B    = CARD_W + 2 * BLEED   # 2.75" with bleed
CARD_H_B    = CARD_H + 2 * BLEED   # 3.75" with bleed

SAFE_INSET  = 0.125 * inch   # additional inset from trim edge = safe zone
SAFE_W      = CARD_W - 2 * SAFE_INSET   # 2.25" safe content width
SAFE_H      = CARD_H - 2 * SAFE_INSET   # 3.25" safe content height

COLS        = 3
ROWS        = 2
PAGE_W, PAGE_H = letter   # 612 x 792 pts

# Grid offsets: center the 3x2 grid on letter page
GRID_W = COLS * CARD_W_B
GRID_H = ROWS * CARD_H_B
GRID_X = (PAGE_W - GRID_W) / 2
GRID_Y = (PAGE_H - GRID_H) / 2

# ─── Zone proportions (relative to trim card height) ─────────────────────────

TOP_BAR_H   = CARD_H * 0.18   # ~0.63" category bar
BOTTOM_H    = CARD_H * 0.20   # ~0.70" word label area
SYMBOL_H    = CARD_H - TOP_BAR_H - BOTTOM_H  # remaining center

# ─── Fitzgerald Key color map ─────────────────────────────────────────────────

FITZGERALD = {
    "verb":          "#2D6A2D",   # Green
    "pronoun":       "#B8860B",   # Yellow/gold
    "noun":          "#CC5500",   # Orange
    "adjective":     "#1A5276",   # Blue
    "preposition":   "#7B2D8B",   # Pink/purple
    "social":        "#7B2D8B",   # same as preposition
    "question":      "#6A0572",   # Purple
    "adverb":        "#5D4037",   # Brown
    "conjunction":   "#424242",   # Dark gray
    "negation":      "#B71C1C",   # Red
    "determiner":    "#616161",   # Gray
    "default":       "#1B1F3B",   # CbD Navy fallback
}

POS_LABEL = {
    "verb":          "verb",
    "pronoun":       "pronoun",
    "noun":          "noun",
    "adjective":     "adjective",
    "preposition":   "preposition",
    "social":        "social",
    "question":      "question word",
    "adverb":        "adverb",
    "conjunction":   "conjunction",
    "negation":      "negation",
    "determiner":    "determiner",
}

CATEGORY_LABEL = {
    "verb":          "ACTIONS",
    "pronoun":       "PEOPLE",
    "noun":          "THINGS",
    "adjective":     "DESCRIBING",
    "preposition":   "LITTLE WORDS",
    "social":        "SOCIAL",
    "question":      "QUESTIONS",
    "adverb":        "ADVERBS",
    "conjunction":   "CONNECTORS",
    "negation":      "NEGATION",
    "determiner":    "LITTLE WORDS",
}

CODING_SYMBOL = {
    "core":    "★",
    "heart":   "♥",
    "fringe":  "",
}

# ─── Demo word list ───────────────────────────────────────────────────────────

DEMO_WORDS = [
    {"word": "go",        "pos": "verb",        "coding": "core"},
    {"word": "want",      "pos": "verb",        "coding": "core"},
    {"word": "stop",      "pos": "negation",    "coding": "core"},
    {"word": "I",         "pos": "pronoun",     "coding": "core"},
    {"word": "you",       "pos": "pronoun",     "coding": "core"},
    {"word": "more",      "pos": "adjective",   "coding": "core"},
    {"word": "help",      "pos": "verb",        "coding": "core"},
    {"word": "not",       "pos": "negation",    "coding": "core"},
    {"word": "happy",     "pos": "adjective",   "coding": "fringe"},
    {"word": "the",       "pos": "determiner",  "coding": "core"},
    {"word": "because",   "pos": "conjunction", "coding": "fringe"},
    {"word": "what",      "pos": "question",    "coding": "core"},
]

# ─── Drawing functions ────────────────────────────────────────────────────────

def draw_card(c, x, y, word_data):
    """
    Draw one card at position (x, y) — bottom-left corner of bleed area.
    x, y are in points, measured from bottom-left of page.
    """
    pos      = word_data.get("pos", "default").lower()
    word     = word_data.get("word", "")
    coding   = word_data.get("coding", "fringe").lower()
    symbol_path = word_data.get("symbol_path", None)

    fitz_hex = FITZGERALD.get(pos, FITZGERALD["default"])
    fitz_color = HexColor(fitz_hex)
    cat_label = CATEGORY_LABEL.get(pos, pos.upper())
    pos_label = POS_LABEL.get(pos, pos)
    code_char = CODING_SYMBOL.get(coding, "")

    # Trim card origin (inset by bleed)
    tx = x + BLEED
    ty = y + BLEED

    # ── Background: white card ──
    c.setFillColor(white)
    c.rect(tx, ty, CARD_W, CARD_H, fill=1, stroke=0)

    # ── Border: Fitzgerald color, 3pt ──
    c.setStrokeColor(fitz_color)
    c.setLineWidth(3)
    c.rect(tx, ty, CARD_W, CARD_H, fill=0, stroke=1)

    # ── Zone 1: Top bar ──
    bar_y = ty + CARD_H - TOP_BAR_H
    c.setFillColor(fitz_color)
    c.rect(tx, bar_y, CARD_W, TOP_BAR_H, fill=1, stroke=0)

    # Category label (white, bold, centered)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 9)
    label_x = tx + CARD_W / 2
    label_y = bar_y + TOP_BAR_H / 2 - 4
    c.drawCentredString(label_x, label_y, cat_label)

    # Coding symbol (★ or ♥) — top right of bar
    if code_char:
        c.setFont("Helvetica-Bold", 10)
        c.drawString(tx + CARD_W - 14, bar_y + TOP_BAR_H / 2 - 5, code_char)

    # ── Zone 2: Symbol image (center zone) ──
    sym_y = ty + BOTTOM_H
    sym_h = SYMBOL_H
    sym_x = tx
    sym_w = CARD_W

    if symbol_path and os.path.exists(symbol_path):
        # Draw actual image, centered and padded
        pad = 8
        c.drawImage(symbol_path,
                    sym_x + pad, sym_y + pad,
                    width=sym_w - 2*pad,
                    height=sym_h - 2*pad,
                    preserveAspectRatio=True,
                    anchor='c',
                    mask='auto')
    else:
        # Placeholder: light gray box with word initial
        c.setFillColor(HexColor("#F0F0F0"))
        c.rect(sym_x + 6, sym_y + 6, sym_w - 12, sym_h - 12, fill=1, stroke=0)
        c.setFillColor(HexColor("#AAAAAA"))
        c.setFont("Helvetica", 36)
        c.drawCentredString(sym_x + sym_w/2, sym_y + sym_h/2 - 14, word[0].upper() if word else "?")

    # ── Zone 3: Bottom word label ──
    # Word label (bold, large)
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 14)
    word_label_y = ty + BOTTOM_H * 0.52
    c.drawCentredString(tx + CARD_W/2, word_label_y, word)

    # POS sublabel (smaller, gray)
    c.setFillColor(HexColor("#666666"))
    c.setFont("Helvetica", 7)
    pos_label_y = ty + BOTTOM_H * 0.18
    c.drawCentredString(tx + CARD_W/2, pos_label_y, pos_label)


def draw_cut_marks(c, x, y):
    """Draw hairline cut marks at trim corners (outside bleed area)."""
    tx = x + BLEED
    ty = y + BLEED
    mark = 0.08 * inch
    gap  = 0.04 * inch
    c.setStrokeColor(HexColor("#CCCCCC"))
    c.setLineWidth(0.25)

    corners = [
        (tx, ty),
        (tx + CARD_W, ty),
        (tx, ty + CARD_H),
        (tx + CARD_W, ty + CARD_H),
    ]
    for cx, cy in corners:
        # horizontal mark
        if cx == tx:
            c.line(cx - gap - mark, cy, cx - gap, cy)
        else:
            c.line(cx + gap, cy, cx + gap + mark, cy)
        # vertical mark
        if cy == ty:
            c.line(cx, cy - gap - mark, cx, cy - gap)
        else:
            c.line(cx, cy + gap, cx, cy + gap + mark)


def build_pdf(words, output_path):
    c = canvas.Canvas(output_path, pagesize=letter)
    c.setTitle("CbD Symbol Cards — 9 Cent Copy Print Ready")
    c.setAuthor("Communicate by Design")

    cards_per_page = COLS * ROWS
    total = len(words)
    pages = (total + cards_per_page - 1) // cards_per_page

    for page_num in range(pages):
        start = page_num * cards_per_page
        page_words = words[start:start + cards_per_page]

        for i, word_data in enumerate(page_words):
            col = i % COLS
            row = (ROWS - 1) - (i // COLS)   # top row first
            x = GRID_X + col * CARD_W_B
            y = GRID_Y + row * CARD_H_B

            draw_card(c, x, y, word_data)
            draw_cut_marks(c, x, y)

        # Page label
        c.setFillColor(HexColor("#AAAAAA"))
        c.setFont("Helvetica", 7)
        c.drawCentredString(PAGE_W/2, 18,
            f"Communicate by Design — Symbol Cards — Page {page_num+1}/{pages} "
            f"— Print: 2.75\"×3.75\" on 110# Matte Cardstock — Trim to 2.5\"×3.5\"")

        if page_num < pages - 1:
            c.showPage()

    c.save()
    print(f"✓ Saved: {output_path}  ({total} cards, {pages} page{'s' if pages > 1 else ''})")


# ─── CSV loader ───────────────────────────────────────────────────────────────

def load_csv(path):
    words = []
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            words.append({
                "word":        row.get("word", "").strip(),
                "pos":         row.get("pos", "default").strip().lower(),
                "coding":      row.get("coding", "fringe").strip().lower(),
                "symbol_path": row.get("symbol_path", "").strip(),
            })
    return words


# ─── CLI ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CbD Symbol Card PDF Generator")
    parser.add_argument("--input",  help="CSV file with word list")
    parser.add_argument("--output", default="cbd_symbol_cards.pdf", help="Output PDF path")
    parser.add_argument("--demo",   action="store_true", help="Generate demo cards without CSV")
    args = parser.parse_args()

    if args.demo:
        words = DEMO_WORDS
    elif args.input:
        if not os.path.exists(args.input):
            print(f"Error: CSV not found: {args.input}", file=sys.stderr)
            sys.exit(1)
        words = load_csv(args.input)
    else:
        parser.print_help()
        sys.exit(1)

    build_pdf(words, args.output)

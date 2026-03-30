#!/usr/bin/env python3
"""
CbD Symbol Card PDF Generator — Reusable Template
===================================================
Produces print-ready 2.5" × 3.5" trading cards using ARASAAC symbols.
Standard across ALL Communicate by Design product lines.

Usage:
    from cbd_symbol_cards import build_symbol_cards

    build_symbol_cards(
        unit_title="504 Sit-In 1977",
        words=[
            {"word": "think", "type": "core"},
            {"word": "disability", "type": "fringe"},
            ...
        ],
        output_path="/path/to/output.pdf",
    )

CLI:
    python cbd_symbol_cards.py --unit "504 Sit-In 1977" --vocab vocab.json --output cards.pdf

Design: Approved Session 12 trading card layout.
  Zone 1: Light tint category bar + color dot + dark gray text
  Zone 2: ARASAAC symbol (or empty drawing box with "draw it" tucked top-right)
  Zone 3: Word label in Fitzgerald color + POS sublabel

Dependencies: pip install reportlab --break-system-packages
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, Color
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os, math, json, sys

# ── Paths ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SYMBOL_CACHE = os.path.join(SCRIPT_DIR, "symbol_cache")

# ── Trading card dimensions ──
CARD_W = 2.5 * inch
CARD_H = 3.5 * inch

# Page layout: 3 columns × 3 rows on letter (8.5 × 11)
PAGE_W, PAGE_H = letter
MARGIN_X = (PAGE_W - 3 * CARD_W) / 2
MARGIN_Y = (PAGE_H - 3 * CARD_H) / 2

# Zone heights
CAT_BAR_H = 0.30 * inch
WORD_ZONE_H = 0.55 * inch
FITZ_BORDER = 3  # points


# ══════════════════════════════════════════════════════════════
# FITZGERALD KEY — Python port of fitzgerald_key.js GENERAL sets
# Same categories, same classification logic.
# ══════════════════════════════════════════════════════════════

FITZ_PEOPLE = {
    'i', 'you', 'he', 'she', 'we', 'they', 'my', 'your', 'our', 'their',
    'who', 'someone', 'everyone', 'people', 'human', 'him', 'his', 'us',
    'it', 'me', 'that',
}

FITZ_ACTIONS = {
    'think', 'feel', 'know', 'want', 'need', 'help', 'stop', 'fight', 'change',
    'show', 'prove', 'mean', 'say', 'tell', 'believe', 'make', 'do', 'go', 'get',
    'give', 'like', 'live', 'care', 'move', 'swim', 'learn', 'die', 'protect',
    'paint', 'lie', 'approve', 'deny', 'claim', 'review', 'test', 'occupy',
    'demand', 'sign', 'agree', 'disagree', 'crawl', 'protest', 'verify',
    'corroborate', 'organize', 'contradict', 'cause', 'read', 'write',
    'work', 'use', 'find', 'try', 'put', 'take', 'see', 'look', 'hear',
    'play', 'come', 'turn', 'open', 'close', 'start', 'begin', 'finish',
    'keep', 'bring', 'send', 'build', 'break', 'grow', 'eat', 'drink',
    'sleep', 'walk', 'stand', 'sit', 'wait', 'watch', 'listen', 'talk',
    'speak', 'ask', 'answer', 'explain', 'describe', 'compare', 'analyze',
    'evaluate', 'identify', 'observe', 'support', 'include', 'follow',
    'choose', 'decide', 'create', 'share', 'connect', 'push', 'pull',
}

FITZ_DESCRIPTIONS = {
    'good', 'bad', 'right', 'wrong', 'different', 'same', 'more', 'less',
    'true', 'false', 'strong', 'weak', 'big', 'small', 'little', 'free',
    'safe', 'sick', 'healthy', 'wild', 'dangerous', 'reliable', 'accessible',
    'new', 'old', 'important', 'best', 'hard', 'easy', 'long', 'short',
    'fast', 'slow', 'happy', 'sad', 'angry', 'afraid', 'sure', 'ready',
    'able', 'enough', 'many', 'few', 'all', 'some', 'every', 'each', 'not',
}

FITZ_PREPOSITIONS = {
    'because', 'before', 'after', 'then', 'first', 'last', 'but', 'if',
    'about', 'and', 'which', 'when', 'where', 'today', 'now',
    'here', 'there', 'in', 'on', 'at', 'up', 'down', 'to', 'from',
    'with', 'for', 'of', 'by', 'into', 'out', 'over', 'under', 'between',
    'through', 'during', 'until', 'while', 'also', 'too', 'next', 'again',
    'still', 'already', 'always', 'never', 'sometimes', 'or', 'so',
}

FITZ_SOCIAL = {
    'yes', 'no', 'please', 'thank', 'sorry', 'hi', 'hello', 'bye',
    'why', 'what', 'how', 'question', 'okay', 'wow',
}


def classify_fitzgerald(word):
    """Classify a word into its Fitzgerald Key category.
    Returns dict with: key, color, word_color, bar_tint, dot_color, label, pos_label."""
    w = word.lower()

    if w in FITZ_PEOPLE:
        key = 'People'
    elif w in FITZ_ACTIONS:
        key = 'Actions'
    elif w in FITZ_DESCRIPTIONS:
        key = 'Descriptions'
    elif w in FITZ_PREPOSITIONS:
        key = 'Prepositions'
    elif w in FITZ_SOCIAL:
        key = 'Social'
    else:
        key = 'Nouns'  # Default: nouns (white/gold in Fitzgerald)

    return FITZ_STYLES[key]


# ── Visual styles per Fitzgerald category ──
# Matches approved Session 12 design exactly.
FITZ_STYLES = {
    'People': {
        'key': 'People',
        'color': '#D4A800',        # Border color (Zone 2)
        'word_color': '#B8860B',   # Word text (Zone 3)
        'bar_tint': '#FFF3E0',     # Light tint background (Zone 1)
        'dot_color': '#D4A800',    # Category dot (Zone 1)
        'label': 'PEOPLE / PRONOUNS',
        'pos_label': 'PEOPLE',
    },
    'Actions': {
        'key': 'Actions',
        'color': '#00A86B',
        'word_color': '#2E7D32',
        'bar_tint': '#E8F5E9',
        'dot_color': '#00A86B',
        'label': 'VERBS / ACTIONS',
        'pos_label': 'ACTIONS',
    },
    'Descriptions': {
        'key': 'Descriptions',
        'color': '#FF8C00',
        'word_color': '#E65100',
        'bar_tint': '#FFF3E0',
        'dot_color': '#FF8C00',
        'label': 'DESCRIPTIONS',
        'pos_label': 'DESCRIPTIONS',
    },
    'Nouns': {
        'key': 'Nouns',
        'color': '#8B6914',
        'word_color': '#6B4F10',
        'bar_tint': '#FBE9E7',
        'dot_color': '#8B6914',
        'label': 'NOUNS',
        'pos_label': 'NOUNS',
    },
    'Prepositions': {
        'key': 'Prepositions',
        'color': '#4A90D9',
        'word_color': '#1565C0',
        'bar_tint': '#E3F2FD',
        'dot_color': '#4A90D9',
        'label': 'LITTLE WORDS',
        'pos_label': 'PREPOSITIONS',
    },
    'Social': {
        'key': 'Social',
        'color': '#E88CA5',
        'word_color': '#C2185B',
        'bar_tint': '#FCE4EC',
        'dot_color': '#E88CA5',
        'label': 'SOCIAL / FEELINGS',
        'pos_label': 'SOCIAL',
    },
}


# ══════════════════════════════════════════════════════════════
# Symbol lookup
# ══════════════════════════════════════════════════════════════

def get_symbol_path(word):
    """Get path to cached ARASAAC symbol PNG."""
    clean = word.lower().replace('-', '_').replace("'", "")
    fp = os.path.join(SYMBOL_CACHE, f"arasaac_{clean}.png")
    if os.path.exists(fp):
        return fp
    fp2 = os.path.join(SYMBOL_CACHE, f"arasaac_{word.lower()}.png")
    if os.path.exists(fp2):
        return fp2
    return None


# ══════════════════════════════════════════════════════════════
# Card drawing
# ══════════════════════════════════════════════════════════════

def draw_card(c, x, y, word, is_core=False):
    """Draw a single 2.5×3.5 trading card at position (x, y) — bottom-left corner.
    Approved design: light tint bar + color dot + dark gray text."""
    fitz = classify_fitzgerald(word)

    # Card background with rounded corners
    c.saveState()
    c.setStrokeColor(HexColor("#DDDDDD"))
    c.setLineWidth(0.5)
    c.setFillColor(white)
    c.roundRect(x, y, CARD_W, CARD_H, 8, fill=1, stroke=1)
    c.restoreState()

    # ── ZONE 1: Category bar — light tint + color dot + dark gray text ──
    c.saveState()
    c.setFillColor(HexColor(fitz['bar_tint']))
    c.rect(x + 1, y + CARD_H - CAT_BAR_H, CARD_W - 2, CAT_BAR_H - 1, fill=1, stroke=0)

    # Color dot (left side)
    c.setFillColor(HexColor(fitz['dot_color']))
    c.circle(x + 14, y + CARD_H - CAT_BAR_H / 2, 3, fill=1, stroke=0)

    # Category text (dark gray, left-aligned after dot)
    c.setFillColor(HexColor("#666666"))
    c.setFont("Helvetica-Bold", 7)
    label = fitz['label']
    if is_core:
        label += '  \u2605'
    c.drawString(x + 22, y + CARD_H - CAT_BAR_H / 2 - 3, label)
    c.restoreState()

    # ── ZONE 2: Symbol area with Fitzgerald Key colored border ──
    symbol_x = x + 6
    symbol_y = y + WORD_ZONE_H + 2
    symbol_w = CARD_W - 12
    symbol_h = CARD_H - CAT_BAR_H - WORD_ZONE_H - 8

    c.saveState()
    c.setStrokeColor(HexColor(fitz['color']))
    c.setLineWidth(FITZ_BORDER)
    c.setFillColor(white)
    c.roundRect(symbol_x, symbol_y, symbol_w, symbol_h, 6, fill=1, stroke=1)

    sym_path = get_symbol_path(word)
    sym_cx = symbol_x + symbol_w / 2
    sym_cy = symbol_y + symbol_h / 2

    if sym_path:
        # Draw ARASAAC symbol centered in Zone 2
        img = ImageReader(sym_path)
        img_size = min(symbol_w - 16, symbol_h - 16)
        c.drawImage(
            img,
            sym_cx - img_size / 2,
            sym_cy - img_size / 2,
            width=img_size,
            height=img_size,
            preserveAspectRatio=True,
            mask='auto',
        )
    else:
        # No symbol available — empty drawing box.
        # Tiny "draw it" label tucked into top-right corner only.
        c.setFillColor(HexColor("#CCCCCC"))
        c.setFont("Helvetica", 6)
        c.drawRightString(
            symbol_x + symbol_w - 8,
            symbol_y + symbol_h - 14,
            "draw it \u270F"
        )

    c.restoreState()

    # ── ZONE 3: Word label + part-of-speech sublabel ──
    c.saveState()
    c.setFillColor(HexColor("#FAFAFA"))
    c.rect(x + 1, y + 1, CARD_W - 2, WORD_ZONE_H, fill=1, stroke=0)
    c.setStrokeColor(HexColor("#EEEEEE"))
    c.setLineWidth(0.5)
    c.line(x + 1, y + WORD_ZONE_H, x + CARD_W - 1, y + WORD_ZONE_H)

    # Word text (bold, darker Fitzgerald color)
    c.setFillColor(HexColor(fitz['word_color']))
    font_size = 20
    c.setFont("Helvetica-Bold", font_size)
    text_w = c.stringWidth(word, "Helvetica-Bold", font_size)
    if text_w > CARD_W - 20:
        font_size = 14
        c.setFont("Helvetica-Bold", font_size)
        text_w = c.stringWidth(word, "Helvetica-Bold", font_size)
    if text_w > CARD_W - 20:
        font_size = 11
        c.setFont("Helvetica-Bold", font_size)
        text_w = c.stringWidth(word, "Helvetica-Bold", font_size)
    c.drawString(x + (CARD_W - text_w) / 2, y + WORD_ZONE_H / 2 + 2, word)

    # POS sublabel
    c.setFillColor(Color(0, 0, 0, 0.35))
    c.setFont("Helvetica", 6.5)
    pos_text = fitz['pos_label']
    pos_w = c.stringWidth(pos_text, "Helvetica", 6.5)
    c.drawString(x + (CARD_W - pos_w) / 2, y + 8, pos_text)
    c.restoreState()


def draw_cut_guides(c):
    """Draw light dashed cut guides on page margins."""
    c.saveState()
    c.setStrokeColor(HexColor("#CCCCCC"))
    c.setLineWidth(0.25)
    c.setDash(3, 3)
    for col in range(4):
        gx = MARGIN_X + col * CARD_W
        c.line(gx, 0, gx, MARGIN_Y - 4)
        c.line(gx, PAGE_H - MARGIN_Y + 4, gx, PAGE_H)
    for row in range(4):
        gy = MARGIN_Y + row * CARD_H
        c.line(0, gy, MARGIN_X - 4, gy)
        c.line(PAGE_W - MARGIN_X + 4, gy, PAGE_W, gy)
    c.restoreState()


def draw_page_header(c, text):
    """Minimal header — right-aligned, tiny."""
    c.saveState()
    c.setFont("Helvetica", 6)
    c.setFillColor(HexColor("#BBBBBB"))
    tw = c.stringWidth(text, "Helvetica", 6)
    c.drawString(PAGE_W - MARGIN_X - tw, PAGE_H - MARGIN_Y / 2 + 2, text)
    c.restoreState()


def draw_page_footer(c, page_num, total_pages):
    """Minimal footer with card dimensions."""
    c.saveState()
    c.setFont("Helvetica", 5.5)
    c.setFillColor(HexColor("#BBBBBB"))
    c.drawCentredString(
        PAGE_W / 2, MARGIN_Y / 2 - 2,
        f'2.5" \u00d7 3.5"  \u2022  Page {page_num} of {total_pages}'
    )
    c.restoreState()


# ══════════════════════════════════════════════════════════════
# Main build function — call from any unit build script
# ══════════════════════════════════════════════════════════════

def build_symbol_cards(unit_title, words, output_path):
    """
    Build a print-ready symbol card PDF for any CbD unit.

    Args:
        unit_title: str — e.g. "504 Sit-In 1977", "Radium Girls", "UFLI Lesson 23"
        words: list of dicts — [{"word": "think", "type": "core"}, ...]
                type must be "core" or "fringe"
        output_path: str — full path for the output PDF

    Returns:
        dict with stats: pages, total, core_count, fringe_count, symbols_found, draw_it_count
    """
    core_words = {w['word'] for w in words if w.get('type') == 'core'}
    # Sort: core first (grouped by Fitzgerald category), then fringe (same)
    def sort_key(w):
        is_fringe = 0 if w['word'] in core_words else 1
        fitz = classify_fitzgerald(w['word'])
        cat_order = ['People', 'Actions', 'Descriptions', 'Nouns', 'Prepositions', 'Social']
        cat_idx = cat_order.index(fitz['key']) if fitz['key'] in cat_order else 99
        return (is_fringe, cat_idx, w['word'].lower())

    sorted_words = sorted(words, key=sort_key)
    all_word_strings = [w['word'] for w in sorted_words]

    total_pages = math.ceil(len(all_word_strings) / 9)

    c = canvas.Canvas(output_path, pagesize=letter)
    c.setTitle(f"{unit_title} \u2014 Symbol Cards")
    c.setAuthor("Communicate by Design")

    core_count = len(core_words)

    for page_idx in range(total_pages):
        page_words = sorted_words[page_idx * 9 : (page_idx + 1) * 9]

        draw_cut_guides(c)

        # Determine page label
        first_word_on_page = page_words[0]['word']
        if first_word_on_page in core_words:
            if page_idx == 0:
                header = f"{unit_title} | Core Words"
            else:
                header = f"{unit_title} | Core Words (cont.)"
        else:
            header = f"{unit_title} | Fringe Vocabulary"

        draw_page_header(c, header)
        draw_page_footer(c, page_idx + 1, total_pages)

        for idx, w in enumerate(page_words):
            col = idx % 3
            row = 2 - idx // 3  # top-to-bottom
            cx = MARGIN_X + col * CARD_W
            cy = MARGIN_Y + row * CARD_H
            draw_card(c, cx, cy, w['word'], is_core=(w['word'] in core_words))

        c.showPage()

    c.save()

    # Stats
    symbols_found = sum(1 for w in all_word_strings if get_symbol_path(w))
    draw_it = len(all_word_strings) - symbols_found

    stats = {
        'pages': total_pages,
        'total': len(all_word_strings),
        'core_count': core_count,
        'fringe_count': len(all_word_strings) - core_count,
        'symbols_found': symbols_found,
        'draw_it_count': draw_it,
    }

    print(f"\u2705 Built {stats['pages']} pages, {stats['total']} cards")
    print(f"   Output: {output_path}")
    print(f"   Core: {stats['core_count']} | Fringe: {stats['fringe_count']}")
    print(f"   Symbols: {stats['symbols_found']}/{stats['total']} ({stats['draw_it_count']} Draw It!)")

    return stats


# ══════════════════════════════════════════════════════════════
# CLI — build cards from a JSON vocab file
# ══════════════════════════════════════════════════════════════

def main():
    """CLI entry point. Usage:
        python cbd_symbol_cards.py --unit "Unit Title" --vocab vocab.json --output cards.pdf
        python cbd_symbol_cards.py --unit "504 Sit-In 1977" --vocab-js  (reads cbd_unit_vocab.js unit 4)
    """
    import argparse
    parser = argparse.ArgumentParser(description="CbD Symbol Card PDF Generator")
    parser.add_argument('--unit', required=True, help='Unit title (e.g. "504 Sit-In 1977")')
    parser.add_argument('--vocab', help='Path to vocab JSON file: [{"word": "think", "type": "core"}, ...]')
    parser.add_argument('--output', help='Output PDF path (default: <unit>_Symbol_Cards.pdf in current dir)')

    args = parser.parse_args()

    if args.vocab:
        with open(args.vocab) as f:
            words = json.load(f)
    else:
        print("Error: --vocab is required (JSON file with word list)")
        sys.exit(1)

    output = args.output or f"{args.unit.replace(' ', '_')}_Symbol_Cards.pdf"

    build_symbol_cards(args.unit, words, output)


if __name__ == "__main__":
    main()

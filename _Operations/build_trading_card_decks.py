#!/usr/bin/env python3
"""
build_trading_card_decks.py
===========================
Master build script for ALL CbD AAC Trading Card decks.
Generates print-ready PDFs for 9 Cent Copy Multi-Page Documents product.

Decks:
  1. UFLI Phonics Deck (Lessons 1-34: all symbol cards)
  2. Alphabet Deck (26 lowercase + 26 uppercase + phoneme cards)
  3. Upper Elementary Core Deck (200-300 cross-ecosystem core words)

Print spec (9 Cent Copy — Multi-Page Documents, 1-up):
  - Product: Multi-Page Documents, Both Sides, Full Color
  - Page size: 2.5" x 3.5" (one card per page — NO multiple-up)
  - Margins: 0.25" white margin built into artwork on all four edges
  - Art area: 2.0" x 3.0" centered on 2.5" x 3.5" page
  - Bleed: White Margin (No Bleed) — printer default
  - Paper: 80# Matte Cover Paper - Heavy Flyer Weight
  - File format: PDF, 300 DPI images
  - Double-sided: odd pages = fronts, even pages = backs
  - Card backs: Canva design DAHEmP8Ai3o (page 1 = florals/butterflies, page 2 = pink rainbow music)

Usage:
  python3 build_trading_card_decks.py --deck ufli
  python3 build_trading_card_decks.py --deck alphabet
  python3 build_trading_card_decks.py --deck core
  python3 build_trading_card_decks.py --deck all

Dependencies: pip install reportlab --break-system-packages
"""

import argparse
import json
import math
import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black, Color
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register DejaVu Sans for Unicode diacritics (breve marks on phonemes)
_DEJAVU_PATH = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
_DEJAVU_BOLD_PATH = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
if os.path.exists(_DEJAVU_PATH):
    pdfmetrics.registerFont(TTFont('DejaVuSans', _DEJAVU_PATH))
if os.path.exists(_DEJAVU_BOLD_PATH):
    pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', _DEJAVU_BOLD_PATH))

# ── Paths ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SYMBOL_CACHE = os.path.join(SCRIPT_DIR, "symbol_cache")
SYMBOL_LIBRARY = os.path.join(SCRIPT_DIR, "symbol_library")
PRODUCTS_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "Products", "AAC Trading Cards")

# Card back images (exported from Canva design DAHEmP8Ai3o at 300 DPI)
CARD_BACK_DEFAULT = os.path.join(PRODUCTS_DIR, "card_back_default.png")  # Florals/butterflies (white bg, bleed-safe)
CARD_BACK_CUSTOM  = os.path.join(PRODUCTS_DIR, "card_back_pink_rainbow.png")  # Pink rainbow music (Kylee theme)

# ─── Dimensions (9 Cent Copy — White Margin, No Bleed) ──────────────────
CARD_W = 2.5 * inch          # card width
CARD_H = 3.5 * inch          # card height
GUTTER = 0.125 * inch        # 1/8" gap between cards for clean cutting
PRINT_MARGIN = 0.25 * inch   # 9CC requires 0.25" white margin on all edges
# Art area = card minus margins: 2.0" × 3.0"
ART_W = CARD_W - 2 * PRINT_MARGIN
ART_H = CARD_H - 2 * PRINT_MARGIN

COLS = 3
ROWS = 3
PAGE_W, PAGE_H = letter       # 8.5" x 11"

# Grid with gutters between cards:
#   Width:  3×2.5" + 2×0.125" = 7.75"  → side margins 0.375" each ✓
#   Height: 3×3.5" + 2×0.125" = 10.75" → top/bottom margins 0.125" each
GRID_W = COLS * CARD_W + (COLS - 1) * GUTTER   # 7.75"
GRID_H = ROWS * CARD_H + (ROWS - 1) * GUTTER   # 10.75"
GRID_X = (PAGE_W - GRID_W) / 2   # center horizontally
GRID_Y = (PAGE_H - GRID_H) / 2   # center vertically

# Zone proportions (relative to trim card)
TOP_BAR_H = CARD_H * 0.10    # ~0.35" category bar
BOTTOM_H = CARD_H * 0.18     # ~0.63" word label area
SYMBOL_H = CARD_H - TOP_BAR_H - BOTTOM_H

# CbD Brand colors
NAVY = '#1B1F3B'
TEAL = '#006DA0'
AMBER = '#FFB703'
YELLOW = '#FFD700'

# ─── Fitzgerald Key ─────────────────────────────────────────────────────
FITZ_PEOPLE = {
    'i', 'you', 'he', 'she', 'we', 'they', 'my', 'your', 'our', 'their',
    'who', 'someone', 'everyone', 'people', 'human', 'him', 'his', 'us',
    'it', 'me', 'that', 'myself', 'yourself', 'her', 'them', 'its',
    'nobody', 'somebody', 'anybody', 'herself', 'himself', 'themselves',
}

FITZ_ACTIONS = {
    'think', 'feel', 'know', 'want', 'need', 'help', 'stop', 'fight', 'change',
    'show', 'prove', 'mean', 'say', 'tell', 'believe', 'make', 'do', 'go', 'get',
    'give', 'like', 'live', 'care', 'move', 'swim', 'learn', 'die', 'protect',
    'paint', 'lie', 'approve', 'deny', 'claim', 'review', 'test', 'occupy',
    'demand', 'sign', 'agree', 'disagree', 'crawl', 'protest', 'verify',
    'organize', 'cause', 'read', 'write', 'work', 'use', 'find', 'try',
    'put', 'take', 'see', 'look', 'hear', 'play', 'come', 'turn', 'open',
    'close', 'start', 'begin', 'finish', 'keep', 'bring', 'send', 'build',
    'break', 'grow', 'eat', 'drink', 'sleep', 'walk', 'stand', 'sit', 'wait',
    'watch', 'listen', 'talk', 'speak', 'ask', 'answer', 'explain', 'describe',
    'compare', 'analyze', 'evaluate', 'identify', 'observe', 'support',
    'include', 'follow', 'choose', 'decide', 'create', 'share', 'connect',
    'push', 'pull', 'run', 'jump', 'throw', 'catch', 'hold', 'carry',
    'drop', 'pick', 'draw', 'sing', 'dance', 'laugh', 'cry', 'smile',
    'hug', 'kiss', 'touch', 'wash', 'clean', 'cook', 'cut', 'fix',
    'call', 'check', 'count', 'guess', 'hope', 'wish', 'remember',
    'forget', 'understand', 'wonder', 'practice', 'plan', 'measure',
    'add', 'subtract', 'multiply', 'divide', 'solve', 'figure',
    'happen', 'let', 'set', 'fit', 'hit', 'bit', 'got', 'had',
    'has', 'had', 'can', 'could', 'will', 'would', 'should', 'must',
    'did', 'does', 'was', 'were', 'am', 'is', 'are', 'been', 'being',
    'have', 'has', 'had', 'may', 'might', 'shall',
    # CVC words that are verbs
    'nap', 'tap', 'pat', 'sip', 'sit', 'fit', 'pin', 'tip', 'nip',
    'fan', 'dig', 'dip', 'dab', 'jog', 'jab', 'jig', 'beg', 'bet',
    'bid', 'bob', 'bop', 'bud', 'bug', 'bun', 'bus', 'but', 'cab',
    'can', 'cap', 'cop', 'cob', 'cod', 'cog', 'con', 'cot', 'cub',
    'cud', 'cup', 'cut', 'dab', 'dam', 'den', 'dip', 'dog', 'dot',
    'dub', 'dud', 'dug', 'dun', 'fad', 'fag', 'fan', 'fib', 'fig',
    'fin', 'fix', 'fob', 'fog', 'fop', 'fox', 'fun', 'gab', 'gag',
    'gap', 'gas', 'get', 'gig', 'gin', 'got', 'gum', 'gun', 'gut',
    'had', 'ham', 'has', 'hat', 'hem', 'hen', 'hid', 'him', 'hip',
    'hit', 'hob', 'hog', 'hop', 'hot', 'hub', 'hug', 'hum', 'hut',
    'jab', 'jag', 'jam', 'jet', 'jig', 'job', 'jog', 'jot', 'jug',
    'jut', 'keg', 'kid', 'kin', 'kit', 'lag', 'lap', 'led', 'leg',
    'let', 'lid', 'lip', 'lit', 'log', 'lop', 'lot', 'lug',
    'mad', 'man', 'map', 'mat', 'met', 'mix', 'mob', 'mod', 'mom',
    'mop', 'mud', 'mug', 'nab', 'nag', 'net', 'nib', 'nod', 'not',
    'nun', 'nut', 'pad', 'pal', 'pan', 'peg', 'pen', 'pet', 'pig',
    'pit', 'pod', 'pop', 'pot', 'pub', 'pug', 'pun', 'pup', 'put',
    'rag', 'ram', 'ran', 'rap', 'rat', 'red', 'rib', 'rid', 'rig',
    'rim', 'rip', 'rob', 'rod', 'rot', 'rub', 'rug', 'rum', 'run',
    'rut', 'sac', 'sad', 'sag', 'sap', 'sat', 'set', 'sin', 'sob',
    'sod', 'son', 'sop', 'sot', 'sub', 'sum', 'sun', 'sup',
    'tab', 'tad', 'tag', 'tan', 'tat', 'ten', 'tin', 'tit', 'tod',
    'ton', 'top', 'tot', 'tub', 'tug', 'tun',
    'van', 'vat', 'vet', 'vim', 'vow',
    'wad', 'wag', 'wet', 'wig', 'win', 'wit', 'wok', 'won',
    'yak', 'yam', 'yap', 'yet', 'zip', 'zap',
}

FITZ_DESCRIPTIONS = {
    'good', 'bad', 'right', 'wrong', 'different', 'same', 'more', 'less',
    'true', 'false', 'strong', 'weak', 'big', 'small', 'little', 'free',
    'safe', 'sick', 'healthy', 'wild', 'dangerous', 'accessible', 'new',
    'old', 'important', 'best', 'hard', 'easy', 'long', 'short', 'fast',
    'slow', 'happy', 'sad', 'angry', 'afraid', 'sure', 'ready', 'able',
    'enough', 'many', 'few', 'all', 'some', 'every', 'each', 'not',
    'nice', 'mean', 'kind', 'brave', 'funny', 'silly', 'quiet', 'loud',
    'pretty', 'ugly', 'clean', 'dirty', 'cold', 'hot', 'warm', 'cool',
    'dark', 'light', 'bright', 'full', 'empty', 'real', 'fake', 'great',
    'terrible', 'wonderful', 'beautiful', 'ugly', 'huge', 'tiny',
    'thick', 'thin', 'wide', 'narrow', 'deep', 'shallow', 'heavy',
    'dry', 'wet', 'soft', 'rough', 'smooth', 'sharp', 'dull',
    'favorite', 'special', 'certain', 'possible', 'impossible',
    'fair', 'unfair', 'awesome', 'amazing', 'boring', 'interesting',
    'different', 'similar', 'own', 'other', 'another', 'next', 'last',
    'first', 'second', 'third', 'only', 'both', 'whole', 'half',
}

FITZ_PREPOSITIONS = {
    'because', 'before', 'after', 'then', 'but', 'if', 'about', 'and',
    'which', 'when', 'where', 'today', 'now', 'here', 'there', 'in',
    'on', 'at', 'up', 'down', 'to', 'from', 'with', 'for', 'of', 'by',
    'into', 'out', 'over', 'under', 'between', 'through', 'during',
    'until', 'while', 'also', 'too', 'again', 'still', 'already',
    'always', 'never', 'sometimes', 'or', 'so', 'just', 'very',
    'really', 'maybe', 'probably', 'almost', 'together', 'apart',
    'away', 'back', 'off', 'around', 'along', 'across', 'behind',
    'beside', 'above', 'below', 'near', 'far', 'inside', 'outside',
    'except', 'instead', 'without', 'than', 'since', 'yet',
    'however', 'therefore', 'although', 'though',
}

FITZ_SOCIAL = {
    'yes', 'no', 'please', 'thank', 'thanks', 'sorry', 'hi', 'hello',
    'bye', 'goodbye', 'why', 'what', 'how', 'okay', 'wow', 'oh',
    'oops', 'uh-oh', 'yay', 'cool', 'awesome', 'ouch', 'ew', 'hmm',
    'whoa', 'love', 'hate', 'scared', 'worried', 'excited', 'mad',
    'frustrated', 'confused', 'proud', 'embarrassed', 'bored', 'tired',
    'hungry', 'thirsty', 'hurt', 'fine', 'great', 'terrible',
    'like', 'dislike', 'enjoy', 'prefer',
}

# Fitzgerald styles (matching approved Session 12 design)
FITZ_STYLES = {
    'People': {
        'key': 'People', 'color': '#D4A800', 'word_color': '#B8860B',
        'bar_tint': '#FFF8E1', 'dot_color': '#D4A800',
        'label': 'PEOPLE / PRONOUNS', 'pos_label': 'PEOPLE',
        'bar_solid': '#D4A800',
    },
    'Actions': {
        'key': 'Actions', 'color': '#00A86B', 'word_color': '#2E7D32',
        'bar_tint': '#E8F5E9', 'dot_color': '#00A86B',
        'label': 'VERBS / ACTIONS', 'pos_label': 'ACTIONS',
        'bar_solid': '#00A86B',
    },
    'Descriptions': {
        'key': 'Descriptions', 'color': '#FF8C00', 'word_color': '#E65100',
        'bar_tint': '#FFF3E0', 'dot_color': '#FF8C00',
        'label': 'DESCRIPTIONS', 'pos_label': 'DESCRIPTIONS',
        'bar_solid': '#FF8C00',
    },
    'Nouns': {
        'key': 'Nouns', 'color': '#8B6914', 'word_color': '#6B4F10',
        'bar_tint': '#FBE9E7', 'dot_color': '#8B6914',
        'label': 'NOUNS', 'pos_label': 'NOUNS',
        'bar_solid': '#8B6914',
    },
    'Prepositions': {
        'key': 'Prepositions', 'color': '#4A90D9', 'word_color': '#1565C0',
        'bar_tint': '#E3F2FD', 'dot_color': '#4A90D9',
        'label': 'LITTLE WORDS', 'pos_label': 'PREPOSITIONS',
        'bar_solid': '#4A90D9',
    },
    'Social': {
        'key': 'Social', 'color': '#E88CA5', 'word_color': '#C2185B',
        'bar_tint': '#FCE4EC', 'dot_color': '#E88CA5',
        'label': 'SOCIAL / FEELINGS', 'pos_label': 'SOCIAL',
        'bar_solid': '#E88CA5',
    },
}

# Phoneme mapping for alphabet deck
PHONEME_MAP = {
    'a': '/ă/ as in apple',
    'b': '/b/ as in bat',
    'c': '/k/ as in cat',
    'd': '/d/ as in dog',
    'e': '/ĕ/ as in egg',
    'f': '/f/ as in fish',
    'g': '/g/ as in goat',
    'h': '/h/ as in hat',
    'i': '/ĭ/ as in igloo',
    'j': '/j/ as in jump',
    'k': '/k/ as in kite',
    'l': '/l/ as in lamp',
    'm': '/m/ as in map',
    'n': '/n/ as in nest',
    'o': '/ŏ/ as in octopus',
    'p': '/p/ as in pig',
    'q': '/kw/ as in queen',
    'r': '/r/ as in run',
    's': '/s/ as in sun',
    't': '/t/ as in top',
    'u': '/ŭ/ as in up',
    'v': '/v/ as in van',
    'w': '/w/ as in wet',
    'x': '/ks/ as in fox',
    'y': '/y/ as in yes',
    'z': '/z/ as in zip',
}


def classify_fitzgerald(word):
    """Classify a word into Fitzgerald Key category."""
    w = word.lower().strip()
    if w in FITZ_PEOPLE:
        return FITZ_STYLES['People']
    elif w in FITZ_ACTIONS:
        return FITZ_STYLES['Actions']
    elif w in FITZ_DESCRIPTIONS:
        return FITZ_STYLES['Descriptions']
    elif w in FITZ_PREPOSITIONS:
        return FITZ_STYLES['Prepositions']
    elif w in FITZ_SOCIAL:
        return FITZ_STYLES['Social']
    else:
        return FITZ_STYLES['Nouns']


def get_symbol_path(word):
    """Get cached ARASAAC symbol PNG path."""
    clean = word.lower().replace('-', '_').replace("'", "").replace(' ', '_')
    # Check symbol_library first (400 words), then symbol_cache (139 words)
    for base_dir in [SYMBOL_LIBRARY, SYMBOL_CACHE]:
        for name in [f"arasaac_{clean}.png", f"arasaac_{word}.png", f"arasaac_{word.lower()}.png"]:
            fp = os.path.join(base_dir, name)
            if os.path.exists(fp):
                return fp
    return None


# ══════════════════════════════════════════════════════════════
# Card drawing — FRONT
# ══════════════════════════════════════════════════════════════

def draw_front_card(c, x, y, word, is_core=False, card_type='symbol', card_data=None):
    """
    Draw one front card at position (x, y) — bottom-left corner, no bleed.
    card_type: 'symbol', 'letter_lower', 'letter_upper', 'phoneme',
               'lesson_phoneme', 'divider'
    """
    tx = x
    ty = y

    # ── Divider card: special full-card design ──
    if card_type == 'divider':
        _draw_divider_card(c, tx, ty, card_data or {})
        return

    # ── Lesson phoneme card: uses lesson data directly ──
    if card_type == 'lesson_phoneme':
        _draw_lesson_phoneme_card(c, tx, ty, card_data or {})
        return

    fitz = classify_fitzgerald(word) if card_type == 'symbol' else FITZ_STYLES['Nouns']

    # ── White card background ──
    c.saveState()
    c.setFillColor(white)
    c.roundRect(tx, ty, CARD_W, CARD_H, 6, fill=1, stroke=0)

    # ── Border ──
    if card_type == 'symbol':
        c.setStrokeColor(HexColor(fitz['color']))
    elif card_type in ('letter_lower', 'letter_upper'):
        c.setStrokeColor(HexColor(TEAL))
    elif card_type == 'phoneme':
        c.setStrokeColor(HexColor(AMBER))
    c.setLineWidth(3)
    c.roundRect(tx, ty, CARD_W, CARD_H, 6, fill=0, stroke=1)
    c.restoreState()

    if card_type == 'symbol':
        _draw_symbol_card_front(c, tx, ty, word, fitz, is_core)
    elif card_type == 'letter_lower':
        _draw_letter_card_front(c, tx, ty, word, case='lower')
    elif card_type == 'letter_upper':
        _draw_letter_card_front(c, tx, ty, word, case='upper')
    elif card_type == 'phoneme':
        _draw_phoneme_card_front(c, tx, ty, word)


def _draw_divider_card(c, tx, ty, card_data):
    """Lesson divider card — navy background, lesson number, phoneme info.

    These go between lesson groups so the teacher can quickly flip to
    the right lesson in the deck or binder.
    """
    # Navy background with rounded corners
    c.saveState()
    c.setFillColor(HexColor(NAVY))
    c.roundRect(tx, ty, CARD_W, CARD_H, 6, fill=1, stroke=0)

    # Teal inner border
    c.setStrokeColor(HexColor(TEAL))
    c.setLineWidth(2)
    margin = 6
    c.roundRect(tx + margin, ty + margin, CARD_W - 2*margin, CARD_H - 2*margin,
                4, fill=0, stroke=1)

    # Lesson number — big and centered
    lesson_text = card_data.get('word', 'Lesson')
    c.setFillColor(white)
    c.setFont('Helvetica-Bold', 28)
    tw = c.stringWidth(lesson_text, 'Helvetica-Bold', 28)
    c.drawString(tx + (CARD_W - tw) / 2, ty + CARD_H * 0.62, lesson_text)

    # Phoneme / grapheme line — use DejaVu Sans for Unicode breve diacritics
    phoneme = card_data.get('phoneme', '')
    grapheme = card_data.get('grapheme', '')
    if phoneme:
        pg_text = f'{phoneme}  ({grapheme})'
        _pfont = 'DejaVuSans-Bold' if os.path.exists(_DEJAVU_BOLD_PATH) else 'Helvetica-Bold'
        c.setFont(_pfont, 16)
        c.setFillColor(HexColor(AMBER))
        tw = c.stringWidth(pg_text, _pfont, 16)
        c.drawString(tx + (CARD_W - tw) / 2, ty + CARD_H * 0.48, pg_text)

    # Word count summary
    n_new = card_data.get('n_new', 0)
    n_heart = card_data.get('n_heart', 0)
    summary = f'{n_new} words'
    if n_heart:
        summary += f'  +  {n_heart} heart'
    c.setFont('Helvetica', 9)
    c.setFillColor(HexColor('#AAAAAA'))
    tw = c.stringWidth(summary, 'Helvetica', 9)
    c.drawString(tx + (CARD_W - tw) / 2, ty + CARD_H * 0.35, summary)

    # CbD branding at bottom
    c.setFont('Helvetica', 7)
    c.setFillColor(HexColor('#666666'))
    brand = 'Communicate by Design'
    tw = c.stringWidth(brand, 'Helvetica', 7)
    c.drawString(tx + (CARD_W - tw) / 2, ty + 12, brand)

    c.restoreState()


def _draw_symbol_card_front(c, tx, ty, word, fitz, is_core):
    """Symbol card: category bar + ARASAAC image + word label."""
    # Zone 1: Category bar (light tint)
    c.saveState()
    c.setFillColor(HexColor(fitz['bar_tint']))
    c.rect(tx + 2, ty + CARD_H - TOP_BAR_H, CARD_W - 4, TOP_BAR_H - 2, fill=1, stroke=0)

    # Color dot
    c.setFillColor(HexColor(fitz['dot_color']))
    c.circle(tx + 14, ty + CARD_H - TOP_BAR_H / 2, 3, fill=1, stroke=0)

    # Core star indicator (no category text — color dot is enough)
    if is_core:
        c.setFillColor(HexColor('#666666'))
        c.setFont('Helvetica-Bold', 7)
        c.drawString(tx + 22, ty + CARD_H - TOP_BAR_H / 2 - 3, '\u2605')
    c.restoreState()

    # Zone 2: Symbol
    sym_x = tx + 6
    sym_y = ty + BOTTOM_H + 2
    sym_w = CARD_W - 12
    sym_h = SYMBOL_H - 6

    c.saveState()
    c.setStrokeColor(HexColor(fitz['color']))
    c.setLineWidth(2)
    c.setFillColor(white)
    c.roundRect(sym_x, sym_y, sym_w, sym_h, 4, fill=1, stroke=1)

    sym_path = get_symbol_path(word)
    if sym_path:
        img = ImageReader(sym_path)
        img_size = min(sym_w - 16, sym_h - 16)
        c.drawImage(img,
                    sym_x + sym_w/2 - img_size/2,
                    sym_y + sym_h/2 - img_size/2,
                    width=img_size, height=img_size,
                    preserveAspectRatio=True, mask='auto')
    else:
        # Draw-it placeholder
        c.setFillColor(HexColor('#CCCCCC'))
        c.setFont('Helvetica', 6)
        c.drawRightString(sym_x + sym_w - 8, sym_y + sym_h - 14, 'draw it \u270F')
    c.restoreState()

    # Zone 3: Word label
    c.saveState()
    c.setFillColor(HexColor('#FAFAFA'))
    c.rect(tx + 2, ty + 2, CARD_W - 4, BOTTOM_H - 2, fill=1, stroke=0)

    # Word text
    c.setFillColor(HexColor(fitz['word_color']))
    font_size = 18
    c.setFont('Helvetica-Bold', font_size)
    tw = c.stringWidth(word, 'Helvetica-Bold', font_size)
    if tw > CARD_W - 20:
        font_size = 13
        c.setFont('Helvetica-Bold', font_size)
        tw = c.stringWidth(word, 'Helvetica-Bold', font_size)
    c.drawString(tx + (CARD_W - tw) / 2, ty + BOTTOM_H / 2 + 2, word)

    # No POS sublabel — keep cards clean, just color + word
    c.restoreState()


def _draw_letter_card_front(c, tx, ty, letter, case='lower'):
    """Letter card: big letter centered."""
    display = letter.lower() if case == 'lower' else letter.upper()
    color = HexColor(TEAL)

    # Top bar
    c.saveState()
    c.setFillColor(HexColor('#E3F2FD'))
    c.rect(tx + 2, ty + CARD_H - TOP_BAR_H, CARD_W - 4, TOP_BAR_H - 2, fill=1, stroke=0)
    c.restoreState()

    # Big letter in center
    c.saveState()
    c.setFillColor(color)
    font_size = 120
    c.setFont('Helvetica-Bold', font_size)
    tw = c.stringWidth(display, 'Helvetica-Bold', font_size)
    center_y = ty + BOTTOM_H + SYMBOL_H / 2 - font_size * 0.35
    c.drawString(tx + (CARD_W - tw) / 2, center_y, display)
    c.restoreState()

    # Bottom: both cases shown
    c.saveState()
    c.setFillColor(HexColor('#FAFAFA'))
    c.rect(tx + 2, ty + 2, CARD_W - 4, BOTTOM_H - 2, fill=1, stroke=0)
    c.setFillColor(color)
    c.setFont('Helvetica-Bold', 16)
    pair = f'{letter.upper()}{letter.lower()}'
    pw = c.stringWidth(pair, 'Helvetica-Bold', 16)
    c.drawString(tx + (CARD_W - pw) / 2, ty + BOTTOM_H / 2 + 1, pair)
    c.restoreState()


def _draw_phoneme_card_front(c, tx, ty, letter):
    """Phoneme card: phoneme notation + keyword."""
    phoneme_info = PHONEME_MAP.get(letter.lower(), f'/{letter}/')
    parts = phoneme_info.split(' as in ')
    phoneme_text = parts[0]
    keyword = parts[1] if len(parts) > 1 else ''

    # Top bar (amber)
    c.saveState()
    c.setFillColor(HexColor('#FFF8E1'))
    c.rect(tx + 2, ty + CARD_H - TOP_BAR_H, CARD_W - 4, TOP_BAR_H - 2, fill=1, stroke=0)
    c.restoreState()

    # Phoneme in center — use DejaVu Sans for Unicode diacritics
    c.saveState()
    c.setFillColor(HexColor(AMBER))
    font_size = 48
    _pfont = 'DejaVuSans-Bold' if os.path.exists(_DEJAVU_BOLD_PATH) else 'Helvetica-Bold'
    c.setFont(_pfont, font_size)
    tw = c.stringWidth(phoneme_text, _pfont, font_size)
    if tw > CARD_W - 20:
        font_size = 36
        c.setFont(_pfont, font_size)
        tw = c.stringWidth(phoneme_text, _pfont, font_size)
    center_y = ty + BOTTOM_H + SYMBOL_H / 2 + 10
    c.drawString(tx + (CARD_W - tw) / 2, center_y, phoneme_text)

    # Keyword below phoneme
    if keyword:
        c.setFillColor(HexColor('#666666'))
        c.setFont('Helvetica', 14)
        kw_text = f'as in {keyword}'
        kw = c.stringWidth(kw_text, 'Helvetica', 14)
        c.drawString(tx + (CARD_W - kw) / 2, center_y - 30, kw_text)
    c.restoreState()

    # Bottom: letter pair
    c.saveState()
    c.setFillColor(HexColor('#FAFAFA'))
    c.rect(tx + 2, ty + 2, CARD_W - 4, BOTTOM_H - 2, fill=1, stroke=0)
    c.setFillColor(HexColor(NAVY))
    c.setFont('Helvetica-Bold', 16)
    pair = f'{letter.upper()}{letter.lower()}'
    pw = c.stringWidth(pair, 'Helvetica-Bold', 16)
    c.drawString(tx + (CARD_W - pw) / 2, ty + BOTTOM_H / 2 + 1, pair)
    c.restoreState()


def _draw_lesson_phoneme_card(c, tx, ty, card_data):
    """Lesson-specific phoneme card — shows phoneme, grapheme, keyword.

    Unlike _draw_phoneme_card_front (which takes a single letter),
    this uses the lesson's actual phoneme/grapheme data, handling
    multi-char graphemes like 'qu', '-s', 'CVC', etc.
    """
    phoneme = card_data.get('phoneme', '')   # e.g. '/ŭ/'
    grapheme = card_data.get('grapheme', '')  # e.g. 'u', 'qu', '-s'
    lesson_num = card_data.get('lesson', 0)

    # Try to get keyword from PHONEME_MAP via first letter of grapheme
    keyword = ''
    g_letter = grapheme.lstrip('-').lower()[:1]
    if g_letter and g_letter in PHONEME_MAP:
        parts = PHONEME_MAP[g_letter].split(' as in ')
        if len(parts) > 1:
            keyword = parts[1]

    _pfont = 'DejaVuSans-Bold' if os.path.exists(_DEJAVU_BOLD_PATH) else 'Helvetica-Bold'

    # White card background with amber border
    c.saveState()
    c.setFillColor(white)
    c.roundRect(tx, ty, CARD_W, CARD_H, 6, fill=1, stroke=0)
    c.setStrokeColor(HexColor(AMBER))
    c.setLineWidth(3)
    c.roundRect(tx, ty, CARD_W, CARD_H, 6, fill=0, stroke=1)
    c.restoreState()

    # Top bar — amber tint with lesson number
    c.saveState()
    c.setFillColor(HexColor('#FFF8E1'))
    c.rect(tx + 2, ty + CARD_H - TOP_BAR_H, CARD_W - 4, TOP_BAR_H - 2, fill=1, stroke=0)
    c.setFillColor(HexColor('#888888'))
    c.setFont('Helvetica-Bold', 7)
    c.drawCentredString(tx + CARD_W / 2, ty + CARD_H - TOP_BAR_H / 2 - 3,
                        f'LESSON {lesson_num}')
    c.restoreState()

    # Phoneme in center — large, using DejaVu for diacritics
    c.saveState()
    c.setFillColor(HexColor(AMBER))
    font_size = 48
    display = phoneme if phoneme else f'/{grapheme}/'
    c.setFont(_pfont, font_size)
    tw = c.stringWidth(display, _pfont, font_size)
    if tw > CARD_W - 20:
        font_size = 36
        c.setFont(_pfont, font_size)
        tw = c.stringWidth(display, _pfont, font_size)
    if tw > CARD_W - 20:
        font_size = 28
        c.setFont(_pfont, font_size)
        tw = c.stringWidth(display, _pfont, font_size)
    center_y = ty + BOTTOM_H + SYMBOL_H / 2 + 10
    c.drawString(tx + (CARD_W - tw) / 2, center_y, display)

    # Keyword below phoneme
    if keyword:
        c.setFillColor(HexColor('#666666'))
        c.setFont('Helvetica', 14)
        kw_text = f'as in {keyword}'
        kw = c.stringWidth(kw_text, 'Helvetica', 14)
        c.drawString(tx + (CARD_W - kw) / 2, center_y - 30, kw_text)
    c.restoreState()

    # Bottom: grapheme display
    c.saveState()
    c.setFillColor(HexColor('#FAFAFA'))
    c.rect(tx + 2, ty + 2, CARD_W - 4, BOTTOM_H - 2, fill=1, stroke=0)
    c.setFillColor(HexColor(NAVY))
    g_display = grapheme
    if len(grapheme) == 1:
        g_display = f'{grapheme.upper()}{grapheme.lower()}'
    elif len(grapheme) == 2 and grapheme.isalpha():
        g_display = f'{grapheme.upper()}  {grapheme.lower()}'
    c.setFont('Helvetica-Bold', 16)
    gw = c.stringWidth(g_display, 'Helvetica-Bold', 16)
    c.drawString(tx + (CARD_W - gw) / 2, ty + BOTTOM_H / 2 + 1, g_display)
    c.restoreState()


# ══════════════════════════════════════════════════════════════
# Card drawing — BACK (CbD logo on navy)
# ══════════════════════════════════════════════════════════════

def draw_back_card(c, x, y, back_image_path=None):
    """Draw card back using Canva-exported design image.
    Falls back to navy CbD branding if image not found."""
    tx = x
    ty = y

    if back_image_path and os.path.exists(back_image_path):
        # Use Canva back design — 750x1050px = 2.5"x3.5" at 300 DPI
        img = ImageReader(back_image_path)
        c.drawImage(img, tx, ty, width=CARD_W, height=CARD_H,
                    preserveAspectRatio=True, mask='auto')
    else:
        # Fallback: solid navy with CbD text
        c.saveState()
        c.setFillColor(HexColor(NAVY))
        c.roundRect(tx, ty, CARD_W, CARD_H, 6, fill=1, stroke=0)

        c.setFillColor(HexColor('#00B4D8'))
        c.setFont('Helvetica-Bold', 11)
        text1 = 'COMMUNICATE'
        tw1 = c.stringWidth(text1, 'Helvetica-Bold', 11)
        c.drawString(tx + (CARD_W - tw1) / 2, ty + CARD_H / 2 + 20, text1)

        c.setFillColor(HexColor(AMBER))
        c.setFont('Helvetica-Bold', 11)
        text2 = 'BY DESIGN'
        tw2 = c.stringWidth(text2, 'Helvetica-Bold', 11)
        c.drawString(tx + (CARD_W - tw2) / 2, ty + CARD_H / 2 + 4, text2)

        c.setFillColor(HexColor('#8888AA'))
        c.setFont('Helvetica', 6)
        c.drawCentredString(tx + CARD_W / 2, ty + 24, 'Where AT Meets Practice')
        c.restoreState()


# ══════════════════════════════════════════════════════════════
# Cut marks
# ══════════════════════════════════════════════════════════════

def card_position(col, row):
    """Get (x, y) bottom-left position for card at grid (col, row), accounting for gutters."""
    x = GRID_X + col * (CARD_W + GUTTER)
    y = GRID_Y + row * (CARD_H + GUTTER)
    return x, y


def draw_cut_marks(c):
    """Draw hairline cut marks around each card position, accounting for gutters."""
    c.saveState()
    c.setStrokeColor(HexColor('#BBBBBB'))
    c.setLineWidth(0.25)
    mark_len = 0.10 * inch

    # Draw corner marks for each card slot
    for col in range(COLS):
        for row in range(ROWS):
            cx, cy = card_position(col, row)
            # Four corners of this card
            corners = [
                (cx, cy),                          # bottom-left
                (cx + CARD_W, cy),                 # bottom-right
                (cx, cy + CARD_H),                 # top-left
                (cx + CARD_W, cy + CARD_H),        # top-right
            ]
            for (px, py) in corners:
                # Horizontal mark extending into gutter/margin
                if px <= cx:  # left edge
                    c.line(px - mark_len, py, px, py)
                if px >= cx + CARD_W:  # right edge
                    c.line(px, py, px + mark_len, py)
                # Vertical mark extending into gutter/margin
                if py <= cy:  # bottom edge
                    c.line(px, py - mark_len, px, py)
                if py >= cy + CARD_H:  # top edge
                    c.line(px, py, px, py + mark_len)

    c.restoreState()


def draw_page_footer(c, page_num, total_pages, deck_name):
    """Minimal footer."""
    c.saveState()
    c.setFont('Helvetica', 5)
    c.setFillColor(HexColor('#AAAAAA'))
    c.drawCentredString(PAGE_W / 2, 14,
        f'Communicate by Design \u2014 {deck_name} \u2014 Page {page_num}/{total_pages} '
        f'\u2014 Print on cardstock, trim to 2.5" \u00d7 3.5"')
    c.restoreState()


# ══════════════════════════════════════════════════════════════
# PDF builder — interleaved front/back for double-sided
# ══════════════════════════════════════════════════════════════

def build_deck_pdf(cards, output_path, deck_name, cards_per_page=9, back_image=None):
    """
    Build a print-ready PDF — ONE CARD PER PAGE at 2.5" × 3.5".

    9 Cent Copy requirement: No multiple-up. Each page IS one card.
    Page size = 2.5" × 3.5" (trading card).
    Printed both sides: odd pages = fronts, even pages = backs.

    Card backs use Canva-exported PNG image (default: Mrs. McCardel florals).

    Each card dict: {word, type, card_type}
      card_type: 'symbol', 'letter_lower', 'letter_upper', 'phoneme'
      type: 'core', 'fringe', 'heart' (for symbol cards)
    """
    # Resolve back image path
    if back_image is None:
        back_image = CARD_BACK_DEFAULT
    if not os.path.exists(back_image):
        print(f'  \u26a0\ufe0f  Card back image not found: {back_image}')
        print(f'      Using programmatic fallback.')
        back_image = None

    total_cards = len(cards)
    total_pdf_pages = total_cards * 2  # front + back for each card

    # One card per page — page size IS the card size
    card_page = (CARD_W, CARD_H)  # 2.5" × 3.5"

    c = canvas.Canvas(output_path, pagesize=card_page)
    c.setTitle(f'Communicate by Design \u2014 {deck_name}')
    c.setAuthor('Communicate by Design')

    for card_idx, card in enumerate(cards):
        card_type = card.get('card_type', 'symbol')
        is_core = card.get('type', '') == 'core'
        word = card.get('word', '')

        # ── FRONT PAGE ──
        # Translate canvas so (0,0) starts at the margin inset.
        # All drawing functions use CARD_W/CARD_H which are unchanged,
        # but we scale the art into the margin-safe zone via translate + scale.
        c.saveState()
        c.translate(PRINT_MARGIN, PRINT_MARGIN)
        c.scale(ART_W / CARD_W, ART_H / CARD_H)
        draw_front_card(c, 0, 0, word, is_core=is_core, card_type=card_type, card_data=card)
        c.restoreState()
        c.showPage()

        # ── BACK PAGE ──
        c.saveState()
        c.translate(PRINT_MARGIN, PRINT_MARGIN)
        c.scale(ART_W / CARD_W, ART_H / CARD_H)
        draw_back_card(c, 0, 0, back_image_path=back_image)
        c.restoreState()
        c.showPage()

    c.save()
    back_label = 'Canva design' if back_image else 'programmatic fallback'
    total_sheets = total_cards  # both sides = 1 sheet per card
    print(f'\n\u2705 {deck_name}')
    print(f'   Cards: {total_cards}')
    print(f'   PDF pages: {total_pdf_pages} ({total_cards} fronts + {total_cards} backs)')
    print(f'   Sheets (both sides): {total_sheets}')
    print(f'   Page size: 2.5" \u00d7 3.5" (one card per page)')
    print(f'   Art area: 2.0" \u00d7 3.0" (0.25" white margin on all edges)')
    print(f'   Backs: {back_label}')
    print(f'   Output: {output_path}')
    return {'cards': total_cards, 'pages': total_pdf_pages, 'sheets': total_sheets, 'path': output_path}


# ══════════════════════════════════════════════════════════════
# DECK BUILDERS
# ══════════════════════════════════════════════════════════════

def build_ufli_deck():
    """Build UFLI Phonics symbol card deck (Lessons 5-34, sorted by lesson).

    Cards are ordered by lesson number so the teacher can flip through
    in sequence. A divider card is inserted before each lesson's words
    for quick navigation.
    """
    json_path = '/sessions/funny-lucid-bardeen/ufli_all_words.json'
    if not os.path.exists(json_path):
        print(f'Error: {json_path} not found. Run word extraction first.')
        sys.exit(1)

    with open(json_path) as f:
        raw_words = json.load(f)

    # Get lesson configs for phoneme/grapheme info on dividers
    lesson_info = {}
    lesson_json = '/sessions/funny-lucid-bardeen/ufli_lessons_all.json'
    if os.path.exists(lesson_json):
        with open(lesson_json) as f:
            for l in json.load(f):
                lesson_info[l['number']] = {
                    'phoneme': l.get('phoneme', ''),
                    'grapheme': l.get('grapheme', ''),
                    'newWords': len(l.get('newWords', [])),
                    'reviewWords': len(l.get('reviewWords', [])),
                    'heartWords': len(l.get('heartWords', [])),
                }

    # Group words by lesson
    from collections import defaultdict
    by_lesson = defaultdict(list)
    for w in raw_words:
        by_lesson[w.get('lesson', 0)].append(w)

    # Build card list: lesson order, divider card before each lesson
    cards = []
    for lesson_num in sorted(by_lesson.keys()):
        if lesson_num < 5:
            continue

        # Insert divider card
        info = lesson_info.get(lesson_num, {})
        phoneme = info.get('phoneme', '')
        grapheme = info.get('grapheme', '')
        n_new = info.get('newWords', len(by_lesson[lesson_num]))
        n_review = info.get('reviewWords', 0)
        n_heart = info.get('heartWords', 0)

        cards.append({
            'word': f'Lesson {lesson_num}',
            'type': 'divider',
            'card_type': 'divider',
            'lesson': lesson_num,
            'phoneme': phoneme,
            'grapheme': grapheme,
            'n_new': n_new,
            'n_review': n_review,
            'n_heart': n_heart,
        })

        # Phoneme card right after divider — student earns this with the lesson
        if phoneme:
            cards.append({
                'word': grapheme,
                'type': 'phoneme',
                'card_type': 'lesson_phoneme',
                'lesson': lesson_num,
                'phoneme': phoneme,
                'grapheme': grapheme,
            })

        # Add word cards for this lesson (core first, then fringe, alphabetical)
        lesson_words = by_lesson[lesson_num]
        lesson_words.sort(key=lambda w: (
            0 if w['type'] == 'core' else 1,
            w['word'].lower()
        ))
        for w in lesson_words:
            cards.append({
                'word': w['word'],
                'type': w['type'],
                'card_type': 'symbol',
                'lesson': lesson_num,
            })

    n_phoneme_cards = sum(1 for c in cards if c.get('card_type') == 'lesson_phoneme')
    n_word_cards = sum(1 for c in cards if c.get('card_type') == 'symbol')
    n_dividers = sum(1 for c in cards if c.get('card_type') == 'divider')
    print(f'  Organized: {len(by_lesson)} lessons, {n_word_cards} word cards + {n_phoneme_cards} phoneme cards + {n_dividers} dividers')

    output = os.path.join(PRODUCTS_DIR, 'UFLI Phonics Deck', 'CbD_UFLI_Symbol_Cards_Print_Ready.pdf')
    return build_deck_pdf(cards, output, 'UFLI Phonics Symbol Cards')


def build_alphabet_deck():
    """Build Alphabet deck: 26 lowercase + 26 uppercase + 26 phoneme = 78 cards."""
    cards = []
    letters = 'abcdefghijklmnopqrstuvwxyz'

    # Lowercase letters
    for letter in letters:
        cards.append({'word': letter, 'type': 'alphabet', 'card_type': 'letter_lower'})

    # Uppercase letters
    for letter in letters:
        cards.append({'word': letter, 'type': 'alphabet', 'card_type': 'letter_upper'})

    # Phoneme cards
    for letter in letters:
        cards.append({'word': letter, 'type': 'alphabet', 'card_type': 'phoneme'})

    output = os.path.join(PRODUCTS_DIR, 'Alphabet Deck', 'CbD_Alphabet_Deck_Print_Ready.pdf')
    return build_deck_pdf(cards, output, 'Alphabet Deck')


def _core_word_lists():
    """
    Return three nested core vocabulary tiers. Each tier includes all words
    from the previous tier. Based on AAC research — tiers reflect AAC
    experience level, NOT age or grade.

    Sources:
      - Project Core (UNC CECP) — 36 universal core words
      - Banajee, DiCarlo, & Stricklin (2003) — toddler core
      - Van Tatenhove (2009) — core vocabulary for AAC
      - TD Snap Core First vocabulary set
      - LAMP/Unity (PRC-Saltillo) core vocabulary
      - Proloquo2Go core vocabulary
      - TouchChat core vocabulary
      - Yorkston & Beukelman core vocabulary research
    """

    # ════════════════════════════════════════════════════════════
    # STARTER CORE (~50 words)
    # Project Core 36 + high-frequency additions from Banajee
    # + Van Tatenhove. Entry point for any new communicator.
    # ════════════════════════════════════════════════════════════
    starter = [
        # Project Core 36 (UNC Center for Literacy & Disability Studies)
        'I', 'you', 'he', 'she', 'it', 'we', 'they',
        'want', 'go', 'get', 'make', 'turn', 'put', 'do',
        'like', 'look', 'help', 'can', 'not', 'is',
        'that', 'the', 'a', 'my', 'his', 'her',
        'on', 'in', 'off', 'up',
        'more', 'all', 'some', 'different',
        'here', 'where', 'what', 'why', 'when', 'how',
        # High-frequency additions (Banajee 2003 + Van Tatenhove)
        'yes', 'no', 'stop', 'open', 'eat', 'drink',
        'big', 'little', 'good', 'bad', 'done', 'again',
        'mine', 'this',
    ]

    # ════════════════════════════════════════════════════════════
    # GROWING CORE (~170 words — includes ALL Starter words)
    # Expanded from Van Tatenhove intermediate, TD Snap/LAMP
    # intermediate grids, Proloquo2Go research, Yorkston
    # ════════════════════════════════════════════════════════════
    growing_additions = [
        # More pronouns/people
        'me', 'him', 'them', 'us', 'our', 'your', 'their',
        # Expanded verbs
        'come', 'see', 'play', 'read', 'write', 'tell', 'say',
        'ask', 'know', 'think', 'feel', 'hear', 'give', 'take',
        'bring', 'show', 'find', 'try', 'use', 'work', 'need',
        'have', 'was', 'are', 'will', 'would', 'could', 'should',
        'let', 'start', 'finish', 'wait', 'sit', 'stand', 'move',
        'run', 'walk', 'talk', 'watch', 'listen', 'laugh', 'cry',
        # Expanded descriptions
        'happy', 'sad', 'mad', 'scared', 'tired', 'sick',
        'hot', 'cold', 'new', 'old', 'fast', 'slow',
        'hard', 'easy', 'fun', 'same', 'other',
        'right', 'wrong', 'first', 'last', 'next',
        'many', 'few', 'much', 'very', 'really',
        # Expanded prepositions/location/time
        'out', 'down', 'with', 'for', 'to', 'from', 'at',
        'about', 'after', 'before', 'now', 'then', 'today',
        'tomorrow', 'yesterday',
        # Social/feelings
        'please', 'thank', 'sorry', 'hi', 'bye',
        'because', 'but', 'and', 'or', 'if',
        # Nouns (high frequency)
        'home', 'school', 'book', 'friend', 'mom', 'dad',
        'name', 'thing', 'place', 'time', 'day', 'way',
        'people', 'water', 'food',
    ]

    # ════════════════════════════════════════════════════════════
    # FULL CORE (~375 words — includes ALL Growing words)
    # Complete cross-ecosystem research set. Academic,
    # social-emotional, and daily living vocabulary.
    # ════════════════════════════════════════════════════════════
    full_additions = [
        # Additional pronouns
        'myself', 'yourself', 'who', 'somebody', 'nobody',
        'everybody', 'someone', 'anyone',
        # Additional verbs
        'love', 'listen', 'sing', 'dance', 'smile',
        'learn', 'explain', 'describe', 'compare', 'choose',
        'decide', 'create', 'build', 'share', 'practice',
        'understand', 'remember', 'forget', 'guess', 'wonder',
        'figure', 'solve', 'plan', 'check', 'fix',
        'begin', 'keep', 'hold', 'carry',
        'speak', 'call', 'send', 'follow', 'join',
        'sleep', 'wash', 'clean', 'cook', 'close',
        'push', 'pull', 'pick', 'drop', 'throw', 'catch', 'jump',
        'break', 'cut', 'grow', 'change', 'happen',
        'must', 'am', 'were', 'has', 'had', 'did',
        'draw',
        # Additional descriptions
        'small', 'less', 'nice', 'mean', 'kind', 'brave',
        'funny', 'silly', 'cool', 'boring', 'interesting',
        'favorite', 'special', 'important', 'ready', 'sure',
        'enough', 'every', 'each', 'another', 'own',
        'real', 'great', 'best', 'fair', 'unfair', 'possible',
        'strong', 'weak', 'full', 'empty', 'dirty',
        'dark', 'light', 'pretty', 'beautiful',
        'both', 'whole', 'half', 'second', 'third', 'only',
        'long', 'short', 'loud', 'quiet',
        # Additional nouns
        'class', 'teacher', 'student', 'paper', 'pencil',
        'computer', 'game', 'test', 'question', 'answer',
        'idea', 'problem', 'story', 'word', 'number',
        'picture', 'page', 'group', 'team', 'project', 'homework',
        'night', 'week', 'minute', 'hour', 'morning',
        'room', 'outside', 'inside',
        'stuff', 'part', 'side',
        'money', 'phone', 'door', 'table',
        'chair', 'bed', 'car', 'bus',
        'hand', 'head', 'eye', 'mouth', 'body',
        'family', 'brother', 'sister', 'baby',
        'boy', 'girl', 'woman', 'kid', 'person', 'man',
        # Additional prepositions / little words
        'of', 'by', 'into', 'over', 'under', 'around',
        'through', 'between', 'near', 'far',
        'there', 'still', 'already', 'always',
        'never', 'sometimes', 'maybe', 'just',
        'almost', 'together', 'away', 'back', 'too', 'also',
        'so', 'than',
        # Additional social/feelings
        'thanks', 'hello', 'okay', 'wow', 'oh', 'oops',
        'excited', 'worried', 'frustrated', 'confused', 'proud',
        'embarrassed', 'bored', 'hurt', 'fine',
        # Words needed for nesting (in Starter/Growing but missing from original Full)
        'that', 'the', 'a', 'done', 'mine', 'this',
        'fun', 'much', 'people',
    ]

    def dedup(word_list):
        seen = set()
        result = []
        for w in word_list:
            wl = w.lower()
            if wl not in seen:
                seen.add(wl)
                result.append(w)
        return result

    starter_words = dedup(starter)
    growing_words = dedup(starter + growing_additions)
    full_words = dedup(starter + growing_additions + full_additions)

    return starter_words, growing_words, full_words


def _build_core_tier(words, tier_name, folder_name, file_prefix):
    """Build a single core deck tier PDF and save word list."""
    cards = []
    for w in words:
        cards.append({
            'word': w,
            'type': 'core',
            'card_type': 'symbol',
        })

    # Sort by Fitzgerald category, then alphabetical
    cat_order = ['People', 'Actions', 'Descriptions', 'Nouns', 'Prepositions', 'Social']
    def sort_key(card):
        fitz = classify_fitzgerald(card['word'])
        cat_idx = cat_order.index(fitz['key']) if fitz['key'] in cat_order else 99
        return (cat_idx, card['word'].lower())
    cards.sort(key=sort_key)

    # Ensure output folder exists
    out_dir = os.path.join(PRODUCTS_DIR, folder_name)
    os.makedirs(out_dir, exist_ok=True)

    # Save word list as JSON
    ref_path = os.path.join(out_dir, f'{file_prefix}_word_list.json')
    with open(ref_path, 'w') as f:
        json.dump([{'word': c['word'], 'category': classify_fitzgerald(c['word'])['key']} for c in cards], f, indent=2)
    print(f'\u2705 {tier_name} word list saved: {ref_path} ({len(cards)} words)')

    output = os.path.join(out_dir, f'CbD_{file_prefix}_Print_Ready.pdf')
    return build_deck_pdf(cards, output, tier_name)


def build_core_decks():
    """Build all three nested core vocabulary tiers."""
    starter_words, growing_words, full_words = _core_word_lists()

    # Verify nesting
    starter_set = {w.lower() for w in starter_words}
    growing_set = {w.lower() for w in growing_words}
    full_set = {w.lower() for w in full_words}
    assert starter_set <= growing_set, f"Starter words missing from Growing: {starter_set - growing_set}"
    assert growing_set <= full_set, f"Growing words missing from Full: {growing_set - full_set}"
    print(f'\n\u2705 Nesting verified: Starter ({len(starter_words)}) \u2286 Growing ({len(growing_words)}) \u2286 Full ({len(full_words)})')

    results = {}
    results['starter'] = _build_core_tier(
        starter_words, 'Starter Core Deck', 'Starter Core Deck', 'Starter_Core')
    results['growing'] = _build_core_tier(
        growing_words, 'Growing Core Deck', 'Growing Core Deck', 'Growing_Core')
    results['full'] = _build_core_tier(
        full_words, 'Full Core Deck', 'Full Core Deck', 'Full_Core')
    return results


def build_core_deck():
    """Backwards-compatible: builds all three core tiers, returns Full stats."""
    results = build_core_decks()
    return results['full']


# ══════════════════════════════════════════════════════════════
# Print Spec File Generator
# ══════════════════════════════════════════════════════════════

def write_print_spec(deck_name, result, output_dir):
    """Write a print spec file for 9 Cent Copy ordering.

    Contains everything needed to place the order:
    card count, page count, sheet count, size, print settings.
    """
    cards = result['cards']
    pages = result['pages']
    sheets = result.get('sheets', cards)  # both sides = 1 sheet per card
    pdf_path = result['path']
    pdf_name = os.path.basename(pdf_path)

    spec_path = os.path.join(output_dir, f'{deck_name.replace(" ", "_")}_Print_Spec.txt')
    with open(spec_path, 'w') as f:
        f.write(f'{"=" * 60}\n')
        f.write(f'PRINT SPEC — {deck_name}\n')
        f.write(f'Communicate by Design\n')
        f.write(f'{"=" * 60}\n\n')

        f.write(f'FILE: {pdf_name}\n\n')

        f.write(f'9 CENT COPY ORDER SETTINGS:\n')
        f.write(f'  Product:             Multi-Page Documents\n')
        f.write(f'  Size:                2.5in x 3.5in\n')
        f.write(f'  Printed On:          Both Sides\n')
        f.write(f'  Number of Pages:     {pages}\n')
        f.write(f'  Sheets of Paper:     {sheets}\n')
        f.write(f'  Color:               Full Color\n')
        f.write(f'  Paper Weight:        80# Matte Cover Paper - Heavy Flyer Weight\n')
        f.write(f'  Bleed:               White Margin (No Bleed)\n')
        f.write(f'  Quantity:            1\n\n')

        f.write(f'DECK CONTENTS:\n')
        f.write(f'  Total cards:         {cards}\n')
        f.write(f'  Total PDF pages:     {pages} ({cards} fronts + {cards} backs)\n')
        f.write(f'  Total sheets:        {sheets} (both sides printed)\n')
        f.write(f'  Page size:           2.5" x 3.5" (one card per page)\n\n')

        f.write(f'IMPORTANT:\n')
        f.write(f'  - Each page is ONE card (2.5" x 3.5"). No multiple-up.\n')
        f.write(f'  - 0.25" white margin built into artwork on all four edges.\n')
        f.write(f'  - Art area: 2.0" x 3.0" centered on 2.5" x 3.5" page.\n')
        f.write(f'  - Odd pages = card fronts, even pages = card backs.\n')
        f.write(f'  - Cards are double-sided: front image + branded back.\n')
        f.write(f'  - No cutting required — each page IS the card.\n')
        f.write(f'  - Use 80# matte cover stock (heavy flyer weight).\n\n')

        f.write(f'BINDER STORAGE:\n')
        f.write(f'  - 9-pocket trading card binder pages (standard hobby supply)\n')
        f.write(f'  - Cards organized by Fitzgerald Key category (color tabs)\n')
        f.write(f'  - 50 binder pages x 9 pockets = 450 card capacity\n\n')

        f.write(f'© Communicate by Design. Where AT Meets Practice.\n')

    print(f'  📄 Print spec: {spec_path}')
    return spec_path


# ══════════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════════

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CbD AAC Trading Card Deck Builder')
    parser.add_argument('--deck', choices=['ufli', 'alphabet', 'core', 'all'],
                        default='all', help='Which deck to build')
    args = parser.parse_args()

    print('=' * 60)
    print('CbD AAC Trading Card Deck Builder')
    print('9 Cent Copy Print-Ready (Double-Sided)')
    print('=' * 60)

    results = {}

    if args.deck in ('ufli', 'all'):
        results['ufli'] = build_ufli_deck()

    if args.deck in ('alphabet', 'all'):
        results['alphabet'] = build_alphabet_deck()

    if args.deck in ('core', 'all'):
        results['core'] = build_core_deck()

    # Generate print spec files
    print('\n📄 Generating print spec files...')
    deck_names = {
        'ufli': 'UFLI Phonics Deck',
        'alphabet': 'Alphabet Deck',
        'core': 'Full Core Deck',
        'starter': 'Starter Core Deck',
        'growing': 'Growing Core Deck',
    }
    for key, r in results.items():
        name = deck_names.get(key, key)
        out_dir = os.path.dirname(r['path'])
        write_print_spec(name, r, out_dir)

    print('\n' + '=' * 60)
    print('BUILD SUMMARY')
    print('=' * 60)
    total_cards = 0
    total_pages = 0
    total_sheets = 0
    for name, r in results.items():
        sheets = r.get('sheets', r['cards'])
        print(f'  {name}: {r["cards"]} cards, {r["pages"]} pages, {sheets} sheets')
        total_cards += r['cards']
        total_pages += r['pages']
        total_sheets += sheets
    print(f'  TOTAL: {total_cards} cards, {total_pages} pages, {total_sheets} sheets')
    print(f'\nAll files in: {PRODUCTS_DIR}')
    print('9 Cent Copy: 2.5x3.5, Both Sides, Full Color, 80# Matte Cover')

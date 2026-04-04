#!/usr/bin/env python3
"""
cbd_trading_cards.py
====================
Shared module for generating AAC trading card deck PDFs from any CbD product.

Every CbD product with AAC words (nonfiction units, UFLI packets, fiction
anchor texts, AT/AAC tools) should include a companion trading card deck.
This module makes it one function call.

Usage in a build script:
    from cbd_trading_cards import build_product_deck

    # Words can be simple strings or dicts with 'word' and optional 'type'
    words = ["think", "feel", "want", "help", "protest", "fight"]
    # — or —
    words = [
        {"word": "think", "type": "core"},
        {"word": "protest", "type": "fringe"},
    ]

    build_product_deck(
        product_name="504 Sit-In Unit",
        words=words,
        output_path="Products/Nonfiction Units/504 Sit-In/CbD_504_Sit_In_Trading_Cards.pdf",
    )

CLI usage (for quick generation without a build script):
    python3 cbd_trading_cards.py --name "504 Sit-In" --words think,feel,want,help --output cards.pdf
    python3 cbd_trading_cards.py --name "Keiko Unit" --json words.json --output cards.pdf

Dependencies: pip install reportlab --break-system-packages

The in-document symbol cards (Component 2 of printable kits) remain at access-
level sizing for student use. These trading cards are the 2.5"×3.5" binder
cards — included in the TPT zip as an optional print resource.
"""

import argparse
import json
import os
import sys

# Import everything we need from the main deck builder
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from build_trading_card_decks import (
    build_deck_pdf,
    classify_fitzgerald,
    get_symbol_path,
    CARD_BACK_DEFAULT,
    PRODUCTS_DIR,
)


def build_product_deck(product_name, words, output_path, back_image=None):
    """
    Generate a trading card deck PDF for any CbD product.

    Args:
        product_name: Display name (e.g., "504 Sit-In Unit", "UFLI Lesson 12")
        words: List of words. Each item can be:
            - A string: "think" (classified as fringe by default)
            - A dict: {"word": "think", "type": "core"} or {"word": "think"}
        output_path: Where to save the PDF (absolute or relative to CWD)
        back_image: Optional path to card back PNG. Defaults to CbD florals.

    Returns:
        dict with 'cards', 'pages', 'path' keys

    Notes:
        - Words are auto-classified into Fitzgerald Key categories
        - ARASAAC symbols are pulled from the shared cache (_Operations/symbol_cache/)
        - Words without cached symbols get a "Draw It" placeholder
        - Core words get a ★ marker on the card
        - Cards are sorted by Fitzgerald category, then alphabetically
        - Output is print-ready for 9 Cent Copy (8.5x11, double-sided, 0.25" margins)
    """
    # Normalize word list
    cards = []
    seen = set()
    for item in words:
        if isinstance(item, str):
            word = item.strip()
            word_type = 'fringe'
        elif isinstance(item, dict):
            word = item.get('word', '').strip()
            word_type = item.get('type', 'fringe')
        else:
            continue

        if not word:
            continue

        # Deduplicate (case-insensitive)
        wl = word.lower()
        if wl in seen:
            continue
        seen.add(wl)

        cards.append({
            'word': word,
            'type': word_type,
            'card_type': 'symbol',
        })

    if not cards:
        print(f'⚠️  No words provided for {product_name} trading cards.')
        return {'cards': 0, 'pages': 0, 'path': output_path}

    # Sort by Fitzgerald category, core first, then alphabetical
    cat_order = ['People', 'Actions', 'Descriptions', 'Nouns', 'Prepositions', 'Social']
    def sort_key(card):
        is_fringe = 0 if card['type'] == 'core' else 1
        fitz = classify_fitzgerald(card['word'])
        cat_idx = cat_order.index(fitz['key']) if fitz['key'] in cat_order else 99
        return (is_fringe, cat_idx, card['word'].lower())

    cards.sort(key=sort_key)

    # Ensure output directory exists
    out_dir = os.path.dirname(os.path.abspath(output_path))
    os.makedirs(out_dir, exist_ok=True)

    # Build the deck
    deck_label = f'{product_name} Trading Cards'
    result = build_deck_pdf(cards, output_path, deck_label, back_image=back_image)

    # Also save word list as JSON alongside the PDF
    json_path = output_path.replace('.pdf', '_word_list.json')
    word_data = [{'word': c['word'], 'type': c['type'],
                  'category': classify_fitzgerald(c['word'])['key']} for c in cards]
    with open(json_path, 'w') as f:
        json.dump(word_data, f, indent=2)

    return result


def build_from_vocab_config(product_name, vocab_config, output_path):
    """
    Build trading cards from a nonfiction unit vocab config (as used in
    _Operations/cbd_unit_vocab.js). Expects a list of dicts with
    'word' and optionally 'core' boolean.

    This is a convenience wrapper for nonfiction units where vocab is
    already structured.
    """
    words = []
    for item in vocab_config:
        word = item.get('word', item.get('term', ''))
        is_core = item.get('core', False)
        words.append({
            'word': word,
            'type': 'core' if is_core else 'fringe',
        })
    return build_product_deck(product_name, words, output_path)


# ══════════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════════

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate AAC trading card deck for any CbD product')
    parser.add_argument('--name', required=True,
                        help='Product name (e.g., "504 Sit-In Unit")')
    parser.add_argument('--words', default=None,
                        help='Comma-separated word list')
    parser.add_argument('--json', default=None, dest='json_file',
                        help='JSON file with word list (array of strings or {word, type} dicts)')
    parser.add_argument('--output', required=True,
                        help='Output PDF path')

    args = parser.parse_args()

    if args.json_file:
        with open(args.json_file) as f:
            words = json.load(f)
    elif args.words:
        words = [w.strip() for w in args.words.split(',')]
    else:
        print('Error: provide --words or --json')
        sys.exit(1)

    result = build_product_deck(args.name, words, args.output)
    print(f'\nDone: {result["cards"]} cards, {result["pages"]} pages → {result["path"]}')

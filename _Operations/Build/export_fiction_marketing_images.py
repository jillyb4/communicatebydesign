#!/usr/bin/env python3
"""
export_fiction_marketing_images.py
Communicate by Design — Fiction Anchor Text Marketing Image Exporter

PURPOSE:
  Exports Image 2 (Communication Board A) and Image 3 (Student Response Page 1)
  as PNG files for Fiction Anchor Text units.

  These PNGs are used for:
    - TPT listing additional images (uploaded alongside the cover)
    - Canva bulk import (Image 2 and Image 3 Canva templates)
    - Tailwind/Pinterest pins (Pins 2 and 3 for each product)

OUTPUT (per-unit structure, locked 2026-04-17):
  Products/Fiction Anchor Texts/[Unit Folder]/Marketing/Images/[Key]_Image2_CommBoard.png
  Products/Fiction Anchor Texts/[Unit Folder]/Marketing/Images/[Key]_Image3_SymbolCards.png
  Products/Fiction Anchor Texts/[Unit Folder]/Marketing/Images/[Key]_Image4_PartnerSetup.png
  Products/Fiction Anchor Texts/[Unit Folder]/Marketing/Images/[Key]_Image5_StudentActivity1.png
  Products/Fiction Anchor Texts/[Unit Folder]/Marketing/Images/[Key]_Image6_StudentActivity2.png

USAGE:
  python3 _Operations/Build/export_fiction_marketing_images.py
  python3 _Operations/Build/export_fiction_marketing_images.py --title "Wonder"

REQUIRES: pymupdf
  pip install pymupdf --break-system-packages

5-IMAGE STANDARD (locked 2026-04-17):
  Image 1 = TPT Cover (from Canva fiction bulk template DAHGBZ-LtRo — Jill exports)
  Image 2 = Communication Board A — Character/Theme Vocabulary (p.4, idx 3)
  Image 3 = Core Word Symbol Cards (p.2, idx 1)
  Image 4 = Partner/Communication Environment Setup page (p.1, idx 0)
  Image 5 = Student Activity Part 1 (p.9, idx 8)
  Image 6 = Student Activity Part 2 (p.10, idx 9)

PAGE INDEX REFERENCE (13-page packet structure):
  idx 0  = Layer 1: Communication Environment Setup ← IMAGE 4
  idx 1  = Layer 2: Core Word Symbol Cards ← IMAGE 3
  idx 2  = Layer 2: Fringe Word Symbol Cards
  idx 3  = Layer 3: Board A (Character/Theme Vocabulary) ← IMAGE 2
  idx 4  = Layer 3: Board B (Emotion + Reasoning)
  idx 5  = Layer 3: Board C (Literary Discussion Moves)
  idx 6  = Layer 4a: Vocabulary Map
  idx 7  = Layer 4b: AAC Session Tracker
  idx 8  = Layer 5: Student Response Part 1 ← IMAGE 5
  idx 9  = Layer 5: Student Response Part 2 ← IMAGE 6
  idx 10 = Layer 5: Student Response Part 3
  idx 11 = Layer 5: Student Response Part 4
  idx 12 = Layer 5: Student Response Part 5

CANVA WORKFLOW:
  1. Upload exported PNGs to Canva media library
  2. Open fiction bulk pin template DAHGBZ-LtRo
  3. Add unit page; reference these PNGs for Image 2 and Image 3 slots
  4. Export cover PNG (Image 1) from bulk template
  5. Upload Image 1, 2, 3 to TPT listing as additional product images

CSV WORKFLOW:
  Canva CSV: [Unit Folder]/Marketing/[Unit]_Canva_BulkImport.csv
  Marketing Plan: [Unit Folder]/Marketing/[Unit]_Marketing_Plan.md
"""

import fitz  # pymupdf
import os
import argparse

# ── CONFIG ───────────────────────────────────────────────────────────────────

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CBD_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))

FICTION_BASE = os.path.join(CBD_ROOT, "Products", "Fiction Anchor Texts")
# Output goes into each unit's Marketing/Images/ folder (per-unit structure, locked 2026-04-17)
# OUT_DIR is resolved per-unit below — not a shared folder

# 2× zoom = ~144 DPI — sharp for web/social, reasonable file size
ZOOM = fitz.Matrix(2, 2)

# Page indices (0-based) to export
IDX_PARTNER_SETUP = 0   # Layer 1: Communication Environment Setup (partner reference page)
IDX_CORE_SYMBOLS  = 1   # Layer 2: Core Word Symbol Cards
IDX_COMM_BOARD    = 3   # Layer 3: Board A — first communication board (Character/Theme vocab)
IDX_STUDENT_P1    = 8   # Layer 5: Student Response Part 1
IDX_STUDENT_P2    = 9   # Layer 5: Student Response Part 2

# Unit registry: (display_title, folder_name, tpt_subfolder, file_key)
# Add new units here as they are built.
FICTION_UNITS = [
    (
        "Wonder",
        "Wonder - Character Analysis",
        "Wonder_Character_Analysis_TPT",
        "Wonder",
    ),
    (
        "The Giver",
        "The Giver - Theme Analysis",
        "The_Giver_Theme_Analysis_TPT",
        "TheGiver",
    ),
    # Future units — add as built:
    # ("Rules", "Rules - Identity", "Rules_Identity_TPT", "Rules"),
    # ("Out of My Mind", "Out of My Mind - Character Voice", "OutOfMyMind_TPT", "OutOfMyMind"),
    # ("Hatchet", "Hatchet - Survival Theme", "Hatchet_TPT", "Hatchet"),
    # ("Ghost", "Ghost - Identity Theme", "Ghost_TPT", "Ghost"),
]


# ── EXPORT FUNCTION ──────────────────────────────────────────────────────────

def find_packet(folder_name, tpt_subfolder, file_key):
    """Find the printable packet PDF. Check TPT subfolder first, then unit root."""
    candidates = [
        os.path.join(FICTION_BASE, folder_name, tpt_subfolder,
                     f"{file_key.replace(' ', '_')}_*Printable_Packet.pdf"),
        os.path.join(FICTION_BASE, folder_name,
                     f"*Printable_Packet.pdf"),
    ]
    # Try TPT subfolder first with known naming pattern
    tpt_path = os.path.join(FICTION_BASE, folder_name, tpt_subfolder)
    unit_path = os.path.join(FICTION_BASE, folder_name)

    for search_dir in [tpt_path, unit_path]:
        if os.path.isdir(search_dir):
            for fname in os.listdir(search_dir):
                if "Printable_Packet" in fname and fname.endswith(".pdf"):
                    return os.path.join(search_dir, fname)
    return None


def export_images(title_filter=None):
    results = []

    for title, folder_name, tpt_subfolder, key in FICTION_UNITS:
        if title_filter and title.lower() != title_filter.lower():
            continue

        # Per-unit output folder: [Unit Folder]/Marketing/Images/
        out_dir = os.path.join(FICTION_BASE, folder_name, "Marketing", "Images")
        os.makedirs(out_dir, exist_ok=True)

        packet_path = find_packet(folder_name, tpt_subfolder, key)

        if not packet_path:
            print(f"  ⚠️  {title}: Printable_Packet.pdf not found in expected folders")
            results.append((title, "MISSING PDF", "MISSING PDF"))
            continue

        print(f"  {title}: reading {os.path.basename(packet_path)}")
        doc = fitz.open(packet_path)
        page_count = len(doc)

        exports = [
            (IDX_COMM_BOARD,    f"{key}_Image2_CommBoard.png",         "Image2 CommBoard"),
            (IDX_CORE_SYMBOLS,  f"{key}_Image3_SymbolCards.png",        "Image3 SymbolCards"),
            (IDX_PARTNER_SETUP, f"{key}_Image4_PartnerSetup.png",       "Image4 PartnerSetup"),
            (IDX_STUDENT_P1,    f"{key}_Image5_StudentActivity1.png",   "Image5 StudentActivity1"),
            (IDX_STUDENT_P2,    f"{key}_Image6_StudentActivity2.png",   "Image6 StudentActivity2"),
        ]

        statuses = []
        for idx, fname, label in exports:
            out_path = os.path.join(out_dir, fname)
            if idx < page_count:
                doc[idx].get_pixmap(matrix=ZOOM).save(out_path)
                statuses.append(f"{label}=✓")
            else:
                print(f"    ⚠️  page idx {idx} not found (only {page_count} pages)")
                statuses.append(f"{label}=MISSING")

        doc.close()
        print(f"    {' | '.join(statuses)}")
        results.append((title, statuses))

    print()
    print("PNGs saved to: [Unit Folder]/Marketing/Images/  (per-unit, per new structure)")
    print()
    print("Next steps:")
    print("  1. Upload PNGs from Marketing/Images/ to your Canva media library")
    print("  2. Open fiction bulk pin template DAHGBZ-LtRo")
    print("  3. Add the unit page; place Image 2 + Image 3 PNGs in their slots")
    print("  4. Export cover PNG (Image 1) from Canva")
    print("  5. Give Claude the 3 Canva image URLs + TPT product URL")
    print("     → Claude will build the 3 Pinterest pins + social post")
    print("  6. Upload Image 1, 2, 3 to TPT listing as additional product images")
    print()
    print("Marketing plan for copy/paste: [Unit Folder]/Marketing/[Unit]_Marketing_Plan.md")
    print("Canva CSV:                      [Unit Folder]/Marketing/[Unit]_Canva_BulkImport.csv")

    return results


# ── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Export marketing PNGs for Fiction Anchor Text units (Image 2 + Image 3)"
    )
    parser.add_argument(
        "--title",
        type=str,
        default=None,
        help='Export one unit only, e.g. --title "Wonder" or --title "The Giver"'
    )
    args = parser.parse_args()

    print("Communicate by Design — Fiction Anchor Text Marketing Image Export")
    print("=" * 60)
    export_images(title_filter=args.title)

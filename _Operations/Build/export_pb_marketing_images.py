#!/usr/bin/env python3
"""
export_pb_marketing_images.py
Communicate by Design — Picture Book Companion Marketing Image Exporter

PURPOSE:
  Exports Image 2 (Communication Board) and Image 3 (Core Word Symbol Cards)
  as PNG files for all 6 Picture Book Companion titles.

  These PNGs are used for:
    - TPT listing additional images (uploaded alongside the cover)
    - Canva bulk import (Image 2 and Image 3 Canva templates)
    - Tailwind/Pinterest pins (Pins 2 and 3 for each product)

OUTPUT:
  Marketing/Product Images/PB Companions/[Key]_Image2_CommBoard.png
  Marketing/Product Images/PB Companions/[Key]_Image3_StudentActivities.png

USAGE:
  python3 _Operations/Build/export_pb_marketing_images.py
  python3 _Operations/Build/export_pb_marketing_images.py --title "A Friend for Henry"

REQUIRES: pymupdf
  pip install pymupdf --break-system-packages

3-IMAGE STANDARD (locked 2026-04-17):
  Image 1 = TPT Cover (from Canva bulk template DAHF6DObHZ4 — Jill exports)
  Image 2 = Communication Board (p.1 of [Key]_Communication_Board.pdf)
  Image 3 = Student Activities (p.1 of [Key]_Student_Activities.pdf)

CANVA BULK IMPORT RULE:
  Upload exported PNGs to Canva media library before running bulk import.
  Reference exact filename in the CSV image2_filename / image3_filename columns.
  image3_filename references [Key]_Image3_StudentActivities.png (Activity 1 page).
  Text variables (title, grade, standards) auto-fill via CSV.
  Images place into the designated frame in the Canva template.
  CSV lives at: Distrubution/Pinterest/PB_Companions_Canva_BulkImport.csv
"""

import fitz  # pymupdf
import os
import sys
import argparse

# ── CONFIG ──────────────────────────────────────────────────────────────────

# Base folder — adjust if running from outside the CbD root
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CBD_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))

PB_BASE = os.path.join(CBD_ROOT, "Products", "Picture Book Companions")
OUT_DIR = os.path.join(CBD_ROOT, "Marketing", "Product Images", "PB Companions")

# Resolution: 2× zoom = ~144 DPI — sharp for web/social, keeps file size reasonable
ZOOM = fitz.Matrix(2, 2)

# Title → (product folder, TPT subfolder, file key)
COMPANIONS = [
    ("A Friend for Henry",      "TPT A Friend for Henry",   "AFriendForHenry"),
    ("I Talk Like a River",     "TPT I Talk Like a River",  "ITalkLikeARiver"),
    ("Ian's Walk",              "TPT Ian's Walk",           "IansWalk"),
    ("Emmanuel's Dream",        "TPT Emmanuel Dream",       "EmmanuelsDream"),
    ("My Friend Isabelle",      "TPT My Friend Isabelle",   "MyFriendIsabelle"),
    ("All the Way to the Top",  "All the Way to the Top",   "AllTheWayToTheTop"),
]

# ── EXPORT FUNCTION ──────────────────────────────────────────────────────────

def export_images(title_filter=None):
    os.makedirs(OUT_DIR, exist_ok=True)

    results = []

    for title, tpt_folder, key in COMPANIONS:
        if title_filter and title.lower() != title_filter.lower():
            continue

        folder = os.path.join(PB_BASE, title, tpt_folder)

        if not os.path.isdir(folder):
            print(f"  ⚠️  {title}: folder not found at {folder}")
            results.append((title, "MISSING FOLDER", "MISSING FOLDER"))
            continue

        # Image 2: Communication Board (page 1)
        comm_pdf = os.path.join(folder, f"{key}_Communication_Board.pdf")
        img2_out = os.path.join(OUT_DIR, f"{key}_Image2_CommBoard.png")

        if os.path.exists(comm_pdf):
            doc = fitz.open(comm_pdf)
            doc[0].get_pixmap(matrix=ZOOM).save(img2_out)
            doc.close()
            status2 = "✓"
        else:
            print(f"  ⚠️  {title}: Communication_Board.pdf not found")
            status2 = "MISSING PDF"

        # Image 3: Student Activities — Activity 1 (page 1)
        sym_pdf = os.path.join(folder, f"{key}_Student_Activities.pdf")
        img3_out = os.path.join(OUT_DIR, f"{key}_Image3_StudentActivities.png")

        if os.path.exists(sym_pdf):
            doc = fitz.open(sym_pdf)
            doc[0].get_pixmap(matrix=ZOOM).save(img3_out)
            doc.close()
            status3 = "✓"
        else:
            print(f"  ⚠️  {title}: Student_Activities.pdf not found")
            status3 = "MISSING PDF"

        print(f"  {title}: Image2={status2}  Image3={status3}")
        results.append((title, status2, status3))

    print()
    print(f"Output folder: {OUT_DIR}")
    print()
    print("Next steps:")
    print("  1. Upload all PNGs to your Canva media library")
    print("  2. Build Canva Image 2 template (Comm Board frame + title/grade text fields)")
    print("  3. Build Canva Image 3 template (Symbol Cards frame + title text field)")
    print("  4. Run Canva bulk import using PB_Companions_Canva_BulkImport.csv")
    print("     (image2_filename and image3_filename columns reference uploaded filenames)")
    print("  5. Upload Image 1, 2, 3 to each TPT listing as additional product images")

    return results


# ── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Export marketing PNGs for Picture Book Companions (Image 2 + Image 3)"
    )
    parser.add_argument(
        "--title",
        type=str,
        default=None,
        help='Export one title only, e.g. --title "A Friend for Henry"'
    )
    args = parser.parse_args()

    print("Communicate by Design — PB Companion Marketing Image Export")
    print("=" * 60)
    export_images(title_filter=args.title)

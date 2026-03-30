"""
build_wonder_assembly.py — Communicate by Design
=================================================
Assembles the final Wonder: Character Analysis PDF for TPT delivery.

STRUCTURE OF THE FINAL PDF:
  Part 1 — Full Unit Guide      (from Wonder_Character_Analysis_COMPLETE.pdf)
  Part 2 — Student Printables   (from Wonder_Character_Analysis_Printable_Packet.pdf)
             p1  Communication Environment Setup
             p2  Core word symbol cards (12 words)
             p3  Fringe word symbol cards (12 words)
             p4  Board A — Character Description
             p5  Board B — Emotion + Reasoning
             p6  Board C — Literary Discussion Moves
             p7  Vocabulary Map
             p8–9 AAC Session Tracker

USAGE:
  python3 build_wonder_assembly.py

PREREQUISITE:
  Wonder_Character_Analysis_COMPLETE.pdf must exist in this folder.
  Create it by opening Wonder_Character_Analysis_COMPLETE.docx in Word
  and using File → Save As → PDF (not Print to PDF).

OUTPUT:
  Wonder_Character_Analysis_FULL.pdf  ←  this is the TPT upload file
"""

import os
import sys
from pypdf import PdfReader, PdfWriter

HERE = os.path.dirname(os.path.abspath(__file__))

UNIT_PDF    = os.path.join(HERE, "Wonder_Character_Analysis_COMPLETE.pdf")
PACKET_PDF  = os.path.join(HERE, "Wonder_Character_Analysis_Printable_Packet.pdf")
OUTPUT_PDF  = os.path.join(HERE, "Wonder_Character_Analysis_FULL.pdf")

UNIT_TITLE  = "Wonder: Character Analysis"

def main():
    print(f"\n{'─' * 60}")
    print(f"CbD Fiction Unit Assembly — {UNIT_TITLE}")
    print(f"{'─' * 60}\n")

    # ── Pre-flight checks ────────────────────────────────────────────────────
    missing = []
    if not os.path.exists(UNIT_PDF):
        missing.append(
            f"  MISSING: {os.path.basename(UNIT_PDF)}\n"
            f"    → Open Wonder_Character_Analysis_COMPLETE.docx in Word\n"
            f"    → File → Save As → PDF\n"
            f"    → Save to this folder as: Wonder_Character_Analysis_COMPLETE.pdf"
        )
    if not os.path.exists(PACKET_PDF):
        missing.append(
            f"  MISSING: {os.path.basename(PACKET_PDF)}\n"
            f"    → Run: python3 build_wonder_printable_packet.py"
        )
    if missing:
        print("⚠️  Cannot assemble — required files missing:\n")
        for m in missing:
            print(m)
        sys.exit(1)

    # ── Merge ────────────────────────────────────────────────────────────────
    unit_reader   = PdfReader(UNIT_PDF)
    packet_reader = PdfReader(PACKET_PDF)
    writer        = PdfWriter()

    print(f"Part 1 — Full Unit Guide")
    for i, page in enumerate(unit_reader.pages):
        writer.add_page(page)
    print(f"  {len(unit_reader.pages)} pages  ← {os.path.basename(UNIT_PDF)}")

    print(f"\nPart 2 — Student Printables")
    for i, page in enumerate(packet_reader.pages):
        writer.add_page(page)
    print(f"  {len(packet_reader.pages)} pages  ← {os.path.basename(PACKET_PDF)}")

    total = len(unit_reader.pages) + len(packet_reader.pages)

    # ── Write output ─────────────────────────────────────────────────────────
    with open(OUTPUT_PDF, "wb") as f:
        writer.write(f)

    size_kb = os.path.getsize(OUTPUT_PDF) / 1024
    print(f"\n{'─' * 60}")
    print(f"✓  FULL PDF assembled: {total} pages  ({size_kb:.0f} KB)")
    print(f"   {OUTPUT_PDF}")
    print(f"\nTPT upload file: Wonder_Character_Analysis_FULL.pdf")
    print(f"  Student printables start at page {len(unit_reader.pages) + 1}")
    print(f"{'─' * 60}\n")

if __name__ == "__main__":
    main()

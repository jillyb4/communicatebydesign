"""
build_student_complete.py — Picture Book Companions
Assembles Student COMPLETE PDF for one or all titles.

Assembly order (matches All the Way to the Top standard):
  1. Student Activities PDF       (export from Word — do NOT use LibreOffice)
  2. Communication Board PDF      (build_symbol_pages_picbook.py output)
  3. Symbol Pages PDF             (build_symbol_pages_picbook.py output)
  4. AAC Communication Session Tracker PDF (shared asset)

Usage:
  python3 build_student_complete.py                  # build all 5
  python3 build_student_complete.py "A Friend for Henry"
  python3 build_student_complete.py "Ian's Walk"
"""

import os, sys
from pypdf import PdfWriter, PdfReader

BASE = os.path.dirname(os.path.abspath(__file__))

TRACKER_PATH = os.path.join(
    BASE, "..", "AT AAC IEP TEAM Supports",
    "AAC Communication Data and Trackers",
    "AAC_Communication_Session_Tracker.pdf"
)

TITLES = [
    {
        "title":   "A Friend for Henry",
        "folder":  "A Friend for Henry",
        "prefix":  "AFriendForHenry",
    },
    {
        "title":   "I Talk Like a River",
        "folder":  "I Talk Like a River",
        "prefix":  "ITalkLikeARiver",
    },
    {
        "title":   "Ian's Walk",
        "folder":  "Ian's Walk",
        "prefix":  "IansWalk",
    },
    {
        "title":   "Emmanuel's Dream",
        "folder":  "Emmanuel's Dream",
        "prefix":  "EmmanuelsDream",
    },
    {
        "title":   "My Friend Isabelle",
        "folder":  "My Friend Isabelle",
        "prefix":  "MyFriendIsabelle",
    },
]


def assemble(t: dict) -> None:
    folder = os.path.join(BASE, t["folder"])
    p = t["prefix"]

    student_pdf   = os.path.join(folder, f"{p}_Student_Activities.pdf")
    comm_board    = os.path.join(folder, f"{p}_Communication_Board.pdf")
    symbol_pages  = os.path.join(folder, f"{p}_Symbol_Pages.pdf")
    tracker       = TRACKER_PATH
    out_path      = os.path.join(folder, f"{p}_Student_COMPLETE.pdf")

    missing = [f for f in [student_pdf, comm_board, symbol_pages, tracker]
               if not os.path.exists(f)]

    if missing:
        print(f"\n⚠  {t['title']} — missing files (skipping):")
        for m in missing:
            label = os.path.basename(m)
            if "Student_Activities.pdf" in m:
                label += "  ← export from Word: File > Save As > PDF"
            print(f"   {label}")
        return

    writer = PdfWriter()
    for path in [student_pdf, comm_board, symbol_pages, tracker]:
        reader = PdfReader(path)
        for page in reader.pages:
            writer.add_page(page)

    with open(out_path, "wb") as f:
        writer.write(f)

    total = sum(len(PdfReader(p).pages)
                for p in [student_pdf, comm_board, symbol_pages, tracker])
    print(f"✓  {t['title']}: {total}pp → {os.path.basename(out_path)}")


def main():
    arg = " ".join(sys.argv[1:]).strip() if len(sys.argv) > 1 else ""

    if arg:
        matches = [t for t in TITLES if t["title"].lower() == arg.lower()
                   or t["folder"].lower() == arg.lower()]
        if not matches:
            print(f"Unknown title: {arg}")
            print("Available:", [t["title"] for t in TITLES])
            sys.exit(1)
        for t in matches:
            assemble(t)
    else:
        print("Assembling Student COMPLETE PDFs for all Picture Book Companions...\n")
        for t in TITLES:
            assemble(t)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
export_docx_to_pdf.py — Communicate by Design
Automates Word → PDF export using the actual Microsoft Word engine (via docx2pdf/osascript).
This is equivalent to File → Save As → PDF in Word. NOT LibreOffice.

Usage:
    # Export a single file:
    python3 export_docx_to_pdf.py path/to/Unit_COMPLETE.docx

    # Export to a specific output path:
    python3 export_docx_to_pdf.py path/to/Unit_COMPLETE.docx path/to/output.pdf

    # Export all COMPLETE.docx files in a product folder:
    python3 export_docx_to_pdf.py --product-line nonfiction
    python3 export_docx_to_pdf.py --product-line poetry
    python3 export_docx_to_pdf.py --product-line fiction

Requirements:
    pip install docx2pdf --break-system-packages
    Microsoft Word for Mac must be installed (uses the Word engine via osascript)

Why this exists:
    LibreOffice breaks table formatting and creates blank MCQ pages in CbD nonfiction,
    fiction, and poetry unit docx files. docx2pdf calls Word's own rendering engine,
    producing identical output to manual File → Save As → PDF.
    Picture Book Companions are EXEMPT — they use ReportLab Python builds, not docx.
"""

import sys
import os
import subprocess
from pathlib import Path

# ── iCloud root path ──────────────────────────────────────────────────────────
ICLOUD_ROOT = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/Communicate by Design"

# ── Product line → COMPLETE.docx search patterns ─────────────────────────────
PRODUCT_LINE_PATTERNS = {
    "nonfiction": {
        "search_root": ICLOUD_ROOT / "Products/Nonfiction Units",
        "pattern": "**/*_COMPLETE.docx",
        "output_dir_name": None,  # same folder as docx
    },
    "poetry": {
        "search_root": ICLOUD_ROOT / "Products/Poetry Reading Units",
        "pattern": "**/*_COMPLETE.docx",
        "output_dir_name": None,
    },
    "fiction": {
        "search_root": ICLOUD_ROOT / "Products/Fiction Anchor Texts",
        "pattern": "**/*_COMPLETE.docx",
        "output_dir_name": None,
    },
}


def check_word_installed():
    """Verify Microsoft Word is available via osascript."""
    result = subprocess.run(
        ["osascript", "-e", 'tell application "Microsoft Word" to return name'],
        capture_output=True, text=True
    )
    return result.returncode == 0


def export_single(input_path: Path, output_path: Path = None) -> bool:
    """
    Export a single .docx file to PDF using Word's engine.
    Returns True on success, False on failure.
    """
    try:
        from docx2pdf import convert
    except ImportError:
        print("ERROR: docx2pdf not installed. Run: pip install docx2pdf --break-system-packages")
        return False

    input_path = Path(input_path).resolve()
    if not input_path.exists():
        print(f"ERROR: Input file not found: {input_path}")
        return False

    if not str(input_path).endswith(".docx"):
        print(f"ERROR: Input must be a .docx file: {input_path}")
        return False

    if output_path is None:
        output_path = input_path.with_suffix(".pdf")
    else:
        output_path = Path(output_path).resolve()

    print(f"Exporting: {input_path.name}")
    print(f"       to: {output_path}")
    print("  (Using Microsoft Word engine — this may briefly activate Word)")

    try:
        convert(str(input_path), str(output_path), keep_active=False)
        if output_path.exists():
            size_kb = output_path.stat().st_size / 1024
            print(f"✓ Success: {output_path.name} ({size_kb:.0f} KB)")
            return True
        else:
            print(f"✗ Failed: PDF not created at expected path")
            return False
    except Exception as e:
        print(f"✗ Error during conversion: {e}")
        return False


def export_product_line(line_key: str) -> None:
    """
    Find all COMPLETE.docx files for a product line and export each to PDF.
    """
    if line_key not in PRODUCT_LINE_PATTERNS:
        print(f"ERROR: Unknown product line '{line_key}'")
        print(f"Valid options: {', '.join(PRODUCT_LINE_PATTERNS.keys())}")
        sys.exit(1)

    config = PRODUCT_LINE_PATTERNS[line_key]
    search_root = config["search_root"]

    if not search_root.exists():
        print(f"ERROR: Product line folder not found: {search_root}")
        sys.exit(1)

    docx_files = list(search_root.glob(config["pattern"]))
    if not docx_files:
        print(f"No COMPLETE.docx files found in: {search_root}")
        sys.exit(0)

    print(f"\nFound {len(docx_files)} COMPLETE.docx file(s) in {line_key}:")
    for f in docx_files:
        print(f"  • {f.relative_to(search_root)}")

    print()
    success = 0
    failed = 0
    for docx_path in sorted(docx_files):
        ok = export_single(docx_path)
        if ok:
            success += 1
        else:
            failed += 1
        print()

    print(f"─────────────────────────────")
    print(f"Done: {success} succeeded, {failed} failed")


def main():
    args = sys.argv[1:]

    if not args:
        print(__doc__)
        sys.exit(0)

    # Product line mode
    if args[0] == "--product-line":
        if len(args) < 2:
            print("ERROR: --product-line requires a value (nonfiction, poetry, fiction)")
            sys.exit(1)
        if not check_word_installed():
            print("ERROR: Microsoft Word for Mac is required but not found.")
            print("       Install Word and try again. LibreOffice cannot be used for these exports.")
            sys.exit(1)
        export_product_line(args[1])
        return

    # Single file mode
    input_path = Path(args[0])
    output_path = Path(args[1]) if len(args) > 1 else None

    if not check_word_installed():
        print("ERROR: Microsoft Word for Mac is required but not found.")
        print("       Install Word and try again. LibreOffice cannot be used for these exports.")
        sys.exit(1)

    ok = export_single(input_path, output_path)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()

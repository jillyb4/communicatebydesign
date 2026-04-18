"""
build_wonder_tpt_package.py — Communicate by Design
=====================================================
Builds the complete TPT folder + ZIP for:
  Wonder: Character Analysis — Fiction Anchor Text Unit
  Grades 3–8  |  RL.5.3 / RL.5.6

OUTPUT FOLDER:
  Wonder_Character_Analysis_TPT/
  ├── Wonder_Character_Analysis_COMPLETE.docx          ← Full teacher unit + all 5 lessons (Word / Google-convertible)
  ├── Wonder_Character_Analysis_Answer_Key.pdf         ← Teacher answer key — NOT for student use
  ├── Wonder_Character_Analysis_Printable_Packet.pdf   ← Student-facing: symbol cards, boards, tracker, response pages
  └── (Wonder_Welcome_to_the_Product.pdf)              ← TO DO — not yet built

OUTPUT ZIP:
  Wonder_Character_Analysis_TPT.zip          ← Upload directly to TPT

USAGE:
  python3 build_wonder_tpt_package.py

PREREQUISITES:
  1. Wonder_Character_Analysis_COMPLETE.docx must be in this folder
     (It is the full unit built by build_wonder_character_analysis.js)
  2. Wonder_Character_Analysis_Printable_Packet.pdf must be in this folder
     (Built by build_wonder_printable_packet.py — run that first if missing)

NOTE — COMPLETE.pdf vs COMPLETE.docx:
  The TPT zip ships the .docx (teachers can convert to Google Docs).
  If you also want to include the PDF version of the unit, export from Word first:
    Word → File → Save As → PDF  →  Wonder_Character_Analysis_COMPLETE.pdf
  Then add it to the TPT folder manually or update this script.
"""

import io
import os
import sys
import shutil
import zipfile

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, HRFlowable
)
from reportlab.lib.colors import HexColor

# ── Brand colors ───────────────────────────────────────────────────────────────
NAVY  = HexColor("#1B1F3B")
TEAL  = HexColor("#006DA0")   # documents / WCAG AA on white
AMBER = HexColor("#FFB703")
WHITE = HexColor("#FFFFFF")
SLATE = HexColor("#94A3B8")

HERE = os.path.dirname(os.path.abspath(__file__))

DOCX_FILE    = os.path.join(HERE, "Wonder_Character_Analysis_COMPLETE.docx")
PACKET_PDF   = os.path.join(HERE, "Wonder_Character_Analysis_Printable_Packet.pdf")
ANSWER_KEY   = os.path.join(HERE, "Wonder_Character_Analysis_Answer_Key.pdf")
TPT_FOLDER   = os.path.join(HERE, "Wonder_Character_Analysis_TPT")
ZIP_OUT      = os.path.join(HERE, "Wonder_Character_Analysis_TPT.zip")
WELCOME_ROOT = os.path.join(HERE, "Wonder_Welcome_to_the_Product.pdf")

UNIT_TITLE  = "Wonder: Character Analysis"
GRADE_RANGE = "Grades 3–8"
STANDARDS   = "RL.5.3 / RL.5.6"
PREFIX      = "Wonder"


# ══════════════════════════════════════════════════════════════════════════════
# WELCOME PDF
# ══════════════════════════════════════════════════════════════════════════════

def build_welcome_pdf() -> bytes:
    """
    2-page branded Welcome to the Product PDF.
    Page 1: Welcome banner + What's Inside + What Makes This Different
    Page 2: How to Use + Accessibility Statement + About the Creator + Terms of Use
    """
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=letter,
        leftMargin=0.75*inch, rightMargin=0.75*inch,
        topMargin=0.5*inch,   bottomMargin=0.5*inch
    )

    # ── Styles ────────────────────────────────────────────────────────────────
    h2   = ParagraphStyle("h2",   fontName="Helvetica-Bold",
                fontSize=11, textColor=TEAL, leading=14, spaceBefore=10, spaceAfter=4)
    body = ParagraphStyle("body", fontName="Helvetica",
                fontSize=9,  textColor=NAVY, leading=13, spaceAfter=3)
    item = ParagraphStyle("item", fontName="Helvetica",
                fontSize=9,  textColor=NAVY, leading=13, leftIndent=12, spaceAfter=2)
    small = ParagraphStyle("small", fontName="Helvetica",
                fontSize=8, textColor=SLATE, leading=11, spaceAfter=2)

    # ── Running header ────────────────────────────────────────────────────────
    hdr_row = Table([[
        Paragraph(f"<i>{UNIT_TITLE}</i>",
                  ParagraphStyle("hl", fontName="Helvetica-Oblique",
                      fontSize=9, textColor=NAVY, leading=13)),
        Paragraph(
            "<b><font color='#006DA0'>COMMUNICATE</font> "
            "<font color='#FFB703'>BY DESIGN</font></b>",
            ParagraphStyle("br", fontName="Helvetica-Bold",
                fontSize=9, textColor=TEAL, leading=13, alignment=TA_RIGHT)),
    ]], colWidths=[4.5*inch, 2.5*inch])
    hdr_row.setStyle(TableStyle([
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",    (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
        ("LEFTPADDING",   (0,0), (-1,-1), 0),
        ("RIGHTPADDING",  (0,0), (-1,-1), 0),
    ]))

    # ── Title banner ──────────────────────────────────────────────────────────
    title_tbl = Table([[
        Paragraph(
            f"Welcome to<br/><b>{UNIT_TITLE}</b>",
            ParagraphStyle("tt", fontName="Helvetica-Bold",
                fontSize=16, textColor=WHITE, leading=22, alignment=TA_LEFT)),
        Paragraph(
            f"<b>{GRADE_RANGE}<br/>Communicate by Design</b>",
            ParagraphStyle("ttr", fontName="Helvetica-Bold",
                fontSize=10, textColor=AMBER, leading=14, alignment=TA_RIGHT)),
    ]], colWidths=[4.8*inch, 2.2*inch])
    title_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), NAVY),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",    (0,0), (-1,-1), 12),
        ("BOTTOMPADDING", (0,0), (-1,-1), 12),
        ("LEFTPADDING",   (0,0), (-1,-1), 14),
        ("RIGHTPADDING",  (0,0), (-1,-1), 12),
    ]))

    footer_text = (
        f"{UNIT_TITLE}  ·  Communicate by Design  ·  "
        "teacherspayteachers.com/store/communicate-by-design  ·  "
        "© Communicate by Design. All rights reserved."
    )
    footer_style = ParagraphStyle("ft", fontName="Helvetica", fontSize=7,
        textColor=SLATE, leading=9, alignment=TA_CENTER)

    story = [

        # ══════════════════════════════════════════════════
        # PAGE 1 — Welcome · What's Inside · What's Different
        # ══════════════════════════════════════════════════
        hdr_row,
        HRFlowable(width="100%", thickness=1.5, color=TEAL, spaceAfter=6),
        title_tbl,
        Spacer(1, 10),

        Paragraph("What's Inside", h2),
        HRFlowable(width="100%", thickness=0.75, color=AMBER, spaceAfter=5),
        Paragraph("• <b>COMPLETE.docx</b> — Full unit guide: teacher reference pages, lesson sequence, "
                  "modeling scripts, vocabulary preview routine, three reading versions (V1/V2/V3), "
                  "activities, IEP goal stems, SDI documentation tools, and pacing guide. "
                  "Convert to Google Docs for digital student access.", item),
        Paragraph("• <b>Printable Packet (PDF)</b> — Everything your students and AAC team handle: "
                  "ARASAAC symbol cards for 12 core and 12 fringe words, three communication boards "
                  "(Character Description · Emotion + Reasoning · Literary Discussion Moves), "
                  "vocabulary map, AAC Session Tracker, and five student response pages "
                  "(one per Part of the novel).", item),
        Spacer(1, 8),

        Paragraph("What Makes This Product Different", h2),
        HRFlowable(width="100%", thickness=0.75, color=AMBER, spaceAfter=5),
        Paragraph(
            "Most novel studies were built for one learner profile. "
            "This one was built for every student in the room — "
            "including the ones who cannot produce a written response independently.",
            body),
        Paragraph(
            f"• <b>The text stays the same. ({STANDARDS})</b> — "
            "This is not a simplified retelling. Students engage with <i>Wonder</i> itself. "
            "Three reading versions vary the Lexile (V1: 900–1050 · V2: 650–800 · V3: 400–550); "
            "the standard, the question, and the expectation do not. "
            "No ability labels on student materials — teachers sort, students do not know.",
            item),
        Paragraph(
            "• <b>AAC access built in from the start</b> — not a sidebar. "
            "Communication boards for character description, emotional reasoning, and "
            "literary discussion moves are included so every student can participate "
            "in the same conversation, regardless of how they communicate. "
            "ARASAAC symbol cards are color-coded by Fitzgerald Key category.",
            item),
        Paragraph(
            "• <b>IEP-aligned by design</b> — includes model ELA goal stems "
            f"for {STANDARDS} and AAC communication goal stems. "
            "SDI component labeling is built into teacher pages. "
            "The AAC Session Tracker supports IEP progress monitoring.",
            item),
        Paragraph(
            "• <b>Partner guidance embedded at point of use</b> — not supplemental. "
            "Paraeducators, families, and related service providers each have a named role. "
            "Communication partner mode guidance and 5-second wait time "
            "reminders are woven into the lesson sequence.",
            item),
        Paragraph(
            "• <b>WCAG 2.2 Level AA</b> — both the PDF and the Word document "
            "meet ADA Title II accessibility standards. "
            "The Word document converts cleanly to Google Docs for screen reader access.",
            item),

        Spacer(1, 10),
        HRFlowable(width="100%", thickness=0.5, color=TEAL, spaceAfter=3),
        Paragraph(footer_text, footer_style),

        # ══════════════════════════════════════════════════
        # PAGE 2 — How to Use · Accessibility · About · Terms
        # ══════════════════════════════════════════════════
        PageBreak(),
        hdr_row,
        HRFlowable(width="100%", thickness=1.5, color=TEAL, spaceAfter=6),

        Paragraph("How to Use This Product", h2),
        HRFlowable(width="100%", thickness=0.75, color=AMBER, spaceAfter=5),
        Paragraph(
            "<b>Step 1 — Share the Printable Packet with your student's AAC team before the unit begins.</b> "
            "Allow 1–2 weeks for fringe vocabulary to be available on student AAC systems. "
            "The fringe word list is on the symbol card page inside the Printable Packet. "
            "Core words are likely already on student systems — confirm before Lesson 1.",
            item),
        Paragraph(
            "<b>Step 2 — Run the Vocabulary Preview Routine before Lesson 1.</b> "
            "The 5-minute routine in COMPLETE.docx introduces the five highest-priority words "
            "using Say &amp; Show → Check → Connect → Flag. "
            "This is the single highest-leverage pre-teaching move for AAC-using students.",
            item),
        Paragraph(
            "<b>Step 3 — Choose the reading version for each student.</b> "
            "V1 (900–1050 Lexile), V2 (650–800), or V3 (400–550). "
            "Lexile information is never printed on student pages — "
            "only the teacher guide labels versions.",
            item),
        Paragraph(
            "<b>Step 4 — Print the Printable Packet.</b> "
            "Print and laminate the communication boards for repeated use. "
            "Print the symbol cards as a class set or individual sets. "
            "Print the student response pages — one per student per Part of the novel.",
            item),
        Paragraph(
            "<b>Step 5 — Open COMPLETE.docx for teacher reference.</b> "
            "Teacher modeling scripts, checkpoint protocols, annotation codes, "
            "and IEP goal stems are in the Word document. "
            "Convert to Google Docs if your school uses Google Classroom.",
            item),
        Paragraph(
            "<b>Step 6 — Use the AAC Session Tracker (page 8–9 of the Printable Packet).</b> "
            "Record each student's communication mode per session. "
            "This document supports IEP progress monitoring and SLP collaboration.",
            item),
        Spacer(1, 6),

        Paragraph("Accessibility Statement", h2),
        HRFlowable(width="100%", thickness=0.75, color=AMBER, spaceAfter=5),
        Paragraph(
            "This product is designed to WCAG 2.2 Level AA standards. "
            "Materials include three differentiated reading versions across Lexile ranges, "
            "ARASAAC symbol-supported vocabulary (core and fringe), "
            "AAC communication boards for literary discussion, "
            "and IEP-aligned goal stems. "
            "Every scaffold varies the access — the expectation does not change.",
            body),
        Spacer(1, 6),

        Paragraph("About the Creator", h2),
        HRFlowable(width="100%", thickness=0.75, color=AMBER, spaceAfter=5),
        Paragraph(
            "Jill McCardel is a special educator and advocate with years of experience "
            "supporting students with complex communication needs, learning differences, "
            "and IEPs. Communicate by Design creates evidence-based, accessible "
            "instructional materials for special education teams — grounded in "
            "presume-competence principles and built for real classrooms.",
            body),
        Paragraph(
            "<b>Store:</b> teacherspayteachers.com/store/communicate-by-design  "
            "&nbsp;&nbsp;<b>Substack:</b> communicatebydesign.substack.com  "
            "&nbsp;&nbsp;<b>Instagram:</b> @communicatebydesignaac",
            small),
        Spacer(1, 6),

        Paragraph("Terms of Use", h2),
        HRFlowable(width="100%", thickness=0.75, color=AMBER, spaceAfter=5),
        Paragraph(
            "This product is licensed for use by a single educator. "
            "You may print and copy materials for your students. "
            "You may not redistribute, resell, or share this product digitally "
            "with other educators outside your classroom. "
            "To share with colleagues, please direct them to purchase their own copy. "
            "ARASAAC symbols used under Creative Commons Attribution-NonCommercial-"
            "NoDerivatives 4.0 International License.",
            body),

        Spacer(1, 10),
        HRFlowable(width="100%", thickness=0.5, color=TEAL, spaceAfter=3),
        Paragraph(footer_text, footer_style),
    ]

    doc.build(story)
    return buf.getvalue()


# ══════════════════════════════════════════════════════════════════════════════
# TPT FOLDER + ZIP ASSEMBLY
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print(f"\n{'═'*60}")
    print(f"  CbD Fiction TPT Package Builder")
    print(f"  {UNIT_TITLE}  ·  {GRADE_RANGE}  ·  {STANDARDS}")
    print(f"{'═'*60}\n")

    # ── Pre-flight check ──────────────────────────────────────────────────────
    warnings = []
    if not os.path.exists(DOCX_FILE):
        warnings.append(
            f"  ⚠️  MISSING: Wonder_Character_Analysis_COMPLETE.docx\n"
            f"     → This file must exist in this folder.\n"
            f"     → It was built by build_wonder_character_analysis.js\n"
            f"     → Make sure iCloud has synced it before running this script."
        )
    if not os.path.exists(PACKET_PDF):
        warnings.append(
            f"  ⚠️  MISSING: Wonder_Character_Analysis_Printable_Packet.pdf\n"
            f"     → Run: python3 build_wonder_printable_packet.py"
        )
    if warnings:
        print("Pre-flight issues found:\n")
        for w in warnings:
            print(w + "\n")
        if not os.path.exists(DOCX_FILE):
            print("Cannot build complete TPT package without COMPLETE.docx.")
            print("Building Welcome PDF only...\n")

    # ── Create TPT folder ─────────────────────────────────────────────────────
    os.makedirs(TPT_FOLDER, exist_ok=True)
    print(f"TPT folder: {TPT_FOLDER}\n")

    copied = []
    skipped = []

    # ── 1. Welcome PDF ────────────────────────────────────────────────────────
    print("Building Welcome_to_the_Product.pdf...")
    welcome_bytes = build_welcome_pdf()

    welcome_tpt = os.path.join(TPT_FOLDER, "Wonder_Welcome_to_the_Product.pdf")
    with open(welcome_tpt, "wb") as f:
        f.write(welcome_bytes)
    with open(WELCOME_ROOT, "wb") as f:
        f.write(welcome_bytes)

    size_kb = len(welcome_bytes) / 1024
    print(f"  ✓ Wonder_Welcome_to_the_Product.pdf  ({size_kb:.0f} KB)  → TPT folder + root")
    copied.append("Wonder_Welcome_to_the_Product.pdf")

    # ── 2. COMPLETE.docx ──────────────────────────────────────────────────────
    docx_dest = os.path.join(TPT_FOLDER, "Wonder_Character_Analysis_COMPLETE.docx")
    if os.path.exists(DOCX_FILE):
        shutil.copy2(DOCX_FILE, docx_dest)
        size_kb = os.path.getsize(docx_dest) / 1024
        print(f"  ✓ Wonder_Character_Analysis_COMPLETE.docx  ({size_kb:.0f} KB)")
        copied.append("Wonder_Character_Analysis_COMPLETE.docx")
    else:
        print(f"  ⚠️  SKIPPED: Wonder_Character_Analysis_COMPLETE.docx  (not found — add manually)")
        skipped.append("Wonder_Character_Analysis_COMPLETE.docx")

    # ── 3. Printable Packet PDF ───────────────────────────────────────────────
    packet_dest = os.path.join(TPT_FOLDER, "Wonder_Character_Analysis_Printable_Packet.pdf")
    if os.path.exists(PACKET_PDF):
        shutil.copy2(PACKET_PDF, packet_dest)
        size_kb = os.path.getsize(packet_dest) / 1024
        print(f"  ✓ Wonder_Character_Analysis_Printable_Packet.pdf  ({size_kb:.0f} KB)")
        copied.append("Wonder_Character_Analysis_Printable_Packet.pdf")
    else:
        print(f"  ⚠️  SKIPPED: Wonder_Character_Analysis_Printable_Packet.pdf  (not found)")
        skipped.append("Wonder_Character_Analysis_Printable_Packet.pdf")

    # ── 4. Answer Key PDF ─────────────────────────────────────────────────────
    key_dest = os.path.join(TPT_FOLDER, "Wonder_Character_Analysis_Answer_Key.pdf")
    if os.path.exists(ANSWER_KEY):
        shutil.copy2(ANSWER_KEY, key_dest)
        size_kb = os.path.getsize(key_dest) / 1024
        print(f"  ✓ Wonder_Character_Analysis_Answer_Key.pdf  ({size_kb:.0f} KB)")
        copied.append("Wonder_Character_Analysis_Answer_Key.pdf")
    else:
        print(f"  ⚠️  SKIPPED: Wonder_Character_Analysis_Answer_Key.pdf  (run build_wonder_answer_keys.py first)")
        skipped.append("Wonder_Character_Analysis_Answer_Key.pdf")
        skipped.append("Wonder_Character_Analysis_Printable_Packet.pdf")

    # ── Zip ───────────────────────────────────────────────────────────────────
    print(f"\nCreating ZIP: {os.path.basename(ZIP_OUT)}")
    with zipfile.ZipFile(ZIP_OUT, "w", zipfile.ZIP_DEFLATED) as zf:
        for fname in os.listdir(TPT_FOLDER):
            fpath = os.path.join(TPT_FOLDER, fname)
            if os.path.isfile(fpath):
                zf.write(fpath, fname)
                print(f"  + {fname}")

    zip_kb = os.path.getsize(ZIP_OUT) / 1024

    # ── Summary ───────────────────────────────────────────────────────────────
    print(f"\n{'═'*60}")
    print(f"  COMPLETE: {len(copied)} files assembled")
    print(f"  ZIP: Wonder_Character_Analysis_TPT.zip  ({zip_kb:.0f} KB)")

    if skipped:
        print(f"\n  ⚠️  {len(skipped)} file(s) missing from ZIP — add manually:")
        for s in skipped:
            print(f"     • {s}")
        print(f"\n  When COMPLETE.docx is available:")
        print(f"     1. Ensure it's in this folder")
        print(f"     2. Re-run: python3 build_wonder_tpt_package.py")
        print(f"     3. Upload the new Wonder_Character_Analysis_TPT.zip to TPT")
    else:
        print(f"\n  ✓ All files present. Ready to upload to TPT.")

    print(f"\n  TPT Folder contents:")
    for fname in sorted(os.listdir(TPT_FOLDER)):
        fpath = os.path.join(TPT_FOLDER, fname)
        if os.path.isfile(fpath):
            kb = os.path.getsize(fpath) / 1024
            print(f"     {fname}  ({kb:.0f} KB)")

    print(f"\n  ⚠️  REMINDER before uploading to TPT:")
    print(f"     • Pricing not yet locked — decide $8.95 or $9.95 first")
    print(f"     • Cover color/design not yet built")
    print(f"     • Rubric not yet built (Layer 6 — add before listing)")
    print(f"     • Add product record to Airtable once pricing + cover are confirmed")
    print(f"{'═'*60}\n")


if __name__ == "__main__":
    main()

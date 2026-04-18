"""
build_rules_welcome.py — Communicate by Design
====================================================
Builds the Welcome to the Product PDF for:
  Rules: Identity and Belonging — Fiction Anchor Text Unit
  Unit 3 of 6  |  Grades 4–6  |  RL.4.3 · RL.4.6 · RL.5.3

OUTPUT:
  ../Product Files/Rules_Identity_and_Belonging_Welcome_to_the_Product.pdf

USAGE:
  python3 build_rules_welcome.py
"""

import io
import os
import shutil

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
TEAL  = HexColor("#006DA0")
AMBER = HexColor("#FFB703")
WHITE = HexColor("#FFFFFF")
SLATE = HexColor("#94A3B8")

HERE = os.path.dirname(os.path.abspath(__file__))

TMP_OUT     = "/tmp/Rules_Identity_and_Belonging_Welcome_to_the_Product.pdf"
WELCOME_OUT = os.path.join(HERE, "..", "Product Files",
                            "Rules_Identity_and_Belonging_Welcome_to_the_Product.pdf")

UNIT_TITLE  = "Rules: Identity and Belonging"
GRADE_RANGE = "Grades 4–6"
STANDARDS   = "RL.4.3 · RL.4.6 · RL.5.3"
UNIT_NUM    = "Fiction Anchor Text Unit 3 of 6"


def build_welcome_pdf() -> bytes:
    """
    2-page branded Welcome to the Product PDF for Rules.
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
            f"<b>{GRADE_RANGE}<br/>{UNIT_NUM}</b>",
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
        Paragraph(
            "• <b>Teaching Materials.docx</b> — Full unit teacher reference: research base, "
            "novel overview, all 5 parts with activities and partner guidance at point of use, "
            "communication access vocabulary table (23 words: 12 core, 11 fringe), "
            "before-reading activities including Jason's Communication Book Primer, "
            "Belonging Evidence Chart template with sentence frames, "
            "IEP goal stems for RL.4.3/4.6/5.3 and three AAC communication goals, "
            "rubric, and answer key. Convert to Google Docs for digital student access.", item),
        Paragraph(
            "• <b>Fiction Printable Packet (PDF, 13 pages)</b> — Communication Environment "
            "Setup guide · Core word symbol cards (12 words) · Fringe word symbol cards "
            "(12 words, chapter order) · Board A: Character Description Board — LOOKS LIKE / "
            "DOES / FEELS / WANTS for Catherine and Jason (landscape) · "
            "Board B: Emotion + Belonging · Board C: Literary Discussion Moves with "
            "[RULE] / [BELONG] / [CHANGE] annotation codes · Vocabulary Map · "
            "AAC Session Tracker · Student Response Pages for all 5 parts.", item),
        Spacer(1, 8),

        Paragraph("What Makes This Product Different", h2),
        HRFlowable(width="100%", thickness=0.75, color=AMBER, spaceAfter=5),
        Paragraph(
            "Your students are reading <i>Rules</i>. This unit gives every student — "
            "including AAC users — meaningful access to what the novel is actually about: "
            "what it means to belong, and what it costs to be honest about that.",
            body),
        Paragraph(
            f"• <b>Character analysis and point of view. ({STANDARDS})</b> — "
            "Five parts, one central arc: how Catherine's beliefs about belonging change "
            "through her friendship with Jason. Students track evidence across the novel "
            "using the Belonging Evidence Chart, then build a full character analysis by Part 5. "
            "The chart is the scaffold; by the synthesis, it becomes the outline.",
            item),
        Paragraph(
            "• <b>Jason communicates — and so does every student in this class.</b> — "
            "Jason uses word cards, a form of low-tech AAC. This unit treats him as "
            "a full communicator — not a symbol of disability, not a lesson about inclusion. "
            "He has perspective, humor, preferences, and something important to say. "
            "Students who use AAC see themselves in the text. Students who don't "
            "encounter a communication system as a feature of character, not a plot device.",
            item),
        Paragraph(
            "• <b>The Belonging Evidence Chart</b> — one chart built across all five parts, "
            "capturing what Catherine believes → what happens → how her thinking shifts. "
            "Every student uses the same chart — the access layer varies, the task does not. "
            "By Part 5, the chart is the outline for the synthesis response.",
            item),
        Paragraph(
            "• <b>AAC access designed in from the first page</b> — not added on. "
            "Every part has a clear AAC pathway: device, e-tran board, symbol cards, "
            "gaze access, or alternative pencil. Partner guidance is written at point of use. "
            "Board A (Character Description Board) has a dedicated column for both "
            "Catherine and Jason — every student is tracking both characters.",
            item),
        Paragraph(
            "• <b>IEP-aligned by design</b> — includes model goal stems for RL.4.3, RL.4.6, "
            "and RL.5.3, plus three AAC communication goals. SDI component labeling built "
            "into teacher pages. The AAC Session Tracker supports progress monitoring.",
            item),
        Paragraph(
            "• <b>WCAG 2.2 Level AA</b> — both the PDF and the Word document meet "
            "ADA Title II accessibility standards. The Word document converts cleanly "
            "to Google Docs for screen reader access.",
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
            "<b>Step 1 — Share the Printable Packet with your student's AAC team before "
            "the unit begins.</b> Allow 1–2 weeks for fringe vocabulary to be available "
            "on student AAC systems. The fringe word list (in chapter order) is on the "
            "symbol card page inside the Printable Packet. Core words are likely already "
            "on student systems — confirm before Part 1.",
            item),
        Paragraph(
            "<b>Step 2 — Read the Jason's Communication Book Primer in Teaching "
            "Materials before Part 1.</b> This two-paragraph teacher note prepares you "
            "to talk about Jason's word cards accurately — what they are, how they work, "
            "and how to treat AAC output from students in your class the same way you "
            "treat Jason's communication in the text.",
            item),
        Paragraph(
            "<b>Step 3 — Run the Vocabulary Preview Routine before Part 1.</b> "
            "The routine in Teaching Materials introduces the five highest-priority words "
            "using Say &amp; Show → Check → Connect → Flag. Pre-teaching <i>belong</i>, "
            "<i>fair</i>, <i>honest</i>, <i>hide</i>, and <i>rule</i> is the single "
            "highest-leverage move before any character analysis task with AAC users.",
            item),
        Paragraph(
            "<b>Step 4 — Set up communication access for each student.</b> "
            "Every student reads the same text. Confirm which communication boards, "
            "symbol cards, and response methods each student will use before Part 1 begins.",
            item),
        Paragraph(
            "<b>Step 5 — Print the Printable Packet.</b> Laminate the three communication "
            "boards (Board A/B/C) for repeated use. Print symbol cards as a class set or "
            "individual sets. Print one student response page per student per part.",
            item),
        Paragraph(
            "<b>Step 6 — Build the Belonging Evidence Chart across all five parts.</b> "
            "The chart is cumulative — students add to it each part. By Part 5, the "
            "completed chart is the outline for the character analysis synthesis. "
            "Partner guidance at each part tells teams exactly how to support this.",
            item),
        Paragraph(
            "<b>Step 7 — Use the AAC Session Tracker.</b> Record each student's "
            "communication mode per session. This supports IEP progress monitoring "
            "and SLP collaboration.",
            item),
        Spacer(1, 6),

        Paragraph("Accessibility Statement", h2),
        HRFlowable(width="100%", thickness=0.75, color=AMBER, spaceAfter=5),
        Paragraph(
            "This product is designed to WCAG 2.2 Level AA standards. "
            "Materials include ARASAAC symbol-supported vocabulary (core and fringe), "
            "AAC communication boards for character analysis and literary discussion, "
            "and IEP-aligned goal stems. "
            "Every student engages with the same text and the same standard — "
            "the access layer varies, the expectation does not.",
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


def main():
    print(f"\n{'═'*60}")
    print(f"  CbD Fiction Welcome PDF Builder")
    print(f"  {UNIT_TITLE}  ·  {GRADE_RANGE}  ·  {STANDARDS}")
    print(f"{'═'*60}\n")

    print("Building Welcome_to_the_Product.pdf...")
    welcome_bytes = build_welcome_pdf()

    # Write to /tmp first, then copy to iCloud destination
    with open(TMP_OUT, "wb") as f:
        f.write(welcome_bytes)

    os.makedirs(os.path.dirname(os.path.abspath(WELCOME_OUT)), exist_ok=True)
    shutil.copy2(TMP_OUT, WELCOME_OUT)

    size_kb = len(welcome_bytes) / 1024
    print(f"  ✅ Built: {os.path.basename(WELCOME_OUT)}  ({size_kb:.0f} KB)")
    print(f"     Path: {WELCOME_OUT}")
    print(f"\n  Pages: 2")
    print(f"  Page 1: Welcome banner · What's Inside · What Makes This Different")
    print(f"  Page 2: How to Use · Accessibility Statement · About · Terms of Use")
    print(f"\n  Next steps:")
    print(f"  1. Open PDF and verify layout")
    print(f"  2. Run python3 _Operations/Build/export_docx_to_pdf.py on Teaching_Materials.docx")
    print(f"  3. Assemble TPT folder (4 files):")
    print(f"     • Rules_Identity_and_Belonging_Teaching_Materials.docx")
    print(f"     • Rules_Identity_and_Belonging_Printable_Packet.pdf  (13pp)")
    print(f"     • Rules_Identity_and_Belonging_Welcome_to_the_Product.pdf  (2pp)")
    print(f"     • [Teaching_Materials.pdf — after Word export]")
    print(f"  4. Update Airtable Products record for Rules")
    print(f"{'═'*60}\n")


if __name__ == "__main__":
    main()

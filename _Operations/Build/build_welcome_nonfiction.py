#!/usr/bin/env python3
"""
build_welcome_nonfiction.py
Builds a standardized Welcome Packet PDF for all 6 CbD nonfiction units.

Structure (3 pages):
  Page 1 — What's Inside + What Makes This Different
  Page 2 — How to Use + V1/V2/V3 Quick Reference + Core vs. Fringe AAC Guide
  Page 3 — About Communicate by Design + About Jill + Accessibility Statement + Terms of Use

Run: python3 _Operations/Build/build_welcome_nonfiction.py
     python3 _Operations/Build/build_welcome_nonfiction.py --unit frances_kelsey
"""

import os
import sys
import argparse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

# ─────────────────────────────────────────────────────────────────────────────
# BRAND COLORS
# ─────────────────────────────────────────────────────────────────────────────
NAVY   = colors.HexColor("#1B1F3B")
TEAL   = colors.HexColor("#006DA0")
AMBER  = colors.HexColor("#FFB703")
WHITE  = colors.white
LIGHT  = colors.HexColor("#F0F4F8")   # very light blue-grey for table rows
FONT   = "Helvetica"
FONT_B = "Helvetica-Bold"

W, H = letter
MARGIN = 0.65 * inch
CONTENT_W = W - 2 * MARGIN

# ─────────────────────────────────────────────────────────────────────────────
# UNIT CONFIG
# ─────────────────────────────────────────────────────────────────────────────
BASE = os.path.join(os.path.dirname(__file__), "..", "..")

UNITS = {
    "frances_kelsey": {
        "title": "Frances Kelsey: The Woman Who Said No",
        "draft_path": "Products/Nonfiction Units/Frances Kelsey/Frances_Kelsey_Unit_DRAFT.md",
        "grades": "6–10",
        "skill": "Claim, Evidence, Reasoning",
        "skill_num": "#5",
        "parts": "4 Parts",
        "annotation_lens": "C (Claim) · E (Evidence) · R (Reasoning)",
        "whats_inside": [
            "Multi-version informational passages (V1, V2, V3 Lexile ranges)",
            "CER annotation guide and strategy card",
            "Evidence sort and evidence strength rating activities",
            "Word bank, sentence frames, and tools page",
            "Writing prompts, self-assessment, and rubric",
            "Evidence recording sheet",
            "Research choice board",
            "Teacher answer key — included in this Welcome Packet (see last pages)",
            "Communication Access Packet with ARASAAC vocabulary cards",
            "Symbol cards (included in Student Print Materials)",
            "AAC Communication Session Tracker (included in Student Print Materials)",
        ],
        "student_print_note": (
            "Student Print Materials is the print-and-copy file for students. "
            "Section 1: Student Handouts (annotation guide, strategy card, word bank, sentence frames, "
            "tools page, writing prompt, rubric, evidence recording sheet). "
            "Section 2–4: Passage + Activities for Version 1, Version 2, and Version 3 — each self-contained. "
            "Print only the version assigned to each student. Do not print the COMPLETE."
        ),
        "tpt_folder": "Products/Nonfiction Units/Frances Kelsey/Frances_Kelsey_TPT",
        "output_name": "Frances_Kelsey_Welcome_to_the_Product.pdf",
    },
    "radium_girls": {
        "title": "Radium Girls: When Workers Fought Back",
        "draft_path": "Products/Nonfiction Units/Radium Girls/Radium_Girls_Unit_DRAFT.md",
        "grades": "6–10",
        "skill": "Close Reading & Annotation",
        "skill_num": "#1",
        "parts": "4 Parts",
        "annotation_lens": "H (Human Cost) · Ha (Hazard) · D (Decision)",
        "whats_inside": [
            "Multi-version informational passages (V1, V2, V3 Lexile ranges)",
            "Annotation guide and annotation strategy card",
            "Multiple choice questions and short answer activities",
            "Word bank, sentence frames, and tools page",
            "Writing prompts, self-assessment, and rubric",
            "Evidence recording sheet",
            "Research choice board",
            "Teacher answer key — included in this Welcome Packet (see last pages)",
            "Communication Access Packet with ARASAAC vocabulary cards",
            "Symbol cards (included in Student Print Materials)",
            "AAC Communication Session Tracker (included in Student Print Materials)",
        ],
        "student_print_note": (
            "Student Print Materials is the print-and-copy file for students. "
            "It contains: passages (all 3 versions, in order), annotation guide, strategy card, "
            "word bank, sentence frames, tools page, writing prompt, self-assessment rubric, "
            "and evidence recording sheet. Print this file and distribute — do not print the COMPLETE."
        ),
        "tpt_folder": "Products/Nonfiction Units/Radium Girls/Radium_Girls_TPT",
        "output_name": "Radium_Girls_Welcome_to_the_Product.pdf",
    },
    "keiko": {
        "title": "Keiko: The Orca Who Came Home",
        "draft_path": "Products/Nonfiction Units/Keiko/Keiko_Unit_DRAFT.md",
        "grades": "6–10",
        "skill": "Close Reading & Annotation",
        "skill_num": "#1",
        "parts": "3 Parts",
        "annotation_lens": "F (Fact) · R (Research) · C (Connection)",
        "whats_inside": [
            "Multi-version informational passages (V1, V2, V3 Lexile ranges)",
            "Annotation guide and annotation strategy card",
            "Multiple choice questions and short answer activities",
            "Word bank, sentence frames, and tools page",
            "Writing prompts, self-assessment, and rubric",
            "Evidence recording sheet",
            "Research choice board",
            "Teacher answer key — included in this Welcome Packet (see last pages)",
            "Communication Access Packet with ARASAAC vocabulary cards",
            "Symbol cards (included in Student Print Materials)",
            "AAC Communication Session Tracker (included in Student Print Materials)",
        ],
        "student_print_note": (
            "Student Print Materials is the print-and-copy file for students. "
            "It contains: passages (all 3 versions, in order), annotation guide, strategy card, "
            "word bank, sentence frames, tools page, writing prompt, self-assessment rubric, "
            "and evidence recording sheet. Print this file and distribute — do not print the COMPLETE."
        ),
        "tpt_folder": "Products/Nonfiction Units/Keiko/Keiko_TPT",
        "output_name": "Keiko_Welcome_to_the_Product.pdf",
    },
    "zitkala_sa": {
        "title": "Zitkala-Ša: Her Words, Her Fight",
        "grades": "6–10",
        "skill": "Text Structure",
        "skill_num": "#3",
        "parts": "3 Parts",
        "annotation_lens": "S (Structure) · E (Effect) · C (Change)",
        "whats_inside": [
            "Multi-version informational passages (V1, V2, V3 Lexile ranges)",
            "Text structure mapping guide and annotation tools",
            "Multiple choice questions and short answer activities",
            "Word bank, sentence frames, and tools page",
            "Writing prompts, self-assessment, and rubric",
            "Evidence recording sheet",
            "Research choice board",
            "Teacher answer key — included in this Welcome Packet (see last pages)",
            "Communication Access Packet with ARASAAC vocabulary cards",
            "Symbol cards (included in Student Print Materials)",
            "AAC Communication Session Tracker (included in Student Print Materials)",
        ],
        "student_print_note": (
            "Student Print Materials is the print-and-copy file for students. "
            "It contains: passages (all 3 versions, in order), text structure guide, "
            "word bank, sentence frames, tools page, writing prompt, self-assessment rubric, "
            "and evidence recording sheet. Print this file and distribute — do not print the COMPLETE."
        ),
        "tpt_folder": "Products/Nonfiction Units/Zitkala-Sa/Zitkala_Sa_TPT",
        "output_name": "Zitkala_Sa_Welcome_to_the_Product.pdf",
    },
    "504_sit_in": {
        "title": "The 504 Sit-In: Disability Rights on the Line",
        "draft_path": "Products/Nonfiction Units/504 Sit In/504_Sit_In_Unit_DRAFT.md",
        "grades": "6–10",
        "skill": "Author's Purpose & Perspective",
        "skill_num": "#4",
        "parts": "4 Parts",
        "annotation_lens": "P (Purpose) · E (Evidence) · V (Viewpoint)",
        "has_cap": False,
        "whats_inside": [
            "Multi-version informational passages (V1, V2, V3 Lexile ranges)",
            "Author's purpose and perspective tracking guide",
            "Multiple choice questions and short answer activities",
            "Word bank, sentence frames, and tools page",
            "Writing prompts, self-assessment, and rubric",
            "Evidence recording sheet",
            "Research choice board",
            "Teacher answer key — included in this Welcome Packet (see last pages)",
            "Symbol cards (included in Student Print Materials)",
            "AAC Communication Session Tracker (included in Student Print Materials)",
        ],
        "student_print_note": (
            "Student Print Materials is the print-and-copy file for students. "
            "It contains: passages (all 3 versions, in order), perspective tracking guide, "
            "word bank, sentence frames, tools page, writing prompt, self-assessment rubric, "
            "and evidence recording sheet. Print this file and distribute — do not print the COMPLETE."
        ),
        "tpt_folder": "Products/Nonfiction Units/504 Sit In/504_Sit_In_TPT",
        "output_name": "504_Sit_In_Welcome_to_the_Product.pdf",
    },
    "capitol_crawl": {
        "title": "The Capitol Crawl: March 12, 1990",
        "draft_path": "Products/Nonfiction Units/Capitol Crawl/Capitol_Crawl_Lesson_DRAFT.md",
        "grades": "6–10",
        "skill": "Sourcing & Corroboration",
        "skill_num": "#6",
        "parts": "3 Parts",
        "annotation_lens": "S (Source) · C (Corroborate) · R (Reliable?)",
        "whats_inside": [
            "Multi-version informational passages (V1, V2, V3 Lexile ranges)",
            "Source tracking and corroboration framework",
            "Multiple choice questions and short answer activities",
            "Word bank, sentence frames, and tools page",
            "Writing prompts, self-assessment, and rubric",
            "Evidence recording sheet",
            "Research choice board",
            "Teacher answer key — included in this Welcome Packet (see last pages)",
            "Communication Access Packet with ARASAAC vocabulary cards",
            "Symbol cards (included in Student Print Materials)",
            "AAC Communication Session Tracker (included in Student Print Materials)",
        ],
        "student_print_note": (
            "Student Print Materials is the print-and-copy file for students. "
            "It contains: passages (all 3 versions, in order), source tracking guide, "
            "word bank, sentence frames, tools page, writing prompt, self-assessment rubric, "
            "and evidence recording sheet. Print this file and distribute — do not print the COMPLETE."
        ),
        "tpt_folder": "Products/Nonfiction Units/Capitol Crawl/Capitol_Crawl_TPT",
        "output_name": "Capitol_Crawl_Welcome_to_the_Product.pdf",
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# STYLES
# ─────────────────────────────────────────────────────────────────────────────
def make_styles():
    return {
        "unit_title": ParagraphStyle("unit_title",
            fontName=FONT_B, fontSize=18, textColor=WHITE,
            leading=22, spaceAfter=4),
        "unit_sub": ParagraphStyle("unit_sub",
            fontName=FONT, fontSize=11, textColor=AMBER,
            leading=14, spaceAfter=2),
        "header_brand": ParagraphStyle("header_brand",
            fontName=FONT_B, fontSize=10, textColor=TEAL,
            leading=12, alignment=TA_RIGHT),
        "section_head": ParagraphStyle("section_head",
            fontName=FONT_B, fontSize=12, textColor=NAVY,
            leading=15, spaceBefore=14, spaceAfter=5,
            borderPadding=(0, 0, 3, 0)),
        "body": ParagraphStyle("body",
            fontName=FONT, fontSize=9.5, textColor=NAVY,
            leading=14, spaceAfter=3),
        "body_small": ParagraphStyle("body_small",
            fontName=FONT, fontSize=8.5, textColor=NAVY,
            leading=12, spaceAfter=2),
        "bullet": ParagraphStyle("bullet",
            fontName=FONT, fontSize=9.5, textColor=NAVY,
            leading=13, spaceAfter=2,
            leftIndent=12, bulletIndent=0),
        "callout": ParagraphStyle("callout",
            fontName=FONT, fontSize=9, textColor=NAVY,
            leading=13, spaceAfter=2,
            leftIndent=8, rightIndent=8),
        "table_head": ParagraphStyle("table_head",
            fontName=FONT_B, fontSize=9, textColor=WHITE,
            leading=12, alignment=TA_CENTER),
        "table_cell": ParagraphStyle("table_cell",
            fontName=FONT, fontSize=9, textColor=NAVY,
            leading=12),
        "table_cell_b": ParagraphStyle("table_cell_b",
            fontName=FONT_B, fontSize=9, textColor=NAVY,
            leading=12),
        "footer": ParagraphStyle("footer",
            fontName=FONT, fontSize=7.5, textColor=colors.HexColor("#666666"),
            leading=10, alignment=TA_CENTER),
        "page3_head": ParagraphStyle("page3_head",
            fontName=FONT_B, fontSize=10, textColor=TEAL,
            leading=13, spaceBefore=10, spaceAfter=3),
        "page3_body": ParagraphStyle("page3_body",
            fontName=FONT, fontSize=9, textColor=NAVY,
            leading=13, spaceAfter=3),
    }


# ─────────────────────────────────────────────────────────────────────────────
# HEADER BANNER (navy background, unit title + brand)
# ─────────────────────────────────────────────────────────────────────────────
def header_banner(unit, S):
    brand_cell = Paragraph('<font color="#006DA0">COMMUNICATE</font> <font color="#FFB703">BY DESIGN</font>', S["header_brand"])
    title_cell = Paragraph(unit["title"], S["unit_title"])
    sub_cell   = Paragraph(f'Grades {unit["grades"]}  ·  Communicate by Design', S["unit_sub"])

    tbl = Table(
        [[brand_cell], [title_cell], [sub_cell]],
        colWidths=[CONTENT_W],
    )
    tbl.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (-1,-1), NAVY),
        ("TOPPADDING",  (0,0), (-1,-1), 10),
        ("BOTTOMPADDING",(0,0),(-1,-1), 6),
        ("LEFTPADDING", (0,0), (-1,-1), 14),
        ("RIGHTPADDING",(0,0), (-1,-1), 14),
        ("ALIGN",       (0,0), (-1,-1), "LEFT"),
        ("VALIGN",      (0,0), (-1,-1), "MIDDLE"),
    ]))
    return tbl


# ─────────────────────────────────────────────────────────────────────────────
# FOOTER LINE
# ─────────────────────────────────────────────────────────────────────────────
def footer_line(unit, S):
    text = (f'{unit["title"]} · Communicate by Design · '
            'teacherspayteachers.com/store/communicate-by-design · '
            '© Communicate by Design. All rights reserved.')
    return [
        HRFlowable(width=CONTENT_W, thickness=0.5, color=TEAL, spaceAfter=4),
        Paragraph(text, S["footer"]),
    ]


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 1 — What's Inside + What Makes This Different
# ─────────────────────────────────────────────────────────────────────────────
def page1(unit, S):
    story = []
    story.append(header_banner(unit, S))
    story.append(Spacer(1, 10))

    # What's Inside
    story.append(Paragraph("What's Inside", S["section_head"]))
    story.append(HRFlowable(width=CONTENT_W, thickness=1, color=TEAL, spaceAfter=6))
    for item in unit["whats_inside"]:
        story.append(Paragraph(f"◆  {item}", S["bullet"]))

    story.append(Spacer(1, 10))

    # Student Print Materials callout box
    callout_tbl = Table(
        [[Paragraph(
            f'<b>Student Print Materials</b> — {unit["student_print_note"]}',
            S["callout"]
        )]],
        colWidths=[CONTENT_W],
    )
    callout_tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,-1), colors.HexColor("#E8F4F8")),
        ("TOPPADDING",   (0,0), (-1,-1), 8),
        ("BOTTOMPADDING",(0,0), (-1,-1), 8),
        ("LEFTPADDING",  (0,0), (-1,-1), 10),
        ("RIGHTPADDING", (0,0), (-1,-1), 10),
        ("BOX",          (0,0), (-1,-1), 1, TEAL),
    ]))
    story.append(callout_tbl)
    story.append(Spacer(1, 12))

    # What Makes This Different
    story.append(Paragraph("What Makes This Product Different", S["section_head"]))
    story.append(HRFlowable(width=CONTENT_W, thickness=1, color=TEAL, spaceAfter=6))

    differentiators = [
        ("Three reading versions — one unit.",
         "V1, V2, and V3 Lexile ranges let every student access the same content, the same unit question, "
         "and the same activities. The scaffold varies. The expectation does not. "
         "No ability labels appear on student materials — teachers sort, students don't know."),
        ("AAC access built in from the start — not bolted on.",
         "Every unit includes a Communication Access Packet with ARASAAC symbol cards for core and fringe "
         "vocabulary, a Top 5 Priority Vocabulary page, and an AAC Session Tracker. Symbol cards and the "
         "session tracker are included in Student Print Materials so the whole team has what they need."),
        ("IEP-aligned by design.",
         "Includes IEP goal stems, SDI documentation tools (Checkpoint Protocol), and participation "
         "pathways for students who cannot produce written responses."),
        ("Partner guidance embedded — not just for the teacher.",
         "Paraeducators, families, and related service providers each have a clear role. Three communication "
         "partner modes are explained in the unit itself."),
        ("WCAG 2.2 Level AA.",
         "PDFs and Word documents meet ADA Title II accessibility standards. The Word document is "
         "fully Google-convertible for digital access."),
    ]
    for bold, body in differentiators:
        story.append(Paragraph(f'<b>{bold}</b>  {body}', S["body"]))
        story.append(Spacer(1, 4))

    story.extend(footer_line(unit, S))
    story.append(PageBreak())
    return story


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 2 — How to Use + V1/V2/V3 Reference + AAC Core vs. Fringe
# ─────────────────────────────────────────────────────────────────────────────
def page2(unit, S):
    story = []
    story.append(header_banner(unit, S))
    story.append(Spacer(1, 10))

    # ── How to Use ──
    story.append(Paragraph("How to Use This Product", S["section_head"]))
    story.append(HRFlowable(width=CONTENT_W, thickness=1, color=TEAL, spaceAfter=6))

    has_cap = unit.get("has_cap", True)
    cap_step = (
        "Make fringe vocabulary accessible before Lesson 1.",
        "Fringe words are unit-specific vocabulary students need before the unit begins. "
        "Anyone on the team can do this — teacher, para, family. "
        "The Communication Access Packet (Communication_Access_Packet.pdf in this folder) has the full fringe word list "
        "and symbol cards. Low-tech option: write each word on an index card with a drawing and velcro it to a response board. "
        "No device required."
    ) if has_cap else (
        "Make fringe vocabulary accessible before Lesson 1.",
        "Fringe words are unit-specific vocabulary students need before the unit begins. "
        "Anyone on the team can do this — teacher, para, family. "
        "The symbol cards in Student Print Materials include the fringe word list. "
        "Low-tech option: write each word on an index card with a drawing and velcro it to a response board. "
        "No device required."
    )

    steps = [
        cap_step,
        ("Step 2 — Run the Vocabulary Preview Routine before Lesson 1.",
         "The 5-minute routine is in the COMPLETE.docx on the Vocabulary Preview page. "
         "It introduces the 5 highest-priority words using the Say & Show → Check → Connect → Flag sequence."),
        ("Step 3 — Choose the reading version for each student.",
         "V1 (900–1050 Lexile), V2 (650–800), or V3 (400–550). See the version table below. "
         "Student pages are labeled with small letters or numbers — Lexile information is never printed on student pages."),
        ("Step 4 — Print Student Print Materials.",
         "Student_Print_Materials.docx is the only file you copy for students. "
         "It is organized in four sections: (1) Student Handouts — annotation guide, strategy card, "
         "word bank, sentence frames, tools, writing prompt, and rubric; "
         "(2) Version 1 Passage + Activities; (3) Version 2 Passage + Activities; "
         "(4) Version 3 Passage + Activities. "
         "Print Section 1 for everyone. Print only the version section that matches each student."),
        ("Step 5 — Find the Teacher Answer Key in this Welcome Packet.",
         "The Answer Key is on the last pages of this PDF (starting after the Terms of Use). "
         "All other teacher reference pages — modeling scripts, checkpoint protocols, vocabulary preview, "
         "and pacing guide — are in the COMPLETE.docx. Convert to Google Docs if needed."),
        ("Step 6 — Use the AAC Session Tracker.",
         "Found in Student Print Materials (last section). Record the communication mode each student "
         "used each session. This document supports IEP progress monitoring."),
    ]
    for bold, body in steps:
        story.append(Paragraph(f'<b>{bold}</b>  {body}', S["body"]))
        story.append(Spacer(1, 3))

    story.append(Spacer(1, 10))

    # ── V1/V2/V3 Quick Reference ──
    story.append(Paragraph("Reading Versions — Quick Reference", S["section_head"]))
    story.append(HRFlowable(width=CONTENT_W, thickness=1, color=TEAL, spaceAfter=6))

    col_w = CONTENT_W / 4
    version_data = [
        [
            Paragraph("Version", S["table_head"]),
            Paragraph("Lexile Range", S["table_head"]),
            Paragraph("Text Features", S["table_head"]),
            Paragraph("Response Format", S["table_head"]),
        ],
        [
            Paragraph("V1", S["table_cell_b"]),
            Paragraph("900–1050", S["table_cell"]),
            Paragraph("Academic prose, compound-complex sentences, vocabulary in context", S["table_cell"]),
            Paragraph("Extended analytical response with text evidence", S["table_cell"]),
        ],
        [
            Paragraph("V2", S["table_cell_b"]),
            Paragraph("650–800", S["table_cell"]),
            Paragraph("Clear academic language, parenthetical definitions, guided annotation", S["table_cell"]),
            Paragraph("Guided response with sentence starters", S["table_cell"]),
        ],
        [
            Paragraph("V3", S["table_cell_b"]),
            Paragraph("400–550", S["table_cell"]),
            Paragraph("Short sentences, in-text vocabulary boxes, pre-identified annotation prompts", S["table_cell"]),
            Paragraph("Yes/No + circle response + fringe word options", S["table_cell"]),
        ],
    ]
    version_tbl = Table(version_data, colWidths=[col_w]*4)
    version_tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), NAVY),
        ("BACKGROUND",   (0,1), (-1,1), WHITE),
        ("BACKGROUND",   (0,2), (-1,2), LIGHT),
        ("BACKGROUND",   (0,3), (-1,3), WHITE),
        ("GRID",         (0,0), (-1,-1), 0.5, colors.HexColor("#CCCCCC")),
        ("TOPPADDING",   (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0), (-1,-1), 5),
        ("LEFTPADDING",  (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("VALIGN",       (0,0), (-1,-1), "TOP"),
    ]))
    story.append(version_tbl)

    story.append(Paragraph(
        '<i>"The scaffold varies, the expectation does not." — '
        'All versions use the same unit question, same activities, same rubric.</i>',
        S["body_small"]
    ))
    story.append(Spacer(1, 10))

    # ── Core vs. Fringe AAC Quick Guide ──
    story.append(Paragraph("AAC Vocabulary — Core vs. Fringe", S["section_head"]))
    story.append(HRFlowable(width=CONTENT_W, thickness=1, color=TEAL, spaceAfter=6))

    half = CONTENT_W / 2
    aac_data = [
        [
            Paragraph("Core Words", S["table_head"]),
            Paragraph("Fringe Words", S["table_head"]),
        ],
        [
            Paragraph(
                '<b>High-frequency words present on most AAC systems.</b> '
                'Students can already access these — no pre-programming needed. '
                'Examples: <i>think, feel, know, same, different, because, stop, show, true, wrong, help.</i>',
                S["table_cell"]
            ),
            Paragraph(
                '<b>Unit-specific vocabulary students need before the unit begins.</b> '
                'These words must be made accessible before Lesson 1 — programmed on device, '
                'written on index cards, or added to a low-tech board. '
                f'See the Communication Access Packet for this unit\'s fringe word list.',
                S["table_cell"]
            ),
        ],
        [
            Paragraph(
                'Teacher, para, SLP, or family can model these words during reading and discussion. '
                'They appear on the symbol cards in Student Print Materials.',
                S["body_small"]
            ),
            Paragraph(
                'No device required — a word written on an index card with a drawing and velcro is valid AAC. '
                'Symbol cards for fringe words are in Student Print Materials.',
                S["body_small"]
            ),
        ],
    ]
    aac_tbl = Table(aac_data, colWidths=[half, half])
    aac_tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (0,0), NAVY),
        ("BACKGROUND",   (1,0), (1,0), TEAL),
        ("BACKGROUND",   (0,1), (-1,1), WHITE),
        ("BACKGROUND",   (0,2), (-1,2), LIGHT),
        ("GRID",         (0,0), (-1,-1), 0.5, colors.HexColor("#CCCCCC")),
        ("TOPPADDING",   (0,0), (-1,-1), 6),
        ("BOTTOMPADDING",(0,0), (-1,-1), 6),
        ("LEFTPADDING",  (0,0), (-1,-1), 8),
        ("RIGHTPADDING", (0,0), (-1,-1), 8),
        ("VALIGN",       (0,0), (-1,-1), "TOP"),
    ]))
    story.append(aac_tbl)

    story.append(Spacer(1, 6))
    story.extend(footer_line(unit, S))
    story.append(PageBreak())
    return story


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 3 — About CbD + About Jill + Accessibility + Terms
# ─────────────────────────────────────────────────────────────────────────────
def page3(unit, S):
    story = []
    story.append(header_banner(unit, S))
    story.append(Spacer(1, 12))

    # About Communicate by Design
    story.append(Paragraph("About Communicate by Design", S["page3_head"]))
    story.append(HRFlowable(width=CONTENT_W, thickness=0.75, color=TEAL, spaceAfter=5))
    story.append(Paragraph(
        "Communicate by Design creates evidence-based, accessible instructional materials for special education "
        "teams. Every product is built on the belief that access to language and literacy is a right — not a "
        "privilege — and that every student, especially complex communicators, deserves curriculum that was "
        "designed with them in mind from the start. Products are grounded in presume-competence principles, "
        "AAC-inclusive design, and real classroom practice.",
        S["page3_body"]
    ))
    story.append(Paragraph(
        "Store: teacherspayteachers.com/store/communicate-by-design  ·  "
        "Substack: communicatebydesign.substack.com  ·  "
        "Instagram: @communicatebydesignaac  ·  "
        "Questions: mrs.mccardel@gmail.com",
        S["page3_body"]
    ))
    story.append(Spacer(1, 8))

    # About the Creator
    story.append(Paragraph("About the Creator", S["page3_head"]))
    story.append(HRFlowable(width=CONTENT_W, thickness=0.75, color=TEAL, spaceAfter=5))
    story.append(Paragraph(
        "Jill McCardel, MAT, MPA is a special educator and advocate with years of experience supporting students "
        "with complex communication needs, learning differences, and IEPs. She created Communicate by Design "
        "to close the gap between what students need in the classroom and what curriculum has historically "
        "provided — materials that are built for every learner, not retrofitted for some of them.",
        S["page3_body"]
    ))
    story.append(Spacer(1, 8))

    # Accessibility Statement
    story.append(Paragraph("Accessibility Statement", S["page3_head"]))
    story.append(HRFlowable(width=CONTENT_W, thickness=0.75, color=TEAL, spaceAfter=5))
    story.append(Paragraph(
        "This product is designed to WCAG 2.2 Level AA standards. Materials include multi-version passages "
        "across three Lexile ranges, ARASAAC symbol-supported vocabulary, AAC participation pathways, and "
        "IEP-aligned goal stems. The Word document (.docx) is structured with accessible heading styles and "
        "is fully convertible to Google Docs. Every scaffold varies the access — the expectation does not change.",
        S["page3_body"]
    ))
    story.append(Spacer(1, 8))

    # Terms of Use
    story.append(Paragraph("Terms of Use", S["page3_head"]))
    story.append(HRFlowable(width=CONTENT_W, thickness=0.75, color=TEAL, spaceAfter=5))
    story.append(Paragraph(
        "This product is licensed for use by a single educator. You may print and copy materials for your "
        "students. You may not redistribute, resell, or share this product digitally with other educators "
        "outside your classroom. To share with colleagues, please direct them to purchase their own copy at "
        "teacherspayteachers.com/store/communicate-by-design.",
        S["page3_body"]
    ))
    story.append(Paragraph(
        "ARASAAC symbols used under Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 "
        "International License. Communicate by Design is not affiliated with ARASAAC or the Aragonese "
        "Government. Symbol copyright belongs to the Government of Aragon and ARASAAC contributors.",
        S["page3_body"]
    ))
    story.append(Spacer(1, 8))

    story.extend(footer_line(unit, S))
    return story


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 4+ — Teacher Answer Key (extracted from DRAFT.md)
# ─────────────────────────────────────────────────────────────────────────────
def page4_answer_key(unit, S):
    """Render Teacher Answer Key from the unit's DRAFT.md into the welcome PDF."""
    draft_rel = unit.get("draft_path")
    if not draft_rel:
        return []
    draft_full = os.path.join(BASE, draft_rel)
    if not os.path.exists(draft_full):
        return []

    with open(draft_full, encoding="utf-8") as f:
        md = f.read()

    # Extract the AK section — look for Teacher Answer Key header to end of file
    # (before **COMMUNICATE** marker)
    ak_markers = [
        "## Teacher Answer Key",
        "# Teacher Answer Key",
        "## TEACHER ANSWER KEY",
        "# TEACHER ANSWER KEY",
    ]
    ak_start = -1
    for marker in ak_markers:
        idx = md.find(marker)
        if idx != -1:
            ak_start = idx
            break

    if ak_start == -1:
        return []  # No AK found in this draft

    end_marker = "**COMMUNICATE** by Design"
    ak_end = md.find(end_marker, ak_start)
    ak_text = md[ak_start: ak_end if ak_end != -1 else len(md)].strip()

    story = []
    story.append(PageBreak())
    story.append(header_banner(unit, S))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Teacher Answer Key", S["section_head"]))
    story.append(Paragraph(
        "Teacher-Facing Only — Do Not Distribute to Students",
        ParagraphStyle("ak_warning", fontName=FONT_B, fontSize=9,
                       textColor=colors.HexColor("#CC0000"), leading=12, spaceAfter=6)
    ))
    story.append(HRFlowable(width=CONTENT_W, thickness=1, color=TEAL, spaceAfter=8))

    # Render lines: ### = part heading, ## = section heading, table rows, plain text
    ak_label = ParagraphStyle("ak_label", fontName=FONT_B, fontSize=10,
                               textColor=NAVY, leading=14, spaceBefore=10, spaceAfter=3)
    ak_sub   = ParagraphStyle("ak_sub", fontName=FONT_B, fontSize=9,
                               textColor=TEAL, leading=12, spaceBefore=6, spaceAfter=2)
    ak_body  = ParagraphStyle("ak_body", fontName=FONT, fontSize=8.5,
                               textColor=NAVY, leading=12, spaceAfter=2)
    ak_red   = ParagraphStyle("ak_red", fontName=FONT_B, fontSize=8.5,
                               textColor=colors.HexColor("#CC0000"), leading=12, spaceAfter=2)

    in_table = False
    table_rows = []
    table_cols = 0

    def flush_table():
        nonlocal in_table, table_rows, table_cols
        if not table_rows:
            in_table = False
            return []
        items = []
        # Build col widths evenly
        cols = max(len(r) for r in table_rows)
        col_w = CONTENT_W / cols
        data = []
        for ri, row in enumerate(table_rows):
            # pad short rows
            while len(row) < cols:
                row.append("")
            style = ak_body if ri > 0 else ParagraphStyle(
                "ak_th", fontName=FONT_B, fontSize=8.5, textColor=WHITE, leading=11)
            data.append([Paragraph(cell.strip(), style) for cell in row])
        tbl = Table(data, colWidths=[col_w] * cols)
        tbl_style = [
            ("BACKGROUND",    (0,0), (-1,0), NAVY),
            ("GRID",          (0,0), (-1,-1), 0.4, colors.HexColor("#CCCCCC")),
            ("TOPPADDING",    (0,0), (-1,-1), 4),
            ("BOTTOMPADDING", (0,0), (-1,-1), 4),
            ("LEFTPADDING",   (0,0), (-1,-1), 5),
            ("RIGHTPADDING",  (0,0), (-1,-1), 5),
            ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ]
        for ri in range(1, len(data)):
            bg = WHITE if ri % 2 == 1 else colors.HexColor("#F0F4F8")
            tbl_style.append(("BACKGROUND", (0,ri), (-1,ri), bg))
        tbl.setStyle(TableStyle(tbl_style))
        items.append(tbl)
        items.append(Spacer(1, 4))
        table_rows = []
        table_cols = 0
        in_table = False
        return items

    for line in ak_text.split("\n"):
        stripped = line.strip()
        if not stripped:
            if in_table:
                story.extend(flush_table())
            continue

        # Table row detection
        if stripped.startswith("|") and stripped.endswith("|"):
            if stripped.replace("|", "").replace("-", "").strip() == "":
                # separator row — skip
                continue
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if not in_table:
                in_table = True
                table_rows = []
            table_rows.append(cells)
            continue
        else:
            if in_table:
                story.extend(flush_table())

        # Headings
        if stripped.startswith("### "):
            text = stripped[4:].replace("**", "")
            story.append(Paragraph(text, ak_label))
        elif stripped.startswith("## ") or stripped.startswith("# "):
            text = stripped.lstrip("#").strip().replace("**", "")
            if "Teacher Answer Key" in text or "Teacher-Facing" in text:
                continue  # already rendered as section header
            story.append(Paragraph(text, ak_sub))
        elif stripped.startswith("- ") or stripped.startswith("• "):
            text = stripped[2:].replace("**", "").replace("→", "→")
            story.append(Paragraph(f"◆  {text}", ak_body))
        elif stripped.startswith("Sample strong response:"):
            text = stripped.replace("**", "")
            story.append(Paragraph(f'<i>{text}</i>', ak_body))
        elif stripped.startswith("Note:"):
            story.append(Paragraph(stripped, ak_body))
        else:
            text = stripped.replace("**", "")
            story.append(Paragraph(text, ak_body))

    if in_table:
        story.extend(flush_table())

    story.extend(footer_line(unit, S))
    return story


# ─────────────────────────────────────────────────────────────────────────────
# BUILD ONE UNIT
# ─────────────────────────────────────────────────────────────────────────────
def build_unit(key, unit):
    out_dir = os.path.join(BASE, unit["tpt_folder"])
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, unit["output_name"])

    doc = SimpleDocTemplate(
        out_path,
        pagesize=letter,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN,
        title=f'Welcome — {unit["title"]}',
        author="Communicate by Design",
        subject="Welcome Packet",
    )

    S = make_styles()
    story = []
    story.extend(page1(unit, S))
    story.extend(page2(unit, S))
    story.extend(page3(unit, S))
    story.extend(page4_answer_key(unit, S))

    doc.build(story)
    print(f"  ✓  {key:20s}  →  {out_path.split('Communicate by Design/')[-1]}")
    return out_path


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Build Welcome Packets for CbD nonfiction units")
    parser.add_argument("--unit", help="Single unit key (e.g. frances_kelsey). Omit to build all.")
    args = parser.parse_args()

    print("\nCommunicate by Design — Welcome Packet Builder")
    print("=" * 55)

    if args.unit:
        if args.unit not in UNITS:
            print(f"Unknown unit: {args.unit}")
            print(f"Valid keys: {', '.join(UNITS.keys())}")
            sys.exit(1)
        build_unit(args.unit, UNITS[args.unit])
    else:
        for key, unit in UNITS.items():
            build_unit(key, unit)

    print("\nDone.\n")


if __name__ == "__main__":
    main()

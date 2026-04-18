#!/usr/bin/env python3
"""
build_welcome_poetry_unit1.py
Builds the Welcome to the Product PDF for Poetry Reading Unit 1:
What the Voice Carries — Figurative Language in Poetry

Structure:
  Page 1 — What's Inside + What Makes This Different
  Page 2 — How to Use + NFMA Framework Reference + AAC Core vs. Fringe Guide
  Page 3 — About Communicate by Design + About Jill + Accessibility + Terms of Use

Output: WhatTheVoiceCarries_Welcome_to_the_Product.pdf
"""

import os
from pathlib import Path
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
# BRAND COLORS — Poetry line uses Deep Violet (docs) + Bright Violet (accents)
# ─────────────────────────────────────────────────────────────────────────────
NAVY    = colors.HexColor("#1B1F3B")
VIOLET  = colors.HexColor("#6B21A8")    # Deep Violet — WCAG AAA on white ~12:1
AMBER   = colors.HexColor("#FFB703")
WHITE   = colors.white
LIGHT   = colors.HexColor("#F3EEF8")    # very light violet-tint for table rows
FONT    = "Helvetica"
FONT_B  = "Helvetica-Bold"

W, H = letter
MARGIN = 0.65 * inch
CONTENT_W = W - 2 * MARGIN

# ─────────────────────────────────────────────────────────────────────────────
# UNIT CONFIG
# ─────────────────────────────────────────────────────────────────────────────
UNIT = {
    "title": "What the Voice Carries — Figurative Language in Poetry",
    "product_line": "Poetry Reading Units",
    "grades": "6–10",
    "standards": "RL.6.4, RL.7.4, L.5.5a–c",
    "price": "$9.95",
    "poems": [
        '"We Wear the Mask" — Paul Laurence Dunbar',
        '"I\'m Nobody! Who are you?" — Emily Dickinson',
        '"The Man with the Hoe" — Edwin Markham',
        '"The Words I Carry" — original Communicate by Design poem',
    ],
    "whats_inside": [
        "Unit COMPLETE — teacher document with 16 sections: NFMA framework overview, all 4 poem texts, "
        "differentiated NFMA activities across V1/V2/V3 for each poem, partner guidance at point of use, "
        "IEP goal stems, and a 4-criterion rubric",
        "Student Packet (13 pages) — NFMA response pages for all 4 poems, all three access levels, "
        "sentence frames, and an AAC Communication Session Tracker",
        "Communication Access Packet (12 pages) — vocabulary handoff for the SLP and team, "
        "Fitzgerald Key organization, ARASAAC symbol references, 2-week pre-programming timeline, "
        "and Top 5 Priority Vocabulary page",
        "This Welcome to the Product PDF — at-a-glance guide for the IEP team",
    ],
    "output_path": "/sessions/dreamy-pensive-allen/WhatTheVoiceCarries_Welcome_to_the_Product.pdf",
    "final_path": (
        "/sessions/dreamy-pensive-allen/mnt/Communicate by Design"
        "/Products/Poetry Reading Units/Unit 1 - What the Voice Carries"
        "/WhatTheVoiceCarries_Welcome_to_the_Product.pdf"
    ),
}


# ─────────────────────────────────────────────────────────────────────────────
# STYLES
# ─────────────────────────────────────────────────────────────────────────────
def make_styles():
    return {
        "unit_title": ParagraphStyle("unit_title",
            fontName=FONT_B, fontSize=16, textColor=WHITE,
            leading=20, spaceAfter=4),
        "unit_sub": ParagraphStyle("unit_sub",
            fontName=FONT, fontSize=10, textColor=AMBER,
            leading=13, spaceAfter=2),
        "header_brand": ParagraphStyle("header_brand",
            fontName=FONT_B, fontSize=10, textColor=WHITE,
            leading=12, alignment=TA_RIGHT),
        "section_head": ParagraphStyle("section_head",
            fontName=FONT_B, fontSize=12, textColor=VIOLET,
            leading=15, spaceBefore=14, spaceAfter=5),
        "body": ParagraphStyle("body",
            fontName=FONT, fontSize=9.5, textColor=NAVY,
            leading=14, spaceAfter=3),
        "body_small": ParagraphStyle("body_small",
            fontName=FONT, fontSize=8.5, textColor=NAVY,
            leading=12, spaceAfter=2),
        "bullet": ParagraphStyle("bullet",
            fontName=FONT, fontSize=9.5, textColor=NAVY,
            leading=13, spaceAfter=3,
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
            fontName=FONT_B, fontSize=10, textColor=VIOLET,
            leading=13, spaceBefore=10, spaceAfter=3),
        "page3_body": ParagraphStyle("page3_body",
            fontName=FONT, fontSize=9, textColor=NAVY,
            leading=13, spaceAfter=3),
        "nfma_letter": ParagraphStyle("nfma_letter",
            fontName=FONT_B, fontSize=22, textColor=WHITE,
            leading=26, alignment=TA_CENTER),
        "nfma_label": ParagraphStyle("nfma_label",
            fontName=FONT_B, fontSize=10, textColor=AMBER,
            leading=13, alignment=TA_CENTER),
        "nfma_desc": ParagraphStyle("nfma_desc",
            fontName=FONT, fontSize=8.5, textColor=WHITE,
            leading=12, alignment=TA_CENTER),
    }


# ─────────────────────────────────────────────────────────────────────────────
# HEADER BANNER (navy background)
# ─────────────────────────────────────────────────────────────────────────────
def header_banner(S):
    brand_cell = Paragraph(
        '<font color="#C084FC">COMMUNICATE</font> <font color="#FFB703">BY DESIGN</font>',
        S["header_brand"]
    )
    title_cell = Paragraph(UNIT["title"], S["unit_title"])
    sub_cell   = Paragraph(
        f'Poetry Reading Unit  ·  Grades {UNIT["grades"]}  ·  Communicate by Design',
        S["unit_sub"]
    )
    tbl = Table(
        [[brand_cell], [title_cell], [sub_cell]],
        colWidths=[CONTENT_W],
    )
    tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,-1), NAVY),
        ("TOPPADDING",   (0,0), (-1,-1), 10),
        ("BOTTOMPADDING",(0,0), (-1,-1), 6),
        ("LEFTPADDING",  (0,0), (-1,-1), 14),
        ("RIGHTPADDING", (0,0), (-1,-1), 14),
        ("ALIGN",        (0,0), (-1,-1), "LEFT"),
        ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
    ]))
    return tbl


def footer_line(S):
    text = (
        f'{UNIT["title"]} · Communicate by Design · '
        'teacherspayteachers.com/store/communicate-by-design · '
        '© Communicate by Design. All rights reserved.'
    )
    return [
        HRFlowable(width=CONTENT_W, thickness=0.5, color=VIOLET, spaceAfter=4),
        Paragraph(text, S["footer"]),
    ]


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 1 — What's Inside + What Makes This Different
# ─────────────────────────────────────────────────────────────────────────────
def page1(S):
    story = []
    story.append(header_banner(S))
    story.append(Spacer(1, 10))

    # The 4 Anchor Poems
    story.append(Paragraph("The 4 Anchor Poems", S["section_head"]))
    story.append(HRFlowable(width=CONTENT_W, thickness=1, color=VIOLET, spaceAfter=6))
    for poem in UNIT["poems"]:
        story.append(Paragraph(f"◆  {poem}", S["bullet"]))
    story.append(Spacer(1, 6))

    # What's Inside
    story.append(Paragraph("What's Inside This Product", S["section_head"]))
    story.append(HRFlowable(width=CONTENT_W, thickness=1, color=VIOLET, spaceAfter=6))
    for item in UNIT["whats_inside"]:
        story.append(Paragraph(f"◆  {item}", S["bullet"]))

    story.append(Spacer(1, 10))

    # What Makes This Different
    story.append(Paragraph("What Makes This Product Different", S["section_head"]))
    story.append(HRFlowable(width=CONTENT_W, thickness=1, color=VIOLET, spaceAfter=6))

    differentiators = [
        ("Real poetry for every student.",
         "All 4 poems are taught at the full grade-level text — the same poem, the same figurative language, "
         "the same essential question across V1, V2, and V3. The scaffold changes. The poem doesn't. "
         "No ability labels appear on student materials."),
        ("NFMA: a poetry framework built for access.",
         "The NFMA framework (Notice · Feel · Mean · Ask) gives every student a repeatable strategy "
         "for approaching figurative language — and gives AAC users a clear pathway through each step. "
         "V1, V2, and V3 scaffolds are built into every NFMA activity."),
        ("AAC access designed in from line one.",
         "Every NFMA step has an explicit AAC pathway — SGD, e-tran board, symbol cards, gaze access, or "
         "alternative pencil. Partner guidance is written at point of use. The Communication Access Packet "
         "gives your SLP and team what they need 2 weeks before Day 1."),
        ('"The Words I Carry" — an original poem from Communicate by Design.',
         'The fourth poem is written from the perspective of an AAC user. "The Words I Carry" treats '
         "AAC communication as a metaphor — the speaker's voice is different, not lesser. This is ELA "
         "that reflects the students who are actually in the classroom."),
        ("IEP-aligned by design.",
         "Includes IEP goal stems for the academic ELA skill (RL.6.4 / RL.7.4 / L.5.5a–c) and a separate "
         "AAC communication goal stem. SDI components are labeled in the teacher document."),
    ]
    for bold, body in differentiators:
        story.append(Paragraph(f'<b>{bold}</b>  {body}', S["body"]))
        story.append(Spacer(1, 4))

    story.extend(footer_line(S))
    story.append(PageBreak())
    return story


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 2 — How to Use + NFMA Framework + AAC Core vs. Fringe
# ─────────────────────────────────────────────────────────────────────────────
def page2(S):
    story = []
    story.append(header_banner(S))
    story.append(Spacer(1, 10))

    # How to Use
    story.append(Paragraph("How to Use This Product", S["section_head"]))
    story.append(HRFlowable(width=CONTENT_W, thickness=1, color=VIOLET, spaceAfter=6))

    steps = [
        ("Step 1 — Share the Communication Access Packet with your team.",
         "The Communication Access Packet (CAP) is the team coordination document. Send it to the SLP, "
         "para, and any support staff at least 2 weeks before Day 1. It includes the vocabulary list, "
         "Fitzgerald Key organization, ARASAAC symbol references, and a 2-week programming timeline. "
         "No device required — any vocabulary method counts."),
        ("Step 2 — Choose the reading version for each student.",
         "V1 (grade-level text), V2 (guided access with sentence starters), or V3 (vocabulary support "
         "built in, same NFMA steps). The Student Packet organizes all three versions. "
         "Version labels are teacher-facing only — they do not appear on student pages."),
        ("Step 3 — Teach the NFMA framework before Poem 1.",
         "The NFMA overview is on the first pages of the COMPLETE.docx. Walk students through the four "
         "steps using a familiar short text before starting the anchor poems. "
         "The NFMA acronym is on the Student Packet cover for reference."),
        ("Step 4 — Print the Student Packet.",
         "The Student Packet is the copy-and-distribute file. It contains NFMA response pages for all "
         "4 poems across V1/V2/V3, sentence frames, and the AAC Communication Session Tracker. "
         "Print Section 1 (overview) for everyone. Print only the version section that matches each student."),
        ("Step 5 — Use the AAC Communication Session Tracker.",
         "In the Student Packet (last pages). Record the communication mode used each session. "
         "This document supports IEP progress monitoring and can be shared with the team."),
    ]
    for bold, body in steps:
        story.append(Paragraph(f'<b>{bold}</b>  {body}', S["body"]))
        story.append(Spacer(1, 3))

    story.append(Spacer(1, 10))

    # NFMA Framework Reference
    story.append(Paragraph("The NFMA Framework — Quick Reference", S["section_head"]))
    story.append(HRFlowable(width=CONTENT_W, thickness=1, color=VIOLET, spaceAfter=6))

    col_w = CONTENT_W / 4
    nfma_data = [
        [
            Paragraph("N", S["nfma_letter"]),
            Paragraph("F", S["nfma_letter"]),
            Paragraph("M", S["nfma_letter"]),
            Paragraph("A", S["nfma_letter"]),
        ],
        [
            Paragraph("NOTICE", S["nfma_label"]),
            Paragraph("FEEL", S["nfma_label"]),
            Paragraph("MEAN", S["nfma_label"]),
            Paragraph("ASK", S["nfma_label"]),
        ],
        [
            Paragraph("Find the figurative language. Name the device.", S["nfma_desc"]),
            Paragraph("What effect does it create? What does the reader feel?", S["nfma_desc"]),
            Paragraph("What does the figurative language reveal about meaning?", S["nfma_desc"]),
            Paragraph("What question does it raise? What would you ask the poet?", S["nfma_desc"]),
        ],
    ]
    nfma_tbl = Table(nfma_data, colWidths=[col_w]*4, rowHeights=[32, 18, None])
    nfma_tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,-1), VIOLET),
        ("TOPPADDING",   (0,0), (-1,0), 6),
        ("BOTTOMPADDING",(0,0), (-1,0), 2),
        ("TOPPADDING",   (0,1), (-1,1), 2),
        ("BOTTOMPADDING",(0,1), (-1,1), 2),
        ("TOPPADDING",   (0,2), (-1,2), 4),
        ("BOTTOMPADDING",(0,2), (-1,2), 8),
        ("LEFTPADDING",  (0,0), (-1,-1), 4),
        ("RIGHTPADDING", (0,0), (-1,-1), 4),
        ("ALIGN",        (0,0), (-1,-1), "CENTER"),
        ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
        ("LINEAFTER",    (0,0), (2,2), 0.5, colors.HexColor("#9333EA")),
    ]))
    story.append(nfma_tbl)
    story.append(Paragraph(
        '<i>The NFMA framework applies to all 4 anchor poems. Every step has V1, V2, and V3 scaffolds. '
        'The standard stays the same across all three versions. The access changes.</i>',
        S["body_small"]
    ))
    story.append(Spacer(1, 10))

    # AAC Core vs. Fringe
    story.append(Paragraph("AAC Vocabulary — Core vs. Fringe", S["section_head"]))
    story.append(HRFlowable(width=CONTENT_W, thickness=1, color=VIOLET, spaceAfter=6))

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
                'Examples: <i>think, feel, know, same, different, because, show, true, wrong, ask.</i>',
                S["table_cell"]
            ),
            Paragraph(
                '<b>Unit-specific vocabulary students need before the unit begins.</b> '
                'These words must be made accessible before Lesson 1 — programmed on device, '
                'written on index cards, or added to a low-tech board. '
                'See the Communication Access Packet for the full fringe word list.',
                S["table_cell"]
            ),
        ],
        [
            Paragraph(
                'Teacher, para, or any team member can model these words during reading and discussion.',
                S["body_small"]
            ),
            Paragraph(
                'No device required. A word written on an index card with a drawing and velcro is valid AAC.',
                S["body_small"]
            ),
        ],
    ]
    aac_tbl = Table(aac_data, colWidths=[half, half])
    aac_tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (0,0), NAVY),
        ("BACKGROUND",   (1,0), (1,0), VIOLET),
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
    story.extend(footer_line(S))
    story.append(PageBreak())
    return story


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 3 — About CbD + About Jill + Accessibility + Terms
# ─────────────────────────────────────────────────────────────────────────────
def page3(S):
    story = []
    story.append(header_banner(S))
    story.append(Spacer(1, 12))

    story.append(Paragraph("About Communicate by Design", S["page3_head"]))
    story.append(HRFlowable(width=CONTENT_W, thickness=0.75, color=VIOLET, spaceAfter=5))
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

    story.append(Paragraph("About the Creator", S["page3_head"]))
    story.append(HRFlowable(width=CONTENT_W, thickness=0.75, color=VIOLET, spaceAfter=5))
    story.append(Paragraph(
        "Jill McCardel, MAT, MPA is a special educator and advocate with years of experience supporting students "
        "with complex communication needs, learning differences, and IEPs. She created Communicate by Design "
        "to close the gap between what students need in the classroom and what curriculum has historically "
        "provided — materials that are built for every learner, not retrofitted for some of them.",
        S["page3_body"]
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("About 'The Words I Carry'", S["page3_head"]))
    story.append(HRFlowable(width=CONTENT_W, thickness=0.75, color=VIOLET, spaceAfter=5))
    story.append(Paragraph(
        '"The Words I Carry" is an original poem written by Communicate by Design. '
        'It is the only poem in this unit written from the perspective of an AAC user — a speaker whose voice '
        "is real, carries meaning, and moves in ways that don't always look like speech. "
        "It was written to ensure that students who communicate differently see themselves in the curriculum. "
        "All rights reserved. This poem may not be reproduced outside of Communicate by Design products.",
        S["page3_body"]
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Accessibility Statement", S["page3_head"]))
    story.append(HRFlowable(width=CONTENT_W, thickness=0.75, color=VIOLET, spaceAfter=5))
    story.append(Paragraph(
        "This product is designed to WCAG 2.2 Level AA standards. Materials include three-version NFMA "
        "scaffolds, ARASAAC symbol-supported vocabulary in the Communication Access Packet, AAC participation "
        "pathways at every NFMA step, and IEP-aligned goal stems. The Word document (.docx) is structured with "
        "accessible heading styles and is fully convertible to Google Docs. "
        "Every scaffold varies the access — the expectation does not change.",
        S["page3_body"]
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Terms of Use", S["page3_head"]))
    story.append(HRFlowable(width=CONTENT_W, thickness=0.75, color=VIOLET, spaceAfter=5))
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

    story.extend(footer_line(S))
    return story


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
def build():
    output_path = UNIT["output_path"]
    print(f"Building: {output_path}")

    S = make_styles()
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=MARGIN,
        title="What the Voice Carries — Welcome to the Product",
        author="Communicate by Design",
        subject="Poetry Reading Unit 1 · Grades 6–10 · Communicate by Design",
        creator="Communicate by Design",
    )

    story = []
    story.extend(page1(S))
    story.extend(page2(S))
    story.extend(page3(S))

    doc.build(story)

    import shutil
    p = Path(output_path)
    if p.exists():
        size_kb = p.stat().st_size / 1024
        print(f"✓ Built: {p.name} ({size_kb:.0f} KB)")
        # Copy to final iCloud-mounted path
        final = UNIT["final_path"]
        shutil.copy2(str(p), final)
        print(f"✓ Copied to: {final}")
        return True
    else:
        print("✗ Output file not found after build")
        return False


if __name__ == "__main__":
    build()

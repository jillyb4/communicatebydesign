"""
Session Tracker — What the Voice Carries
Poetry Reading Units · Unit 1 · Communicate by Design

Purpose: Para-administered quick-score data collection. One scoring page per poem.
Rubric: 3-level (DNM / Approaching / Meets) · 4 criteria · RL.6.4 Figurative Language

Structure:
  p1    Cover + Para Instructions
  p2    Poem 1 — "We Wear the Mask" (3 sessions × 4 criteria)
  p3    Poem 2 — "I'm Nobody! Who are you?"
  p4    Poem 3 — "The Man with the Hoe"
  p5    Poem 4 — "The Words I Carry" (CbD Original)
  p6    Cross-Poem Progress Summary

Colors: VIOLET #6B21A8, NAVY #1B1F3B, AMBER #FFB703, TEAL #006DA0
"""

import os, io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas as rl_canvas

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(BASE, "What_the_Voice_Carries_Session_Tracker.pdf")

UNIT  = "What the Voice Carries — Figurative Language in Poetry"
STORE = "teacherspayteachers.com/store/communicate-by-design"

# ── Colors ────────────────────────────────────────────────────────────────────
VIOLET = colors.HexColor("#6B21A8")
LVIOLET= colors.HexColor("#EDE9FE")
NAVY   = colors.HexColor("#1B1F3B")
TEAL   = colors.HexColor("#006DA0")
AMBER  = colors.HexColor("#FFB703")
SLATE  = colors.HexColor("#94A3B8")
WHITE  = colors.white
LGRAY  = colors.HexColor("#F5F5F5")
MGRAY  = colors.HexColor("#DDDDDD")
YELLOW_BG = colors.HexColor("#FFF9C4")

W, H = letter

POEMS = [
    ("We Wear the Mask",         "Paul Laurence Dunbar · 1896",    "Extended metaphor — the mask hides true feelings"),
    ("I'm Nobody! Who are you?", "Emily Dickinson · c. 1891",       "Metaphor — Nobody/Somebody as identity categories"),
    ("The Man with the Hoe",     "Edwin Markham · 1913",            "Imagery — physical labor as social commentary"),
    ("The Words I Carry",        "Communicate by Design · 2026",    "Metaphor — voice as river; words as stones"),
]

CRITERIA = [
    ("C1 · NOTICE",  "Identifies a line containing figurative language"),
    ("C2 · NOTICE",  "Names the type of figurative language (metaphor / imagery / other)"),
    ("C3 · MEAN",    "Interprets what the figurative language means beyond the literal"),
    ("C4 · FEEL+MEAN","Explains effect on tone or mood with at least one poem connection"),
]

# ── Styles ────────────────────────────────────────────────────────────────────
H1    = ParagraphStyle("H1",   fontName="Helvetica-Bold",  fontSize=13, textColor=VIOLET, leading=17, spaceAfter=6)
H2    = ParagraphStyle("H2",   fontName="Helvetica-Bold",  fontSize=10, textColor=NAVY,   leading=13, spaceAfter=4)
BODY  = ParagraphStyle("BD",   fontName="Helvetica",       fontSize=8.5,textColor=NAVY,   leading=12, spaceAfter=3)
BOLD  = ParagraphStyle("BL",   fontName="Helvetica-Bold",  fontSize=8.5,textColor=NAVY,   leading=12, spaceAfter=3)
SML   = ParagraphStyle("SM",   fontName="Helvetica",       fontSize=7.5,textColor=SLATE,  leading=10, spaceAfter=2)
CTR   = ParagraphStyle("CT",   fontName="Helvetica",       fontSize=8.5,textColor=NAVY,   leading=12, spaceAfter=3, alignment=TA_CENTER)
CTRBLD= ParagraphStyle("CB",   fontName="Helvetica-Bold",  fontSize=8.5,textColor=WHITE,  leading=12, spaceAfter=3, alignment=TA_CENTER)
FOOT  = ParagraphStyle("FT",   fontName="Helvetica",       fontSize=7,  textColor=SLATE,  leading=9,  alignment=TA_CENTER)

def hdr():
    hl = ParagraphStyle("hl", fontName="Helvetica-Oblique", fontSize=8.5, textColor=NAVY, leading=12)
    hr = ParagraphStyle("hr", fontName="Helvetica-Bold",    fontSize=8.5, textColor=TEAL, leading=12, alignment=TA_RIGHT)
    t = Table([[
        Paragraph(f"<i>{UNIT}</i>", hl),
        Paragraph("<b><font color='#006DA0'>COMMUNICATE</font> <font color='#FFB703'>BY DESIGN</font></b>", hr),
    ]], colWidths=[4.5*inch, 2.5*inch])
    t.setStyle(TableStyle([
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("TOPPADDING",(0,0),(-1,-1),0),
        ("BOTTOMPADDING",(0,0),(-1,-1),3),
        ("LEFTPADDING",(0,0),(-1,-1),0),
        ("RIGHTPADDING",(0,0),(-1,-1),0),
    ]))
    return t

def foot():
    return Paragraph(
        f"{UNIT}  ·  Session Tracker  ·  Communicate by Design  ·  {STORE}", FOOT)

def sec_bar(title):
    t = Table([[Paragraph(f"<b>{title}</b>", CTRBLD)]], colWidths=[7*inch])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),VIOLET),
        ("TOPPADDING",(0,0),(-1,-1),5),
        ("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),8),
        ("RIGHTPADDING",(0,0),(-1,-1),8),
    ]))
    return t

def callout(text, bg=None):
    bg = bg or LVIOLET
    t = Table([[Paragraph(text, BODY)]], colWidths=[6.8*inch])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),bg),
        ("BOX",(0,0),(-1,-1),1,VIOLET),
        ("TOPPADDING",(0,0),(-1,-1),5),
        ("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),8),
        ("RIGHTPADDING",(0,0),(-1,-1),8),
    ]))
    return t

# ── Page 1: Cover / Para Instructions ────────────────────────────────────────
def build_cover(c):
    c.saveState()
    c.setFillColor(NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(VIOLET)
    c.rect(0, H * 0.60, W, 5, fill=1, stroke=0)

    c.setFillColor(AMBER)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(W/2, H * 0.64, "PARA SESSION TRACKER")

    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(W/2, H * 0.695, "What the Voice Carries")
    c.setFont("Helvetica", 13)
    c.setFillColor(colors.HexColor("#C084FC"))
    c.drawCentredString(W/2, H * 0.655, "Figurative Language in Poetry")

    c.setFillColor(VIOLET)
    c.roundRect(W/2 - 1.5*inch, H * 0.555, 3.0*inch, 0.33*inch, 5, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 9.5)
    c.drawCentredString(W/2, H * 0.564, "POETRY READING UNITS · UNIT 1  ·  GRADES 6–10")

    # Para instructions summary box
    c.setFillColor(colors.HexColor("#1E2A4A"))
    c.roundRect(0.75*inch, H*0.26, W - 1.5*inch, H*0.27, 8, fill=1, stroke=0)
    c.setFillColor(AMBER)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(W/2, H*0.505, "FOR THE PARAEDUCATOR")
    c.setFillColor(WHITE)
    c.setFont("Helvetica", 9)
    lines = [
        "This tracker is your data collection tool for each poem session.",
        "Circle DNM, A, or M for each criterion after the student responds.",
        "You do not need to score in real time — score at the end of the activity.",
        "All response modes count equally: AAC, pointing, eye gaze, writing, or speech.",
        "Pass completed tracker pages to the special educator weekly.",
    ]
    y = H * 0.475
    for line in lines:
        c.drawCentredString(W/2, y, line)
        y -= 0.165*inch

    # NFMA legend
    c.setFillColor(VIOLET)
    c.rect(0.75*inch, H*0.20, W - 1.5*inch, 0.3*inch, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 9)
    legend = "N = NOTICE   F = FEEL   M = MEAN   A = ASK"
    c.drawCentredString(W/2, H*0.211, legend)

    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(W/2 - 0.35*inch, H * 0.08, "COMMUNICATE")
    c.setFillColor(AMBER)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(W/2 + 0.75*inch, H * 0.08, "BY DESIGN")
    c.setFillColor(SLATE)
    c.setFont("Helvetica", 8)
    c.drawCentredString(W/2, H * 0.056, STORE)
    c.setFillColor(AMBER)
    c.rect(0, 0, W, 4, fill=1, stroke=0)
    c.restoreState()
    c.showPage()

# ── Poem Scoring Pages ────────────────────────────────────────────────────────
def page_poem(poem_title, poet_info, device_focus):
    story = [hdr(), Spacer(1, 0.06*inch)]

    # Poem title bar
    title_bar = Table([[
        Paragraph(f"<b>{poem_title}</b>", ParagraphStyle("pt", fontName="Helvetica-Bold",
            fontSize=11, textColor=WHITE, leading=14)),
        Paragraph(f"<i>{poet_info}</i>", ParagraphStyle("pi", fontName="Helvetica-Oblique",
            fontSize=9, textColor=colors.HexColor("#C084FC"), leading=12, alignment=TA_RIGHT)),
    ]], colWidths=[4.0*inch, 3.0*inch])
    title_bar.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),VIOLET),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("TOPPADDING",(0,0),(-1,-1),6),
        ("BOTTOMPADDING",(0,0),(-1,-1),6),
        ("LEFTPADDING",(0,0),(-1,-1),8),
        ("RIGHTPADDING",(0,0),(-1,-1),8),
    ]))
    story.append(title_bar)
    story.append(Spacer(1, 0.04*inch))
    story.append(Paragraph(f"<b>Primary device:</b> {device_focus}", SML))
    story.append(Spacer(1, 0.08*inch))

    # Student info row
    info_row = Table([[
        Paragraph("Student: ___________________________________", BODY),
        Paragraph("IEP #: ____________", BODY),
        Paragraph("Version: [ ] V1  [ ] V2  [ ] V3", BODY),
    ]], colWidths=[3.0*inch, 1.6*inch, 2.4*inch])
    info_row.setStyle(TableStyle([
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("TOPPADDING",(0,0),(-1,-1),3),
        ("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),0),
        ("RIGHTPADDING",(0,0),(-1,-1),4),
    ]))
    story.append(info_row)

    # 3-session scoring table
    # Header row: blank | Session 1 (3 cols: DNM / A / M) | Session 2 | Session 3
    hdr_style = ParagraphStyle("ths", fontName="Helvetica-Bold", fontSize=8,
        textColor=WHITE, leading=10, alignment=TA_CENTER)
    crit_style = ParagraphStyle("crs", fontName="Helvetica-Bold", fontSize=8,
        textColor=NAVY, leading=10)
    desc_style = ParagraphStyle("dsc", fontName="Helvetica", fontSize=7.5,
        textColor=colors.HexColor("#444444"), leading=10)
    cell_style = ParagraphStyle("cls", fontName="Helvetica", fontSize=10,
        textColor=NAVY, leading=12, alignment=TA_CENTER)

    COL_CRIT  = 2.4 * inch
    COL_SCORE = 0.52 * inch   # DNM / A / M — 3 per session × 3 sessions = 9 cols
    TOTAL_W   = COL_CRIT + COL_SCORE * 9  # = 2.4 + 4.68 = 7.08 ≈ 7 inch

    # Adjust to fit
    COL_SCORE = 0.50 * inch
    TOTAL_W   = COL_CRIT + COL_SCORE * 9

    def sess_hdr(n):
        return [
            Paragraph(f"S{n}", hdr_style),
            Paragraph("D", hdr_style),
            Paragraph("A", hdr_style),
        ]

    header_row = (
        [Paragraph("Criterion", hdr_style)] +
        sess_hdr(1) + sess_hdr(2) + sess_hdr(3)
    )

    # Sub-header row (DNM / A / M labels)
    sub_row = (
        [Paragraph("", hdr_style)] +
        [Paragraph(lbl, ParagraphStyle("slbl", fontName="Helvetica", fontSize=6.5,
            textColor=colors.HexColor("#CCCCCC"), leading=9, alignment=TA_CENTER))
         for lbl in ["DNM","A","M"] * 3]
    )

    rows = [header_row, sub_row]
    for crit_lbl, crit_desc in CRITERIA:
        row = [
            [Paragraph(crit_lbl, crit_style), Paragraph(crit_desc, desc_style)]
        ] + [Paragraph("○", cell_style) for _ in range(9)]
        rows.append(row)

    # Date row at bottom
    date_row = [
        Paragraph("<b>Date</b>", crit_style)
    ] + [
        Paragraph("__ /__ /__", ParagraphStyle("dr", fontName="Helvetica", fontSize=6.5,
            textColor=NAVY, leading=9, alignment=TA_CENTER))
        for _ in range(3)
    ] + [Paragraph("", crit_style)] * 3 + [
        Paragraph("__ /__ /__", ParagraphStyle("dr", fontName="Helvetica", fontSize=6.5,
            textColor=NAVY, leading=9, alignment=TA_CENTER))
        for _ in range(3)
    ] + [Paragraph("", crit_style)] * 3 + [
        Paragraph("__ /__ /__", ParagraphStyle("dr", fontName="Helvetica", fontSize=6.5,
            textColor=NAVY, leading=9, alignment=TA_CENTER))
        for _ in range(3)
    ]

    # Rebuild date row cleanly: date spans first 3 cols of each session block
    date_row = [Paragraph("<b>Date →</b>", crit_style)]
    for s in range(3):
        date_row.append(Paragraph("__ /__ /__", ParagraphStyle("dr2", fontName="Helvetica",
            fontSize=7, textColor=NAVY, leading=10, alignment=TA_CENTER)))
        date_row.append(Paragraph("", cell_style))
        date_row.append(Paragraph("", cell_style))
    rows.append(date_row)

    col_widths = [COL_CRIT] + [COL_SCORE] * 9
    tbl = Table(rows, colWidths=col_widths)

    tbl_style = [
        # Header rows
        ("BACKGROUND",(0,0),(-1,0), VIOLET),
        ("BACKGROUND",(0,1),(-1,1), colors.HexColor("#2D1B4E")),
        ("TEXTCOLOR",(0,0),(-1,1), WHITE),
        # Criterion rows
        ("FONTSIZE",(0,2),(0,-1), 8),
        ("VALIGN",(0,0),(-1,-1), "MIDDLE"),
        ("TOPPADDING",(0,0),(-1,-1), 3),
        ("BOTTOMPADDING",(0,0),(-1,-1), 3),
        ("LEFTPADDING",(0,0),(-1,-1), 3),
        ("RIGHTPADDING",(0,0),(-1,-1), 3),
        ("GRID",(0,0),(-1,-1), 0.5, MGRAY),
        # Session group dividers
        ("LINEAFTER",(3,0),(3,-1), 1.5, NAVY),   # after session 1 block (cols 1-3)
        ("LINEAFTER",(6,0),(6,-1), 1.5, NAVY),   # after session 2 block (cols 4-6)
        # Shade DNM column for each session block (cols 1, 4, 7)
        ("BACKGROUND",(1,2),(1,-2), colors.HexColor("#FEE2E2")),
        ("BACKGROUND",(4,2),(4,-2), colors.HexColor("#FEE2E2")),
        ("BACKGROUND",(7,2),(7,-2), colors.HexColor("#FEE2E2")),
        # Shade M (Meets) column for each session block (cols 3, 6, 9)
        ("BACKGROUND",(3,2),(3,-2), colors.HexColor("#D1FAE5")),
        ("BACKGROUND",(6,2),(6,-2), colors.HexColor("#D1FAE5")),
        ("BACKGROUND",(9,2),(9,-2), colors.HexColor("#D1FAE5")),
        # Bottom date row
        ("BACKGROUND",(0,-1),(-1,-1), colors.HexColor("#F5F3FF")),
        # Span the criterion column header
        ("SPAN",(0,0),(0,1)),
        # Span headers for each session block
        ("SPAN",(1,0),(3,0)),
        ("SPAN",(4,0),(6,0)),
        ("SPAN",(7,0),(9,0)),
    ]
    tbl.setStyle(TableStyle(tbl_style))
    story.append(tbl)
    story.append(Spacer(1, 0.06*inch))

    # Legend
    legend_style = ParagraphStyle("lg", fontName="Helvetica", fontSize=7.5, textColor=NAVY, leading=10)
    legend = Table([[
        Paragraph("<b>D = Does Not Yet Meet</b>  ·  <b>A = Approaching</b>  ·  <b>M = Meets</b>", legend_style),
        Paragraph("All response modes count equally: AAC · pointing · eye gaze · writing · speech", SML),
    ]], colWidths=[3.5*inch, 3.5*inch])
    legend.setStyle(TableStyle([
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("TOPPADDING",(0,0),(-1,-1),3),
        ("BOTTOMPADDING",(0,0),(-1,-1),3),
        ("LEFTPADDING",(0,0),(-1,-1),0),
        ("RIGHTPADDING",(0,0),(-1,-1),0),
    ]))
    story.append(legend)
    story.append(Spacer(1, 0.08*inch))

    # Response mode + notes fields (2 sets per page for 2 sessions if needed)
    for s_num in range(1, 4):
        rm_row = Table([[
            Paragraph(f"<b>Session {s_num} — Response mode used:</b> [ ] AAC device  [ ] Eye gaze  [ ] Pointing  [ ] Symbol card  [ ] Writing  [ ] Speech", BODY),
        ]], colWidths=[7.0*inch])
        rm_row.setStyle(TableStyle([
            ("TOPPADDING",(0,0),(-1,-1),3),
            ("BOTTOMPADDING",(0,0),(-1,-1),2),
            ("LEFTPADDING",(0,0),(-1,-1),0),
            ("RIGHTPADDING",(0,0),(-1,-1),0),
        ]))
        story.append(rm_row)
        note_row = Table([[
            Paragraph(f"<b>Session {s_num} — Notes:</b>  ____________________________________________________________", BODY),
        ]], colWidths=[7.0*inch])
        note_row.setStyle(TableStyle([
            ("TOPPADDING",(0,0),(-1,-1),1),
            ("BOTTOMPADDING",(0,0),(-1,-1),4),
            ("LEFTPADDING",(0,0),(-1,-1),0),
            ("RIGHTPADDING",(0,0),(-1,-1),0),
        ]))
        story.append(note_row)

    story.append(Spacer(1, 0.06*inch))
    story.append(callout(
        "<b>IEP data threshold:</b> Meets on Criteria 3 and 4 (MEAN + FEEL) across 3 consecutive sessions = "
        "mastery on the academic goal. Criteria 1 and 2 support the skill but the standard requires interpretation, "
        "not identification alone. Pass tracker to educator after each poem cycle for IEP data review.",
        bg=YELLOW_BG))
    story.append(Spacer(1, 0.08*inch))
    story.append(foot())
    return story

# ── Page 6: Cross-Poem Progress Summary ──────────────────────────────────────
def page_summary():
    story = [hdr(), Spacer(1, 0.08*inch)]
    story.append(sec_bar("CROSS-POEM PROGRESS SUMMARY"))
    story.append(Spacer(1, 0.06*inch))
    story.append(Paragraph(
        "Complete after all 4 poems are finished. Record best session score (DNM / A / M) per poem per criterion. "
        "Use to identify patterns: which NFMA steps are consistent, which need additional instructional focus.", BODY))
    story.append(Spacer(1, 0.1*inch))

    # Student info
    story.append(Paragraph("Student: _______________________________________   Date completed: _________________", BODY))
    story.append(Spacer(1, 0.1*inch))

    hdr_style = ParagraphStyle("sh", fontName="Helvetica-Bold", fontSize=8, textColor=WHITE, leading=10, alignment=TA_CENTER)
    crit_s = ParagraphStyle("cs", fontName="Helvetica", fontSize=8, textColor=NAVY, leading=10)
    cell_s = ParagraphStyle("ce", fontName="Helvetica", fontSize=9, textColor=NAVY, leading=11, alignment=TA_CENTER)
    poem_s = ParagraphStyle("ps", fontName="Helvetica-Bold", fontSize=7.5, textColor=VIOLET, leading=10, alignment=TA_CENTER)

    poem_headers = [
        Paragraph("We Wear\nthe Mask", poem_s),
        Paragraph("I'm Nobody!\nWho are you?", poem_s),
        Paragraph("The Man\nwith the Hoe", poem_s),
        Paragraph("The Words\nI Carry", poem_s),
    ]
    hdr_row = [Paragraph("Criterion", hdr_style)] + poem_headers
    rows = [hdr_row]
    for crit_lbl, crit_desc in CRITERIA:
        rows.append([
            [Paragraph(crit_lbl, ParagraphStyle("cll", fontName="Helvetica-Bold",
                fontSize=7.5, textColor=NAVY, leading=10)),
             Paragraph(crit_desc, ParagraphStyle("cld", fontName="Helvetica",
                fontSize=7, textColor=SLATE, leading=9))],
        ] + [Paragraph("D  /  A  /  M", cell_s) for _ in range(4)])

    col_widths = [2.5*inch] + [1.1*inch] * 4
    tbl = Table(rows, colWidths=col_widths)
    tbl.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0), VIOLET),
        ("TEXTCOLOR",(0,0),(-1,0), WHITE),
        ("FONTSIZE",(0,0),(-1,-1), 8),
        ("VALIGN",(0,0),(-1,-1), "MIDDLE"),
        ("TOPPADDING",(0,0),(-1,-1), 6),
        ("BOTTOMPADDING",(0,0),(-1,-1), 6),
        ("LEFTPADDING",(0,0),(-1,-1), 4),
        ("RIGHTPADDING",(0,0),(-1,-1), 4),
        ("GRID",(0,0),(-1,-1), 0.5, MGRAY),
        ("LINEBELOW",(0,0),(-1,0), 1.5, NAVY),
    ]))
    story.append(tbl)
    story.append(Spacer(1, 0.12*inch))

    # Pattern analysis prompts
    story.append(Paragraph("<b>Pattern Analysis (educator completes):</b>", H2))
    prompts = [
        "Which criterion is most consistently at Meets across all 4 poems?",
        "Which criterion is most often at Does Not Yet Meet or Approaching?",
        "Which poem showed the strongest overall performance?",
        "Which poem was most difficult? What might explain the difference?",
        "Is response mode consistent across poems, or does it shift between poems?",
        "Is the student on track for mastery (Meets on C3 + C4 for 3 consecutive sessions)?",
    ]
    for prompt in prompts:
        t = Table([[
            Paragraph(f"• {prompt}", BODY),
            Paragraph("_______________________________________________________________", SML),
        ]], colWidths=[2.8*inch, 4.2*inch])
        t.setStyle(TableStyle([
            ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
            ("TOPPADDING",(0,0),(-1,-1),4),
            ("BOTTOMPADDING",(0,0),(-1,-1),4),
            ("LEFTPADDING",(0,0),(-1,-1),0),
            ("RIGHTPADDING",(0,0),(-1,-1),0),
            ("LINEBELOW",(0,0),(-1,-1),0.4,MGRAY),
        ]))
        story.append(t)

    story.append(Spacer(1, 0.12*inch))
    story.append(callout(
        "<b>Next steps:</b> Share this summary with the SLP at the end of the unit. "
        "If the student is Approaching or DNM on C3/C4 across all poems, discuss whether additional "
        "vocabulary pre-teaching or a different sentence frame is needed before the next poetry unit."))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(
        "© Communicate by Design  ·  All rights reserved  ·  " + STORE, FOOT))
    story.append(Spacer(1, 0.04*inch))
    story.append(foot())
    return story

# ── Build ─────────────────────────────────────────────────────────────────────
def build():
    # Cover via canvas
    cover_buf = io.BytesIO()
    c = rl_canvas.Canvas(cover_buf, pagesize=letter)
    build_cover(c)
    c.save()
    cover_bytes = cover_buf.getvalue()

    # Inner pages via Flowables
    inner_buf = io.BytesIO()
    doc = SimpleDocTemplate(
        inner_buf, pagesize=letter,
        leftMargin=0.75*inch, rightMargin=0.75*inch,
        topMargin=0.5*inch, bottomMargin=0.5*inch
    )
    all_pages = []
    for i, (title, poet, device) in enumerate(POEMS):
        all_pages += page_poem(title, poet, device)
        if i < len(POEMS) - 1:
            all_pages.append(PageBreak())
    all_pages.append(PageBreak())
    all_pages += page_summary()
    doc.build(all_pages)
    inner_bytes = inner_buf.getvalue()

    # Merge
    from pypdf import PdfReader, PdfWriter
    writer = PdfWriter()
    for reader in [PdfReader(io.BytesIO(cover_bytes)), PdfReader(io.BytesIO(inner_bytes))]:
        for page in reader.pages:
            writer.add_page(page)
    writer.add_metadata({
        "/Title": "What the Voice Carries — Session Tracker",
        "/Author": "Communicate by Design — Jill McCardel",
        "/Subject": "Poetry Reading Units · Unit 1 · Para Data Collection",
    })
    with open(OUT, "wb") as f:
        writer.write(f)

    import os as _os
    size_kb = _os.path.getsize(OUT) / 1024
    from pypdf import PdfReader as PR
    pages = len(PR(OUT).pages)
    print(f"Session Tracker created: {OUT}")
    print(f"Size: {size_kb:.1f} KB  ·  Pages: {pages} (1 cover + 4 poem pages + 1 summary)")

if __name__ == "__main__":
    build()

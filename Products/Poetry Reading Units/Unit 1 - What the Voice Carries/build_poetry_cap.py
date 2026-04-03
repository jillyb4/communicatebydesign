"""
Communication Access Packet — What the Voice Carries
Poetry Reading Units · Unit 1 · Communicate by Design

Structure:
  p1    Cover
  p2    How to Use This Packet
  p3    SLP Pre-Programming Checklist + Timeline
  p4    Fringe Vocabulary Reference Table (all 10 fringe words)
  p5    Semi-Core Verification Checklist (5 words to verify on device)
  p6    Top 5 Fringe — Symbol Cards (speaker, mask, voice, labor, hoe)
  p7    Text-Label Cards — Abstract Terms (figurative language, metaphor, imagery, tone, pretend)
  p8    Response Core Vocabulary Reference
  p9    Partner Quick Reference — NFMA Partner Moves
  p10   IEP Goal Stems

Colors: VIOLET #6B21A8 (poetry line docs), NAVY #1B1F3B, AMBER #FFB703, TEAL #006DA0
"""

import os, io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.platypus.flowables import Image as RLImage

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE      = os.path.dirname(os.path.abspath(__file__))
SYM_CACHE = os.path.join(BASE, "..", "..", "..", "_Operations", "symbol_cache")
OUT       = os.path.join(BASE, "What_the_Voice_Carries_CAP.pdf")

UNIT  = "What the Voice Carries — Figurative Language in Poetry"
STORE = "teacherspayteachers.com/store/communicate-by-design"

# ── Brand Colors ──────────────────────────────────────────────────────────────
VIOLET = colors.HexColor("#6B21A8")
LVIOLET= colors.HexColor("#EDE9FE")   # light violet bg
NAVY   = colors.HexColor("#1B1F3B")
TEAL   = colors.HexColor("#006DA0")
AMBER  = colors.HexColor("#FFB703")
SLATE  = colors.HexColor("#94A3B8")
WHITE  = colors.white
LGRAY  = colors.HexColor("#F5F5F5")
MGRAY  = colors.HexColor("#DDDDDD")

# ── Fitzgerald Key Colors ─────────────────────────────────────────────────────
FKC = {
    "green":  colors.HexColor("#C8E6C9"),
    "orange": colors.HexColor("#FFE0B2"),
    "yellow": colors.HexColor("#FFF9C4"),
    "blue":   colors.HexColor("#BBDEFB"),
    "pink":   colors.HexColor("#FCE4EC"),
    "white":  colors.HexColor("#F5F5F5"),
}
FKC_BORDER = {
    "green":  colors.HexColor("#2E7D32"),
    "orange": colors.HexColor("#E65100"),
    "yellow": colors.HexColor("#F57F17"),
    "blue":   colors.HexColor("#1565C0"),
    "pink":   colors.HexColor("#880E4F"),
    "white":  colors.HexColor("#757575"),
}

# ── Vocabulary Data ───────────────────────────────────────────────────────────
# (word, fk_category, aac_layer, instruct_layer, tier, notes, has_symbol)
FRINGE_VOCAB = [
    ("figurative language", "white", "Fringe", "Explicit",    3, "Unit overarching term; teach before Day 1; ★ Top 5", False),
    ("metaphor",            "white", "Fringe", "Explicit",    3, "Primary device in Dunbar + CbD poem; ★ Top 5",      False),
    ("imagery",             "white", "Fringe", "Explicit",    3, "Primary device in Markham + CbD poem; ★ Top 5",     False),
    ("tone",                "white", "Fringe", "Explicit",    3, "Connects FEEL → MEAN; all 4 poems; ★ Top 5",        False),
    ("speaker",             "white", "Fringe", "Explicit",    3, "Who is talking? All 4 poems; ★ Top 5",              True),
    ("mask",                "white", "Fringe", "Explicit",    3, "Literal → extended metaphor (Dunbar); teach literal first", True),
    ("pretend",             "green", "Fringe", "Generative",  2, "Connects to Dunbar's mask; generative in MEAN",     False),
    ("voice",               "white", "Fringe", "Generative",  2, "Unit title word; generative in all NFMA responses", True),
    ("labor",               "white", "Fringe", "Background",  3, "Markham context; background only",                  True),
    ("hoe",                 "white", "Fringe", "Background",  3, "Markham poem title; concrete tool; background only",True),
]

SEMI_CORE = [
    ("hide",  "green", "Dunbar; generative in FEEL/MEAN responses"),
    ("pain",  "pink",  "Dunbar; generative in FEEL step"),
    ("proud", "pink",  "CbD poem/Dickinson; generative in FEEL step"),
    ("alone", "pink",  "Dickinson; generative in FEEL step"),
    ("free",  "pink",  "CbD poem; generative in MEAN step"),
]

RESPONSE_CORE = [
    "because", "show", "prove", "agree", "same", "different",
    "not", "true", "wrong", "feel", "mean", "notice", "ask"
]

# ── Helpers ───────────────────────────────────────────────────────────────────

def sym_path(word):
    p = os.path.join(SYM_CACHE, f"arasaac_{word.lower().replace(' ','_')}.png")
    return p if os.path.exists(p) else None

W, H = letter

def build_cover(c):
    """Full-bleed navy cover with violet accent."""
    c.saveState()
    # Navy background
    c.setFillColor(NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    # Violet accent bar
    c.setFillColor(VIOLET)
    c.rect(0, H * 0.60, W, 6, fill=1, stroke=0)
    c.rect(0, H * 0.59 - 2, W, 2, fill=1, stroke=0)

    # "COMMUNICATION ACCESS PACKET" label
    c.setFillColor(AMBER)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(W/2, H * 0.64, "COMMUNICATION ACCESS PACKET")

    # Unit title
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 22)
    # Word wrap the unit title
    line1 = "What the Voice Carries"
    line2 = "Figurative Language in Poetry"
    c.drawCentredString(W/2, H * 0.70, line1)
    c.setFont("Helvetica", 15)
    c.setFillColor(colors.HexColor("#C084FC"))   # bright violet accent
    c.drawCentredString(W/2, H * 0.655, line2)

    # Product line badge
    c.setFillColor(VIOLET)
    c.roundRect(W/2 - 1.4*inch, H * 0.555, 2.8*inch, 0.35*inch, 6, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(W/2, H * 0.565, "POETRY READING UNITS · UNIT 1")

    # Who it's for
    c.setFillColor(SLATE)
    c.setFont("Helvetica", 10)
    c.drawCentredString(W/2, H * 0.52, "For the SLP, Special Educator, and AAC Communication Team")

    # Grade / price band
    c.setFillColor(colors.HexColor("#94A3B8"))
    c.setFont("Helvetica", 10)
    c.drawCentredString(W/2, H * 0.49, "Grades 6–10  ·  RL.6.4 / RL.7.4 / L.5.5")

    # CbD wordmark
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(W/2 - 0.35*inch, H * 0.08, "COMMUNICATE")
    c.setFillColor(AMBER)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(W/2 + 0.85*inch, H * 0.08, "BY DESIGN")
    c.setFillColor(SLATE)
    c.setFont("Helvetica", 8)
    c.drawCentredString(W/2, H * 0.055, STORE)

    # amber bottom bar
    c.setFillColor(AMBER)
    c.rect(0, 0, W, 4, fill=1, stroke=0)
    c.restoreState()
    c.showPage()


def make_doc(buf):
    return SimpleDocTemplate(
        buf, pagesize=letter,
        leftMargin=0.75*inch, rightMargin=0.75*inch,
        topMargin=0.55*inch, bottomMargin=0.55*inch
    )

# ── Paragraph Styles ─────────────────────────────────────────────────────────
H1   = ParagraphStyle("H1", fontName="Helvetica-Bold",   fontSize=14, textColor=VIOLET, leading=18, spaceAfter=6)
H2   = ParagraphStyle("H2", fontName="Helvetica-Bold",   fontSize=11, textColor=NAVY,   leading=14, spaceAfter=4)
BODY = ParagraphStyle("BD", fontName="Helvetica",        fontSize=9,  textColor=NAVY,   leading=13, spaceAfter=4)
BOLD = ParagraphStyle("BL", fontName="Helvetica-Bold",   fontSize=9,  textColor=NAVY,   leading=13, spaceAfter=4)
SML  = ParagraphStyle("SM", fontName="Helvetica",        fontSize=8,  textColor=SLATE,  leading=11, spaceAfter=2)
CTR  = ParagraphStyle("CT", fontName="Helvetica",        fontSize=9,  textColor=NAVY,   leading=13, spaceAfter=4, alignment=TA_CENTER)
CTRBOLD = ParagraphStyle("CB", fontName="Helvetica-Bold",fontSize=9,  textColor=WHITE,  leading=13, spaceAfter=4, alignment=TA_CENTER)
FOOT = ParagraphStyle("FT", fontName="Helvetica",        fontSize=7,  textColor=SLATE,  leading=9,  alignment=TA_CENTER)

def hdr():
    hl = ParagraphStyle("hl", fontName="Helvetica-Oblique", fontSize=9, textColor=NAVY, leading=13)
    hr = ParagraphStyle("hr", fontName="Helvetica-Bold",    fontSize=9, textColor=TEAL, leading=13, alignment=TA_RIGHT)
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
        f"{UNIT}  ·  Communication Access Packet  ·  "
        "Communicate by Design  ·  " + STORE, FOOT)

def sec_bar(title):
    """Violet section bar."""
    t = Table([[Paragraph(f"<b>{title}</b>", CTRBOLD)]], colWidths=[7*inch])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),VIOLET),
        ("TOPPADDING",(0,0),(-1,-1),5),
        ("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),8),
        ("RIGHTPADDING",(0,0),(-1,-1),8),
    ]))
    return t

def callout_box(text, bg=None):
    bg = bg or LVIOLET
    t = Table([[Paragraph(text, BODY)]], colWidths=[6.8*inch])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),bg),
        ("BOX",(0,0),(-1,-1),1,VIOLET),
        ("TOPPADDING",(0,0),(-1,-1),6),
        ("BOTTOMPADDING",(0,0),(-1,-1),6),
        ("LEFTPADDING",(0,0),(-1,-1),10),
        ("RIGHTPADDING",(0,0),(-1,-1),10),
    ]))
    return t

# ── Page 2: How to Use ────────────────────────────────────────────────────────
def page_how_to_use():
    story = [hdr(), Spacer(1, 0.1*inch)]
    story.append(sec_bar("HOW TO USE THIS PACKET"))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(
        "This Communication Access Packet (CAP) is the communication team's shared preparation tool for <i>What the Voice Carries</i>. "
        "It supports students who use any form of AAC — SGD, e-trans board, symbol cards, alternative pencil, or a combination. "
        "No student should be waiting for device programming before they can participate. "
        "Symbol cards and printed choice boards in this packet provide immediate access on Day 1.", BODY))
    story.append(Spacer(1, 0.08*inch))

    story.append(Paragraph("<b>Who uses this packet:</b>", BOLD))
    rows = [
        ["Special Educator", "Owns vocabulary access planning. Prepares low-tech symbol cards and printed choice boards so students can participate on Day 1 — before any device programming. Models fringe words at every NFMA prompt (ALgS)."],
        ["SLP", "Contributes fringe vocabulary list for potential SGD programming. Whether and which words go on the SGD is a team conversation based on student interest and use — not a unilateral programming decision. The CAP supports that conversation."],
        ["Paraeducator", "Uses Partner Quick Reference during student sessions. Follows 5-second wait, Choice Offer, and Expand moves. Can prepare and use low-tech symbol cards independently."],
        ["Student", "Uses any form of AAC — device, symbol cards, e-trans board, alternative pencil — to respond to NFMA prompts. All response modes are valid and equivalent."],
    ]
    tbl = Table(rows, colWidths=[1.2*inch, 5.8*inch])
    tbl.setStyle(TableStyle([
        ("FONTNAME",(0,0),(0,-1),"Helvetica-Bold"),
        ("FONTNAME",(1,0),(1,-1),"Helvetica"),
        ("FONTSIZE",(0,0),(-1,-1),9),
        ("TEXTCOLOR",(0,0),(-1,-1),NAVY),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("TOPPADDING",(0,0),(-1,-1),4),
        ("BOTTOMPADDING",(0,0),(-1,-1),4),
        ("LEFTPADDING",(0,0),(-1,-1),4),
        ("RIGHTPADDING",(0,0),(-1,-1),4),
        ("LINEBELOW",(0,0),(-1,-2),0.5,MGRAY),
        ("BOX",(0,0),(-1,-1),0.75,MGRAY),
    ]))
    story.append(tbl)
    story.append(Spacer(1, 0.12*inch))

    story.append(Paragraph("<b>What's included in this packet:</b>", BOLD))
    items = [
        "Vocabulary Access Checklist — low-tech symbol access (Day 1) and SGD conversation guide (team-driven)",
        "Fringe Vocabulary Reference Table — all 10 unit fringe words with Fitzgerald Key category",
        "Semi-Core Verification Checklist — 5 words to confirm are accessible on the student's system",
        "Symbol Cards (print, cut, laminate) — 5 words with ARASAAC symbols: speaker, mask, voice, labor, hoe",
        "Text-Label Cards — 5 abstract terms without clear picture symbols: figurative language, metaphor, imagery, tone, pretend",
        "Response Core Vocabulary — standard CbD set used across all product lines; builds one motor pathway",
        "Partner Quick Reference — NFMA partner moves at each step with wait time guidance",
        "IEP Goal Stems — academic (RL.6.4) and AAC communication goal language",
    ]
    for item in items:
        story.append(Paragraph(f"• {item}", BODY))
    story.append(Spacer(1, 0.12*inch))

    story.append(callout_box(
        "<b>AAC access is active at ALL versions.</b> V1, V2, and V3 students all use the same vocabulary — via symbol cards, "
        "low-tech boards, or their AAC device. The scaffold changes; the vocabulary and the standard do not. "
        "A student using a V3 format with symbol cards is working toward the same RL.6.4 standard as a V1 student with a device. "
        "The access layer is the product. Device programming is one access path — not the only one."))
    story.append(Spacer(1, 0.15*inch))
    story.append(foot())
    return story

# ── Page 3: SLP Checklist ─────────────────────────────────────────────────────
def page_slp_checklist():
    story = [hdr(), Spacer(1, 0.1*inch)]
    story.append(sec_bar("VOCABULARY ACCESS CHECKLIST — COMMUNICATION TEAM"))
    story.append(Spacer(1, 0.08*inch))

    story.append(callout_box(
        "<b>Two tiers — two timelines.</b> "
        "Tier 1 (Day 1): Symbol cards and printed choice boards in this packet give students immediate access — no device programming required. Any team member can prepare these. "
        "Tier 2 (Team conversation): Whether fringe words go onto the student's SGD is a separate discussion based on student interest and use. "
        "The list below supports that conversation. No student waits for Tier 2 before participating."))
    story.append(Spacer(1, 0.1*inch))

    story.append(Paragraph("<b>Fringe Vocabulary — Low-Tech Access Checklist (Tier 1, Day 1)</b>", H2))
    story.append(Paragraph(
        "Symbol cards for these words are in this packet. Print, cut, and laminate. "
        "Any team member can prepare and use them. Check each word as cards are ready.", BODY))
    story.append(Spacer(1, 0.04*inch))
    chk_rows = [
        ["[ ]", "figurative language", "★ Top 5 · Teach before Day 1 · Text-label card included"],
        ["[ ]", "metaphor",            "★ Top 5 · Text-label card included"],
        ["[ ]", "imagery",             "★ Top 5 · Text-label card included"],
        ["[ ]", "tone",                "★ Top 5 · Text-label card included"],
        ["[ ]", "speaker",             "★ Top 5 · Symbol card included (ARASAAC)"],
        ["[ ]", "mask",                "Symbol card included · Teach literal meaning first, then figurative"],
        ["[ ]", "pretend",             "Text-label card included · Connects to Dunbar's mask metaphor"],
        ["[ ]", "voice",               "Symbol card included (ARASAAC) · Unit title word"],
        ["[ ]", "labor",               "Symbol card included (ARASAAC) · Background — Markham context"],
        ["[ ]", "hoe",                 "Symbol card included (ARASAAC) · Concrete tool — define before reading"],
    ]
    tbl = Table(chk_rows, colWidths=[0.3*inch, 1.4*inch, 5.3*inch])
    tbl.setStyle(TableStyle([
        ("FONTNAME",(0,0),(0,-1),"Helvetica"),
        ("FONTNAME",(1,0),(1,-1),"Helvetica-Bold"),
        ("FONTNAME",(2,0),(2,-1),"Helvetica"),
        ("FONTSIZE",(0,0),(-1,-1),9),
        ("TEXTCOLOR",(0,0),(-1,-1),NAVY),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("TOPPADDING",(0,0),(-1,-1),5),
        ("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),4),
        ("RIGHTPADDING",(0,0),(-1,-1),4),
        ("LINEBELOW",(0,0),(-1,-2),0.5,MGRAY),
        ("BOX",(0,0),(-1,-1),0.75,MGRAY),
        ("BACKGROUND",(0,0),(-1,4),colors.HexColor("#F0E8FF")),  # top 5 shaded
    ]))
    story.append(tbl)
    story.append(Spacer(1, 0.12*inch))

    story.append(Paragraph("<b>Semi-Core Verification — 5 Words to Confirm Are Accessible</b>", H2))
    story.append(Paragraph(
        "These words are likely already on the student's AAC system or low-tech board. "
        "Confirm they are accessible before Day 1. If absent from the device, add them to the low-tech choice board — "
        "whether they also go on the SGD is a team conversation.", BODY))
    semi_rows = [
        ["[ ]", "hide",  "Green (verb)",  "Dunbar — FEEL/MEAN generative"],
        ["[ ]", "pain",  "Pink (feeling)", "Dunbar — FEEL generative"],
        ["[ ]", "proud", "Pink (feeling)", "Dickinson / CbD poem — FEEL generative"],
        ["[ ]", "alone", "Pink (feeling)", "Dickinson — FEEL generative"],
        ["[ ]", "free",  "Pink (feeling)", "CbD poem — MEAN generative"],
    ]
    s_tbl = Table(semi_rows, colWidths=[0.3*inch, 0.9*inch, 1.2*inch, 4.6*inch])
    s_tbl.setStyle(TableStyle([
        ("FONTNAME",(0,0),(0,-1),"Helvetica"),
        ("FONTNAME",(1,0),(1,-1),"Helvetica-Bold"),
        ("FONTNAME",(2,0),(2,-1),"Helvetica-Oblique"),
        ("FONTNAME",(3,0),(3,-1),"Helvetica"),
        ("FONTSIZE",(0,0),(-1,-1),9),
        ("TEXTCOLOR",(0,0),(-1,-1),NAVY),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("TOPPADDING",(0,0),(-1,-1),5),
        ("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),4),
        ("RIGHTPADDING",(0,0),(-1,-1),4),
        ("LINEBELOW",(0,0),(-1,-2),0.5,MGRAY),
        ("BOX",(0,0),(-1,-1),0.75,MGRAY),
    ]))
    story.append(s_tbl)
    story.append(Spacer(1, 0.12*inch))

    story.append(Paragraph("<b>Communication Team Timeline</b>", H2))
    tl_rows = [
        ["Before Day 1\n(any team member)", "Print, cut, and laminate symbol cards and text-label cards from this packet. "
                                  "Prepare printed choice boards if student uses low-tech AAC. "
                                  "Confirm the 5 semi-core words are accessible on whatever system the student uses."],
        ["Before Day 1\n(SLP contribution)", "Review the fringe vocabulary list for potential SGD additions. "
                                  "Consider: will this student return to these words? If yes — program as individual words "
                                  "AND consider loading NFMA response frames as phrase buttons to reduce motor planning "
                                  "(e.g., 'The figurative language is ___ because ___' as one button + content fill-in)."],
        ["Day 1", "Confirm low-tech symbol access is ready. Confirm partner has Partner Quick Reference. "
                  "Student can participate in full lesson using symbol cards — device programming is not a prerequisite."],
        ["Week 1", "Check in after Poem 1. Is the student using the vocabulary? Reaching for words independently? "
                   "This data informs whether additional fringe words belong on the SGD."],
        ["Ongoing", "Review Session Tracker weekly. If student shows interest and returns to vocabulary — "
                    "consider adding to SGD. If understanding is demonstrated via low-tech only — "
                    "that is sufficient. Standard met."],
    ]
    tl_tbl = Table(tl_rows, colWidths=[1.6*inch, 5.4*inch])
    tl_tbl.setStyle(TableStyle([
        ("FONTNAME",(0,0),(0,-1),"Helvetica-Bold"),
        ("FONTNAME",(1,0),(1,-1),"Helvetica"),
        ("FONTSIZE",(0,0),(-1,-1),9),
        ("TEXTCOLOR",(0,0),(-1,-1),NAVY),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("TOPPADDING",(0,0),(-1,-1),5),
        ("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),4),
        ("RIGHTPADDING",(0,0),(-1,-1),4),
        ("LINEBELOW",(0,0),(-1,-2),0.5,MGRAY),
        ("BOX",(0,0),(-1,-1),0.75,MGRAY),
    ]))
    story.append(tl_tbl)
    story.append(Spacer(1, 0.12*inch))
    story.append(foot())
    return story

# ── Page 4: Fringe Vocabulary Reference Table ─────────────────────────────────
def page_fringe_table():
    story = [hdr(), Spacer(1, 0.1*inch)]
    story.append(sec_bar("FRINGE VOCABULARY REFERENCE TABLE"))
    story.append(Spacer(1, 0.08*inch))
    story.append(Paragraph(
        "All 10 fringe vocabulary words for Unit 1. Pre-program before Day 1. "
        "Top 5 priority words are shaded — these are the explicit instruction targets.", BODY))
    story.append(Spacer(1, 0.08*inch))

    hdr_row = [
        Paragraph("<b>Word</b>", CTRBOLD),
        Paragraph("<b>Fitzgerald Key</b>", CTRBOLD),
        Paragraph("<b>AAC Layer</b>", CTRBOLD),
        Paragraph("<b>Instructional Role</b>", CTRBOLD),
        Paragraph("<b>Tier</b>", CTRBOLD),
        Paragraph("<b>Symbol</b>", CTRBOLD),
    ]
    rows = [hdr_row]
    for word, fk, aac, inst, tier, note, has_sym in FRINGE_VOCAB:
        top5 = "★" in note
        rows.append([
            Paragraph(f"<b>{word}</b>" + (" ★" if top5 else ""), BODY),
            Paragraph(f"{fk.title()}", BODY),
            Paragraph(aac, BODY),
            Paragraph(inst, BODY),
            Paragraph(str(tier), CTR),
            Paragraph("✓ ARASAAC" if has_sym else "Text label", BODY),
        ])

    tbl = Table(rows, colWidths=[1.25*inch, 0.85*inch, 0.75*inch, 1.0*inch, 0.4*inch, 0.95*inch])
    style = [
        ("BACKGROUND",(0,0),(-1,0),VIOLET),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("TEXTCOLOR",(0,0),(-1,0),WHITE),
        ("FONTNAME",(0,1),(0,-1),"Helvetica-Bold"),
        ("FONTNAME",(1,1),(-1,-1),"Helvetica"),
        ("FONTSIZE",(0,0),(-1,-1),9),
        ("TEXTCOLOR",(0,1),(-1,-1),NAVY),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("TOPPADDING",(0,0),(-1,-1),5),
        ("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),4),
        ("RIGHTPADDING",(0,0),(-1,-1),4),
        ("GRID",(0,0),(-1,-1),0.5,MGRAY),
    ]
    # shade top 5 rows (rows 1–5)
    for r in range(1, 6):
        style.append(("BACKGROUND",(0,r),(-1,r),colors.HexColor("#F0E8FF")))
    tbl.setStyle(TableStyle(style))
    story.append(tbl)
    story.append(Spacer(1, 0.1*inch))

    story.append(Paragraph(
        "<b>Fitzgerald Key color codes:</b> White/Grey = nouns · Green = verbs · "
        "Pink = feelings/social · Orange = adjectives · Blue = prepositions · Yellow = pronouns", SML))
    story.append(Spacer(1, 0.08*inch))
    story.append(callout_box(
        "<b>★ Top 5 priority fringe words</b> (shaded above) are the explicit instruction targets for this unit. "
        "All other fringe words are background or generative support vocabulary. If device capacity is limited, "
        "prioritize the Top 5 before any other pre-programming."))
    story.append(Spacer(1, 0.15*inch))
    story.append(foot())
    return story

# ── Page 5: Semi-Core Verification ───────────────────────────────────────────
# (Folded into page 3 above — skip to symbol cards)

# ── Page 6: Symbol Cards (5 words with ARASAAC symbols) ──────────────────────
def page_symbol_cards():
    """5 symbol cards matching cbd_symbol_cards.py template:
       Zone 1: category bar + color dot + category label
       Zone 2: ARASAAC symbol with Fitzgerald border
       Zone 3: word (bold) + POS sublabel — NO notes, NO definitions.
    """
    # (word, fk_key) — no notes on cards per CbD standard
    SYM_WORDS = [
        ("speaker", "white"),
        ("mask",    "white"),
        ("voice",   "white"),
        ("labor",   "white"),
        ("hoe",     "white"),
    ]
    SYM_W = 1.65 * inch
    SYM_H = 1.65 * inch

    story = [hdr(), Spacer(1, 0.06*inch)]
    story.append(sec_bar("SYMBOL CARDS — Print, Cut, and Laminate"))
    story.append(Spacer(1, 0.06*inch))
    story.append(Paragraph(
        "ARASAAC symbols for 5 concrete vocabulary words. Print on cardstock, cut along borders, laminate. "
        "Use for low-tech AAC choice boards, PEC sets, or as pre-teach visual support before programming.", BODY))
    story.append(Spacer(1, 0.08*inch))

    # Fitzgerald-style category styles for nouns (white) and verbs (green)
    FK_STYLES = {
        "white": {"bar": colors.HexColor("#F5F5F5"), "dot": colors.HexColor("#8B6914"),
                  "border": colors.HexColor("#8B6914"), "word": colors.HexColor("#6B4F10"),
                  "label": "NOUNS"},
        "green": {"bar": colors.HexColor("#E8F5E9"), "dot": colors.HexColor("#00A86B"),
                  "border": colors.HexColor("#2E7D32"), "word": colors.HexColor("#2E7D32"),
                  "label": "ACTIONS"},
    }

    CAT_BAR_H  = 0.28 * inch
    WORD_ZONE_H = 0.52 * inch
    CARD_W = 3.0 * inch
    CARD_H = 3.5 * inch

    def card_cell(word, fk):
        """Build one symbol card matching the standard 3-zone template."""
        img_path = sym_path(word)
        st = FK_STYLES[fk]

        cat_bar_style = ParagraphStyle("cb2", fontName="Helvetica-Bold", fontSize=7,
            textColor=colors.HexColor("#666666"), leading=10)
        word_style = ParagraphStyle("ws2", fontName="Helvetica-Bold", fontSize=16,
            textColor=st["word"], leading=20, alignment=TA_CENTER)
        pos_style  = ParagraphStyle("ps2", fontName="Helvetica", fontSize=7,
            textColor=colors.HexColor("#888888"), leading=9, alignment=TA_CENTER)

        # Zone 1 — category bar row
        cat_bar = Table([[
            Paragraph(f"● {st['label']}", cat_bar_style),
        ]], colWidths=[CARD_W - 12])
        cat_bar.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,-1), st["bar"]),
            ("TOPPADDING",(0,0),(-1,-1), 4),
            ("BOTTOMPADDING",(0,0),(-1,-1), 4),
            ("LEFTPADDING",(0,0),(-1,-1), 8),
            ("RIGHTPADDING",(0,0),(-1,-1), 4),
        ]))

        # Zone 2 — symbol box with Fitzgerald border
        sym_items = []
        if img_path:
            sym_items = [RLImage(img_path, width=SYM_W, height=SYM_H)]
        else:
            sym_items = [Spacer(SYM_W, SYM_H)]
        sym_box = Table([sym_items], colWidths=[CARD_W - 16])
        sym_box.setStyle(TableStyle([
            ("BOX",(0,0),(-1,-1), 2.5, st["border"]),
            ("ALIGN",(0,0),(-1,-1),"CENTER"),
            ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
            ("TOPPADDING",(0,0),(-1,-1), 4),
            ("BOTTOMPADDING",(0,0),(-1,-1), 4),
            ("LEFTPADDING",(0,0),(-1,-1), 4),
            ("RIGHTPADDING",(0,0),(-1,-1), 4),
        ]))

        # Zone 3 — word + POS label (NO extra notes)
        word_zone = Table([[
            [Paragraph(word.upper(), word_style),
             Paragraph(st["label"], pos_style)]
        ]], colWidths=[CARD_W - 12])
        word_zone.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,-1), colors.HexColor("#FAFAFA")),
            ("TOPPADDING",(0,0),(-1,-1), 4),
            ("BOTTOMPADDING",(0,0),(-1,-1), 4),
            ("LEFTPADDING",(0,0),(-1,-1), 4),
            ("RIGHTPADDING",(0,0),(-1,-1), 4),
            ("ALIGN",(0,0),(-1,-1),"CENTER"),
        ]))

        # Outer card wrapper
        card = Table([
            [cat_bar],
            [sym_box],
            [word_zone],
        ], colWidths=[CARD_W])
        card.setStyle(TableStyle([
            ("BOX",(0,0),(-1,-1), 0.5, colors.HexColor("#DDDDDD")),
            ("LEFTPADDING",(0,0),(-1,-1), 6),
            ("RIGHTPADDING",(0,0),(-1,-1), 6),
            ("TOPPADDING",(0,0),(-1,-1), 0),
            ("BOTTOMPADDING",(0,0),(-1,-1), 0),
        ]))
        return card

    cells = [card_cell(w, fk) for w, fk in SYM_WORDS]

    # 2-column grid
    rows = []
    for i in range(0, len(cells), 2):
        row = []
        for j in range(2):
            row.append(cells[i + j] if (i + j) < len(cells) else Spacer(3.0*inch, 1))
        rows.append(row)

    grid = Table(rows, colWidths=[3.5*inch, 3.5*inch], rowHeights=None)
    grid.setStyle(TableStyle([
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("TOPPADDING",(0,0),(-1,-1),5),
        ("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),5),
        ("RIGHTPADDING",(0,0),(-1,-1),5),
    ]))
    story.append(grid)
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(
        "Symbol borders follow the Fitzgerald Key color system. ARASAAC symbols © ARASAAC — used under Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 license.", SML))
    story.append(Spacer(1, 0.08*inch))
    story.append(foot())
    return story

# ── Page 7: Text-Label Cards (abstract terms) ─────────────────────────────────
def page_text_label_cards():
    """Text-label cards for abstract terms without ARASAAC symbols.
       Matches standard card template: category bar + draw-it box + word + POS label.
       NO definitions on cards per CbD standard.
    """
    # (word, fk_key) — no definitions on cards
    LABEL_WORDS = [
        ("figurative language", "white"),
        ("metaphor",            "white"),
        ("imagery",             "white"),
        ("tone",                "white"),
        ("pretend",             "green"),
    ]

    FK_STYLES = {
        "white": {"bar": colors.HexColor("#F5F5F5"), "dot": colors.HexColor("#8B6914"),
                  "border": colors.HexColor("#8B6914"), "word": colors.HexColor("#6B4F10"),
                  "label": "NOUNS"},
        "green": {"bar": colors.HexColor("#E8F5E9"), "dot": colors.HexColor("#00A86B"),
                  "border": colors.HexColor("#2E7D32"), "word": colors.HexColor("#2E7D32"),
                  "label": "ACTIONS"},
    }

    CARD_W = 3.0 * inch

    story = [hdr(), Spacer(1, 0.06*inch)]
    story.append(sec_bar("TEXT-LABEL CARDS — Print, Cut, and Laminate"))
    story.append(Spacer(1, 0.06*inch))
    story.append(Paragraph(
        "These 5 vocabulary words are abstract literary terms without clear picture symbols. "
        "Print on cardstock, cut along borders, laminate. Use for choice boards and pre-teach reference. "
        "Teach meaning explicitly before each poem — do not rely on the card as a definition.", BODY))
    story.append(Spacer(1, 0.08*inch))

    def label_card(word, fk):
        st = FK_STYLES[fk]
        cat_style = ParagraphStyle("lcs", fontName="Helvetica-Bold", fontSize=7,
            textColor=colors.HexColor("#666666"), leading=10)
        word_style = ParagraphStyle("lws", fontName="Helvetica-Bold", fontSize=15,
            textColor=st["word"], leading=19, alignment=TA_CENTER)
        pos_style  = ParagraphStyle("lps", fontName="Helvetica", fontSize=7,
            textColor=colors.HexColor("#888888"), leading=9, alignment=TA_CENTER)
        draw_style = ParagraphStyle("ldr", fontName="Helvetica", fontSize=7,
            textColor=colors.HexColor("#AAAAAA"), leading=9, alignment=TA_RIGHT)

        # Zone 1 — category bar
        cat_bar = Table([[Paragraph(f"● {st['label']}", cat_style)]], colWidths=[CARD_W - 12])
        cat_bar.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,-1), st["bar"]),
            ("TOPPADDING",(0,0),(-1,-1),4), ("BOTTOMPADDING",(0,0),(-1,-1),4),
            ("LEFTPADDING",(0,0),(-1,-1),8), ("RIGHTPADDING",(0,0),(-1,-1),4),
        ]))

        # Zone 2 — empty drawing box with "draw it ✏" (matches template for missing symbols)
        draw_box = Table([[Paragraph("draw it ✏", draw_style)]], colWidths=[CARD_W - 16])
        draw_box.setStyle(TableStyle([
            ("BOX",(0,0),(-1,-1), 2.5, st["border"]),
            ("ALIGN",(0,0),(-1,-1),"RIGHT"),
            ("VALIGN",(0,0),(-1,-1),"TOP"),
            ("TOPPADDING",(0,0),(-1,-1), 48),
            ("BOTTOMPADDING",(0,0),(-1,-1), 48),
            ("LEFTPADDING",(0,0),(-1,-1), 6),
            ("RIGHTPADDING",(0,0),(-1,-1), 8),
        ]))

        # Zone 3 — word + POS label (NO definitions)
        word_zone = Table([[
            [Paragraph(word.upper(), word_style),
             Paragraph(st["label"], pos_style)]
        ]], colWidths=[CARD_W - 12])
        word_zone.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,-1), colors.HexColor("#FAFAFA")),
            ("ALIGN",(0,0),(-1,-1),"CENTER"),
            ("TOPPADDING",(0,0),(-1,-1),4), ("BOTTOMPADDING",(0,0),(-1,-1),4),
            ("LEFTPADDING",(0,0),(-1,-1),4), ("RIGHTPADDING",(0,0),(-1,-1),4),
        ]))

        card = Table([[cat_bar], [draw_box], [word_zone]], colWidths=[CARD_W])
        card.setStyle(TableStyle([
            ("BOX",(0,0),(-1,-1), 0.5, colors.HexColor("#DDDDDD")),
            ("LEFTPADDING",(0,0),(-1,-1),6), ("RIGHTPADDING",(0,0),(-1,-1),6),
            ("TOPPADDING",(0,0),(-1,-1),0), ("BOTTOMPADDING",(0,0),(-1,-1),0),
        ]))
        return card

    # 2-column grid
    cards = [label_card(w, fk) for w, fk in LABEL_WORDS]
    rows = []
    for i in range(0, len(cards), 2):
        row = [cards[i], cards[i+1] if (i+1) < len(cards) else Spacer(3.0*inch, 1)]
        rows.append(row)

    grid = Table(rows, colWidths=[3.5*inch, 3.5*inch])
    grid.setStyle(TableStyle([
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("TOPPADDING",(0,0),(-1,-1),5), ("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),5), ("RIGHTPADDING",(0,0),(-1,-1),5),
    ]))
    story.append(grid)
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(
        "Symbol borders follow the Fitzgerald Key color system. Teach word meaning explicitly before each poem session. "
        "ARASAAC symbols © ARASAAC — CC BY-NC-ND 4.0.", SML))
    story.append(Spacer(1, 0.06*inch))
    story.append(foot())
    return story

# ── Page 8: Response Core Vocabulary ─────────────────────────────────────────
def page_response_core():
    story = [hdr(), Spacer(1, 0.1*inch)]
    story.append(sec_bar("RESPONSE CORE VOCABULARY"))
    story.append(Spacer(1, 0.08*inch))
    story.append(Paragraph(
        "These 13 core words are the standard response vocabulary for all CbD products. "
        "They are already on most robust AAC systems. Students who have used CbD nonfiction units "
        "arrive at poetry already fluent with this response vocabulary — the pathway is built.", BODY))
    story.append(Spacer(1, 0.1*inch))

    core_styled = [ParagraphStyle("cw", fontName="Helvetica-Bold", fontSize=16,
        textColor=NAVY, leading=20, alignment=TA_CENTER)]
    note_style  = ParagraphStyle("cn", fontName="Helvetica", fontSize=8,
        textColor=SLATE, leading=11, alignment=TA_CENTER)

    core_rows = [RESPONSE_CORE[i:i+4] for i in range(0, len(RESPONSE_CORE), 4)]
    tbl_rows = []
    for row_words in core_rows:
        row_cells = []
        for w in row_words:
            c = Table([[Paragraph(w, core_styled[0])]], colWidths=[1.55*inch])
            c.setStyle(TableStyle([
                ("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#F0E8FF")),
                ("BOX",(0,0),(-1,-1),1.5,VIOLET),
                ("ALIGN",(0,0),(-1,-1),"CENTER"),
                ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                ("TOPPADDING",(0,0),(-1,-1),8),
                ("BOTTOMPADDING",(0,0),(-1,-1),8),
            ]))
            row_cells.append(c)
        while len(row_cells) < 4:
            row_cells.append(Spacer(1.55*inch, 1))
        tbl_rows.append(row_cells)

    grid = Table(tbl_rows, colWidths=[1.7*inch, 1.7*inch, 1.7*inch, 1.7*inch])
    grid.setStyle(TableStyle([
        ("TOPPADDING",(0,0),(-1,-1),4),
        ("BOTTOMPADDING",(0,0),(-1,-1),4),
        ("LEFTPADDING",(0,0),(-1,-1),4),
        ("RIGHTPADDING",(0,0),(-1,-1),4),
    ]))
    story.append(grid)
    story.append(Spacer(1, 0.12*inch))

    story.append(callout_box(
        "<b>Motor pathway note:</b> The same 13 response words appear in all CbD nonfiction and poetry units. "
        "Students build a stable motor route to these words across units. Do not change the location of "
        "core words on the device when adding unit fringe vocabulary — navigate to fringe from the same access path."))
    story.append(Spacer(1, 0.12*inch))

    story.append(Paragraph("<b>ALgS reminder for all team members:</b>", BOLD))
    story.append(Paragraph(
        "Aided Language Stimulation (ALgS) means the partner points to or selects the target word on the AAC system "
        "at the same moment they say it aloud. At every NFMA prompt, model at minimum: <b>the unit fringe word + because</b>. "
        "Do this even when the student does not respond. Model without expectation.", BODY))
    story.append(Spacer(1, 0.15*inch))
    story.append(foot())
    return story

# ── Page 9: Partner Quick Reference ──────────────────────────────────────────
def page_partner_reference():
    story = [hdr(), Spacer(1, 0.06*inch)]
    story.append(sec_bar("PARTNER QUICK REFERENCE — NFMA Partner Moves"))
    story.append(Spacer(1, 0.06*inch))
    story.append(Paragraph(
        "Keep this page visible during every poetry session. "
        "These moves apply at all three versions (V1/V2/V3).", BODY))
    story.append(Spacer(1, 0.08*inch))

    story.append(Paragraph("<b>The 4 Partner Behaviors</b>", H2))
    behav_rows = [
        ["MODEL", "At each NFMA prompt, point to the target word on the AAC system while saying it. "
                  "Model: figurative language + tone + because. Do this before the student responds, not after."],
        ["WAIT",  "After any prompt or model, wait a full 5 seconds in silence. "
                  "Count silently: 1 Mississippi… 2 Mississippi… 3 Mississippi… 4 Mississippi… 5 Mississippi. "
                  "Do not redirect, fill in, or restate the prompt during the wait."],
        ["EXPAND","When the student responds, add 1–2 more words to their utterance. "
                  "If student indicates 'sad' → partner says and models: 'sad because hiding.' "
                  "Expansion is not correction — it is language modeling."],
        ["OFFER CHOICE", "If the student does not respond after 5 seconds: "
                  "offer a reduced choice field (2 options, not more). "
                  "Example: 'Is it a metaphor or imagery?' Point to each option on the device or a text card."],
    ]
    b_tbl = Table(behav_rows, colWidths=[1.0*inch, 6.0*inch])
    b_tbl.setStyle(TableStyle([
        ("FONTNAME",(0,0),(0,-1),"Helvetica-Bold"),
        ("FONTSIZE",(0,0),(0,-1),9),
        ("TEXTCOLOR",(0,0),(0,-1),VIOLET),
        ("FONTNAME",(1,0),(1,-1),"Helvetica"),
        ("FONTSIZE",(1,0),(1,-1),9),
        ("TEXTCOLOR",(1,0),(1,-1),NAVY),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("TOPPADDING",(0,0),(-1,-1),6),
        ("BOTTOMPADDING",(0,0),(-1,-1),6),
        ("LEFTPADDING",(0,0),(-1,-1),4),
        ("RIGHTPADDING",(0,0),(-1,-1),4),
        ("LINEBELOW",(0,0),(-1,-2),0.5,MGRAY),
        ("BOX",(0,0),(-1,-1),0.75,MGRAY),
    ]))
    story.append(b_tbl)
    story.append(Spacer(1, 0.12*inch))

    story.append(Paragraph("<b>NFMA Prompt Guide — What to say and model at each step</b>", H2))
    nfma_rows = [
        [Paragraph("<b>N</b>\nNOTICE", ParagraphStyle("ns", fontName="Helvetica-Bold",
            fontSize=10, textColor=WHITE, leading=13, alignment=TA_CENTER)),
         Paragraph(
            "<b>Say:</b> \"Which words in this poem stand out? Show me.\"\n"
            "<b>Model on device:</b> <i>figurative language</i> or <i>imagery</i> or <i>metaphor</i>\n"
            "<b>After 5 sec:</b> offer 2 options — point to two specific lines in the poem", BODY)],
        [Paragraph("<b>F</b>\nFEEL", ParagraphStyle("fs2", fontName="Helvetica-Bold",
            fontSize=10, textColor=WHITE, leading=13, alignment=TA_CENTER)),
         Paragraph(
            "<b>Say:</b> \"What feeling does this part of the poem create?\"\n"
            "<b>Model on device:</b> <i>tone</i> + a feeling word (sad, proud, tired, strong)\n"
            "<b>After 5 sec:</b> offer a choice board of 4 feelings — point to each one", BODY)],
        [Paragraph("<b>M</b>\nMEAN", ParagraphStyle("ms", fontName="Helvetica-Bold",
            fontSize=10, textColor=WHITE, leading=13, alignment=TA_CENTER)),
         Paragraph(
            "<b>Say:</b> \"What is the poet really saying here?\"\n"
            "<b>Model on device:</b> <i>mean</i> + <i>because</i>\n"
            "<b>V3:</b> offer 3 printed options — 2 interpretive, 1 distractor — point to each; "
            "after selection, ask: \"Why?\" and frame: 'I chose ___ because ___.'", BODY)],
        [Paragraph("<b>A</b>\nASK", ParagraphStyle("as2", fontName="Helvetica-Bold",
            fontSize=10, textColor=WHITE, leading=13, alignment=TA_CENTER)),
         Paragraph(
            "<b>Say:</b> \"What question does this poem raise for you? Use 'I wonder _____.'\"\n"
            "<b>Then say:</b> \"Can you show me a line in the poem that begins to answer it?\"\n"
            "<b>V3:</b> Student points to or taps the line — this counts as citing evidence. "
            "Partner says the line aloud and writes it down.", BODY)],
    ]

    col_styles = [
        ParagraphStyle("n_lbl", fontName="Helvetica-Bold", fontSize=10,
            textColor=WHITE, leading=13, alignment=TA_CENTER),
    ]

    nfma_tbl = Table(nfma_rows, colWidths=[0.75*inch, 6.25*inch])
    nfma_style = [
        ("FONTNAME",(0,0),(-1,-1),"Helvetica"),
        ("FONTSIZE",(0,0),(-1,-1),9),
        ("TEXTCOLOR",(0,0),(-1,-1),NAVY),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("TOPPADDING",(0,0),(-1,-1),8),
        ("BOTTOMPADDING",(0,0),(-1,-1),8),
        ("LEFTPADDING",(0,0),(-1,-1),6),
        ("RIGHTPADDING",(0,0),(-1,-1),6),
        ("LINEBELOW",(0,0),(-1,-2),0.5,MGRAY),
        ("BOX",(0,0),(-1,-1),0.75,MGRAY),
        ("BACKGROUND",(0,0),(0,-1),VIOLET),
    ]
    nfma_tbl.setStyle(TableStyle(nfma_style))
    story.append(nfma_tbl)
    story.append(Spacer(1, 0.12*inch))
    story.append(foot())
    return story

# ── Page 10: IEP Goal Stems ───────────────────────────────────────────────────
def page_iep_goals():
    story = [hdr(), Spacer(1, 0.1*inch)]
    story.append(sec_bar("IEP GOAL STEMS"))
    story.append(Spacer(1, 0.08*inch))
    story.append(Paragraph(
        "These are model goal stems — starting points for IEP teams, not compliance guarantees. "
        "Insert student name, IEP date, and adjust criterion as appropriate for the individual student. "
        "Goals are framed as accommodations: same standard, different access.", BODY))
    story.append(Spacer(1, 0.1*inch))

    story.append(Paragraph("<b>Academic Goal — RL.6.4 / L.5.5 (Figurative Language in Poetry)</b>", H2))
    story.append(callout_box(
        "Given a short poem with at least one example of figurative language (metaphor or imagery), "
        "[student name] will <b>identify</b> the figurative language and <b>explain</b> its effect on meaning or tone "
        "using a sentence frame and their AAC system, achieving 80% accuracy across 3 consecutive trials "
        "as measured by the CbD unit rubric, by [IEP date]."))
    story.append(Spacer(1, 0.08*inch))
    goal1_rows = [
        ["Observable verbs:",  "identify, explain"],
        ["IDEA compliance:",   "Same standard as non-disabled peers; scaffold = access, not modification"],
        ["Measurement tool:", "CbD unit rubric (3-level: Does Not Yet Meet / Approaching / Meets)"],
        ["Mastery criteria:",  "80% accuracy across 3 consecutive trials, generalized across 2+ partners"],
        ["IEP data:",          "'Meets' on Criteria 3 and 4 (interpretive criteria) = mastery on academic goal"],
    ]
    g1_tbl = Table(goal1_rows, colWidths=[1.4*inch, 5.6*inch])
    g1_tbl.setStyle(TableStyle([
        ("FONTNAME",(0,0),(0,-1),"Helvetica-Bold"),
        ("FONTNAME",(1,0),(1,-1),"Helvetica"),
        ("FONTSIZE",(0,0),(-1,-1),9),
        ("TEXTCOLOR",(0,0),(-1,-1),NAVY),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("TOPPADDING",(0,0),(-1,-1),4),
        ("BOTTOMPADDING",(0,0),(-1,-1),4),
        ("LEFTPADDING",(0,0),(-1,-1),4),
        ("RIGHTPADDING",(0,0),(-1,-1),4),
        ("LINEBELOW",(0,0),(-1,-2),0.5,MGRAY),
    ]))
    story.append(g1_tbl)
    story.append(Spacer(1, 0.14*inch))

    story.append(Paragraph("<b>AAC Communication Goal</b>", H2))
    story.append(callout_box(
        "Given a partner-read poem and a NFMA response prompt, [student name] will <b>produce</b> a "
        "2–3 symbol utterance that includes at least one fringe literary vocabulary word "
        "(e.g., metaphor, tone, imagery) and one core connector word (e.g., because, same, feel), "
        "with no more than one verbal prompt, across 2 communication partners, achieving 80% accuracy "
        "across 3 consecutive sessions as measured by the CbD Session Tracker, by [IEP date]."))
    story.append(Spacer(1, 0.08*inch))
    goal2_rows = [
        ["Observable verb:",       "produce"],
        ["Measurement tool:",      "CbD Session Tracker (para-administered)"],
        ["Mastery criteria:",       "80% accuracy across 3 consecutive sessions, generalized across 2+ partners"],
        ["Partner requirement:",   "Generalization: special educator + para minimum"],
        ["Note for SLP:",          "Pre-programming due 2 weeks before Day 1. Top 5 priority: figurative language, "
                                    "metaphor, imagery, tone, speaker. All fringe navigable within 2 touches."],
    ]
    g2_tbl = Table(goal2_rows, colWidths=[1.4*inch, 5.6*inch])
    g2_tbl.setStyle(TableStyle([
        ("FONTNAME",(0,0),(0,-1),"Helvetica-Bold"),
        ("FONTNAME",(1,0),(1,-1),"Helvetica"),
        ("FONTSIZE",(0,0),(-1,-1),9),
        ("TEXTCOLOR",(0,0),(-1,-1),NAVY),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("TOPPADDING",(0,0),(-1,-1),4),
        ("BOTTOMPADDING",(0,0),(-1,-1),4),
        ("LEFTPADDING",(0,0),(-1,-1),4),
        ("RIGHTPADDING",(0,0),(-1,-1),4),
        ("LINEBELOW",(0,0),(-1,-2),0.5,MGRAY),
    ]))
    story.append(g2_tbl)
    story.append(Spacer(1, 0.14*inch))

    story.append(Paragraph("<b>Modification Flag</b>", H2))
    story.append(callout_box(
        "If a student is working toward an alternate achievement standard and identification only (Criteria 1–2) "
        "is the IEP target, document this explicitly in the IEP. Do not use this unit's rubric language to describe "
        "that student's performance — they are working toward a different standard, not failing this one.",
        bg=colors.HexColor("#FFF3CD")))
    story.append(Spacer(1, 0.12*inch))
    story.append(Paragraph(
        "<b>About Communicate by Design:</b> CbD builds special education instructional resources with AAC access built in at every layer. "
        "Products are designed by a special educator and advocate. "
        "All CbD products target WCAG 2.2 Level AA accessibility.", SML))
    story.append(Spacer(1, 0.06*inch))
    story.append(Paragraph(
        "© Communicate by Design · communicatebydesign.substack.com · " + STORE, FOOT))
    story.append(Spacer(1, 0.04*inch))
    story.append(foot())
    return story

# ── Build ─────────────────────────────────────────────────────────────────────
def build():
    buf = io.BytesIO()
    c = rl_canvas.Canvas(buf, pagesize=letter)
    build_cover(c)
    c.save()
    cover_bytes = buf.getvalue()

    # Inner pages via Flowables
    inner_buf = io.BytesIO()
    doc = make_doc(inner_buf)

    all_pages = (
        page_how_to_use()       + [PageBreak()] +
        page_slp_checklist()    + [PageBreak()] +
        page_fringe_table()     + [PageBreak()] +
        page_symbol_cards()     + [PageBreak()] +
        page_text_label_cards() + [PageBreak()] +
        page_response_core()    + [PageBreak()] +
        page_partner_reference()+ [PageBreak()] +
        page_iep_goals()
    )
    doc.build(all_pages)
    inner_bytes = inner_buf.getvalue()

    # Merge cover + inner pages + shared AAC Session Tracker (roll-up to standard data collection)
    from pypdf import PdfReader, PdfWriter
    SHARED_TRACKER = os.path.join(
        BASE, "..", "..", "Nonfiction Units", "AAC_Communication_Session_Tracker.pdf"
    )
    writer = PdfWriter()
    sources = [
        PdfReader(io.BytesIO(cover_bytes)),
        PdfReader(io.BytesIO(inner_bytes)),
    ]
    if os.path.exists(SHARED_TRACKER):
        sources.append(PdfReader(SHARED_TRACKER))
    else:
        print(f"⚠️  Shared tracker not found at: {SHARED_TRACKER}")
        print("   CAP built without roll-up tracker. Add manually after build.")
    for reader in sources:
        for page in reader.pages:
            writer.add_page(page)
    writer.add_metadata({
        "/Title": "What the Voice Carries — Communication Access Packet",
        "/Author": "Communicate by Design — Jill McCardel",
        "/Subject": "Poetry Reading Units · Unit 1 · CAP",
    })
    with open(OUT, "wb") as f:
        writer.write(f)

    import os as _os
    size_kb = _os.path.getsize(OUT) / 1024
    from pypdf import PdfReader as PR
    pages = len(PR(OUT).pages)
    print(f"CAP created: {OUT}")
    print(f"Size: {size_kb:.1f} KB  ·  Pages: {pages}")

if __name__ == "__main__":
    build()

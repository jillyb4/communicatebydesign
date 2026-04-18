"""
Rules: Identity and Belonging — Fiction Printable Packet
Communicate by Design

Builds: Rules_Identity_and_Belonging_Printable_Packet.pdf
Spec:   _Operations/memory/fiction_printable_packet_spec.md

Structure:
  p1       Layer 1  — Communication Environment Setup
  p2       Layer 2  — Core word symbol cards (Set A, 12 words, 3×4 grid)
  p3       Layer 2  — Fringe word symbol cards (Set A, 12 words, chapter order)
  p4       Layer 3  — Board A: Character Description Board (landscape)
                      Categories: LOOKS LIKE / DOES / FEELS / WANTS
                      Characters: Catherine, Jason
  p5       Layer 3  — Board B: Emotion + Belonging (portrait)
                      Emotional vocab + belonging connectors
  p6       Layer 3  — Board C: Literary Discussion Moves (portrait)
                      [RULE] / [BELONG] / [CHANGE] annotation codes
  p7       Layer 4a — Unit Vocabulary Map
  p8–9     Layer 4b — AAC Session Tracker (appended unchanged)
  p10      Layer 5  — Student Response: Part 1 — The Rules
  p11      Layer 5  — Student Response: Part 2 — Meeting Jason
  p12      Layer 5  — Student Response: Part 3 — Rules Break Down
  p13      Layer 5  — Student Response: Part 4 — What Catherine Learns
  p14      Layer 5  — Student Response: Part 5 — Whole-Book Synthesis

Symbol notes:
  rule      → arasaac_law.png     (law = rule — closest available)
  belong    → arasaac_include.png (include = belong — locked symbol sub)
  normal    → arasaac_same.png    (same = normal — closest available)
  honest    → arasaac_honest.png  (verified present)
  proud     → arasaac_proud.png   (verified present)
  brave     → arasaac_brave.png   (verified present)
  clinic    → None                (draw-your-own placeholder)
  word card → None                (draw-your-own — AAC-specific)
  embarrassed→ arasaac_embarrassed.png (if present) else draw-your-own
  Catherine → None                (proper noun — draw-your-own)
  Jason     → None                (proper noun — draw-your-own)
"""

import os, io, textwrap
from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter, landscape as rl_landscape
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.platypus.flowables import Image as RLImage

# ── Paths ─────────────────────────────────────────────────────────────────────

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MNT        = os.path.join(SCRIPT_DIR, "..", "..", "..", "..")  # Communicate by Design/
SYM_CACHE  = os.path.join(MNT, "_Operations/Symbols/symbol_cache")
TRACKER    = os.path.join(MNT, "_Operations/_Shared_Inserts/AAC_Communication_Session_Tracker.pdf")
OUT_PATH   = os.path.join(SCRIPT_DIR, "..", "Product Files",
                           "Rules_Identity_and_Belonging_Printable_Packet.pdf")

UNIT_TITLE = "Rules: Identity and Belonging"

# ── Brand colors ──────────────────────────────────────────────────────────────

NAVY  = colors.HexColor("#1B1F3B")
TEAL  = colors.HexColor("#006DA0")
AMBER = colors.HexColor("#FFB703")
SLATE = colors.HexColor("#94A3B8")
WHITE = colors.white

# ── Fitzgerald Key ─────────────────────────────────────────────────────────────

FK_BG = {
    "green":  colors.HexColor("#E8F5E9"),
    "orange": colors.HexColor("#FFF3E0"),
    "yellow": colors.HexColor("#FFF8DC"),
    "brown":  colors.HexColor("#FFF5D6"),
    "blue":   colors.HexColor("#E3F2FD"),
    "pink":   colors.HexColor("#FCE4EC"),
    "white":  colors.HexColor("#F5F5F5"),
}
FK_BORDER = {
    "green":  colors.HexColor("#00A86B"),
    "orange": colors.HexColor("#FF8C00"),
    "yellow": colors.HexColor("#D4A800"),
    "brown":  colors.HexColor("#8B6914"),
    "blue":   colors.HexColor("#4A90D9"),
    "pink":   colors.HexColor("#E88CA5"),
    "white":  colors.HexColor("#AAAAAA"),
}

# ── Fitzgerald category per word ──────────────────────────────────────────────

WORD_FK = {
    # Set A Core — 12 words
    "belong":    "green",   # verb
    "want":      "green",   # verb
    "feel":      "green",   # verb
    "think":     "green",   # verb
    "know":      "green",   # verb
    "change":    "green",   # verb
    "choose":    "green",   # verb
    "same":      "orange",  # description
    "different": "orange",  # description
    "hide":      "green",   # verb
    "fair":      "orange",  # description
    "because":   "blue",    # connector/little word
    # Set A Fringe — 12 words
    "normal":      "orange",  # description
    "rule":        "brown",   # noun
    "clinic":      "brown",   # noun
    "word card":   "brown",   # noun (Jason's AAC)
    "embarrassed": "pink",    # feeling/description
    "honest":      "orange",  # description
    "Catherine":   "yellow",  # person
    "Jason":       "yellow",  # person
    "David":       "yellow",  # person
    "Kristi":      "yellow",  # person
    "proud":       "orange",  # description
    "brave":       "orange",  # description
    # Boards extra vocabulary
    "sad":       "pink",    "scared":    "pink",    "happy":    "pink",
    "angry":     "pink",    "confused":  "orange",  "worried":  "pink",
    "alone":     "orange",  "together":  "orange",  "okay":     "orange",
    "real":      "orange",  "free":      "orange",
    "i think":   "white",   "i feel":    "white",
    "i agree":   "white",   "i disagree":"white",
    "the character shows": "white",
    "the evidence shows":  "white",
    "on page":   "white",   "the author says": "white",
    "this shows":"white",   "the character":   "yellow",
    "[rule]":    "brown",   "[belong]":  "green",   "[change]": "orange",
}

def fk(word):
    return WORD_FK.get(word.lower(), "white")

# ── Symbol path lookup ────────────────────────────────────────────────────────

SYMBOL_FILE = {
    # Set A Core
    "belong":    "arasaac_include.png",        # ★ locked sub: belong → include
    "want":      "arasaac_want.png",
    "feel":      "arasaac_feel.png",
    "think":     "arasaac_think.png",
    "know":      "arasaac_know.png",
    "change":    "arasaac_change.png",
    "choose":    "arasaac_choose.png",
    "same":      "arasaac_same.png",
    "different": "arasaac_different.png",
    "hide":      "arasaac_hide.png",
    "fair":      "arasaac_fair.png",
    "because":   "arasaac_because.png",
    # Set A Fringe — chapter order
    "normal":      "arasaac_same.png",         # ★ same = normal (closest available)
    "rule":        "arasaac_law.png",           # ★ law = rule (closest available)
    "clinic":      None,                        # draw-your-own
    "word card":   None,                        # draw-your-own (AAC-specific)
    "embarrassed": "arasaac_embarrassed.png",   # verify present; else draw-your-own
    "honest":      "arasaac_honest.png",
    "Catherine":   None,                        # proper noun — draw-your-own
    "Jason":       None,                        # proper noun — draw-your-own
    "David":       None,                        # proper noun — draw-your-own
    "Kristi":      None,                        # proper noun — draw-your-own
    "proud":       "arasaac_proud.png",
    "brave":       "arasaac_brave.png",
    # Board extras
    "sad":       "arasaac_sad.png",
    "scared":    "arasaac_scared.png",
    "happy":     "arasaac_happy.png",
    "angry":     "arasaac_mad.png",            # ★ mad = angry
    "confused":  "arasaac_confused.png",
    "worried":   "arasaac_worried.png",
    "alone":     "arasaac_alone_7253.png",
    "together":  "arasaac_together.png",
    "okay":      "arasaac_okay.png",
    "real":      "arasaac_real.png",
    "free":      "arasaac_free.png",
    "agree":     "arasaac_agree.png",
    "disagree":  "arasaac_disagree.png",
    "page":      "arasaac_page.png",
    "show":      "arasaac_show.png",
    "tell":      "arasaac_tell.png",
}

def sym_path(word):
    fname = SYMBOL_FILE.get(word.lower())
    if fname is None:
        return None   # explicit draw-your-own
    if fname:
        p = os.path.join(SYM_CACHE, fname)
        return p if os.path.exists(p) else None
    # Fallback
    p = os.path.join(SYM_CACHE, f"arasaac_{word.lower().replace(' ', '_')}.png")
    return p if os.path.exists(p) else None

# ── Running header + footer ────────────────────────────────────────────────────

def header_flowable():
    hl = ParagraphStyle("hl", fontName="Helvetica-Oblique",
        fontSize=9, textColor=NAVY, leading=13)
    hr = ParagraphStyle("hr", fontName="Helvetica-Bold",
        fontSize=9, leading=13, alignment=TA_RIGHT)
    t = Table([[
        Paragraph(f"<i>{UNIT_TITLE}</i>", hl),
        Paragraph(
            "<font color='#006DA0'><b>COMMUNICATE</b></font>"
            " <font color='#FFB703'><b>BY DESIGN</b></font>", hr),
    ]], colWidths=[4.5*inch, 2.5*inch])
    t.setStyle(TableStyle([
        ("VALIGN", (0,0),(-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0),(-1,-1), 0),
        ("BOTTOMPADDING", (0,0),(-1,-1), 3),
        ("LEFTPADDING", (0,0),(-1,-1), 0),
        ("RIGHTPADDING", (0,0),(-1,-1), 0),
    ]))
    return t

def footer_text():
    return (f"{UNIT_TITLE}  ·  Fiction Printable Packet  ·  "
            "Communicate by Design  ·  teacherspayteachers.com/store/communicate-by-design")

def footer_flowable():
    fs = ParagraphStyle("fs", fontName="Helvetica", fontSize=7,
        textColor=SLATE, leading=9, alignment=TA_CENTER)
    return Paragraph(footer_text(), fs)

# ─────────────────────────────────────────────────────────────────────────────
# LAYER 1 — Communication Environment Setup
# ─────────────────────────────────────────────────────────────────────────────

def build_layer1_pdf() -> bytes:
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter,
        leftMargin=0.55*inch, rightMargin=0.55*inch,
        topMargin=0.35*inch, bottomMargin=0.35*inch)

    H1   = ParagraphStyle("h1", fontName="Helvetica-Bold",
        fontSize=12, textColor=NAVY, leading=15, spaceAfter=3)
    H2   = ParagraphStyle("h2", fontName="Helvetica-Bold",
        fontSize=9, textColor=TEAL, leading=12, spaceBefore=5, spaceAfter=2)
    BODY = ParagraphStyle("body", fontName="Helvetica",
        fontSize=8, textColor=NAVY, leading=11, spaceAfter=2)
    WARN = ParagraphStyle("warn", fontName="Helvetica-Oblique",
        fontSize=7.5, textColor=colors.HexColor("#B45309"), leading=10,
        borderColor=colors.HexColor("#FDE68A"),
        borderWidth=1, borderPadding=(3,5,3,5),
        backColor=colors.HexColor("#FFFBEB"), spaceAfter=4)
    LABEL = ParagraphStyle("label", fontName="Helvetica-Bold",
        fontSize=8.5, textColor=NAVY, leading=12)
    SMALL = ParagraphStyle("small", fontName="Helvetica",
        fontSize=7.5, textColor=NAVY, leading=10)

    story = [header_flowable(),
             HRFlowable(width="100%", thickness=1.5, color=TEAL, spaceAfter=5)]

    story.append(Paragraph(
        "Communication Environment Setup  —  Print once. Laminate. Keep in hand during instruction.", H1))

    # ── Partner Modes ─────────────────────────────────────────────────────────
    story.append(Paragraph("PARTNER MODE GUIDE", H2))
    story.append(Paragraph(
        "<b>⚠️ Defaulting to Mode 1 all day is the #1 AAC barrier. "
        "Most partners were never taught when to switch modes.</b>", WARN))

    mode_data = [
        [Paragraph("<b>Mode 1: Instructional</b>", LABEL),
         Paragraph("Use prompt hierarchy + collect data. "
                   "<b>Use during:</b> targeted communication skill instruction.", SMALL)],
        [Paragraph("<b>Mode 2: Partnership</b>", LABEL),
         Paragraph("No demands. Follow student lead. Note spontaneous communications. "
                   "<b>Use during:</b> shared reading of Rules, discussion, text exploration. "
                   "NEVER use Mode 1 during the novel read.", SMALL)],
        [Paragraph("<b>Mode 3: Facilitated Participation</b>", LABEL),
         Paragraph("Enable access only — do not interpret or prompt. "
                   "<b>Use during:</b> student engaging independently with text.", SMALL)],
    ]
    mode_table = Table(mode_data, colWidths=[1.9*inch, 5.3*inch])
    mode_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (0,-1), colors.HexColor("#EFF6FF")),
        ("BACKGROUND", (1,0), (1,-1), colors.white),
        ("BOX", (0,0), (-1,-1), 1, TEAL),
        ("INNERGRID", (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 3),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
        ("LEFTPADDING", (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
    ]))
    story.append(mode_table)

    # ── Jason's Communication Book Note ──────────────────────────────────────
    story.append(Paragraph("JASON'S WORD CARDS — A NOTE BEFORE YOU BEGIN", H2))
    story.append(Paragraph(
        "<b>Jason communicates using word cards — a form of low-tech AAC. "
        "This is a complete communication system, not a limitation.</b> "
        "When reading Rules aloud, give Jason's communications full wait time. "
        "When a student uses any AAC system during discussion, treat their output "
        "the same way you treat Jason's: as complete, intentional communication. "
        "Do not interpret, fill in, or rush. Partner records. Student leads.", BODY))

    # ── Prompt Hierarchy ─────────────────────────────────────────────────────
    story.append(Paragraph("PROMPT HIERARCHY  —  Mode 1 Only", H2))

    ph_data = [
        ["1", "Wait", "3–5 seconds minimum. No talking. Watch for any communication."],
        ["2", "Indirect Cue", "Gesture toward communication system without speaking."],
        ["3", "Direct Cue", "Point to specific symbol or location on the system."],
        ["4", "Verbal Model", "Say the word AND show it on the system simultaneously."],
        ["5", "Reassess Access",
         "Non-response = environment data, not intent failure. Check barrier list before continuing."],
    ]
    ph_styles = [
        ParagraphStyle("phn", fontName="Helvetica-Bold", fontSize=10,
            textColor=WHITE, leading=13, alignment=TA_CENTER),
        ParagraphStyle("phl", fontName="Helvetica-Bold", fontSize=8.5,
            textColor=NAVY, leading=11),
        ParagraphStyle("phd", fontName="Helvetica", fontSize=8,
            textColor=NAVY, leading=11),
    ]
    ph_rows = []
    bg_colors = ["#1B1F3B","#1E4B7B","#1E5A8A","#006DA0","#007DB0"]
    for i, (num, lbl, desc) in enumerate(ph_data):
        ph_rows.append([
            Paragraph(num, ph_styles[0]),
            Paragraph(lbl, ph_styles[1]),
            Paragraph(desc, ph_styles[2]),
        ])
    ph_table = Table(ph_rows, colWidths=[0.35*inch, 1.4*inch, 5.45*inch])
    ph_ts = [
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LEFTPADDING", (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("BOX", (0,0), (-1,-1), 1, NAVY),
        ("INNERGRID", (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
    ]
    for i, hex_col in enumerate(bg_colors):
        ph_ts.append(("BACKGROUND", (0,i), (0,i), colors.HexColor(hex_col)))
        ph_ts.append(("TEXTCOLOR", (0,i), (0,i), WHITE))
    ph_table.setStyle(TableStyle(ph_ts))
    story.append(ph_table)

    # ── Barrier Check ──────────────────────────────────────────────────────────
    story.append(Paragraph("BARRIER CHECK  —  Circle Before Each Session", H2))

    barrier_items = [
        "Wait time given?",
        "Student positioned for their access method?",
        "Lighting adequate for symbol visibility?",
        "Access method available and within reach?",
        "Symbols and board positioned correctly?",
    ]
    b_style = ParagraphStyle("bs", fontName="Helvetica", fontSize=8,
        textColor=NAVY, leading=11)
    b_yn = ParagraphStyle("byn", fontName="Helvetica-Bold", fontSize=7.5,
        textColor=TEAL, leading=10)
    b_rows = []
    for item in barrier_items:
        b_rows.append([Paragraph(item, b_style), Paragraph("○ Yes   ○ No", b_yn)])
    b_table = Table(b_rows, colWidths=[4.5*inch, 1.4*inch])
    b_table.setStyle(TableStyle([
        ("BOX", (0,0), (-1,-1), 1, TEAL),
        ("INNERGRID", (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 2),
        ("BOTTOMPADDING", (0,0), (-1,-1), 2),
        ("LEFTPADDING", (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 4),
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
    ]))
    story.append(b_table)

    # ── Tools in this packet ──────────────────────────────────────────────────
    story.append(Paragraph("TOOLS IN THIS PACKET", H2))
    t_row_style = ParagraphStyle("trs", fontName="Helvetica", fontSize=7.5,
        textColor=NAVY, leading=10)
    t_lbl_style = ParagraphStyle("tls", fontName="Helvetica-Bold", fontSize=7.5,
        textColor=NAVY, leading=10)
    tools_compact = [
        ("p.2", "Core Word Symbol Cards (12 words)",
         "SDI targets — confirm with AAC team before adding to device"),
        ("p.3", "Fringe Word Symbol Cards (12 words)",
         "Chapter order — includes proper nouns (Catherine, Jason, David, Kristi)"),
        ("p.4", "Board A — Character Description Board",
         "LOOKS LIKE / DOES / FEELS / WANTS for Catherine and Jason — use Parts 1–4"),
        ("p.5", "Board B — Emotion + Belonging",
         "Emotional vocab + belonging connectors — use throughout"),
        ("p.6", "Board C — Literary Discussion Moves",
         "Discussion + evidence + [RULE][BELONG][CHANGE] annotation codes"),
        ("p.7", "Vocabulary Map",
         "Unit-wide library tracker — fill team-wide, not per session"),
        ("p.8–9", "AAC Session Tracker",
         "Print 1 per session — transfer data to unit tracker"),
    ]
    t_rows = []
    for pg, tool, use in tools_compact:
        t_rows.append([
            Paragraph(pg, t_row_style),
            Paragraph(f"<b>{tool}</b>", t_lbl_style),
            Paragraph(use, t_row_style),
        ])
    tools_table = Table(t_rows, colWidths=[0.55*inch, 2.6*inch, 4.1*inch])
    tools_table.setStyle(TableStyle([
        ("ROWBACKGROUNDS", (0,0), (-1,-1),
         [colors.HexColor("#F0F9FF"), colors.white]),
        ("BOX", (0,0), (-1,-1), 1, TEAL),
        ("INNERGRID", (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 2),
        ("BOTTOMPADDING", (0,0), (-1,-1), 2),
        ("LEFTPADDING", (0,0), (-1,-1), 4),
        ("RIGHTPADDING", (0,0), (-1,-1), 4),
        ("ALIGN", (0,0), (0,-1), "CENTER"),
    ]))
    story.append(tools_table)

    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=0.5, color=TEAL, spaceAfter=2))
    story.append(footer_flowable())

    doc.build(story)
    return buf.getvalue()


# ─────────────────────────────────────────────────────────────────────────────
# LAYER 2 — Symbol Cards (Set A, 3×4 grid, 2"×2" cards)
# ─────────────────────────────────────────────────────────────────────────────

# Set A Core — 12 words (Fitzgerald Key category order)
SET_A_CORE = [
    "belong",  "want",    "feel",    "think",   # verbs
    "know",    "change",  "choose",  "hide",    # verbs cont.
    "same",    "different","fair",   "because", # descriptions + connector
]

# Set A Fringe — 12 words (chapter/section order in Rules)
SET_A_FRINGE = [
    "normal",      # Ch. 1   — Catherine's opening desire for a normal summer
    "rule",        # Ch. 1–3 — Catherine's rules notebook; the central motif
    "clinic",      # Ch. 3–4 — where Catherine takes David to occupational therapy
    "word card",   # Ch. 4   — Jason's AAC system; how he communicates
    "embarrassed", # Ch. 5–6 — Catherine's feelings at the clinic
    "honest",      # Ch. 8–9 — Jason asks Catherine to be honest
    "Catherine",   # throughout — protagonist, point-of-view character
    "Jason",       # throughout — AAC user, central relationship
    "David",       # throughout — Catherine's brother
    "Kristi",      # Ch. 10  — the neighbor Catherine wants as a friend
    "proud",       # Ch. 18+ — Catherine becoming proud of Jason
    "brave",       # Ch. 20+ — Catherine choosing to stand by Jason
]


def build_layer2_symbol_cards_pdf(title: str, words: list,
                                   section_note: str = "") -> bytes:
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter,
        leftMargin=0.4*inch, rightMargin=0.4*inch,
        topMargin=0.4*inch, bottomMargin=0.35*inch)

    COLS     = 3
    ROWS     = 4
    CARD_H   = int(2 * inch)
    SYM_SIZE = 88

    word_lbl  = ParagraphStyle("wl",  fontName="Helvetica-Bold",
        fontSize=11, textColor=NAVY, leading=14, alignment=TA_CENTER)
    small_lbl = ParagraphStyle("sl",  fontName="Helvetica-Bold",
        fontSize=9,  textColor=NAVY, leading=11, alignment=TA_CENTER)
    sec_head  = ParagraphStyle("sh",  fontName="Helvetica-Bold",
        fontSize=10.5, textColor=NAVY, leading=14, spaceAfter=3)
    note_style = ParagraphStyle("ns", fontName="Helvetica-Oblique",
        fontSize=7.5, textColor=colors.HexColor("#475569"), leading=10,
        spaceAfter=4, borderColor=TEAL, borderWidth=0.5,
        borderPadding=(3,5,3,5), backColor=colors.HexColor("#F0F9FF"))

    GAP          = 5
    CARD_OUTER_W = (7.7 / 3) * inch
    CARD_INNER_W = CARD_OUTER_W - 2 * GAP
    CARD_INNER_H = CARD_H       - 2 * GAP

    padded = list(words)[:12]
    while len(padded) < 12:
        padded.append("")

    rows_of_words = [padded[r*COLS:(r+1)*COLS] for r in range(ROWS)]

    def make_card(w):
        if not w:
            return Spacer(1, 1)
        cat    = fk(w)
        border = FK_BORDER[cat]
        sp     = sym_path(w)
        lbl_style = small_lbl if len(w) > 10 else word_lbl
        content = []
        if sp:
            content.append(RLImage(sp, width=SYM_SIZE, height=SYM_SIZE))
        else:
            DRAW_SIZE = CARD_INNER_H - 24
            draw_box = Table([[Paragraph("✏", ParagraphStyle(
                "db", fontName="Helvetica", fontSize=22,
                textColor=colors.HexColor("#AAAAAA"),
                alignment=TA_CENTER, leading=DRAW_SIZE * 0.55))]],
                colWidths=[DRAW_SIZE], rowHeights=[DRAW_SIZE])
            draw_box.setStyle(TableStyle([
                ("BACKGROUND",    (0,0), (0,0), colors.white),
                ("BOX",           (0,0), (0,0), 1, colors.HexColor("#AAAAAA")),
                ("ALIGN",         (0,0), (0,0), "CENTER"),
                ("VALIGN",        (0,0), (0,0), "MIDDLE"),
            ]))
            content.append(draw_box)
        content.append(Spacer(1, 3))
        content.append(Paragraph(w.upper(), lbl_style))
        inner = Table([[content]], colWidths=[CARD_INNER_W],
                       rowHeights=[CARD_INNER_H])
        inner.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (0,0), colors.white),
            ("ALIGN",         (0,0), (0,0), "CENTER"),
            ("VALIGN",        (0,0), (0,0), "MIDDLE"),
            ("TOPPADDING",    (0,0), (0,0), 5),
            ("BOTTOMPADDING", (0,0), (0,0), 5),
            ("LEFTPADDING",   (0,0), (0,0), 3),
            ("RIGHTPADDING",  (0,0), (0,0), 3),
            ("BOX",           (0,0), (0,0), 3, border),
        ]))
        return inner

    story = [header_flowable(),
             HRFlowable(width="100%", thickness=1.5, color=TEAL, spaceAfter=4)]
    story.append(Paragraph(title, sec_head))
    if section_note:
        story.append(Paragraph(section_note, note_style))

    grid_data = [[make_card(w) for w in row_words] for row_words in rows_of_words]
    grid = Table(grid_data,
                 colWidths=[CARD_OUTER_W] * COLS,
                 rowHeights=[CARD_H] * ROWS)
    grid.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), colors.white),
        ("ALIGN",         (0,0), (-1,-1), "CENTER"),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",    (0,0), (-1,-1), GAP),
        ("BOTTOMPADDING", (0,0), (-1,-1), GAP),
        ("LEFTPADDING",   (0,0), (-1,-1), GAP),
        ("RIGHTPADDING",  (0,0), (-1,-1), GAP),
    ]))
    story.append(grid)
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=0.5, color=TEAL, spaceAfter=2))
    story.append(footer_flowable())

    doc.build(story)
    return buf.getvalue()


# ─────────────────────────────────────────────────────────────────────────────
# LAYER 3 — Communication Boards (canvas-based)
# ─────────────────────────────────────────────────────────────────────────────

# Board A: Character Description Board (Rules — character analysis)
# Two characters, 4 categories each (landscape, 2 character blocks × 4 rows × 3 cells)
# Layout: label col | Catherine 3 cells | Jason 3 cells
BOARD_A_ROWS = [
    ("LOOKS LIKE", [
        # Catherine side (3 cells — descriptions)
        ("same",      "orange"),
        ("different", "orange"),
        ("okay",      "orange"),
        # Jason side (3 cells)
        ("same",      "orange"),
        ("different", "orange"),
        ("brave",     "orange"),
    ]),
    ("DOES", [
        # Catherine
        ("hide",   "green"),
        ("choose", "green"),
        ("change", "green"),
        # Jason
        ("want",   "green"),
        ("feel",   "green"),
        ("know",   "green"),
    ]),
    ("FEELS", [
        # Catherine
        ("embarrassed", "pink"),
        ("scared",      "pink"),
        ("proud",       "orange"),
        # Jason
        ("happy",    "pink"),
        ("angry",    "pink"),
        ("honest",   "orange"),
    ]),
    ("WANTS", [
        # Catherine
        ("belong",   "green"),
        ("fair",     "orange"),
        ("normal",   "orange"),
        # Jason
        ("belong",   "green"),
        ("real",     "orange"),
        ("free",     "orange"),
    ]),
]

BOARD_B_EMOTIONAL = [
    "feel", "sad", "scared", "happy", "angry",
    "confused", "proud", "brave", "worried", "embarrassed",
    "alone", "together", "okay", "honest",
]
BOARD_B_BELONGING = ["belong", "because", "hide", "choose", "fair", "change"]

BOARD_C_DISCUSSION = ["i think", "i feel", "the character", "i agree", "i disagree", "because"]
BOARD_C_EVIDENCE   = ["the evidence shows", "on page", "the author says", "this shows"]
# Rules-specific annotation codes — LOCKED
BOARD_C_CODES = [
    ("[RULE]",   "what Catherine believes about who belongs and who doesn't",  "brown"),
    ("[BELONG]", "how belonging happens or doesn't happen in this moment",      "green"),
    ("[CHANGE]", "a shift in Catherine's thinking or behavior",                 "orange"),
]


def _draw_header_footer_canvas(c, pg_w, pg_h, is_landscape=False):
    M = 0.45 * inch
    c.setStrokeColor(TEAL)
    c.setLineWidth(1.5)
    c.line(M, pg_h - M - 16, pg_w - M, pg_h - M - 16)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Oblique", 8.5)
    c.drawString(M, pg_h - M - 12, UNIT_TITLE)
    byw_text = " BY DESIGN"
    cbd_text = "COMMUNICATE"
    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColor(TEAL)
    right_x = pg_w - M
    c.drawRightString(right_x - c.stringWidth(byw_text, "Helvetica-Bold", 8.5),
                      pg_h - M - 12, cbd_text)
    c.setFillColor(AMBER)
    c.drawRightString(right_x, pg_h - M - 12, byw_text)
    c.setStrokeColor(TEAL)
    c.setLineWidth(0.5)
    c.line(M, M + 14, pg_w - M, M + 14)
    c.setFillColor(SLATE)
    c.setFont("Helvetica", 6.5)
    c.drawCentredString(pg_w / 2, M + 4, footer_text())


def _draw_board_cell_canvas(c, x, y, w, h, word, fk_color, sym_file=None,
                             label_override=None):
    """Print-safe: white fill, FK color as border only. Reads in B&W."""
    border_col = FK_BORDER.get(fk_color, FK_BORDER["white"])
    c.setFillColor(colors.white)
    c.rect(x, y, w, h, fill=1, stroke=0)
    c.setStrokeColor(border_col)
    c.setLineWidth(2.5)
    c.rect(x, y, w, h, fill=0, stroke=1)
    label = (label_override or word).upper()
    SYM = min(int(h * 0.58), int(w * 0.75), 72)
    LABEL_H = 18
    sp = sym_file or sym_path(word)
    if sp and os.path.exists(sp):
        sym_x = x + (w - SYM) / 2
        sym_y = y + LABEL_H + (h - LABEL_H - SYM) / 2
        c.drawImage(sp, sym_x, sym_y, SYM, SYM,
                    preserveAspectRatio=True, mask="auto")
    else:
        ph_size = min(SYM, 40)
        bx = x + (w - ph_size) / 2
        by = y + LABEL_H + (h - LABEL_H - ph_size) / 2
        c.setFillColor(colors.white)
        c.setStrokeColor(colors.HexColor("#AAAAAA"))
        c.setLineWidth(0.75)
        c.setDash(3, 3)
        c.rect(bx, by, ph_size, ph_size, fill=1, stroke=1)
        c.setDash()
        c.setFillColor(colors.HexColor("#AAAAAA"))
        c.setFont("Helvetica", 10)
        c.drawCentredString(x + w / 2, by + ph_size / 2 - 5, "✏")
    c.setFillColor(NAVY)
    max_font = 10
    font_size = max_font
    while font_size > 5:
        if c.stringWidth(label, "Helvetica-Bold", font_size) <= w - 6:
            break
        font_size -= 0.5
    c.setFont("Helvetica-Bold", font_size)
    c.drawCentredString(x + w / 2, y + 4, label)


def build_layer3_board_a_pdf() -> bytes:
    """Board A: Character Description Board (landscape, 2 character sections × 4 rows)."""
    PG_W, PG_H = rl_landscape(letter)
    M_X, M_TOP, M_BOT = 0.4*inch, 0.5*inch, 0.45*inch

    buf = io.BytesIO()
    c = rl_canvas.Canvas(buf, pagesize=(PG_W, PG_H))

    _draw_header_footer_canvas(c, PG_W, PG_H, is_landscape=True)

    HEADER_Y = PG_H - M_TOP - 22
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(M_X, HEADER_Y, "Board A — Character Description Board")
    c.setFont("Helvetica", 8)
    c.setFillColor(SLATE)
    c.drawString(M_X, HEADER_Y - 13,
        "Select words to describe Catherine and Jason. "
        "Use Parts 1–4 Character Evidence Chart. Partner records.")

    GRID_TOP  = HEADER_Y - 26
    GRID_BOT  = M_BOT + 22
    GRID_H    = GRID_TOP - GRID_BOT
    N_ROWS    = len(BOARD_A_ROWS)    # 4

    # Column layout: row label | Catherine header + 3 cells | Jason header + 3 cells
    LABEL_COL = 0.95 * inch
    AVAIL_W   = PG_W - 2*M_X - LABEL_COL
    CHAR_W    = AVAIL_W / 2                # width for each character's 3 cells
    N_CHAR_COLS = 3
    CELL_W    = CHAR_W / N_CHAR_COLS
    CELL_H    = GRID_H / (N_ROWS + 1)     # +1 for character header row

    c.setFont("Helvetica-Oblique", 7)
    c.setFillColor(colors.HexColor("#64748B"))
    c.drawRightString(PG_W - M_X, M_BOT + 16,
        "Print at 11\"×17\" for gaze-accessible cell size (2\"×2\" minimum).")

    # ── Character header row ─────────────────────────────────────────────────
    header_row_y_top = GRID_TOP
    header_row_y_bot = header_row_y_top - CELL_H

    # Catherine header
    cath_x = M_X + LABEL_COL
    c.setFillColor(NAVY)
    c.rect(cath_x, header_row_y_bot, CHAR_W, CELL_H, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(cath_x + CHAR_W / 2, header_row_y_bot + CELL_H / 2 - 5, "CATHERINE")

    # Jason header
    jason_x = M_X + LABEL_COL + CHAR_W
    c.setFillColor(TEAL)
    c.rect(jason_x, header_row_y_bot, CHAR_W, CELL_H, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(jason_x + CHAR_W / 2, header_row_y_bot + CELL_H / 2 - 5, "JASON")

    # Divider line between character sections
    c.setStrokeColor(WHITE)
    c.setLineWidth(2)
    c.line(jason_x, header_row_y_bot, jason_x, GRID_BOT)

    # ── Category rows ─────────────────────────────────────────────────────────
    for row_idx, (cat_label, cells) in enumerate(BOARD_A_ROWS):
        row_y_top = header_row_y_bot - row_idx * CELL_H
        row_y_bot = row_y_top - CELL_H

        # Row label (rotated, navy bar)
        c.setFillColor(NAVY)
        c.rect(M_X, row_y_bot, LABEL_COL, CELL_H, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 9)
        c.saveState()
        cx = M_X + LABEL_COL / 2
        cy = row_y_bot + CELL_H / 2
        c.translate(cx, cy)
        c.rotate(90)
        c.drawCentredString(0, -4, cat_label)
        c.restoreState()
        c.setStrokeColor(colors.HexColor("#FFFFFF"))
        c.setLineWidth(1.5)
        c.rect(M_X, row_y_bot, LABEL_COL, CELL_H, fill=0, stroke=1)

        # Catherine cells (first 3 in each row)
        for col_idx in range(N_CHAR_COLS):
            word, fk_col = cells[col_idx]
            cell_x = M_X + LABEL_COL + col_idx * CELL_W
            _draw_board_cell_canvas(c, cell_x, row_y_bot, CELL_W, CELL_H,
                                     word, fk_col)

        # Jason cells (last 3 in each row)
        for col_idx in range(N_CHAR_COLS):
            word, fk_col = cells[N_CHAR_COLS + col_idx]
            cell_x = M_X + LABEL_COL + CHAR_W + col_idx * CELL_W
            _draw_board_cell_canvas(c, cell_x, row_y_bot, CELL_W, CELL_H,
                                     word, fk_col)

    c.save()
    return buf.getvalue()


def build_layer3_board_b_pdf() -> bytes:
    """Board B: Emotion + Belonging (portrait, 2 sections)."""
    PG_W, PG_H = letter
    M_X, M_TOP, M_BOT = 0.4*inch, 0.5*inch, 0.45*inch

    buf = io.BytesIO()
    c = rl_canvas.Canvas(buf, pagesize=(PG_W, PG_H))
    _draw_header_footer_canvas(c, PG_W, PG_H)

    HEADER_Y = PG_H - M_TOP - 22
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(M_X, HEADER_Y, "Board B — Emotion + Belonging")
    c.setFont("Helvetica", 8)
    c.setFillColor(SLATE)
    c.drawString(M_X, HEADER_Y - 13,
        "Use throughout: Before Reading (spontaneous, Mode 2) and during activities (Mode 1).")

    AVAIL_W    = PG_W - 2 * M_X
    GRID_TOP   = HEADER_Y - 26
    FOOTER_TOP = M_BOT + 22

    EMO_COLS = 7
    EMO_ROWS = 2
    emo_words = list(BOARD_B_EMOTIONAL)
    while len(emo_words) < EMO_COLS * EMO_ROWS:
        emo_words.append("")

    # Section bar — print-safe: white fill, teal border, navy text
    c.setFillColor(colors.white)
    c.setStrokeColor(TEAL)
    c.setLineWidth(1.5)
    c.rect(M_X, GRID_TOP - 16, AVAIL_W, 16, fill=1, stroke=1)
    # Teal left accent bar
    c.setFillColor(TEAL)
    c.rect(M_X, GRID_TOP - 16, 3, 16, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(M_X + 8, GRID_TOP - 12, "EMOTIONAL VOCABULARY")

    EMO_CELL_W = AVAIL_W / EMO_COLS
    EMO_CELL_H = 86
    emo_grid_top = GRID_TOP - 16

    for row_i in range(EMO_ROWS):
        for col_i in range(EMO_COLS):
            idx = row_i * EMO_COLS + col_i
            if idx >= len(emo_words) or not emo_words[idx]:
                continue
            word = emo_words[idx]
            cell_x = M_X + col_i * EMO_CELL_W
            cell_y = emo_grid_top - (row_i + 1) * EMO_CELL_H
            _draw_board_cell_canvas(c, cell_x, cell_y, EMO_CELL_W, EMO_CELL_H,
                                     word, fk(word))

    belonging_top = emo_grid_top - EMO_ROWS * EMO_CELL_H - 10
    # Section bar — print-safe: white fill, navy border, navy text
    c.setFillColor(colors.white)
    c.setStrokeColor(NAVY)
    c.setLineWidth(1.5)
    c.rect(M_X, belonging_top - 16, AVAIL_W, 16, fill=1, stroke=1)
    c.setFillColor(NAVY)
    c.rect(M_X, belonging_top - 16, 3, 16, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(M_X + 8, belonging_top - 12,
        "BELONGING CONNECTORS  —  These carry the identity and belonging work of Parts 2–4")

    BEL_COLS   = len(BOARD_B_BELONGING)
    BEL_CELL_W = AVAIL_W / BEL_COLS
    remaining_h = belonging_top - 16 - FOOTER_TOP
    BEL_CELL_H  = min(remaining_h, 108)
    bel_grid_top = belonging_top - 16

    for col_i, word in enumerate(BOARD_B_BELONGING):
        cell_x = M_X + col_i * BEL_CELL_W
        cell_y = bel_grid_top - BEL_CELL_H
        _draw_board_cell_canvas(c, cell_x, cell_y, BEL_CELL_W, BEL_CELL_H,
                                 word, fk(word))

    c.setFont("Helvetica-Oblique", 7)
    c.setFillColor(colors.HexColor("#64748B"))
    c.drawRightString(PG_W - M_X, M_BOT + 16,
        "Print at 11\"×17\" for gaze-accessible cell size (2\"×2\" minimum).")

    c.save()
    return buf.getvalue()


def build_layer3_board_c_pdf() -> bytes:
    """Board C: Literary Discussion Moves (portrait) — Rules annotation codes."""
    PG_W, PG_H = letter
    M_X, M_TOP, M_BOT = 0.4*inch, 0.5*inch, 0.45*inch

    buf = io.BytesIO()
    c = rl_canvas.Canvas(buf, pagesize=(PG_W, PG_H))
    _draw_header_footer_canvas(c, PG_W, PG_H)

    HEADER_Y = PG_H - M_TOP - 22
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(M_X, HEADER_Y, "Board C — Literary Discussion Moves")
    c.setFont("Helvetica", 8)
    c.setFillColor(SLATE)
    c.drawString(M_X, HEADER_Y - 13,
        "Use during all unit activities. Laminate and keep on the student's workspace.")

    AVAIL_W    = PG_W - 2 * M_X
    GRID_TOP   = HEADER_Y - 26
    FOOTER_TOP = M_BOT + 22

    # ── Discussion moves (6 cells, 3×2) ──────────────────────────────────────
    DISC_COLS  = 3
    DISC_CELL_W = AVAIL_W / DISC_COLS
    DISC_CELL_H = 90

    # Section bar — print-safe
    c.setFillColor(colors.white)
    c.setStrokeColor(TEAL)
    c.setLineWidth(1.5)
    c.rect(M_X, GRID_TOP - 16, AVAIL_W, 16, fill=1, stroke=1)
    c.setFillColor(TEAL)
    c.rect(M_X, GRID_TOP - 16, 3, 16, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(M_X + 8, GRID_TOP - 12, "DISCUSSION MOVES")

    disc_grid_top = GRID_TOP - 16
    for i, phrase in enumerate(BOARD_C_DISCUSSION):
        row_i = i // DISC_COLS
        col_i = i % DISC_COLS
        cell_x = M_X + col_i * DISC_CELL_W
        cell_y = disc_grid_top - (row_i + 1) * DISC_CELL_H
        fk_col     = "blue"
        bg_col     = FK_BG[fk_col]
        border_col = FK_BORDER[fk_col]
        c.setFillColor(bg_col)
        c.rect(cell_x, cell_y, DISC_CELL_W, DISC_CELL_H, fill=1, stroke=0)
        c.setStrokeColor(border_col)
        c.setLineWidth(2.5)
        c.rect(cell_x, cell_y, DISC_CELL_W, DISC_CELL_H, fill=0, stroke=1)
        c.setFillColor(NAVY)
        font_size = 11
        while font_size > 7:
            if c.stringWidth(phrase.upper(), "Helvetica-Bold", font_size) <= DISC_CELL_W - 10:
                break
            font_size -= 0.5
        c.setFont("Helvetica-Bold", font_size)
        c.drawCentredString(cell_x + DISC_CELL_W/2, cell_y + DISC_CELL_H/2 - 5, phrase.upper())
        c.setFont("Helvetica", 7.5)
        c.setFillColor(SLATE)
        c.drawCentredString(cell_x + DISC_CELL_W/2, cell_y + 8, "...")

    # ── Evidence citing (4 cells, 2×2) ───────────────────────────────────────
    ev_top = disc_grid_top - 2 * DISC_CELL_H - 8
    c.setFillColor(colors.white)
    c.setStrokeColor(NAVY)
    c.setLineWidth(1.5)
    c.rect(M_X, ev_top - 16, AVAIL_W, 16, fill=1, stroke=1)
    c.setFillColor(NAVY)
    c.rect(M_X, ev_top - 16, 3, 16, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(M_X + 8, ev_top - 12, "CITING EVIDENCE")

    EV_COLS   = 2
    EV_CELL_W = AVAIL_W / EV_COLS
    EV_CELL_H = 85
    ev_grid_top = ev_top - 16

    for i, phrase in enumerate(BOARD_C_EVIDENCE):
        row_i = i // EV_COLS
        col_i = i % EV_COLS
        cell_x = M_X + col_i * EV_CELL_W
        cell_y = ev_grid_top - (row_i + 1) * EV_CELL_H
        fk_col     = "green"
        bg_col     = FK_BG[fk_col]
        border_col = FK_BORDER[fk_col]
        c.setFillColor(bg_col)
        c.rect(cell_x, cell_y, EV_CELL_W, EV_CELL_H, fill=1, stroke=0)
        c.setStrokeColor(border_col)
        c.setLineWidth(2.5)
        c.rect(cell_x, cell_y, EV_CELL_W, EV_CELL_H, fill=0, stroke=1)
        c.setFillColor(NAVY)
        font_size = 11
        while font_size > 7:
            if c.stringWidth(phrase.upper(), "Helvetica-Bold", font_size) <= EV_CELL_W - 12:
                break
            font_size -= 0.5
        c.setFont("Helvetica-Bold", font_size)
        c.drawCentredString(cell_x + EV_CELL_W/2, cell_y + EV_CELL_H/2 - 4, phrase.upper())

    # ── Annotation codes (3 cells, horizontal) — Rules-specific ──────────────
    ann_top = ev_grid_top - 2 * EV_CELL_H - 8
    remaining_h = ann_top - 16 - FOOTER_TOP
    ANN_CELL_H  = min(remaining_h, 100)
    ANN_CELL_W  = AVAIL_W / 3

    c.setFillColor(colors.white)
    c.setStrokeColor(NAVY)
    c.setLineWidth(1.5)
    c.rect(M_X, ann_top - 16, AVAIL_W, 16, fill=1, stroke=1)
    c.setFillColor(NAVY)
    c.rect(M_X, ann_top - 16, 3, 16, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(M_X + 8, ann_top - 12,
        "IDENTITY EVIDENCE CHART CODES  —  Rules: Identity and Belonging")

    ann_grid_top = ann_top - 16
    for i, (code, desc, fk_col) in enumerate(BOARD_C_CODES):
        cell_x = M_X + i * ANN_CELL_W
        cell_y = ann_grid_top - ANN_CELL_H
        bg_col     = FK_BG[fk_col]
        border_col = FK_BORDER[fk_col]
        c.setFillColor(bg_col)
        c.rect(cell_x, cell_y, ANN_CELL_W, ANN_CELL_H, fill=1, stroke=0)
        c.setStrokeColor(border_col)
        c.setLineWidth(3)
        c.rect(cell_x, cell_y, ANN_CELL_W, ANN_CELL_H, fill=0, stroke=1)
        # Code label (large)
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(cell_x + ANN_CELL_W/2, cell_y + ANN_CELL_H - 24, code)
        # Description (wrapping)
        c.setFont("Helvetica", 8)
        c.setFillColor(colors.HexColor("#475569"))
        wrapped_d = textwrap.wrap(desc, 26)
        line_y = cell_y + ANN_CELL_H - 40
        for dl in wrapped_d[:3]:
            c.drawCentredString(cell_x + ANN_CELL_W/2, line_y, dl)
            line_y -= 11

    c.setFont("Helvetica-Oblique", 7)
    c.setFillColor(colors.HexColor("#64748B"))
    c.drawRightString(PG_W - M_X, M_BOT + 16,
        "Laminate all boards. Use throughout the unit.")

    c.save()
    return buf.getvalue()


# ─────────────────────────────────────────────────────────────────────────────
# LAYER 4a — Unit Vocabulary Map
# ─────────────────────────────────────────────────────────────────────────────

ALL_UNIT_WORDS = [
    # Core words
    ("belong",    "core"), ("want",      "core"), ("feel",      "core"),
    ("think",     "core"), ("know",      "core"), ("change",    "core"),
    ("choose",    "core"), ("hide",      "core"), ("same",      "core"),
    ("different", "core"), ("fair",      "core"), ("because",   "core"),
    # Fringe words — chapter order
    ("normal",      "fringe"), ("rule",        "fringe"), ("clinic",      "fringe"),
    ("word card",   "fringe"), ("embarrassed", "fringe"), ("honest",      "fringe"),
    ("Catherine",   "fringe"), ("Jason",       "fringe"), ("David",       "fringe"),
    ("Kristi",      "fringe"), ("proud",       "fringe"), ("brave",       "fringe"),
]


def build_layer4a_vocab_map_pdf() -> bytes:
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter,
        leftMargin=0.55*inch, rightMargin=0.55*inch,
        topMargin=0.4*inch, bottomMargin=0.4*inch)

    H1   = ParagraphStyle("h1", fontName="Helvetica-Bold",
        fontSize=13, textColor=NAVY, leading=17, spaceAfter=4)
    BODY = ParagraphStyle("body", fontName="Helvetica",
        fontSize=8, textColor=NAVY, leading=11, spaceAfter=5)
    NOTE = ParagraphStyle("note", fontName="Helvetica-Oblique",
        fontSize=8, textColor=colors.HexColor("#475569"), leading=11,
        borderColor=AMBER, borderWidth=1, borderPadding=(4,6,4,6),
        backColor=colors.HexColor("#FFFBEB"), spaceAfter=6)
    LABEL = ParagraphStyle("lbl", fontName="Helvetica-Bold",
        fontSize=8.5, textColor=WHITE, leading=11, alignment=TA_CENTER)
    CELL  = ParagraphStyle("cell", fontName="Helvetica",
        fontSize=8, textColor=NAVY, leading=10)
    CELL_C = ParagraphStyle("cellc", fontName="Helvetica",
        fontSize=10, textColor=colors.HexColor("#94A3B8"), leading=12, alignment=TA_CENTER)
    TYPE_CORE   = ParagraphStyle("tc", fontName="Helvetica-Bold", fontSize=7.5,
        textColor=colors.HexColor("#1E5A8A"), leading=10, alignment=TA_CENTER)
    TYPE_FRINGE = ParagraphStyle("tf", fontName="Helvetica-Bold", fontSize=7.5,
        textColor=colors.HexColor("#92400E"), leading=10, alignment=TA_CENTER)

    story = [header_flowable(),
             HRFlowable(width="100%", thickness=1.5, color=TEAL, spaceAfter=5)]

    story.append(Paragraph(f"Building a Vocabulary Library: {UNIT_TITLE}", H1))
    story.append(Paragraph(
        "These words belong to this student's permanent vocabulary library — "
        "not just this unit. Words marked <b>Generalized</b> are ready to add "
        "to their AAC system or communication book.", NOTE))

    COLS_W = [1.4*inch, 0.75*inch, 0.9*inch, 0.9*inch, 1.1*inch, 1.1*inch, 1.65*inch]
    headers = ["Word", "Type", "Introduced\n○", "Modeled\n○", "Spontaneous\nUse  ○",
               "Generalized\n★", "Notes"]
    hdr_row = [Paragraph(h, LABEL) for h in headers]

    data = [hdr_row]
    for word, wtype in ALL_UNIT_WORDS:
        type_style = TYPE_CORE if wtype == "core" else TYPE_FRINGE
        data.append([
            Paragraph(word, CELL),
            Paragraph(wtype, type_style),
            Paragraph("○", CELL_C), Paragraph("○", CELL_C),
            Paragraph("○", CELL_C), Paragraph("○", CELL_C),
            Paragraph("", CELL),
        ])

    tbl = Table(data, colWidths=COLS_W, repeatRows=1)
    ts  = [
        ("BACKGROUND",    (0,0), (-1,0), NAVY),
        ("ALIGN",         (0,0), (-1,0), "CENTER"),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0,1), (-1,-1),
         [colors.HexColor("#F8FAFC"), colors.white]),
        ("LINEBELOW",     (0,12), (-1,12), 1.5, AMBER),  # after 12 core words
        ("BOX",           (0,0), (-1,-1), 1, NAVY),
        ("INNERGRID",     (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ("TOPPADDING",    (0,0), (-1,-1), 3),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
        ("LEFTPADDING",   (0,0), (-1,-1), 5),
        ("RIGHTPADDING",  (0,0), (-1,-1), 5),
    ]
    tbl.setStyle(TableStyle(ts))
    story.append(tbl)

    story.append(Spacer(1, 5))
    story.append(Paragraph(
        "★ Generalized = used spontaneously with 2+ different partners across 2+ settings. "
        "Ready to request on AAC system or communication book. Note the date and context.",
        BODY))

    story.append(Spacer(1, 3))
    story.append(HRFlowable(width="100%", thickness=0.5, color=TEAL, spaceAfter=2))
    story.append(footer_flowable())

    doc.build(story)
    return buf.getvalue()


# ─────────────────────────────────────────────────────────────────────────────
# LAYER 5 — Student Response Pages (5 parts — character analysis / identity focus)
# ─────────────────────────────────────────────────────────────────────────────

STUDENT_PARTS = [
    {
        "num": 1,
        "title": "The Rules",
        "skill": "Character Introduction",
        "prompt": (
            "What rules does Catherine write in her notebook? "
            "What do the rules tell you about how Catherine thinks belonging works? "
            "Find two rules that show what she believes."
        ),
        "vocab": ["rule", "belong", "same", "different", "fair", "because", "normal"],
        "response": "lines",
        "frames": [
            "One of Catherine's rules is ___________________________________",
            "because she believes ________________________________________.",
            "This shows that Catherine thinks belonging means _______________.",
        ],
    },
    {
        "num": 2,
        "title": "Meeting Jason",
        "skill": "Character Evidence",
        "prompt": (
            "How does Catherine feel when she first meets Jason at the clinic? "
            "What does Jason want that surprises Catherine? "
            "Use evidence from the text."
        ),
        "vocab": ["feel", "embarrassed", "honest", "want", "hide", "word card", "know"],
        "response": "sentence",
        "frame": "Catherine felt ________________________ because ________________________. "
                 "Jason wanted ________________________, which shows that ________________________.",
    },
    {
        "num": 3,
        "title": "Rules Break Down",
        "skill": "Character Evidence",
        "prompt": (
            "What happens when Catherine's rules stop working? "
            "Show what Catherine believed BEFORE meeting Jason and what starts to change. "
            "How do her feelings about belonging shift?"
        ),
        "vocab": ["change", "same", "different", "belong", "hide", "fair", "choose"],
        "response": "beforeafter",
    },
    {
        "num": 4,
        "title": "What Catherine Learns",
        "skill": "Character Evidence",
        "prompt": (
            "What does Catherine choose to do at the end of the novel? "
            "Why is her choice difficult? "
            "What does her choice show about what she now believes about belonging?"
        ),
        "vocab": ["choose", "brave", "proud", "belong", "because", "honest", "fair"],
        "response": "lines",
        "frames": [
            "Catherine chose to ___________________________________________",
            "even though ________________________________________________.",
            "This shows she now believes _________________________________.",
        ],
    },
    {
        "num": 5,
        "title": "Whole-Book Synthesis",
        "skill": "Character Synthesis",
        "prompt": (
            "According to Cynthia Lord, what does it really mean to belong — "
            "and what gets in the way? "
            "Use evidence from at least two parts of the book. "
            "Show how Catherine's thinking changes from the beginning to the end."
        ),
        "vocab": ["think", "belong", "because", "change", "fair", "honest", "choose", "different"],
        "response": "lines",
        "frames": [
            "At the beginning of Rules, Catherine believed __________________",
            "___________________. By the end, she learned that belonging means",
            "___________________. For example, when _______________________",
            "___________________. This shows that ________________________.",
        ],
    },
]

# Rules-specific annotation codes for student pages
ANNOTATION_CODES = [("[RULE]", "brown"), ("[BELONG]", "green"), ("[CHANGE]", "orange")]


def _draw_vocab_chip_canvas(c, x, y, word, chip_w, chip_h):
    """Print-safe: white fill, FK color as border only. Reads in B&W."""
    fk_col = fk(word)
    bdr = FK_BORDER.get(fk_col, colors.HexColor("#AAAAAA"))
    c.setFillColor(colors.white)
    c.setStrokeColor(bdr)
    c.setLineWidth(1.5)
    c.roundRect(x, y, chip_w, chip_h, 3, fill=1, stroke=1)
    c.setFillColor(NAVY)
    fs = 7.5
    while fs > 5.5 and c.stringWidth(word, "Helvetica-Bold", fs) > chip_w - 6:
        fs -= 0.5
    c.setFont("Helvetica-Bold", fs)
    c.drawCentredString(x + chip_w / 2, y + chip_h / 2 - fs * 0.35, word)


def _draw_response_box(c, M_X, AVAIL_W, y_top, box_h, label="Your response:"):
    """White background, navy left accent bar, ruled lines at 32pt spacing."""
    BAR_W      = 5
    LINE_COLOR = colors.HexColor("#94A3B8")
    LINE_W     = 0.75
    LINE_SP    = 32
    INNER_X    = M_X + BAR_W + 6
    INNER_W    = AVAIL_W - BAR_W - 10

    c.setFillColor(colors.white)
    c.rect(M_X, y_top - box_h, AVAIL_W, box_h, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.rect(M_X, y_top - box_h, BAR_W, box_h, fill=1, stroke=0)
    c.setStrokeColor(NAVY)
    c.setLineWidth(1.0)
    c.rect(M_X, y_top - box_h, AVAIL_W, box_h, fill=0, stroke=1)
    c.setFillColor(SLATE)
    c.setFont("Helvetica-Oblique", 7.5)
    c.drawString(INNER_X, y_top - 11, label)

    line_start_y = y_top - 20
    line_bottom  = y_top - box_h + 10
    ly = line_start_y
    while ly > line_bottom:
        c.setStrokeColor(LINE_COLOR)
        c.setLineWidth(LINE_W)
        c.line(INNER_X, ly, M_X + AVAIL_W - 8, ly)
        ly -= LINE_SP


def _draw_student_page(c, PG_W, PG_H, part):
    M_X     = 0.55 * inch
    M_TOP   = 0.42 * inch
    M_BOT   = 0.38 * inch
    AVAIL_W = PG_W - 2 * M_X
    y       = PG_H - M_TOP

    # ── Running header ────────────────────────────────────────────────────────
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Oblique", 8.5)
    c.drawString(M_X, y - 10, UNIT_TITLE)
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 8.5)
    comm_w = c.stringWidth("COMMUNICATE", "Helvetica-Bold", 8.5)
    c.drawRightString(PG_W - M_X, y - 10, "COMMUNICATE")
    c.setFillColor(AMBER)
    c.drawRightString(PG_W - M_X - comm_w - 3, y - 10, "BY DESIGN  ·")
    y -= 14

    c.setStrokeColor(TEAL)
    c.setLineWidth(1.5)
    c.line(M_X, y, PG_W - M_X, y)
    y -= 8

    # ── Part label bar ────────────────────────────────────────────────────────
    BAR_H = 20
    c.setFillColor(NAVY)
    c.rect(M_X, y - BAR_H, AVAIL_W, BAR_H, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(M_X + 8, y - BAR_H + 6,
                 f"PART {part['num']}  ·  {part['skill'].upper()}  ·  Student Response Page")
    y -= BAR_H + 4

    # ── Activity title ────────────────────────────────────────────────────────
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(M_X, y - 15, part["title"])
    y -= 22

    # ── Student info row ──────────────────────────────────────────────────────
    INFO_H = 22
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.setLineWidth(0.75)
    for (label, x_frac, w_frac) in [
        ("Name:",    0,    0.40),
        ("Class:",   0.41, 0.25),
        ("Teacher:", 0.67, 0.17),
        ("Date:",    0.85, 0.15),
    ]:
        bx = M_X + AVAIL_W * x_frac
        bw = AVAIL_W * w_frac
        c.setFillColor(colors.white)
        c.rect(bx, y - INFO_H, bw, INFO_H, fill=1, stroke=1)
        c.setFillColor(SLATE)
        c.setFont("Helvetica", 7.5)
        c.drawString(bx + 4, y - INFO_H + 8, label)
    y -= INFO_H + 6

    # ── Prompt box ────────────────────────────────────────────────────────────
    chars_per_line = max(60, int((AVAIL_W - 16) / 4.7))
    wrapped = textwrap.wrap(part["prompt"], chars_per_line)
    PROMPT_LINE_H = 12
    PROMPT_PAD    = 8
    PROMPT_H      = max(40, len(wrapped) * PROMPT_LINE_H + 2 * PROMPT_PAD)

    c.setFillColor(colors.HexColor("#EFF6FF"))
    c.rect(M_X, y - PROMPT_H, AVAIL_W, PROMPT_H, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.rect(M_X, y - PROMPT_H, 5, PROMPT_H, fill=1, stroke=0)
    c.setStrokeColor(TEAL)
    c.setLineWidth(1.0)
    c.rect(M_X, y - PROMPT_H, AVAIL_W, PROMPT_H, fill=0, stroke=1)
    c.setFillColor(NAVY)
    c.setFont("Helvetica", 9)
    ty = y - PROMPT_PAD - PROMPT_LINE_H
    for line in wrapped:
        c.drawString(M_X + 13, ty, line)
        ty -= PROMPT_LINE_H
    y -= PROMPT_H + 6

    # ── Vocabulary strip ──────────────────────────────────────────────────────
    c.setFillColor(SLATE)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(M_X, y - 9, "Vocabulary:")
    y -= 12

    vocab_words  = part["vocab"]
    N_CHIPS      = len(vocab_words)
    CHIP_H       = 22
    CHIP_GAP     = 5
    CHIP_W       = min(80, (AVAIL_W - (N_CHIPS - 1) * CHIP_GAP) / N_CHIPS)
    strip_w      = N_CHIPS * CHIP_W + (N_CHIPS - 1) * CHIP_GAP
    chip_x_start = M_X + (AVAIL_W - strip_w) / 2

    for j, word in enumerate(vocab_words):
        cx = chip_x_start + j * (CHIP_W + CHIP_GAP)
        _draw_vocab_chip_canvas(c, cx, y - CHIP_H, word, CHIP_W, CHIP_H)
    y -= CHIP_H + 8

    # ── Annotation code reminder strip ───────────────────────────────────────
    FOOTER_RESERVED = 30
    ANN_Y = M_BOT + FOOTER_RESERVED + 2
    ax = M_X
    c.setFont("Helvetica-Bold", 7)
    for code, fk_col in ANNOTATION_CODES:
        bg  = FK_BG.get(fk_col)
        bdr = FK_BORDER.get(fk_col)
        cw  = c.stringWidth(code, "Helvetica-Bold", 7) + 10
        c.setFillColor(bg)
        c.setStrokeColor(bdr)
        c.setLineWidth(1.0)
        c.roundRect(ax, ANN_Y - 14, cw, 14, 3, fill=1, stroke=1)
        c.setFillColor(NAVY)
        c.drawString(ax + 5, ANN_Y - 10, code)
        ax += cw + 5

    # ── Response area ─────────────────────────────────────────────────────────
    RESPONSE_H = y - M_BOT - FOOTER_RESERVED
    resp_type  = part.get("response", "lines")

    if resp_type == "sentence":
        frame = part.get("frame", "________________________ because ________________________.")
        # Sentence frame box
        SF_PAD    = 10
        SF_LINE_H = 15
        # Wrap the frame across multiple lines if needed
        frame_chars = max(50, int((AVAIL_W - 24) / 5.2))
        frame_lines = textwrap.wrap(frame, frame_chars)
        SF_H = SF_PAD * 2 + SF_LINE_H * len(frame_lines) + 4
        c.setFillColor(colors.white)
        c.setStrokeColor(AMBER)
        c.setLineWidth(2.0)
        c.rect(M_X, y - SF_H, AVAIL_W, SF_H, fill=1, stroke=1)
        c.setFillColor(AMBER)
        c.rect(M_X, y - SF_H, 5, SF_H, fill=1, stroke=0)
        c.setFillColor(NAVY)
        c.setFont("Helvetica", 9)
        fline_y = y - SF_PAD - SF_LINE_H
        for fl in frame_lines:
            c.drawString(M_X + 13, fline_y, fl)
            fline_y -= SF_LINE_H
        y -= SF_H + 8

        remaining = y - M_BOT - FOOTER_RESERVED
        _draw_response_box(c, M_X, AVAIL_W, y, remaining, label="Tell me more:")

    elif resp_type == "beforeafter":
        col_w  = (AVAIL_W - 8) / 2
        body_h = RESPONSE_H - 24
        HDR_H  = 24

        # BEFORE header — print-safe: white fill, slate border
        c.setFillColor(colors.white)
        c.setStrokeColor(colors.HexColor("#475569"))
        c.setLineWidth(2.0)
        c.rect(M_X, y - HDR_H, col_w, HDR_H, fill=1, stroke=1)
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(M_X + col_w / 2, y - HDR_H + 7, "BEFORE — MEETING JASON")

        # AFTER header — print-safe: white fill, teal border
        c.setFillColor(colors.white)
        c.setStrokeColor(TEAL)
        c.setLineWidth(2.0)
        c.rect(M_X + col_w + 8, y - HDR_H, col_w, HDR_H, fill=1, stroke=1)
        c.setFillColor(NAVY)
        c.drawCentredString(M_X + col_w + 8 + col_w / 2, y - HDR_H + 7, "AFTER — RULES BREAK DOWN")

        # Column bodies — white, navy left accent bars, ruled lines
        for col_x in [M_X, M_X + col_w + 8]:
            c.setFillColor(colors.white)
            c.rect(col_x, y - HDR_H - body_h, col_w, body_h, fill=1, stroke=0)
            c.setFillColor(NAVY)
            c.rect(col_x, y - HDR_H - body_h, 5, body_h, fill=1, stroke=0)
            c.setStrokeColor(NAVY)
            c.setLineWidth(1.0)
            c.rect(col_x, y - HDR_H - body_h, col_w, body_h, fill=0, stroke=1)
            c.setFillColor(SLATE)
            c.setFont("Helvetica-Oblique", 7.5)
            c.drawString(col_x + 10, y - HDR_H - 12, "Catherine believed / felt...")
            line_y = y - HDR_H - 22
            line_bot = y - HDR_H - body_h + 8
            while line_y > line_bot:
                c.setStrokeColor(colors.HexColor("#94A3B8"))
                c.setLineWidth(0.75)
                c.line(col_x + 10, line_y, col_x + col_w - 8, line_y)
                line_y -= 32

        # Arrow between columns
        c.setFillColor(AMBER)
        c.setFont("Helvetica-Bold", 22)
        c.drawCentredString(M_X + AVAIL_W / 2, y - HDR_H - body_h / 2 - 10, "→")

    elif resp_type == "lines":
        frames = part.get("frames", [])

        if frames:
            SF_LINE_H  = 28
            SF_PAD     = 10
            total_sf_h = len(frames) * SF_LINE_H + SF_PAD * 2

            c.setFillColor(colors.white)
            c.rect(M_X, y - total_sf_h, AVAIL_W, total_sf_h, fill=1, stroke=0)
            c.setFillColor(AMBER)
            c.rect(M_X, y - total_sf_h, 5, total_sf_h, fill=1, stroke=0)
            c.setStrokeColor(AMBER)
            c.setLineWidth(2.0)
            c.rect(M_X, y - total_sf_h, AVAIL_W, total_sf_h, fill=0, stroke=1)

            c.setFillColor(NAVY)
            c.setFont("Helvetica", 9)
            for fi, fr_text in enumerate(frames):
                line_y = y - SF_PAD - (fi + 1) * SF_LINE_H + 14
                max_chars = max(40, int((AVAIL_W - 24) / 5.0))
                fparts = textwrap.wrap(fr_text, max_chars)
                for fp in fparts[:1]:
                    c.drawString(M_X + 13, line_y, fp)
                c.setStrokeColor(colors.HexColor("#94A3B8"))
                c.setLineWidth(0.75)
                c.line(M_X + 13, line_y - 3, M_X + AVAIL_W - 10, line_y - 3)

            y -= total_sf_h + 8

        remaining = y - M_BOT - FOOTER_RESERVED
        _draw_response_box(c, M_X, AVAIL_W, y, remaining, label="Tell me more:")

    # ── Footer ────────────────────────────────────────────────────────────────
    c.setStrokeColor(TEAL)
    c.setLineWidth(0.75)
    c.line(M_X, M_BOT + 16, PG_W - M_X, M_BOT + 16)
    c.setFillColor(SLATE)
    c.setFont("Helvetica", 6.5)
    c.drawCentredString(PG_W / 2, M_BOT + 5, footer_text())


def build_layer5_student_response_pages_pdf() -> bytes:
    buf = io.BytesIO()
    c   = rl_canvas.Canvas(buf, pagesize=letter)
    PG_W, PG_H = letter
    for part in STUDENT_PARTS:
        _draw_student_page(c, PG_W, PG_H, part)
        c.showPage()
    c.save()
    return buf.getvalue()


# ─────────────────────────────────────────────────────────────────────────────
# ASSEMBLE FINAL PDF
# ─────────────────────────────────────────────────────────────────────────────

def build_packet():
    # Ensure output directory exists
    os.makedirs(os.path.dirname(os.path.abspath(OUT_PATH)), exist_ok=True)

    writer = PdfWriter()

    print("Building Layer 1 — Communication Environment Setup...")
    l1 = PdfReader(io.BytesIO(build_layer1_pdf()))
    for p in l1.pages: writer.add_page(p)
    print(f"  Added {len(l1.pages)} page(s)")

    print("Building Layer 2 — Core Word Symbol Cards...")
    l2a = PdfReader(io.BytesIO(build_layer2_symbol_cards_pdf(
        "Core Word Symbol Cards — Set A",
        SET_A_CORE,
        section_note=(
            "These 12 core words are SDI instruction targets. "
            "Core vocabulary is likely already on the student's system."
        )
    )))
    for p in l2a.pages: writer.add_page(p)
    print(f"  Added {len(l2a.pages)} page(s)")

    print("Building Layer 2 — Fringe Word Symbol Cards...")
    l2b = PdfReader(io.BytesIO(build_layer2_symbol_cards_pdf(
        "Fringe Word Symbol Cards — Unit-Specific Vocabulary",
        SET_A_FRINGE,
        section_note=(
            "Words are organized by when they first appear in Rules. "
            "Includes proper nouns (Catherine, Jason, David, Kristi) — "
            "create custom picture cards using photos or drawings for these. "
            "⚠️ Several words (clinic, word card) have draw-your-own placeholders — "
            "add ARASAAC symbols when available or create custom cards."
        )
    )))
    for p in l2b.pages: writer.add_page(p)
    print(f"  Added {len(l2b.pages)} page(s)")

    print("Building Layer 3 — Board A: Character Description Board...")
    l3a = PdfReader(io.BytesIO(build_layer3_board_a_pdf()))
    for p in l3a.pages: writer.add_page(p)
    print(f"  Added {len(l3a.pages)} page(s)")

    print("Building Layer 3 — Board B: Emotion + Belonging...")
    l3b = PdfReader(io.BytesIO(build_layer3_board_b_pdf()))
    for p in l3b.pages: writer.add_page(p)
    print(f"  Added {len(l3b.pages)} page(s)")

    print("Building Layer 3 — Board C: Literary Discussion Moves...")
    l3c = PdfReader(io.BytesIO(build_layer3_board_c_pdf()))
    for p in l3c.pages: writer.add_page(p)
    print(f"  Added {len(l3c.pages)} page(s)")

    print("Building Layer 4a — Vocabulary Map...")
    l4a = PdfReader(io.BytesIO(build_layer4a_vocab_map_pdf()))
    for p in l4a.pages: writer.add_page(p)
    print(f"  Added {len(l4a.pages)} page(s)")

    print("Appending Layer 4b — AAC Session Tracker...")
    if os.path.exists(TRACKER):
        tracker = PdfReader(TRACKER)
        for p in tracker.pages: writer.add_page(p)
        print(f"  Added {len(tracker.pages)} page(s)")
    else:
        # Try alternate path
        alt_tracker = os.path.join(MNT, "Products/Nonfiction Units/AAC_Communication_Session_Tracker.pdf")
        if os.path.exists(alt_tracker):
            tracker = PdfReader(alt_tracker)
            for p in tracker.pages: writer.add_page(p)
            print(f"  Added {len(tracker.pages)} page(s) [from alternate path]")
        else:
            print(f"  ⚠️  Tracker not found. Skipping Layer 4b. Add manually after build.")
            print(f"     Expected: {TRACKER}")

    print("Building Layer 5 — Student Response Pages...")
    l5 = PdfReader(io.BytesIO(build_layer5_student_response_pages_pdf()))
    for p in l5.pages: writer.add_page(p)
    print(f"  Added {len(l5.pages)} page(s)")

    # Write to /tmp first (iCloud write rule), then copy to destination
    tmp_path = "/tmp/Rules_Identity_and_Belonging_Printable_Packet.pdf"
    with open(tmp_path, "wb") as f:
        writer.write(f)

    import shutil
    shutil.copy2(tmp_path, OUT_PATH)

    total = len(writer.pages)
    print(f"\n✅ Built: {OUT_PATH}")
    print(f"   Total pages: {total}")
    print()
    print("Page map:")
    print("  p1     Layer 1  — Communication Environment Setup")
    print("  p2     Layer 2  — Core word symbol cards (12 words)")
    print("  p3     Layer 2  — Fringe word symbol cards (12 words, chapter order)")
    print("  p4     Layer 3  — Board A: Character Description Board (landscape)")
    print("  p5     Layer 3  — Board B: Emotion + Belonging")
    print("  p6     Layer 3  — Board C: Literary Discussion Moves + Rules Codes")
    print("  p7     Layer 4a — Vocabulary Map (12 core + 12 fringe)")
    print("  p8–9   Layer 4b — AAC Session Tracker")
    print("  p10    Layer 5  — Student Response: Part 1 — The Rules")
    print("  p11    Layer 5  — Student Response: Part 2 — Meeting Jason")
    print("  p12    Layer 5  — Student Response: Part 3 — Rules Break Down")
    print("  p13    Layer 5  — Student Response: Part 4 — What Catherine Learns")
    print("  p14    Layer 5  — Student Response: Part 5 — Whole-Book Synthesis")
    print()
    print("Symbol notes:")
    print("  belong     → arasaac_include.png  (locked sub: belong → include)")
    print("  normal     → arasaac_same.png     (same = normal, closest available)")
    print("  rule       → arasaac_law.png      (law = rule, closest available)")
    print("  clinic     → draw-your-own        (no close match in cache)")
    print("  word card  → draw-your-own        (AAC-specific; no standard symbol)")
    print("  embarrassed→ arasaac_embarrassed.png (verify present in cache)")
    print("  Catherine, Jason, David, Kristi → draw-your-own (proper nouns)")


if __name__ == "__main__":
    build_packet()

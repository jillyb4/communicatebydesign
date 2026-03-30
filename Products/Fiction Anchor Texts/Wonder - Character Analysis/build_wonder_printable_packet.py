"""
Wonder: Character Analysis — Fiction Printable Packet
Communicate by Design

Builds: Wonder_Character_Analysis_Printable_Packet.pdf
Spec:   _Operations/memory/fiction_printable_packet_spec.md

Structure:
  p1       Layer 1  — Communication Environment Setup
  p2       Layer 2  — Core word symbol cards (Set A, 12 words, 3×4 grid)
  p3       Layer 2  — Fringe word symbol cards (Set A, 12 words, in chapter order)
  p4       Layer 3  — Board A: Character Description (landscape)
  p5       Layer 3  — Board B: Emotion + Reasoning (portrait)
  p6       Layer 3  — Board C: Literary Discussion Moves (portrait)
  p7       Layer 4a — Unit Vocabulary Map
  p8–9     Layer 4b — AAC Session Tracker (appended unchanged)

Symbol substitutions (approved, 2026-03-29):
  belong          → include  (arasaac_include_11702.png)
  ordinary        → usual    (arasaac_usual_2547.png)
  face looks diff → face     (arasaac_face_2684.png)
"""

import os, io
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
MNT        = os.path.join(SCRIPT_DIR, "..", "..", "..")   # Communicate by Design/
SYM_CACHE  = os.path.join(MNT, "_Operations/symbol_cache")
TRACKER    = os.path.join(MNT, "Products/Nonfiction Units/AAC_Communication_Session_Tracker.pdf")
OUT_PATH   = os.path.join(SCRIPT_DIR, "Wonder_Character_Analysis_Printable_Packet.pdf")

UNIT_TITLE = "Wonder: Character Analysis"

# ── Brand colors ──────────────────────────────────────────────────────────────

NAVY  = colors.HexColor("#1B1F3B")
TEAL  = colors.HexColor("#006DA0")
AMBER = colors.HexColor("#FFB703")
SLATE = colors.HexColor("#94A3B8")
WHITE = colors.white

# ── Fitzgerald Key ─────────────────────────────────────────────────────────────
# Per spec: Green=Verbs/Actions, Orange=Descriptions/Adj, Yellow=People/Pronouns,
#           Brown=Nouns, Blue=Little Words/Prepositions, Pink=Social/Feelings

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
    "feel":    "green",   # verb
    "want":    "green",   # verb
    "think":   "green",   # verb
    "know":    "green",   # verb
    "change":  "green",   # verb
    "because": "blue",    # connector/little word
    "maybe":   "orange",  # description
    "sad":     "pink",    # feeling
    "scared":  "pink",    # feeling
    "happy":   "pink",    # feeling
    "alone":   "orange",  # description
    "kind":    "orange",  # description
    # Set A Fringe — 12 words (organized by chapter order in unit)
    "ordinary":           "orange",   # description
    "helmet":             "brown",    # noun
    "school":             "brown",    # noun
    "face looks different": "orange", # description
    "bully":              "brown",    # noun (person)
    "brave":              "orange",   # description
    "friend":             "yellow",   # people/pronoun category
    "belong":             "green",    # verb
    "loyal":              "orange",   # description
    "invisible":          "orange",   # description
    "choose":             "green",    # verb
    "different":          "orange",   # description
    # Board extras (used in Boards A/B/C)
    "big":     "orange", "small":   "orange", "young":  "orange",
    "old":     "orange", "wears":   "green",  "carries": "green",
    "runs":    "green",  "hides":   "green",  "fights":  "green",
    "cries":   "green",  "laughs":  "green",  "helps":   "green",
    "leaves":  "green",  "saves":   "green",  "lies":    "green",
    "tells the truth": "green",
    "angry":   "pink",   "confused":"orange", "proud":   "orange",
    "worried": "pink",
    "probably":"blue",
    "i think":   "white", "i feel":   "white",
    "the character": "yellow",
    "i agree": "white",  "i disagree": "white",
    "the evidence shows": "white", "on page": "white",
    "the author says": "white", "this shows": "white",
    "[trait]": "orange", "[why]": "blue", "[change]": "green",
}

def fk(word):
    """Return Fitzgerald Key color name for word."""
    return WORD_FK.get(word.lower(), "white")

# ── Symbol path lookup ────────────────────────────────────────────────────────
# Maps canonical word → filename in symbol_cache. Substitution words noted.

SYMBOL_FILE = {
    # Set A Core
    "feel":    "arasaac_feel.png",
    "want":    "arasaac_want.png",
    "think":   "arasaac_think.png",
    "know":    "arasaac_know.png",
    "change":  "arasaac_change.png",
    "because": "arasaac_because.png",
    "maybe":   "arasaac_maybe.png",
    "sad":     "arasaac_sad.png",
    "scared":  "arasaac_scared.png",
    "happy":   "arasaac_happy.png",
    "alone":   "arasaac_alone_7253.png",
    "kind":    "arasaac_kind.png",
    # Set A Fringe — in chapter order
    "ordinary":             "arasaac_usual_2547.png",    # ★ substitute
    "helmet":               "arasaac_helmet_2691.png",
    "school":               "arasaac_school.png",
    "face looks different": "arasaac_face_2684.png",     # ★ face symbol used
    "bully":                "arasaac_bully_12321.png",
    "brave":                "arasaac_brave.png",
    "friend":               "arasaac_friend.png",
    "belong":               "arasaac_include_11702.png", # ★ substitute
    "loyal":                "arasaac_loyal_33006.png",
    "invisible":            "arasaac_invisible_32755.png",
    "choose":               "arasaac_choose.png",
    "different":            "arasaac_different.png",
    # Board extras
    "big":      "arasaac_big.png",
    "small":    "arasaac_small.png",
    "old":      "arasaac_old.png",
    "carries":  "arasaac_carry.png",
    "runs":     "arasaac_run.png",
    "fights":   "arasaac_fight.png",
    "cries":    "arasaac_cry.png",
    "laughs":   "arasaac_laugh.png",
    "helps":    "arasaac_help.png",
    "lies":     "arasaac_lie.png",
    "confused": "arasaac_confused.png",
    "proud":    "arasaac_proud.png",
    "worried":  "arasaac_worried.png",
    "agree":    "arasaac_agree.png",
    "disagree": "arasaac_disagree.png",
    "page":     "arasaac_page.png",
    "show":     "arasaac_show.png",
    "tell":     "arasaac_tell.png",
}

def sym_path(word):
    """Return full path to symbol PNG if it exists, else None."""
    fname = SYMBOL_FILE.get(word.lower())
    if fname:
        p = os.path.join(SYM_CACHE, fname)
        return p if os.path.exists(p) else None
    # Fallback: try arasaac_[word].png
    p = os.path.join(SYM_CACHE, f"arasaac_{word.lower().replace(' ', '_')}.png")
    return p if os.path.exists(p) else None

# ── Running header + footer (flowable) ────────────────────────────────────────

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

    H1 = ParagraphStyle("h1", fontName="Helvetica-Bold",
        fontSize=12, textColor=NAVY, leading=15, spaceAfter=3)
    H2 = ParagraphStyle("h2", fontName="Helvetica-Bold",
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

    # Title
    story.append(Paragraph("Communication Environment Setup  —  Print once. Laminate. Keep in hand during instruction.", H1))

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
                   "<b>Use during:</b> shared reading, discussion, text exploration.", SMALL)],
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

    # ── Prompt Hierarchy (Mode 1) ─────────────────────────────────────────────
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
    b_row = []
    b_style = ParagraphStyle("bs", fontName="Helvetica", fontSize=8,
        textColor=NAVY, leading=11)
    b_yn = ParagraphStyle("byn", fontName="Helvetica-Bold", fontSize=7.5,
        textColor=TEAL, leading=10)
    for item in barrier_items:
        b_row.append([
            Paragraph(item, b_style),
            Paragraph("○ Yes   ○ No", b_yn),
        ])
    b_table = Table(b_row, colWidths=[4.5*inch, 1.4*inch],
                    repeatRows=0)
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

    # ── Tools + Access quick reference ────────────────────────────────────────
    story.append(Paragraph("TOOLS IN THIS PACKET", H2))
    t_row_style = ParagraphStyle("trs", fontName="Helvetica", fontSize=7.5,
        textColor=NAVY, leading=10)
    t_lbl_style = ParagraphStyle("tls", fontName="Helvetica-Bold", fontSize=7.5,
        textColor=NAVY, leading=10)
    tools_compact = [
        ("p.2", "Core Word Symbol Cards (12)",
         "SDI targets — confirm with AAC team before adding to device"),
        ("p.3", "Fringe Word Symbol Cards (12)",
         "Chapter order — consult full team before selecting access method"),
        ("p.4", "Board A — Character Description",
         "LOOKS LIKE / DOES / FEELS / WANTS — use Parts 1–4"),
        ("p.5", "Board B — Emotion + Reasoning",
         "Emotional vocab + reasoning connectors — use throughout"),
        ("p.6", "Board C — Literary Discussion Moves",
         "Discussion + evidence + [TRAIT][WHY][CHANGE] codes"),
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
    tools_table = Table(t_rows, colWidths=[0.55*inch, 2.3*inch, 4.35*inch])
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

# Set A Core — 12 words (organized by Fitzgerald Key category)
SET_A_CORE = [
    "feel", "want", "think", "know", "change", "choose",  # verbs
    "sad", "scared", "happy", "alone",                     # feelings/descriptions
    "maybe", "kind",                                        # descriptions/connectors
]

# Set A Fringe — 12 words (organized by chapter order in Wonder)
SET_A_FRINGE = [
    "ordinary",           # Part 1 "Wonder" — Auggie's opening wish
    "helmet",             # Part 1 — Auggie's space helmet
    "school",             # Part 1 "The Auggie Tour" — first day of school
    "face looks different",  # Part 1 — description of Auggie's appearance
    "bully",              # Part 1 — Julian and others
    "brave",              # Parts 2–3 — courage theme
    "friend",             # Part 2 — Jack Will
    "belong",             # Parts 3–4 — belonging theme
    "loyal",              # Part 4 "Jack Will" — Halloween section
    "invisible",          # Multiple parts — feeling unseen
    "different",          # Throughout — central theme
    "kind",               # Part 8 "August" — Mr. Tushman's speech
]

# Override: 'kind' appears in both core and fringe slots — remove from core if
# it would cause a duplicate. Per vocab spec, 'kind' is tagged as core.
# Fringe list uses 'kind' as a placeholder for book-arc sequence only.
# Final authoritative lists per cbd_unit_vocab.js entry #7:
SET_A_CORE = [
    "feel", "want", "think", "know", "change", "because",
    "maybe", "sad", "scared", "happy", "alone", "kind",
]
SET_A_FRINGE = [
    "ordinary", "helmet", "school", "face looks different",
    "bully", "brave", "friend", "belong",
    "loyal", "invisible", "choose", "different",
]

def build_layer2_symbol_cards_pdf(title: str, words: list,
                                   section_note: str = "") -> bytes:
    """
    Build a 3-column × 4-row grid of 2"×2" symbol cards.
    words: list of exactly 12 words (pad or trim to 12).
    """
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter,
        leftMargin=0.4*inch, rightMargin=0.4*inch,
        topMargin=0.4*inch, bottomMargin=0.35*inch)

    COLS     = 3
    ROWS     = 4
    CARD_H   = int(2 * inch)   # 144pt
    SYM_SIZE = 88

    word_lbl = ParagraphStyle("wl", fontName="Helvetica-Bold",
        fontSize=11, textColor=NAVY, leading=14, alignment=TA_CENTER)
    small_lbl = ParagraphStyle("sl", fontName="Helvetica-Bold",
        fontSize=9, textColor=NAVY, leading=11, alignment=TA_CENTER)
    sec_head = ParagraphStyle("sh", fontName="Helvetica-Bold",
        fontSize=10.5, textColor=NAVY, leading=14, spaceAfter=3)
    note_style = ParagraphStyle("ns", fontName="Helvetica-Oblique",
        fontSize=7.5, textColor=colors.HexColor("#475569"), leading=10,
        spaceAfter=4, borderColor=TEAL, borderWidth=0.5,
        borderPadding=(3,5,3,5), backColor=colors.HexColor("#F0F9FF"))
    GAP          = 5
    CARD_OUTER_W = (7.7 / 3) * inch
    CARD_INNER_W = CARD_OUTER_W - 2 * GAP
    CARD_INNER_H = CARD_H       - 2 * GAP

    # Pad to 12
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
        # Choose label style based on word length
        lbl_style = small_lbl if len(w) > 10 else word_lbl
        content = []
        if sp:
            content.append(RLImage(sp, width=SYM_SIZE, height=SYM_SIZE))
        else:
            content.append(Spacer(1, SYM_SIZE))
            ph = ParagraphStyle("ph", fontName="Helvetica-Oblique",
                fontSize=8, textColor=colors.HexColor("#AAAAAA"),
                leading=10, alignment=TA_CENTER)
            content.append(Paragraph("(no symbol)", ph))
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
# LAYER 3 — Communication Boards (canvas-based for precise layout)
# ─────────────────────────────────────────────────────────────────────────────

# Board data
BOARD_A_ROWS = [
    ("LOOKS LIKE", [
        ("big",              "orange"),
        ("small",            "orange"),
        ("young",            "orange"),
        ("old",              "orange"),
        ("carries",          "green"),
        ("face looks different", "orange"),
    ]),
    ("DOES", [
        ("runs",    "green"),
        ("hides",   "green"),
        ("fights",  "green"),
        ("helps",   "green"),
        ("lies",    "green"),
        ("tells the truth", "green"),
    ]),
    ("FEELS", [
        ("sad",     "pink"),
        ("scared",  "pink"),
        ("happy",   "pink"),
        ("alone",   "orange"),
        ("brave",   "orange"),
        ("worried", "pink"),
    ]),
    ("WANTS", [
        ("want",      "green"),
        ("belong",    "green"),
        ("friend",    "yellow"),
        ("choose",    "green"),
        ("invisible", "orange"),
        ("different", "orange"),
    ]),
]

BOARD_B_EMOTIONAL = [
    "feel", "sad", "scared", "happy", "alone",
    "angry", "confused", "proud", "brave", "worried",
    "kind", "different", "belong", "invisible",
]
BOARD_B_REASONING = ["because", "maybe", "probably", "think", "know", "change"]

BOARD_C_DISCUSSION = ["i think", "i feel", "the character", "i agree", "i disagree", "because"]
BOARD_C_EVIDENCE   = ["the evidence shows", "on page", "the author says", "this shows"]
BOARD_C_CODES      = ["[TRAIT]", "[WHY]", "[CHANGE]"]


def _draw_header_footer_canvas(c, pg_w, pg_h, is_landscape=False):
    """Draw running header + footer on a canvas page."""
    M = 0.45 * inch

    # Header line
    c.setStrokeColor(TEAL)
    c.setLineWidth(1.5)
    c.line(M, pg_h - M - 16, pg_w - M, pg_h - M - 16)

    # Header text
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Oblique", 8.5)
    c.drawString(M, pg_h - M - 12, UNIT_TITLE)
    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColor(TEAL)
    c.drawRightString(pg_w - M, pg_h - M - 12, "COMMUNICATE ")
    c.setFillColor(AMBER)
    bw = c.stringWidth("COMMUNICATE ", "Helvetica-Bold", 8.5)
    c.drawRightString(pg_w - M + bw - c.stringWidth("COMMUNICATE ", "Helvetica-Bold", 8.5),
                      pg_h - M - 12, "BY DESIGN")

    # Simpler header — just draw the combined string
    c.setFillColor(TEAL)
    cbd_text = "COMMUNICATE"
    byw_text = " BY DESIGN"
    total_w = c.stringWidth(cbd_text + byw_text, "Helvetica-Bold", 8.5)
    right_x = pg_w - M
    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColor(TEAL)
    c.drawRightString(right_x - c.stringWidth(byw_text, "Helvetica-Bold", 8.5),
                      pg_h - M - 12, cbd_text)
    c.setFillColor(AMBER)
    c.drawRightString(right_x, pg_h - M - 12, byw_text)

    # Footer line
    c.setStrokeColor(TEAL)
    c.setLineWidth(0.5)
    c.line(M, M + 14, pg_w - M, M + 14)

    # Footer text
    c.setFillColor(SLATE)
    c.setFont("Helvetica", 6.5)
    ft = footer_text()
    c.drawCentredString(pg_w / 2, M + 4, ft)


def _draw_board_cell_canvas(c, x, y, w, h, word, fk_color, sym_file=None,
                             label_override=None):
    """
    Draw a single board cell at (x,y) bottom-left, size w×h.
    Symbol centered in upper portion, word label in lower portion.
    """
    bg_col     = FK_BG.get(fk_color, FK_BG["white"])
    border_col = FK_BORDER.get(fk_color, FK_BORDER["white"])

    # Background
    c.setFillColor(bg_col)
    c.rect(x, y, w, h, fill=1, stroke=0)

    # Border
    c.setStrokeColor(border_col)
    c.setLineWidth(2.5)
    c.rect(x, y, w, h, fill=0, stroke=1)

    label = (label_override or word).upper()
    SYM = min(int(h * 0.58), int(w * 0.75), 72)
    LABEL_H = 18  # reserved for label at bottom

    # Symbol
    sp = sym_file or sym_path(word)
    if sp and os.path.exists(sp):
        sym_x = x + (w - SYM) / 2
        sym_y = y + LABEL_H + (h - LABEL_H - SYM) / 2
        c.drawImage(sp, sym_x, sym_y, SYM, SYM,
                    preserveAspectRatio=True, mask="auto")
    else:
        # Placeholder grey box
        c.setFillColor(colors.HexColor("#E2E8F0"))
        ph_size = min(SYM, 40)
        c.rect(x + (w - ph_size)/2, y + LABEL_H + (h - LABEL_H - ph_size)/2,
               ph_size, ph_size, fill=1, stroke=0)

    # Label (may need to wrap if long)
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
    """Board A: Character Description (landscape, 4 rows × 6 cells)."""
    PG_W, PG_H = rl_landscape(letter)   # 792 × 612
    M_X, M_TOP, M_BOT = 0.4*inch, 0.5*inch, 0.45*inch

    buf = io.BytesIO()
    c = rl_canvas.Canvas(buf, pagesize=(PG_W, PG_H))

    _draw_header_footer_canvas(c, PG_W, PG_H, is_landscape=True)

    # Board title
    HEADER_Y = PG_H - M_TOP - 22
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(M_X, HEADER_Y, "Board A — Character Description")
    c.setFont("Helvetica", 8)
    c.setFillColor(SLATE)
    c.drawString(M_X, HEADER_Y - 13,
        "Select one word from each row to describe the character. Partner records the description.")

    # Grid layout
    GRID_TOP  = HEADER_Y - 26
    GRID_BOT  = M_BOT + 22       # leave room for footer
    GRID_H    = GRID_TOP - GRID_BOT
    N_ROWS    = len(BOARD_A_ROWS)   # 4
    N_COLS    = 6                   # items per row
    LABEL_COL = 1.0 * inch          # category label column width
    AVAIL_W   = PG_W - 2*M_X - LABEL_COL
    CELL_W    = AVAIL_W / N_COLS
    CELL_H    = GRID_H / N_ROWS

    note_style_small = (
        "Print at 11\"×17\" for gaze-accessible cell size (2\"×2\" minimum)."
    )
    c.setFont("Helvetica-Oblique", 7)
    c.setFillColor(colors.HexColor("#64748B"))
    c.drawRightString(PG_W - M_X, M_BOT + 16, note_style_small)

    for row_idx, (cat_label, cells) in enumerate(BOARD_A_ROWS):
        row_y_top = GRID_TOP - row_idx * CELL_H
        row_y_bot = row_y_top - CELL_H

        # Category label cell (left column)
        c.setFillColor(NAVY)
        c.rect(M_X, row_y_bot, LABEL_COL, CELL_H, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 10)
        # Rotate text for vertical category label
        c.saveState()
        cx = M_X + LABEL_COL / 2
        cy = row_y_bot + CELL_H / 2
        c.translate(cx, cy)
        c.rotate(90)
        c.drawCentredString(0, -4, cat_label)
        c.restoreState()

        # Cell border on label
        c.setStrokeColor(colors.HexColor("#FFFFFF"))
        c.setLineWidth(1.5)
        c.rect(M_X, row_y_bot, LABEL_COL, CELL_H, fill=0, stroke=1)

        # Content cells
        for col_idx, (word, fk_col) in enumerate(cells):
            cell_x = M_X + LABEL_COL + col_idx * CELL_W
            _draw_board_cell_canvas(c, cell_x, row_y_bot, CELL_W, CELL_H,
                                     word, fk_col)

    c.save()
    return buf.getvalue()


def build_layer3_board_b_pdf() -> bytes:
    """Board B: Emotion + Reasoning (portrait, 2 sections)."""
    PG_W, PG_H = letter   # 612 × 792
    M_X, M_TOP, M_BOT = 0.4*inch, 0.5*inch, 0.45*inch

    buf = io.BytesIO()
    c = rl_canvas.Canvas(buf, pagesize=(PG_W, PG_H))

    _draw_header_footer_canvas(c, PG_W, PG_H)

    # Title
    HEADER_Y = PG_H - M_TOP - 22
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(M_X, HEADER_Y, "Board B — Emotion + Reasoning")
    c.setFont("Helvetica", 8)
    c.setFillColor(SLATE)
    c.drawString(M_X, HEADER_Y - 13,
        "Use throughout: Before Reading (spontaneous, Mode 2) and during activities (Mode 1).")

    AVAIL_W = PG_W - 2 * M_X
    GRID_TOP = HEADER_Y - 26
    FOOTER_TOP = M_BOT + 22

    # ── Emotional vocabulary section ──────────────────────────────────────────
    EMO_COLS = 7
    EMO_ROWS = 2
    emo_words = BOARD_B_EMOTIONAL  # 14 words → 7×2
    while len(emo_words) < EMO_COLS * EMO_ROWS:
        emo_words = list(emo_words) + [""]

    # Section label
    c.setFillColor(TEAL)
    c.rect(M_X, GRID_TOP - 16, AVAIL_W, 16, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(M_X + 5, GRID_TOP - 12, "EMOTIONAL VOCABULARY")

    EMO_CELL_W = AVAIL_W / EMO_COLS
    EMO_CELL_H = 86  # pts ≈ 1.2"
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

    # ── Reasoning connectors section ──────────────────────────────────────────
    reasoning_top = emo_grid_top - EMO_ROWS * EMO_CELL_H - 10

    c.setFillColor(NAVY)
    c.rect(M_X, reasoning_top - 16, AVAIL_W, 16, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(M_X + 5, reasoning_top - 12,
        "REASONING CONNECTORS  —  These carry the inference and motivation work of Parts 3–4")

    RSN_COLS = len(BOARD_B_REASONING)  # 6
    RSN_CELL_W = AVAIL_W / RSN_COLS
    remaining_h = reasoning_top - 16 - FOOTER_TOP
    RSN_CELL_H = min(remaining_h, 108)  # up to 1.5"

    rsn_grid_top = reasoning_top - 16
    for col_i, word in enumerate(BOARD_B_REASONING):
        cell_x = M_X + col_i * RSN_CELL_W
        cell_y = rsn_grid_top - RSN_CELL_H
        _draw_board_cell_canvas(c, cell_x, cell_y, RSN_CELL_W, RSN_CELL_H,
                                 word, fk(word))

    c.setFont("Helvetica-Oblique", 7)
    c.setFillColor(colors.HexColor("#64748B"))
    c.drawRightString(PG_W - M_X, M_BOT + 16,
        "Print at 11\"×17\" for gaze-accessible cell size (2\"×2\" minimum).")

    c.save()
    return buf.getvalue()


def build_layer3_board_c_pdf() -> bytes:
    """Board C: Literary Discussion Moves (portrait)."""
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

    AVAIL_W   = PG_W - 2 * M_X
    GRID_TOP  = HEADER_Y - 26
    FOOTER_TOP = M_BOT + 22

    # ── Discussion moves (6 cells, 3×2) ──────────────────────────────────────
    DISC_COLS = 3
    disc_words = BOARD_C_DISCUSSION   # 6 items
    DISC_CELL_W = AVAIL_W / DISC_COLS
    DISC_CELL_H = 90

    c.setFillColor(TEAL)
    c.rect(M_X, GRID_TOP - 16, AVAIL_W, 16, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(M_X + 5, GRID_TOP - 12, "DISCUSSION MOVES")

    disc_grid_top = GRID_TOP - 16
    for i, phrase in enumerate(disc_words):
        row_i = i // DISC_COLS
        col_i = i % DISC_COLS
        cell_x = M_X + col_i * DISC_CELL_W
        cell_y = disc_grid_top - (row_i + 1) * DISC_CELL_H
        # Text-heavy cell — draw manually
        fk_col = "blue"
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

    c.setFillColor(NAVY)
    c.rect(M_X, ev_top - 16, AVAIL_W, 16, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(M_X + 5, ev_top - 12, "CITING EVIDENCE")

    EV_COLS   = 2
    ev_words  = BOARD_C_EVIDENCE
    EV_CELL_W = AVAIL_W / EV_COLS
    EV_CELL_H = 85

    ev_grid_top = ev_top - 16
    for i, phrase in enumerate(ev_words):
        row_i = i // EV_COLS
        col_i = i % EV_COLS
        cell_x = M_X + col_i * EV_CELL_W
        cell_y = ev_grid_top - (row_i + 1) * EV_CELL_H
        fk_col = "green"
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

    # ── Annotation codes (3 cells, horizontal) ───────────────────────────────
    ann_top = ev_grid_top - 2 * EV_CELL_H - 8
    remaining_h = ann_top - 16 - FOOTER_TOP
    ANN_CELL_H = min(remaining_h, 100)
    ANN_CELL_W = AVAIL_W / 3

    c.setFillColor(colors.HexColor("#1B1F3B"))
    c.rect(M_X, ann_top - 16, AVAIL_W, 16, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(M_X + 5, ann_top - 12,
        "ANNOTATION CODES  —  Wonder: Character Analysis  (LOCKED 2026-03-29)")

    ann_descriptions = {
        "[TRAIT]":  ("who the character is",  "orange"),
        "[WHY]":    ("why they act that way",  "blue"),
        "[CHANGE]": ("how the character changes", "green"),
    }
    ann_grid_top = ann_top - 16
    for i, (code, (desc, fk_col)) in enumerate(ann_descriptions.items()):
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
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(cell_x + ANN_CELL_W/2, cell_y + ANN_CELL_H - 28, code)
        # Description (smaller)
        c.setFont("Helvetica", 9)
        c.setFillColor(colors.HexColor("#475569"))
        c.drawCentredString(cell_x + ANN_CELL_W/2, cell_y + 16, desc)
        # Symbol if any
        sp = sym_path(code.lower().strip("[]"))
        if sp and os.path.exists(sp):
            sym_sz = 40
            c.drawImage(sp, cell_x + (ANN_CELL_W - sym_sz)/2,
                         cell_y + (ANN_CELL_H - sym_sz)/2 - 5,
                         sym_sz, sym_sz, mask="auto")

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
    # Core words (type = core)
    ("feel",    "core"),   ("want",    "core"), ("think",   "core"),
    ("know",    "core"),   ("change",  "core"), ("because", "core"),
    ("maybe",   "core"),   ("sad",     "core"), ("scared",  "core"),
    ("happy",   "core"),   ("alone",   "core"), ("kind",    "core"),
    # Fringe words (type = fringe) — chapter order
    ("ordinary",             "fringe"), ("helmet",    "fringe"),
    ("school",               "fringe"), ("face looks different", "fringe"),
    ("bully",                "fringe"), ("brave",     "fringe"),
    ("friend",               "fringe"), ("belong",    "fringe"),
    ("loyal",                "fringe"), ("invisible", "fringe"),
    ("choose",               "fringe"), ("different", "fringe"),
]


def build_layer4a_vocab_map_pdf() -> bytes:
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter,
        leftMargin=0.55*inch, rightMargin=0.55*inch,
        topMargin=0.4*inch, bottomMargin=0.4*inch)

    H1 = ParagraphStyle("h1", fontName="Helvetica-Bold",
        fontSize=13, textColor=NAVY, leading=17, spaceAfter=4)
    BODY = ParagraphStyle("body", fontName="Helvetica",
        fontSize=8, textColor=NAVY, leading=11, spaceAfter=5)
    NOTE = ParagraphStyle("note", fontName="Helvetica-Oblique",
        fontSize=8, textColor=colors.HexColor("#475569"), leading=11,
        borderColor=AMBER, borderWidth=1, borderPadding=(4,6,4,6),
        backColor=colors.HexColor("#FFFBEB"), spaceAfter=6)
    LABEL = ParagraphStyle("lbl", fontName="Helvetica-Bold",
        fontSize=8.5, textColor=NAVY, leading=11, alignment=TA_CENTER)
    CELL = ParagraphStyle("cell", fontName="Helvetica",
        fontSize=8, textColor=NAVY, leading=10)
    CELL_C = ParagraphStyle("cellc", fontName="Helvetica",
        fontSize=8, textColor=NAVY, leading=10, alignment=TA_CENTER)
    TYPE_CORE   = ParagraphStyle("tc", fontName="Helvetica-Bold", fontSize=7.5,
        textColor=colors.HexColor("#1E5A8A"), leading=10, alignment=TA_CENTER)
    TYPE_FRINGE = ParagraphStyle("tf", fontName="Helvetica-Bold", fontSize=7.5,
        textColor=colors.HexColor("#92400E"), leading=10, alignment=TA_CENTER)

    story = [header_flowable(),
             HRFlowable(width="100%", thickness=1.5, color=TEAL, spaceAfter=5)]

    story.append(Paragraph(
        f"Building a Vocabulary Library: {UNIT_TITLE}", H1))
    story.append(Paragraph(
        "These words belong to this student's permanent vocabulary library — "
        "not just this unit. Words marked <b>Generalized</b> are ready to add "
        "to their AAC system or communication book.", NOTE))

    # Column headers
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
            Paragraph("○", CELL_C),
            Paragraph("○", CELL_C),
            Paragraph("○", CELL_C),
            Paragraph("○", CELL_C),
            Paragraph("", CELL),
        ])

    tbl = Table(data, colWidths=COLS_W, repeatRows=1)
    ts  = [
        # Header row
        ("BACKGROUND",    (0,0), (-1,0), NAVY),
        ("TEXTCOLOR",     (0,0), (-1,0), WHITE),
        ("FONTNAME",      (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,0), 8.5),
        ("ALIGN",         (0,0), (-1,0), "CENTER"),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        # Alternating rows
        ("ROWBACKGROUNDS", (0,1), (-1,-1),
         [colors.HexColor("#F8FAFC"), colors.white]),
        # Divider between core and fringe
        ("LINEBELOW",     (0,12), (-1,12), 1.5, AMBER),
        # Borders
        ("BOX",           (0,0), (-1,-1), 1, NAVY),
        ("INNERGRID",     (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        # Padding
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
# ASSEMBLE FINAL PDF
# ─────────────────────────────────────────────────────────────────────────────

def build_packet():
    writer = PdfWriter()

    print("Building Layer 1 — Communication Environment Setup...")
    l1 = PdfReader(io.BytesIO(build_layer1_pdf()))
    for p in l1.pages:
        writer.add_page(p)
    print(f"  Added {len(l1.pages)} page(s)")

    print("Building Layer 2 — Core Word Symbol Cards...")
    l2a = PdfReader(io.BytesIO(build_layer2_symbol_cards_pdf(
        "Core Word Symbol Cards — Set A",
        SET_A_CORE,
        section_note=(
            "These 12 core words are SDI instruction targets. "
            "Core vocabulary is likely already on the student's system. "
            "Confirm with the AAC team before adding to the device."
        )
    )))
    for p in l2a.pages:
        writer.add_page(p)
    print(f"  Added {len(l2a.pages)} page(s)")

    print("Building Layer 2 — Fringe Word Symbol Cards...")
    l2b = PdfReader(io.BytesIO(build_layer2_symbol_cards_pdf(
        "Fringe Word Symbol Cards — Unit-Specific Vocabulary",
        SET_A_FRINGE,
        section_note=(
            "Words are organized by when they first appear in Wonder. "
            "Students may use printed cards, symbols from an existing symbol set, "
            "or programmed device pages. "
            "Consult the full AAC team before selecting access method for fringe words."
        )
    )))
    for p in l2b.pages:
        writer.add_page(p)
    print(f"  Added {len(l2b.pages)} page(s)")

    print("Building Layer 3 — Board A: Character Description...")
    l3a = PdfReader(io.BytesIO(build_layer3_board_a_pdf()))
    for p in l3a.pages:
        writer.add_page(p)
    print(f"  Added {len(l3a.pages)} page(s)")

    print("Building Layer 3 — Board B: Emotion + Reasoning...")
    l3b = PdfReader(io.BytesIO(build_layer3_board_b_pdf()))
    for p in l3b.pages:
        writer.add_page(p)
    print(f"  Added {len(l3b.pages)} page(s)")

    print("Building Layer 3 — Board C: Literary Discussion Moves...")
    l3c = PdfReader(io.BytesIO(build_layer3_board_c_pdf()))
    for p in l3c.pages:
        writer.add_page(p)
    print(f"  Added {len(l3c.pages)} page(s)")

    print("Building Layer 4a — Vocabulary Map...")
    l4a = PdfReader(io.BytesIO(build_layer4a_vocab_map_pdf()))
    for p in l4a.pages:
        writer.add_page(p)
    print(f"  Added {len(l4a.pages)} page(s)")

    print("Appending Layer 4b — AAC Session Tracker...")
    if os.path.exists(TRACKER):
        tracker = PdfReader(TRACKER)
        for p in tracker.pages:
            writer.add_page(p)
        print(f"  Added {len(tracker.pages)} page(s)")
    else:
        print(f"  ⚠️  Tracker not found at: {TRACKER}")
        print(f"     Skipping Layer 4b. Add manually after build.")

    with open(OUT_PATH, "wb") as f:
        writer.write(f)

    total = len(writer.pages)
    print(f"\n✅ Built: {OUT_PATH}")
    print(f"   Total pages: {total}")
    print()
    print("Page map:")
    print("  p1     Layer 1  — Communication Environment Setup")
    print("  p2     Layer 2  — Core word symbol cards (12 words)")
    print("  p3     Layer 2  — Fringe word symbol cards (12 words, chapter order)")
    print("  p4     Layer 3  — Board A: Character Description (landscape)")
    print("  p5     Layer 3  — Board B: Emotion + Reasoning")
    print("  p6     Layer 3  — Board C: Literary Discussion Moves")
    print("  p7     Layer 4a — Vocabulary Map")
    print("  p8–9   Layer 4b — AAC Session Tracker")
    print()
    print("Symbol substitutions used:")
    print("  belong          → include  (arasaac_include_11702.png)")
    print("  ordinary        → usual    (arasaac_usual_2547.png)")
    print("  face looks diff → face     (arasaac_face_2684.png)")
    print()
    print("Next steps:")
    print("  1. Open PDF and run packet QC checklist")
    print("     (_Operations/memory/fiction_printable_packet_spec.md)")
    print("  2. Delete Wonder_Character_Analysis_Printable_Kit.docx (wrong format — manual Finder)")
    print("  3. Confirm symbol substitutions with Jill")


if __name__ == "__main__":
    build_packet()

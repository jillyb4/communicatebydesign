"""
build_all_units.py
==================
Builds Communication Access Packets for all 5 remaining nonfiction units,
creates Welcome/Terms PDFs for all 6 units, then assembles TPT folders.

Units:
  504 Sit-In, Keiko, Radium Girls, Capitol Crawl, Zitkala-Sa
  (Frances Kelsey packet already built — Welcome/Terms + TPT folder assembled here)

Output per unit:
  Products/Nonfiction Units/[UNIT]/[UNIT]_Communication_Access_Packet.pdf
  Products/Nonfiction Units/[UNIT]/[UNIT]_Welcome_and_Terms.pdf
  Products/Nonfiction Units/[UNIT]/[UNIT]_TPT/
      [UNIT]_COMPLETE.docx
      [UNIT]_Symbol_Cards.pdf          (if exists)
      [UNIT]_Communication_Access_Packet.pdf
      [UNIT]_Welcome_and_Terms.pdf
"""

import os, io, shutil
from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus.flowables import Image as RLImage

# ── Paths ─────────────────────────────────────────────────────────────────────
# Updated 2026-03-29: session path updated to current session

MNT       = "/sessions/kind-gracious-keller/mnt/Communicate by Design"
SCRATCH   = "/sessions/kind-gracious-keller"
SYM_CACHE = os.path.join(MNT, "_Operations/symbol_cache")
TRACKER   = os.path.join(MNT, "Products/Nonfiction Units/AAC_Communication_Session_Tracker.pdf")
NF_ROOT   = os.path.join(MNT, "Products/Nonfiction Units")

# ── Brand colors ──────────────────────────────────────────────────────────────

NAVY  = colors.HexColor("#1B1F3B")
TEAL  = colors.HexColor("#006DA0")
AMBER = colors.HexColor("#FFB703")
SLATE = colors.HexColor("#94A3B8")
WHITE = colors.white

# ── Fitzgerald Key ─────────────────────────────────────────────────────────────

FKC_BORDER = {
    "green":  colors.HexColor("#2E7D32"),
    "orange": colors.HexColor("#E65100"),
    "yellow": colors.HexColor("#F57F17"),
    "blue":   colors.HexColor("#1565C0"),
    "pink":   colors.HexColor("#880E4F"),
    "white":  colors.HexColor("#757575"),
}

VERBS        = {'say','think','know','want','help','stop','show','prove','tell',
                'believe','go','give','protect','approve','deny','claim','test',
                'question','answer','fight','change','mean','care','evaluate',
                'identify','support','decide','create','feel','make','need',
                'sit','organize','occupy','demand','corroborate','verify','agree',
                'disagree','do','move','swim','learn','die','prove','crawl'}
ADJECTIVES   = {'good','bad','wrong','right','more','different','same','true',
                'strong','weak','safe','important','clear','brave','fair','free',
                'equal','federal','reliable','healthy','sick','wild','false',
                'less','first','last'}
PRONOUNS     = {'i','you','he','she','we','they','my','your','who','what',
                'where','when','which'}
PREPOSITIONS = {'because','but','if','in','on','at','up','yet','as','before',
                'after','and','why'}
SOCIAL       = {'not','yes','no','please','thank','sorry'}

def fk_cat(word):
    w = word.lower().strip().split()[0]   # use first word for multi-word terms
    if w in SOCIAL:       return "pink"
    if w in PRONOUNS:     return "yellow"
    if w in VERBS:        return "green"
    if w in ADJECTIVES:   return "orange"
    if w in PREPOSITIONS: return "blue"
    return "white"

def sym_img_path(word):
    key = word.lower().replace(' ', '_').replace('-', '_').replace('š', 's')
    p = os.path.join(SYM_CACHE, f"arasaac_{key}.png")
    return p if os.path.exists(p) else None

# ── Unit configurations ───────────────────────────────────────────────────────

UNITS = {
    "504 Sit-In": {
        "folder":     "504 Sit In",
        "unit_pdf":   os.path.join(SCRATCH, "504_Sit_In_Unit_COMPLETE.pdf"),
        "aac_pages":  [17, 18],
        "docx":       "504_Sit_In_Unit_COMPLETE.docx",
        "sym_cards":  "504_Sit_In_Symbol_Cards.pdf",
        "prefix":     "504_Sit_In",
        "display":    "504 Sit-In: 26 Hours That Changed America",
        "grade_range": "Grades 6–10",
        "core_words": [
            'people','change','feel','fight','help','make','need','show',
            'sit','stop','tell','think','want','brave','different','fair',
            'free','important','right','safe','same','strong','wrong'
        ],
        "fringe_words": [
            'approve','crawl','demand','deny','occupy','organize','protest',
            'prove','sign','access','advocate','barrier','building','community',
            'disability','discrimination','equal','federal','government','law',
            'rights','section'
        ],
        "top5_core":   ['fight','show','stop','right','change'],
        "top5_fringe": ['protest','law','disability','equal','rights'],
        # Student print pages (zero-indexed) — confirmed 2026-03-29 via PDF keyword scan
        "student_pages": [2, 4, 7, 10, 13, 14, 15, 16, 17, 18, 20, 23, 24, 26, 27, 28, 29, 31, 32, 33, 35],
        "what_inside": [
            "Multi-version informational passages (V1, V2, V3 Lexile ranges)",
            "Annotation tools and reading frameworks",
            "Differentiation strategies for all learners",
            "MLL & AAC communication access support",
            "IEP goal stems and SDI documentation tools",
            "Symbol Cards PDF",
            "Communication Access Packet with ARASAAC vocabulary cards",
            "AAC Communication Session Tracker",
        ],
    },
    "Keiko": {
        "folder":     "Keiko",
        "unit_pdf":   os.path.join(SCRATCH, "Keiko_Unit_COMPLETE.pdf"),
        "aac_pages":  [7, 8],
        "docx":       "Keiko_Unit_COMPLETE.docx",
        "sym_cards":  None,
        "prefix":     "Keiko",
        "display":    "Keiko: The Orca Who Came Home",
        "grade_range": "Grades 6–10",
        "core_words": [
            'think','feel','know','good','bad','best','free','live','place',
            'because','why','help','care','same','different','more','less',
            'before','after','true','false','show','mean','prove','first',
            'then','last','which'
        ],
        "fringe_words": [
            'captivity','ocean','whale','park','sick','healthy','home',
            'family','pod','human','wild','move','swim','learn','die',
            'freedom','safe','danger','company','protect','today'
        ],
        "top5_core":   ['free','because','help','show','true'],
        "top5_fringe": ['captivity','whale','ocean','wild','freedom'],
        # Student print pages (zero-indexed) — confirmed 2026-03-29 via PDF keyword scan
        "student_pages": [2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 21],
        "what_inside": [
            "Multi-version informational passages (V1, V2, V3 Lexile ranges)",
            "Annotation tools and reading frameworks",
            "Differentiation strategies for all learners",
            "MLL & AAC communication access support",
            "IEP goal stems and SDI documentation tools",
            "Communication Access Packet with ARASAAC vocabulary cards",
            "AAC Communication Session Tracker",
        ],
    },
    "Radium Girls": {
        "folder":     "Radium Girls",
        "unit_pdf":   os.path.join(SCRATCH, "Radium_Girls_Unit_COMPLETE.pdf"),
        "aac_pages":  [6, 7],
        "docx":       "Radium_Girls_Unit_COMPLETE.docx",
        "sym_cards":  None,
        "prefix":     "Radium_Girls",
        "display":    "The Radium Girls: The Women Who Fought Back",
        "grade_range": "Grades 6–10",
        "core_words": [
            'think','feel','know','good','bad','right','wrong','because',
            'why','help','stop','fight','change','same','different','more',
            'less','before','after','true','false','show','mean','prove',
            'first','then','last'
        ],
        "fringe_words": [
            'radium','factory','worker','paint','sick','law','court','safe',
            'danger','company','money','protect','today','bone','doctor',
            'lie','proof'
        ],
        "top5_core":   ['prove','wrong','stop','fight','show'],
        "top5_fringe": ['radium','factory','safe','danger','lie'],
        # Student print pages (zero-indexed) — confirmed 2026-03-29 via PDF keyword scan
        "student_pages": [2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
        "what_inside": [
            "Multi-version informational passages (V1, V2, V3 Lexile ranges)",
            "Annotation tools and reading frameworks",
            "Differentiation strategies for all learners",
            "MLL & AAC communication access support",
            "IEP goal stems and SDI documentation tools",
            "Communication Access Packet with ARASAAC vocabulary cards",
            "AAC Communication Session Tracker",
        ],
    },
    "Capitol Crawl": {
        "folder":     "Capitol Crawl",
        "unit_pdf":   os.path.join(SCRATCH, "Capitol_Crawl_Lesson_COMPLETE.pdf"),
        "aac_pages":  [10, 11],  # confirmed 2026-03-29: idx 10=Differentiating, idx 11=Communication Access
        "docx":       "Capitol_Crawl_Lesson_COMPLETE.docx",
        "sym_cards":  None,
        "prefix":     "Capitol_Crawl",
        "display":    "The Capitol Crawl: March 12, 1990",
        "grade_range": "Grades 6–10",
        "core_words": [
            'think','know','true','false','same','different','good','bad',
            'strong','weak','because','but','agree','disagree','why',
            'who','what','where','when'
        ],
        # 'disability' added 2026-03-29 — vocabulary framework gap (ADA/Jennifer Keelan context)
        "fringe_words": [
            'crawl','Capitol','steps','protest','law','disability','ADA','ADAPT',
            'source','reliable','corroborate','evidence','claim','verify',
            'contradict'
        ],
        # Top 5 updated 2026-03-29 to center disability rights vocabulary
        "top5_core":   ['because','agree','strong','true','same'],
        "top5_fringe": ['disability','ADA','evidence','claim','corroborate'],
        # Student print pages (zero-indexed) — confirmed 2026-03-29 via PDF keyword scan
        "student_pages": [2, 3, 4, 7, 10, 11, 31, 44, 45, 46, 48, 49],
        "what_inside": [
            "Multi-version informational passages (V1, V2, V3 Lexile ranges)",
            "Source tracking and corroboration framework",
            "Differentiation strategies for all learners",
            "MLL & AAC communication access support",
            "IEP goal stems and SDI documentation tools",
            "Communication Access Packet with ARASAAC vocabulary cards",
            "AAC Communication Session Tracker",
        ],
    },
    "Zitkala-Sa": {
        "folder":     "Zitkala-Sa",
        "unit_pdf":   os.path.join(SCRATCH, "Zitkala-Sa_Lesson_COMPLETE.pdf"),
        "aac_pages":  [11],          # confirmed 2026-03-29: idx 11=Differentiating/Communication Access
        "docx":       "Zitkala-Sa_Lesson_COMPLETE.docx",
        "sym_cards":  "Zitkala-Sa_Symbol_Cards.pdf",
        "prefix":     "Zitkala_Sa",
        "display":    "Zitkala-Ša: Testifying in Her Own Voice",
        "grade_range": "Grades 6–10",
        "core_words": [
            'think','know','feel','why','because','but','and','same',
            'different','change','make','do','help','stop','want','need',
            'right','wrong','good','bad'
        ],
        "fringe_words": [
            'zitkala','boarding','assimilation','dakota','reservation',
            'hair','spirit','testimony','organize'
        ],
        "top5_core":   ['change','need','right','stop','because'],
        "top5_fringe": ['assimilation','boarding','spirit','testimony','reservation'],
        # Student print pages (zero-indexed) — confirmed 2026-03-29 via PDF keyword scan
        "student_pages": [2, 4, 7, 11, 32, 48, 49, 50, 53, 55, 56, 57, 58, 59, 60],
        "what_inside": [
            "Multi-version informational passages (V1, V2, V3 Lexile ranges)",
            "Annotation tools and reading frameworks",
            "Differentiation strategies for all learners",
            "MLL & AAC communication access support",
            "IEP goal stems and SDI documentation tools",
            "Symbol Cards PDF",
            "Communication Access Packet with ARASAAC vocabulary cards",
            "AAC Communication Session Tracker",
        ],
    },
    # Frances Kelsey — rebuilt 2026-03-29 with vocabulary framework alignment
    "Frances Kelsey": {
        "folder":     "Frances Kelsey",
        "unit_pdf":   os.path.join(SCRATCH, "Frances_Kelsey_Unit_COMPLETE.pdf"),
        "aac_pages":  [7, 8, 9],
        "docx":       "Frances_Kelsey_COMPLETE.docx",
        "sym_cards":  "Frances_Kelsey_Symbol_Cards.pdf",
        "prefix":     "Frances_Kelsey",
        "display":    "Frances Kelsey: The Woman Who Said No",
        "grade_range": "Grades 6–10",
        # Full vocabulary added 2026-03-29 (previously empty — framework alignment)
        "core_words": [
            'say','think','know','want','not','good','bad','wrong','right',
            'help','stop','go','more','different','same','because','but',
            'if','true','question','answer','prove','show','tell','believe',
            'strong','weak'
        ],
        "fringe_words": [
            'FDA','drug','safe','test','approve','deny','claim','evidence',
            'reasoning','thalidomide','birth defect','company','pressure',
            'review','scientist','law','protect'
        ],
        "top5_core":   ['not','show','wrong','because','strong'],
        "top5_fringe": ['safe','test','deny','pressure','claim'],
        # Student print pages (zero-indexed) — confirmed 2026-03-29 via PDF keyword scan
        "student_pages": [3, 4, 5, 7, 8, 9, 17, 19, 20, 21, 23, 24, 62, 84, 85],
        "what_inside": [
            "Multi-version informational passages (V1, V2, V3 Lexile ranges)",
            "CER (Claim-Evidence-Reasoning) framework and annotation tools",
            "Differentiation strategies for all learners",
            "MLL & AAC communication access support",
            "IEP goal stems and SDI documentation tools",
            "Symbol Cards PDF",
            "Communication Access Packet with ARASAAC vocabulary cards",
            "AAC Communication Session Tracker",
        ],
    },
}

# ── Shared style helpers ───────────────────────────────────────────────────────

def header_flowable(unit_title):
    hl = ParagraphStyle("hl", fontName="Helvetica-Oblique",
        fontSize=9, textColor=NAVY, leading=13)
    hr = ParagraphStyle("hr", fontName="Helvetica-Bold",
        fontSize=9, textColor=TEAL, leading=13, alignment=TA_RIGHT)
    t = Table([[
        Paragraph(f"<i>{unit_title}</i>", hl),
        Paragraph(
            "<b><font color='#006DA0'>COMMUNICATE</font> "
            "<font color='#FFB703'>BY DESIGN</font></b>", hr),
    ]], colWidths=[4.5*inch, 2.5*inch])
    t.setStyle(TableStyle([
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",    (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
        ("LEFTPADDING",   (0,0), (-1,-1), 0),
        ("RIGHTPADDING",  (0,0), (-1,-1), 0),
    ]))
    return t

def footer_flowable(unit_title):
    fs = ParagraphStyle("fs", fontName="Helvetica", fontSize=7,
        textColor=SLATE, leading=9, alignment=TA_CENTER)
    return Paragraph(
        f"{unit_title}  ·  Communication Access Packet  ·  "
        "Communicate by Design  ·  teacherspayteachers.com/store/communicate-by-design",
        fs)

# ── Top-5 callout page ────────────────────────────────────────────────────────

def build_top5_pdf(unit_cfg) -> bytes:
    unit_title   = unit_cfg["display"]
    TOP5_CORE    = unit_cfg["top5_core"]
    TOP5_FRINGE  = unit_cfg["top5_fringe"]

    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter,
        leftMargin=0.75*inch, rightMargin=0.75*inch,
        topMargin=0.5*inch,  bottomMargin=0.5*inch)

    h1       = ParagraphStyle("h1", fontName="Helvetica-Bold",
                   fontSize=13, textColor=NAVY, leading=17, spaceAfter=6)
    intro    = ParagraphStyle("intro", fontName="Helvetica",
                   fontSize=9, textColor=NAVY, leading=13, spaceAfter=8)
    col_hdr  = ParagraphStyle("ch", fontName="Helvetica-Bold",
                   fontSize=10, textColor=WHITE, leading=13, alignment=TA_CENTER)
    word_lbl = ParagraphStyle("wl", fontName="Helvetica-Bold",
                   fontSize=16, textColor=NAVY, leading=20, alignment=TA_CENTER)

    SYM_SIZE = 72

    def word_cell(w):
        cat    = fk_cat(w)
        border = FKC_BORDER[cat]
        sp     = sym_img_path(w)
        items  = []
        if sp:
            items.append(RLImage(sp, width=SYM_SIZE, height=SYM_SIZE))
        else:
            items.append(Spacer(SYM_SIZE, SYM_SIZE))
        items.append(Spacer(1, 3))
        items.append(Paragraph(w.upper(), word_lbl))
        return items, border

    def make_col(words, hdr_txt, hdr_bg):
        rows        = [[Paragraph(hdr_txt, col_hdr)]]
        row_borders = [None]
        for w in words:
            items, border = word_cell(w)
            rows.append([items])
            row_borders.append(border)
        tbl = Table(rows, colWidths=[3.1*inch])
        style = [
            ("BACKGROUND", (0,0), (0,0), hdr_bg),
            ("BACKGROUND", (0,1), (0,-1), WHITE),
            ("ALIGN",  (0,0), (-1,-1), "CENTER"),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
            ("TOPPADDING",    (0,0), (-1,-1), 5),
            ("BOTTOMPADDING", (0,0), (-1,-1), 5),
            ("LEFTPADDING",   (0,0), (-1,-1), 4),
            ("RIGHTPADDING",  (0,0), (-1,-1), 4),
            ("GRID", (0,0), (-1,-1), 0.75, colors.HexColor("#DDDDDD")),
        ]
        for r_idx, border in enumerate(row_borders[1:], start=1):
            style.append(("BOX", (0, r_idx), (0, r_idx), 2, border))
        tbl.setStyle(TableStyle(style))
        return tbl

    core_col   = make_col(TOP5_CORE,   "TOP 5 CORE WORDS",   TEAL)
    fringe_col = make_col(TOP5_FRINGE, "TOP 5 FRINGE WORDS", NAVY)

    two_col = Table([[core_col, fringe_col]], colWidths=[3.3*inch, 3.3*inch])
    two_col.setStyle(TableStyle([
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING",   (0,0), (-1,-1), 0),
        ("RIGHTPADDING",  (0,0), (-1,-1), 6),
        ("TOPPADDING",    (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
    ]))

    story = [
        header_flowable(unit_title),
        HRFlowable(width="100%", thickness=1.5, color=TEAL, spaceAfter=6),
        Paragraph("Priority Vocabulary for Communication Access", h1),
        Paragraph(
            "These are the highest-priority vocabulary words for this unit. "
            "Core words appear on most AAC systems. "
            "Fringe words are unit-specific — students may use printed cards, "
            "symbols from an existing PEC set, or programmed device pages.",
            intro),
        two_col,
        Spacer(1, 8),
        HRFlowable(width="100%", thickness=0.5, color=TEAL, spaceAfter=3),
        footer_flowable(unit_title),
    ]
    doc.build(story)
    return buf.getvalue()


# ── Symbol card pages ─────────────────────────────────────────────────────────

def build_symbol_pages_pdf(section_title: str, words: list, unit_title: str) -> bytes:
    """3 cols × 4 rows = 12 per page, 2"×2" fixed card size, nested table whitespace."""
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter,
        leftMargin=0.4*inch, rightMargin=0.4*inch,
        topMargin=0.4*inch,  bottomMargin=0.35*inch)

    COLS     = 3
    ROWS     = 4
    PER_PAGE = COLS * ROWS
    CARD_H   = int(2 * inch)
    SYM      = 88

    word_lbl = ParagraphStyle("wl", fontName="Helvetica-Bold",
        fontSize=13, textColor=NAVY, leading=16, alignment=TA_CENTER)
    sec_head = ParagraphStyle("sh", fontName="Helvetica-Bold",
        fontSize=11, textColor=NAVY, leading=14, spaceAfter=4)

    padded = list(words)
    while len(padded) % PER_PAGE != 0:
        padded.append("")
    pages_words = [padded[i:i+PER_PAGE] for i in range(0, len(padded), PER_PAGE)]

    story = []
    for pg_idx, page_words in enumerate(pages_words):
        if pg_idx > 0:
            story.append(PageBreak())

        story.append(header_flowable(unit_title))
        story.append(HRFlowable(width="100%", thickness=1.5, color=TEAL, spaceAfter=4))
        label = section_title if pg_idx == 0 else f"{section_title} (cont.)"
        story.append(Paragraph(label, sec_head))

        rows = [page_words[r*COLS:(r+1)*COLS] for r in range(ROWS)]

        GAP          = 5
        CARD_OUTER_W = (7.7 / 3) * inch
        CARD_INNER_W = CARD_OUTER_W - 2 * GAP
        CARD_INNER_H = CARD_H       - 2 * GAP

        def make_card(w):
            if not w:
                return Spacer(1, 1)
            cat    = fk_cat(w)
            border = FKC_BORDER[cat]
            sp     = sym_img_path(w)
            content = []
            if sp:
                content.append(RLImage(sp, width=SYM, height=SYM))
            else:
                content.append(Spacer(1, SYM))
                ph = ParagraphStyle("ph", fontName="Helvetica-Oblique",
                    fontSize=9, textColor=colors.HexColor("#AAAAAA"),
                    leading=11, alignment=TA_CENTER)
                content.append(Paragraph("(no symbol)", ph))
            content.append(Spacer(1, 4))
            content.append(Paragraph(w.upper(), word_lbl))
            inner = Table([[content]],
                          colWidths=[CARD_INNER_W],
                          rowHeights=[CARD_INNER_H])
            inner.setStyle(TableStyle([
                ("BACKGROUND",    (0,0), (0,0), WHITE),
                ("ALIGN",         (0,0), (0,0), "CENTER"),
                ("VALIGN",        (0,0), (0,0), "MIDDLE"),
                ("TOPPADDING",    (0,0), (0,0), 6),
                ("BOTTOMPADDING", (0,0), (0,0), 6),
                ("LEFTPADDING",   (0,0), (0,0), 4),
                ("RIGHTPADDING",  (0,0), (0,0), 4),
                ("BOX",           (0,0), (0,0), 3, border),
            ]))
            return inner

        grid_data = [[make_card(w) for w in row] for row in rows]
        grid = Table(grid_data,
                     colWidths=[CARD_OUTER_W] * COLS,
                     rowHeights=[CARD_H] * ROWS)
        grid.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (-1,-1), WHITE),
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
        story.append(footer_flowable(unit_title))

    doc.build(story)
    return buf.getvalue()


# ── Welcome to the Product PDF ────────────────────────────────────────────────
#
# UPDATED 2026-03-29 — New structure per TPT folder spec:
#   Page 1: Welcome + What's Inside + What Makes This Product Different
#   Page 2: How to Use This Product + Accessibility Statement + About the Creator + Terms
#
# This is the teacher orientation document. It answers:
#   1. What is this product?
#   2. What makes it different from standard ELA units?
#   3. How do I use it in my classroom?
#
def build_welcome_pdf(unit_cfg) -> bytes:
    """Branded Welcome to the Product PDF — 2-page orientation for TPT folder."""
    unit_title  = unit_cfg["display"]
    grade_range = unit_cfg["grade_range"]
    what_inside = unit_cfg["what_inside"]

    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter,
        leftMargin=0.75*inch, rightMargin=0.75*inch,
        topMargin=0.5*inch,   bottomMargin=0.5*inch)

    h1    = ParagraphStyle("h1", fontName="Helvetica-Bold",
                fontSize=14, textColor=NAVY, leading=18, spaceAfter=4)
    h2    = ParagraphStyle("h2", fontName="Helvetica-Bold",
                fontSize=11, textColor=TEAL, leading=14,
                spaceBefore=10, spaceAfter=4)
    body  = ParagraphStyle("body", fontName="Helvetica",
                fontSize=9, textColor=NAVY, leading=13, spaceAfter=3)
    item  = ParagraphStyle("item", fontName="Helvetica",
                fontSize=9, textColor=NAVY, leading=13,
                leftIndent=12, spaceAfter=2)
    small = ParagraphStyle("small", fontName="Helvetica",
                fontSize=8, textColor=SLATE, leading=11, spaceAfter=2)
    brand_right = ParagraphStyle("br", fontName="Helvetica-Bold",
                      fontSize=9, textColor=TEAL, leading=13, alignment=TA_RIGHT)

    hdr_row = Table([[
        Paragraph(f"<i>{unit_title}</i>",
                  ParagraphStyle("hl", fontName="Helvetica-Oblique",
                      fontSize=9, textColor=NAVY, leading=13)),
        Paragraph(
            "<b><font color='#006DA0'>COMMUNICATE</font> "
            "<font color='#FFB703'>BY DESIGN</font></b>",
            brand_right),
    ]], colWidths=[4.5*inch, 2.5*inch])
    hdr_row.setStyle(TableStyle([
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",    (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
        ("LEFTPADDING",   (0,0), (-1,-1), 0),
        ("RIGHTPADDING",  (0,0), (-1,-1), 0),
    ]))

    # Title block
    title_tbl = Table([[
        Paragraph(f"Welcome to<br/><b>{unit_title}</b>",
                  ParagraphStyle("tt", fontName="Helvetica-Bold",
                      fontSize=16, textColor=WHITE, leading=22, alignment=TA_LEFT)),
        Paragraph(f"<b>{grade_range}<br/>Communicate by Design</b>",
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

    # What's Inside list
    inside_items = []
    for wi in what_inside:
        inside_items.append(Paragraph(f"• {wi}", item))

    story = [
        # ── PAGE 1: Welcome + What's Inside + What Makes This Different ──────
        hdr_row,
        HRFlowable(width="100%", thickness=1.5, color=TEAL, spaceAfter=6),
        title_tbl,
        Spacer(1, 10),

        Paragraph("What's Inside", h2),
        HRFlowable(width="100%", thickness=0.75, color=AMBER, spaceAfter=5),
        *inside_items,
        Spacer(1, 8),

        Paragraph("What Makes This Product Different", h2),
        HRFlowable(width="100%", thickness=0.75, color=AMBER, spaceAfter=5),
        Paragraph(
            "Most ELA units were built for a single learner profile. "
            "This one was built for everyone in the room.",
            body),
        Paragraph(
            "• <b>Three reading versions (V1 / V2 / V3)</b> — same unit question, "
            "same activities, same expectation. The Lexile range varies; the rigor does not. "
            "No ability labels on student materials. Teachers sort; students don't know.",
            item),
        Paragraph(
            "• <b>AAC access built in from the start</b> — not as an add-on. "
            "Every unit includes a Communication Access Packet with ARASAAC symbol cards "
            "for core and fringe vocabulary, a Top 5 Priority Vocabulary page, "
            "and an AAC Session Tracker. The SLP can program fringe vocabulary "
            "before the unit begins using the fringe word list.",
            item),
        Paragraph(
            "• <b>IEP-aligned by design</b> — includes IEP goal stems, "
            "SDI documentation tools (Checkpoint Protocol), and participation pathways "
            "for students who cannot produce written responses.",
            item),
        Paragraph(
            "• <b>Partner guidance embedded</b> — not just for the teacher. "
            "Paraeducators, families, and related service providers each have "
            "a clear role. Three communication partner modes are explained "
            "in the unit itself.",
            item),
        Paragraph(
            "• <b>WCAG 2.2 Level AA</b> — PDFs and Word documents both meet "
            "ADA Title II accessibility standards. "
            "The Word document is fully Google-convertible for digital access.",
            item),

        Spacer(1, 10),
        HRFlowable(width="100%", thickness=0.5, color=TEAL, spaceAfter=3),
        Paragraph(
            f"{unit_title}  ·  Communicate by Design  ·  "
            "teacherspayteachers.com/store/communicate-by-design  ·  "
            "© Communicate by Design. All rights reserved.",
            ParagraphStyle("ft", fontName="Helvetica", fontSize=7,
                textColor=SLATE, leading=9, alignment=TA_CENTER)),

        # ── PAGE 2: How to Use + Accessibility Statement + About + Terms ──────
        PageBreak(),
        hdr_row,
        HRFlowable(width="100%", thickness=1.5, color=TEAL, spaceAfter=6),

        Paragraph("How to Use This Product", h2),
        HRFlowable(width="100%", thickness=0.75, color=AMBER, spaceAfter=5),
        Paragraph(
            "<b>Step 1 — Send the Communication Access Packet to your SLP first.</b> "
            "Allow 1–2 weeks for fringe vocabulary to be programmed before the unit begins. "
            "The CAP is in this folder labeled Communication_Access_Packet.",
            item),
        Paragraph(
            "<b>Step 2 — Run the Vocabulary Preview Routine</b> before Lesson 1. "
            "The 5-minute routine is on the Vocabulary Preview page in the unit. "
            "It introduces the 5 highest-priority words using the Say &amp; Show → "
            "Check → Connect → Flag sequence.",
            item),
        Paragraph(
            "<b>Step 3 — Choose the reading version for each student.</b> "
            "V1 (900–1050 Lexile), V2 (650–800), or V3 (400–550). "
            "The student pages are labeled with small letters or numbers — "
            "Lexile information is never printed on student pages.",
            item),
        Paragraph(
            "<b>Step 4 — Print Student Print Materials.</b> "
            "The Student_Print_Materials PDF contains only the pages students "
            "handle: annotation guide, passages, activities, sentence frames, "
            "evidence sheet, prompt, and rubric. Print and copy from that file.",
            item),
        Paragraph(
            "<b>Step 5 — Open the COMPLETE.docx for everything else.</b> "
            "Teacher reference pages, modeling scripts, checkpoint protocols, "
            "and pacing guides are in the Word document. "
            "Convert to Google Docs if your school uses Google Classroom.",
            item),
        Paragraph(
            "<b>Step 6 — Use the AAC Session Tracker (last page of the CAP).</b> "
            "Record the communication mode each student used each session. "
            "This document supports IEP progress monitoring.",
            item),
        Spacer(1, 6),

        Paragraph("Accessibility Statement", h2),
        HRFlowable(width="100%", thickness=0.75, color=AMBER, spaceAfter=5),
        Paragraph(
            "This product is designed to WCAG 2.2 Level AA standards. "
            "Materials include multi-version passages across three Lexile ranges, "
            "ARASAAC symbol-supported vocabulary, AAC participation pathways, "
            "and IEP-aligned goal stems. Every scaffold varies the access; "
            "the expectation does not change.",
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
        Paragraph(
            f"{unit_title}  ·  Communicate by Design  ·  "
            "teacherspayteachers.com/store/communicate-by-design  ·  "
            "© Communicate by Design. All rights reserved.",
            ParagraphStyle("ft", fontName="Helvetica", fontSize=7,
                textColor=SLATE, leading=9, alignment=TA_CENTER)),
    ]
    doc.build(story)
    return buf.getvalue()


# ── Assemble one Communication Access Packet ──────────────────────────────────

def build_comm_access_packet(unit_name, unit_cfg):
    folder   = os.path.join(NF_ROOT, unit_cfg["folder"])
    prefix   = unit_cfg["prefix"]
    out_path = os.path.join(folder, f"{prefix}_Communication_Access_Packet.pdf")

    unit_reader    = PdfReader(unit_cfg["unit_pdf"])
    tracker_reader = PdfReader(TRACKER)
    writer         = PdfWriter()

    # 1. Real AAC pages from unit
    for idx in unit_cfg["aac_pages"]:
        writer.add_page(unit_reader.pages[idx])

    # 2. Top 5 callout page
    top5_bytes  = build_top5_pdf(unit_cfg)
    top5_reader = PdfReader(io.BytesIO(top5_bytes))
    writer.add_page(top5_reader.pages[0])

    # 3. Core word symbol pages
    core_bytes  = build_symbol_pages_pdf(
        "Core Words", unit_cfg["core_words"], unit_cfg["display"])
    core_reader = PdfReader(io.BytesIO(core_bytes))
    for p in core_reader.pages:
        writer.add_page(p)

    # 4. Fringe word symbol pages
    fringe_bytes  = build_symbol_pages_pdf(
        "Fringe Words — Unit-Specific Vocabulary",
        unit_cfg["fringe_words"], unit_cfg["display"])
    fringe_reader = PdfReader(io.BytesIO(fringe_bytes))
    for p in fringe_reader.pages:
        writer.add_page(p)

    # 5. Tracker
    for p in tracker_reader.pages:
        writer.add_page(p)

    os.makedirs(folder, exist_ok=True)
    with open(out_path, "wb") as f:
        writer.write(f)

    total = len(writer.pages)
    print(f"  ✓ Comm Access Packet: {total} pages  →  {out_path}")
    return out_path


# ── Assemble TPT folder for one unit ─────────────────────────────────────────
#
# UPDATED 2026-03-29 — New 4-component TPT folder standard:
#
#   [prefix]_TPT/
#   ├── [prefix]_Welcome_to_the_Product.pdf   ← Welcome + What Makes Different + How to Use + Terms
#   ├── [prefix]_COMPLETE.docx                ← Full unit Word packet (Google-convertible)
#   ├── [prefix]_Communication_Access_Packet.pdf  ← AAC-specific: unit pages + Top 5 + symbol cards + tracker
#   └── [prefix]_Student_Print_Materials.pdf  ← Print-only student materials (activities, prompts, tools)
#
# RATIONALE:
#   - COMPLETE.docx: teachers can convert to Google Docs for student access
#   - CAP: SLP/AAC team handoff; can't be found anywhere else
#   - Student Print Materials: fast copy-ready packet for student use
#   - Welcome PDF: orientation for the teacher; what makes this different from standard ELA
#
# NOTE on Student Print Materials:
#   This requires a `student_pages` key in the unit config listing PDF page indices.
#   If `student_pages` is not configured or the PDF is missing, this file is skipped
#   with a warning. Add page indices after verifying the COMPLETE.docx PDF export.
#
def assemble_tpt_folder(unit_name, unit_cfg):
    unit_folder = os.path.join(NF_ROOT, unit_cfg["folder"])
    prefix      = unit_cfg["prefix"]
    tpt_folder  = os.path.join(unit_folder, f"{prefix}_TPT")
    os.makedirs(tpt_folder, exist_ok=True)

    copies = []

    # ── 1. Welcome to the Product PDF ─────────────────────────────────────────
    welcome_bytes = build_welcome_pdf(unit_cfg)
    welcome_path  = os.path.join(tpt_folder, f"{prefix}_Welcome_to_the_Product.pdf")
    with open(welcome_path, "wb") as f:
        f.write(welcome_bytes)
    copies.append(f"{prefix}_Welcome_to_the_Product.pdf")

    # Also save to unit root for reference
    welcome_root = os.path.join(unit_folder, f"{prefix}_Welcome_to_the_Product.pdf")
    with open(welcome_root, "wb") as f:
        f.write(welcome_bytes)

    # ── 2. COMPLETE.docx ──────────────────────────────────────────────────────
    if unit_cfg["docx"]:
        # Check unit folder first, then TPT subfolder
        src_docx = os.path.join(unit_folder, unit_cfg["docx"])
        if not os.path.exists(src_docx):
            src_docx = os.path.join(unit_folder, f"{prefix}_TPT", unit_cfg["docx"])
        if os.path.exists(src_docx):
            dst = os.path.join(tpt_folder, f"{prefix}_COMPLETE.docx")
            shutil.copy2(src_docx, dst)
            copies.append(f"{prefix}_COMPLETE.docx")
        else:
            print(f"  ⚠ DOCX not found (build JS script first): {src_docx}")

    # ── 3. Communication Access Packet ────────────────────────────────────────
    cap_src = os.path.join(unit_folder, f"{prefix}_Communication_Access_Packet.pdf")
    if os.path.exists(cap_src):
        dst = os.path.join(tpt_folder, f"{prefix}_Communication_Access_Packet.pdf")
        shutil.copy2(cap_src, dst)
        copies.append(f"{prefix}_Communication_Access_Packet.pdf")
    else:
        print(f"  ⚠ Comm Access Packet not found: {cap_src}")

    # ── 4. Student Print Materials ────────────────────────────────────────────
    student_pages = unit_cfg.get("student_pages")
    unit_pdf_path = unit_cfg.get("unit_pdf")
    if student_pages and unit_pdf_path and os.path.exists(unit_pdf_path):
        try:
            student_bytes = build_student_print_materials(unit_cfg, student_pages)
            spm_path = os.path.join(tpt_folder, f"{prefix}_Student_Print_Materials.pdf")
            with open(spm_path, "wb") as f:
                f.write(student_bytes)
            copies.append(f"{prefix}_Student_Print_Materials.pdf")
        except Exception as e:
            print(f"  ⚠ Student Print Materials failed: {e}")
    else:
        print(f"  ⚠ Student Print Materials: student_pages not configured or unit PDF missing.")
        print(f"      → Add 'student_pages' key to unit config with page indices after PDF export.")

    print(f"  ✓ TPT folder: {tpt_folder}")
    for c in copies:
        print(f"      {c}")
    return tpt_folder


# ── Student Print Materials extractor ────────────────────────────────────────
#
# Extracts print-only student pages from the unit PDF.
# Pages are specified as zero-indexed page indices in the unit config:
#   "student_pages": [list_of_zero_indexed_page_numbers]
#
# Standard student print materials (what gets printed and handed to students):
#   - Annotation Guide / Text Interaction Tool Guide
#   - Sentence Frames
#   - V1 passage + reading activity
#   - V2 passage + reading activity
#   - V3 passage + reading activity
#   - Evidence Recording Sheet
#   - Unit Prompt
#   - Self-Assessment Checklist
#   - Rubric
#   - Research Choice Board
#
# Page indices must be confirmed from the unit PDF after COMPLETE.docx is exported.
#
def build_student_print_materials(unit_cfg, page_indices) -> bytes:
    unit_pdf_path = unit_cfg["unit_pdf"]
    unit_title    = unit_cfg["display"]
    prefix        = unit_cfg["prefix"]

    reader = PdfReader(unit_pdf_path)
    writer = PdfWriter()

    for idx in page_indices:
        if idx < len(reader.pages):
            writer.add_page(reader.pages[idx])
        else:
            print(f"  ⚠ Student page index {idx} out of range (unit has {len(reader.pages)} pages)")

    buf = io.BytesIO()
    writer.write(buf)
    return buf.getvalue()


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("CbD Nonfiction — Communication Access Packets + TPT Folder Build")
    print("=" * 70)

    for unit_name, cfg in UNITS.items():
        print(f"\n{'─'*60}")
        print(f"  {unit_name}")
        print(f"{'─'*60}")

        # Build Comm Access Packet (all units rebuilt with vocabulary framework 2026-03-29)
        if cfg["core_words"] or cfg["fringe_words"]:
            if os.path.exists(cfg["unit_pdf"]):
                print(f"  Building Communication Access Packet…")
                build_comm_access_packet(unit_name, cfg)
            else:
                print(f"  ⚠ Unit PDF not found — skipping CAP build: {cfg['unit_pdf']}")
                print(f"      → Export COMPLETE.docx to PDF first (Word → File → Save As → PDF)")
                print(f"      → Save to scratch: {cfg['unit_pdf']}")
        else:
            print(f"  ⚠ No vocabulary configured for {unit_name} — skipping CAP build")

        # Assemble TPT folder
        print(f"  Assembling TPT folder…")
        assemble_tpt_folder(unit_name, cfg)

    print(f"\n{'='*70}")
    print("Build complete.")
    print(f"{'='*70}")
    print("\nTPT folders ready to zip:")
    for unit_name, cfg in UNITS.items():
        folder = os.path.join(NF_ROOT, cfg["folder"], f"{cfg['prefix']}_TPT")
        print(f"  {folder}")


if __name__ == "__main__":
    main()

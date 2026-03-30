"""
Communication Access Packet — Frances Kelsey
Built for a student using eye gaze (print/cut/laminate for PEC board).

Structure:
  p1    Real unit page — Annotation Tool Options / AAC (idx 6)
  p2    Real unit page — Teacher Support Reference MLL & AAC (idx 7)
  p3    Real unit page — AAC continuation / partner modes (idx 8)
  p4    Real unit page — AT Tools table / IEP Goal Stems (idx 9)
  p5    Top 5 Core + Top 5 Fringe callout (designed — symbol + word)
  p6+   Core word symbol pages — 2x2 gaze-accessible (4 per page)
  pN+   Fringe word symbol pages — 2x2 gaze-accessible (4 per page)
  end   AAC Tracker PDF (appended as-is)
"""

import os, io
from pypdf import PdfReader, PdfWriter
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
from reportlab.platypus.flowables import Image as RLImage

# ── Paths ────────────────────────────────────────────────────────────────────

MNT       = "/sessions/beautiful-wonderful-mendel/mnt/Communicate by Design"
SCRATCH   = "/sessions/beautiful-wonderful-mendel"
SYM_CACHE = os.path.join(MNT, "_Operations/symbol_cache")
UNIT_PDF  = os.path.join(SCRATCH, "Frances_Kelsey_Unit_v2.pdf")
SYM_PDF   = os.path.join(MNT, "Products/Nonfiction Units/Frances Kelsey/Frances_Kelsey_Symbol_Cards.pdf")
TRACKER   = os.path.join(MNT, "Products/Nonfiction Units/AAC_Communication_Session_Tracker.pdf")
OUT_PATH  = os.path.join(MNT, "Products/Nonfiction Units/Frances Kelsey/Frances_Kelsey_Communication_Access_Packet.pdf")

UNIT_TITLE = "Frances Kelsey: The Woman Who Said No"

# ── Brand colors ─────────────────────────────────────────────────────────────

NAVY  = colors.HexColor("#1B1F3B")
TEAL  = colors.HexColor("#006DA0")
AMBER = colors.HexColor("#FFB703")
SLATE = colors.HexColor("#94A3B8")

# ── AAC access language constants ─────────────────────────────────────────────
# Single source of truth. Update here → updates all nonfiction unit output.
# Do not inline these strings elsewhere in this file.

AAC_CORE_NOTE = (
    "Core words are part of most AAC ecosystems. "
    "Fringe words are unit-specific — students may use printed cards, "
    "symbols from an existing PEC set, or programmed device pages."
)

# ── Fitzgerald Key (print-safe, large-cell gaze accessible) ──────────────────

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

VERBS        = {'say','think','know','want','help','stop','show','prove','tell',
                'believe','go','give','protect','approve','deny','claim','test',
                'question','answer','fight','change','mean','care','evaluate',
                'identify','support','decide','create'}
ADJECTIVES   = {'good','bad','wrong','right','more','different','same','true',
                'strong','weak','safe','important','clear'}
PRONOUNS     = {'i','you','he','she','we','they','my','your','who'}
PREPOSITIONS = {'because','but','if','in','on','at','up','yet','as'}
SOCIAL       = {'not','yes','no','please','thank','sorry'}

def fk_cat(word):
    w = word.lower().strip()
    if w in SOCIAL:       return "pink"
    if w in PRONOUNS:     return "yellow"
    if w in VERBS:        return "green"
    if w in ADJECTIVES:   return "orange"
    if w in PREPOSITIONS: return "blue"
    return "white"

def sym_img_path(word):
    p = os.path.join(SYM_CACHE, f"arasaac_{word.lower().replace(' ','_')}.png")
    return p if os.path.exists(p) else None

# ── Running header ────────────────────────────────────────────────────────────

def header_flowable():
    hl = ParagraphStyle("hl", fontName="Helvetica-Oblique",
        fontSize=9, textColor=NAVY, leading=13)
    hr = ParagraphStyle("hr", fontName="Helvetica-Bold",
        fontSize=9, textColor=TEAL, leading=13, alignment=TA_RIGHT)
    t = Table([[
        Paragraph(f"<i>{UNIT_TITLE}</i>", hl),
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

def footer_flowable():
    fs = ParagraphStyle("fs", fontName="Helvetica", fontSize=7,
        textColor=SLATE, leading=9, alignment=TA_CENTER)
    return Paragraph(
        f"{UNIT_TITLE}  ·  Communication Access Packet  ·  "
        "Communicate by Design  ·  teacherspayteachers.com/store/communicate-by-design",
        fs)


# ── Top-5 callout page ────────────────────────────────────────────────────────

TOP5_CORE   = ['not', 'show', 'wrong', 'because', 'strong']
TOP5_FRINGE = ['safe', 'test', 'deny', 'pressure', 'claim']

def build_top5_pdf() -> bytes:
    """Build a single-page Top 5 callout as bytes."""
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter,
        leftMargin=0.75*inch, rightMargin=0.75*inch,
        topMargin=0.5*inch, bottomMargin=0.5*inch)

    h1   = ParagraphStyle("h1", fontName="Helvetica-Bold",
        fontSize=13, textColor=NAVY, leading=17, spaceAfter=6)
    intro = ParagraphStyle("intro", fontName="Helvetica",
        fontSize=9, textColor=NAVY, leading=13, spaceAfter=8)
    col_hdr = ParagraphStyle("ch", fontName="Helvetica-Bold",
        fontSize=10, textColor=colors.white, leading=13, alignment=TA_CENTER)
    word_lbl = ParagraphStyle("wl", fontName="Helvetica-Bold",
        fontSize=16, textColor=NAVY, leading=20, alignment=TA_CENTER)
    fs = ParagraphStyle("fs", fontName="Helvetica", fontSize=7,
        textColor=SLATE, leading=9, alignment=TA_CENTER)

    SYM_SIZE = 72

    def word_cell(w):
        cat    = fk_cat(w)
        border = FKC_BORDER[cat]   # colored outline, white center
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
        rows       = [[Paragraph(hdr_txt, col_hdr)]]
        row_borders = [None]   # header row keeps solid fill, no per-cell BOX needed
        for w in words:
            items, border = word_cell(w)
            rows.append([items])
            row_borders.append(border)
        tbl = Table(rows, colWidths=[3.1*inch])
        style = [
            ("BACKGROUND", (0,0), (0,0), hdr_bg),          # header solid fill
            ("BACKGROUND", (0,1), (0,-1), colors.white),   # word rows — white
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
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING", (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
    ]))

    story = [
        header_flowable(),
        HRFlowable(width="100%", thickness=1.5, color=TEAL, spaceAfter=6),
        Paragraph("Priority Vocabulary for Communication Access", h1),
        Paragraph(
            f"These are the highest-priority vocabulary words for this unit. {AAC_CORE_NOTE}",
            intro),
        two_col,
        Spacer(1, 8),
        HRFlowable(width="100%", thickness=0.5, color=TEAL, spaceAfter=3),
        footer_flowable(),
    ]
    doc.build(story)
    return buf.getvalue()


# ── 2x2 gaze-accessible symbol pages ─────────────────────────────────────────

def build_symbol_pages_pdf(section_title: str, words: list) -> bytes:
    """
    Build symbol grid pages at 3 cols × 4 rows (12 per page) for print/cut/laminate or PEC board.
    Each card is a fixed 2"×2" (144pt). 3 columns fill the printable width; 4 rows per page.
    """
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter,
        leftMargin=0.4*inch, rightMargin=0.4*inch,
        topMargin=0.4*inch, bottomMargin=0.35*inch)

    COLS      = 3
    ROWS      = 4
    PER_PAGE  = COLS * ROWS          # 12 per page
    CARD_H    = int(2 * inch)        # 2" tall — fixed card height
    SYM       = 88                   # pts — symbol image, fits within 2" card

    word_lbl = ParagraphStyle("wl", fontName="Helvetica-Bold",
        fontSize=13, textColor=NAVY, leading=16, alignment=TA_CENTER)
    sec_head = ParagraphStyle("sh", fontName="Helvetica-Bold",
        fontSize=11, textColor=NAVY, leading=14, spaceAfter=4)
    fs = ParagraphStyle("fs", fontName="Helvetica", fontSize=7,
        textColor=SLATE, leading=9, alignment=TA_CENTER)

    # Pad to multiple of 12
    padded = list(words)
    while len(padded) % PER_PAGE != 0:
        padded.append("")

    pages_words = [padded[i:i+PER_PAGE] for i in range(0, len(padded), PER_PAGE)]

    story = []
    for pg_idx, page_words in enumerate(pages_words):
        if pg_idx > 0:
            story.append(PageBreak())

        story.append(header_flowable())
        story.append(HRFlowable(width="100%", thickness=1.5, color=TEAL, spaceAfter=4))
        label = section_title if pg_idx == 0 else f"{section_title} (cont.)"
        story.append(Paragraph(label, sec_head))

        rows = [page_words[r*COLS:(r+1)*COLS] for r in range(ROWS)]

        # ── Nested table approach ──────────────────────────────────────────────
        # Each card is its own inner Table with a FK-colored BOX border.
        # The outer grid Table has padding that creates PHYSICAL white space
        # between cards — actual gap, not just a line between touching borders.
        GAP          = 5                           # pts of white space each side of a card
        CARD_OUTER_W = (7.7 / 3) * inch            # outer cell = full column width
        CARD_INNER_W = CARD_OUTER_W - 2 * GAP      # inner card width after gaps
        CARD_INNER_H = CARD_H       - 2 * GAP      # inner card height after gaps

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
                ("BACKGROUND",    (0,0), (0,0), colors.white),
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


# ── Word lists ────────────────────────────────────────────────────────────────

CORE_WORDS   = ['say','think','know','want','not','good','bad','wrong','right',
                'help','stop','go','more','different','same','because','but','if',
                'true','question','answer','prove','show','tell','believe','strong','weak']

FRINGE_WORDS = ['drug','safe','test','approve','deny','claim','evidence',
                'thalidomide','company','pressure','review','scientist','law','protect']


# ── Assemble final PDF ────────────────────────────────────────────────────────

def build_packet():
    unit_reader    = PdfReader(UNIT_PDF)
    tracker_reader = PdfReader(TRACKER)
    writer         = PdfWriter()

    # 1. Real Communication Access pages from unit (idx 7–9: MLL & AAC dedicated pages)
    for idx in [7, 8, 9]:
        writer.add_page(unit_reader.pages[idx])

    # 2. Top 5 callout page
    top5_bytes   = build_top5_pdf()
    top5_reader  = PdfReader(io.BytesIO(top5_bytes))
    writer.add_page(top5_reader.pages[0])

    # 3. Core word 2x2 symbol pages
    core_bytes   = build_symbol_pages_pdf("Core Words", CORE_WORDS)
    core_reader  = PdfReader(io.BytesIO(core_bytes))
    for p in core_reader.pages:
        writer.add_page(p)

    # 4. Fringe word 2x2 symbol pages
    fringe_bytes  = build_symbol_pages_pdf("Fringe Words — Unit-Specific Vocabulary", FRINGE_WORDS)
    fringe_reader = PdfReader(io.BytesIO(fringe_bytes))
    for p in fringe_reader.pages:
        writer.add_page(p)

    # 5. Tracker PDF
    for p in tracker_reader.pages:
        writer.add_page(p)

    with open(OUT_PATH, "wb") as f:
        writer.write(f)

    total = len(writer.pages)
    print(f"Built: {OUT_PATH}")
    print(f"  Real unit pages (idx 7-9):  3")
    print(f"  Top 5 callout:              1")
    print(f"  Core word grids:            {len(core_reader.pages)}")
    print(f"  Fringe word grids:          {len(fringe_reader.pages)}")
    print(f"  Session Tracker:            {len(tracker_reader.pages)}")
    print(f"  TOTAL: {total} pages")

if __name__ == "__main__":
    build_packet()

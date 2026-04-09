"""
Symbol Pages — All 6 Nonfiction Reading Units
Builds Core Words and Fringe Words symbol grid pages as PDFs.

Gold standard spec — matches build_symbol_pages_picbook.py EXACTLY:
  • Symbol image (ARASAAC PNG, 88pt) OR "(no symbol)" italic placeholder
  • Word label: ALL CAPS, Helvetica-Bold, 13pt, navy, centered
  • FK-colored 3pt border, white background
  • Nothing else — no category bar, no core/fringe label, no star, no POS text

Two sections per unit, each on its own page(s):
  1. Core Words
  2. Fringe Words — Unit-Specific Vocabulary

Grid: 3 columns × 4 rows = 12 cards per page
Card size: 2" × 2" (fixed — NEVER resize)

Word lists sourced from: _Operations/memory/nonfiction_build_reference.md (confirmed/locked)
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
from reportlab.platypus.flowables import Image as RLImage
from pypdf import PdfReader, PdfWriter

# ── Paths ─────────────────────────────────────────────────────────────────────

MNT       = "/sessions/focused-beautiful-johnson/mnt/Communicate by Design"
SYM_CACHE = os.path.join(MNT, "_Operations/Symbols/symbol_cache")
NF_ROOT   = os.path.join(MNT, "Products/Nonfiction Units")

# ── Brand colors ──────────────────────────────────────────────────────────────

NAVY  = colors.HexColor("#1B1F3B")
TEAL  = colors.HexColor("#006DA0")
AMBER = colors.HexColor("#FFB703")
SLATE = colors.HexColor("#94A3B8")

# ── Fitzgerald Key border colors ──────────────────────────────────────────────

FKC_BORDER = {
    "green":  colors.HexColor("#2E7D32"),   # Verbs/Actions
    "orange": colors.HexColor("#E65100"),   # Adjectives/Descriptions
    "yellow": colors.HexColor("#F57F17"),   # Pronouns/People
    "blue":   colors.HexColor("#1565C0"),   # Little Words/Prepositions
    "pink":   colors.HexColor("#880E4F"),   # Social
    "white":  colors.HexColor("#757575"),   # Nouns/Other (gray border)
}

# ── FK word category sets (matches build_comm_access_packet.py exactly) ───────

VERBS        = {'say','think','know','want','help','stop','show','prove','tell',
                'believe','go','give','protect','approve','deny','claim','test',
                'question','answer','fight','change','mean','care','evaluate',
                'identify','support','decide','create','can','crawl','live',
                'place','move','swim','learn','die','agree','disagree','sit',
                'make','need','feel','occupy','organize','protest','sign',
                'demand','verify','corroborate','contradict','result'}
ADJECTIVES   = {'good','bad','wrong','right','more','different','same','true',
                'strong','weak','safe','important','clear','equal','brave',
                'free','best','healthy','sick','wild','fair','federal','reliable'}
PRONOUNS     = {'i','you','he','she','we','they','my','your','who'}
PREPOSITIONS = {'because','but','if','in','on','at','up','yet','as','before',
                'after','which','where','when','why','then','first','last',
                'less','true','false'}
SOCIAL       = {'not','yes','no','please','thank','sorry'}

def fk_cat(word):
    """Return FK color key for a word."""
    w = word.lower().strip().split()[0]  # use first word for multi-word phrases
    if w in SOCIAL:        return "pink"
    if w in PRONOUNS:      return "yellow"
    if w in VERBS:         return "green"
    if w in ADJECTIVES:    return "orange"
    if w in PREPOSITIONS:  return "blue"
    return "white"

def sym_img_path(word):
    """Return path to cached ARASAAC PNG, or None if not found."""
    # Try exact match, then underscore version
    clean = word.lower().replace(' ', '_').replace('-', '_').replace('ā', 'a').replace('š', 's')
    candidates = [
        os.path.join(SYM_CACHE, f"arasaac_{clean}.png"),
        os.path.join(SYM_CACHE, f"arasaac_{word.lower().replace(' ', '_')}.png"),
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return None

# ── Unit vocabulary (from nonfiction_build_reference.md — confirmed/locked) ───

UNITS = {
    "Frances_Kelsey": {
        "title": "Frances Kelsey and the Thalidomide Crisis",
        "short_title": "Frances Kelsey",
        "folder": "Frances Kelsey",
        "tpt_folder": "Frances_Kelsey_TPT",
        "out_name": "Frances_Kelsey_Symbol_Pages.pdf",
        "core": [
            "say","think","know","want","not","good","bad","wrong","right",
            "help","stop","go","more","different","same","because","but","if",
            "true","question","answer","prove","show","tell","believe","strong",
            "weak",
        ],
        "fringe": [
            "drug","safe","test","approve","deny","claim","evidence",
            "thalidomide","company","pressure","review","scientist","law","protect",
        ],
    },
    "504_Sit_In": {
        "title": "504 Sit-In 1977",
        "short_title": "504 Sit-In",
        "folder": "504 Sit In",
        "tpt_folder": "504_Sit_In_TPT",
        "out_name": "504_Sit_In_Symbol_Pages.pdf",
        "core": [
            "people","change","feel","fight","help","make","need","show","sit",
            "stop","tell","think","want","brave","different","fair","free",
            "important","right","safe","same","strong","wrong",
        ],
        "fringe": [
            "approve","crawl","demand","deny","occupy","organize","protest",
            "prove","sign","access","advocate","barrier","building","community",
            "disability","discrimination","equal","federal","government","law",
            "rights","section",
        ],
    },
    "Keiko": {
        "title": "Keiko: A Whale's Journey",
        "short_title": "Keiko",
        "folder": "Keiko",
        "tpt_folder": "Keiko_TPT",
        "out_name": "Keiko_Symbol_Pages.pdf",
        "core": [
            "think","feel","know","good","bad","best","free","live","place",
            "because","why","help","care","same","different","more","less",
            "before","after","true","false","show","mean","prove","first",
            "then","last","which",
        ],
        "fringe": [
            "captivity","ocean","whale","park","sick","healthy","home","family",
            "pod","human","wild","move","swim","learn","die","freedom","safe",
            "danger","company","protect","today",
        ],
    },
    "Radium_Girls": {
        "title": "Radium Girls",
        "short_title": "Radium Girls",
        "folder": "Radium Girls",
        "tpt_folder": "Radium_Girls_TPT",
        "out_name": "Radium_Girls_Symbol_Pages.pdf",
        "core": [
            "think","feel","know","good","bad","right","wrong","because","why",
            "help","stop","fight","change","same","different","more","less",
            "before","after","true","false","show","mean","prove","first",
            "then","last",
        ],
        "fringe": [
            "radium","factory","worker","paint","sick","law","court","safe",
            "danger","company","money","protect","today","bone","doctor","lie",
            "proof",
        ],
    },
    "Capitol_Crawl": {
        "title": "Capitol Crawl 1990",
        "short_title": "Capitol Crawl",
        "folder": "Capitol Crawl",
        "tpt_folder": "Capitol_Crawl_TPT",
        "out_name": "Capitol_Crawl_Symbol_Pages.pdf",
        "core": [
            "think","know","true","false","same","different","good","bad",
            "strong","weak","because","but","agree","disagree","why","who",
            "what","where","when",
        ],
        "fringe": [
            "crawl","Capitol","steps","protest","law","ADA","ADAPT","source",
            "reliable","corroborate","evidence","claim","verify","contradict",
        ],
    },
    "Zitkala_Sa": {
        "title": "Zitkala-Ša",
        "short_title": "Zitkala-Ša",
        "folder": "Zitkala-Sa",
        "tpt_folder": "Zitkala_Sa_TPT",
        "out_name": "Zitkala_Sa_Symbol_Pages.pdf",
        "core": [
            "think","know","feel","why","because","but","and","same","different",
            "change","make","do","help","stop","want","need","right","wrong",
            "good","bad",
        ],
        "fringe": [
            # Tier 2 structural/skill terms — pre-program before Lesson 1
            "cause","effect","problem","solution","structure","organize",
            "result","evidence","policy","identity","culture",
            # Unit-specific content fringe
            "boarding school","assimilation","reservation",
            "hair cutting","spirit","testimony","zitkala","dakota",
        ],
    },
}

# ── Header / footer ────────────────────────────────────────────────────────────

def header_flowable(unit_title):
    hl = ParagraphStyle("hl", fontName="Helvetica-Oblique",
        fontSize=9, textColor=NAVY, leading=13)
    hr = ParagraphStyle("hr", fontName="Helvetica-Bold",
        fontSize=9, textColor=TEAL, leading=13, alignment=TA_RIGHT)
    t = Table([[
        Paragraph(f"<i>{unit_title}</i>", hl),
        Paragraph(
            "<b><font color='#006DA0'>COMMUNICATE</font>"
            " <font color='#FFB703'>BY DESIGN</font></b>",
            hr),
    ]], colWidths=[4.5*inch, 2.5*inch])
    t.setStyle(TableStyle([
        ("VALIGN",         (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",     (0,0), (-1,-1), 0),
        ("BOTTOMPADDING",  (0,0), (-1,-1), 3),
        ("LEFTPADDING",    (0,0), (-1,-1), 0),
        ("RIGHTPADDING",   (0,0), (-1,-1), 0),
    ]))
    return t

def footer_flowable(unit_title):
    fs = ParagraphStyle("fs", fontName="Helvetica", fontSize=7,
        textColor=SLATE, leading=9, alignment=TA_CENTER)
    return Paragraph(
        f"{unit_title}  ·  Communicate by Design  ·  "
        "Pictographic symbols © Government of Aragón. ARASAAC (arasaac.org). "
        "Licensed under CC BY-NC-SA 4.0.",
        fs)

# ── Symbol grid builder ────────────────────────────────────────────────────────

def build_symbol_pages_pdf(section_title: str, words: list, unit_title: str) -> bytes:
    """
    Build symbol grid pages — 3 cols × 4 rows (12 per page).
    Each card: symbol image + ALL CAPS word label + FK-colored border.
    Gold standard spec — identical to picture book build.
    """
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter,
        leftMargin=0.4*inch, rightMargin=0.4*inch,
        topMargin=0.4*inch, bottomMargin=0.35*inch)

    COLS     = 3
    ROWS     = 4
    PER_PAGE = COLS * ROWS    # 12 per page
    CARD_H   = int(2 * inch)  # 2" fixed
    SYM      = 88             # pts — symbol image size

    word_lbl = ParagraphStyle("wl", fontName="Helvetica-Bold",
        fontSize=13, textColor=NAVY, leading=16, alignment=TA_CENTER)
    sec_head = ParagraphStyle("sh", fontName="Helvetica-Bold",
        fontSize=11, textColor=NAVY, leading=14, spaceAfter=4)

    # Pad word list to a multiple of PER_PAGE
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
        CARD_INNER_H = CARD_H - 2 * GAP

        def make_card(w):
            """
            LOCKED spec: symbol image + ALL CAPS word label + FK border.
            No category bar. No core/fringe label. No star. No part-of-speech.
            Empty word → invisible spacer.
            """
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

            inner = Table(
                [[content]],
                colWidths=[CARD_INNER_W],
                rowHeights=[CARD_INNER_H],
            )
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

        grid = Table(
            grid_data,
            colWidths=[CARD_OUTER_W] * COLS,
            rowHeights=[CARD_H] * ROWS,
        )
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
        story.append(footer_flowable(unit_title))

    doc.build(story)
    return buf.getvalue()


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    total_built = 0

    for key, unit in UNITS.items():
        title       = unit["title"]
        short_title = unit["short_title"]
        folder      = unit["folder"]
        tpt_folder  = unit["tpt_folder"]
        out_name    = unit["out_name"]
        core_words  = unit["core"]
        fringe_words = unit["fringe"]

        unit_dir = os.path.join(NF_ROOT, folder)
        tpt_dir  = os.path.join(unit_dir, tpt_folder)
        out_path = os.path.join(tpt_dir, out_name)

        print(f"\n{'='*60}")
        print(f"Building: {short_title}")
        print(f"  Core words: {len(core_words)}  |  Fringe words: {len(fringe_words)}")

        # Check symbols availability
        missing = []
        for w in core_words + fringe_words:
            if not sym_img_path(w):
                missing.append(w)
        if missing:
            print(f"  ⚠ No ARASAAC symbol (will show placeholder): {missing}")

        # Build core section
        core_pdf = build_symbol_pages_pdf("Core Words", core_words, short_title)
        core_reader = PdfReader(io.BytesIO(core_pdf))

        # Build fringe section
        fringe_pdf = build_symbol_pages_pdf(
            "Fringe Words — Unit-Specific Vocabulary", fringe_words, short_title)
        fringe_reader = PdfReader(io.BytesIO(fringe_pdf))

        # Merge into single PDF
        writer = PdfWriter()
        for page in core_reader.pages:
            writer.add_page(page)
        for page in fringe_reader.pages:
            writer.add_page(page)

        # Ensure output dir exists
        os.makedirs(tpt_dir, exist_ok=True)

        with open(out_path, "wb") as f:
            writer.write(f)

        total_pages = len(core_reader.pages) + len(fringe_reader.pages)
        print(f"  ✓ Written: {out_path}")
        print(f"    Core: {len(core_reader.pages)} page(s)  |  Fringe: {len(fringe_reader.pages)} page(s)  |  Total: {total_pages} pages")
        total_built += 1

    print(f"\n{'='*60}")
    print(f"Done. Built symbol pages for {total_built} of {len(UNITS)} units.")


if __name__ == "__main__":
    main()

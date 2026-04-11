"""
cbd_worksheet_templates.py
Communicate by Design — ReportLab Student Worksheet Template System
Version 2.1 | Updated 2026-04-11

PURPOSE
-------
Provides reusable, brand-consistent, modality-neutral student worksheet page
templates for ALL CbD product lines. Single source of truth for student-facing
activity layout. Do not build student worksheet pages outside this module.

CORE DESIGN PHILOSOPHY (v2.1 — locked)
---------------------------------------
These worksheets do not specify how a student responds. Symbol cards glued to
the page, eye gaze + scribe, pencil, typed response on a device — all are valid
and all demonstrate the same skill. The worksheet's job is to make the language
of the skill accessible (via sentence frames and vocabulary design) and to
accept any response modality equally.

The access_note parameter is OPTIONAL and should NEVER instruct the student on
HOW to respond. If used at all, it should only point to language support:
  ✓ "Key vocabulary for this activity is in your communication packet."
  ✗ "Write, type, or use your communication system to respond."  ← wrong
  ✗ "Circle your answer or use gaze to indicate."               ← wrong

If no access_note is passed, nothing is printed. This is the correct default.

PRINT-FIRST DESIGN RULES (v2.0 — locked)
-----------------------------------------
These rules exist because worksheets are printed and written on by hand.
1. NO filled boxes or zones in response areas. White only.
2. NO gray fills anywhere. Students write on these.
3. Zone identity comes from a left-edge colored bar (3pt) + bold label only.
4. Section separation = thin teal horizontal rule (0.75pt), not a filled header.
5. Symbol placeholder = thin dashed border only, no fill.
6. Vocabulary cards = FK-colored 3pt left border only — white background.
7. Writing lines = light gray ruled lines (0.5pt #CCCCCC) with generous spacing.
8. The only color on the page should be the header rule, section labels, and
   FK left borders. Everything the student interacts with is white/black.

DESIGN PRINCIPLES
-----------------
1. Modality-neutral: the layout never assumes a response method. Every activity
   accepts pencil, symbol selection, scribe, AAC device output, or any other
   form of communication as an equally valid response.
2. Language-first: sentence frames and vocabulary design carry the AAC access
   load. The CAP provides the symbol vocabulary — the worksheet does not
   duplicate it. The worksheet's structure maps cleanly onto the language a
   student needs to demonstrate the skill.
3. Visual predictability: same zones in the same positions every time — students
   learn the layout once and transfer it across units and product lines.
4. Print-friendly: white response areas, thin borders, black body text.
5. Version-agnostic structure: same template used for V1/V2/V3 — version label
   in header only, never in activity design.

TEMPLATE CATALOG
----------------
  make_mcq_page()             — Multiple choice questions (4 options, A/B/C/D)
  make_short_answer_page()    — Short answer / open-ended response; word_bank= for V3
  make_cer_page()             — Claim-Evidence-Reasoning organizer; word_bank= for V3
  make_evidence_sort_page()   — Evidence sort / text interaction tool (3 columns)
  make_vocab_preview_page()   — Key vocabulary pre-teaching (Descriptive Teaching Model)
  make_annotation_guide_page()— Annotation guide — 3-code system with tips
  make_descriptor_board_page()— Attribute/description board with composition zone
  make_partner_prompt_card()  — TEACHER document: partner prompt card (goes in Teacher Packet)

VERSION DIFFERENTIATION
-----------------------
  V1/V2/V3 differences are handled through content parameters — NOT separate templates.
  Same function, different data passed in.
    word_bank=None     → V1 or V2 page (nothing printed above questions)
    word_bank=[...]    → V3 page (word strip printed above questions; words from CAP)
    sentence_frame=... → Available on any version; standard scaffold
  The version label appears in the WorksheetDoc header (version_label="V3") — never
  baked into the template functions themselves.

USAGE
-----
  from cbd_worksheet_templates import (
      WorksheetDoc, make_mcq_page, make_short_answer_page,
      make_cer_page, make_evidence_sort_page, make_vocab_preview_page
  )

  doc = WorksheetDoc(
      output_path="output/Frances_Kelsey_Student_Worksheets.pdf",
      unit_title="Frances Kelsey: The Woman Who Said No",
      product_line="Nonfiction Reading Unit",
      version_label=None,   # None = no version label; "V3" for V3 packets
  )
  story = []
  story += make_vocab_preview_page(doc, words=[...])
  story += make_mcq_page(doc, title="Part 1", questions=[...])
  story += make_cer_page(doc, title="Part 2", prompt="Why did...")
  doc.build(story)

DATA FORMATS
------------
mcq_data = [
  {
    "stem": "Why did the FDA want to approve Thalidomide?",
    "options": ["A. It was cheap.", "B. Europe used it.", "C. Kelsey approved it.", "D. No side effects."],
    "has_symbol_zone": False,
  }, ...
]

sa_data = [
  {
    "prompt": "What was one reason Kelsey thought the drug needed more testing?",
    "lines": 4,
    "sentence_frame": None,   # or "Kelsey thought _____ because _____."
    "has_symbol_zone": True,
  }, ...
]
"""

import io
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus.flowables import Image as RLImage

# ═══════════════════════════════════════════════════════════
#  BRAND CONSTANTS
# ═══════════════════════════════════════════════════════════

NAVY  = colors.HexColor("#1B1F3B")
TEAL  = colors.HexColor("#006DA0")
AMBER = colors.HexColor("#FFB703")
SLATE = colors.HexColor("#94A3B8")
WHITE = colors.white
BLACK = colors.black

# Print-safe light rule colors
RULE_COLOR   = colors.HexColor("#CCCCCC")   # writing lines
BORDER_LIGHT = colors.HexColor("#DDDDDD")   # table grid lines
DASHED_COLOR = colors.HexColor("#AAAAAA")   # symbol placeholder border

# Fitzgerald Key left-border colors (3pt left rule on vocab cards)
FKC_BORDER = {
    "green":  colors.HexColor("#2E7D32"),
    "orange": colors.HexColor("#E65100"),
    "yellow": colors.HexColor("#F57F17"),
    "blue":   colors.HexColor("#1565C0"),
    "pink":   colors.HexColor("#880E4F"),
    "white":  colors.HexColor("#757575"),
}

# Fitzgerald Key word categories
_VERBS       = {'say','think','know','want','help','stop','show','prove','tell',
                'believe','go','give','protect','approve','deny','claim','test',
                'question','answer','fight','change','mean','care','evaluate',
                'identify','support','decide','create'}
_ADJECTIVES  = {'good','bad','wrong','right','more','different','same','true',
                'strong','weak','safe','important','clear'}
_PRONOUNS    = {'i','you','he','she','we','they','my','your','who'}
_PREPOSITIONS= {'because','but','if','in','on','at','up','yet','as'}
_SOCIAL      = {'not','yes','no','please','thank','sorry'}

def fk_cat(word: str) -> str:
    w = word.lower().strip()
    if w in _SOCIAL:        return "pink"
    if w in _PRONOUNS:      return "yellow"
    if w in _VERBS:         return "green"
    if w in _ADJECTIVES:    return "orange"
    if w in _PREPOSITIONS:  return "blue"
    return "white"

# ═══════════════════════════════════════════════════════════
#  STYLE FACTORY
# ═══════════════════════════════════════════════════════════

def _styles():
    return {
        "page_title": ParagraphStyle("page_title",
            fontName="Helvetica-Bold", fontSize=13, textColor=NAVY,
            leading=17, spaceAfter=4),
        "page_subtitle": ParagraphStyle("page_subtitle",
            fontName="Helvetica", fontSize=9, textColor=SLATE,
            leading=12, spaceAfter=6),
        "section_label": ParagraphStyle("section_label",
            fontName="Helvetica-Bold", fontSize=10, textColor=TEAL,
            leading=13, spaceAfter=2),
        "section_note": ParagraphStyle("section_note",
            fontName="Helvetica-Oblique", fontSize=8, textColor=SLATE,
            leading=11, spaceAfter=3),
        "body": ParagraphStyle("body",
            fontName="Helvetica", fontSize=10, textColor=BLACK,
            leading=14, spaceAfter=4),
        "question_stem": ParagraphStyle("question_stem",
            fontName="Helvetica-Bold", fontSize=10, textColor=NAVY,
            leading=14, spaceAfter=3),
        "option": ParagraphStyle("option",
            fontName="Helvetica", fontSize=10, textColor=BLACK,
            leading=14, spaceAfter=2, leftIndent=6),
        "frame": ParagraphStyle("frame",
            fontName="Helvetica-Oblique", fontSize=10, textColor=NAVY,
            leading=14, spaceAfter=2),
        "vocab_word": ParagraphStyle("vocab_word",
            fontName="Helvetica-Bold", fontSize=12, textColor=NAVY,
            leading=16, alignment=TA_CENTER),
        "vocab_def": ParagraphStyle("vocab_def",
            fontName="Helvetica", fontSize=9, textColor=BLACK,
            leading=13),
        "header_left": ParagraphStyle("header_left",
            fontName="Helvetica-Oblique", fontSize=9, textColor=NAVY, leading=12),
        "header_right": ParagraphStyle("header_right",
            fontName="Helvetica-Bold", fontSize=9, textColor=TEAL,
            leading=12, alignment=TA_RIGHT),
        "footer": ParagraphStyle("footer",
            fontName="Helvetica", fontSize=7, textColor=SLATE,
            leading=9, alignment=TA_CENTER),
        # CER zone labels — navy text, no fill, left-bar only
        "cer_zone_label": ParagraphStyle("cer_zone_label",
            fontName="Helvetica-Bold", fontSize=11, textColor=NAVY,
            leading=14),
        "cer_zone_sub": ParagraphStyle("cer_zone_sub",
            fontName="Helvetica", fontSize=9, textColor=SLATE,
            leading=12),
        "cer_prompt": ParagraphStyle("cer_prompt",
            fontName="Helvetica-Bold", fontSize=10, textColor=NAVY,
            leading=14, spaceAfter=4),
        "access_note": ParagraphStyle("access_note",
            fontName="Helvetica-Oblique", fontSize=8, textColor=SLATE,
            leading=11),
    }

# ═══════════════════════════════════════════════════════════
#  WORKSHEET DOC
# ═══════════════════════════════════════════════════════════

class WorksheetDoc:
    """
    Manages page setup, running header, and footer for all worksheet pages.
    Pass an instance to every make_*_page() function.
    """
    def __init__(self, output_path: str, unit_title: str,
                 product_line: str = "Communicate by Design",
                 version_label: str = None,
                 left_margin: float = 0.75,
                 right_margin: float = 0.75,
                 top_margin: float = 0.6,
                 bottom_margin: float = 0.5):
        self.output_path   = output_path
        self.unit_title    = unit_title
        self.product_line  = product_line
        self.version_label = version_label
        self.lm = left_margin * inch
        self.rm = right_margin * inch
        self.tm = top_margin * inch
        self.bm = bottom_margin * inch
        self.usable_width = 8.5 * inch - self.lm - self.rm
        self.S = _styles()
        self._doc = SimpleDocTemplate(
            output_path, pagesize=letter,
            leftMargin=self.lm, rightMargin=self.rm,
            topMargin=self.tm, bottomMargin=self.bm,
        )

    def header(self) -> Table:
        S = self.S
        right_content = (
            "<b><font color='#006DA0'>COMMUNICATE</font> "
            "<font color='#FFB703'>BY DESIGN</font></b>"
        )
        if self.version_label:
            right_content += f"   <b><font color='#1B1F3B'>{self.version_label}</font></b>"
        t = Table([[
            Paragraph(f"<i>{self.unit_title}</i>", S["header_left"]),
            Paragraph(right_content, S["header_right"]),
        ]], colWidths=[self.usable_width * 0.55, self.usable_width * 0.45])
        t.setStyle(TableStyle([
            ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
            ("TOPPADDING",    (0,0), (-1,-1), 0),
            ("BOTTOMPADDING", (0,0), (-1,-1), 3),
            ("LEFTPADDING",   (0,0), (-1,-1), 0),
            ("RIGHTPADDING",  (0,0), (-1,-1), 0),
        ]))
        return t

    def divider(self, thickness: float = 1.5, color=None, space_after: float = 6):
        return HRFlowable(
            width="100%", thickness=thickness,
            color=color or TEAL, spaceAfter=space_after
        )

    def thin_rule(self, space_before: float = 6, space_after: float = 6):
        """Light gray section separator — no ink cost."""
        return HRFlowable(
            width="100%", thickness=0.5,
            color=RULE_COLOR,
            spaceBefore=space_before, spaceAfter=space_after
        )

    def footer(self) -> Paragraph:
        return Paragraph(
            f"{self.unit_title}  ·  {self.product_line}  ·  "
            "Communicate by Design  ·  "
            "teacherspayteachers.com/store/communicate-by-design",
            self.S["footer"]
        )

    def page_header_block(self, title: str, subtitle: str = None) -> list:
        S = self.S
        out = [self.header(), self.divider(),
               Paragraph(title, S["page_title"])]
        if subtitle:
            out.append(Paragraph(subtitle, S["page_subtitle"]))
        return out

    def build(self, story: list):
        self._doc.build(story)
        print(f"✓ Worksheet PDF written: {self.output_path}")

    def build_to_bytes(self, story: list) -> bytes:
        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=letter,
            leftMargin=self.lm, rightMargin=self.rm,
            topMargin=self.tm, bottomMargin=self.bm)
        doc.build(story)
        return buf.getvalue()


# ═══════════════════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════════════════

def _writing_lines(width: float, count: int = 4,
                   line_spacing: float = 0.30) -> list:
    """
    Returns a list of flowables: ruled writing lines with generous spacing.
    White background — no fill. Students write directly on these.
    """
    items = []
    for _ in range(count):
        items.append(
            HRFlowable(width=width, thickness=0.5,
                       color=RULE_COLOR, spaceAfter=2)
        )
        items.append(Spacer(1, line_spacing * inch))
    return items


def _zone_label_row(label: str, sublabel: str, bar_color,
                    usable_width: float, S: dict) -> Table:
    """
    Print-safe zone label: 3pt colored left bar + bold label + sublabel.
    No fill. No header block. Just a left accent bar and text.
    Used for CER zone headers and section breaks.
    """
    content = [
        Paragraph(f"<b>{label}</b>", S["cer_zone_label"]),
        Paragraph(sublabel, S["cer_zone_sub"]),
    ]
    t = Table([[content]], colWidths=[usable_width])
    t.setStyle(TableStyle([
        ("LINEBEFORE",    (0,0), (0,0), 3, bar_color),
        ("TOPPADDING",    (0,0), (0,0), 4),
        ("BOTTOMPADDING", (0,0), (0,0), 4),
        ("LEFTPADDING",   (0,0), (0,0), 8),
        ("RIGHTPADDING",  (0,0), (0,0), 0),
        ("BACKGROUND",    (0,0), (0,0), WHITE),
    ]))
    return t


def _word_bank(words: list, usable_width: float, label: str = "Key Words") -> Table:
    """
    Renders a vocabulary reference strip — a bordered row of words students can
    circle, point to, or reference when composing their response.

    Print-first: white background, teal left bar (3pt), light gray outer box.
    Words are laid out inline, bold, separated by a thin divider.

    Label is "Key Words" (not "Word Bank") — the strip is a reference, not a
    one-word fill-in cue. Sentence frames should use "..." or ":" as a
    continuation marker, never a single ___ blank.

    This is a V3 scaffold. V1/V2 pages pass word_bank=None — nothing is printed.
    The words here should be the same vocabulary from the CAP — not new words.
    The word bank reduces the retrieval demand; the comprehension task stays the same.
    """
    word_style = ParagraphStyle("wb_word",
        fontName="Helvetica-Bold", fontSize=10,
        textColor=NAVY, leading=14)
    label_style = ParagraphStyle("wb_label",
        fontName="Helvetica-Oblique", fontSize=8,
        textColor=SLATE, leading=11)

    # Build word cells — each word in its own mini-cell, separated by light borders
    word_cells = []
    for w in words:
        word_cells.append(Paragraph(w, word_style))

    # Single-row table of words
    n = len(word_cells)
    if n == 0:
        return Spacer(1, 0)

    col_w = (usable_width - 0.6 * inch) / n  # leave room for label column
    words_tbl = Table([word_cells], colWidths=[col_w] * n)
    words_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), WHITE),
        ("GRID",          (0,0), (-1,-1), 0.5, BORDER_LIGHT),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
        ("RIGHTPADDING",  (0,0), (-1,-1), 6),
        ("ALIGN",         (0,0), (-1,-1), "CENTER"),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ]))

    # Outer wrapper — teal left bar + label column
    wrapper = Table(
        [[Paragraph(label, label_style), words_tbl]],
        colWidths=[0.6 * inch, usable_width - 0.6 * inch]
    )
    wrapper.setStyle(TableStyle([
        ("LINEBEFORE",    (0,0), (0,0), 3, TEAL),
        ("BACKGROUND",    (0,0), (-1,-1), WHITE),
        ("BOX",           (0,0), (-1,-1), 0.5, BORDER_LIGHT),
        ("TOPPADDING",    (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LEFTPADDING",   (0,0), (0,0), 6),
        ("RIGHTPADDING",  (0,0), (-1,-1), 0),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ]))
    return wrapper


def _symbol_placeholder(width: float = 1.0, height: float = 1.0) -> Table:
    """
    Thin dashed-border symbol card placeholder. No fill.
    Students or teachers affix a physical symbol card here.
    """
    label_style = ParagraphStyle("sym_ph", fontName="Helvetica-Oblique",
        fontSize=7, textColor=SLATE, leading=10, alignment=TA_CENTER)
    t = Table(
        [[Paragraph("symbol", label_style)]],
        colWidths=[width * inch],
        rowHeights=[height * inch]
    )
    t.setStyle(TableStyle([
        ("BOX",           (0,0), (0,0), 0.75, DASHED_COLOR),
        ("BACKGROUND",    (0,0), (0,0), WHITE),
        ("ALIGN",         (0,0), (0,0), "CENTER"),
        ("VALIGN",        (0,0), (0,0), "MIDDLE"),
        ("TOPPADDING",    (0,0), (0,0), 4),
        ("BOTTOMPADDING", (0,0), (0,0), 4),
    ]))
    return t


# ═══════════════════════════════════════════════════════════
#  TEMPLATE 1: MCQ PAGE
# ═══════════════════════════════════════════════════════════

def make_mcq_page(doc: WorksheetDoc, title: str, questions: list,
                  access_note: str = None) -> list:
    """
    Multiple choice question page.
    Each question: numbered stem + 4 options with ○ circle for circling.
    Optional left symbol placeholder column.

    Each question dict:
      stem           : str
      options        : list[str] — 4 options (include letter: "A. ...")
      has_symbol_zone: bool — left symbol column (default False)
    """
    S = doc.S
    usable = doc.usable_width
    story = doc.page_header_block(title)

    if access_note:
        story.append(Paragraph(access_note, S["access_note"]))
        story.append(Spacer(1, 8))

    for i, q in enumerate(questions):
        stem         = q.get("stem") or q.get("text", "")
        options      = q.get("options") or [f"{ltr}  {txt}" for ltr, txt in q.get("choices", [])]
        has_sym      = q.get("has_symbol_zone", False)
        sym_w        = 1.0 * inch if has_sym else 0
        gap          = 0.1 * inch if has_sym else 0
        content_w    = usable - sym_w - gap

        q_content = [Paragraph(f"{i+1}.  {stem}", S["question_stem"])]
        for opt in options:
            q_content.append(Paragraph(f"○  {opt}", S["option"]))
        q_content.append(Spacer(1, 8))

        if has_sym:
            sym_cell = _symbol_placeholder(width=sym_w / inch, height=0.9)
            row = [[sym_cell, q_content]]
            col_widths = [sym_w, content_w]
        else:
            row = [[q_content]]
            col_widths = [content_w]

        q_table = Table(row, colWidths=col_widths)
        q_table.setStyle(TableStyle([
            ("VALIGN",        (0,0), (-1,-1), "TOP"),
            ("TOPPADDING",    (0,0), (-1,-1), 0),
            ("BOTTOMPADDING", (0,0), (-1,-1), 0),
            ("LEFTPADDING",   (0,0), (-1,-1), 0),
            ("RIGHTPADDING",  (0,0), (-1,-1), 0),
            ("LINEBELOW",     (0,0), (-1,-1), 0.5, BORDER_LIGHT),
        ]))
        story.append(KeepTogether(q_table))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 8))
    story.append(doc.thin_rule(space_before=4, space_after=3))
    story.append(doc.footer())
    story.append(PageBreak())
    return story


# ═══════════════════════════════════════════════════════════
#  TEMPLATE 2: SHORT ANSWER PAGE
# ═══════════════════════════════════════════════════════════

def make_short_answer_page(doc: WorksheetDoc, title: str, questions: list,
                            word_bank: list = None,
                            access_note: str = None) -> list:
    """
    Short answer page with optional sentence frames and optional word bank.
    Response areas are plain ruled lines — white, no fill.

    word_bank : list[str] or None
        V3 scaffold — a strip of vocabulary words printed above all questions.
        Students circle, point to, or reference these words when composing
        their response. Words should come from the CAP — not new vocabulary.
        Pass None (default) for V1/V2 — nothing is printed.

    Each question dict:
      prompt / text    : str
      lines            : int — writing lines (default 4)
      sentence_frame / frame : str or None
    """
    S = doc.S
    usable = doc.usable_width
    story = doc.page_header_block(title)

    if access_note:
        story.append(Paragraph(access_note, S["access_note"]))
        story.append(Spacer(1, 8))

    # Word bank — V3 only; renders above all questions
    if word_bank:
        story.append(_word_bank(word_bank, usable))
        story.append(Spacer(1, 10))

    for i, q in enumerate(questions):
        prompt       = q.get("prompt") or q.get("text", "")
        n_lines      = q.get("lines", 4)
        frame        = q.get("sentence_frame") or q.get("frame", None)
        has_sym      = q.get("has_symbol_zone", False)
        sym_w        = 1.0 * inch if has_sym else 0
        gap          = 0.1 * inch if has_sym else 0
        content_w    = usable - sym_w - gap

        content = [Paragraph(f"{i+1}.  {prompt}", S["question_stem"])]
        if frame:
            content.append(Spacer(1, 3))
            content.append(Paragraph(frame, S["frame"]))
        content.append(Spacer(1, 5))
        content += _writing_lines(content_w, count=n_lines)
        content.append(Spacer(1, 6))

        if has_sym:
            sym_cell = _symbol_placeholder(width=sym_w / inch, height=0.9)
            row = [[sym_cell, content]]
            col_widths = [sym_w, content_w]
        else:
            row = [[content]]
            col_widths = [content_w]

        q_table = Table(row, colWidths=col_widths)
        q_table.setStyle(TableStyle([
            ("VALIGN",        (0,0), (-1,-1), "TOP"),
            ("TOPPADDING",    (0,0), (-1,-1), 0),
            ("BOTTOMPADDING", (0,0), (-1,-1), 0),
            ("LEFTPADDING",   (0,0), (-1,-1), 0),
            ("RIGHTPADDING",  (0,0), (-1,-1), 0),
        ]))
        story.append(KeepTogether(q_table))

    story.append(doc.thin_rule(space_before=4, space_after=3))
    story.append(doc.footer())
    story.append(PageBreak())
    return story


# ═══════════════════════════════════════════════════════════
#  TEMPLATE 3: CER ORGANIZER PAGE
# ═══════════════════════════════════════════════════════════

def make_cer_page(doc: WorksheetDoc, title: str, prompt: str,
                  claim_frame: str = None,
                  evidence_slots: int = 2,
                  reasoning_lines: int = 3,
                  word_bank: list = None,
                  access_note: str = None) -> list:
    """
    Claim-Evidence-Reasoning organizer.
    Three zones identified by left-bar color + bold label.
    NO filled headers. NO gray zones. White throughout.

    word_bank : list[str] or None
        V3 scaffold — printed above the question prompt. Same as make_short_answer_page().
        Students reference these words when writing their Claim, Evidence, and Reasoning.
        Pass None (default) for V1/V2.

    Zone colors:
      CLAIM     — amber left bar  (#FFB703)
      EVIDENCE  — teal left bar   (#006DA0)
      REASONING — navy left bar   (#1B1F3B)
    """
    S = doc.S
    usable = doc.usable_width
    story = doc.page_header_block(title)

    if access_note:
        story.append(Paragraph(access_note, S["access_note"]))
        story.append(Spacer(1, 6))

    # Word bank — V3 only; renders above the question prompt
    if word_bank:
        story.append(_word_bank(word_bank, usable))
        story.append(Spacer(1, 10))

    # ── Question prompt (thin teal left bar only) ─────────────────────────────
    prompt_row = Table(
        [[Paragraph(f"<b>Question:</b>  {prompt}", S["cer_prompt"])]],
        colWidths=[usable]
    )
    prompt_row.setStyle(TableStyle([
        ("LINEBEFORE",    (0,0), (0,0), 3, TEAL),
        ("BACKGROUND",    (0,0), (0,0), WHITE),
        ("TOPPADDING",    (0,0), (0,0), 5),
        ("BOTTOMPADDING", (0,0), (0,0), 5),
        ("LEFTPADDING",   (0,0), (0,0), 8),
        ("RIGHTPADDING",  (0,0), (0,0), 0),
    ]))
    story.append(prompt_row)
    story.append(Spacer(1, 10))

    # ── CLAIM zone ────────────────────────────────────────────────────────────
    story.append(_zone_label_row("CLAIM", "My answer to the question",
                                 AMBER, usable, S))
    story.append(Spacer(1, 4))
    if claim_frame:
        story.append(Paragraph(claim_frame, S["frame"]))
        story.append(Spacer(1, 3))
    story += _writing_lines(usable, count=2)
    story.append(doc.thin_rule(space_before=8, space_after=8))

    # ── EVIDENCE zones ────────────────────────────────────────────────────────
    story.append(_zone_label_row("EVIDENCE", "Proof from the text — quote or paraphrase",
                                 TEAL, usable, S))
    story.append(Spacer(1, 6))

    n_slots = len(evidence_slots) if isinstance(evidence_slots, list) else evidence_slots
    slot_labels = evidence_slots if isinstance(evidence_slots, list) else [f"Evidence {i+1}:" for i in range(n_slots)]

    for slot_i, slot_label in enumerate(slot_labels):
        story.append(Paragraph(slot_label, S["section_label"]))
        story.append(Paragraph("Quote or describe what the text says:", S["section_note"]))
        story += _writing_lines(usable, count=2)
        story.append(Paragraph("This matters because:", S["section_note"]))
        story += _writing_lines(usable, count=1)
        if slot_i < n_slots - 1:
            story.append(doc.thin_rule(space_before=4, space_after=6))

    story.append(doc.thin_rule(space_before=8, space_after=8))

    # ── REASONING zone ────────────────────────────────────────────────────────
    story.append(_zone_label_row("REASONING", "How your evidence supports your claim",
                                 NAVY, usable, S))
    story.append(Spacer(1, 4))
    story += _writing_lines(usable, count=reasoning_lines)
    story.append(Spacer(1, 8))

    story.append(doc.thin_rule(space_before=4, space_after=3))
    story.append(doc.footer())
    story.append(PageBreak())
    return story


# ═══════════════════════════════════════════════════════════
#  TEMPLATE 4: EVIDENCE SORT / TEXT INTERACTION TOOL
# ═══════════════════════════════════════════════════════════

def make_evidence_sort_page(doc: WorksheetDoc, title: str,
                             columns: list, prompt: str = None,
                             access_note: str = None) -> list:
    """
    3-column evidence sort / text interaction tool.
    Column headers use colored left borders and bold labels — no fills.
    Grid lines are light gray (print-safe).

    columns : list of 3 dicts —
        "header"  : str — column label (e.g. "H")
        "subhead" : str — descriptor
        "color"   : color — left bar color for the header cell
        "lines"   : int — writing lines per row (default 3)
        "rows"    : int — evidence rows (default 4)
    """
    S = doc.S
    usable = doc.usable_width
    story = doc.page_header_block(title)

    if access_note:
        story.append(Paragraph(access_note, S["access_note"]))

    if prompt:
        story.append(Spacer(1, 4))
        story.append(Paragraph(prompt, S["body"]))
    story.append(Spacer(1, 8))

    if len(columns) != 3:
        raise ValueError("make_evidence_sort_page requires exactly 3 columns.")

    col_w = usable / 3
    max_rows = max(c.get("rows", 4) for c in columns)
    n_lines  = max(c.get("lines", 3) for c in columns)

    # Header row — left bar + label, white background
    hdr_cells = []
    for col in columns:
        hdr_content = [
            Paragraph(f"<b>{col['header']}</b>", ParagraphStyle(
                "es_hdr", fontName="Helvetica-Bold", fontSize=13,
                textColor=NAVY, leading=17)),
            Paragraph(col.get("subhead", ""), ParagraphStyle(
                "es_sub", fontName="Helvetica", fontSize=8,
                textColor=SLATE, leading=11)),
        ]
        hdr_cells.append(hdr_content)

    hdr_tbl = Table([hdr_cells], colWidths=[col_w] * 3)
    hdr_style = [
        ("BACKGROUND",    (0,0), (-1,-1), WHITE),
        ("GRID",          (0,0), (-1,-1), 0.75, BORDER_LIGHT),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("RIGHTPADDING",  (0,0), (-1,-1), 6),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
    ]
    for ci, col in enumerate(columns):
        hdr_style.append(("LINEBEFORE", (ci,0), (ci,0), 3, col.get("color", NAVY)))
    hdr_tbl.setStyle(TableStyle(hdr_style))
    story.append(hdr_tbl)

    # Data rows — white, light grid
    for _ in range(max_rows):
        row_cells = []
        for _ in columns:
            cell = []
            for li in range(n_lines):
                cell.append(
                    HRFlowable(width="100%", thickness=0.5,
                               color=RULE_COLOR, spaceAfter=1)
                )
                cell.append(Spacer(1, 0.24 * inch))
            row_cells.append(cell)

        data_row = Table([row_cells], colWidths=[col_w] * 3)
        data_row.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (-1,-1), WHITE),
            ("GRID",          (0,0), (-1,-1), 0.5, BORDER_LIGHT),
            ("TOPPADDING",    (0,0), (-1,-1), 6),
            ("BOTTOMPADDING", (0,0), (-1,-1), 6),
            ("LEFTPADDING",   (0,0), (-1,-1), 6),
            ("RIGHTPADDING",  (0,0), (-1,-1), 6),
            ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ]))
        story.append(data_row)

    story.append(Spacer(1, 8))
    story.append(doc.thin_rule(space_before=4, space_after=3))
    story.append(doc.footer())
    story.append(PageBreak())
    return story


# ═══════════════════════════════════════════════════════════
#  TEMPLATE 5: VOCABULARY PREVIEW PAGE
# ═══════════════════════════════════════════════════════════

def make_vocab_preview_page(doc: WorksheetDoc, words: list,
                             title: str = "Key Vocabulary — Before You Read",
                             sym_cache_path: str = None,
                             access_note: str = None) -> list:
    """
    Vocabulary pre-teaching page using the Descriptive Teaching Model.
    Each word: FK-colored 3pt left border (no fill) + symbol image + word +
    definition + 4-step teaching routine table.

    words : list of dicts —
        "word"       : str
        "definition" : str — plain-language student-facing definition
        "example"    : str or None — use in a sentence from the passage
        "is_core"    : bool — True = core word (★)

    sym_cache_path : str or None — path to symbol_cache folder
    """
    S = doc.S
    usable = doc.usable_width

    story = doc.page_header_block(title)
    if access_note:
        story.append(Paragraph(access_note, S["access_note"]))
        story.append(Spacer(1, 8))

    # Symbol size — LOCKED at 88pt (matches build_comm_access_packet.py spec)
    SYM_SIZE  = 88   # pts — do not change
    SYM_COL_W = 1.5 * inch   # 108pt usable — holds 88pt image with padding

    for w in words:
        word       = w.get("word", "")
        definition = w.get("definition", "")
        example    = w.get("example", None)
        is_core    = w.get("is_core", False)
        cat        = fk_cat(word)
        fk_border  = FKC_BORDER[cat]
        star_label = "★ core" if is_core else "fringe"

        # Symbol column
        sym_col = []
        if sym_cache_path:
            sym_path = os.path.join(
                sym_cache_path,
                f"arasaac_{word.lower().replace(' ', '_')}.png"
            )
            if os.path.exists(sym_path):
                sym_col.append(RLImage(sym_path, width=SYM_SIZE, height=SYM_SIZE))
            else:
                sym_col.append(Spacer(SYM_SIZE, SYM_SIZE))
        else:
            sym_col.append(Spacer(SYM_SIZE, SYM_SIZE))
        sym_col.append(Spacer(1, 3))
        sym_col.append(Paragraph(word.upper(), S["vocab_word"]))
        sym_col.append(Paragraph(star_label, ParagraphStyle(
            "star", fontName="Helvetica", fontSize=7,
            textColor=SLATE, leading=9, alignment=TA_CENTER)))

        # Definition column
        def_col_w = usable - SYM_COL_W - 0.1 * inch
        def_col = [Paragraph(definition, S["vocab_def"])]
        if example:
            def_col.append(Spacer(1, 3))
            def_col.append(Paragraph(
                f"<i>In the text: {example}</i>",
                ParagraphStyle("vex", fontName="Helvetica-Oblique",
                    fontSize=9, textColor=SLATE, leading=12)
            ))
        def_col.append(Spacer(1, 5))

        # 4-step teaching routine
        routine = [
            ["Say & Show", "Partner says the word and points to the symbol."],
            ["Check",      "Find the word on your device or word card."],
            ["Connect",    "Partner uses the word in a sentence from the passage."],
            ["Flag",       "Mark or flag the word when you see it in the text."],
        ]
        routine_rows = []
        for step, desc in routine:
            routine_rows.append([
                Paragraph(f"<b>{step}</b>", S["section_note"]),
                Paragraph(desc, S["access_note"]),
            ])
        routine_tbl = Table(routine_rows,
                            colWidths=[1.1 * inch, def_col_w - 1.2 * inch])
        routine_tbl.setStyle(TableStyle([
            ("GRID",          (0,0), (-1,-1), 0.5, BORDER_LIGHT),
            ("BACKGROUND",    (0,0), (-1,-1), WHITE),
            ("TOPPADDING",    (0,0), (-1,-1), 3),
            ("BOTTOMPADDING", (0,0), (-1,-1), 3),
            ("LEFTPADDING",   (0,0), (-1,-1), 4),
            ("RIGHTPADDING",  (0,0), (-1,-1), 4),
            ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ]))
        def_col.append(routine_tbl)

        # Word card — FK 3pt left border only, white background
        word_card = Table(
            [[sym_col, def_col]],
            colWidths=[SYM_COL_W, def_col_w]
        )
        word_card.setStyle(TableStyle([
            ("LINEBEFORE",    (0,0), (0,0), 3, fk_border),
            ("BACKGROUND",    (0,0), (-1,-1), WHITE),
            ("BOX",           (0,0), (-1,-1), 0.5, BORDER_LIGHT),
            ("TOPPADDING",    (0,0), (-1,-1), 6),
            ("BOTTOMPADDING", (0,0), (-1,-1), 6),
            ("LEFTPADDING",   (0,0), (-1,-1), 6),
            ("RIGHTPADDING",  (0,0), (-1,-1), 6),
            ("VALIGN",        (0,0), (-1,-1), "TOP"),
            ("ALIGN",         (0,0), (0,0), "CENTER"),
        ]))
        story.append(KeepTogether(word_card))
        story.append(Spacer(1, 8))

    story.append(doc.thin_rule(space_before=4, space_after=3))
    story.append(doc.footer())
    story.append(PageBreak())
    return story


# ═══════════════════════════════════════════════════════════
#  TEMPLATE 6: ANNOTATION GUIDE PAGE
# ═══════════════════════════════════════════════════════════

def make_annotation_guide_page(doc: WorksheetDoc,
                                codes: list,
                                title: str = "Annotation Guide",
                                tips: list = None) -> list:
    """
    1-page annotation guide: 3 code cards + optional tips.
    Code badge = colored box (small, minimal ink) + label + example.
    No large fills.

    codes : list of 3 dicts —
        "code"    : str — annotation symbol (e.g. "H")
        "label"   : str — what it means
        "example" : str — example of what to look for
        "color"   : color — badge background color
    """
    S = doc.S
    usable = doc.usable_width
    story = doc.page_header_block(title,
        subtitle="Use these codes to mark the text as you read.")

    if len(codes) != 3:
        raise ValueError("make_annotation_guide_page requires exactly 3 codes.")

    col_w = usable / 3

    # Code cards — small colored badge (the only fill on the page), white card body
    code_cells = []
    for code in codes:
        badge_style = ParagraphStyle("badge",
            fontName="Helvetica-Bold", fontSize=20,
            textColor=WHITE, leading=24, alignment=TA_CENTER)
        badge = Table(
            [[Paragraph(code["code"], badge_style)]],
            colWidths=[0.5 * inch], rowHeights=[0.5 * inch]
        )
        badge.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (0,0), code.get("color", NAVY)),
            ("ALIGN",         (0,0), (0,0), "CENTER"),
            ("VALIGN",        (0,0), (0,0), "MIDDLE"),
            ("TOPPADDING",    (0,0), (0,0), 0),
            ("BOTTOMPADDING", (0,0), (0,0), 0),
        ]))
        cell = [
            badge,
            Spacer(1, 4),
            Paragraph(f"<b>{code['label']}</b>", S["section_label"]),
            Spacer(1, 3),
            Paragraph(code.get("example", ""), S["body"]),
        ]
        code_cells.append(cell)

    codes_tbl = Table([code_cells], colWidths=[col_w] * 3)
    codes_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), WHITE),
        ("GRID",          (0,0), (-1,-1), 0.5, BORDER_LIGHT),
        ("TOPPADDING",    (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("RIGHTPADDING",  (0,0), (-1,-1), 8),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
    ]))
    story.append(codes_tbl)
    story.append(Spacer(1, 12))

    if tips:
        story.append(Paragraph("Tips:", S["section_label"]))
        story.append(Spacer(1, 4))
        for tip in tips:
            story.append(Paragraph(f"•  {tip}", S["body"]))
            story.append(Spacer(1, 3))

    story.append(Spacer(1, 10))
    story.append(doc.thin_rule(space_before=4, space_after=3))
    story.append(doc.footer())
    story.append(PageBreak())
    return story


# ═══════════════════════════════════════════════════════════
#  TEMPLATE 7: DESCRIPTOR BOARD PAGE
# ═══════════════════════════════════════════════════════════

def make_descriptor_board_page(doc: WorksheetDoc,
                                title: str,
                                columns: list,
                                prompt: str = None,
                                sentence_frame: str = None,
                                response_lines: int = 4,
                                access_note: str = None) -> list:
    """
    Descriptor board for Describe to Draw and Descriptive Teaching Model activities.
    Builds a row of attribute columns (e.g. Appearance / Action / Emotion) — each
    with a colored left-bar header, word slots, and writing lines below for the
    student to compose a description from selected attributes.

    Used for:
      - Describe to Draw (Fiction Anchor Texts) — student selects descriptors,
        partner draws from the description. The drawing is the comprehension evidence.
      - Descriptive Teaching Model (all product lines) — moves students from
        labeling to meaningful description using attribute categories.

    columns : list of dicts —
        "header"   : str  — column label (e.g. "Appearance", "Action", "Emotion")
        "color"    : color — left-bar color for the header (use brand colors)
        "words"    : list[str] — attribute words pre-loaded in this column
                     (these are the vocabulary options — student selects from them)
        "rows"     : int  — extra blank rows for student/partner to add words (default 2)

    prompt         : str  — activity direction (e.g. "You are the director. Describe
                             this character so your partner can draw them.")
    sentence_frame : str  — optional frame for the composed description below
    response_lines : int  — writing lines below the board for the composed description
    access_note    : str  — optional; points to language support only. Never
                             instructs HOW to respond. Default: nothing printed.

    Example call:
        make_descriptor_board_page(doc,
            title="Describe Auggie",
            columns=[
                {"header": "Appearance", "color": TEAL,
                 "words": ["short", "young", "wears a helmet", "has a scar"],
                 "rows": 2},
                {"header": "Action",     "color": AMBER,
                 "words": ["runs", "hides", "laughs", "fights", "leaves"],
                 "rows": 2},
                {"header": "Emotion",    "color": NAVY,
                 "words": ["scared", "proud", "alone", "hopeful", "angry"],
                 "rows": 2},
            ],
            prompt="You are the director. Tell me what this character looks like.",
            sentence_frame="This character is __________ and feels __________.",
        )
    """
    S = doc.S
    usable = doc.usable_width
    story = doc.page_header_block(title)

    if access_note:
        story.append(Paragraph(access_note, S["access_note"]))
        story.append(Spacer(1, 6))

    if prompt:
        story.append(Paragraph(prompt, S["body"]))
        story.append(Spacer(1, 8))

    # ── Attribute columns ─────────────────────────────────────────────────────
    n_cols  = len(columns)
    col_w   = usable / n_cols

    # Header row — colored left bar + bold label, white background
    hdr_cells = []
    for col in columns:
        hdr_cells.append(
            Paragraph(f"<b>{col['header']}</b>",
                      ParagraphStyle("db_hdr", fontName="Helvetica-Bold",
                                     fontSize=12, textColor=NAVY, leading=16))
        )
    hdr_tbl = Table([hdr_cells], colWidths=[col_w] * n_cols)
    hdr_style = [
        ("BACKGROUND",    (0,0), (-1,-1), WHITE),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING",   (0,0), (-1,-1), 10),
        ("RIGHTPADDING",  (0,0), (-1,-1), 6),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("LINEBELOW",     (0,0), (-1,-1), 1.5, TEAL),
    ]
    for ci, col in enumerate(columns):
        hdr_style.append(("LINEBEFORE", (ci,0), (ci,0), 3,
                           col.get("color", TEAL)))
    hdr_tbl.setStyle(TableStyle(hdr_style))
    story.append(hdr_tbl)

    # Word rows — pre-loaded attribute words, one per row
    # Find max word count across columns to set row count
    max_words = max(len(col.get("words", [])) + col.get("rows", 2)
                    for col in columns)

    word_style = ParagraphStyle("db_word", fontName="Helvetica",
                                 fontSize=10, textColor=BLACK, leading=14)

    for row_i in range(max_words):
        row_cells = []
        for col in columns:
            words     = col.get("words", [])
            is_preset = row_i < len(words)
            if is_preset:
                # Pre-loaded word — printed text
                cell_content = Paragraph(words[row_i], word_style)
            else:
                # Blank row — thin ruled line for student/partner to add a word
                cell_content = HRFlowable(
                    width="90%", thickness=0.5,
                    color=RULE_COLOR, spaceAfter=1
                )
            row_cells.append(cell_content)

        row_tbl = Table([row_cells], colWidths=[col_w] * n_cols)
        row_style = [
            ("BACKGROUND",    (0,0), (-1,-1), WHITE),
            ("GRID",          (0,0), (-1,-1), 0.5, BORDER_LIGHT),
            ("TOPPADDING",    (0,0), (-1,-1), 5),
            ("BOTTOMPADDING", (0,0), (-1,-1), 5),
            ("LEFTPADDING",   (0,0), (-1,-1), 10),
            ("RIGHTPADDING",  (0,0), (-1,-1), 6),
            ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ]
        for ci, col in enumerate(columns):
            row_style.append(("LINEBEFORE", (ci,0), (ci,0), 3,
                               col.get("color", TEAL)))
        row_tbl.setStyle(TableStyle(row_style))
        story.append(row_tbl)

    story.append(Spacer(1, 12))

    # ── Composition zone — student builds description from selected words ──────
    story.append(_zone_label_row(
        "MY DESCRIPTION",
        "Use the words above to describe this character or subject.",
        TEAL, usable, S
    ))
    story.append(Spacer(1, 6))

    if sentence_frame:
        story.append(Paragraph(sentence_frame, S["frame"]))
        story.append(Spacer(1, 4))

    story += _writing_lines(usable, count=response_lines)
    story.append(Spacer(1, 8))

    story.append(doc.thin_rule(space_before=4, space_after=3))
    story.append(doc.footer())
    story.append(PageBreak())
    return story


# ═══════════════════════════════════════════════════════════
#  TEMPLATE 8: PARTNER PROMPT CARD
# ═══════════════════════════════════════════════════════════

def make_partner_prompt_card(doc: WorksheetDoc,
                              title: str,
                              prompts: list,
                              card_note: str = None,
                              access_note: str = None) -> list:
    """
    Partner-facing prompt card — landscape-style layout within the standard
    page. Used for:
      - Dialogic Reading CROWD prompt cards (Picture Book Companions)
      - ALM partner scripts (all product lines)
      - Inferencing scaffold partner cue cards

    This is a TEACHER/PARTNER document, not a student worksheet. It lives in
    the Teacher Packet, not the Student Activities PDF. Include it in the
    make_partner_prompt_card() call from the Teacher build script, not the
    student worksheet build.

    prompts : list of dicts —
        "type"     : str  — prompt type label (e.g. "COMPLETION", "RECALL", "WH-")
        "color"    : color — left-bar color for this prompt type
        "prompt"   : str  — the actual prompt text the partner says
        "response" : str  — what response to look for / accept
        "wait"     : str or None — wait time note (e.g. "Wait 5 seconds.")

    card_note   : str — top-of-card teacher note (e.g. "Use during Reading 2.
                         Model each response on the student's AAC system BEFORE
                         asking for their response.")
    access_note : str — optional; additional access guidance. Default: nothing.

    Example call:
        make_partner_prompt_card(doc,
            title="CROWD Prompt Cards — All the Way to the Top",
            card_note="Model the response on the student's system before asking. "
                      "Accept any communicative act as a response.",
            prompts=[
                {"type": "COMPLETION", "color": AMBER,
                 "prompt": "Jennifer crawled up the Capitol steps because she wanted to ______.",
                 "response": "Accept: symbol selection, gesture, gaze, verbal approximation.",
                 "wait": "Wait 5 seconds after modeling."},
                {"type": "RECALL",    "color": TEAL,
                 "prompt": "What did Jennifer do when she got to the top?",
                 "response": "Accept: pointing to scene image, symbol, gesture.",
                 "wait": "Wait 5 seconds."},
                {"type": "WH-",       "color": NAVY,
                 "prompt": "Where did Jennifer go to make change happen?",
                 "response": "Accept: symbol for 'Capitol' or 'Washington' or any place indicator.",
                 "wait": "Wait 5 seconds."},
            ]
        )
    """
    S = doc.S
    usable = doc.usable_width

    # Partner card gets a distinct header — "PARTNER GUIDE" in amber to signal
    # this is not a student page
    partner_header_style = ParagraphStyle("partner_hdr",
        fontName="Helvetica-Bold", fontSize=9,
        textColor=AMBER, leading=12, alignment=TA_RIGHT)

    story = []
    # Custom header for partner card — adds PARTNER GUIDE badge
    right_content = (
        "<b><font color='#006DA0'>COMMUNICATE</font> "
        "<font color='#FFB703'>BY DESIGN</font></b>"
        "   <b><font color='#FFB703'>▶ PARTNER GUIDE</font></b>"
    )
    hdr_tbl = Table([[
        Paragraph(f"<i>{doc.unit_title}</i>", S["header_left"]),
        Paragraph(right_content, S["header_right"]),
    ]], colWidths=[doc.usable_width * 0.55, doc.usable_width * 0.45])
    hdr_tbl.setStyle(TableStyle([
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",    (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
        ("LEFTPADDING",   (0,0), (-1,-1), 0),
        ("RIGHTPADDING",  (0,0), (-1,-1), 0),
    ]))
    story.append(hdr_tbl)
    story.append(doc.divider())
    story.append(Paragraph(title, S["page_title"]))
    story.append(Spacer(1, 4))

    if card_note:
        # Card note gets amber left bar — signals this is a teacher instruction
        note_tbl = Table(
            [[Paragraph(card_note, S["section_note"])]],
            colWidths=[usable]
        )
        note_tbl.setStyle(TableStyle([
            ("LINEBEFORE",    (0,0), (0,0), 3, AMBER),
            ("BACKGROUND",    (0,0), (0,0), WHITE),
            ("TOPPADDING",    (0,0), (0,0), 5),
            ("BOTTOMPADDING", (0,0), (0,0), 5),
            ("LEFTPADDING",   (0,0), (0,0), 8),
            ("RIGHTPADDING",  (0,0), (0,0), 0),
        ]))
        story.append(note_tbl)
        story.append(Spacer(1, 8))

    if access_note:
        story.append(Paragraph(access_note, S["access_note"]))
        story.append(Spacer(1, 6))

    # ── Prompt cards — one per prompt ─────────────────────────────────────────
    type_label_style = ParagraphStyle("pc_type",
        fontName="Helvetica-Bold", fontSize=9,
        textColor=WHITE, leading=12, alignment=TA_CENTER)
    prompt_style = ParagraphStyle("pc_prompt",
        fontName="Helvetica-Bold", fontSize=10,
        textColor=NAVY, leading=14)
    response_style = ParagraphStyle("pc_resp",
        fontName="Helvetica", fontSize=9,
        textColor=BLACK, leading=13)
    wait_style = ParagraphStyle("pc_wait",
        fontName="Helvetica-Oblique", fontSize=8,
        textColor=SLATE, leading=11)

    for p in prompts:
        ptype    = p.get("type", "PROMPT")
        pcolor   = p.get("color", TEAL)
        prompt   = p.get("prompt", "")
        response = p.get("response", "")
        wait     = p.get("wait", None)

        # Type badge — small colored pill on the left
        badge_tbl = Table(
            [[Paragraph(ptype, type_label_style)]],
            colWidths=[1.1 * inch],
            rowHeights=[0.28 * inch]
        )
        badge_tbl.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (0,0), pcolor),
            ("ALIGN",         (0,0), (0,0), "CENTER"),
            ("VALIGN",        (0,0), (0,0), "MIDDLE"),
            ("TOPPADDING",    (0,0), (0,0), 2),
            ("BOTTOMPADDING", (0,0), (0,0), 2),
            ("LEFTPADDING",   (0,0), (0,0), 4),
            ("RIGHTPADDING",  (0,0), (0,0), 4),
        ]))

        content_w = usable - 1.2 * inch
        content = [
            Paragraph(f"<i>Say:</i> {prompt}", prompt_style),
            Spacer(1, 3),
            Paragraph(f"<b>Accept:</b> {response}", response_style),
        ]
        if wait:
            content.append(Paragraph(wait, wait_style))

        card_row = Table(
            [[badge_tbl, content]],
            colWidths=[1.2 * inch, content_w]
        )
        card_row.setStyle(TableStyle([
            ("VALIGN",        (0,0), (-1,-1), "TOP"),
            ("TOPPADDING",    (0,0), (-1,-1), 8),
            ("BOTTOMPADDING", (0,0), (-1,-1), 8),
            ("LEFTPADDING",   (0,0), (-1,-1), 6),
            ("RIGHTPADDING",  (0,0), (-1,-1), 6),
            ("BACKGROUND",    (0,0), (-1,-1), WHITE),
            ("BOX",           (0,0), (-1,-1), 0.75, BORDER_LIGHT),
            ("LINEBEFORE",    (0,0), (0,-1), 3, pcolor),
        ]))
        story.append(KeepTogether(card_row))
        story.append(Spacer(1, 6))

    story.append(Spacer(1, 8))
    story.append(doc.thin_rule(space_before=4, space_after=3))
    story.append(doc.footer())
    story.append(PageBreak())
    return story


# ═══════════════════════════════════════════════════════════
#  DEMO BUILD
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    out = "/tmp/cbd_worksheet_demo.pdf"
    doc = WorksheetDoc(
        output_path=out,
        unit_title="Frances Kelsey: The Woman Who Said No",
        product_line="Nonfiction Reading Unit",
        version_label="V3",
    )
    story = []

    story += make_vocab_preview_page(doc, words=[
        {"word": "pressure",  "definition": "When someone tries hard to make you do something you don't want to do.",
         "example": "The drug company put pressure on Kelsey to approve the drug quickly.",
         "is_core": False},
        {"word": "approve",   "definition": "To officially say yes to something.",
         "example": "Kelsey would not approve the drug until she had more proof it was safe.",
         "is_core": True},
        {"word": "deny",      "definition": "To say no to a request.",
         "example": "She decided to deny the application.", "is_core": True},
    ])

    story += make_mcq_page(doc, title="Part 1: Comprehension Check",
        questions=[
            {"stem": "Why did the drug company want Kelsey to approve Thalidomide quickly?",
             "options": ["A. It was already being used safely in Canada.",
                         "B. European countries were already selling it.",
                         "C. Kelsey had already tested it.",
                         "D. The FDA required fast approvals."],
             "has_symbol_zone": True},
            {"stem": "What was Kelsey's main concern about the drug?",
             "options": ["A. It was too expensive to produce.",
                         "B. It had not been tested long enough.",
                         "C. Other scientists had approved it.",
                         "D. The company did not have a license."],
             "has_symbol_zone": True},
        ]
    )

    story += make_cer_page(doc,
        title="Part 2: Claim-Evidence-Reasoning",
        prompt="Why was Frances Kelsey's decision important for public safety?",
        claim_frame="Frances Kelsey's decision was important because __________.",
        evidence_slots=2, reasoning_lines=3,
    )

    story += make_short_answer_page(doc, title="Part 3: Short Answer",
        questions=[
            {"prompt": "What is one word that describes Frances Kelsey? Explain why.",
             "lines": 4,
             "sentence_frame": "I think Kelsey was __________ because __________.",
             "has_symbol_zone": True},
            {"prompt": "How do you think Kelsey felt when the drug company pressured her?",
             "lines": 3,
             "sentence_frame": "I think she felt __________ because __________.",
             "has_symbol_zone": True},
        ]
    )

    story += make_evidence_sort_page(doc,
        title="Evidence Sort: Perspectives on Thalidomide",
        prompt="As you read, sort evidence into the three columns below.",
        columns=[
            {"header": "F", "subhead": "Frances Kelsey's View",  "color": NAVY,  "lines": 3, "rows": 4},
            {"header": "C", "subhead": "Drug Company's View",    "color": TEAL,  "lines": 3, "rows": 4},
            {"header": "G", "subhead": "Government / Public",    "color": AMBER, "lines": 3, "rows": 4},
        ]
    )

    story += make_annotation_guide_page(doc,
        codes=[
            {"code": "F", "label": "Frances's Reasoning",
             "example": "Mark moments where Kelsey explains why she said no.", "color": NAVY},
            {"code": "P", "label": "Pressure on Kelsey",
             "example": "Mark moments where the company pushed her.", "color": TEAL},
            {"code": "E", "label": "Evidence She Needed",
             "example": "Mark what Kelsey said was missing.", "color": AMBER},
        ],
        tips=[
            "Write the code letter in the margin next to the sentence.",
            "You can mark the same sentence with more than one code.",
            "If you use AAC, tell your partner which code to write for you.",
        ]
    )

    doc.build(story)
    print(f"\nDemo PDF: {out}")

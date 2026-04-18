"""
build_wonder_answer_keys.py — Communicate by Design
=====================================================
Builds the Teacher Answer Key PDF for:
  Wonder: Character Analysis — Fiction Anchor Text Unit
  Grades 3–8  |  RL.3.3 · RL.5.3 · RL.6.3 · RL.7.3

OUTPUT:
  Wonder_Character_Analysis_Answer_Key.pdf

STRUCTURE:
  Cover / How to Use This Document
  Part 1 — Describe to Draw: Model Character Description (Auggie)
  Part 2 — Same and Different: Character Comparison (Via + Jack)
  Part 3 — Why Did They Do That?: Character Motivation (Julian + Miranda)
  Part 4 — Before and After: Character Change Arc (Auggie + Jack)
  Part 5 — The Big Idea: Theme — Model Write-Ables Responses

USAGE:
  python3 build_wonder_answer_keys.py
"""

import io
import os

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, HRFlowable
)
from reportlab.lib.colors import HexColor

# ── Brand colors ──────────────────────────────────────────────────────────────
NAVY  = HexColor("#1B1F3B")
TEAL  = HexColor("#006DA0")
AMBER = HexColor("#FFB703")
WHITE = HexColor("#FFFFFF")
SLATE = HexColor("#94A3B8")
LIGHT = HexColor("#F0F4F8")   # answer box background
GREEN = HexColor("#14532D")   # model answer label
LGREY = HexColor("#E2E8F0")   # row alt

HERE = os.path.dirname(os.path.abspath(__file__))
WONDER_DIR = os.path.join(
    HERE, "mnt", "com~apple~CloudDocs--Communicate by Design",
    "Products", "Fiction Anchor Texts", "Wonder - Character Analysis"
)
OUTPUT = os.path.join(WONDER_DIR, "Wonder_Character_Analysis_Answer_Key.pdf")


# ── Styles ─────────────────────────────────────────────────────────────────────

def make_styles():
    h1   = ParagraphStyle("h1",   fontName="Helvetica-Bold",
               fontSize=13, textColor=WHITE,   leading=18, spaceAfter=4)
    h2   = ParagraphStyle("h2",   fontName="Helvetica-Bold",
               fontSize=11, textColor=TEAL,    leading=14, spaceBefore=10, spaceAfter=4)
    h3   = ParagraphStyle("h3",   fontName="Helvetica-Bold",
               fontSize=9,  textColor=NAVY,    leading=13, spaceBefore=6,  spaceAfter=2)
    body = ParagraphStyle("body", fontName="Helvetica",
               fontSize=9,  textColor=NAVY,    leading=13, spaceAfter=3)
    ans  = ParagraphStyle("ans",  fontName="Helvetica",
               fontSize=9,  textColor=HexColor("#0f2e10"), leading=13, spaceAfter=3,
               leftIndent=8)
    note = ParagraphStyle("note", fontName="Helvetica-Oblique",
               fontSize=8,  textColor=HexColor("#374151"),  leading=11, spaceAfter=4,
               leftIndent=8)
    small= ParagraphStyle("small",fontName="Helvetica",
               fontSize=8,  textColor=SLATE,   leading=10, spaceAfter=2)
    ft   = ParagraphStyle("ft",   fontName="Helvetica",
               fontSize=7,  textColor=SLATE,   leading=9, alignment=TA_CENTER)
    return h1, h2, h3, body, ans, note, small, ft


def running_header(title_text):
    h1, h2, h3, body, ans, note, small, ft = make_styles()
    row = Table([[
        Paragraph(f"<i>{title_text}</i>",
                  ParagraphStyle("hl", fontName="Helvetica-Oblique",
                      fontSize=9, textColor=NAVY, leading=13)),
        Paragraph(
            "<b><font color='#006DA0'>COMMUNICATE</font> "
            "<font color='#FFB703'>BY DESIGN</font></b>  "
            "<font color='#94A3B8'>— Teacher Answer Key</font>",
            ParagraphStyle("br", fontName="Helvetica-Bold",
                fontSize=9, textColor=TEAL, leading=13, alignment=TA_RIGHT)),
    ]], colWidths=[3.5*inch, 3.5*inch])
    row.setStyle(TableStyle([
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",    (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
        ("LEFTPADDING",   (0,0), (-1,-1), 0),
        ("RIGHTPADDING",  (0,0), (-1,-1), 0),
    ]))
    return row


def part_banner(part_num, title, novel_section, standard):
    """Navy banner for each Part."""
    tbl = Table([[
        Paragraph(
            f"<b>Part {part_num}: {title}</b>",
            ParagraphStyle("pt", fontName="Helvetica-Bold",
                fontSize=13, textColor=WHITE, leading=17, alignment=TA_LEFT)),
        Paragraph(
            f"<b><font color='#FFB703'>{novel_section}</font><br/>"
            f"<font color='#94A3B8' size='8'>{standard}</font></b>",
            ParagraphStyle("pr", fontName="Helvetica-Bold",
                fontSize=9, textColor=AMBER, leading=13, alignment=TA_RIGHT)),
    ]], colWidths=[4.6*inch, 2.4*inch])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), NAVY),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",    (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("LEFTPADDING",   (0,0), (-1,-1), 14),
        ("RIGHTPADDING",  (0,0), (-1,-1), 12),
    ]))
    return tbl


def answer_box(label, content_paras):
    """Teal-labeled answer box."""
    h1, h2, h3, body, ans, note, small, ft = make_styles()
    label_cell = Paragraph(
        f"<b>{label}</b>",
        ParagraphStyle("lbl", fontName="Helvetica-Bold",
            fontSize=8, textColor=WHITE, leading=11, alignment=TA_CENTER))
    content_cell = [Spacer(1, 4)] + content_paras + [Spacer(1, 4)]
    tbl = Table([[label_cell], [content_cell]], colWidths=[7.0*inch])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (0,0), TEAL),
        ("BACKGROUND",    (0,1), (0,1), LIGHT),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("RIGHTPADDING",  (0,0), (-1,-1), 8),
        ("BOX",           (0,0), (-1,-1), 0.5, TEAL),
    ]))
    return tbl


def model_table(headers, rows, col_widths=None):
    """Striped answer table."""
    if col_widths is None:
        n = len(headers)
        col_widths = [7.0*inch / n] * n

    header_style = ParagraphStyle("th", fontName="Helvetica-Bold",
        fontSize=8, textColor=WHITE, leading=11)
    cell_style   = ParagraphStyle("td", fontName="Helvetica",
        fontSize=8, textColor=NAVY, leading=12)

    data = [[Paragraph(h, header_style) for h in headers]]
    for i, row in enumerate(rows):
        data.append([Paragraph(cell, cell_style) for cell in row])

    tbl = Table(data, colWidths=col_widths, repeatRows=1)
    style = [
        ("BACKGROUND",    (0,0), (-1,0), NAVY),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
        ("RIGHTPADDING",  (0,0), (-1,-1), 6),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ("GRID",          (0,0), (-1,-1), 0.4, HexColor("#CBD5E1")),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0,i), (-1,i), LGREY))
    tbl.setStyle(TableStyle(style))
    return tbl


FOOTER_TEXT = (
    "Wonder: Character Analysis  ·  Teacher Answer Key  ·  Communicate by Design  ·  "
    "teacherspayteachers.com/store/communicate-by-design  ·  © Communicate by Design. All rights reserved."
)


def build_answer_key() -> bytes:
    h1, h2, h3, body, ans, note, small, ft = make_styles()
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=letter,
        leftMargin=0.75*inch, rightMargin=0.75*inch,
        topMargin=0.5*inch,   bottomMargin=0.5*inch
    )

    CW = 7.0 * inch   # content width
    col2 = lambda a, b: [round(CW*a), round(CW*b)]
    col3 = lambda a, b, c: [round(CW*a), round(CW*b), round(CW*c)]
    col4 = lambda a, b, c, d: [round(CW*a), round(CW*b), round(CW*c), round(CW*d)]

    S = story = []

    # ══════════════════════════════════════════════════════════════════════
    # COVER PAGE
    # ══════════════════════════════════════════════════════════════════════

    cover_banner = Table([[
        Paragraph(
            "Wonder: Character Analysis<br/>"
            "<font size='11'>Teacher Answer Key</font>",
            ParagraphStyle("cov", fontName="Helvetica-Bold",
                fontSize=18, textColor=WHITE, leading=26, alignment=TA_LEFT)),
        Paragraph(
            "<b>Grades 3–8<br/>Communicate by Design</b>",
            ParagraphStyle("covr", fontName="Helvetica-Bold",
                fontSize=10, textColor=AMBER, leading=14, alignment=TA_RIGHT)),
    ]], colWidths=[5.0*inch, 2.0*inch])
    cover_banner.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), NAVY),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",    (0,0), (-1,-1), 18),
        ("BOTTOMPADDING", (0,0), (-1,-1), 18),
        ("LEFTPADDING",   (0,0), (-1,-1), 16),
        ("RIGHTPADDING",  (0,0), (-1,-1), 14),
    ]))

    not_for_student_banner = Table([[
        Paragraph(
            "⚠️  TEACHER DOCUMENT — NOT FOR STUDENT USE",
            ParagraphStyle("warn", fontName="Helvetica-Bold",
                fontSize=9, textColor=WHITE, leading=13, alignment=TA_CENTER)),
    ]], colWidths=[CW])
    not_for_student_banner.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), HexColor("#7c2d12")),
        ("TOPPADDING",    (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("RIGHTPADDING",  (0,0), (-1,-1), 8),
    ]))

    S += [
        cover_banner,
        not_for_student_banner,
        Spacer(1, 12),
        Paragraph("How to Use This Document", h2),
        HRFlowable(width="100%", thickness=0.75, color=AMBER, spaceAfter=5),
        Paragraph(
            "This Answer Key provides model responses for each of the five student response pages in the Printable Packet. "
            "These are not the only correct answers — they are evidence-based examples of what meeting the standard looks like "
            "for each Part of the novel.",
            body),
        Paragraph(
            "Use this document to:",
            body),
        Paragraph("• Score student responses against the rubric (when built)", body),
        Paragraph("• Prepare discussion prompts before each Part", body),
        Paragraph("• Model AAC-accessible responses during instruction (Aided Language Stimulation)", body),
        Paragraph("• Conference with paraprofessionals before Mode 1 activities", body),
        Spacer(1, 8),
        model_table(
            ["Part", "Novel Section", "Activity", "Standard"],
            [
                ["1", "August — Chapters 1–9",        "Describe to Draw: Character Description",    "RL.3.3 · RL.5.3"],
                ["2", "Via + Jack — Chapters 10–29",  "Same and Different: Character Comparison",   "RL.5.3 · RL.6.3"],
                ["3", "Julian + Miranda — Ch. 30–45", "Why Did They Do That?: Character Motivation","RL.6.3 · RL.7.3"],
                ["4", "Part 6 + Epilogue — Ch. 46–52","Before and After: Character Change",         "RL.6.3 · RL.7.3"],
                ["5", "Whole Book — Synthesis",        "The Big Idea: Theme Through Character",     "RL.3.2 · RL.5.2 · RL.7.2"],
            ],
            col4(0.06, 0.26, 0.42, 0.26)
        ),
        Spacer(1, 8),
        Paragraph(
            "Annotation codes used in student response pages: [TRAIT] = observable character trait · "
            "[WHY] = motivation or cause · [CHANGE] = shift in character across the arc. "
            "Model answers below show where these codes apply.",
            note),
        Spacer(1, 6),
        HRFlowable(width="100%", thickness=0.5, color=TEAL, spaceAfter=3),
        Paragraph(FOOTER_TEXT, ft),
    ]

    # ══════════════════════════════════════════════════════════════════════
    # PART 1 — DESCRIBE TO DRAW
    # ══════════════════════════════════════════════════════════════════════

    S += [
        PageBreak(),
        running_header("Wonder: Character Analysis — Answer Key"),
        HRFlowable(width="100%", thickness=1.5, color=TEAL, spaceAfter=6),
        part_banner("1", "Describe to Draw",
                    "August · Chapters 1–9", "RL.3.3 · RL.5.3"),
        Spacer(1, 10),

        Paragraph("Student Response Page: Describe to Draw", h2),
        HRFlowable(width="100%", thickness=0.75, color=AMBER, spaceAfter=5),
        Paragraph(
            "The student response page asks students to build a description of the main character "
            "(Auggie) using the character description board and core/fringe vocabulary. "
            "The drawing box is completed by the partner based on the student's description.",
            body),
        Spacer(1, 6),

        answer_box("MODEL RESPONSE — Character Description (Auggie, Part 1)", [
            Paragraph("<b>What does this character look like?</b>", h3),
            Paragraph(
                "He is small. He is a boy. His face looks different from other people's faces. "
                "He wears a helmet sometimes (at the start — this is a memory from when he was younger).",
                ans),
            Paragraph("[TRAIT] face looks different · small · boy", note),
            Spacer(1, 5),
            Paragraph("<b>What does this character do?</b>", h3),
            Paragraph(
                "He goes to school for the first time. He walks into a classroom where no one knows him. "
                "He looks at the floor. He tries not to be seen. He makes a friend (Summer sits with him at lunch).",
                ans),
            Paragraph("[TRAIT] brave (goes even when he is scared) · [WHY] he has to go to school · [TRAIT] wants friends", note),
            Spacer(1, 5),
            Paragraph("<b>How does this character feel?</b>", h3),
            Paragraph(
                "He feels scared and brave at the same time. He feels different. "
                "He feels like people are staring at him. He wants to be invisible.",
                ans),
            Paragraph("[TRAIT] scared · [TRAIT] brave · [TRAIT] wants to belong", note),
            Spacer(1, 5),
            Paragraph("<b>What does this character want?</b>", h3),
            Paragraph(
                "He wants to be seen as a regular kid. He wants a friend. He wants people to look past his face. "
                "He wants to belong.",
                ans),
            Paragraph("[TRAIT] wants to belong · [TRAIT] wants to be ordinary", note),
        ]),
        Spacer(1, 8),

        Paragraph("Scoring Notes", h2),
        HRFlowable(width="100%", thickness=0.75, color=AMBER, spaceAfter=5),
        model_table(
            ["Rubric Level", "What It Looks Like in Part 1"],
            [
                ["Meets",
                 "Student produces at least 3 description elements (appearance + feeling + wanting/goal) using AAC system, board, or gesture + partner record. Description is accurate to the text."],
                ["Approaching",
                 "Student produces 1–2 description elements. May use appearance only (face, small) without connecting to feeling or motivation."],
                ["Does Not Yet Meet",
                 "Student does not produce a description unprompted. May require Level 4–5 prompt (verbal model + demonstration on device). Record vocabulary availability — if vocabulary is not programmed, this is an access barrier, not a comprehension barrier."],
            ],
            col2(0.20, 0.80)
        ),
        Spacer(1, 6),
        Paragraph(
            "⚠️  If a student cannot select 'different' or 'face looks different,' the fringe vocabulary was not pre-programmed. "
            "This is an access issue, not a comprehension issue. Document on the Communication Session Tracker and notify the SLP.",
            note),
        Spacer(1, 6),
        HRFlowable(width="100%", thickness=0.5, color=TEAL, spaceAfter=3),
        Paragraph(FOOTER_TEXT, ft),
    ]

    # ══════════════════════════════════════════════════════════════════════
    # PART 2 — SAME AND DIFFERENT
    # ══════════════════════════════════════════════════════════════════════

    S += [
        PageBreak(),
        running_header("Wonder: Character Analysis — Answer Key"),
        HRFlowable(width="100%", thickness=1.5, color=TEAL, spaceAfter=6),
        part_banner("2", "Same and Different",
                    "Via + Jack · Chapters 10–29", "RL.5.3 · RL.6.3"),
        Spacer(1, 10),

        Paragraph("Student Response Page: Same and Different", h2),
        HRFlowable(width="100%", thickness=0.75, color=AMBER, spaceAfter=5),
        Paragraph(
            "Students compare two characters. The comparison structure has four rows: looks like · acts like · feels · wants. "
            "Model answers below are for the Via / Jack comparison, which is the recommended pair for Part 2.",
            body),
        Spacer(1, 6),

        answer_box("MODEL RESPONSE — Via and Jack Comparison", [
            model_table(
                ["", "Via (Auggie's older sister)", "Both", "Jack (Auggie's classmate)"],
                [
                    ["Looks like",
                     "Older girl · teenager · dark hair · stands beside Auggie but sometimes far back",
                     "—",
                     "Boy · about Auggie's age · looks ordinary · typical school kid"],
                    ["Acts like",
                     "Protects Auggie · hides how much she worries · puts his needs first even when it hurts her",
                     "Both care about Auggie · Both feel pulled between loyalty and their own needs",
                     "Becomes Auggie's friend · then says something cruel (Halloween) · then chooses Auggie at the snowball fight"],
                    ["Feels",
                     "[TRAIT] invisible · [TRAIT] left out · [TRAIT] loves Auggie · [TRAIT] guilty",
                     "Both feel unsure · Both feel something is unfair",
                     "[TRAIT] guilty · [TRAIT] conflicted · [TRAIT] loyal (at the end)"],
                    ["Wants",
                     "[TRAIT] to be seen · to be her own person · not just 'Auggie's sister'",
                     "Both want to be good · Both want to belong",
                     "[TRAIT] to fit in · to keep Auggie as a friend · [CHANGE] to make the right choice"],
                ],
                col4(0.14, 0.29, 0.16, 0.29) if False else None  # use default equal cols
            ),
        ]),
        Spacer(1, 8),

        Paragraph("Key Discussion Points for Part 2", h2),
        HRFlowable(width="100%", thickness=0.75, color=AMBER, spaceAfter=5),
        model_table(
            ["Prompt", "What to Listen/Watch For"],
            [
                ["How does Via feel about her brother?",
                 "Student should show BOTH love AND complicated feelings (invisible, jealous, guilty). "
                 "A response of only 'she loves him' is partial — push for the conflict."],
                ["What does Jack do that is hard to understand?",
                 "Halloween scene — Jack says something mean about Auggie to fit in. Student should connect: "
                 "he did it because he wanted to belong / because he was scared of Julian. "
                 "This is the core [WHY] moment of Jack's arc."],
                ["How does Jack change by the end of this section?",
                 "He stands up for Auggie at the snowball fight. [CHANGE] from: protects himself first → "
                 "chooses Auggie even though it costs him social status."],
            ],
            col2(0.38, 0.62)
        ),
        Spacer(1, 6),
        HRFlowable(width="100%", thickness=0.5, color=TEAL, spaceAfter=3),
        Paragraph(FOOTER_TEXT, ft),
    ]

    # ══════════════════════════════════════════════════════════════════════
    # PART 3 — WHY DID THEY DO THAT?
    # ══════════════════════════════════════════════════════════════════════

    S += [
        PageBreak(),
        running_header("Wonder: Character Analysis — Answer Key"),
        HRFlowable(width="100%", thickness=1.5, color=TEAL, spaceAfter=6),
        part_banner("3", "Why Did They Do That?",
                    "Julian + Miranda · Chapters 30–45", "RL.6.3 · RL.7.3"),
        Spacer(1, 10),

        Paragraph("Student Response Page: Character Motivation", h2),
        HRFlowable(width="100%", thickness=0.75, color=AMBER, spaceAfter=5),
        Paragraph(
            "The motivation page asks students to apply the Because / Maybe / Probably scaffold "
            "to explain WHY a character acts the way they do. "
            "This is the inferencing section — answers will vary more than earlier parts. "
            "Accept any response grounded in text evidence.",
            body),
        Spacer(1, 6),

        answer_box("MODEL RESPONSE — Julian's Motivation", [
            Paragraph("<b>This character acts unkind because…</b>", h3),
            Paragraph(
                "…he is scared of being different too. He does not want people to look at him the way they look at Auggie. "
                "Being unkind to Auggie makes him feel powerful and safe.",
                ans),
            Paragraph("[WHY] fear of difference · [WHY] wants social power · [WHY] protecting himself by excluding others", note),
            Spacer(1, 5),
            Paragraph("<b>Maybe this character feels ___ on the inside.</b>", h3),
            Paragraph(
                "Maybe he feels scared. Maybe he feels alone. Maybe he feels like if he is kind to Auggie, "
                "people will think he is different too.",
                ans),
            Paragraph("[TRAIT] scared · [TRAIT] insecure — these are inferred, not stated in the text at this point", note),
            Spacer(1, 5),
            Paragraph("<b>This character probably chose to do that because…</b>", h3),
            Paragraph(
                "…he probably wanted to stay popular. He knew that being unkind to Auggie made him look powerful. "
                "He chose status over kindness.",
                ans),
            Paragraph("[WHY] social status · [WHY] choice — this is the key: he CHOSE it, it was not an accident", note),
        ]),
        Spacer(1, 8),

        answer_box("MODEL RESPONSE — Miranda's Motivation (optional extension)", [
            Paragraph(
                "Miranda tells people that her family adopted Auggie — she pretends he is her brother. "
                "[WHY] She does this because she misses him. She and Via grew apart over the summer and she doesn't know "
                "how to get back to that friendship. She uses Auggie as a way to hold on to the family she loved.",
                ans),
            Paragraph("[WHY] grief over a lost friendship · [WHY] wanting to belong to something · [TRAIT] lonely", note),
        ]),
        Spacer(1, 8),

        Paragraph("Scoring Notes — Motivation Is Inferred", h2),
        HRFlowable(width="100%", thickness=0.75, color=AMBER, spaceAfter=5),
        Paragraph(
            "Motivation questions are inference tasks — the text does not explicitly state why Julian is unkind. "
            "Students are synthesizing evidence + reasoning. Score for quality of reasoning, not for matching the model exactly.",
            body),
        model_table(
            ["Rubric Level", "What It Looks Like in Part 3"],
            [
                ["Meets",
                 "Student produces a motivation claim using because / maybe / probably with at least one text-grounded reason. "
                 "Connects character's action to an internal state (scared, wants, feels)."],
                ["Approaching",
                 "Student identifies the behavior ('he is mean') but does not explain why. "
                 "Prompt: 'Why might he act that way? What might he feel inside?'"],
                ["Does Not Yet Meet",
                 "Student cannot connect behavior to internal motivation without Level 4 prompt. "
                 "Check: Is 'because' available on the student's system? Is 'maybe' accessible? "
                 "These are the core words for inference — if they are not available, address vocabulary access first."],
            ],
            col2(0.20, 0.80)
        ),
        Spacer(1, 6),
        HRFlowable(width="100%", thickness=0.5, color=TEAL, spaceAfter=3),
        Paragraph(FOOTER_TEXT, ft),
    ]

    # ══════════════════════════════════════════════════════════════════════
    # PART 4 — BEFORE AND AFTER
    # ══════════════════════════════════════════════════════════════════════

    S += [
        PageBreak(),
        running_header("Wonder: Character Analysis — Answer Key"),
        HRFlowable(width="100%", thickness=1.5, color=TEAL, spaceAfter=6),
        part_banner("4", "Before and After",
                    "Part 6 + Epilogue · Chapters 46–52", "RL.6.3 · RL.7.3"),
        Spacer(1, 10),

        Paragraph("Student Response Page: Character Change Arc", h2),
        HRFlowable(width="100%", thickness=0.75, color=AMBER, spaceAfter=5),
        Paragraph(
            "The Before/After response page tracks how a character changes across the whole novel. "
            "Model answers below are given for Auggie (primary) and Jack (secondary). "
            "Julian can also be used for an extension or grade 7 standard focus.",
            body),
        Spacer(1, 6),

        answer_box("MODEL RESPONSE — Auggie's Character Change Arc", [
            model_table(
                ["", "At the Beginning", "Something Changes When…", "At the End"],
                [
                    ["How they feel",
                     "Scared · wants to be invisible · dreads school",
                     "Summer sits with him at lunch without being asked · Jack stands up for him at the snowball fight",
                     "Feels like he belongs · brave · accepted · happy"],
                    ["What they want",
                     "Wants to be invisible · wants to be ordinary · wants ONE friend",
                     "He realizes people see him — really see him",
                     "Wants to be seen as himself · accepts that he is not ordinary and that is okay"],
                    ["How others see them",
                     "Most students stare, avoid, or are unkind",
                     "More students choose kindness after Julian leaves",
                     "The whole school gives him a standing ovation at graduation"],
                    ["What they do",
                     "Keeps to himself · doesn't fight back · tries to hide",
                     "Starts showing who he is — his humor, his kindness, his Star Wars love",
                     "Speaks up · is funny · has real friends · receives the Henry Ward Beecher Award"],
                ],
                col4(0.18, 0.24, 0.30, 0.28)
            ),
            Spacer(1, 4),
            Paragraph("[CHANGE] The clearest change: At the start Auggie wants to be INVISIBLE. At the end he is seen — and he wants to be.", note),
        ]),
        Spacer(1, 8),

        answer_box("MODEL RESPONSE — Jack's Character Change Arc (secondary)", [
            model_table(
                ["", "At the Beginning", "Something Changes When…", "At the End"],
                [
                    ["How they feel",
                     "Conflicted · wants to be Auggie's friend but also wants to fit in with Julian",
                     "Halloween — he says something cruel about Auggie and Auggie hears it",
                     "Guilty → repentant → loyal · chose Auggie even when it cost him"],
                    ["What they do",
                     "Follows Julian's rules · sometimes protects Auggie, sometimes doesn't",
                     "Auggie stops speaking to him · Jack punches Julian at the Halloween party",
                     "Fights for Auggie at the snowball fight · is Auggie's real friend"],
                ],
                col4(0.18, 0.24, 0.30, 0.28)
            ),
            Spacer(1, 4),
            Paragraph("[CHANGE] Jack's arc: chooses social safety → loses Auggie → chooses Auggie even though it costs him. This is the 'choose kind' precept in action.", note),
        ]),
        Spacer(1, 6),
        HRFlowable(width="100%", thickness=0.5, color=TEAL, spaceAfter=3),
        Paragraph(FOOTER_TEXT, ft),
    ]

    # ══════════════════════════════════════════════════════════════════════
    # PART 5 — THE BIG IDEA
    # ══════════════════════════════════════════════════════════════════════

    S += [
        PageBreak(),
        running_header("Wonder: Character Analysis — Answer Key"),
        HRFlowable(width="100%", thickness=1.5, color=TEAL, spaceAfter=6),
        part_banner("5", "The Big Idea",
                    "Whole Book · Synthesis", "RL.3.2 · RL.5.2 · RL.6.2 · RL.7.2"),
        Spacer(1, 10),

        Paragraph("Student Response Page: Theme Through Character", h2),
        HRFlowable(width="100%", thickness=0.75, color=AMBER, spaceAfter=5),
        Paragraph(
            "The synthesis activity uses Write-Ables frames — generative sentence structures built from core vocabulary. "
            "Any completion that is grounded in the novel and connects a character's journey to a theme is acceptable. "
            "Model responses below show what meeting the standard looks like.",
            body),
        Spacer(1, 6),

        answer_box("MODEL WRITE-ABLES RESPONSES", [
            model_table(
                ["Frame", "Model Response", "Core Words Used"],
                [
                    ["The main character changes because ___.",
                     "The main character changes because he learns that he belongs. "
                     "He starts the year wanting to be invisible and ends it being seen — and choosing to be.",
                     "change · belong · know · want"],
                    ["The character who is unkind acts that way because ___.",
                     "The character who is unkind acts that way because he is scared of being different. "
                     "Maybe he does not want people to look at him the way they look at the main character.",
                     "because · scared · different · maybe · want"],
                    ["The most important thing this story teaches is ___.",
                     "The most important thing this story teaches is to choose kind. "
                     "Every character has a moment where they can choose to be kind or to protect themselves. "
                     "The ones who choose kind are the ones who belong at the end.",
                     "choose · kind · belong"],
                    ["I think the character who is bravest is the one who ___.",
                     "I think the character who is bravest is the one who sat with the main character at lunch "
                     "on the first day without being asked to. She did not know him. She just chose kindness.",
                     "brave · choose · kind · friend"],
                ],
                col3(0.32, 0.46, 0.22)
            ),
        ]),
        Spacer(1, 8),

        answer_box("SYMBOL SORT — Model Theme Selection", [
            Paragraph(
                "If using the symbol sort version: the correct primary sort is <b>YES, the story is about this</b> "
                "for: <b>kind · belong · different · choose · see</b>. "
                "Secondary (Maybe): <b>brave · together · invisible</b>. "
                "Students may reasonably argue for 'invisible' as a primary theme — Auggie's wish to be invisible "
                "and his eventual decision to stop hiding is central to his arc. Accept with evidence.",
                ans),
        ]),
        Spacer(1, 8),

        Paragraph("Theme Statements — What Meets the Standard Looks Like", h2),
        HRFlowable(width="100%", thickness=0.75, color=AMBER, spaceAfter=5),
        model_table(
            ["Standard", "Minimum Evidence for 'Meets'"],
            [
                ["RL.3.2",
                 "Student identifies the central message or lesson: 'Choose kind' / 'Be kind to people who look different.' "
                 "Can be produced with symbol selection or sentence frame — no written response required."],
                ["RL.5.2",
                 "Student states a theme AND connects it to a specific character: "
                 "'The theme is belonging, and the main character shows this because he goes from wanting to be invisible to being celebrated.'"],
                ["RL.6.2 / RL.7.2",
                 "Student states a theme supported by evidence from at least two characters or events: "
                 "'The theme is that belonging is something you choose, not something that happens to you. "
                 "The main character chooses to stay in school. Jack chooses Auggie at the snowball fight. "
                 "Summer chooses to sit with him on day one. All three choices build the theme.'"],
            ],
            col2(0.15, 0.85)
        ),
        Spacer(1, 8),
        HRFlowable(width="100%", thickness=0.5, color=TEAL, spaceAfter=3),
        Paragraph(FOOTER_TEXT, ft),
    ]

    doc.build(story)
    return buf.getvalue()


def main():
    print(f"\n{'═'*60}")
    print("  CbD Fiction Answer Key Builder")
    print("  Wonder: Character Analysis  ·  Grades 3–8")
    print(f"{'═'*60}\n")

    os.makedirs(WONDER_DIR, exist_ok=True)
    print("Building Teacher Answer Key...")
    pdf_bytes = build_answer_key()

    with open(OUTPUT, "wb") as f:
        f.write(pdf_bytes)

    size_kb = len(pdf_bytes) / 1024
    print(f"  ✓ Wonder_Character_Analysis_Answer_Key.pdf  ({size_kb:.0f} KB)")
    print(f"  → {OUTPUT}")
    print(f"\n{'═'*60}\n")


if __name__ == "__main__":
    main()

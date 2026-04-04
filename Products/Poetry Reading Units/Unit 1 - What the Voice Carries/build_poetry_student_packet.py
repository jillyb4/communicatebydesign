"""
Student Poetry Packet — What the Voice Carries
Communicate by Design · Unit 1, Poetry Reading Units

STANDARD: B&W printable student activity.
Follows CbD student packet rules in _Operations/memory/build_system_reference.md
→ Student Packet / Student Activity PDF Standard — HARD RULES.
Reference: Wonder build_wonder_printable_packet.py Layer 5 (gold standard).

All pages print cleanly in grayscale.
- One thin navy header bar per page (16–18pt, white text) — only colored fill allowed.
- No amber/violet/teal fills on any activity element.
- Response areas: white fill, light gray border.
- NFMA step labels: bold text + 3pt left accent bar, no pill fill.
- Cover: white background, text only.

Structure:
  p1       Cover page (white, text only)
  p2-5     V1 pages — one per poem (open written response)
  p6-9     V2 pages — one per poem (guided frames + [ ] choices)
  p10-13   V3 pages — one per poem (indicate/point/AAC response)
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas as rl_canvas

BASE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(BASE, "What_the_Voice_Carries_Student_Packet.pdf")

# ── Brand ──────────────────────────────────────────────────────────────────────
NAVY     = colors.HexColor("#1B1F3B")   # header bar fill + primary text
SLATE    = colors.HexColor("#94A3B8")   # rules, footer, secondary text
LT_GRAY  = colors.HexColor("#CBD5E1")   # response area borders
NEAR_BLK = colors.HexColor("#1E293B")   # body text (near-black)
WHITE    = colors.white

# ── Content ────────────────────────────────────────────────────────────────────
POEMS = [
    ("We Wear the Mask",         "Paul Laurence Dunbar · 1896"),
    ("I'm Nobody! Who are you?", "Emily Dickinson · c. 1891"),
    ("The Man with the Hoe",     "Edwin Markham · 1913"),
    ("The Words I Carry",        "Communicate by Design · 2026"),
]

UNIT  = "What the Voice Carries — Figurative Language in Poetry"
STORE = "teacherspayteachers.com/store/communicate-by-design"
W, H  = letter

# ── Page layout constants ──────────────────────────────────────────────────────
LM = 0.5 * inch   # left margin
RM = W - LM       # right margin
TM = H - 0.5 * inch  # top margin (below header)
BM = 0.55 * inch  # bottom margin (above footer)
AVAIL_W = RM - LM

# ── Shared page elements ───────────────────────────────────────────────────────

def draw_header(c):
    """Running header: unit title left · CbD right · thin rule below."""
    y = H - 0.32 * inch
    c.setFont("Helvetica", 7.5)
    c.setFillColor(SLATE)
    c.drawString(LM, y, UNIT)
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(NAVY)
    c.drawRightString(RM, y, "Communicate by Design")
    c.setStrokeColor(SLATE)
    c.setLineWidth(0.4)
    c.line(LM, H - 0.4 * inch, RM, H - 0.4 * inch)


def draw_footer(c, label):
    """Footer rule + label."""
    c.setStrokeColor(SLATE)
    c.setLineWidth(0.4)
    c.line(LM, 0.44 * inch, RM, 0.44 * inch)
    c.setFont("Helvetica", 6.5)
    c.setFillColor(SLATE)
    c.drawCentredString(W / 2, 0.28 * inch,
                        f"{UNIT}  ·  {label}  ·  Communicate by Design  ·  {STORE}")


def poem_header_bar(c, poem_title, poet, y):
    """
    Thin navy bar — ONLY colored fill on student pages (18pt height).
    Rule 2: matches Wonder Layer 5 BAR_H = 18.
    """
    BAR_H = 18
    c.setFillColor(NAVY)
    c.rect(LM, y - BAR_H, AVAIL_W, BAR_H, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 9.5)
    c.setFillColor(WHITE)
    c.drawString(LM + 7, y - BAR_H + 5, poem_title)
    c.setFont("Helvetica-Oblique", 7.5)
    c.drawRightString(RM - 7, y - BAR_H + 5, poet)
    return y - BAR_H - 5


def version_bar(c, code, description, y):
    """
    Version label (V1/V2/V3) — plain bold text + thin gray rule.
    No color fill. Rule 3.
    """
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(NAVY)
    c.drawString(LM, y, code)
    tail_x = LM + c.stringWidth(code + "  ", "Helvetica-Bold", 9)
    c.setFont("Helvetica", 8.5)
    c.setFillColor(SLATE)
    c.drawString(tail_x, y, description)
    y -= 9
    c.setStrokeColor(SLATE)
    c.setLineWidth(0.3)
    c.line(LM, y, RM, y)
    return y - 6


def name_row(c, y):
    """Name / Date / Poem fill-in row."""
    c.setFont("Helvetica", 8.5)
    c.setFillColor(NEAR_BLK)
    c.drawString(LM, y,
        "Name: ________________________________   Date: ____________   Poem: ________________________")
    return y - 16


def nfma_step(c, code, desc, y):
    """
    NFMA step — bold code text + 3pt left accent bar (navy).
    No fill on the label itself. Rule 3.
    """
    accent_h = 16
    c.setFillColor(NAVY)
    c.rect(LM, y - accent_h + 4, 3, accent_h, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(NAVY)
    c.drawString(LM + 7, y, code)
    c.setFont("Helvetica", 8.5)
    c.setFillColor(NEAR_BLK)
    c.drawString(LM + 7 + c.stringWidth(code + "  ", "Helvetica-Bold", 9), y, desc)
    return y - 17


def response_lines(c, y, n=3):
    """Plain blank writing lines."""
    for _ in range(n):
        y -= 20
        c.setStrokeColor(SLATE)
        c.setLineWidth(0.5)
        c.line(LM + 8, y, RM, y)
    return y - 7


def response_box(c, y, h=0.45 * inch, label=None):
    """
    White box with light gray border — for indicate/select response areas.
    Rule 4: white fill, #CBD5E1 border.
    """
    c.setFillColor(WHITE)
    c.setStrokeColor(LT_GRAY)
    c.setLineWidth(0.7)
    c.rect(LM, y - h, AVAIL_W, h, fill=1, stroke=1)
    if label:
        c.setFont("Helvetica", 8)
        c.setFillColor(SLATE)
        c.drawString(LM + 8, y - h + 7, label)
    return y - h - 6


def choice_row(c, y, choices):
    """[ ] checkbox options on a line."""
    x = LM + 8
    c.setFont("Helvetica", 8.5)
    c.setFillColor(NEAR_BLK)
    for ch in choices:
        c.drawString(x, y, f"[ ]  {ch}")
        x += c.stringWidth(f"[ ]  {ch}     ", "Helvetica", 8.5)
    return y - 15


def sentence_frame(c, y, text):
    """Single sentence-frame fill-in line."""
    c.setFont("Helvetica", 8.5)
    c.setFillColor(NEAR_BLK)
    c.drawString(LM + 8, y, text)
    return y - 18


# ── Cover page (white background, text only) ──────────────────────────────────

def cover_page(c):
    y = H - 0.9 * inch

    # Unit title block
    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(NAVY)
    c.drawCentredString(W / 2, y, "What the Voice Carries")
    y -= 26

    c.setFont("Helvetica", 12)
    c.setFillColor(SLATE)
    c.drawCentredString(W / 2, y, "Figurative Language in Poetry")
    y -= 14

    # Thin navy rule
    c.setStrokeColor(NAVY)
    c.setLineWidth(1)
    c.line(LM, y, RM, y)
    y -= 18

    # Packet label
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(NAVY)
    c.drawCentredString(W / 2, y, "Student Response Packet")
    y -= 14

    # Essential question
    c.setFont("Helvetica-Oblique", 9.5)
    c.setFillColor(NEAR_BLK)
    c.drawCentredString(W / 2, y,
        "How do poets use figurative language to say what words alone cannot?")
    y -= 28

    # Thin slate rule
    c.setStrokeColor(SLATE)
    c.setLineWidth(0.5)
    c.line(LM, y, RM, y)
    y -= 18

    # Poems
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(NAVY)
    c.drawCentredString(W / 2, y, "This packet includes four poems:")
    y -= 14

    for title, poet in POEMS:
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(NEAR_BLK)
        c.drawCentredString(W / 2, y, title)
        y -= 11
        c.setFont("Helvetica-Oblique", 8)
        c.setFillColor(SLATE)
        c.drawCentredString(W / 2, y, poet)
        y -= 17

    y -= 8
    c.setStrokeColor(SLATE)
    c.setLineWidth(0.4)
    c.line(LM, y, RM, y)
    y -= 18

    # NFMA strategy
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(NAVY)
    c.drawCentredString(W / 2, y, "NOTICE  ·  FEEL  ·  MEAN  ·  ASK")
    y -= 14

    c.setFont("Helvetica", 8.5)
    c.setFillColor(SLATE)
    c.drawCentredString(W / 2, y, "Use the NFMA strategy with every poem.")
    y -= 14

    nfma_desc = [
        ("N — NOTICE:", "Identify figurative language. Name the type and copy the line."),
        ("F — FEEL:", "What emotion does this language create? What is the tone?"),
        ("M — MEAN:", "What does the figurative language really mean? What is the poet's message?"),
        ("A — ASK:", "What do you still wonder? Point to, select, or indicate evidence from the poem."),
    ]
    for code, desc in nfma_desc:
        c.setFont("Helvetica-Bold", 8.5)
        c.setFillColor(NAVY)
        c.drawString(1.1 * inch, y, code)
        c.setFont("Helvetica", 8.5)
        c.setFillColor(NEAR_BLK)
        c.drawString(1.1 * inch + c.stringWidth(code + " ", "Helvetica-Bold", 8.5), y, desc)
        y -= 13

    y -= 12
    c.setStrokeColor(SLATE)
    c.setLineWidth(0.4)
    c.line(LM, y, RM, y)
    y -= 16

    # Version guide
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(NAVY)
    c.drawCentredString(W / 2, y, "Version Guide")
    y -= 13

    versions = [
        ("V1 — Open Analysis:", "Complete sentences with evidence from the poem."),
        ("V2 — Guided Response:", "Sentence frames and [ ] choice boxes."),
        ("V3 — Symbol-Supported:", "Indicate, point, or use AAC to respond. All access modes valid."),
    ]
    for code, desc in versions:
        c.setFont("Helvetica-Bold", 8.5)
        c.setFillColor(NAVY)
        c.drawString(1.1 * inch, y, code)
        c.setFont("Helvetica", 8.5)
        c.setFillColor(NEAR_BLK)
        c.drawString(1.1 * inch + c.stringWidth(code + " ", "Helvetica-Bold", 8.5), y, desc)
        y -= 13

    # Footer
    draw_footer(c, "Student Response Packet")
    c.showPage()


# ── V1 — Open analysis ────────────────────────────────────────────────────────

def v1_page(c, poem_title, poet):
    draw_header(c)
    y = TM

    y = poem_header_bar(c, poem_title, poet, y)
    y = version_bar(c, "V1 — Open Analysis",
                    "Write your response using complete sentences and evidence from the poem.", y)
    y = name_row(c, y)
    y -= 4

    y = nfma_step(c, "N — NOTICE:", "Identify one example of figurative language. Name the type and copy the line from the poem.", y)
    y = response_lines(c, y, n=3)
    y -= 6

    y = nfma_step(c, "F — FEEL:", "What feeling does this figurative language create? How does it connect to the poem's tone?", y)
    y = response_lines(c, y, n=3)
    y -= 6

    y = nfma_step(c, "M — MEAN:", "What does this figurative language really mean? What does it reveal about the poet's message?", y)
    y = response_lines(c, y, n=4)
    y -= 6

    y = nfma_step(c, "A — ASK:", "Write one question you still have. Then copy at least one line from the poem as evidence.", y)
    y = response_lines(c, y, n=3)

    draw_footer(c, "V1 — Open Analysis")
    c.showPage()


# ── V2 — Guided frames ────────────────────────────────────────────────────────

def v2_page(c, poem_title, poet):
    draw_header(c)
    y = TM

    y = poem_header_bar(c, poem_title, poet, y)
    y = version_bar(c, "V2 — Guided Response",
                    "Use the sentence frames and choice boxes. Complete every step.", y)
    y = name_row(c, y)
    y -= 4

    # N
    y = nfma_step(c, "N — NOTICE:", "What kind of figurative language did you notice?", y)
    y = choice_row(c, y, ["metaphor", "simile", "imagery", "personification", "other: __________"])
    c.setFont("Helvetica", 8.5)
    c.setFillColor(NEAR_BLK)
    c.drawString(LM + 8, y, "The poet uses _________________________ when they write:")
    y -= 16
    y = response_lines(c, y, n=2)
    y -= 6

    # F
    y = nfma_step(c, "F — FEEL:", "What feeling does this language create?", y)
    y = choice_row(c, y, ["hopeful", "hidden", "sad", "proud", "angry", "resigned"])
    y = sentence_frame(c, y, "This creates a _________________ tone because _______________________________.")
    y -= 6

    # M
    y = nfma_step(c, "M — MEAN:", "What does the figurative language really mean?", y)
    y = sentence_frame(c, y, "The figurative language means _________________________________________________")
    y = sentence_frame(c, y, "beyond the literal. This reveals ________________________________________________")
    c.setFont("Helvetica", 8.5)
    c.setFillColor(NEAR_BLK)
    c.drawString(LM + 8, y, "about the poet's message.")
    y -= 22

    # A
    y = nfma_step(c, "A — ASK:", "What do you still wonder?", y)
    y = sentence_frame(c, y, "I wonder ______________________________________________________________________.")
    y = sentence_frame(c, y, "The evidence from the poem is: ________________________________________________.")

    draw_footer(c, "V2 — Guided Response")
    c.showPage()


# ── V3 — Symbol-supported / indicate ─────────────────────────────────────────

def v3_page(c, poem_title, poet):
    draw_header(c)
    y = TM

    y = poem_header_bar(c, poem_title, poet, y)
    y = version_bar(c, "V3 — Symbol-Supported Response",
                    "Partner reads aloud · 5-second wait after each prompt · All access modes valid", y)
    y = name_row(c, y)
    y -= 4

    # N — NOTICE
    y = nfma_step(c, "N — NOTICE:", "Indicate the line that uses figurative language.  [Partner: do not tell — wait 5 seconds]", y)
    c.setFont("Helvetica", 8.5)
    c.setFillColor(NEAR_BLK)
    c.drawString(LM + 8, y, "What kind?  Circle, point to, or indicate:")
    y -= 14
    y = response_box(c, y, h=0.38 * inch,
                     label="metaphor          simile          imagery          personification          other: ________")
    y -= 2

    # F — FEEL
    y = nfma_step(c, "F — FEEL:", "How does this poem make you feel?  [Partner: offer 4 choices, wait]", y)
    y = response_box(c, y, h=0.38 * inch,
                     label="hopeful          hidden          sad          proud")
    c.setFont("Helvetica", 8.5)
    c.setFillColor(NEAR_BLK)
    c.drawString(LM + 8, y, "It feels _________________________ because ________________________________.")
    y -= 20

    # M — MEAN
    y = nfma_step(c, "M — MEAN:", "What does the figurative language really mean?  [Partner: read each choice, wait]", y)
    y = response_box(c, y, h=0.42 * inch,
                     label="[ ] The poet is hiding something.     [ ] The poet is proud.     [ ] The poet is in pain.")
    y -= 2

    # A — ASK
    y = nfma_step(c, "A — ASK:", "What do you wonder?  [Partner: read choices, then point to poem for evidence]", y)
    y = response_box(c, y, h=0.42 * inch,
                     label="[ ] I wonder why the poet chose this word.   [ ] I wonder what happened next.   [ ] I wonder who the speaker is.")
    c.setFont("Helvetica", 8)
    c.setFillColor(SLATE)
    c.drawString(LM + 8, y, "Point to or indicate a line in the poem as evidence.  Partner: circle the line.")

    draw_footer(c, "V3 — Symbol-Supported Response")
    c.showPage()


# ── Build ─────────────────────────────────────────────────────────────────────

def build():
    c = rl_canvas.Canvas(OUT, pagesize=letter)

    # PDF metadata
    c.setTitle("What the Voice Carries — Student Poetry Packet | Communicate by Design")
    c.setAuthor("Communicate by Design | Jill McCardel")
    c.setSubject("Poetry Reading Unit · Figurative Language Analysis · Grades 6–10")
    c.setCreator("Communicate by Design")

    cover_page(c)

    for poem_title, poet in POEMS:
        v1_page(c, poem_title, poet)

    for poem_title, poet in POEMS:
        v2_page(c, poem_title, poet)

    for poem_title, poet in POEMS:
        v3_page(c, poem_title, poet)

    c.save()
    size = os.path.getsize(OUT)
    print(f"Student Packet (b&w printable): {OUT}")
    print(f"Size: {size / 1024:.1f} KB  ·  Pages: 13 (1 cover + 4 V1 + 4 V2 + 4 V3)")
    print("Standard: white background · thin navy bar only · light gray borders")


if __name__ == "__main__":
    build()

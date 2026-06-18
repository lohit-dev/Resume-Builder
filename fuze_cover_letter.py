from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    HRFlowable,
)
from reportlab.lib.enums import TA_LEFT, TA_RIGHT

OUTPUT = "./resumes/fuze_cover_letter.pdf"

# ── Colours ──────────────────────────────────────────────────────────────────
BLACK = colors.HexColor("#0d0d0d")
DARK = colors.HexColor("#1a1a1a")
MUTED = colors.HexColor("#555555")
RULE = colors.HexColor("#c7d5ea")
ACCENT = colors.HexColor("#1f5fa8")

# ── Document ─────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=letter,
    leftMargin=0.65 * inch,
    rightMargin=0.65 * inch,
    topMargin=0.55 * inch,
    bottomMargin=0.55 * inch,
)


# ── Styles ────────────────────────────────────────────────────────────────────
def S(name, **kw):
    base = {
        "fontName": "Helvetica",
        "fontSize": 10,
        "leading": 15,
        "textColor": BLACK,
        "spaceAfter": 0,
        "spaceBefore": 0,
    }
    base.update(kw)
    return ParagraphStyle(name, **base)


name_style = S(
    "name", fontName="Helvetica-Bold", fontSize=20, leading=24, alignment=TA_LEFT
)
contact_style = S(
    "contact", fontSize=8.2, textColor=MUTED, alignment=TA_LEFT, leading=12
)
date_style = S("date", fontSize=9.2, textColor=MUTED, alignment=TA_RIGHT, leading=13)
body_style = S("body", fontSize=9.8, leading=16.5, textColor=DARK)
sig_style = S(
    "sig", fontName="Helvetica-Bold", fontSize=10, textColor=BLACK, leading=14
)


def rule():
    return HRFlowable(
        width="100%", thickness=0.5, color=RULE, spaceAfter=5, spaceBefore=0
    )


def sp(h=4):
    return Spacer(1, h)


def para(text):
    return Paragraph(text, body_style)


# ── Content ───────────────────────────────────────────────────────────────────
story = []

# Header
story.append(Paragraph("Dinavahi Lohith Sai", name_style))
story.append(sp(2))
story.append(
    Paragraph(
        "Full-Stack &amp; Systems Developer &nbsp;·&nbsp; Go &nbsp;·&nbsp; Rust &nbsp;·&nbsp; TypeScript &nbsp;·&nbsp; Cloud &amp; Open Source",
        S("sub", fontSize=9.5, textColor=MUTED, alignment=TA_LEFT, leading=13),
    )
)
story.append(sp(4))
story.append(
    Paragraph(
        "lohitsaidev@gmail.com · +91 70757-53289 · Vijayawada, India", contact_style
    )
)
story.append(sp(2))
story.append(
    Paragraph(
        "<link href='https://github.com/lohit-dev'>github.com/lohit-dev</link> · "
        "<link href='https://lohit.xyz'>lohit.xyz</link> · "
        "<link href='https://resume.lohit.xyz'>resume.lohit.xyz</link>",
        contact_style,
    )
)
story.append(sp(8))
story.append(rule())
story.append(sp(10))

# Date
story.append(Paragraph("June 18, 2026", date_style))
story.append(sp(12))

# Addressee
story.append(para("<b>Fuze Health Talent Acquisition Team</b>"))
story.append(sp(2))
story.append(para("Remote, United States"))
story.append(sp(16))

# Salutation
story.append(para("Dear Hiring Team,"))
story.append(sp(12))

# Para 1 - Opening & motivation
story.append(
    para(
        "I am excited to apply for the Graduate Software Engineer position at Fuze Health. "
        "I recently completed my B.Tech in Computer Science and have spent the past 1.5 years "
        "building production backend systems in Go and Rust. What drew me to Fuze Health is the "
        "opportunity to work at the intersection of software engineering, cloud platforms, and "
        "real-world healthcare impact. The chance to contribute to products that genuinely help "
        "patients is something I find deeply motivating."
    )
)
story.append(sp(11))

# Para 2 - Production experience & observability
story.append(
    para(
        "At Hashira Works, I built and maintained backend services for Garden Finance in Go and Rust. "
        "A core part of that work involved reading application logs, tracing failures across watcher "
        "services and order-execution pipelines, and getting to the root cause quickly under production "
        "pressure. I also shipped monitoring automation including a Twitter bot for high-value trade "
        "alerts and a Strava-to-Discord notification bot, both of which are still running after three "
        "design iterations. Those experiences taught me how critical clear observability and solid "
        "documentation are when things go wrong."
    )
)
story.append(sp(11))

# Para 3 - Hackathon, tech breadth & closing
story.append(
    para(
        "My technical background includes Go, Rust, Python, TypeScript, PostgreSQL, AWS, Docker, "
        "and REST APIs. I enjoy learning new tools quickly and have proven that under pressure. At the "
        "Polkadot Cloud Hackathon, I led backend development for TravelID 2.0, a blockchain-based "
        "travel identity verification platform built in Rust and Axum, and we won 3rd place and a "
        "$1,000 prize. I also taught Python to first-year engineering students, which strengthened "
        "my ability to explain technical problems clearly across different audiences. I would love the "
        "opportunity to bring this background to Fuze Health and grow alongside an experienced "
        "engineering team."
    )
)
story.append(sp(11))

# Para 4 - Thank you
story.append(
    para("Thank you for your time and consideration.")
)
story.append(sp(20))

# Sign-off
story.append(para("Warm regards,"))
story.append(sp(12))
story.append(Paragraph("Dinavahi Lohith Sai", sig_style))
story.append(sp(3))
story.append(
    Paragraph(
        "<link href='mailto:lohitsaidev@gmail.com'>lohitsaidev@gmail.com</link> · "
        "<link href='https://lohit.xyz'>lohit.xyz</link> · "
        "<link href='https://github.com/lohit-dev'>github.com/lohit-dev</link>",
        contact_style,
    )
)

# ── Build ─────────────────────────────────────────────────────────────────────
doc.build(story)
print(f"Done → {OUTPUT}")

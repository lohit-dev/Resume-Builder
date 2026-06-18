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

OUTPUT = "./resumes/cover_letter.pdf"

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
        "Full-Stack &amp; Systems Developer &nbsp;·&nbsp; Go &nbsp;·&nbsp; Rust &nbsp;·&nbsp; Typescript &nbsp;·&nbsp; Cloud &amp; Open Source",
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
story.append(Paragraph("May 20, 2026", date_style))
story.append(sp(12))

# Addressee
story.append(para("<b>HENNGE K.K. Engineering Talent Acquisition Team</b>"))
story.append(sp(2))
story.append(para("Shibuya-ku, Tokyo, Japan"))
story.append(sp(16))

# Salutation
story.append(para("Dear HENNGE Recruitment Team,"))
story.append(sp(12))

# Para 1 — Third time, genuine motivation
story.append(
    para(
        "This is my third time applying to HENNGE's Global Internship Program, and I want to be upfront "
        "about that. I keep coming back because I genuinely want to be here not just in Japan, but at "
        "HENNGE specifically. The culture of always challenging, the international engineering team, and "
        "the seriousness with which you approach cloud security are things I have not found elsewhere. "
        "Each application has made me a stronger engineer, and I believe this one reflects that."
    )
)
story.append(sp(11))

# Para 2 — Mission 3 highlight
story.append(
    para(
        "I particularly love Mission 3 always. Implementing a TOTP client from scratch reading "
        "RFC 6238 and its errata, switching from the default HMAC-SHA-1 to HMAC-SHA-512, deriving the "
        "shared secret correctly, and wiring it all into an HTTP Basic Auth POST was genuinely "
        "interesting. The RFC reading will always be the hardest part, technical specifications reward patience and "
        "precision in a way that I find satisfying once it clicks. Getting that 200 back felt earned."
    )
)
story.append(sp(11))

# Para 3 — Experience, brief
story.append(
    para(
        "Over the past 1.5 years at Hashira Works, I built production backend services for Garden Finance "
        "in Go and Rust, watcher services, on-chain extraction pipelines, and cross-chain integrations "
        "that are still running in production. I also won 3rd place ($1,000) at the Polkadot Cloud "
        "Hackathon, leading backend development for a decentralised document verification platform in Rust "
        "and Axum. I am comfortable with Go, Docker, AWS, and Unix environments, and I am finished my "
        "B.Tech in Computer Science this year."
    )
)
story.append(sp(11))

# Para 4 — Culture, Japan, closing
story.append(
    para(
        "On a personal note, I have been learning Japanese, and I follow authors like Yuu Kamiya and "
        "Reki Kawahara whose work first made me curious about Japan. I am not applying because Japan is "
        "an opportunity, I am applying because HENNGE is a place I want to contribute to and grow in. "
        "I would be grateful for the chance to show that in person. Please consider this CV."
    )
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

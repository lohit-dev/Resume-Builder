"""
Cover letter PDF template.

Usage:
    from templates.cover_letter import build
    build(profile, meta, paragraphs, "./resumes/output.pdf")

Args:
    profile    – dict from content/profile.yaml
    meta       – dict from cover letter frontmatter (company, date, salutation, …)
    paragraphs – list[str] of body paragraph strings (plain text, no HTML needed)
    output_path – where to write the PDF
"""
import html as _html
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.enums import TA_LEFT, TA_RIGHT

# ── Palette ───────────────────────────────────────────────────────────────────
BLACK = colors.HexColor("#0d0d0d")
DARK  = colors.HexColor("#1a1a1a")
MUTED = colors.HexColor("#555555")
RULE  = colors.HexColor("#c7d5ea")


def _style(name, **kw):
    base = dict(fontName="Helvetica", fontSize=10, leading=15,
                textColor=BLACK, spaceAfter=0, spaceBefore=0)
    base.update(kw)
    return ParagraphStyle(name, **base)


def _sp(h=4):
    return Spacer(1, h)


def _rule():
    return HRFlowable(width="100%", thickness=0.5, color=RULE,
                      spaceAfter=5, spaceBefore=0)


def _e(text):
    """Escape plain text for safe use inside reportlab Paragraph."""
    return _html.escape(str(text))


# ── Main builder ──────────────────────────────────────────────────────────────
def build(profile: dict, meta: dict, paragraphs: list, output_path: str):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=0.65 * inch,
        rightMargin=0.65 * inch,
        topMargin=0.55 * inch,
        bottomMargin=0.55 * inch,
    )

    name_st    = _style("cl_name",    fontName="Helvetica-Bold", fontSize=20, leading=24, alignment=TA_LEFT)
    contact_st = _style("cl_contact", fontSize=8.2, textColor=MUTED, alignment=TA_LEFT, leading=12)
    sub_st     = _style("cl_sub",     fontSize=9.5, textColor=MUTED, alignment=TA_LEFT, leading=13)
    date_st    = _style("cl_date",    fontSize=9.2, textColor=MUTED, alignment=TA_RIGHT, leading=13)
    body_st    = _style("cl_body",    fontSize=9.8, leading=16.5, textColor=DARK)
    sig_st     = _style("cl_sig",     fontName="Helvetica-Bold", fontSize=10, textColor=BLACK, leading=14)

    def para(text):
        return Paragraph(text, body_st)

    links = profile["links"]
    story = []

    # ── Header ────────────────────────────────────────────────────────────────
    story.append(Paragraph(_e(profile["name"]), name_st))
    story.append(_sp(2))
    story.append(Paragraph(_e(profile["tagline"]), sub_st))
    story.append(_sp(4))
    story.append(Paragraph(
        f"{_e(profile['email'])} · {_e(profile['phone'])} · {_e(profile['location'])}",
        contact_st,
    ))
    story.append(_sp(2))
    story.append(Paragraph(
        f"<link href='{links['github_url']}'>{_e(links['github_label'])}</link> · "
        f"<link href='{links['website_url']}'>{_e(links['website_label'])}</link> · "
        f"<link href='{links['resume_url']}'>{_e(links['resume_label'])}</link>",
        contact_st,
    ))
    story.append(_sp(8))
    story.append(_rule())
    story.append(_sp(10))

    # ── Date ──────────────────────────────────────────────────────────────────
    story.append(Paragraph(_e(meta["date"]), date_st))
    story.append(_sp(12))

    # ── Addressee ─────────────────────────────────────────────────────────────
    company  = _e(meta.get("company", ""))
    team     = _e(meta.get("team", ""))
    location = _e(meta.get("location", ""))
    heading  = f"<b>{company} {team}</b>".strip() if team else f"<b>{company}</b>"
    story.append(para(heading))
    if location:
        story.append(_sp(2))
        story.append(para(location))
    story.append(_sp(16))

    # ── Salutation ────────────────────────────────────────────────────────────
    story.append(para(_e(meta.get("salutation", "Dear Hiring Team,"))))
    story.append(_sp(12))

    # ── Body ──────────────────────────────────────────────────────────────────
    for i, text in enumerate(paragraphs):
        story.append(para(_e(text)))
        if i < len(paragraphs) - 1:
            story.append(_sp(11))
    story.append(_sp(20))

    # ── Sign-off ──────────────────────────────────────────────────────────────
    story.append(para("Warm regards,"))
    story.append(_sp(12))
    story.append(Paragraph(_e(profile["name"]), sig_st))
    story.append(_sp(3))
    story.append(Paragraph(
        f"<link href='mailto:{profile['email']}'>{_e(profile['email'])}</link> · "
        f"<link href='{links['website_url']}'>{_e(links['website_label'])}</link> · "
        f"<link href='{links['github_url']}'>{_e(links['github_label'])}</link>",
        contact_st,
    ))

    doc.build(story)

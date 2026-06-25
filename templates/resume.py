"""
Resume PDF template.

Usage:
    from templates.resume import build
    build(profile, resume_data, "./resumes/resume.pdf")

Args:
    profile     – dict from content/profile.yaml
    resume_data – dict from content/resume.yaml
    output_path – where to write the PDF
"""
import html as _html
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
    Table, TableStyle, KeepTogether, PageBreak,
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER

# ── Palette ───────────────────────────────────────────────────────────────────
BLACK  = colors.HexColor("#0d0d0d")
DARK   = colors.HexColor("#1a1a1a")
MUTED  = colors.HexColor("#555555")
RULE   = colors.HexColor("#c7d5ea")
ACCENT = colors.HexColor("#1f5fa8")


def _style(name, **kw):
    base = dict(fontName="Helvetica", fontSize=10, leading=14,
                textColor=BLACK, spaceAfter=0, spaceBefore=0)
    base.update(kw)
    return ParagraphStyle(name, **base)


def _sp(h=3):
    return Spacer(1, h)


def _rule():
    return HRFlowable(width="100%", thickness=0.5, color=RULE,
                      spaceAfter=4, spaceBefore=0)


def _e(text):
    """Escape plain text for safe use inside reportlab Paragraph."""
    return _html.escape(str(text))


# ── Main builder ──────────────────────────────────────────────────────────────
def build(profile: dict, data: dict, output_path: str):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=0.35 * inch,
        rightMargin=0.55 * inch,
        topMargin=0.45 * inch,
        bottomMargin=0.45 * inch,
    )

    # Styles
    name_st    = _style("r_name",    fontName="Helvetica-Bold", fontSize=20, leading=24, alignment=TA_LEFT)
    contact_st = _style("r_contact", fontSize=8.2, textColor=MUTED, alignment=TA_LEFT, leading=12)
    sub_st     = _style("r_sub",     fontSize=9.5, textColor=MUTED, alignment=TA_LEFT, leading=13)
    section_st = _style("r_section", fontName="Helvetica-Bold", fontSize=9.5,
                        textColor=ACCENT, spaceBefore=7, spaceAfter=2, leading=12)
    jobtitle_st = _style("r_jobtitle", fontName="Helvetica-Bold", fontSize=10, textColor=BLACK, leading=13)
    company_st  = _style("r_company",  fontSize=9, textColor=MUTED, leading=12)
    meta_st     = _style("r_meta",     fontSize=9, textColor=MUTED, leading=12, alignment=TA_LEFT)
    bullet_st   = _style("r_bullet",   fontSize=9.2, leading=13.5, leftIndent=0, firstLineIndent=0, textColor=DARK)
    skills_st   = _style("r_skills",   fontSize=9.2, leading=13.5, textColor=DARK)
    summary_st  = _style("r_summary",  fontSize=9.3, leading=14, textColor=DARK, spaceAfter=2)
    stack_st    = _style("r_stack",    fontSize=8.5, textColor=MUTED, leading=12)

    def section(title):
        return [Paragraph(_e(title).upper(), section_st), _rule()]

    def bullet(text):
        # bullets may contain reportlab HTML markup from YAML — pass through as-is
        return Paragraph(text, bullet_st)

    def exp_header(title, company_line, dates):
        return [
            Paragraph(_e(title), jobtitle_st),
            Paragraph(company_line, company_st),
            Paragraph(_e(dates), meta_st),
            _sp(3),
        ]

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
        f"<link href='{links['linkedin_url']}'>{_e(links['linkedin_label'])}</link> · "
        f"<link href='{links['website_url']}'>{_e(links['website_label'])}</link> · "
        f"<link href='{links['resume_url']}'>{_e(links['resume_label'])}</link>",
        contact_st,
    ))
    story.append(_sp(6))

    # ── Summary ───────────────────────────────────────────────────────────────
    story += section("Summary")
    story.append(_sp(2))
    story.append(Paragraph(data["summary"], summary_st))
    story.append(_sp(4))

    # ── Skills ────────────────────────────────────────────────────────────────
    story += section("Technical Skills")
    story.append(_sp(2))
    for skill in data["skills"]:
        story.append(Paragraph(
            f"<b>{_e(skill['label'])}</b>&nbsp;&nbsp;&nbsp;{_e(skill['value'])}",
            skills_st,
        ))
        story.append(_sp(1.5))
    story.append(_sp(4))

    # ── Experience ────────────────────────────────────────────────────────────
    story += section("Professional Experience")
    story.append(_sp(3))

    for job in data["experience"]:
        # Build company line (with optional link)
        company_name = _e(job["company"])
        if job.get("company_url") and job.get("company_url_label"):
            company_line = (
                f"{company_name} · "
                f"<link href='{job['company_url']}'>{_e(job['company_url_label'])}</link>"
            )
        else:
            company_line = company_name

        story += exp_header(job["title"], company_line, job["dates"])

        for i, b in enumerate(job.get("bullets", [])):
            story.append(bullet(b))
            if i < len(job["bullets"]) - 1:
                story.append(_sp(2))
        story.append(_sp(5))

    # ── Projects ──────────────────────────────────────────────────────────────
    story.append(PageBreak())
    story += section("Projects")
    story.append(_sp(2))

    for proj in data["projects"]:
        block = []
        # Title + optional badge
        if proj.get("badge"):
            block.append(Paragraph(
                f"<b>{_e(proj['title'])}</b>  "
                f"<font color='#1f5fa8'><b><i>{_e(proj['badge'])}</i></b></font>",
                jobtitle_st,
            ))
        else:
            block.append(Paragraph(f"<b>{_e(proj['title'])}</b>", jobtitle_st))

        if proj.get("stack"):
            block.append(Paragraph(_e(proj["stack"]), stack_st))

        block.append(_sp(3))

        for i, b in enumerate(proj.get("bullets", [])):
            block.append(bullet(b))
            if i < len(proj["bullets"]) - 1:
                block.append(_sp(2))

        block.append(_sp(5))
        story.append(KeepTogether(block))

    # ── Education ─────────────────────────────────────────────────────────────
    story += section("Education")
    story.append(_sp(3))

    for edu in data["education"]:
        story += exp_header(edu["degree"], _e(edu["institution"]), edu["dates"])
        for i, b in enumerate(edu.get("bullets", [])):
            story.append(bullet(b))
            if i < len(edu.get("bullets", [])) - 1:
                story.append(_sp(2))
        story.append(_sp(5))

    # ── Languages ─────────────────────────────────────────────────────────────
    story += section("Languages")
    story.append(_sp(2))
    lang_parts = []
    for lang in data["languages"]:
        lang_parts.append(f"<b>{_e(lang['name'])}</b> — {_e(lang['level'])}")
    story.append(Paragraph(
        " &nbsp;&nbsp;·&nbsp;&nbsp; ".join(lang_parts),
        skills_st,
    ))

    doc.build(story)

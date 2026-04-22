
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle, KeepTogether, PageBreak
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
import os

OUTPUT = "./resumes/resume.pdf"

# ── Colours ──────────────────────────────────────────────────────────────────
BLACK   = colors.HexColor("#0d0d0d")
DARK    = colors.HexColor("#1a1a1a")
MUTED   = colors.HexColor("#555555")
RULE    = colors.HexColor("#c7d5ea")
ACCENT  = colors.HexColor("#1f5fa8")

# ── Document ─────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=letter,
    leftMargin=0.35*inch,
    rightMargin=0.55*inch,
    topMargin=0.45*inch,
    bottomMargin=0.45*inch,
)

W = letter[0] - doc.leftMargin - doc.rightMargin   # usable width

# ── Styles ────────────────────────────────────────────────────────────────────
def S(name, **kw):
    base = {
        "fontName": "Helvetica",
        "fontSize": 10,
        "leading": 14,
        "textColor": BLACK,
        "spaceAfter": 0,
        "spaceBefore": 0,
    }
    base.update(kw)
    return ParagraphStyle(name, **base)

name_style      = S("name",      fontName="Helvetica-Bold", fontSize=20, leading=24, textColor=BLACK, alignment=TA_LEFT)
contact_style   = S("contact",   fontSize=8.2, textColor=MUTED, alignment=TA_LEFT, leading=12)
section_style   = S("section",   fontName="Helvetica-Bold", fontSize=9.5, textColor=ACCENT,
                     spaceBefore=7, spaceAfter=2, leading=12)
job_title_style = S("jobtitle",  fontName="Helvetica-Bold", fontSize=10, textColor=BLACK, leading=13)
company_style   = S("company",   fontSize=9, textColor=MUTED, leading=12)
bullet_style    = S("bullet",    fontSize=9.2, leading=13.5, leftIndent=0, firstLineIndent=0,
                     textColor=DARK)
skills_style    = S("skills",    fontSize=9.2, leading=13.5, textColor=DARK)
summary_style   = S("summary",   fontSize=9.3, leading=14, textColor=DARK, spaceAfter=2)
meta_style      = S("meta",      fontSize=9, textColor=MUTED, leading=12, alignment=TA_LEFT)

def rule():
    return HRFlowable(width="100%", thickness=0.5, color=RULE, spaceAfter=4, spaceBefore=0)

def section(title):
    return [Paragraph(title.upper(), section_style), rule()]

def bullet(text):
    return Paragraph(text, bullet_style)

def sp(h=3):
    return Spacer(1, h)

# ── Content ───────────────────────────────────────────────────────────────────
story = []

# NAME
story.append(Paragraph("Dinavahi Lohith Sai", name_style))
story.append(sp(2))
story.append(Paragraph(
    "Full-Stack &amp; Systems Developer &nbsp;·&nbsp; Go &nbsp;·&nbsp; Rust &nbsp;·&nbsp; Node.js &nbsp;·&nbsp; Cloud &amp; Open Source",
    S("sub", fontSize=9.5, textColor=MUTED, alignment=TA_LEFT, leading=13)
))
story.append(sp(4))
story.append(Paragraph(
    "lohitsaidev@gmail.com · +91 70757-53289 · Vijayawada, India",
    contact_style
))
story.append(sp(2))
story.append(Paragraph(
    "<link href='https://github.com/lohit-dev'>github.com/lohit-dev</link> · "
    "<link href='https://www.linkedin.com/in/dinavahi-lohit-sai-192a382b1'>linkedin.com/in/dinavahi-lohit-sai-192a382b1</link> · "
    "<link href='https://lohit.xyz'>lohit.xyz</link> · "
    "<link href='https://resume.lohit.xyz'>resume.lohit.xyz</link>",
    contact_style
))
story.append(sp(6))

# SUMMARY
story += section("Summary")
story.append(sp(2))
story.append(Paragraph(
    "1.5+ years building production backend systems in Go and Rust. "
    "Built real-time trading infrastructure at <link href='https://garden.finance'>Garden.Finance</link>, shipped multi-chain integrations, and delivered tooling used in daily operations. "
    "Won 3rd place ($1,000) at Polkadot Cloud Hackathon. Looking for backend SDE-1 roles focused on systems and distributed services.",
    summary_style
))
story.append(sp(4))

# SKILLS
story += section("Technical Skills")
story.append(sp(2))

skills_data = [
    ["Languages",         "Go, Rust, TypeScript, JavaScript, Python"],
    ["Backend",           "Axum, Node.js, Express.js, RESTful APIs, WebSockets, Socket.io"],
    ["Databases",         "PostgreSQL, MongoDB, MySQL"],
    ["Infrastructure",    "Docker, Docker Compose, AWS, Git, Gitea, Swagger, CI/CD"],
    ["Frontend / Mobile", "React.js, React Native, Tailwind CSS"],
    ["Tools",             "Neovim, Figma, Android Studio, macOS / Linux (Arch)"],
]

for label, val in skills_data:
    row = Paragraph(
        f"<b>{label}</b>&nbsp;&nbsp;&nbsp;{val}",
        skills_style
    )
    story.append(row)
    story.append(sp(1.5))

story.append(sp(4))

# EXPERIENCE
story += section("Professional Experience")
story.append(sp(3))

def exp_header(title, company_line, dates):
    return [
        Paragraph(title, job_title_style),
        Paragraph(company_line, company_style),
        Paragraph(dates, meta_style),
        sp(3)
    ]

# Hashira
story += exp_header(
    "Software Associate — Go &amp; Rust",
    "Hashira Works · <link href='https://hashira.io'>hashira.io</link>",
    "Dec 2024 – Apr 2026"
)
story.append(bullet(
    "Built and maintained backend services for <b><link href='https://garden.finance'>Garden Finance</link></b> using Go and Rust across watcher services and on-chain extraction pipelines."
))
story.append(sp(2))
story.append(bullet(
    "Built <b>Garden Analyzer</b>, an MCP-integrated analytics app over <link href='https://garden.finance'>Garden.Finance</link> multi-chain data, producing protocol metrics and trend reports."
))
story.append(sp(2))
story.append(bullet(
    "Implemented <b>Spark</b> and <b>Lightning</b> integrations in Rust to expand cross-chain order execution coverage."
))
story.append(sp(2))
story.append(bullet(
    "Built and maintained monitoring automation: Twitter high-value trade image generator bot ($10K+), Strava-to-Discord bot, and a TypeScript arbitrage bot; still running in production after 3 design iterations."
))
story.append(sp(2))
story.append(bullet(
    "Owned deployment scripts and internal tooling for self-hosted infrastructure on Gitea."
))
story.append(sp(5))

# Navodita
story += exp_header(
    "Backend Developer Intern",
    "Navodita Infotech",
    "Feb 2024 – Mar 2024"
)
story.append(bullet(
    "Built a multi-room real-time chat app with Node.js, Express, and Socket.io. "
    "Received a Letter of Recommendation."
))
story.append(sp(5))

# InternIQ
story += exp_header(
    "Web Developer Intern",
    "InternIQ",
    "Mar 2024 – Apr 2024"
)
story.append(bullet(
    "Built and optimized web application features during a 1-month internship; received a Letter of Recommendation for performance."
))
story.append(sp(5))

# Instructor
story += exp_header(
    "Python Instructor (Part-time)",
    "NRI Institute of Technology",
    "May 2022 – Aug 2022"
)
story.append(bullet(
    "Taught Python fundamentals to first-year students such as file I/O, text analysis, logic-building exercises."
))
story.append(sp(2))
story.append(bullet(
    "Designed and delivered beginner-friendly coding sessions including text analyzer, Rock-Paper-Scissors, and file handling projects."
))
story.append(sp(6))

# PROJECTS
story.append(PageBreak())
story += section("Projects")
story.append(sp(2))

def proj_header(title, link_or_badge, stack):
    rows = [Paragraph(f"<b>{title}</b>", job_title_style)]
    if link_or_badge:
        rows.append(Paragraph(link_or_badge, meta_style))
    if stack:
        rows.append(Paragraph(stack, S("stack", fontSize=8.5, textColor=MUTED, leading=12)))
    rows.append(sp(4))
    return rows

# TravelID
travelid_block = []
travelid_block += [
    Paragraph(
        "<b>TravelID 2.0</b> <font color='#1f5fa8'><b><i>3rd Prize · $1,000 · Polkadot Cloud Hackathon</i></b></font>",
        job_title_style
    ),
    Paragraph("Rust, Axum, Subxt, React, TypeScript, PostgreSQL, Polkadot",
              S("stack", fontSize=8.5, textColor=MUTED, leading=12)),
    sp(3)
]
travelid_block.append(bullet(
    "Built a decentralized travel document verification platform on Polkadot using SHA-256 hashes and on-chain Subxt remarks."
))
travelid_block.append(sp(2))
travelid_block.append(bullet(
    "Led backend implementation (Rust, Axum, Subxt) and co-built frontend wallet and QR verification flow."
))
travelid_block.append(sp(5))
story.append(KeepTogether(travelid_block))

# Garden Analyzer
garden_block = []
garden_block += proj_header(
    "Crypto Analyzer",
    "",
    "Go, TypeScript, Claude MCP, <link href='https://garden.finance'>Garden.Finance</link> API, multi-chain data"
)
garden_block.append(bullet(
    "Built an MCP-powered analytics app for <link href='https://garden.finance'>Garden.Finance</link> that evaluates protocol activity across chains and time windows."
))
garden_block.append(sp(2))
garden_block.append(bullet(
    "Generated actionable metrics including 82% volume drop (Q2 vs Q1), 304% new-user increase, and 98% Starknet outbound dominance."
))
garden_block.append(sp(5))
story.append(KeepTogether(garden_block))

# Animax
animax_block = []
animax_block += proj_header(
    "Animax — Anime Streaming App",
    "",
    "React Native, TypeScript, Tailwind CSS, AniWatch API"
)
animax_block.append(bullet(
    "Built a full React Native anime streaming app with browse, search, and episode playback flows."
))
animax_block.append(sp(2))
animax_block.append(bullet(
    "Optimized API fetch and screen transitions for faster load behavior on lower-bandwidth mobile networks."
))
animax_block.append(sp(5))
story.append(KeepTogether(animax_block))

# Real-Time Chat App
chat_block = []
chat_block += [
    Paragraph("<b>Real-Time Chat App</b>", job_title_style),
    Paragraph("Node.js, Express, Socket.io, JavaScript", meta_style),
    sp(3)
]
chat_block.append(bullet(
    "Built a multi-room chat app with live message broadcasting during internship; this became groundwork for Socket.io features later used at Hashira."
))
chat_block.append(sp(5))
story.append(KeepTogether(chat_block))

# Discord / bots
bots_block = []
bots_block += proj_header(
    "Automation Tools/Bots (Discord, Telegram, Twitter)",
    "",
    "Python, TypeScript, discord.py, python-telegram-bot, GitHub API"
)
bots_block.append(bullet(
    "Built a Discord music bot with queue and playback controls used in day-to-day community sessions."
))
bots_block.append(sp(2))
bots_block.append(bullet(
    "Built Telegram and Twitter automation for GitHub release delivery and high-value trade monitoring."
))
bots_block.append(sp(6))
story.append(KeepTogether(bots_block))

# EDUCATION
story += section("Education")
story.append(sp(3))

story += exp_header(
    "B.Tech in Computer Science &amp; Data Science",
    "NRI Institute of Technology, Agiripalli",
    "2022 – 2026 (Final Semester)"
)
story.append(bullet("Member of Google Developers Club; attended hackathons and workshops."))
story.append(sp(2))
story.append(bullet("1st place in college-wide SQL mobile app competition."))
story.append(sp(2))
story.append(bullet("Published two Android apps on the Play Store independently, end-to-end."))
story.append(sp(5))

story += exp_header(
    "Intermediate — MPC (Maths, Physics, Chemistry)",
    "Sri Chaitanya Junior College",
    "2020 – 2022"
)
story.append(sp(2))
story += exp_header(
    "SSC",
    "Ravindra Bharathi Public School",
    "2019 – 2020"
)
story.append(sp(6))

# LANGUAGES
story += section("Languages")
story.append(sp(2))
story.append(Paragraph(
    "<b>English</b> — Proficient &nbsp;&nbsp;·&nbsp;&nbsp; "
    "<b>Telugu</b> — Native &nbsp;&nbsp;·&nbsp;&nbsp; "
    "<b>Hindi</b> — Conversational &nbsp;&nbsp;·&nbsp;&nbsp; "
    "<b>Japanese</b> — Learning",
    skills_style
))

# ── Build ─────────────────────────────────────────────────────────────────────
doc.build(story)
print(f"Done → {OUTPUT}")

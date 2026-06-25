# Resume Builder

Generates PDF resumes and cover letters from structured content files.
Template styling lives in `templates/` — all content is in `content/`.
**You never touch Python to add a new document.**

## Structure

```
content/
  profile.yaml                ← name, contact, links (shared by everything)
  resumes/
    backend.yaml              ← Go/Rust backend-focused resume
    blockchain.yaml           ← Web3/Polkadot/cross-chain resume
    fullstack.yaml            ← React + Node + backend breadth resume
    <new-role>.yaml           ← add more here
  cover_letters/
    mastercard.md             ← letter body + metadata
    fuze.md
    hennge.md
    <new-company>.md          ← add more here

templates/
  cover_letter.py             ← PDF layout engine (no content inside)
  resume.py                   ← PDF layout engine (no content inside)

resumes/                      ← generated PDFs land here
generate.py                   ← CLI entry point
```

## Commands

```bash
# Generate everything
uv run python generate.py all

# Generate a specific resume
uv run python generate.py resume backend
uv run python generate.py resume blockchain
uv run python generate.py resume fullstack

# Generate a specific cover letter
uv run python generate.py cover-letter mastercard
uv run python generate.py cover-letter fuze

# See all available documents
uv run python generate.py --list
```

## Adding a New Resume

1. Create `content/resumes/<role>.yaml` with an `output` field at the top:

```yaml
output: sre_resume.pdf

summary: >-
  Your tailored summary for this role...

skills:
  - label: "Languages"
    value: "Go, Python, Bash"
  # ... rest of skills

experience:
  # ... same structure as existing resumes

projects:
  # ...

education:
  # ...

languages:
  # ...
```

2. Run:
```bash
uv run python generate.py resume <role>
```

## Adding a New Cover Letter

1. Create `content/cover_letters/<company>.md`:

```markdown
---
company: Google
team: Engineering Talent Team
location: Mountain View, CA
date: July 1, 2026
salutation: "Dear Google Recruiting Team,"
output: google_cover_letter.pdf
---

First paragraph of your letter here.

Second paragraph here.

Closing paragraph.
```

2. Run:
```bash
uv run python generate.py cover-letter google
```

## Updating Your Info

| What to change | File to edit |
|---|---|
| Name, email, phone, links | `content/profile.yaml` |
| Resume content for a role | `content/resumes/<role>.yaml` |
| A cover letter | `content/cover_letters/<company>.md` |
| PDF layout / styling | `templates/cover_letter.py` or `templates/resume.py` |

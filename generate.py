"""
generate.py — unified PDF generator

Commands:
  python generate.py resume <name>           → generated/<output from yaml>
  python generate.py cover-letter <name>     → generated/<output from frontmatter>
  python generate.py all                     → all resumes + all cover letters
  python generate.py --list                  → list available resumes and cover letters

Adding a new resume:
  1. Create content/resumes/<name>.yaml
  2. Run: python generate.py resume <name>
  Done.

Adding a new cover letter:
  1. Create content/cover_letters/<name>.md
  2. Run: python generate.py cover-letter <name>
  Done.
"""
import sys
import os
import glob
import yaml

from templates.cover_letter import build as build_cover_letter
from templates.resume import build as build_resume

CONTENT_DIR    = os.path.join(os.path.dirname(__file__), "content")
GEN_DIR        = os.path.join(os.path.dirname(__file__), "generated")
GEN_RESUMES    = os.path.join(GEN_DIR, "resumes")
GEN_CV         = os.path.join(GEN_DIR, "cv")
RESUMES_DIR    = os.path.join(CONTENT_DIR, "resumes")
CL_DIR         = os.path.join(CONTENT_DIR, "cover_letters")


# ── Helpers ───────────────────────────────────────────────────────────────────

def load_profile() -> dict:
    with open(os.path.join(CONTENT_DIR, "profile.yaml"), encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_resume_data(name: str) -> dict:
    path = os.path.join(RESUMES_DIR, f"{name}.yaml")
    if not os.path.exists(path):
        print(f"  Error: {path} not found.")
        sys.exit(1)
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def parse_cover_letter(name: str) -> tuple:
    """Parse a cover letter .md file with YAML frontmatter.
    Returns (meta_dict, list_of_paragraph_strings).
    """
    path = os.path.join(CL_DIR, f"{name}.md")
    if not os.path.exists(path):
        print(f"  Error: {path} not found.")
        sys.exit(1)

    with open(path, encoding="utf-8") as f:
        text = f.read()

    meta, body = {}, text.strip()
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            meta = yaml.safe_load(parts[1]) or {}
            body = parts[2].strip()

    paragraphs = [p.strip() for p in body.split("\n\n") if p.strip()]
    return meta, paragraphs


def list_resumes() -> list:
    pattern = os.path.join(RESUMES_DIR, "*.yaml")
    return sorted(
        os.path.splitext(os.path.basename(f))[0]
        for f in glob.glob(pattern)
    )


def list_cover_letters() -> list:
    pattern = os.path.join(CL_DIR, "*.md")
    return sorted(
        os.path.splitext(os.path.basename(f))[0]
        for f in glob.glob(pattern)
    )


# ── Commands ──────────────────────────────────────────────────────────────────

def cmd_resume(name: str):
    os.makedirs(GEN_RESUMES, exist_ok=True)
    profile = load_profile()
    data    = load_resume_data(name)
    filename = data.get("output", f"{name}_resume.pdf")
    output   = os.path.join(GEN_RESUMES, filename)
    build_resume(profile, data, output)
    print(f"  ✓ resume/{name:<14} → {output}")


def cmd_cover_letter(name: str):
    os.makedirs(GEN_CV, exist_ok=True)
    profile = load_profile()
    meta, paragraphs = parse_cover_letter(name)
    filename = meta.get("output", f"{name}_cover_letter.pdf")
    output   = os.path.join(GEN_CV, filename)
    build_cover_letter(profile, meta, paragraphs, output)
    print(f"  ✓ cover/{name:<16} → {output}")


def cmd_all():
    print("Generating all documents...\n")
    for name in list_resumes():
        cmd_resume(name)
    print()
    for name in list_cover_letters():
        cmd_cover_letter(name)
    print("\nAll done.")


def cmd_list():
    resumes = list_resumes()
    letters = list_cover_letters()

    print("Resumes  (content/resumes/):")
    for name in resumes:
        print(f"  {name}")

    print("\nCover letters  (content/cover_letters/):")
    for name in letters:
        print(f"  {name}")


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]

    if not args:
        cmd_all()
        return

    if args[0] in ("-h", "--help"):
        print(__doc__)
        return

    cmd = args[0]

    if cmd == "resume":
        if len(args) < 2:
            print("Usage: python generate.py resume <name>")
            print("       python generate.py --list   ← to see available names")
            sys.exit(1)
        cmd_resume(args[1])

    elif cmd == "cover-letter":
        if len(args) < 2:
            print("Usage: python generate.py cover-letter <name>")
            print("       python generate.py --list   ← to see available names")
            sys.exit(1)
        cmd_cover_letter(args[1])

    elif cmd == "all":
        cmd_all()

    elif cmd == "--list":
        cmd_list()

    else:
        print(f"Unknown command: {cmd!r}")
        print("Run: python generate.py --help")
        sys.exit(1)


if __name__ == "__main__":
    main()

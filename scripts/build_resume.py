"""Generate docs/resume.tex from data/resume.json.

The JSON file is the editable source of truth. The generated TeX is committed so
content changes remain reviewable even without a LaTeX installation.
"""

from __future__ import annotations

import json
import re
from datetime import date, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "resume.json"
TEMPLATE_PATH = ROOT / "docs" / "resume-template.tex"
OUTPUT_PATH = ROOT / "docs" / "resume.tex"

LATEX_ESCAPES = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}


def tex(value: str) -> str:
    """Escape plain text for LaTeX."""
    return "".join(LATEX_ESCAPES.get(char, char) for char in value)


def rich(value: str) -> str:
    """Convert the supported **bold** JSON markup to LaTeX."""
    pieces = re.split(r"(\*\*.*?\*\*)", value)
    rendered: list[str] = []
    for piece in pieces:
        if piece.startswith("**") and piece.endswith("**"):
            rendered.append(r"\textbf{" + tex(piece[2:-2]) + "}")
        else:
            rendered.append(tex(piece))
    if "**" in "".join(piece for piece in pieces if not (piece.startswith("**") and piece.endswith("**"))):
        raise ValueError(f"Unbalanced bold markup: {value}")
    return "".join(rendered)


def item_list(items: list[str]) -> str:
    body = "\n".join(f"    \\resumeItem{{{rich(item)}}}" for item in items)
    return f"  \\resumeItemListStart\n{body}\n  \\resumeItemListEnd"


def subheading(company: str, period: str, subtitle: str, location: str) -> str:
    return (
        "  \\resumeSubheading\n"
        f"    {{{tex(company)}}}{{{tex(period)}}}\n"
        f"    {{{tex(subtitle)}}}{{{tex(location)}}}"
    )


def experience_start(data: dict) -> date:
    """Find the earliest role start date in the resume data."""
    starts: list[date] = []
    periods: list[str] = []
    for item in data["experience"]:
        periods.append(item["period"])
        periods.extend(role["period"] for role in item.get("roles", []))
    for period in periods:
        value = period.split("--", 1)[0].strip()
        for pattern in ("%b %Y", "%B %Y"):
            try:
                starts.append(datetime.strptime(value, pattern).date())
                break
            except ValueError:
                continue
    if not starts:
        raise ValueError("No parseable experience start date found")
    return min(starts)


def experience_phrase(start: date, as_of: date | None = None) -> str:
    """Return a readable tenure label that updates as the resume is built."""
    as_of = as_of or date.today()
    elapsed_months = max(0, (as_of.year - start.year) * 12 + as_of.month - start.month)
    full_years, remaining_months = divmod(elapsed_months, 12)
    if remaining_months >= 10:
        return f"nearly {full_years + 1} years"
    if remaining_months >= 3:
        return f"more than {full_years} years"
    return f"{full_years}+ years"


def build_body(data: dict) -> str:
    person = data["person"]
    email = person["email"]
    phone_href = re.sub(r"[^+\d]", "", person["phone"])

    header = "\n".join(
        [
            r"\begin{center}",
            f"    \\textbf{{\\Huge {tex(person['name'])}}} " + r"\\ \vspace{4pt}",
            f"    \\small {tex(person['title'])} $|$ {tex(person['location'])} " + r"\\",
            f"    \\href{{tel:{phone_href}}}{{{tex(person['phone'])}}} $|$",
            f"    \\href{{mailto:{email}}}{{{tex(email)}}} " + r"\\",
            f"    \\href{{{person['linkedin']['url']}}}{{{tex(person['linkedin']['label'])}}} $|$",
            f"    \\href{{{person['github']['url']}}}{{{tex(person['github']['label'])}}}",
            r"\end{center}",
            r"\setlength{\footskip}{12pt}",
        ]
    )

    current, *earlier = data["experience"]
    current_parts = [
        r"\section{Experience}",
        r"\resumeSubHeadingListStart",
        subheading(current["company"], current["period"], current["subtitle"], current["location"]),
    ]
    for role in current["roles"]:
        current_parts.append(
            f"  \\resumeSubSubheading{{\\textbf{{{tex(role['title'])}}}}}{{{tex(role['period'])}}}"
        )
        current_parts.append(item_list(role["bullets"]))
    current_parts.append(r"\resumeSubHeadingListEnd")

    earlier_parts = [r"\newpage", r"\section{Earlier Experience}", r"\resumeSubHeadingListStart"]
    for role in earlier:
        earlier_parts.append(subheading(role["company"], role["period"], role["subtitle"], role["location"]))
        earlier_parts.append(item_list(role["bullets"]))
    earlier_parts.append(r"\resumeSubHeadingListEnd")

    skill_lines = (" " + r"\\" + "\n    ").join(
        rf"\textbf{{{tex(skill['category'])}:}} {tex(skill['items'])}" for skill in data["skills"]
    )
    skills = f"""\\section{{Technical Skills}}
\\begin{{itemize}}[leftmargin=0.15in, label={{}}]
  \\small{{\\item{{
    {skill_lines}
  }}}}
\\end{{itemize}}"""

    certifications = "\n".join(f"  \\item {tex(item)}" for item in data["certifications"])
    certs = f"""\\section{{Certifications}}
\\begin{{itemize}}[leftmargin=0.15in, label={{}}, itemsep=2pt]
  \\small
{certifications}
\\end{{itemize}}"""

    education = data["education"]
    education_section = f"""\\section{{Education}}
\\resumeSubHeadingListStart
{subheading(education['degree'], education['period'], education['institution'], education['location'])}
\\resumeSubHeadingListEnd"""

    profile = data["profile"].replace("{experience}", experience_phrase(experience_start(data)))

    return "\n\n".join(
        [
            header,
            rf"\section{{Profile}}" + "\n" + rf"\small{{{tex(profile)}}}",
            "\n".join(current_parts),
            "\n".join(earlier_parts),
            skills,
            certs,
            education_section,
        ]
    )


def main() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    marker = "{{RESUME_BODY}}"
    if template.count(marker) != 1:
        raise ValueError(f"{TEMPLATE_PATH} must contain exactly one {marker} marker")
    output = template.replace(marker, build_body(data)).rstrip() + "\n"
    OUTPUT_PATH.write_text(output, encoding="utf-8", newline="\n")
    print(f"Built {OUTPUT_PATH.relative_to(ROOT)} from {DATA_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

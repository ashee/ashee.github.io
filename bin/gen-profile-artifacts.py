#!/usr/bin/env python3

from __future__ import annotations

import re
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PROFILE = REPO_ROOT / "profile.md"
PUB = REPO_ROOT / "pub"
README = PUB / "README.md"
LINKEDIN = PUB / "linkedin-profile.md"
ONE_PAGER = PUB / "Amitava Shee 1 Pager.md"
RESUME_PDF = PUB / "Amitava Shee Resume.pdf"
ONE_PAGER_PDF = PUB / "Amitava Shee 1 Pager.pdf"
CNAME = REPO_ROOT / "CNAME"


STATE_NAMES = {
    "CA": "California",
    "CO": "Colorado",
    "IN": "Indiana",
    "MD": "Maryland",
    "MI": "Michigan",
    "NY": "New York",
}

MONTHS = {
    "Jan": "January",
    "Feb": "February",
    "Mar": "March",
    "Apr": "April",
    "May": "May",
    "Jun": "June",
    "Jul": "July",
    "Aug": "August",
    "Sep": "September",
    "Oct": "October",
    "Nov": "November",
    "Dec": "December",
}


def read_profile() -> tuple[dict[str, str], str]:
    text = PROFILE.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}, text

    _, raw_meta, body = text.split("---\n", 2)
    meta: dict[str, str] = {}
    current_key: str | None = None
    block_lines: list[str] = []

    for line in raw_meta.splitlines():
        if current_key:
            if line.startswith("  ") or not line:
                block_lines.append(line[2:] if line.startswith("  ") else "")
                continue
            meta[current_key] = "\n".join(block_lines).strip()
            current_key = None
            block_lines = []

        key, sep, value = line.partition(":")
        if not sep:
            continue
        if value.strip() == "|":
            current_key = key.strip()
            block_lines = []
        else:
            meta[key.strip()] = value.strip()

    if current_key:
        meta[current_key] = "\n".join(block_lines).strip()

    return meta, body.lstrip()


def name_and_contact(body: str) -> tuple[str, str, str]:
    lines = [line for line in body.splitlines() if line.strip()]
    name = lines[0].removeprefix("#").strip()
    contact = lines[1].strip()
    location = contact.split("|", 1)[0].strip()
    return name, contact, location


def body_from_summary(body: str) -> str:
    match = re.search(r"^## Summary\s*$", body, flags=re.MULTILINE)
    if not match:
        raise ValueError("profile.md must contain a '## Summary' section")
    return body[match.start() :].strip()


def split_sections(body: str) -> dict[str, str]:
    matches = list(re.finditer(r"^## (.+?)\s*$", body, flags=re.MULTILINE))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        sections[match.group(1)] = body[start:end].strip()
    return sections


def parse_experience(experience: str) -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    current: dict[str, object] | None = None

    for line in experience.splitlines():
        heading = re.match(r"^\*\*(.+?)\*\*\s+\|\s+(.+?)\s+\|\s+(.+?)\s+\|\s+(.+?)\s*$", line)
        if heading:
            if current:
                entries.append(current)
            current = {
                "title": heading.group(1),
                "company": heading.group(2),
                "location": heading.group(3),
                "dates": heading.group(4),
                "bullets": [],
            }
            continue

        if current and line.startswith("- "):
            current["bullets"].append(line[2:])

    if current:
        entries.append(current)
    return entries


def linkedin_location(location: str) -> str:
    city, sep, state = location.partition(", ")
    if sep and state in STATE_NAMES:
        return f"{city}, {STATE_NAMES[state]}, United States"
    return location


def linkedin_dates(dates: str) -> str:
    def expand(match: re.Match[str]) -> str:
        return f"{MONTHS.get(match.group(1), match.group(1))} {match.group(2)}"

    return re.sub(r"\b([A-Z][a-z]{2}) (\d{4})\b", expand, dates)


def generated_notice() -> str:
    return "<!-- Generated from profile.md by bin/gen-profile-artifacts.py. Do not edit facts here. -->"


def build_readme(meta: dict[str, str], body: str) -> str:
    name, _, location = name_and_contact(body)
    headline = meta["website_headline"]
    linkedin_url = meta["linkedin_url"]
    github_url = meta["github_url"]
    profile_body = body_from_summary(body)

    links = (
        '<a class="bi bi-envelope" href="mailto:amitava.shee@gmail.com"> Email</a> / '
        '<a class="bi bi-telephone" href="tel:+16463877200"> Phone</a> / '
        '<a class="bi bi-globe" href="{{site_url}}"> Website</a> / '
        f'<a class="bi bi-linkedin" href="{linkedin_url}"> LinkedIn</a> / '
        f'<a class="bi bi-github" href="{github_url}"> GitHub</a> / '
        '<a class="bi bi-file-earmark-pdf" href="{{site_url}}/Amitava Shee Resume.pdf"> Resume</a>'
    )

    return "\n\n".join(
        [
            generated_notice(),
            f"# {name}",
            f"_{headline}_",
            links,
            location,
            profile_body,
        ]
    ) + "\n"


def build_linkedin(meta: dict[str, str], body: str) -> str:
    sections = split_sections(body)
    experience = parse_experience(sections["Experience"])
    education = sections["Education"]
    certifications = sections["Certifications"]
    skills = [skill.strip() for skill in meta["linkedin_skills"].split(",")]

    lines: list[str] = [
        generated_notice(),
        "",
        "# LinkedIn Profile",
        "",
        "> Derived from `../profile.md`. That file is the canonical source of facts. Update canonical facts there first, then regenerate this document and update LinkedIn.",
        "",
        "## Headline",
        "",
        meta["linkedin_headline"],
        "",
        "## Location",
        "",
        meta["linkedin_location"],
        "",
        "## About",
        "",
        meta["linkedin_about"],
        "",
        "## Experience",
        "",
    ]

    for job in experience:
        lines.extend(
            [
                f"### {job['company']}",
                "",
                f"**Title:** {job['title']}  ",
                f"**Location:** {linkedin_location(str(job['location']))}  ",
                f"**Dates:** {linkedin_dates(str(job['dates']))}",
                "",
            ]
        )
        lines.extend(f"- {bullet}" for bullet in job["bullets"])
        lines.append("")

    lines.extend(["## Education", ""])
    for line in education.splitlines():
        if not line.strip():
            continue
        school, sep, degree = line.partition(" | ")
        lines.extend([f"### {school}", "", f"**Degree:** {degree if sep else line}", ""])

    lines.extend(["## Licenses and Certifications", ""])
    for line in certifications.splitlines():
        if not line.startswith("- "):
            continue
        name, _, issued = line[2:].partition(" | ")
        cert_name, license_sep, license_id = name.partition(", License: ")
        lines.extend([f"### {cert_name}", ""])
        if license_sep:
            lines.extend([f"**Credential ID:** {license_id}  "])
        lines.extend([f"**Issued:** {issued}", ""])

    lines.extend(["## Skills", "", "Suggested skills to prioritize, ordered by relevance to the current profile:", ""])
    lines.extend(f"{index}. {skill}" for index, skill in enumerate(skills, start=1))
    lines.append("")

    return "\n".join(lines)


def build_one_pager(meta: dict[str, str], body: str) -> str:
    name, contact, _ = name_and_contact(body)
    sections = split_sections(body)
    experience = parse_experience(sections["Experience"])
    recent_experience = experience[:3]
    earlier_experience = experience[3:]
    skills = [skill.strip() for skill in meta["linkedin_skills"].split(",")]

    earlier_companies = ", ".join(str(job["company"]) for job in earlier_experience)
    core_skills = " | ".join(skills[:14])

    lines: list[str] = [
        generated_notice(),
        "",
        f"# {name}",
        "",
        contact,
        "",
        "## Technology Executive | AI, Personalization, Search & Platform Engineering",
        "",
        "15+ years leading AI, ML, search, recommendation, cloud, and platform engineering teams across media, fintech, healthcare, education, and financial services. Built internet-scale personalization platforms, modernized search and MLOps systems, led engineering organizations, and delivered measurable cost, scale, and product impact.",
        "",
        "## Selected Impact",
        "",
        "- Launched a SiriusXM recommendation engine for 30M consumers on a new streaming platform in 13 months.",
        "- Reduced monthly cloud spend 68%, from $1.57M to $507K, without impacting system performance.",
        "- Led a 20-person engineering team operating ML platforms for online and batch inference processing over 1B records daily.",
        "- Built MLOps pipelines, advanced search ranking, A/B testing, and distributed search platforms on AWS EKS and Apache Solr.",
        "- Established enterprise architecture programs and healthcare research data platforms supporting national-scale initiatives.",
        "",
        "## Recent Leadership Experience",
        "",
    ]

    for job in recent_experience:
        lines.extend(
            [
                f"### {job['company']} | {job['title']}",
                "",
                f"{job['dates']} | {job['location']}",
                "",
            ]
        )

        bullets = list(job["bullets"])
        if job["company"] == "SiriusXM":
            selected_bullets = [bullets[0], bullets[1], bullets[2], bullets[4]]
        else:
            selected_bullets = bullets[:2]
        lines.extend(f"- {bullet}" for bullet in selected_bullets)
        lines.append("")

    lines.extend(
        [
            "## Earlier Experience Summary",
            "",
            f"Held architecture and engineering leadership roles at {earlier_companies}. Work included healthcare research platforms, enterprise architecture, cloud adoption, Epic selection, banking integrations, securities platforms, SSO, mainframe modernization, EDI, and C/C++ systems engineering.",
            "",
            "## Core Skills",
            "",
            core_skills,
            "",
            "## Education & Certifications",
            "",
            sections["Education"],
            "",
            "MOR Leaders Program | Scrum Alliance",
            "",
        ]
    )

    return "\n".join(lines)


def main() -> None:
    meta, body = read_profile()
    PUB.mkdir(exist_ok=True)
    README.write_text(build_readme(meta, body), encoding="utf-8")
    LINKEDIN.write_text(build_linkedin(meta, body), encoding="utf-8")
    ONE_PAGER.write_text(build_one_pager(meta, body), encoding="utf-8")
    (PUB / ".nojekyll").write_text("", encoding="utf-8")
    if CNAME.exists():
        (PUB / "CNAME").write_text(CNAME.read_text(encoding="utf-8"), encoding="utf-8")

    subprocess.run(
        [str(REPO_ROOT / "bin" / "gen-site.sh"), str(README), str(PUB / "index.html")],
        cwd=REPO_ROOT,
        check=True,
    )
    subprocess.run([str(REPO_ROOT / "bin" / "gen-pdf.sh"), str(PROFILE), str(RESUME_PDF)], cwd=REPO_ROOT, check=True)
    subprocess.run(
        [str(REPO_ROOT / "bin" / "gen-pdf.sh"), str(ONE_PAGER), str(ONE_PAGER_PDF)],
        cwd=REPO_ROOT,
        check=True,
    )


if __name__ == "__main__":
    main()

# AGENTS.md

## Repository purpose

This repository is the source of truth for Amitava Shee's professional profile, including the personal website, resume, and LinkedIn profile. GitHub Pages builds the site with Jekyll using `README.md` as the main page.

## Source of truth

- `Amitava Shee.md` contains the canonical professional-profile content and is the source of truth for the website, resume, and LinkedIn profile, including biography, employment history, accomplishments, skills, education, certifications, and contact details.
- `README.md`, `minimal-resume.md`, `ml-highlights.md`, and generated PDF files may contain older or abbreviated material. Do not use them to overwrite newer facts from `Amitava Shee.md`.
- When updating the published resume, adapt the current content from `Amitava Shee.md` to the existing presentation in `README.md` unless the task says otherwise.
- When preparing LinkedIn content, adapt `Amitava Shee.md` to LinkedIn's section structure and length constraints while preserving the canonical facts. Record factual LinkedIn updates in `Amitava Shee.md` first so the repository remains authoritative.
- Preserve names, dates, metrics, job titles, and contact details exactly unless the user explicitly requests a factual change. Do not invent or infer resume claims.

## Project structure

- `README.md`: GitHub Pages home page and web resume.
- `Amitava Shee.md`: canonical professional-profile content for all publishing channels.
- `linkedin/linkedin-profile.md`: copy-ready LinkedIn presentation derived from the canonical profile.
- `linkedin/update-checklist.md`: manual LinkedIn synchronization and verification workflow.
- `_config.yml`: Jekyll and GitHub Pages configuration.
- `_layouts/default.html`: custom page layout.
- `markdown.css`: print/PDF styling.
- `pdf/resume-header.tex`: compact Pandoc/XeLaTeX styling for the generated resume PDF.
- `bin/s.sh`: runs the local Jekyll development server.
- `bin/gen-pdf.sh`: generates `Amitava Shee Resume.pdf` from the canonical profile.
- `bin/ren-readme-pdf.sh`: legacy helper for manually exported `README.pdf` files.

## Working conventions

- Keep content in Markdown and follow the heading and list style already used in the target file.
- Treat files under `linkedin/` as derivative publishing artifacts. Resolve conflicts in favor of `Amitava Shee.md` and update canonical facts there first.
- Keep changes focused; avoid unrelated rewrites of resume language or site styling.
- Treat all professional-profile content as public-facing. Check spelling, Markdown rendering, date consistency, and punctuation before finishing.
- Never add private or sensitive information that is not already present in the user-designated source.
- Do not commit generated artifacts unless the task specifically requests them.

## Local verification

Install dependencies with `bundle install` when needed, then preview the site with:

```sh
bin/s.sh
```

For content-only changes, also review the Markdown diff and confirm that links and Liquid expressions such as `{{site_url}}` remain intact.

Generate the resume PDF from the repository root with:

```sh
bin/gen-pdf.sh
```

The build requires Pandoc and XeLaTeX and uses `Amitava Shee.md` as its default source. Review the page count, text extraction, and final visual layout after material content or style changes.

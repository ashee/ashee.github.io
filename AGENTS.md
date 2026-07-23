# AGENTS.md

## Repository purpose

This repository is the source of truth for Amitava Shee's professional profile, including the personal website, default resume, chronological resume, and LinkedIn profile. Generated publishing artifacts live under `pub/`; Jekyll is intentionally disabled with `.nojekyll`.

## Source of truth

- `profile.md` contains the canonical professional-profile content and is the source of truth for the website, resume, and LinkedIn profile, including biography, employment history, accomplishments, skills, education, certifications, and contact details.
- `Amitava Shee.md` is retained only as a compatibility pointer to `profile.md`.
- Files under `pub/`, including `pub/README.md`, `pub/index.html`, `pub/linkedin-profile.md`, generated Markdown resumes, copied CSS, and generated PDF files, are generated artifacts. Do not edit factual profile data there.
- `Amitava Shee.md`, `minimal-resume.md`, and `ml-highlights.md` are retained only as compatibility pointers to `profile.md`.
- When updating the published resume, chronological resume, website, or LinkedIn profile, update `profile.md` first and run `bin/gen-profile-artifacts.py`.
- Preserve names, dates, metrics, job titles, and contact details exactly unless the user explicitly requests a factual change. Do not invent or infer resume claims.

## Project structure

- `profile.md`: canonical professional-profile content for all publishing channels.
- `Amitava Shee.md`: compatibility pointer to `profile.md`.
- `minimal-resume.md`: compatibility pointer to `profile.md`.
- `ml-highlights.md`: compatibility pointer to `profile.md`.
- `pub/README.md`: generated Markdown source for the static site home page and web resume.
- `pub/index.html`: generated static site home page.
- `pub/linkedin-profile.md`: generated copy-ready LinkedIn presentation derived from the canonical profile.
- `pub/Amitava Shee Resume.md`: generated concise resume source derived from the canonical profile.
- `pub/Amitava Shee.pdf`: generated default concise resume PDF.
- `pub/Amitava Shee Chronological.pdf`: generated full chronological resume PDF.
- `pub/assets/site.css` and `pub/assets/markdown.css`: copied static assets for the generated site.
- `linkedin/update-checklist.md`: manual LinkedIn synchronization and verification workflow.
- `templates/site.html`: Pandoc HTML template for the static site.
- `assets/site.css`: screen styling for the static site.
- `assets/markdown.css`: print/PDF styling.
- `pdf/resume-header.tex`: compact Pandoc/XeLaTeX styling for the generated resume PDF.
- `bin/gen-profile-artifacts.py`: generates all files under `pub/` from `profile.md`.
- `bin/gen-site.sh`: low-level helper that generates `pub/index.html` from `pub/README.md` by default.
- `bin/s.sh`: generates the static site and serves it locally with Python's HTTP server.
- `bin/gen-pdf.sh`: generates `pub/Amitava Shee Chronological.pdf` from `profile.md` by default.
- `bin/ren-readme-pdf.sh`: legacy helper for manually exported `README.pdf` files.

## Working conventions

- Keep profile content in Markdown and follow the heading and list style already used in `profile.md`.
- Treat files under `pub/` as derivative publishing artifacts. Resolve conflicts in favor of `profile.md` and update canonical facts there first.
- Keep changes focused; avoid unrelated rewrites of resume language or site styling.
- Treat all professional-profile content as public-facing. Check spelling, Markdown rendering, date consistency, and punctuation before finishing.
- Never add private or sensitive information that is not already present in the user-designated source.
- Commit generated files under `pub/` after profile changes when publishing artifacts need to be updated. Do not commit generated PDFs unless the task specifically requests them.

## Local verification

Generate all profile artifacts with:

```sh
bin/gen-profile-artifacts.py
```

This updates `pub/README.md`, `pub/linkedin-profile.md`, `pub/index.html`, `pub/Amitava Shee Resume.md`, `pub/Amitava Shee.pdf`, and `pub/Amitava Shee Chronological.pdf` from `profile.md`.

Generate only the static site with:

```sh
bin/gen-site.sh
```

Preview the generated site with:

```sh
bin/s.sh
```

For content-only changes, review the Markdown diff, run `bin/gen-profile-artifacts.py`, and confirm that links are rendered correctly. `bin/gen-site.sh` replaces `{{site_url}}` placeholders at build time using `CNAME` or the `SITE_URL` environment variable.

Generate the resume PDF from the repository root with:

```sh
bin/gen-pdf.sh
```

The build requires Pandoc and XeLaTeX and uses `profile.md` as its default source, producing the chronological resume by default. Review the page count, text extraction, and final visual layout after material content or style changes.

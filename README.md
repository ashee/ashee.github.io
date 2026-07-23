# Operator Runbook

This repository publishes Amitava Shee's public professional profile: website, concise resume, chronological resume, and LinkedIn-ready profile copy.

## Golden rule

Edit factual profile content only in `profile.md`.

Files under `pub/` are generated publishing artifacts. Do not fix facts there by hand; update `profile.md`, regenerate, and review the generated diff.

## Local prerequisites

Install the tools used by the generators:

```sh
brew install pandoc
brew install --cask mactex-no-gui
```

Open a new shell after installing MacTeX so `xelatex` is on `PATH`.

Optional PDF validation uses `pdfinfo`, available from Poppler:

```sh
brew install poppler
```

## Common operating flows

### Update profile content

1. Edit `profile.md`.
2. Run:

   ```sh
   bin/gen-profile-artifacts.py
   ```

3. Review the source and generated diffs:

   ```sh
   git diff -- profile.md pub
   ```

4. Preview the site if layout or link behavior changed:

   ```sh
   bin/s.sh
   ```

   Open `http://localhost:4000`.

5. Commit `profile.md` and the generated artifacts under `pub/`.

### Update only presentation or styling

For site styling, edit `assets/site.css` or `assets/markdown.css`, then run:

```sh
bin/gen-profile-artifacts.py
```

For HTML structure, edit `templates/site.html`, then regenerate artifacts.

For PDF layout, edit `pdf/resume-header.tex`, then regenerate artifacts and inspect both generated PDFs.

### Generate only the website

Use this when `pub/README.md`, the site template, or site CSS changed and PDF output is not relevant:

```sh
bin/gen-site.sh
```

`bin/gen-site.sh` writes `pub/index.html` and copies CSS into `pub/assets/`.

### Generate only the chronological resume PDF

```sh
bin/gen-pdf.sh
```

By default this uses `profile.md` and writes `pub/Amitava Shee Chronological.pdf`.

## Local Git hook

This checkout has a local pre-commit hook at `.git/hooks/pre-commit`.

When staged inputs affect generated artifacts, the hook runs:

```sh
bin/gen-profile-artifacts.py
```

It does not stage generated files automatically. If regeneration changes files under `pub/`, the hook fails the commit and prints a diff summary. Review and stage the generated artifacts, then run `git commit` again.

The hook triggers for staged changes to:

- `profile.md`
- `CNAME`
- `assets/`
- `templates/`
- `pdf/`
- `bin/gen-profile-artifacts.py`
- `bin/gen-site.sh`
- `bin/gen-pdf.sh`

To bypass artifact generation for one commit:

```sh
SKIP_PROFILE_ARTIFACTS=1 git commit
```

Use the bypass only for commits that cannot affect generated output.

## Verification checklist

Before publishing material changes, check:

- `profile.md` remains the only source for factual changes.
- `pub/README.md`, `pub/index.html`, `pub/linkedin-profile.md`, `pub/Amitava Shee Resume.md`, and both PDFs were regenerated.
- Links in `pub/index.html` point at the expected site URL.
- `pub/Amitava Shee.pdf` is still a concise resume.
- `pub/Amitava Shee Chronological.pdf` renders correctly.
- No private or unapproved contact information was added.

For a full destructive regeneration and artifact presence check, run:

```sh
bin/validate-artifacts.sh
```

This deletes and rebuilds generated artifacts, so run it only when the worktree state is safe for that operation.

## LinkedIn updates

LinkedIn is not updated automatically. After regenerating artifacts, use:

```text
pub/linkedin-profile.md
```

Follow `linkedin/update-checklist.md` to apply and verify the manual LinkedIn update.

## Site URL

`bin/gen-site.sh` derives the public URL from `CNAME`. Override it for a one-off build with:

```sh
SITE_URL=https://example.com bin/gen-site.sh
```

## Troubleshooting

If `pandoc` is missing, install it with Homebrew and rerun generation.

If `xelatex` is missing after installing MacTeX, open a new shell and check:

```sh
command -v xelatex
```

If generated artifacts look stale, rerun `bin/gen-profile-artifacts.py` from the repository root and review `git diff -- pub`.

If the local hook is not running, confirm it is executable:

```sh
ls -l .git/hooks/pre-commit
```

The mode should include `x`.

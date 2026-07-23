#!/usr/bin/env bash

set -euo pipefail

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repo_root=$(CDPATH= cd -- "$script_dir/.." && pwd)
pub_dir="$repo_root/pub"

legacy_artifacts=(
  "$repo_root/README.md"
  "$repo_root/index.html"
  "$repo_root/Amitava Shee Resume.pdf"
  "$repo_root/linkedin/linkedin-profile.md"
)

expected_artifacts=(
  "$pub_dir/README.md"
  "$pub_dir/index.html"
  "$pub_dir/linkedin-profile.md"
  "$pub_dir/Amitava Shee 1 Pager.md"
  "$pub_dir/Amitava Shee 1 Pager.pdf"
  "$pub_dir/Amitava Shee Resume.pdf"
  "$pub_dir/assets/site.css"
  "$pub_dir/assets/markdown.css"
)

pdf_pages() {
  pdfinfo "$1" | awk -F: '/^Pages:/ { gsub(/^[[:space:]]+/, "", $2); print $2 }'
}

echo "Deleting derived artifacts"
rm -rf "$pub_dir"
for artifact in "${legacy_artifacts[@]}"; do
  rm -f "$artifact"
done

echo "Regenerating artifacts"
"$script_dir/gen-profile-artifacts.py"

echo "Validating expected outputs"
for artifact in "${expected_artifacts[@]}"; do
  if [ ! -f "$artifact" ]; then
    echo "error: missing generated artifact: $artifact" >&2
    exit 1
  fi
done

if ! grep -q 'href="assets/site.css"' "$pub_dir/index.html"; then
  echo "error: pub/index.html does not reference assets/site.css" >&2
  exit 1
fi

if ! grep -q 'href="assets/markdown.css"' "$pub_dir/index.html"; then
  echo "error: pub/index.html does not reference assets/markdown.css" >&2
  exit 1
fi

if command -v pdfinfo >/dev/null 2>&1; then
  one_pager_pages=$(pdf_pages "$pub_dir/Amitava Shee 1 Pager.pdf")
  resume_pages=$(pdf_pages "$pub_dir/Amitava Shee Resume.pdf")

  if [ "$one_pager_pages" != "1" ]; then
    echo "error: expected one-page resume PDF to be 1 page, got $one_pager_pages" >&2
    exit 1
  fi

  if [ "$resume_pages" -lt 1 ]; then
    echo "error: expected resume PDF to have at least 1 page, got $resume_pages" >&2
    exit 1
  fi
else
  echo "warning: pdfinfo not found; skipped PDF page-count validation" >&2
fi

echo "Artifact validation passed"

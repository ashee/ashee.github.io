#!/bin/sh

set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repo_root=$(CDPATH= cd -- "$script_dir/.." && pwd)

source_file=${1:-"$repo_root/profile.md"}
output_file=${2:-"$repo_root/Amitava Shee Resume.pdf"}
style_file="$repo_root/pdf/resume-header.tex"

if ! command -v pandoc >/dev/null 2>&1; then
    echo "error: pandoc is required to generate the resume PDF" >&2
    echo "install it with: brew install pandoc" >&2
    exit 1
fi

if ! command -v xelatex >/dev/null 2>&1; then
    echo "error: xelatex is required to generate the resume PDF" >&2
    echo "install a TeX distribution such as MacTeX: brew install --cask mactex-no-gui" >&2
    exit 1
fi

if [ ! -f "$source_file" ]; then
    echo "error: resume source not found: $source_file" >&2
    exit 1
fi

if [ ! -f "$style_file" ]; then
    echo "error: PDF style file not found: $style_file" >&2
    exit 1
fi

output_dir=$(dirname -- "$output_file")
if [ ! -d "$output_dir" ]; then
    echo "error: output directory not found: $output_dir" >&2
    exit 1
fi

build_dir=$(mktemp -d "${TMPDIR:-/tmp}/amitava-resume.XXXXXX")
trap 'rm -rf "$build_dir"' EXIT HUP INT TERM

pandoc "$source_file" \
    --from=gfm \
    --standalone \
    --pdf-engine=xelatex \
    --include-in-header="$style_file" \
    --variable=papersize:letter \
    --variable=geometry:top=0.45in,bottom=0.45in,left=0.55in,right=0.55in \
    --variable=colorlinks:true \
    --variable=linkcolor:MidnightBlue \
    --variable=urlcolor:MidnightBlue \
    --metadata=title-meta:"Amitava Shee Resume" \
    --output="$build_dir/resume.pdf"

mv "$build_dir/resume.pdf" "$output_file"
echo "Generated $output_file"

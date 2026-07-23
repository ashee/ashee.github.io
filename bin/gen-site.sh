#!/usr/bin/env bash

set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repo_root=$(CDPATH= cd -- "$script_dir/.." && pwd)

source_file=${1:-"$repo_root/pub/README.md"}
output_file=${2:-"$repo_root/pub/index.html"}
template_file="$repo_root/templates/site.html"
site_url=${SITE_URL:-}

if ! command -v pandoc >/dev/null 2>&1; then
    echo "error: pandoc is required to generate the static site" >&2
    echo "install it with: brew install pandoc" >&2
    exit 1
fi

if [ ! -f "$source_file" ]; then
    echo "error: site source not found: $source_file" >&2
    exit 1
fi

if [ ! -f "$template_file" ]; then
    echo "error: site template not found: $template_file" >&2
    exit 1
fi

if [ -z "$site_url" ]; then
    if [ -f "$repo_root/CNAME" ]; then
        site_url="https://$(sed -n '1p' "$repo_root/CNAME")"
    else
        site_url="https://ashee.github.io"
    fi
fi

build_dir=$(mktemp -d "${TMPDIR:-/tmp}/amitava-site.XXXXXX")
trap 'rm -rf "$build_dir"' EXIT HUP INT TERM

output_dir=$(dirname -- "$output_file")
mkdir -p "$output_dir"
asset_dir="$output_dir/assets"
mkdir -p "$asset_dir"

sed "s|{{site_url}}|$site_url|g" "$source_file" > "$build_dir/source.md"

pandoc "$build_dir/source.md" \
    --from=gfm+raw_html \
    --to=html5 \
    --standalone \
    --template="$template_file" \
    --metadata=title:"Amitava Shee" \
    --metadata=description:"Consultant - AI, Personalization, and Platform Engineering" \
    --metadata=site_url:"$site_url" \
    --output="$output_file"

cp "$repo_root/assets/site.css" "$asset_dir/site.css"
cp "$repo_root/assets/markdown.css" "$asset_dir/markdown.css"

echo "Generated $output_file"

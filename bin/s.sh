#!/usr/bin/env bash

set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repo_root=$(CDPATH= cd -- "$script_dir/.." && pwd)
port=${PORT:-4000}

"$script_dir/gen-profile-artifacts.py"

cd "$repo_root"
python3 -m http.server "$port"

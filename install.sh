#!/bin/bash
# Link gitfeed into SwiftBar (menu bar) and Übersicht (desktop). Safe to re-run.
# Assumes both apps are installed and have been opened once.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"

swiftbar_dir="$(defaults read com.ameba.SwiftBar PluginDirectory 2>/dev/null || true)"
if [ -n "$swiftbar_dir" ]; then
  ln -sfn "$here/swiftbar/gitfeed.1m.py" "$swiftbar_dir/gitfeed.1m.py"
  echo "menu bar: linked into $swiftbar_dir"
else
  echo "menu bar: open SwiftBar once and choose a plugin folder, then re-run this script"
fi

uebersicht_dir="$HOME/Library/Application Support/Übersicht/widgets"
if [ -d "$uebersicht_dir" ]; then
  ln -sfn "$here/ubersicht/gitfeed.widget" "$uebersicht_dir/gitfeed.widget"
  echo "desktop: linked into $uebersicht_dir"
else
  echo "desktop: open Übersicht once so it creates its widgets folder, then re-run this script"
fi

#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Exit Presentation Mode
# @raycast.mode fullOutput

# Optional parameters:
# @raycast.icon 🖥️
# @raycast.packageName Presentation Mode

# Documentation:
# @raycast.description Show menu bar, restore resolution, and tile windows
# @raycast.author thatgardnerone
# @raycast.authorURL https://github.com/thatgardnerone

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Use the Poetry venv directly (more reliable than relying on PATH)
"$SCRIPT_DIR/.venv/bin/python" -m presentation_mode.cli exit

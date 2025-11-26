#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Enter Presentation Mode
# @raycast.mode fullOutput

# Optional parameters:
# @raycast.icon 🎬
# @raycast.packageName Presentation Mode

# Documentation:
# @raycast.description Hide menu bar, lower resolution, and tile windows for screen sharing
# @raycast.author thatgardnerone
# @raycast.authorURL https://github.com/thatgardnerone

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Use the Poetry venv directly (more reliable than relying on PATH)
"$SCRIPT_DIR/.venv/bin/python" -m presentation_mode.cli enter

"""Configuration for presentation mode."""

import shutil

# Display configuration - auto-detect displayplacer location
DISPLAYPLACER_PATH = shutil.which("displayplacer") or "/opt/homebrew/bin/displayplacer"

# Target presentation width (will find closest available scaled mode)
# 1280 is ideal for crisp 720p-like screen sharing
PRESENTATION_TARGET_WIDTH = 1280

# Normal/exit resolution (external display default)
NORMAL_WIDTH = 2560
NORMAL_HEIGHT = 1440

# Window padding (macOS Tahoe Liquid Glass style)
PADDING_TOP = 12
PADDING_BOTTOM = 12
PADDING_HORIZONTAL = 12

# Timing
RESOLUTION_CHANGE_DELAY = 2.0  # seconds to wait after resolution change

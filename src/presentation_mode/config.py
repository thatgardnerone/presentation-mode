"""Configuration for presentation mode."""

# Display configuration
DISPLAYPLACER_PATH = "/opt/homebrew/bin/displayplacer"

# Known displays with their resolution profiles
DISPLAYS = {
    # MacBook Pro built-in Retina display
    "s4251086178": {
        "name": "Retina",
        "presentation": (1280, 800),   # Closest to 720p available
        "normal": (1728, 1117),        # Native resolution
    },
    # ProArt 5K external monitor
    "s536870912": {
        "name": "ProArt External",
        "presentation": (1280, 720),
        "normal": (2560, 1440),
    },
}

# Window padding (macOS Tahoe Liquid Glass style)
PADDING_TOP = 12
PADDING_BOTTOM = 12
PADDING_HORIZONTAL = 12

# Timing
RESOLUTION_CHANGE_DELAY = 2.0  # seconds to wait after resolution change

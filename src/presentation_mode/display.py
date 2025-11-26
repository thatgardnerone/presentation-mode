"""Display management using displayplacer."""

import subprocess
import re
from .config import (
    DISPLAYPLACER_PATH,
    DISPLAYS,
)


def get_display_info() -> str:
    """Get current display configuration from displayplacer."""
    result = subprocess.run(
        [DISPLAYPLACER_PATH, "list"],
        capture_output=True,
        text=True,
    )
    return result.stdout


def get_main_display_serial() -> str | None:
    """Detect the main display's serial ID from displayplacer.

    Returns:
        Serial ID string (e.g., 's4251086178') or None if not found
    """
    info = get_display_info()

    # Look for the display marked as "main display"
    current_serial = None
    for line in info.split('\n'):
        if "Serial screen id:" in line:
            # Extract serial like "s4251086178"
            match = re.search(r'Serial screen id: (s\d+)', line)
            if match:
                current_serial = match.group(1)
        elif "main display" in line.lower() and current_serial:
            return current_serial

    return None


def get_display_config() -> dict | None:
    """Get configuration for the current main display.

    Returns:
        Display config dict with 'name', 'presentation', 'normal' keys,
        or None if display not recognized
    """
    serial = get_main_display_serial()
    if serial and serial in DISPLAYS:
        config = DISPLAYS[serial].copy()
        config['serial'] = serial
        return config

    # Unknown display - try to auto-detect reasonable defaults
    if serial:
        print(f"Unknown display: {serial}")
        # Return a generic config
        return {
            'serial': serial,
            'name': 'Unknown',
            'presentation': (1280, 720),
            'normal': (1920, 1080),
        }

    return None


def find_mode_id(
    serial: str,
    width: int,
    height: int,
    scaled: bool = True,
) -> str | None:
    """Find the mode ID for a given resolution on a display.

    Args:
        serial: Display serial ID
        width: Target width
        height: Target height
        scaled: If True, look for scaled mode (HiDPI)

    Returns:
        Mode ID string or None if not found
    """
    info = get_display_info()

    # Find the section for our display
    in_target_display = False
    for line in info.split('\n'):
        if serial in line:
            in_target_display = True
            continue

        if in_target_display:
            # Check if we've moved to a different display section
            if line.startswith("Persistent screen id:"):
                break

            # Look for mode line matching our resolution
            # Format: "  mode 42: res:1280x720 hz:60 color_depth:8 scaling:on"
            if f"res:{width}x{height}" in line:
                # For scaled modes, prefer scaling:on
                # For non-scaled, accept lines without scaling:on or with scaling:off
                if scaled:
                    if "scaling:on" in line:
                        match = re.search(r'mode (\d+):', line)
                        if match:
                            return match.group(1)
                else:
                    if "scaling:on" not in line:
                        match = re.search(r'mode (\d+):', line)
                        if match:
                            return match.group(1)

    return None


def set_resolution(width: int, height: int, scaled: bool = True) -> bool:
    """Set the main display to specified resolution.

    Args:
        width: Target width
        height: Target height
        scaled: If True, use scaled (HiDPI) mode

    Returns:
        True if successful, False otherwise
    """
    config = get_display_config()
    if not config:
        print("Could not detect main display")
        return False

    serial = config['serial']
    mode_id = find_mode_id(serial, width, height, scaled)

    if not mode_id:
        print(f"Could not find mode for {width}x{height} (scaled={scaled}) on {config['name']}")
        return False

    # Build displayplacer command
    display_arg = f"id:{serial} mode:{mode_id}"

    result = subprocess.run(
        [DISPLAYPLACER_PATH, display_arg],
        capture_output=True,
        text=True,
    )

    return result.returncode == 0


def set_presentation_resolution() -> bool:
    """Set display to presentation mode resolution."""
    config = get_display_config()
    if not config:
        print("Could not detect main display")
        return False

    width, height = config['presentation']
    print(f"   Using {config['name']} display: {width}x{height}")
    return set_resolution(width, height, scaled=True)


def set_normal_resolution() -> bool:
    """Set display to normal resolution."""
    config = get_display_config()
    if not config:
        print("Could not detect main display")
        return False

    width, height = config['normal']
    print(f"   Using {config['name']} display: {width}x{height}")
    return set_resolution(width, height, scaled=True)


def get_main_display_bounds() -> tuple[int, int, int, int]:
    """Get the usable bounds of the main display (excluding menu bar/dock).

    Returns:
        Tuple of (x, y, width, height) for the main display's visible area
    """
    import Cocoa

    screen = Cocoa.NSScreen.mainScreen()
    if not screen:
        # Fallback to full display bounds
        from Quartz import CGMainDisplayID, CGDisplayBounds
        main_display = CGMainDisplayID()
        bounds = CGDisplayBounds(main_display)
        return (
            int(bounds.origin.x),
            int(bounds.origin.y),
            int(bounds.size.width),
            int(bounds.size.height),
        )

    # visibleFrame excludes menu bar and dock
    visible = screen.visibleFrame()
    full = screen.frame()

    # NSScreen uses bottom-left origin, convert to top-left for window positioning
    # The y offset from top is: full_height - (visible_y + visible_height)
    top_y = full.size.height - (visible.origin.y + visible.size.height)

    return (
        int(visible.origin.x),
        int(top_y),
        int(visible.size.width),
        int(visible.size.height),
    )

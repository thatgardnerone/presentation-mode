"""Display management using displayplacer."""

import subprocess
import re
from .config import (
    DISPLAYPLACER_PATH,
    PRESENTATION_TARGET_WIDTH,
    NORMAL_WIDTH,
    NORMAL_HEIGHT,
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
            match = re.search(r'Serial screen id: (s\d+)', line)
            if match:
                current_serial = match.group(1)
        elif "main display" in line.lower() and current_serial:
            return current_serial

    return None


def get_available_modes(serial: str) -> list[dict]:
    """Get all available display modes for a display.

    Args:
        serial: Display serial ID

    Returns:
        List of mode dicts with 'id', 'width', 'height', 'hz', 'scaled' keys
    """
    info = get_display_info()
    modes = []

    in_target_display = False
    for line in info.split('\n'):
        if serial in line:
            in_target_display = True
            continue

        if in_target_display:
            if line.startswith("Persistent screen id:"):
                break

            # Parse mode line: "  mode 42: res:1280x720 hz:60 color_depth:8 scaling:on"
            match = re.search(r'mode (\d+): res:(\d+)x(\d+) hz:(\d+)', line)
            if match:
                modes.append({
                    'id': match.group(1),
                    'width': int(match.group(2)),
                    'height': int(match.group(3)),
                    'hz': int(match.group(4)),
                    'scaled': 'scaling:on' in line,
                })

    return modes


def get_current_resolution(serial: str) -> tuple[int, int] | None:
    """Get the current resolution for a display.

    Args:
        serial: Display serial ID

    Returns:
        Tuple of (width, height) or None if not found
    """
    info = get_display_info()

    in_target_display = False
    for line in info.split('\n'):
        if serial in line:
            in_target_display = True
            continue

        if in_target_display:
            if line.startswith("Persistent screen id:"):
                break

            # Look for "Resolution: 1728x1117"
            match = re.search(r'Resolution: (\d+)x(\d+)', line)
            if match:
                return (int(match.group(1)), int(match.group(2)))

    return None


def find_presentation_mode(serial: str) -> dict | None:
    """Find the best presentation mode for a display.

    Looks for a scaled mode with width closest to PRESENTATION_TARGET_WIDTH.

    Args:
        serial: Display serial ID

    Returns:
        Mode dict or None if not found
    """
    modes = get_available_modes(serial)

    # Filter to scaled modes only (for crisp text)
    scaled_modes = [m for m in modes if m['scaled']]

    if not scaled_modes:
        return None

    # Find mode closest to target width
    target = PRESENTATION_TARGET_WIDTH
    best = min(scaled_modes, key=lambda m: abs(m['width'] - target))

    return best


def find_mode_for_resolution(serial: str, width: int, height: int) -> dict | None:
    """Find a scaled mode matching the given resolution.

    Args:
        serial: Display serial ID
        width: Target width
        height: Target height

    Returns:
        Mode dict or None if not found
    """
    modes = get_available_modes(serial)

    for mode in modes:
        if mode['width'] == width and mode['height'] == height and mode['scaled']:
            return mode

    return None


def set_mode(serial: str, mode_id: str) -> bool:
    """Set display to a specific mode.

    Args:
        serial: Display serial ID
        mode_id: Mode ID to set

    Returns:
        True if successful, False otherwise
    """
    display_arg = f"id:{serial} mode:{mode_id}"

    result = subprocess.run(
        [DISPLAYPLACER_PATH, display_arg],
        capture_output=True,
        text=True,
    )

    return result.returncode == 0


def set_presentation_resolution() -> bool:
    """Set display to presentation mode resolution.

    Automatically finds the best presentation resolution for the main display.

    Returns:
        True if successful, False otherwise
    """
    serial = get_main_display_serial()
    if not serial:
        print("Could not detect main display")
        return False

    mode = find_presentation_mode(serial)
    if not mode:
        print("Could not find suitable presentation mode")
        return False

    print(f"   Setting {mode['width']}x{mode['height']} (mode {mode['id']})")
    return set_mode(serial, mode['id'])


def set_normal_resolution() -> bool:
    """Set display to normal resolution (2560x1440).

    Returns:
        True if successful, False otherwise
    """
    serial = get_main_display_serial()
    if not serial:
        print("Could not detect main display")
        return False

    mode = find_mode_for_resolution(serial, NORMAL_WIDTH, NORMAL_HEIGHT)
    if not mode:
        print(f"Could not find {NORMAL_WIDTH}x{NORMAL_HEIGHT} mode")
        return False

    print(f"   Setting {mode['width']}x{mode['height']} (mode {mode['id']})")
    return set_mode(serial, mode['id'])


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

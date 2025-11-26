"""Window management using Quartz and Accessibility APIs."""

import time
from Quartz import (
    CGWindowListCopyWindowInfo,
    kCGWindowListOptionOnScreenOnly,
    kCGNullWindowID,
    kCGWindowLayer,
    kCGWindowOwnerName,
    kCGWindowBounds,
    kCGWindowOwnerPID,
    kCGWindowNumber,
)
from ApplicationServices import (
    AXUIElementCreateApplication,
    AXUIElementCopyAttributeValue,
    AXUIElementSetAttributeValue,
    AXValueCreate,
    kAXValueTypeCGPoint,
    kAXValueTypeCGSize,
    kAXErrorSuccess,
)
from CoreFoundation import CFEqual
import Cocoa

from .config import (
    PADDING_TOP,
    PADDING_BOTTOM,
    PADDING_HORIZONTAL,
)


# Apps to skip when resizing windows
SKIP_APPS = {
    "Dock",
    "Window Server",
    "WindowManager",
    "Control Center",
    "Notification Center",
    "Spotlight",
    "SystemUIServer",
    "Finder",  # Desktop windows
    "universalAccessAuthWarn",
    "AXVisualSupportAgent",
    "TextInputMenuAgent",
    "Raycast",
}


def get_windows_on_display(
    display_x: int,
    display_y: int,
    display_width: int,
    display_height: int,
) -> list[dict]:
    """Get all resizable windows on the specified display.

    Args:
        display_x: Left edge of display
        display_y: Top edge of display
        display_width: Width of display
        display_height: Height of display

    Returns:
        List of window dictionaries with app_name, pid, window_id, bounds
    """
    windows = []
    display_max_x = display_x + display_width

    window_list = CGWindowListCopyWindowInfo(
        kCGWindowListOptionOnScreenOnly,
        kCGNullWindowID,
    )

    if not window_list:
        return windows

    for window in window_list:
        # Skip non-normal layer windows (menu bar, dock, etc.)
        layer = window.get(kCGWindowLayer, 0)
        if layer != 0:
            continue

        app_name = window.get(kCGWindowOwnerName, "")
        if app_name in SKIP_APPS:
            continue

        bounds = window.get(kCGWindowBounds)
        if not bounds:
            continue

        window_x = bounds.get("X", 0)
        window_width = bounds.get("Width", 0)

        # Check if window is on our target display
        window_center_x = window_x + window_width / 2
        if window_center_x < display_x or window_center_x >= display_max_x:
            continue

        # Skip tiny windows (likely system elements)
        if bounds.get("Width", 0) < 100 or bounds.get("Height", 0) < 100:
            continue

        windows.append({
            "app_name": app_name,
            "pid": window.get(kCGWindowOwnerPID),
            "window_id": window.get(kCGWindowNumber),
            "bounds": bounds,
        })

    return windows


def resize_window_ax(
    pid: int,
    target_x: int,
    target_y: int,
    target_width: int,
    target_height: int,
) -> bool:
    """Resize a window using the Accessibility API.

    Args:
        pid: Process ID of the application
        target_x: New x position
        target_y: New y position
        target_width: New width
        target_height: New height

    Returns:
        True if successful, False otherwise
    """
    app = AXUIElementCreateApplication(pid)

    # Get all windows for this app
    err, windows = AXUIElementCopyAttributeValue(app, "AXWindows", None)
    if err != kAXErrorSuccess or not windows:
        return False

    # Resize the first (frontmost) window
    if len(windows) == 0:
        return False

    window = windows[0]

    # Create CGPoint for position
    position = Cocoa.NSMakePoint(target_x, target_y)
    position_value = AXValueCreate(kAXValueTypeCGPoint, position)
    if position_value:
        AXUIElementSetAttributeValue(window, "AXPosition", position_value)

    # Create CGSize for size
    size = Cocoa.NSMakeSize(target_width, target_height)
    size_value = AXValueCreate(kAXValueTypeCGSize, size)
    if size_value:
        AXUIElementSetAttributeValue(window, "AXSize", size_value)

    return True


def resize_all_app_windows_ax(
    pid: int,
    target_x: int,
    target_y: int,
    target_width: int,
    target_height: int,
) -> int:
    """Resize all windows of an application using the Accessibility API.

    Args:
        pid: Process ID of the application
        target_x: New x position
        target_y: New y position
        target_width: New width
        target_height: New height

    Returns:
        Number of windows resized
    """
    app = AXUIElementCreateApplication(pid)

    # Get all windows for this app
    err, windows = AXUIElementCopyAttributeValue(app, "AXWindows", None)
    if err != kAXErrorSuccess or not windows:
        return 0

    count = 0
    for window in windows:
        # Create CGPoint for position
        position = Cocoa.NSMakePoint(target_x, target_y)
        position_value = AXValueCreate(kAXValueTypeCGPoint, position)
        if position_value:
            AXUIElementSetAttributeValue(window, "AXPosition", position_value)

        # Create CGSize for size
        size = Cocoa.NSMakeSize(target_width, target_height)
        size_value = AXValueCreate(kAXValueTypeCGSize, size)
        if size_value:
            AXUIElementSetAttributeValue(window, "AXSize", size_value)

        count += 1

    return count


def tile_windows_on_display(
    display_x: int,
    display_y: int,
    display_width: int,
    display_height: int,
) -> int:
    """Resize all windows on display to fill it with padding.

    Args:
        display_x: Left edge of display
        display_y: Top edge of display
        display_width: Width of display
        display_height: Height of display

    Returns:
        Number of windows resized
    """
    # Calculate target window bounds with padding
    target_x = display_x + PADDING_HORIZONTAL
    target_y = display_y + PADDING_TOP
    target_width = display_width - (2 * PADDING_HORIZONTAL)
    target_height = display_height - PADDING_TOP - PADDING_BOTTOM

    # Get windows on this display
    windows = get_windows_on_display(
        display_x, display_y, display_width, display_height
    )

    # Group windows by PID (so we only process each app once)
    pids_processed = set()
    resized_count = 0

    for window in windows:
        pid = window["pid"]
        if pid in pids_processed:
            continue

        pids_processed.add(pid)
        count = resize_all_app_windows_ax(
            pid, target_x, target_y, target_width, target_height
        )
        if count > 0:
            print(f"  Resized {count} window(s) for {window['app_name']}")
            resized_count += count

    return resized_count

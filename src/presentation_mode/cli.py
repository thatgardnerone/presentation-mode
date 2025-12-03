"""CLI entry points for presentation mode."""

import sys
import time

from .config import RESOLUTION_CHANGE_DELAY
from .display import (
    set_presentation_resolution,
    set_normal_resolution,
    get_main_display_bounds,
)
from .menubar import hide_menubar, show_menubar
from .windows import tile_windows_on_display


def enter() -> int:
    """Enter presentation mode.

    1. Hide the menu bar
    2. Set display to presentation resolution
    3. Wait for resolution change to settle
    4. Resize all windows to fill display with padding

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    print("Entering presentation mode...")
    start_time = time.time()

    # Step 1: Hide menu bar
    print("1. Hiding menu bar...")
    if not hide_menubar():
        print("   Warning: Failed to hide menu bar")

    # Step 2: Set presentation resolution
    print("2. Setting presentation resolution...")
    if not set_presentation_resolution():
        print("   Error: Failed to set presentation resolution")
        return 1

    # Step 3: Wait for resolution change to settle
    print(f"3. Waiting {RESOLUTION_CHANGE_DELAY}s for resolution change...")
    time.sleep(RESOLUTION_CHANGE_DELAY)

    # Step 4: Get new display bounds and resize windows
    print("4. Resizing windows...")
    x, y, width, height = get_main_display_bounds()
    print(f"   Display bounds: {width}x{height} at ({x}, {y})")

    count = tile_windows_on_display(x, y, width, height)
    print(f"   Resized {count} window(s)")

    elapsed = time.time() - start_time
    print(f"Done in {elapsed:.2f}s")
    return 0


def exit_mode() -> int:
    """Exit presentation mode.

    1. Show the menu bar
    2. Set display to 2560x1440
    3. Wait for resolution change to settle
    4. Resize all windows to fill display with padding

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    print("Exiting presentation mode...")
    start_time = time.time()

    # Step 1: Show menu bar
    print("1. Showing menu bar...")
    if not show_menubar():
        print("   Warning: Failed to show menu bar")

    # Step 2: Set normal resolution (2560x1440)
    print("2. Setting resolution to 2560x1440...")
    if not set_normal_resolution():
        print("   Error: Failed to set resolution")
        return 1

    # Step 3: Wait for resolution change to settle
    print(f"3. Waiting {RESOLUTION_CHANGE_DELAY}s for resolution change...")
    time.sleep(RESOLUTION_CHANGE_DELAY)

    # Step 4: Get new display bounds and resize windows
    print("4. Resizing windows...")
    x, y, width, height = get_main_display_bounds()
    print(f"   Display bounds: {width}x{height} at ({x}, {y})")

    count = tile_windows_on_display(x, y, width, height)
    print(f"   Resized {count} window(s)")

    elapsed = time.time() - start_time
    print(f"Done in {elapsed:.2f}s")
    return 0


def main():
    """Main entry point for testing."""
    if len(sys.argv) < 2:
        print("Usage: python -m presentation_mode.cli [enter|exit]")
        return 1

    command = sys.argv[1]
    if command == "enter":
        return enter()
    elif command == "exit":
        return exit_mode()
    else:
        print(f"Unknown command: {command}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

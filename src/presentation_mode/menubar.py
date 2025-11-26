"""Menu bar visibility control."""

import subprocess


def set_menubar_autohide(autohide: bool) -> bool:
    """Set the menu bar auto-hide behavior.

    Args:
        autohide: True to auto-hide, False to always show

    Returns:
        True if successful, False otherwise
    """
    value = "true" if autohide else "false"

    result = subprocess.run(
        ["osascript", "-e", f'''
            tell application "System Events"
                tell dock preferences
                    set autohide menu bar to {value}
                end tell
            end tell
        '''],
        capture_output=True,
        text=True,
    )

    return result.returncode == 0


def hide_menubar() -> bool:
    """Hide the menu bar (set to auto-hide)."""
    return set_menubar_autohide(True)


def show_menubar() -> bool:
    """Show the menu bar (disable auto-hide)."""
    return set_menubar_autohide(False)

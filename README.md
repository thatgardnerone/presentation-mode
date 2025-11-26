# Presentation Mode

A macOS tool to quickly switch your display to a lower resolution for crisp screen sharing, with automatic window tiling.

Perfect for YouTube, Google Meet, Zoom, or any screen sharing where viewers benefit from a cleaner, lower-resolution view.

## Features

- **Auto-detects your display** - works with any Mac display (built-in Retina, external monitors)
- **Smart resolution switching** - finds the best ~1280px presentation resolution for your display
- **Automatic window tiling** - resizes all windows to fill the screen with macOS-style padding
- **Menu bar management** - hides menu bar in presentation mode for maximum space
- **State preservation** - remembers and restores your original resolution on exit
- **Raycast integration** - includes script commands for quick access

## Prerequisites

### Required

1. **Python 3.11+** (3.14 recommended)
   ```bash
   # Check your version
   python3 --version

   # Install via pyenv if needed
   brew install pyenv
   pyenv install 3.14.0
   ```

2. **displayplacer** - for display resolution switching
   ```bash
   brew install displayplacer
   ```

3. **Poetry** - for Python dependency management
   ```bash
   brew install poetry
   ```

### Accessibility Permissions

The tool requires Accessibility permissions to resize windows.

1. Open **System Settings** → **Privacy & Security** → **Accessibility**
2. Click the **lock icon** and enter your password
3. Add your terminal app (Terminal, iTerm2, etc.) or **Raycast**
4. Ensure the checkbox is **enabled**
5. **Restart the app** after granting permissions

## Installation

```bash
# Clone the repository
git clone https://github.com/thatgardnerone/presentation-mode.git
cd presentation-mode

# Install dependencies
poetry install
```

## Usage

### Command Line

```bash
# Enter presentation mode
poetry run enter-presentation-mode

# Exit presentation mode
poetry run exit-presentation-mode
```

### Raycast

1. Add the `presentation-mode` folder to Raycast's Script Commands directories
2. Search for "Enter Presentation Mode" or "Exit Presentation Mode"
3. Optionally assign keyboard shortcuts

### Direct Script Execution

```bash
./enter-presentation-mode.sh
./exit-presentation-mode.sh
```

## What It Does

### Enter Presentation Mode

1. **Hides the menu bar** for maximum screen space
2. **Saves your current resolution** for later restoration
3. **Switches to ~1280px width** - finds the closest scaled mode to 1280px
4. **Tiles all windows** with 12px padding (macOS Tahoe style)

### Exit Presentation Mode

1. **Shows the menu bar**
2. **Restores your original resolution**
3. **Re-tiles all windows** to fit the restored resolution

## Configuration

Edit `src/presentation_mode/config.py` to customize:

```python
# Target width for presentation mode (finds closest available)
PRESENTATION_TARGET_WIDTH = 1280

# Window padding (macOS Tahoe Liquid Glass style)
PADDING_TOP = 12
PADDING_BOTTOM = 12
PADDING_HORIZONTAL = 12

# Delay after resolution change (seconds)
RESOLUTION_CHANGE_DELAY = 2.0
```

## How It Works

- Uses **displayplacer** to enumerate available display modes and switch resolutions
- Uses **PyObjC** (Quartz/Cocoa frameworks) to:
  - Detect the main display
  - Get the visible screen area (excluding menu bar/dock)
  - Enumerate windows via `CGWindowListCopyWindowInfo`
  - Resize windows via the Accessibility API (`AXUIElement`)
- Saves state to `~/.presentation-mode-state.json`

## Troubleshooting

### "Could not find suitable presentation mode"

Your display may not have a ~1280px scaled mode. Check available modes:
```bash
displayplacer list
```

### Windows not resizing

1. Ensure Accessibility permissions are granted (see Prerequisites)
2. Try toggling the permission off and on, then restart the app
3. Some apps (like Finder desktop) intentionally cannot be resized

### Wrong resolution on exit

The tool saves your resolution before entering presentation mode. If the state file is corrupted:
```bash
rm ~/.presentation-mode-state.json
```
Then manually set your preferred resolution in System Settings.

## Project Structure

```
presentation-mode/
├── pyproject.toml              # Poetry configuration
├── enter-presentation-mode.sh  # Raycast wrapper
├── exit-presentation-mode.sh   # Raycast wrapper
└── src/presentation_mode/
    ├── __init__.py
    ├── cli.py                  # CLI entry points
    ├── config.py               # Configuration
    ├── display.py              # Display detection & switching
    ├── menubar.py              # Menu bar hide/show
    └── windows.py              # Window enumeration & resizing
```

## License

MIT License - feel free to use and modify as needed.

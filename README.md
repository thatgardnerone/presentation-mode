# Presentation Mode Scripts

Quickly switch your main display to 1280x720 HD resolution with optimized window management for screensharing on YouTube, Google Meet, and other platforms.

## Features

- **Fast display switching**: Changes your main display to 1280x720 (HD) with scaling for crisp visuals
- **Automatic window management**: Resizes all visible windows with macOS Tahoe Liquid Glass design system padding
- **Menu bar auto-hide**: Maximizes screen real estate for presentations
- **State preservation**: Saves and restores your original display settings and window positions
- **Performance benchmarking**: Built-in timing to track and optimize execution speed
- **Raycast integration**: Works seamlessly with Raycast script commands

## Requirements

- macOS Tahoe (or compatible version)
- [displayplacer](https://github.com/jakehilborn/displayplacer) installed via Homebrew
- [Raycast](https://raycast.com/) (optional, but recommended)
- `jq` (optional, for better JSON parsing): `brew install jq`

### Installing displayplacer

```bash
brew install displayplacer
```

### Setting Up Python Environment

The scripts use Python with PyObjC to access macOS window management APIs. A local virtual environment is included for dependency isolation.

**First-time setup:**

```bash
cd /Users/YOUR_USERNAME/code/shortcuts/presentation-mode

# Create Python virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install pyobjc-framework-Quartz pyobjc-framework-Cocoa

# Deactivate
deactivate
```

**Note:** The scripts will automatically use the venv if it exists, otherwise they'll fall back to system Python3 (with reduced functionality).

### ⚠️ IMPORTANT: Accessibility Permissions

**These scripts require Accessibility permissions to control windows.**

#### For Raycast Users:

1. Open **System Settings** > **Privacy & Security** > **Accessibility**
2. Click the **lock icon** to make changes (enter your password)
3. Click the **"+"** button
4. Navigate to **Applications** and select **Raycast.app**
5. Ensure the checkbox next to **Raycast** is **enabled**
6. **Restart Raycast** completely (Cmd+Q then reopen)

#### For Terminal Users:

1. Open **System Settings** > **Privacy & Security** > **Accessibility**
2. Find **Terminal.app** in the list (or add it with the "+" button)
3. Ensure it's **enabled**
4. Restart Terminal

**The script will check permissions on startup and show an error if they're not granted.**

## Installation

### For Raycast (Recommended)

1. **Set up the Python environment** (see "Setting Up Python Environment" above)

2. **Create a symlink or copy the entire folder** to make it accessible to Raycast:
   ```bash
   # Option A: Symlink the scripts (recommended - easier to update)
   ln -s /Users/YOUR_USERNAME/code/shortcuts/presentation-mode/enter-presentation-mode.sh ~/.config/raycast/script-commands/
   ln -s /Users/YOUR_USERNAME/code/shortcuts/presentation-mode/exit-presentation-mode.sh ~/.config/raycast/script-commands/

   # Option B: Copy the scripts (they need access to venv and helper .py files)
   # Note: If copying, you'll need to update paths in the scripts or copy the whole folder structure
   ```

3. **Important:** The scripts need access to the `venv/`, `get_windows.py`, and `resize_windows.py` files in the same directory. Using symlinks (Option A) is recommended.

4. Open Raycast and search for "Enter Presentation Mode" or "Exit Presentation Mode"

5. (Optional) Set up keyboard shortcuts in Raycast for quick access

### Manual Usage

You can also run the scripts directly from the terminal:

```bash
# Enter presentation mode
./enter-presentation-mode.sh

# Exit presentation mode
./exit-presentation-mode.sh
```

## How It Works

### Enter Presentation Mode

1. **Hides the menu bar** for maximum screen space
2. **Saves current state** including:
   - Display configuration (2560x1440@60Hz mode ID)
   - All visible window positions and sizes on the main display
3. **Switches display** to 1280x720 HD resolution with scaling enabled
4. **Resizes windows** using macOS Tahoe Liquid Glass design formula:
   ```
   Frame_window = Frame_visible - (2 × Padding)
   ```
   - Default padding: 12px (matching Tahoe's design system)
   - Creates the native "maximized with floating" appearance
5. **Benchmarks performance** and displays timing breakdown

### Exit Presentation Mode

1. **Reads saved state** from `~/.presentation-mode-state.json`
2. **Restores display** to original 2560x1440@60Hz resolution
3. **Restores window positions** to their original locations and sizes
4. **Shows menu bar** again
5. **Cleans up state file**
6. **Benchmarks performance** and displays timing

## Configuration

### Adjusting Window Padding

Edit the padding variables at the top of `enter-presentation-mode.sh`:

```bash
# macOS Tahoe Liquid Glass Design System
# Standard Tahoe padding: 12-16px (up from 8-10px in Sequoia)

PADDING_TOP=12          # pixels from top
PADDING_BOTTOM=12       # pixels from bottom
PADDING_HORIZONTAL=12   # pixels from left and right
```

**Recommended values:**
- **12px**: Default, matches Tahoe design system
- **16px**: Maximum recommended for Tahoe (larger corner radius)
- **8px**: Minimum for visual floating effect

### Adjusting Display Settings

If you need to target a different display or resolution, edit these variables:

```bash
MAIN_DISPLAY_SERIAL="s536870912"  # Your main display serial
TARGET_WIDTH=1280                  # Presentation width
TARGET_HEIGHT=720                  # Presentation height
```

To find your display serial:
```bash
displayplacer list
```

## Performance

Typical execution times (on M-series Mac):

| Operation | Expected Time |
|-----------|--------------|
| Enter Presentation Mode | 1.5-2.5s |
| Exit Presentation Mode | 1.0-2.0s |
| Display switch | 0.3-0.5s |
| Window enumeration | 0.1-0.3s |
| Window resizing | 0.2-0.5s |

The scripts include detailed benchmarking output to help identify bottlenecks.

## Troubleshooting

### ⚠️ "0 window positions saved" or "No windows were resized"

**This is an accessibility permissions issue.** The script cannot control windows without proper permissions.

**Fix:**
1. Open **System Settings** > **Privacy & Security** > **Accessibility**
2. Find **Raycast** (or **Terminal**) in the list
3. If it's already there, **toggle it OFF then ON again**
4. If not there, click **"+"** and add the application
5. **Restart the application completely** (Quit and reopen)
6. Run the script again

The script now checks permissions on startup (Step 0) and will warn you if permissions aren't granted.

### "Could not find 1280x720 mode with scaling enabled"

Your display may not support 1280x720 with scaling. Check available modes:

```bash
displayplacer list
```

Look for modes with `res:1280x720` and `scaling:on`. If none exist, try a different resolution or disable scaling in the script.

### Windows aren't resizing correctly

1. **Check accessibility permissions** (see issue above)
2. Ensure windows are **visible** (not minimized) on the main display
3. Check that the app supports programmatic window resizing (some apps restrict this)
4. Try increasing the delay after display switch: change `sleep 0.5` to `sleep 1.0`

### Menu bar isn't hiding/showing

This also requires accessibility permissions (see the first troubleshooting issue above).

### State file corruption

If the state file gets corrupted, manually delete it:

```bash
rm ~/.presentation-mode-state.json
```

Then run `exit-presentation-mode.sh` manually or just restore your display using:

```bash
displayplacer list  # Find your original mode ID
displayplacer "id:s536870912 mode:59"  # Use your mode ID
```

### Performance is slow

1. Install `jq` for faster JSON parsing: `brew install jq`
2. Close unnecessary windows before entering presentation mode
3. Reduce the number of displays connected (if possible)
4. Check benchmark output to identify which step is slow

## Display Configuration

This setup assumes:
- **Main display**: 27" 4K external monitor (Serial: s536870912)
- **Native resolution**: 2560x1440@60Hz with scaling
- **Presentation resolution**: 1280x720@60Hz with scaling
- **Mac in clamshell mode**: Built-in display ignored
- **Additional displays**: Not affected by the script

## macOS Tahoe Liquid Glass Design

The window padding follows macOS Tahoe's design system:

- **Squircle corners** require larger padding (12-16px vs 8-10px in Sequoia)
- **Floating appearance** created by consistent margins around window edges
- **Visual hierarchy** maintains the "window within screen" aesthetic

## Files

- `enter-presentation-mode.sh`: Main script to enter presentation mode
- `exit-presentation-mode.sh`: Restore script to exit presentation mode
- `~/.presentation-mode-state.json`: Temporary state file (auto-generated)

## Known Limitations

- Only affects windows on the **main display** (Serial: s536870912)
- Only resizes **visible windows** (minimized/hidden windows are ignored)
- Some applications may not support programmatic window resizing
- Requires accessibility permissions for window management
- Display must support 1280x720 with scaling enabled

## Contributing

Feel free to adjust padding values, add new features, or optimize performance. The scripts are designed to be easily customizable.

## License

MIT License - Feel free to use and modify as needed.

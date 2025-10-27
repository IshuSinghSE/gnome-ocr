# Quick Start Guide

## Current Status

✅ **Package structure verified and working**
✅ **OCR engine tested successfully**
⚠️ **Screenshot tool not installed** (optional - see below)

## Two Ways to Use

### 1. With Screenshot Capture (Requires Screenshot Tool)

First, install a screenshot tool:
```bash
# For GNOME
sudo apt install gnome-screenshot

# OR for cross-desktop
sudo apt install flameshot

# OR for KDE
sudo apt install spectacle
```

Then run:
```bash
python3 -m text_extractor.main
```

This will:
1. Prompt you to select a screen area
2. Extract text from that area
3. Copy it to clipboard
4. Show a notification

### 2. With Existing Images (Works Now!)

No screenshot tool needed - test with any image:

```bash
# Use an existing image file
python3 -m text_extractor.main test_dark.png

# Or any other image
python3 -m text_extractor.main path/to/your/image.png
```

This is perfect for:
- Testing the OCR engine
- Batch processing images
- Development and debugging

## What Just Worked

We successfully tested with `test_dark.png`:
- ✅ Engine loaded in 0.27 seconds
- ✅ OCR completed in 5.10 seconds  
- ✅ Extracted 6 text segments
- ✅ Text copied to clipboard

## Check Screenshot Tools

Run this to see what's available:
```bash
./install/check_screenshot_tools.sh
```

## Installation Options

### Quick Test (No Installation)
```bash
# Just run it
python3 -m text_extractor.main image.png
```

### Full Installation
```bash
# Install system-wide with desktop integration
./install/install.sh
```

This adds:
- Desktop menu entry
- Ready for keyboard shortcuts
- System-wide availability

## Troubleshooting

### "No screenshot tool found"
- Install one: `sudo apt install flameshot` (recommended)
- Or use existing images: `python3 -m text_extractor.main image.png`

### "Screenshot capture failed"
- You might have cancelled the selection
- Try again and complete the area selection
- Or use an existing image as shown above

### Import errors
- Run: `uv sync` or `pip install -e .`
- Make sure you're in the project directory

## Next Steps

1. **Test Now**: `python3 -m text_extractor.main test_dark.png`
2. **Install Screenshot Tool**: `sudo apt install flameshot`
3. **Try Live Capture**: `python3 -m text_extractor.main`
4. **Set Keyboard Shortcut**: See README.md for instructions

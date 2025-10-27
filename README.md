# GNOME Text Extractor

A smart OCR tool for GNOME desktop that extracts text from screenshots with intelligent image preprocessing.

## Features

- 🎯 **Smart Image Preprocessing**: Automatically detects and inverts dark-mode screenshots
- 🚀 **Fast & Accurate**: Uses RapidOCR with ONNX runtime for high-quality text extraction
- 🖥️ **GNOME Integration**: Seamless integration with GNOME screenshot tool
- 📋 **Clipboard Support**: Automatically copies extracted text to clipboard
- 🔔 **Desktop Notifications**: Shows extraction status and results
- 📦 **Clean Architecture**: Designed for easy evolution from v1 (cold-start) to v2 (daemon)

## Requirements

### System Dependencies

- **Screenshot Tool** (one of the following):
  - `gnome-screenshot` (GNOME) - recommended for GNOME users
  - `flameshot` - cross-desktop, feature-rich
  - `spectacle` (KDE) - for KDE Plasma users
- `libnotify-bin` (notify-send) - for desktop notifications

Install on Ubuntu/Debian:
```bash
# For GNOME users
sudo apt install gnome-screenshot libnotify-bin

# Or for a cross-desktop alternative
sudo apt install flameshot libnotify-bin
```

### Python Requirements

- Python 3.8 or higher
- Dependencies are managed via `pyproject.toml`

## Installation

### Quick Install

1. Clone the repository:
```bash
git clone https://github.com/IshuSinghSE/gnome-ocr.git
cd gnome-ocr
```

2. Run the installation script:
```bash
chmod +x install/install.sh
./install/install.sh
```

This will:
- Check for required system dependencies
- Install Python dependencies using `uv` (or `pip` as fallback)
- Install the desktop entry so you can launch from your application menu
- Set up everything needed to run the app

### Manual Install

If you prefer to install manually:

```bash
# Install Python dependencies
uv sync
# or
pip install -e .

# Install desktop entry (optional)
mkdir -p ~/.local/share/applications
cp install/text-extractor.desktop ~/.local/share/applications/
update-desktop-database ~/.local/share/applications/
```

## Usage

### From Application Menu

After installation, find "Text Extractor" in your GNOME application menu and click to launch.

### From Terminal

```bash
# Run with screenshot capture
python3 -m text_extractor.main

# Or test with an existing image file (no screenshot needed)
python3 -m text_extractor.main path/to/image.png

# If installed with pip/uv
text-extractor
# or with existing image
text-extractor path/to/image.png
```

### Setting Up a Keyboard Shortcut (Recommended)

1. Open **Settings** → **Keyboard** → **Keyboard Shortcuts**
2. Scroll to **Custom Shortcuts**
3. Click **+** to add a new shortcut
4. **Name**: `Text Extractor`
5. **Command**: `python3 -m text_extractor.main`
6. Set your preferred shortcut (e.g., `Super+Shift+T`)

Now you can extract text from any part of your screen with a single keystroke!

## How It Works

1. **Capture**: Press your keyboard shortcut or launch the app
2. **Select**: Click and drag to select the area containing text
3. **Process**: The app applies smart preprocessing (dark mode detection, inversion, etc.)
4. **Extract**: RapidOCR extracts the text using ONNX models
5. **Copy**: Text is automatically copied to your clipboard
6. **Notify**: Desktop notification shows the result

## Project Structure

```
gnome-ocr/
├── text_extractor/          # Main Python package
│   ├── __init__.py          # Package initialization
│   ├── backend.py           # OCR engine with smart preprocessing
│   ├── desktop.py           # GNOME desktop integration
│   └── main.py              # v1 entry point (cold-start)
├── install/                 # Installation files
│   ├── install.sh           # Installation script
│   ├── text-extractor.desktop  # GNOME desktop entry
│   └── autostart/           # (Future) For v2 daemon
├── assets/                  # Application assets (icons, etc.)
├── pyproject.toml           # Python project configuration
└── README.md                # This file
```

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
# Format code
black text_extractor/

# Lint code
ruff check text_extractor/
```

### Architecture Notes

This project is designed with a clean architecture that supports evolution:

- **v1 (Current)**: Cold-start mode - loads OCR engine on each run
- **v2 (Future)**: Daemon mode - OCR engine stays loaded in background for instant results

The modular structure (`backend.py`, `desktop.py`, `main.py`) makes this transition seamless.

## Troubleshooting

### "Screenshot capture failed"
- Ensure `gnome-screenshot` is installed
- Check if you cancelled the area selection

### "Failed to load OCR engine"
- Verify Python dependencies are installed: `uv sync` or `pip install -e .`
- Check for sufficient disk space (models are downloaded on first run)

### "No text found"
- Try selecting a larger area
- Ensure the text is clearly visible
- Check that the screenshot isn't too blurry

### Import errors
- Make sure you're running from the project root
- Verify the virtual environment is activated
- Reinstall dependencies: `uv sync --force`

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

MIT License - see LICENSE file for details

## Acknowledgments

- [RapidOCR](https://github.com/RapidAI/RapidOCR) - Fast and accurate OCR engine
- GNOME Project - Desktop environment integration tools

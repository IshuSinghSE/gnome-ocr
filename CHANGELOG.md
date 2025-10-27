# Changelog

All notable changes to GNOME Text Extractor will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-28

### Added
- Initial release of GNOME Text Extractor
- Smart image preprocessing with automatic dark mode detection
- RapidOCR integration with ONNX runtime
- Multi-tool screenshot support (gnome-screenshot, flameshot, spectacle)
- Automatic clipboard integration
- Desktop notifications for extraction status
- GNOME desktop integration with `.desktop` file
- Comprehensive installation script
- Python 3.8+ support
- Clean package structure for future daemon implementation (v2)

### Features
- **Smart Preprocessing**: Automatically detects and inverts dark-mode screenshots for better OCR accuracy
- **Fast OCR**: Uses RapidOCR with ONNX runtime for high-quality text extraction
- **Desktop Integration**: Seamless GNOME experience with screenshot tools and notifications
- **Clipboard Support**: Extracted text automatically copied to clipboard
- **Multi-tool Support**: Works with gnome-screenshot, flameshot, or spectacle

### Technical
- Package structure: `text_extractor/` with separate `backend.py` and `desktop.py` modules
- Modern Python packaging with `pyproject.toml`
- Type hints throughout codebase
- Comprehensive error handling
- Cross-platform Linux support (GNOME, KDE, generic desktops)

[1.0.0]: https://github.com/IshuSinghSE/gnome-ocr/releases/tag/v1.0.0

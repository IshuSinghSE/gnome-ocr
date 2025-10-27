# Contributing to GNOME Text Extractor

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/gnome-ocr.git`
3. Create a feature branch: `git checkout -b feature-name`
4. Make your changes
5. Test your changes thoroughly
6. Commit with clear messages: `git commit -m "Add feature: description"`
7. Push to your fork: `git push origin feature-name`
8. Open a Pull Request

## Development Setup

```bash
# Clone the repository
git clone https://github.com/IshuSinghSE/gnome-ocr.git
cd gnome-ocr

# Install dependencies
uv sync --dev
# or
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black text_extractor/
ruff check text_extractor/
```

## Code Guidelines

- Follow PEP 8 style guide
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions focused and small
- Add tests for new features
- Update documentation for user-facing changes

## Testing

- Test on GNOME Shell (Wayland and X11)
- Test with different screenshot tools (gnome-screenshot, flameshot, spectacle)
- Test with various image types (dark mode, light mode, complex layouts)
- Verify clipboard functionality
- Check desktop notifications

## Pull Request Process

1. Update README.md if needed
2. Update QUICKSTART.md for user-facing changes
3. Ensure all tests pass
4. Update version number in `text_extractor/__init__.py` if appropriate
5. Request review from maintainers

## Reporting Bugs

Use GitHub Issues and include:
- Operating system and version
- Desktop environment (GNOME version, Wayland/X11)
- Python version
- Screenshot tool being used
- Steps to reproduce
- Expected vs actual behavior
- Error messages or logs

## Feature Requests

Open an issue with:
- Clear description of the feature
- Use cases and benefits
- Potential implementation approach (if you have ideas)

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help others learn and grow

## Questions?

Feel free to open an issue for questions or join discussions!

# Distribution Checklist

Use this checklist before releasing a new version.

## Pre-Release

- [ ] All features tested and working
- [ ] Code reviewed and cleaned up
- [ ] No TODO/FIXME comments in critical code
- [ ] All tests pass (if any)
- [ ] Documentation updated
  - [ ] README.md reflects all features
  - [ ] QUICKSTART.md is accurate
  - [ ] CHANGELOG.md has new version entry
  - [ ] CONTRIBUTING.md is up to date
- [ ] Version bumped in:
  - [ ] `pyproject.toml`
  - [ ] `text_extractor/__init__.py`
- [ ] Dependencies reviewed and updated
- [ ] LICENSE file present and correct
- [ ] No sensitive data in code

## Distribution Validation

Run the validation script:
```bash
chmod +x scripts/check-dist.sh
./scripts/check-dist.sh
```

## Build

Build distribution packages:
```bash
chmod +x scripts/build-dist.sh
./scripts/build-dist.sh
```

## Test Distribution

Test the built package:
```bash
# Create a test environment
python3 -m venv test-env
source test-env/bin/activate

# Install the wheel
pip install dist/gnome_text_extractor-*.whl

# Test the command
text-extractor --help  # or test with actual usage

# Cleanup
deactivate
rm -rf test-env
```

## Release

### GitHub Release

1. Commit all changes:
   ```bash
   git add .
   git commit -m "Release v1.0.0"
   git push origin master
   ```

2. Create and push tag:
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```

3. GitHub Actions will automatically create a release with artifacts

### PyPI Release (Optional)

1. Create PyPI account at https://pypi.org/

2. Upload to TestPyPI first:
   ```bash
   python3 -m twine upload --repository testpypi dist/*
   ```

3. Test installation from TestPyPI:
   ```bash
   pip install --index-url https://test.pypi.org/simple/ gnome-text-extractor
   ```

4. If everything works, upload to PyPI:
   ```bash
   python3 -m twine upload dist/*
   ```

## Post-Release

- [ ] GitHub release published successfully
- [ ] Release notes look correct
- [ ] Installation tested from GitHub release
- [ ] Announcement posted (if applicable)
- [ ] Issues/PRs updated with release info

## Version Numbering

Follow [Semantic Versioning](https://semver.org/):
- **MAJOR** (1.0.0): Incompatible API changes
- **MINOR** (0.1.0): New functionality, backwards compatible
- **PATCH** (0.0.1): Bug fixes, backwards compatible

## Common Issues

### Build Fails
- Check Python version (>= 3.8)
- Ensure `build` package is installed
- Review `pyproject.toml` syntax

### Import Fails
- Verify package structure
- Check `__init__.py` exists
- Ensure dependencies are listed

### GitHub Actions Fails
- Check workflow file syntax
- Verify secrets are configured
- Review GitHub Actions logs

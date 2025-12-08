# Contributing to Phishing URL Detector

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, etc.)

### Suggesting Features

Feature requests are welcome! Please:
- Check if the feature already exists
- Describe the use case clearly
- Explain why it would be valuable

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow PEP 8 style guidelines
   - Add tests for new features
   - Update documentation as needed

4. **Test your changes**
   ```bash
   python test_quick.py
   python verify_system.py
   ```

5. **Commit your changes**
   ```bash
   git commit -m "Add: brief description of changes"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Describe your changes
   - Reference any related issues
   - Wait for review

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/phishing-url-detector.git
cd phishing-url-detector

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
python test_quick.py
```

## Code Style

- Follow PEP 8
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and small
- Write tests for new features

## Testing

All contributions should include tests:
- Unit tests for new functions
- Integration tests for new features
- Update existing tests if behavior changes

## Documentation

Update documentation when:
- Adding new features
- Changing existing behavior
- Adding new configuration options
- Modifying API endpoints

## Questions?

Feel free to open an issue for any questions about contributing!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

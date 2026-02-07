# Contributing to MoltMobo

Thank you for your interest in contributing to MoltMobo! 🎉

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Logs from `logs/moltmobo.log`
- Your environment (Android version, Termux version)

### Suggesting Features

We welcome feature suggestions! Please open an issue with:
- Clear description of the feature
- Use case / why it's needed
- Proposed implementation (optional)

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Add tests** for new functionality
5. **Run tests**:
   ```bash
   pytest tests/ -v
   ```
6. **Update documentation** if needed
7. **Commit with clear messages**:
   ```bash
   git commit -m "Add: feature description"
   ```
8. **Push and create Pull Request**

## Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/moltmobo.git
cd moltmobo

# Install dependencies
pip install -r requirements.txt

# Install dev dependencies
pip install pytest black flake8

# Run tests
pytest tests/ -v
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints where possible
- Add docstrings to functions and classes
- Keep functions focused and small
- Comment complex logic

### Formatting

```bash
# Format code
black *.py utils/*.py

# Check style
flake8 *.py utils/*.py
```

## Testing

- Write unit tests for new features
- Ensure all tests pass before submitting PR
- Aim for >80% code coverage

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

## Areas for Contribution

### High Priority
- [ ] Vision-based UI understanding (Moondream integration)
- [ ] More robust error handling
- [ ] Performance optimizations
- [ ] Better LLM prompt engineering

### Medium Priority
- [ ] Support for more LLM providers (OpenAI, Gemini)
- [ ] Web UI for configuration
- [ ] Task scheduling / automation
- [ ] Multi-device support

### Documentation
- [ ] Video tutorials
- [ ] More usage examples
- [ ] API documentation
- [ ] Architecture diagrams

## Pull Request Guidelines

### PR Title Format
- `Add: [feature]` - New feature
- `Fix: [bug]` - Bug fix
- `Docs: [change]` - Documentation
- `Refactor: [change]` - Code refactoring
- `Test: [change]` - Test additions/changes

### PR Description
Include:
- What changed and why
- Related issue number (if any)
- Testing done
- Screenshots (if UI changes)

## Community Guidelines

- Be respectful and constructive
- Help others in issues and discussions
- Share your use cases and experiences
- Report security issues privately

## Questions?

- Open a discussion on GitHub
- Check existing issues and documentation
- Join our community chat (if available)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for making MoltMobo better! 🚀

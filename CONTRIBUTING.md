# Contributing to Virtual Cavity RF Simulator

Thank you for your interest in contributing to the Virtual Cavity RF Simulator! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- Git version control
- Familiarity with RF/accelerator physics (helpful but not required)
- Basic knowledge of GUI development with tkinter/matplotlib

### Development Environment Setup

1. **Fork the Repository**
   ```bash
   # Click the "Fork" button on GitHub, then clone your fork
   git clone https://github.com/iuming/virtual-cavity-simulator.git
   cd virtual-cavity-simulator
   ```

2. **Set Up Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

4. **Verify Installation**
   ```bash
   python -m pytest tests/
   python launch_gui.py
   ```

## 📋 How to Contribute

### Types of Contributions

We welcome various types of contributions:

- 🐛 **Bug Reports**: Help us identify and fix issues
- 💡 **Feature Requests**: Suggest new functionality
- 📖 **Documentation**: Improve docs, tutorials, examples
- 🔧 **Code Contributions**: Bug fixes, new features, optimizations
- 🧪 **Testing**: Add tests, improve test coverage
- 🎨 **UI/UX**: Improve user interface and experience

### Reporting Bugs

Before submitting a bug report:

1. **Check existing issues** to avoid duplicates
2. **Use the latest version** to ensure the bug still exists
3. **Provide minimal reproduction** steps

Bug report template:
```markdown
**Bug Description**
A clear description of the bug

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See error

**Expected Behavior**
What you expected to happen

**Screenshots**
If applicable, add screenshots

**Environment:**
- OS: [e.g., Windows 10, Ubuntu 20.04]
- Python Version: [e.g., 3.8.5]
- Package Versions: [run `pip list`]

**Additional Context**
Any other context about the problem
```

### Suggesting Features

Feature request template:
```markdown
**Feature Description**
A clear description of the feature you'd like to see

**Use Case**
Describe the problem this feature would solve

**Proposed Solution**
Your ideas for implementing this feature

**Alternatives Considered**
Other solutions you've considered

**Additional Context**
Screenshots, mockups, references, etc.
```

## 🔧 Development Workflow

### Branching Strategy

- `main`: Stable release branch
- `develop`: Development integration branch
- `feature/feature-name`: New feature branches
- `bugfix/issue-description`: Bug fix branches
- `hotfix/critical-fix`: Critical fixes for main branch

### Making Changes

1. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Your Changes**
   - Follow coding standards (see below)
   - Add tests for new functionality
   - Update documentation as needed

3. **Test Your Changes**
   ```bash
   python -m pytest tests/
   python -m flake8 .
   python -m black .
   ```

4. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "Add feature: brief description"
   ```

5. **Push and Create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   # Create PR on GitHub
   ```

### Pull Request Process

1. **PR Title**: Use descriptive titles
   - `Add: New feature description`
   - `Fix: Bug description`
   - `Update: Documentation/dependency update`
   - `Refactor: Code refactoring description`

2. **PR Description**: Include:
   - Summary of changes
   - Related issue numbers
   - Testing performed
   - Screenshots (for UI changes)

3. **Review Process**:
   - Code review by maintainers
   - Automated tests must pass
   - Documentation updates required
   - Approval from at least one maintainer

## 📝 Coding Standards

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with some modifications:

- **Line Length**: 88 characters (Black formatter default)
- **Imports**: Use absolute imports, group by standard/third-party/local
- **Docstrings**: Use Google-style docstrings
- **Type Hints**: Encouraged for new code

### Code Formatting

Use automated tools:
```bash
# Format code
black .

# Sort imports
isort .

# Lint code
flake8 .

# Type checking
mypy .
```

### Documentation Strings

Example docstring format:
```python
def simulate_cavity(frequency: float, amplitude: float) -> tuple:
    """Simulate RF cavity response.
    
    Args:
        frequency: RF frequency in Hz
        amplitude: Signal amplitude in V
        
    Returns:
        Tuple of (cavity_voltage, reflected_voltage)
        
    Raises:
        ValueError: If frequency is negative
        
    Example:
        >>> vc, vr = simulate_cavity(1.3e9, 1.0)
        >>> print(f"Cavity voltage: {vc}")
    """
```

### Naming Conventions

- **Variables**: `snake_case`
- **Functions**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private methods**: `_leading_underscore`

## 🧪 Testing Guidelines

### Test Structure

```
tests/
├── test_simulation.py      # Core simulation tests
├── test_gui.py            # GUI component tests
├── test_integration.py    # Integration tests
└── conftest.py           # Pytest configuration
```

### Writing Tests

```python
import pytest
from cavity_simulator import CavitySimulator

class TestCavitySimulator:
    def test_simulation_step(self):
        """Test single simulation step."""
        simulator = CavitySimulator()
        result = simulator.step()
        assert result is not None
        assert len(result) == 3  # vc, vr, dw
    
    @pytest.mark.parametrize("frequency", [1.3e9, 1.4e9])
    def test_frequency_response(self, frequency):
        """Test frequency response."""
        simulator = CavitySimulator(frequency=frequency)
        # Test implementation
```

### Test Coverage

- Aim for >80% code coverage
- Focus on critical paths and edge cases
- Include both unit and integration tests

## 📚 Documentation

### Documentation Structure

```
docs/
├── installation.md         # Installation guide
├── user_guide.md          # User manual
├── api_reference.md       # API documentation
├── developer_guide.md     # Development guide
└── examples/              # Usage examples
```

### Writing Documentation

- Use clear, concise language
- Include code examples
- Add screenshots for GUI features
- Keep documentation up-to-date with code changes

## 🏷️ Release Process

### Version Numbering

We use [Semantic Versioning](https://semver.org/):
- `MAJOR.MINOR.PATCH`
- `MAJOR`: Breaking changes
- `MINOR`: New features (backward compatible)
- `PATCH`: Bug fixes (backward compatible)

### Release Checklist

- [ ] Update version numbers
- [ ] Update CHANGELOG.md
- [ ] Run full test suite
- [ ] Update documentation
- [ ] Create release notes
- [ ] Tag release in Git
- [ ] Create GitHub release

## 🤝 Community Guidelines

### Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Maintain professional communication

### Communication Channels

- **GitHub Issues**: Bug reports, feature requests
- **Pull Requests**: Code contributions, discussions
- **Email**: mliu@ihep.ac.cn for direct contact

## ❓ Getting Help

### Resources

- [README.md](README.md): Project overview
- [User Guide](docs/user_guide.md): Usage instructions
- [API Reference](docs/api_reference.md): Code documentation
- [GitHub Issues](https://github.com/iuming/virtual-cavity-simulator/issues): Community support

### Common Questions

**Q: How do I set up the development environment?**
A: Follow the "Development Environment Setup" section above.

**Q: What should I work on first?**
A: Check the "good first issue" label in GitHub Issues.

**Q: How do I run the tests?**
A: Use `python -m pytest tests/` to run all tests.

**Q: My PR was rejected, what now?**
A: Address the feedback and resubmit. Don't take it personally!

## 🙏 Recognition

Contributors are recognized in:
- [CONTRIBUTORS.md](CONTRIBUTORS.md) file
- GitHub contributors page
- Release notes
- Academic publications (when appropriate)

Thank you for contributing to the Virtual Cavity RF Simulator! 🚀

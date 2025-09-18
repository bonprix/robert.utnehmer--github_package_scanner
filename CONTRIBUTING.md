# Contributing to GitHub IOC Scanner

Thank you for your interest in contributing to the GitHub IOC Scanner! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Issues

1. **Security Issues**: For security-related issues, please email security@example.com instead of using the public issue tracker.

2. **Bug Reports**: Use the GitHub issue tracker to report bugs. Include:
   - Clear description of the issue
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)
   - Log output (with sensitive information redacted)

3. **Feature Requests**: We welcome feature requests! Please:
   - Check if the feature already exists or is planned
   - Describe the use case and benefits
   - Provide examples of how it would work

### Development Process

1. **Fork the Repository**
   ```bash
   git clone https://github.com/your-username/github-ioc-scanner.git
   cd github-ioc-scanner
   ```

2. **Set Up Development Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev]"
   ```

3. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make Your Changes**
   - Follow the coding standards (see below)
   - Add tests for new functionality
   - Update documentation as needed

5. **Run Tests**
   ```bash
   pytest
   pytest --cov=src/github_ioc_scanner  # With coverage
   ```

6. **Submit a Pull Request**
   - Push your branch to your fork
   - Create a pull request with a clear description
   - Link any related issues

## 📝 Coding Standards

### Python Code Style

We follow PEP 8 with some modifications:

- **Line Length**: 88 characters (Black default)
- **Import Sorting**: Use isort with Black profile
- **Type Hints**: Required for all public functions
- **Docstrings**: Google-style docstrings for all public functions

### Code Formatting

We use automated code formatting:

```bash
# Format code
black src/ tests/
isort src/ tests/

# Check formatting
black --check src/ tests/
isort --check-only src/ tests/

# Type checking
mypy src/

# Linting
flake8 src/ tests/
```

### Example Code Style

```python
"""Module docstring describing the purpose."""

from typing import List, Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class ExampleClass:
    """Class docstring describing the class purpose.
    
    Attributes:
        attribute_name: Description of the attribute.
    """
    
    def __init__(self, param: str, optional_param: Optional[int] = None) -> None:
        """Initialize the class.
        
        Args:
            param: Description of the parameter.
            optional_param: Description of the optional parameter.
        """
        self.attribute_name = param
        self._private_attribute = optional_param
    
    def public_method(self, data: List[str]) -> Dict[str, Any]:
        """Public method with proper type hints and docstring.
        
        Args:
            data: List of strings to process.
            
        Returns:
            Dictionary containing processed results.
            
        Raises:
            ValueError: If data is empty.
        """
        if not data:
            raise ValueError("Data cannot be empty")
        
        return {"processed": len(data), "items": data}
```

## 🧪 Testing Guidelines

### Test Structure

- **Unit Tests**: Test individual functions and classes
- **Integration Tests**: Test component interactions
- **End-to-End Tests**: Test complete workflows

### Test Organization

```
tests/
├── test_parsers.py          # Parser unit tests
├── test_github_client.py    # GitHub client tests
├── test_scanner.py          # Scanner integration tests
├── test_cli.py             # CLI interface tests
├── test_batch_*.py         # Batch processing tests
└── test_e2e_*.py           # End-to-end tests
```

### Writing Tests

```python
import pytest
from unittest.mock import Mock, patch

from src.github_ioc_scanner.scanner import GitHubIOCScanner


class TestGitHubIOCScanner:
    """Test cases for GitHubIOCScanner."""
    
    def test_scanner_initialization(self):
        """Test scanner initializes correctly."""
        # Test implementation
        pass
    
    @patch('src.github_ioc_scanner.scanner.GitHubClient')
    def test_scanner_with_mock(self, mock_client):
        """Test scanner with mocked dependencies."""
        # Test implementation with mocks
        pass
    
    def test_error_handling(self):
        """Test proper error handling."""
        with pytest.raises(ValueError):
            # Test code that should raise ValueError
            pass
```

### Test Coverage

- Aim for >90% test coverage
- All new features must include tests
- Critical paths must have comprehensive test coverage

## 📚 Documentation

### Code Documentation

- **Docstrings**: All public functions, classes, and modules
- **Type Hints**: Required for all function signatures
- **Comments**: Explain complex logic, not obvious code

### User Documentation

- **README**: Keep the main README up to date
- **API Documentation**: Document all public APIs
- **Examples**: Provide working examples for new features
- **Changelog**: Update CHANGELOG.md for all changes

## 🔒 Adding IOC Definitions

### IOC File Format

IOC definitions are stored in Python files in the `issues/` directory:

```python
"""
Attack Name - Date

Description of the attack, sources, and context.

Source: URL to threat intelligence or research
Date: When the attack was discovered
Attack Type: Type of supply chain attack
"""

IOC_PACKAGES = {
    # Package name with specific compromised versions
    "malicious-package": ["1.0.0", "1.0.1", "2.0.0"],
    
    # Package where any version is compromised
    "completely-malicious": None,
    
    # Scoped packages
    "@malicious/package": ["1.0.0"],
    "@namespace/compromised": None,
}
```

### IOC Guidelines

1. **Verification**: Verify IOCs from multiple sources
2. **Documentation**: Include source URLs and context
3. **Accuracy**: Ensure package names and versions are correct
4. **Attribution**: Credit original researchers when possible

### IOC Sources

Acceptable sources for IOCs:
- Published security research
- Threat intelligence reports
- Official security advisories
- Verified incident reports
- Package registry takedown notices

## 🚀 Performance Considerations

### Code Performance

- **Async/Await**: Use async code for I/O operations
- **Caching**: Implement appropriate caching strategies
- **Batch Processing**: Use batch operations for multiple requests
- **Memory Usage**: Be mindful of memory consumption with large datasets

### Testing Performance

- **Benchmarks**: Include performance benchmarks for critical paths
- **Profiling**: Profile code to identify bottlenecks
- **Load Testing**: Test with realistic data volumes

## 🔄 Release Process

### Version Numbering

We use Semantic Versioning (SemVer):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Run full test suite
4. Update documentation
5. Create release tag
6. Publish to PyPI

## 🛡️ Security Guidelines

### Secure Coding Practices

- **Input Validation**: Validate all external inputs
- **Error Handling**: Don't expose sensitive information in errors
- **Logging**: Don't log sensitive data (tokens, credentials)
- **Dependencies**: Keep dependencies up to date

### Security Testing

- **Static Analysis**: Use security-focused linters
- **Dependency Scanning**: Regularly scan dependencies for vulnerabilities
- **Secret Detection**: Ensure no secrets are committed

## 📞 Getting Help

### Communication Channels

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Email**: security@example.com for security issues

### Code Review Process

1. All changes require review from a maintainer
2. Automated tests must pass
3. Code must follow style guidelines
4. Documentation must be updated for user-facing changes

## 🏆 Recognition

Contributors will be recognized in:
- `CONTRIBUTORS.md` file
- Release notes for significant contributions
- GitHub contributor statistics

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to the GitHub IOC Scanner! Your efforts help make the software supply chain more secure for everyone. 🙏
# Contributing to porkbun-mcp

Thanks for your interest in contributing! This document outlines how to get started.

## Development Setup

```bash
# Clone the repository
git clone https://github.com/major/porkbun-mcp.git
cd porkbun-mcp

# Install dependencies (requires uv)
uv sync --dev

# Run all checks
make check
```

## Development Commands

```bash
make check        # Full CI: lint + format-check + typecheck + test
make lint         # ruff check
make format       # ruff format
make typecheck    # ty check
make test         # pytest with coverage
make fix          # Auto-fix lint + format
make complexity   # Check for complex functions
```

## Code Standards

- **Line length**: 100 characters
- **Docstrings**: Google-style (enforced by ruff D rules)
- **Type hints**: Required on all functions
- **Type checker**: ty (not pyright or mypy)
- **Async**: Default for I/O operations

## Pull Request Process

1. Fork the repository and create a feature branch
2. Make your changes with tests
3. Ensure `make check` passes
4. Submit a PR with a clear description

### Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation only
- `test:` adding/updating tests
- `refactor:` code change that neither fixes a bug nor adds a feature
- `chore:` maintenance tasks

## Testing

Tests use pytest with pytest-asyncio:

```bash
# Run all tests
make test

# Run specific test file
uv run pytest tests/test_dns_tools.py

# Run with verbose output
uv run pytest -v
```

## Questions?

Open an issue for questions or discussion.

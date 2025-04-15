# Contributing to llmcp

Thank you for your interest in contributing to llmcp!

## Development Setup

### Installing for Development

```bash
# Clone the repository
git clone https://github.com/yourusername/llmcp.git
cd llmcp

# Install in development mode with uv
uv pip install -e .

# Install development dependencies
uv pip install -e ".[dev]"
```

## Running Tests

The test suite is divided into unit tests and integration tests:

```bash
# Run unit tests only (no API calls)
pytest -m "not integration"

# Run integration tests (requires API keys)
pytest -m integration

# Run all tests
pytest
```

Integration tests require valid API keys set as environment variables:
- `OPENAI_API_KEY` - Required for OpenAI models tests
- `ANTHROPIC_API_KEY` - Required for Anthropic models tests

## Code Style

This project uses ruff for linting and formatting:

```bash
# Run linting
ruff check .

# Apply auto-fixes
ruff check --fix .

# Format code
ruff format .
```

## Project Structure

- `src/llmcp/` - Package source code
  - `__init__.py` - Package initialization
  - `cli.py` - Command-line interface
  - `client.py` - Client functionality (search, test)
  - `server.py` - MCP server implementation
- `tests/` - Test suite
  - `test_unit.py` - Unit tests (no API calls)
  - `test_integration.py` - Integration tests (requires API keys)

## Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests to ensure they pass
5. Submit a pull request

## License

By contributing to this project, you agree to license your contributions under the same MIT license used by this project.
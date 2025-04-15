"""llmcp: A minimal CLI for interacting with LLMs via LiteLLM and MCP."""

import importlib.metadata

try:
    __version__ = importlib.metadata.version("llmcp")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.1.0"  # Default during development
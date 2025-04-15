"""Integration tests for llmcp.

These tests require valid API keys and will make actual API calls.
Skip them if you don't have the necessary API keys set up.
"""
import os
import pytest
import subprocess
import json
from io import StringIO
import sys

# Mark all tests as integration tests
pytestmark = pytest.mark.integration


def has_api_key(provider):
    """Check if API key is available for the given provider."""
    if provider == "openai":
        return bool(os.environ.get("OPENAI_API_KEY", ""))
    elif provider == "anthropic":
        return bool(os.environ.get("ANTHROPIC_API_KEY", ""))
    return False


@pytest.mark.skipif(not has_api_key("openai"), reason="OpenAI API key not set")
def test_search_openai():
    """Test that search finds OpenAI models."""
    # Capture stdout
    output = subprocess.check_output(
        ["python", "-m", "llmcp.cli", "search", "gpt-*"],
        text=True
    )
    
    # Verify output contains expected OpenAI models
    assert "gpt-" in output
    assert "OpenAI" in output


@pytest.mark.skipif(not has_api_key("openai"), reason="OpenAI API key not set")
def test_llm_response():
    """Test that testing an LLM returns a valid response."""
    # This is a simple integration test to verify real API interaction
    try:
        # Run the test command with a timeout
        output = subprocess.check_output(
            ["python", "-m", "llmcp.cli", "test", "gpt-3.5-turbo", "What is the capital of France?"],
            text=True,
            timeout=15  # 15 second timeout
        )
        
        # Check if the response contains the expected answer
        assert "Paris" in output
        
    except subprocess.TimeoutExpired:
        pytest.skip("Test timed out - API might be slow or unavailable")
    except subprocess.CalledProcessError:
        pytest.fail("Command execution failed")
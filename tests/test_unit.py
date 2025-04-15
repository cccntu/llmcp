"""Unit tests for core llmcp functionality."""
import pytest
from unittest.mock import patch, MagicMock
import os
import sys

from llmcp.search import get_models, check_api_key


def test_check_api_key():
    """Test API key checking functionality."""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-test"}, clear=True):
        # Should return True for OpenAI since we set that key
        assert check_api_key("openai") is True
        
        # Should return False for providers without keys
        assert check_api_key("anthropic") is False


def test_get_models_minimal():
    """Test that get_models returns a dictionary."""
    with patch("litellm.get_llm_provider") as mock_provider:
        # Mock minimal provider response
        mock_provider.return_value = ("dummy", "openai", "dummy", "dummy")
        
        # Get models
        models = get_models()
        
        # Verify we get a non-empty dictionary
        assert isinstance(models, dict)
        assert len(models) > 0
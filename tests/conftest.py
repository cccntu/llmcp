"""Test configuration for llmcp."""
import pytest
import os
import sys
from pathlib import Path

# Add the project root to the Python path to ensure imports work
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Set critical log level to avoid unnecessary logs during tests
import logging
logging.basicConfig(level=logging.CRITICAL)
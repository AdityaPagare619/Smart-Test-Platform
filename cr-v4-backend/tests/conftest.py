"""
CR-V4 Test Configuration
Pytest fixtures and configuration
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Configure pytest-asyncio
pytest_plugins = ['pytest_asyncio']

# Global fixtures can be added here

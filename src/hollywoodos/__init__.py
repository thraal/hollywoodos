# src/hollywoodos/__init__.py
"""
HollywoodOS - A terminal-based cinematic computer activity simulator.
"""

__version__ = "0.1.0"
__author__ = "thraal"
__email__ = "thraal@gmail.com"

# Import main classes for convenient access
from .app import HollywoodOS
from .core.config_manager import ConfigManager
from .plugins.registry import PluginRegistry

# Define what gets imported with "from hollywoodos import *"
__all__ = [
    "HollywoodOS",
    "ConfigManager", 
    "PluginRegistry",
    "__version__",
]

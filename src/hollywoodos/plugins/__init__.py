# src/hollywoodos/plugins/__init__.py
"""
Plugin system for HollywoodOS.
"""

from .registry import PluginRegistry
from .base import BlinkenPlugin
from .effects import EffectRegistry

__all__ = [
    "PluginRegistry",
    "BlinkenPlugin", 
    "EffectRegistry",
]

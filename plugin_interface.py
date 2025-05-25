from abc import ABC, abstractmethod
from textual.widget import Widget
from typing import Dict, Any

class BlinkenPlugin(ABC):
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
    
    @abstractmethod
    def create_widget(self) -> Widget:
        """Create and return the widget for this plugin"""
        pass
    
    def update_config(self, config: Dict[str, Any]):
        """Update plugin configuration"""
        self.config.update(config)
        self.on_config_updated()
    
    def on_config_updated(self):
        """Called when configuration is updated - override to react to changes"""
        pass
    
    def get_config_value(self, key: str, default=None):
        """Get a configuration value with fallback to default"""
        return self.config.get(key, default)
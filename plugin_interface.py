# plugin_interface.py
from abc import ABC, abstractmethod
from textual.widget import Widget
from typing import Dict, Any, Optional

class BlinkenPlugin(ABC):
    """Base class for all HollywoodOS plugins"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self._widget: Optional[Widget] = None
        
    @abstractmethod
    def create_widget(self) -> Widget:
        """Create and return the widget for this plugin"""
        pass
        
    def get_config(self, key: str, default: Any = None) -> Any:
        """Get a configuration value"""
        return self.config.get(key, default)
        
    def update_config(self, config: Dict[str, Any]):
        """Update plugin configuration"""
        self.config.update(config)
        if self._widget:
            self.on_config_changed()
            
    def on_config_changed(self):
        """Called when configuration changes"""
        pass

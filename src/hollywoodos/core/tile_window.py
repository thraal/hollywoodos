# tile_window.py
from textual.containers import Container
from textual.widget import Widget
from typing import Optional, List
from ..core.config_manager import ConfigManager, WindowConfig, PluginConfig
from ..plugins.registry import PluginRegistry
from ..plugins.base import BlinkenPlugin
import random

class TileWindow(Container):
    """A single tile window that can host plugins"""
    
    def __init__(
        self,
        window_config: WindowConfig,
        config_manager: ConfigManager,
        plugin_registry: PluginRegistry,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.window_config = window_config
        self.config_manager = config_manager
        self.plugin_registry = plugin_registry
        
        self.plugins: List[BlinkenPlugin] = []
        self.current_plugin_index = 0
        self.current_widget: Optional[Widget] = None
        
        self._load_plugins()
        
    def _load_plugins(self):
        """Load all configured plugins"""
        for plugin_config in self.window_config.plugins:
            plugin_class = self.plugin_registry.get_plugin(plugin_config.type)
            if plugin_class:
                merged_config = self.config_manager.get_plugin_config(
                    plugin_config.type,
                    plugin_config.config
                )
                plugin = plugin_class(merged_config)
                self.plugins.append(plugin)
                
    def on_mount(self):
        """Initialize the window after mounting"""
        if self.plugins:
            self._show_current_plugin()
            
            # Start cycling if configured
            if self.window_config.cycle_interval > 0 and len(self.plugins) > 1:
                self.set_interval(
                    self.window_config.cycle_interval,
                    self._cycle_plugin
                )
        else:
            # Show placeholder
            self._show_placeholder()
            
    def _show_current_plugin(self):
        """Display the current plugin"""
        if self.current_widget:
            self.current_widget.remove()
            
        plugin = self.plugins[self.current_plugin_index]
        self.current_widget = plugin.create_widget()
        self.current_widget.add_class("plugin-widget")
        self.mount(self.current_widget)
        
    def _show_placeholder(self):
        """Show placeholder when no plugins available"""
        from textual.widgets import Static
        placeholder = Static(
            "[dim]No plugins configured[/dim]",
            classes="plugin-widget"
        )
        self.mount(placeholder)
        
    def _cycle_plugin(self):
        """Cycle to the next plugin"""
        if len(self.plugins) <= 1:
            return
            
        # Weighted random selection
        weights = [pc.weight for pc in self.window_config.plugins]
        self.current_plugin_index = random.choices(
            range(len(self.plugins)),
            weights=weights
        )[0]
        
        self._show_current_plugin()

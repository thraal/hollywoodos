from textual.widget import Widget
from textual.widgets import Static
from textual.containers import Container
from typing import List, Dict, Any
from plugin_interface import BlinkenPlugin
from config_manager import ConfigManager
import importlib

class CyclingWindow(Container):
    def __init__(self, window_config: Dict[str, Any], config_manager: ConfigManager, **kwargs):
        super().__init__(**kwargs)
        self.window_config = window_config
        self.config_manager = config_manager
        self.plugins: List[BlinkenPlugin] = []
        self.current_plugin_index = 0
        self.current_widget = None
        self.cycle_interval = window_config.get('cycle_interval', 0)
        
        self._load_plugins()
    
    def _load_plugins(self):
        """Load all plugins for this window"""
        plugin_configs = self.window_config.get('plugins', [])
        
        for plugin_config in plugin_configs:
            plugin_type = plugin_config.get('type')
            if not plugin_type:
                continue
            
            try:
                # Get merged configuration for this plugin
                merged_config = self.config_manager.get_plugin_config(
                    plugin_type, plugin_config
                )
                
                # Import and create plugin instance
                plugin_class = self._get_plugin_class(plugin_type)
                if plugin_class:
                    plugin_instance = plugin_class(merged_config)
                    self.plugins.append(plugin_instance)
            
            except Exception as e:
                print(f"Error loading plugin {plugin_type}: {e}")
    
    def _get_plugin_class(self, plugin_type: str):
        """Dynamically import and return plugin class"""
        # This is a simple mapping - you might want to make this more sophisticated
        plugin_mapping = {
            'HexScroll': 'plugins.hex_scroll.HexScroll',
            'NetworkMonitor': 'plugins.network_monitor.NetworkMonitor',
            'SystemLoad': 'plugins.system_load.SystemLoad'
        }
        
        module_path = plugin_mapping.get(plugin_type)
        if not module_path:
            return None
        
        try:
            module_name, class_name = module_path.rsplit('.', 1)
            module = importlib.import_module(module_name)
            return getattr(module, class_name)
        except Exception:
            return None
    
    def _create_current_widget(self):
        """Create widget for current plugin"""
        if not self.plugins:
            # Create a placeholder if no plugins are available
            placeholder = Static("No plugins loaded", id="placeholder")
            placeholder.styles.color = "red"
            placeholder.styles.background = "black"
            placeholder.styles.border = ("solid", "gray")
            self.mount(placeholder)
            return
        
        if self.current_widget:
            self.current_widget.remove()
        
        current_plugin = self.plugins[self.current_plugin_index]
        self.current_widget = current_plugin.create_widget()
        self._apply_styling(self.current_widget, current_plugin.config)
        self.mount(self.current_widget)
    
    def _apply_styling(self, widget: Widget, config: Dict[str, Any]):
        """Apply configuration-based styling to widget"""
        if config.get('border'):
            border_color = config.get('border_color', 'gray')
            widget.styles.border = ("solid", border_color)
        
        color = config.get('color', 'green')
        background = config.get('background', 'black')
        widget.styles.color = color
        widget.styles.background = background
        
        height = config.get('height', 5)
        widget.styles.height = height
    
    def on_mount(self):
        """Set up the widget after mounting and start cycling timer if configured"""
        self._create_current_widget()
        
        if self.cycle_interval > 0 and len(self.plugins) > 1:
            self.set_interval(self.cycle_interval, self.cycle_to_next_plugin)
    
    def cycle_to_next_plugin(self):
        """Cycle to the next plugin"""
        if len(self.plugins) <= 1:
            return
        
        self.current_plugin_index = (self.current_plugin_index + 1) % len(self.plugins)
        self._create_current_widget()
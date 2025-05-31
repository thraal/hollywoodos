# app.py
from textual.app import App

from .core.config_manager import ConfigManager
from .core.window_manager import WindowManager
from .plugins.registry import PluginRegistry

class HollywoodOS(App):
    CSS = """
    /* Ensure the WindowManager occupies the full terminal area */
    WindowManager {
        width: 100%;
        height: 100%;
    }

    /* Style each tile with a visible border */
    TileWindow {
        background: $surface;
        overflow: hidden;
        width: 100%;
        height: 100%;
        border: solid $surface-lighten-1;
    }

    /* Plugin widgets fill their tile container */
    .plugin-widget {
        width: 100%;
        height: 100%;
        overflow: hidden;
    }
    """

    def __init__(self):
        super().__init__()
        self.config_manager = ConfigManager()
        self.plugin_registry = PluginRegistry()
        self.window_manager = None

    def compose(self):
        # Mount the WindowManager so it fills all available space
        self.window_manager = WindowManager(
            self.config_manager,
            self.plugin_registry
        )
        yield self.window_manager

    def action_reload_config(self):
        self.config_manager.reload()
        if self.window_manager is not None:
            self.window_manager.reload_layout()
        self.notify("Configuration reloaded")

    # Note: split_horizontal, split_vertical, and close_window actions 
    # have been removed as they are not supported with fixed layouts
    
    # You could add new actions for switching layouts:
    def action_layout_single(self):
        """Switch to single window layout"""
        self.config_manager._layout.layout_type = "single"
        if self.window_manager is not None:
            self.window_manager.reload_layout()
        self.notify("Switched to single window layout")
        
    def action_layout_2x2(self):
        """Switch to 2x2 grid layout"""
        self.config_manager._layout.layout_type = "2x2"
        if self.window_manager is not None:
            self.window_manager.reload_layout()
        self.notify("Switched to 2x2 grid layout")
        
    def action_layout_2x2_big(self):
        """Switch to 2x2 big window layout"""
        self.config_manager._layout.layout_type = "2x2_big"
        if self.window_manager is not None:
            self.window_manager.reload_layout()
        self.notify("Switched to 2x2 big window layout")
        
    def action_layout_3x3(self):
        """Switch to 3x3 grid layout"""
        self.config_manager._layout.layout_type = "3x3"
        if self.window_manager is not None:
            self.window_manager.reload_layout()
        self.notify("Switched to 3x3 grid layout")
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

    def action_split_horizontal(self):
        if self.window_manager is not None:
            self.window_manager.split_focused_window(horizontal=True)

    def action_split_vertical(self):
        if self.window_manager is not None:
            self.window_manager.split_focused_window(horizontal=False)

    def action_close_window(self):
        if self.window_manager is not None:
            self.window_manager.close_focused_window()

# main.py
from textual.app import App
from textual.containers import Container
from textual.widgets import Header, Footer
from textual.binding import Binding
from textual.geometry import Size
from src.hollywoodos.core.config_manager import ConfigManager
from src.hollywoodos.core.window_manager import WindowManager
from src.hollywoodos.plugins.registry import PluginRegistry

class HollywoodOS(App):
    CSS = """
    WindowManager {
        dock: fill;
    }
    
    TileWindow {
        background: $surface;
        overflow: hidden;
    }
    
    TileWindow.focused {
        border: solid $primary;
    }
    
    TileWindow.unfocused {
        border: solid $surface-lighten-1;
    }
    
    .plugin-widget {
        width: 100%;
        height: 100%;
        overflow: hidden;
    }
    """
    
    BINDINGS = [
        Binding("r", "reload_config", "Reload"),
        Binding("q", "quit", "Quit"),
        Binding("tab", "focus_next", "Next Window"),
        Binding("shift+tab", "focus_previous", "Previous Window"),
        Binding("h", "split_horizontal", "Split Horizontal"),
        Binding("v", "split_vertical", "Split Vertical"),
        Binding("x", "close_window", "Close Window"),
    ]

    def __init__(self):
        super().__init__()
        self.config_manager = ConfigManager()
        self.plugin_registry = PluginRegistry()
        self.window_manager = None

    def compose(self):
        yield Header()
        self.window_manager = WindowManager(
            self.config_manager,
            self.plugin_registry
        )
        yield self.window_manager
        yield Footer()

    def action_reload_config(self):
        self.config_manager.reload()
        self.window_manager.reload_layout()
        self.notify("Configuration reloaded")

    def action_split_horizontal(self):
        self.window_manager.split_focused_window(horizontal=True)

    def action_split_vertical(self):
        self.window_manager.split_focused_window(horizontal=False)

    def action_close_window(self):
        self.window_manager.close_focused_window()

    def action_focus_next(self):
        self.window_manager.focus_next_window()

    def action_focus_previous(self):
        self.window_manager.focus_previous_window()

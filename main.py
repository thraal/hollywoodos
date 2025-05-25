from textual.app import App
from textual.containers import Grid
from textual.widgets import Header, Footer
from textual.binding import Binding
from config_manager import ConfigManager
from cycling_window import CyclingWindow

class HollywoodOS(App):
    CSS = """
    #plugin-grid {
        layout: grid;
        grid-columns: 1fr 1fr 1fr;
        grid-rows: auto auto auto;
        grid-gutter: 1;
        padding: 1;
    }
    
    CyclingWindow {
        border: solid gray;
        background: black;
        height: 10;
    }
    """
    
    BINDINGS = [
        Binding("r", "reload_config", "Reload Config"),
        Binding("q", "quit", "Quit"),
    ]

    def __init__(self):
        super().__init__()
        try:
            self.config_manager = ConfigManager()
        except Exception as e:
            print(f"Error creating ConfigManager: {e}")
            # Create a basic fallback
            self.config_manager = None

    def compose(self):
        yield Header()
        yield Grid(id="plugin-grid")
        yield Footer()

    def on_mount(self):
        if self.config_manager is None:
            print("ConfigManager not available, using defaults")
            return
        self._setup_layout()
        self._create_windows()

    def _setup_layout(self):
        """Configure grid layout based on configuration"""
        if self.config_manager is None:
            return
            
        layout_config = self.config_manager.get_layout_config()
        
        layout_type = layout_config.get('type', 'auto')
        
        if layout_type == 'grid':
            columns = layout_config.get('grid_columns', 3)
            rows = layout_config.get('grid_rows', 3)
        elif layout_type == 'auto':
            # Auto-size based on number of windows
            window_count = len(self.config_manager.get_window_configs())
            import math
            columns = math.ceil(math.sqrt(window_count))
            rows = math.ceil(window_count / columns)
        else:
            columns = 3
            rows = 3
        
        # Apply layout using individual style properties
        grid = self.query_one("#plugin-grid", Grid)
        padding = layout_config.get('padding', 1)
        gutter = layout_config.get('gutter', 1)
        
        # Set grid layout properties
        grid.styles.layout = "grid"
        grid.styles.padding = padding
        # Note: Textual uses different grid syntax - this is a simplified approach

    def _create_windows(self):
        """Create and mount all configured windows"""
        if self.config_manager is None:
            return
            
        grid = self.query_one("#plugin-grid", Grid)
        window_configs = self.config_manager.get_window_configs()
        
        for i, window_config in enumerate(window_configs):
            window_id = window_config.get('id', f'window-{i}')
            
            cycling_window = CyclingWindow(
                window_config=window_config,
                config_manager=self.config_manager,
                id=window_id
            )
            
            grid.mount(cycling_window)

    def action_reload_config(self):
        """Reload configuration and recreate layout"""
        if self.config_manager is None:
            self.notify("Configuration not available!")
            return
            
        self.config_manager.reload_config()
        
        # Clear existing windows
        grid = self.query_one("#plugin-grid", Grid)
        grid.remove_children()
        
        # Recreate layout
        self._setup_layout()
        self._create_windows()
        
        self.notify("Configuration reloaded!")

if __name__ == "__main__":
    HollywoodOS().run()
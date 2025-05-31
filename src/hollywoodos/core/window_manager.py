# window_manager.py
from textual.containers import Container
from typing import List
from .tile_window import TileWindow
from .config_manager import ConfigManager, WindowConfig
from ..plugins.registry import PluginRegistry

class WindowManager(Container):
    """Manages tiled windows with predefined layouts"""
    
    def __init__(self, config_manager: ConfigManager, plugin_registry: PluginRegistry):
        super().__init__()
        self.config_manager = config_manager
        self.plugin_registry = plugin_registry
        self.tiles: List[TileWindow] = []
        self.focused_index = 0
        
    def on_mount(self):
        """Initialize layout when mounted"""
        self.reload_layout()
        
    def reload_layout(self):
        """Reload the entire layout from config"""
        # Clear existing tiles
        for tile in self.tiles:
            tile.remove()
        self.tiles.clear()
        
        # Create layout based on type
        layout_type = self.config_manager.layout.layout_type
        
        if layout_type == "single":
            self._create_single_layout()
        elif layout_type == "2x2":
            self._create_2x2_layout()
        elif layout_type == "2x2_big":
            self._create_2x2_big_layout()
        elif layout_type == "3x3":
            self._create_3x3_layout()
        else:
            # Default to 2x2
            self._create_2x2_layout()
            
    def _get_window_configs(self, count: int) -> List[WindowConfig]:
        """Get window configs, padding with defaults if needed"""
        configs = self.config_manager.windows[:count]
        
        # Pad with defaults if not enough configs
        while len(configs) < count:
            configs.append(self.config_manager.default_window_config)
            
        return configs
        
    def _create_single_layout(self):
        """Create a single full-screen window"""
        configs = self._get_window_configs(1)
        tile = self._create_tile(configs[0])
        self.mount(tile)
        
    def _create_2x2_layout(self):
        """Create a 2x2 grid of equal-sized windows"""
        configs = self._get_window_configs(4)
        
        # Create two rows
        row1 = Container()
        row2 = Container()
        row1.styles.height = "50%"
        row1.styles.dock = "top"
        row2.styles.height = "100%"
        
        self.mount(row1, row2)
        
        # Row 1 - two columns
        tile0 = self._create_tile(configs[0])
        tile0.styles.width = "50%"
        tile0.styles.dock = "left"
        
        tile1 = self._create_tile(configs[1])
        
        row1.mount(tile0, tile1)
        
        # Row 2 - two columns
        tile2 = self._create_tile(configs[2])
        tile2.styles.width = "50%"
        tile2.styles.dock = "left"
        
        tile3 = self._create_tile(configs[3])
        
        row2.mount(tile2, tile3)
        
    def _create_2x2_big_layout(self):
        """Create 2x2 with big window top right
        Layout:
        +-----+----------+
        | 0   |    1     |
        +-----+   (big)  |
        | 2   |          |
        +-----+----------+
        |       3        |
        +----------------+
        """
        configs = self._get_window_configs(4)
        
        # Top container (66% height)
        top_container = Container()
        top_container.styles.height = "66%"
        top_container.styles.dock = "top"
        
        # Bottom container (remaining height)
        bottom_container = Container()
        
        self.mount(top_container, bottom_container)
        
        # Left column in top container (33% width)
        left_column = Container()
        left_column.styles.width = "33%"
        left_column.styles.dock = "left"
        
        top_container.mount(left_column)
        
        # Split left column into two windows
        tile0 = self._create_tile(configs[0])
        tile0.styles.height = "50%"
        tile0.styles.dock = "top"
        
        tile2 = self._create_tile(configs[2])
        
        left_column.mount(tile0, tile2)
        
        # Big window (remaining space in top container)
        tile1 = self._create_tile(configs[1])
        top_container.mount(tile1)
        
        # Bottom full-width window
        tile3 = self._create_tile(configs[3])
        bottom_container.mount(tile3)
        
    def _create_3x3_layout(self):
        """Create a 3x3 grid of equal-sized windows"""
        configs = self._get_window_configs(9)
        
        # Create three rows
        row1 = Container()
        row2 = Container()
        row3 = Container()
        
        row1.styles.height = "33.33%"
        row1.styles.dock = "top"
        row2.styles.height = "50%"
        row2.styles.dock = "top"
        row3.styles.height = "100%"
        
        self.mount(row1, row2, row3)
        
        # Row 1 - three columns
        for i in range(3):
            tile = self._create_tile(configs[i])
            if i < 2:
                tile.styles.width = "33.33%"
                tile.styles.dock = "left"
            row1.mount(tile)
            
        # Row 2 - three columns
        for i in range(3, 6):
            tile = self._create_tile(configs[i])
            if i < 5:
                tile.styles.width = "33.33%"
                tile.styles.dock = "left"
            row2.mount(tile)
            
        # Row 3 - three columns
        for i in range(6, 9):
            tile = self._create_tile(configs[i])
            if i < 8:
                tile.styles.width = "33.33%"
                tile.styles.dock = "left"
            row3.mount(tile)
    
    def _create_tile(self, window_config: WindowConfig) -> TileWindow:
        """Create a single tile window"""
        tile = TileWindow(
            window_config=window_config,
            config_manager=self.config_manager,
            plugin_registry=self.plugin_registry,
            id=window_config.id
        )
        self.tiles.append(tile)
        
        # Set focus on first tile
        if len(self.tiles) == 1:
            tile.add_class("focused")
        else:
            tile.add_class("unfocused")
            
        return tile
        
    def split_focused_window(self, horizontal: bool = True):
        """Not supported with fixed layouts"""
        self.app.notify("Window splitting is not available with fixed layouts")
        
    def close_focused_window(self):
        """Not supported with fixed layouts"""
        self.app.notify("Window closing is not available with fixed layouts")
        
    def focus_next_window(self):
        """Focus the next window"""
        if not self.tiles:
            return
            
        self.tiles[self.focused_index].remove_class("focused")
        self.tiles[self.focused_index].add_class("unfocused")
        
        self.focused_index = (self.focused_index + 1) % len(self.tiles)
        
        self.tiles[self.focused_index].remove_class("unfocused")
        self.tiles[self.focused_index].add_class("focused")
        
    def focus_previous_window(self):
        """Focus the previous window"""
        if not self.tiles:
            return
            
        self.tiles[self.focused_index].remove_class("focused")
        self.tiles[self.focused_index].add_class("unfocused")
        
        self.focused_index = (self.focused_index - 1) % len(self.tiles)
        
        self.tiles[self.focused_index].remove_class("unfocused")
        self.tiles[self.focused_index].add_class("focused")
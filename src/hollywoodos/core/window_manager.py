# window_manager.py
from textual.widget import Widget
from textual.containers import Container
from textual.reactive import reactive
from textual.geometry import Size, Region
from typing import Optional, List
from .tile_window import TileWindow
from .config_manager import ConfigManager, WindowConfig
from ..plugins.registry import PluginRegistry

class WindowManager(Container):
    """Manages tiled windows with smart splitting algorithm"""
    
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
        
        # Create initial layout
        self._create_initial_layout()
        
    def _create_initial_layout(self):
        """Create initial window layout"""
        layout = self.config_manager.layout
        window_configs = self.config_manager.windows
        
        # If no windows configured, create default
        if not window_configs:
            window_configs = [
                self.config_manager.default_window_config 
                for _ in range(layout.initial_windows)
            ]
        
        # Create tiles in a 2x2 grid for 4 windows
        if len(window_configs) == 4:
            # Create two rows
            row1 = Container()
            row2 = Container()
            
            row1.styles.width = "100%"
            row1.styles.height = "50%"
            row1.styles.dock = "top"
            
            row2.styles.width = "100%"
            row2.styles.height = "50%"
            
            self.mount(row1, row2)
            
            # Row 1 - two columns
            r1c1 = self._create_tile(window_configs[0])
            r1c1.styles.width = "50%"
            r1c1.styles.height = "100%"
            r1c1.styles.dock = "left"
            
            r1c2 = self._create_tile(window_configs[1])
            r1c2.styles.width = "100%"
            r1c2.styles.height = "100%"
            
            row1.mount(r1c1, r1c2)
            
            # Row 2 - two columns
            r2c1 = self._create_tile(window_configs[2])
            r2c1.styles.width = "50%"
            r2c1.styles.height = "100%"
            r2c1.styles.dock = "left"
            
            r2c2 = self._create_tile(window_configs[3])
            r2c2.styles.width = "100%"
            r2c2.styles.height = "100%"
            
            row2.mount(r2c1, r2c2)
        else:
            # For other counts, use recursive splitting
            self._create_tiles_balanced(window_configs)
            
    def _create_tiles_balanced(self, window_configs: List[WindowConfig]):
        """Create tiles using balanced binary splitting"""
        if not window_configs:
            return
            
        # For 1 window, use full space
        if len(window_configs) == 1:
            tile = self._create_tile(window_configs[0])
            tile.styles.width = "100%"
            tile.styles.height = "100%"
            self.mount(tile)
            return
            
        # For 2 windows, split vertically (side by side)
        if len(window_configs) == 2:
            left = self._create_tile(window_configs[0])
            right = self._create_tile(window_configs[1])
            
            left.styles.width = "50%"
            left.styles.height = "100%"
            left.styles.dock = "left"
            
            right.styles.width = "100%"
            right.styles.height = "100%"
            
            self.mount(left, right)
            return
            
        # For 3 windows, one big on left, two small on right
        if len(window_configs) == 3:
            left = self._create_tile(window_configs[0])
            left.styles.width = "50%"
            left.styles.height = "100%"
            left.styles.dock = "left"
            
            right_container = Container()
            right_container.styles.width = "100%"
            right_container.styles.height = "100%"
            
            self.mount(left, right_container)
            
            # Split right container horizontally
            top_right = self._create_tile(window_configs[1])
            bottom_right = self._create_tile(window_configs[2])
            
            top_right.styles.width = "100%"
            top_right.styles.height = "50%"
            top_right.styles.dock = "top"
            
            bottom_right.styles.width = "100%"
            bottom_right.styles.height = "50%"
            
            right_container.mount(top_right, bottom_right)
            return
            
        # For more windows, split recursively
        mid = len(window_configs) // 2
        left_configs = window_configs[:mid]
        right_configs = window_configs[mid:]
        
        # Create containers
        top_container = Container()
        bottom_container = Container()
        
        top_container.styles.width = "100%"
        top_container.styles.height = "50%"
        top_container.styles.dock = "top"
        
        bottom_container.styles.width = "100%"
        bottom_container.styles.height = "50%"
        
        self.mount(top_container, bottom_container)
        
        # Recursively create tiles
        self._create_tiles_in_container(top_container, left_configs)
        self._create_tiles_in_container(bottom_container, right_configs)
            
    def _create_tiles_in_container(self, container: Container, window_configs: List[WindowConfig]):
        """Create tiles within a specific container"""
        if len(window_configs) == 1:
            tile = self._create_tile(window_configs[0])
            tile.styles.width = "100%"
            tile.styles.height = "100%"
            container.mount(tile)
        elif len(window_configs) == 2:
            # For 2 windows, always split vertically (side by side)
            left = self._create_tile(window_configs[0])
            right = self._create_tile(window_configs[1])
            
            left.styles.width = "50%"
            left.styles.height = "100%"
            left.styles.dock = "left"
            
            right.styles.width = "100%"
            right.styles.height = "100%"
            
            container.mount(left, right)
        else:
            # For > 2, split horizontally
            mid = len(window_configs) // 2
            left_configs = window_configs[:mid]
            right_configs = window_configs[mid:]
            
            top_sub = Container()
            bottom_sub = Container()
            
            top_sub.styles.width = "100%"
            top_sub.styles.height = "50%"
            top_sub.styles.dock = "top"
            
            bottom_sub.styles.width = "100%"
            bottom_sub.styles.height = "50%"
            
            container.mount(top_sub, bottom_sub)
            
            self._create_tiles_in_container(top_sub, left_configs)
            self._create_tiles_in_container(bottom_sub, right_configs)
    
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
        """Split the currently focused window"""
        if not self.tiles or self.focused_index >= len(self.tiles):
            return
            
        focused_tile = self.tiles[self.focused_index]
        
        # Create new tile with same config
        new_config = WindowConfig(
            id=f"{focused_tile.window_config.id}_split",
            plugins=focused_tile.window_config.plugins.copy(),
            cycle_interval=focused_tile.window_config.cycle_interval
        )
        
        # This would require more complex layout management
        # For now, just notify
        self.notify("Window splitting not yet implemented in this version")
        
    def close_focused_window(self):
        """Close the currently focused window"""
        if len(self.tiles) <= 1:
            self.notify("Cannot close last window")
            return
            
        # Would need to implement proper window closing
        self.notify("Window closing not yet implemented")
        
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

# config_manager.py
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field

@dataclass
class PluginConfig:
    type: str
    config: Dict[str, Any] = field(default_factory=dict)
    weight: float = 1.0

@dataclass
class WindowConfig:
    id: str
    plugins: list[PluginConfig] = field(default_factory=list)
    cycle_interval: float = 0
    min_size: tuple[int, int] = (10, 3)

@dataclass
class LayoutConfig:
    layout_type: str = "2x2"  # single, 2x2, 2x2_big, 3x3
    border_style: str = "solid"
    focus_color: str = "$primary"
    unfocus_color: str = "$surface-lighten-1"

class ConfigManager:
    def __init__(self, config_path: str = "config/default.yaml"):
        self.config_path = Path(config_path)
        self._config = {}
        self._layout = LayoutConfig()
        self._windows = []
        self._plugin_defaults = {}
        self._global_defaults = {}
        self.load()

    def load(self):
        """Load configuration from file"""
        if not self.config_path.exists():
            # Try alternative paths
            alt_paths = [
                Path("config.yaml"),
                Path("config") / "default.yaml",
                Path.cwd() / "config" / "default.yaml",
            ]
            
            for path in alt_paths:
                if path.exists():
                    self.config_path = path
                    break
            else:
                self._create_default_config()
        
        try:
            with open(self.config_path, 'r') as f:
                self._config = yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Error loading config: {e}")
            self._create_default_config()
        
        self._parse_config()

    def _parse_config(self):
        """Parse configuration into structured objects"""
        # Layout config
        layout_data = self._config.get('layout', {})
        self._layout = LayoutConfig(
            layout_type=layout_data.get('layout_type', '2x2'),
            border_style=layout_data.get('border_style', 'solid'),
            focus_color=layout_data.get('focus_color', '$primary'),
            unfocus_color=layout_data.get('unfocus_color', '$surface-lighten-1')
        )
        
        # Global defaults
        self._global_defaults = self._config.get('defaults', {
            'refresh_rate': 0.3,
            'color_scheme': 'matrix',
            'font': 'monospace'
        })
        
        # Plugin defaults
        self._plugin_defaults = self._config.get('plugin_defaults', {})
        
        # Window configs
        self._windows = []
        for window_data in self._config.get('windows', []):
            plugins = []
            for plugin_data in window_data.get('plugins', []):
                plugins.append(PluginConfig(
                    type=plugin_data.get('type', 'HexScroll'),
                    config=plugin_data.get('config', {}),
                    weight=plugin_data.get('weight', 1.0)
                ))
            
            self._windows.append(WindowConfig(
                id=window_data.get('id', 'window'),
                plugins=plugins,
                cycle_interval=window_data.get('cycle_interval', 0),
                min_size=(
                    window_data.get('min_width', 10),
                    window_data.get('min_height', 3)
                )
            ))

    def _create_default_config(self):
        """Create default configuration"""
        default = {
            'layout': {
                'layout_type': '2x2',  # single, 2x2, 2x2_big, 3x3
                'border_style': 'solid'
            },
            'defaults': {
                'refresh_rate': 0.3,
                'color_scheme': 'matrix',
                'font': 'monospace'
            },
            'plugin_defaults': {
                'HexScroll': {
                    'refresh_rate': 0.2,
                    'columns': 16
                },
                'MatrixRain': {
                    'refresh_rate': 0.1,
                    'density': 0.1
                },
                'SystemMonitor': {
                    'refresh_rate': 1.0
                },
                'LogScroll': {
                    'refresh_rate': 0.5
                },
                'TacticalMap': {
                    'target_interval': 5.0,
                    'num_coordinates': 3
                }
            },
            'windows': [
                {
                    'id': 'map',
                    'plugins': [
                        {'type': 'TacticalMap'}
                    ]
                },
                {
                    'id': 'monitor',
                    'plugins': [
                        {'type': 'SystemMonitor'}
                    ]
                },
                {
                    'id': 'logs',
                    'plugins': [
                        {'type': 'LogScroll'}
                    ]
                },
                {
                    'id': 'data',
                    'plugins': [
                        {'type': 'HexScroll', 'config': {'color_scheme': 'amber'}}
                    ]
                }
            ]
        }
        
        # Create config directory if it doesn't exist
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.config_path, 'w') as f:
            yaml.dump(default, f, default_flow_style=False, indent=2)
        
        self._config = default

    def reload(self):
        """Reload configuration from file"""
        self.load()

    def get_plugin_config(self, plugin_type: str, instance_config: Dict[str, Any]) -> Dict[str, Any]:
        """Get merged configuration for a plugin instance"""
        config = self._global_defaults.copy()
        config.update(self._plugin_defaults.get(plugin_type, {}))
        config.update(instance_config)
        return config

    @property
    def layout(self) -> LayoutConfig:
        return self._layout

    @property
    def windows(self) -> list[WindowConfig]:
        return self._windows

    @property
    def default_window_config(self) -> WindowConfig:
        """Get a default window configuration"""
        return WindowConfig(
            id='default',
            plugins=[PluginConfig(type='HexScroll')],
            cycle_interval=0
        )
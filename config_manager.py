import yaml
from pathlib import Path
from typing import Dict, Any, List

class ConfigManager:
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        if not self.config_path.exists():
            return self._create_default_config()
        
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            return self._create_default_config()
    
    def _create_default_config(self) -> Dict[str, Any]:
        """Create default configuration"""
        default = {
            'layout': {
                'type': 'auto',
                'grid_columns': 3,
                'grid_rows': 3,
                'padding': 1,
                'gutter': 1
            },
            'defaults': {
                'refresh_rate': 0.3,
                'color': 'green',
                'background': 'black',
                'font_size': 'normal',
                'border': True,
                'border_color': 'gray',
                'random_generation': True,
                'source_file': None,
                'height': 5
            },
            'plugin_defaults': {},
            'windows': [
                {
                    'id': 'default-window',
                    'cycle_interval': 0,
                    'plugins': [
                        {
                            'type': 'HexScroll',
                            'config': {}
                        }
                    ]
                }
            ]
        }
        
        # Save default config
        self.save_config(default)
        return default
    
    def save_config(self, config: Dict[str, Any] = None):
        """Save configuration to YAML file"""
        if config is None:
            config = self.config
        
        with open(self.config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, indent=2)
    
    def reload_config(self):
        """Reload configuration from file"""
        self.config = self._load_config()
    
    def get_layout_config(self) -> Dict[str, Any]:
        """Get layout configuration"""
        return self.config.get('layout', {})
    
    def get_window_configs(self) -> List[Dict[str, Any]]:
        """Get all window configurations"""
        return self.config.get('windows', [])
    
    def get_plugin_config(self, plugin_type: str, window_config: Dict[str, Any]) -> Dict[str, Any]:
        """Get merged configuration for a specific plugin instance"""
        # Start with global defaults
        config = self.config.get('defaults', {}).copy()
        
        # Apply plugin type defaults
        plugin_defaults = self.config.get('plugin_defaults', {}).get(plugin_type, {})
        config.update(plugin_defaults)
        
        # Apply window-specific plugin config
        config.update(window_config.get('config', {}))
        
        return config
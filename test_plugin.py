#!/usr/bin/env python3
"""
Test a single plugin in fullscreen mode.
Usage: python test_plugin.py [plugin_name] [--config key=value ...]
Example: python test_plugin.py TacticalMap --config target_interval=3.0
"""

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from textual.app import App
from textual.containers import Container
from textual.widgets import Static
from src.hollywoodos.plugins.registry import PluginRegistry
from src.hollywoodos.plugins.base import BlinkenPlugin


class PluginTestApp(App):
    """Simple app to test a single plugin fullscreen"""
    
    CSS = """
    Screen {
        background: $surface;
    }
    
    Container {
        width: 100%;
        height: 100%;
        padding: 0;
        margin: 0;
    }
    
    .plugin-widget {
        width: 100%;
        height: 100%;
    }
    """
    
    from typing import Optional

    def __init__(self, plugin_name: str, config: Optional[dict] = None):
        super().__init__()
        self.plugin_name = plugin_name
        self.config = config or {}
        self.plugin_registry = PluginRegistry()
        
    def compose(self):
        plugin_class = self.plugin_registry.get_plugin(self.plugin_name)
        
        if not plugin_class:
            yield Static(f"Plugin '{self.plugin_name}' not found!\n\nAvailable plugins:\n" + 
                        "\n".join(f"  - {name}" for name in sorted(self.plugin_registry.list_plugins())))
            return
            
        # Create plugin instance
        plugin = plugin_class(self.config)
        widget = plugin.create_widget()
        widget.add_class("plugin-widget")
        
        # Create container and mount widget
        container = Container()
        yield container
        container.mount(widget)


def parse_config(args):
    """Parse command line config arguments"""
    config = {}
    i = 0
    while i < len(args):
        if args[i] == "--config" and i + 1 < len(args):
            # Parse key=value pairs
            pair = args[i + 1]
            if "=" in pair:
                key, value = pair.split("=", 1)
                # Try to parse as number
                try:
                    if "." in value:
                        config[key] = float(value)
                    else:
                        config[key] = int(value)
                except ValueError:
                    config[key] = value
            i += 2
        else:
            i += 1
    return config


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print(__doc__)
        # List available plugins
        registry = PluginRegistry()
        print("\nAvailable plugins:")
        for name in sorted(registry.list_plugins()):
            print(f"  - {name}")
        sys.exit(1)
        
    plugin_name = sys.argv[1]
    config = parse_config(sys.argv[2:])
    
    app = PluginTestApp(plugin_name, config)
    app.run()


if __name__ == "__main__":
    main()
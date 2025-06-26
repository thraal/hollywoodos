#!/usr/bin/env python3
"""
Run HollywoodOS directly without installation.

Usage:
    python run.py                           # Normal mode with config file
    python run.py --test-plugin PLUGIN      # Test a single plugin fullscreen
    python run.py --test-plugin PLUGIN --plugin-config key=value key2=value2
    python run.py --list-plugins            # List available plugins
"""

import sys
import argparse
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))


def parse_plugin_config(config_args):
    """Parse plugin configuration from command line arguments"""
    config = {}
    for arg in config_args:
        if '=' in arg:
            key, value = arg.split('=', 1)
            # Try to parse as number
            try:
                if '.' in value:
                    config[key] = float(value)
                else:
                    config[key] = int(value)
            except ValueError:
                # Keep as string if not a number
                config[key] = value
        else:
            print(f"Warning: Ignoring invalid config '{arg}' (expected key=value)")
    return config


def test_plugin_mode(plugin_name, plugin_config):
    """Run in plugin test mode"""
    from textual.app import App
    from textual.widgets import Static
    from src.hollywoodos.plugins.registry import PluginRegistry
    
    class PluginTestApp(App):
        """Simple app to test a single plugin fullscreen"""
        
        CSS = """
        Screen {
            background: $surface;
        }
        
        .plugin-widget {
            width: 100%;
            height: 100%;
            padding: 0;
            margin: 0;
        }
        """
        
        def __init__(self, plugin_name, config):
            super().__init__()
            self.plugin_name = plugin_name
            self.config = config
            self.plugin_registry = PluginRegistry()
            
        def compose(self):
            plugin_class = self.plugin_registry.get_plugin(self.plugin_name)
            
            if not plugin_class:
                yield Static(
                    f"Plugin '{self.plugin_name}' not found!\n\n"
                    f"Available plugins:\n" + 
                    "\n".join(f"  - {name}" for name in sorted(self.plugin_registry.list_plugins()))
                )
                return
                
            # Create plugin instance
            plugin = plugin_class(self.config)
            widget = plugin.create_widget()
            widget.add_class("plugin-widget")
            
            # Yield the widget directly
            yield widget
    
    app = PluginTestApp(plugin_name, plugin_config)
    app.run()


def list_plugins():
    """List all available plugins"""
    from src.hollywoodos.plugins.registry import PluginRegistry
    
    registry = PluginRegistry()
    print("Available plugins:")
    for name in sorted(registry.list_plugins()):
        print(f"  - {name}")
        
    # Show some examples
    print("\nExamples:")
    print("  python run.py --test-plugin TacticalMap")
    print("  python run.py --test-plugin SystemMonitor")
    print("  python run.py --test-plugin HexScroll --plugin-config color_scheme=amber")
    print("  python run.py --test-plugin MatrixRain --plugin-config density=0.2")


def main():
    """Main entry point with argument parsing"""
    parser = argparse.ArgumentParser(
        description="HollywoodOS - Terminal-based cinematic computer activity simulator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run.py                    # Run normally with config file
  python run.py --test-plugin TacticalMap
  python run.py --test-plugin TacticalMap --plugin-config target_interval=2.0 num_coordinates=5
  python run.py --list-plugins     # Show available plugins
        """
    )
    
    parser.add_argument(
        '--config', 
        default='config/default.yaml',
        help='Path to configuration file (default: config/default.yaml)'
    )
    
    parser.add_argument(
        '--test-plugin',
        metavar='PLUGIN',
        help='Test a single plugin in fullscreen mode'
    )
    
    parser.add_argument(
        '--plugin-config',
        nargs='*',
        default=[],
        help='Plugin configuration as key=value pairs'
    )
    
    parser.add_argument(
        '--list-plugins',
        action='store_true',
        help='List all available plugins and exit'
    )
    
    args = parser.parse_args()
    
    # Handle list plugins
    if args.list_plugins:
        list_plugins()
        sys.exit(0)
    
    # Handle test plugin mode
    if args.test_plugin:
        plugin_config = parse_plugin_config(args.plugin_config)
        test_plugin_mode(args.test_plugin, plugin_config)
        sys.exit(0)
    
    # Normal mode - run the full app
    from src.hollywoodos.app import HollywoodOS
    app = HollywoodOS()
    app.run()


if __name__ == "__main__":
    main()

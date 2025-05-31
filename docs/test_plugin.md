# Plugin Test Program

## Usage

Test a single plugin in fullscreen mode:

```bash
# Basic usage
python test_plugin.py <plugin_name>

# With custom configuration
python test_plugin.py <plugin_name> --config key=value --config key2=value2
```

## Examples

```bash
# Test TacticalMap with default settings
python test_plugin.py TacticalMap

# Test with faster target switching
python test_plugin.py TacticalMap --config target_interval=2.0

# Test with more coordinates
python test_plugin.py TacticalMap --config num_coordinates=5 --config target_interval=3.0

# Test other plugins
python test_plugin.py SystemMonitor
python test_plugin.py HexScroll --config color_scheme=amber
python test_plugin.py MatrixRain --config density=0.2
python test_plugin.py LogScroll --config refresh_rate=0.3
```

## Available Plugins

Run without arguments to see all available plugins:

```bash
python test_plugin.py
```

## Features

- Runs a single plugin in fullscreen
- Allows passing configuration parameters via command line
- Automatically converts numeric values (integers and floats)
- Shows available plugins if an invalid plugin name is provided

## Keyboard Shortcuts

- `q` or `Ctrl+C` - Quit the test program
# Running HollywoodOS

## Quick Start

### Method 1: Direct Run (No Installation)
```bash
python run.py
```

### Method 2: Run as Module
```bash
python -m src.hollywoodos
```

### Method 3: Install and Run
```bash
# Install in development mode
pip install -e .

# Then run
hollywoodos
```

## Requirements
- Python 3.11 or later
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

## Troubleshooting

### Import Errors
If you get import errors, make sure you:
1. Installed the requirements: `pip install -r requirements.txt`
2. Are running from the project root directory
3. Have Python 3.11 or later

### Config File Not Found
The app will create a default config if none exists. You can also manually create `config/default.yaml` or `config.yaml` in the project root.

### No Plugins Loading
Make sure the plugin files are in the correct location under `src/hollywoodos/plugins/builtin/`

## Controls
- `Tab` / `Shift+Tab` - Navigate between windows
- `r` - Reload configuration
- `q` - Quit
- `h` - Split window horizontally (not fully implemented)
- `v` - Split window vertically (not fully implemented)
- `x` - Close window (not fully implemented)
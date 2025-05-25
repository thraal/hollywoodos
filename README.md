# HollywoodOS

A retro-inspired terminal-based operating system simulation built with Textual and Python.

## Features

- Modular plugin system: extend functionality with built-in and third-party plugins such as System Monitor and Log Scroller.
- Themed interface: customizable color schemes and layouts defined in a CSS-like DSL.
- Configurable: settings loaded from `config.yaml` and override via environment variables.
- Cross-platform: tested on Windows, macOS, and Linux.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/thraal/hollywoodos.git
   cd hollywoodos
   ```
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux
   .venv\Scripts\activate     # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Quick Start

Run the application from the project root:
```bash
python run.py
```

Refer to the Running guide for advanced options and troubleshooting.

## Project Structure

```
hollywoodos/
├── src/hollywoodos/     # Application source code
├── docs/                # Documentation: usage, architecture, plugins
├── README.md
├── RUNNING.md           # Running instructions and flags
├── requirements.txt
└── config.yaml.example
```

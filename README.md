# HollywoodOS

A retro-inspired terminal-based cinematic computer activity simulator.

![alt text](<hollywoodos.gif>)

## Features

- Modular plugin system: extend functionality with built-in and third-party plugins such as System Monitor and Log Scroller.
- Themed interface: customizable color schemes and layouts defined in a CSS-like DSL.
- Configurable: settings stored in yaml config file.
- Cross-platform: Linux, Windows, macos.

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

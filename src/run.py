#!/usr/bin/env python3
"""
Run HollywoodOS directly without installation.
"""

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Import and run the app
from hollywoodos.app import HollywoodOS

if __name__ == "__main__":
    app = HollywoodOS()
    app.run()
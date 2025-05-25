#!/usr/bin/env python3
"""HollywoodOS entry point."""

from .app import HollywoodOS

def main():
    """Main entry point."""
    app = HollywoodOS()
    app.run()

if __name__ == "__main__":
    main()
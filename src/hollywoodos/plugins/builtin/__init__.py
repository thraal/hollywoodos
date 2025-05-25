# src/hollywoodos/plugins/builtin/__init__.py
"""Built-in plugins for HollywoodOS."""

# Lazy loading approach - only import when needed
def get_builtin_plugins():
    """Get dictionary of all built-in plugins."""
    from .hex_scroll import HexScroll
    from .matrix_rain import MatrixRain
    from .system_monitor import SystemMonitor
    from .log_scroll import LogScroll
    from .network_monitor import NetworkMonitor
    
    return {
        "HexScroll": HexScroll,
        "MatrixRain": MatrixRain,
        "SystemMonitor": SystemMonitor,
        "LogScroll": LogScroll,
        "NetworkMonitor": NetworkMonitor,
    }
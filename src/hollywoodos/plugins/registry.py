# plugin_registry.py
import importlib
import importlib.util
import inspect
from pathlib import Path
from typing import Dict, Type, Optional, List
from .base import BlinkenPlugin

class PluginRegistry:
    """Central registry for all available plugins"""
    
    def __init__(self):
        self._plugins: Dict[str, Type[BlinkenPlugin]] = {}
        self._scan_plugins()
        
    def _scan_plugins(self):
        """Scan for all available plugins"""
        # Built-in plugins
        self._register_builtin_plugins()
        
        # Scan plugins directory
        plugin_dir = Path("plugins")
        if plugin_dir.exists():
            for file in plugin_dir.glob("*.py"):
                if file.name.startswith("_"):
                    continue
                self._load_plugin_file(file)
                
    def _register_builtin_plugins(self):
        """Register built-in plugins"""
        # Import built-in plugins
        try:
            from .builtin.hex_scroll import HexScroll
            from .builtin.matrix_rain import MatrixRain
            from .builtin.system_monitor import SystemMonitor
            from .builtin.log_scroll import LogScroll
            from .builtin.network_monitor import NetworkMonitor
            
            self.register("HexScroll", HexScroll)
            self.register("MatrixRain", MatrixRain)
            self.register("SystemMonitor", SystemMonitor)
            self.register("LogScroll", LogScroll)
            self.register("NetworkMonitor", NetworkMonitor)
        except ImportError:
            pass
            
    def _load_plugin_file(self, file: Path):
        """Load a plugin from a file"""
        try:
            spec = importlib.util.spec_from_file_location(file.stem, file)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Find all plugin classes in the module
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if issubclass(obj, BlinkenPlugin) and obj != BlinkenPlugin:
                        self.register(name, obj)
        except Exception as e:
            print(f"Error loading plugin {file}: {e}")
            
    def register(self, name: str, plugin_class: Type[BlinkenPlugin]):
        """Register a plugin class"""
        self._plugins[name] = plugin_class
        
    def get_plugin(self, name: str) -> Optional[Type[BlinkenPlugin]]:
        """Get a plugin class by name"""
        return self._plugins.get(name)
        
    def list_plugins(self) -> List[str]:
        """List all available plugin names"""
        return list(self._plugins.keys())
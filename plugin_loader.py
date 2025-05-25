import importlib.util
import pathlib
from plugin_interface import BlinkenPlugin

def load_plugins(folder: str):
    plugins = []
    for path in pathlib.Path(folder).glob("*.py"):
        try:
            spec = importlib.util.spec_from_file_location(path.stem, path)
            if not spec or not spec.loader:
                continue
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            for attr in dir(mod):
                obj = getattr(mod, attr)
                if (
                    isinstance(obj, type)
                    and issubclass(obj, BlinkenPlugin)
                    and obj is not BlinkenPlugin
                ):
                    plugins.append(obj())
        except Exception as e:
            print(f"Failed to load plugin {path.name}: {e}")
    return plugins
from textual.widgets import Static
from textual.reactive import reactive
from textual.widget import Widget
from plugin_interface import BlinkenPlugin
import random
import pathlib

class ScrollingHex(Widget):
    lines = reactive([])

    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        self.config = config
        self.source_lines = []
        self.line_index = 0
        
        # Load source file if specified
        source_file = self.config.get('source_file')
        if source_file and not self.config.get('random_generation', True):
            self._load_source_file(source_file)
        
        # Initialize lines
        lines_count = self.config.get('lines_count', 8)
        self.lines = self._generate_initial_lines(lines_count)

    def _load_source_file(self, source_file):
        """Load hex data from source file"""
        try:
            path = pathlib.Path(source_file)
            if path.exists():
                with open(path, 'r') as f:
                    self.source_lines = [line.strip() for line in f.readlines() if line.strip()]
        except Exception as e:
            print(f"Error loading source file {source_file}: {e}")

    def _generate_initial_lines(self, count):
        """Generate initial hex lines"""
        if self.source_lines and not self.config.get('random_generation', True):
            # Use source file
            return self.source_lines[:count]
        else:
            # Generate random hex
            return [self._generate_random_hex() for _ in range(count)]

    def _generate_random_hex(self):
        """Generate a random hex line"""
        hex_pairs = []
        for _ in range(8):  # 8 hex pairs per line
            hex_pairs.append(f"{random.randint(0, 255):02X}")
        return " ".join(hex_pairs)

    def on_mount(self):
        refresh_rate = self.config.get('refresh_rate', 0.3)
        self.set_interval(refresh_rate, self.scroll_line)

    def scroll_line(self):
        if self.source_lines and not self.config.get('random_generation', True):
            # Cycle through source file lines
            self.line_index = (self.line_index + 1) % len(self.source_lines)
            new_lines = self.lines[1:] + [self.source_lines[self.line_index]]
        else:
            # Generate new random line
            new_lines = self.lines[1:] + [self._generate_random_hex()]
        
        self.lines = new_lines

    def render(self) -> str:
        return "\n".join(self.lines)

class HexScroll(BlinkenPlugin):
    def create_widget(self):
        return ScrollingHex(
            config=self.config,
            id=f"hex-scroll-{id(self)}"
        )
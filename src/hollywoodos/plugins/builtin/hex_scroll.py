# plugins/hex_scroll.py
from textual.widgets import Static
from textual.reactive import reactive
from src.hollywoodos.plugins.base import BlinkenPlugin
from src.hollywoodos.plugins.effects import EffectRegistry
import random
import math

class HexScrollWidget(Static):
    """Scrolling hexadecimal display"""
    
    lines = reactive([])
    
    def __init__(self, config: Dict[str, Any], **kwargs):
        super().__init__(**kwargs)
        self.config = config
        self.effect_registry = EffectRegistry()
        self.frame = 0
        
        # Initialize lines
        self.line_count = 0
        self.column_count = self.config.get('columns', 16)
        self.lines = []
        
    def on_mount(self):
        """Start scrolling when mounted"""
        # Calculate how many lines we can fit
        self.line_count = self.size.height
        self.column_count = min(self.config.get('columns', 16), self.size.width // 3)
        
        # Initialize with random data
        self.lines = [self._generate_hex_line() for _ in range(self.line_count)]
        
        # Start animation
        refresh_rate = self.config.get('refresh_rate', 0.2)
        self.set_interval(refresh_rate, self._update)
        
    def on_resize(self):
        """Handle resize events"""
        new_line_count = self.size.height
        new_column_count = min(self.config.get('columns', 16), self.size.width // 3)
        
        if new_line_count != self.line_count or new_column_count != self.column_count:
            self.line_count = new_line_count
            self.column_count = new_column_count
            
            # Adjust lines
            while len(self.lines) < self.line_count:
                self.lines.append(self._generate_hex_line())
            self.lines = self.lines[:self.line_count]
            
    def _generate_hex_line(self) -> str:
        """Generate a line of hex values"""
        values = []
        for _ in range(self.column_count):
            values.append(f"{random.randint(0, 255):02X}")
        return " ".join(values)
        
    def _update(self):
        """Update the display"""
        self.frame += 1
        
        # Scroll lines
        self.lines = self.lines[1:] + [self._generate_hex_line()]
        
        # Refresh display
        self.refresh()
        
    def render(self) -> str:
        """Render the hex display"""
        text = '\n'.join(self.lines)
        
        # Apply effects
        effects = self.config.get('effects', [])
        if 'glitch' in effects:
            text = self.effect_registry.apply('glitch', text, self.frame)
        if 'pulse' in effects:
            text = self.effect_registry.apply('pulse', text, self.frame)
            
        # Apply color scheme
        color_scheme = self.config.get('color_scheme', 'matrix')
        if color_scheme == 'matrix':
            text = f"[green]{text}[/green]"
        elif color_scheme == 'amber':
            text = f"[yellow]{text}[/yellow]"
        elif color_scheme == 'blue':
            text = f"[cyan]{text}[/cyan]"
            
        return text

class HexScroll(BlinkenPlugin):
    """Hexadecimal scrolling plugin"""
    
    def create_widget(self) -> Widget:
        return HexScrollWidget(self.config)

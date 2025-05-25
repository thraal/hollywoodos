# plugins/matrix_rain.py
from textual.widgets import Static
from textual.reactive import reactive
from textual.widget import Widget
from typing import Dict, Any, List
from ..base import BlinkenPlugin
import random
import math

class MatrixRainWidget(Static):
    """Matrix-style digital rain effect"""
    
    drops = reactive([])
    
    def __init__(self, config: Dict[str, Any], **kwargs):
        super().__init__(**kwargs)
        self.config = config
        self.width = 80
        self.height = 24
        self.drops = []
        self.chars = "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ0123456789"
        
    def on_mount(self):
        """Initialize the rain effect"""
        self.width = self.size.width
        self.height = self.size.height
        
        # Initialize drops
        density = self.config.get('density', 0.1)
        drop_count = int(self.width * density)
        
        self.drops = []
        for _ in range(drop_count):
            self.drops.append({
                'x': random.randint(0, self.width - 1),
                'y': random.randint(-self.height, 0),
                'speed': random.uniform(0.5, 2.0),
                'length': random.randint(5, 15),
                'chars': []
            })
            
        # Start animation
        refresh_rate = self.config.get('refresh_rate', 0.1)
        self.set_interval(refresh_rate, self._update)
        
    def on_resize(self):
        """Handle resize"""
        self.width = self.size.width
        self.height = self.size.height
        
    def _update(self):
        """Update drop positions"""
        for drop in self.drops:
            drop['y'] += drop['speed']
            
            # Reset drop if it goes off screen
            if drop['y'] - drop['length'] > self.height:
                drop['y'] = random.randint(-20, -5)
                drop['x'] = random.randint(0, self.width - 1)
                drop['speed'] = random.uniform(0.5, 2.0)
                drop['length'] = random.randint(5, 15)
                
            # Update characters
            drop['chars'] = [
                random.choice(self.chars) 
                for _ in range(drop['length'])
            ]
            
        self.refresh()
        
    def render(self) -> str:
        """Render the matrix rain"""
        # Create display buffer
        buffer = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        colors = [[0 for _ in range(self.width)] for _ in range(self.height)]
        
        # Draw drops
        for drop in self.drops:
            x = drop['x']
            
            for i, char in enumerate(drop['chars']):
                y = int(drop['y'] - i)
                if 0 <= y < self.height and 0 <= x < self.width:
                    buffer[y][x] = char
                    # Fade based on position in drop
                    if i == 0:
                        colors[y][x] = 3  # Bright white
                    elif i < 3:
                        colors[y][x] = 2  # Bright green
                    else:
                        colors[y][x] = 1  # Dim green
                        
        # Convert buffer to string with colors
        lines = []
        for y in range(self.height):
            line = ''
            for x in range(self.width):
                if colors[y][x] == 3:
                    line += f"[bold white]{buffer[y][x]}[/bold white]"
                elif colors[y][x] == 2:
                    line += f"[green]{buffer[y][x]}[/green]"
                elif colors[y][x] == 1:
                    line += f"[dim green]{buffer[y][x]}[/dim green]"
                else:
                    line += buffer[y][x]
            lines.append(line)
            
        return '\n'.join(lines)

class MatrixRain(BlinkenPlugin):
    """Matrix rain effect plugin"""
    
    def create_widget(self) -> Widget:
        return MatrixRainWidget(self.config)

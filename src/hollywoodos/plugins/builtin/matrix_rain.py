# plugins/matrix_rain.py
from textual.widgets import Static
from textual.reactive import reactive
from textual.widget import Widget
from textual.app import ComposeResult
from textual.events import Resize
from typing import Dict, Any
from ..base import BlinkenPlugin
import random


class MatrixRainWidget(Static):
    """Matrix-style digital rain effect"""
    drops = reactive([])

    def __init__(self, config: Dict[str, Any], **kwargs):
        super().__init__(**kwargs)
        self.config = config
        self.width = 0
        self.height = 0
        self.drops = []
        self.chars = (
            "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄ"  # Japanese katakana
            "ﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ"  # plus numbers below
            "0123456789"
        )

    def on_mount(self) -> None:
        """Initialize the rain effect and start updates"""
        # Build drops data for current size
        self._init_drops()
        # Schedule regular updates
        refresh_rate = self.config.get('refresh_rate', 0.1)
        self.set_interval(refresh_rate, self._update)
        # Draw the first frame immediately
        self._update()

    def on_resize(self, event: Resize) -> None:
        """Reinitialize drops when the widget is resized"""
        self._init_drops()

    def _init_drops(self) -> None:
        """Initialize or reinitialize drop positions based on width/height"""
        self.width = self.size.width
        self.height = self.size.height
        density = self.config.get('density', 0.1)
        drop_count = max(1, int(self.width * density))
        self.drops = []
        for _ in range(drop_count):
            self.drops.append({
                'x': random.randint(0, max(0, self.width - 1)),
                'y': random.uniform(-self.height, 0),
                'speed': random.uniform(0.5, 2.0),
                'length': random.randint(5, 15),
                'chars': []
            })

    def _update(self) -> None:
        """Update drop positions and characters"""
        for drop in self.drops:
            drop['y'] += drop['speed']
            if drop['y'] - drop['length'] > self.height:
                drop['y'] = random.uniform(-self.height, 0)
                drop['x'] = random.randint(0, max(0, self.width - 1))
                drop['speed'] = random.uniform(0.5, 2.0)
                drop['length'] = random.randint(5, 15)
            # Generate new chars
            drop['chars'] = [random.choice(self.chars) for _ in range(drop['length'])]
        # Trigger a render
        self.refresh()

    def render(self) -> str:
        """Render the current rain frame as a text buffer"""
        buffer = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        colors = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for drop in self.drops:
            x = int(drop['x'])
            for i, char in enumerate(drop['chars']):
                y = int(drop['y'] - i)
                if 0 <= y < self.height and 0 <= x < self.width:
                    buffer[y][x] = char
                    if i == 0:
                        colors[y][x] = 3  # brightest
                    elif i < 3:
                        colors[y][x] = 2  # bright
                    else:
                        colors[y][x] = 1  # dim
        # Build lines with markup
        lines = []
        for y in range(self.height):
            line = ''
            for x in range(self.width):
                c = buffer[y][x]
                col = colors[y][x]
                if col == 3:
                    line += f"[bold white]{c}[/bold white]"
                elif col == 2:
                    line += f"[green]{c}[/green]"
                elif col == 1:
                    line += f"[dim green]{c}[/dim green]"
                else:
                    line += ' '
            lines.append(line)
        return '\n'.join(lines)


class MatrixRain(BlinkenPlugin):
    """Matrix rain effect plugin"""

    def create_widget(self) -> Widget:
        return MatrixRainWidget(self.config)

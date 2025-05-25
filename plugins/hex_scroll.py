from textual.widgets import Static
from textual.reactive import reactive
from textual.app import ComposeResult
from textual.widget import Widget
from plugin_interface import BlinkenPlugin
import asyncio

class ScrollingHex(Widget):
    lines = reactive(["DE AD BE EF", "CA FE BA BE"])

    def on_mount(self):
        self.set_interval(0.3, self.scroll_line)

    def scroll_line(self):
        self.lines = self.lines[1:] + [self.lines[0]]
        self.refresh()

    def render(self) -> str:
        return "\n".join(self.lines)

class HexScroll(BlinkenPlugin):
    def create_widget(self):
        return ScrollingHex(id="hex-scroll")
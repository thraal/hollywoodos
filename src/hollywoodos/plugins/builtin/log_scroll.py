# src/hollywoodos/plugins/builtin/log_scroll.py

from textual.widgets import Static
from textual.reactive import reactive
from textual.widget import Widget
from typing import Dict, Any, List
from ..base import BlinkenPlugin


class LogScrollWidget(Static):
    """Scrolling log display"""

    # Declare a reactive list of strings
    logs = reactive[list[str]]([])

    def __init__(self, config: Dict[str, Any], **kwargs):
        # Disable markup so raw [ ] in logs render literally
        super().__init__(markup=False, **kwargs)
        self.config = config
        self.refresh()

    def render(self) -> str:
        """Render the logs, showing only what fits."""
        visible_lines = self.size.height
        if visible_lines <= 0:
            return ""
        # Take the last `visible_lines` entries
        visible_logs = self.logs[-visible_lines:]
        return "\n".join(visible_logs)


class LogScroll(BlinkenPlugin):
    """Log scrolling plugin"""

    def create_widget(self) -> Widget:
        return LogScrollWidget(self.config)

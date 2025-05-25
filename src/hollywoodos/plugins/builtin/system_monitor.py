# src/hollywoodos/plugins/builtin/system_monitor.py

from textual.widgets import Static
from typing import Dict, Any
from ..base import BlinkenPlugin
import random
import time


class SystemMonitorWidget(Static):
    """Fake system monitoring display"""

    def __init__(self, config: Dict[str, Any], **kwargs):
        # Disable markup parsing so [ and ] render literally
        super().__init__(markup=False, **kwargs)
        self.config = config
        self.start_time = time.time()
        self.stats = self._generate_stats()

    def _generate_stats(self) -> Dict[str, int]:
        return {
            "cpu": random.randint(0, 100),
            "memory": random.randint(0, 100),
            "network_rx": random.randint(0, 10**6),
            "network_tx": random.randint(0, 10**6),
            "disk_read": random.randint(0, 10**6),
            "disk_write": random.randint(0, 10**6),
            "processes": random.randint(1, 500),
            "threads": random.randint(1, 2000),
            "uptime": 0,
        }

    def update_stats(self) -> None:
        old = self.stats.copy()
        for key in [
            "cpu",
            "memory",
            "network_rx",
            "network_tx",
            "disk_read",
            "disk_write",
            "processes",
            "threads",
        ]:
            change = random.randint(-5, 5)
            self.stats[key] = max(0, old[key] + change)
        self.stats["uptime"] = int(time.time() - self.start_time)
        self.refresh()

    def render(self) -> str:
        self.update_stats()

        uptime = self.stats["uptime"]
        hours = uptime // 3600
        minutes = (uptime % 3600) // 60
        seconds = uptime % 60

        return f"""SYSTEM MONITOR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CPU Usage:      {self.stats['cpu']:3d}% [{'█' * (self.stats['cpu'] // 10)}{'░' * (10 - self.stats['cpu'] // 10)}]
Memory Usage:   {self.stats['memory']:3d}% [{'█' * (self.stats['memory'] // 10)}{'░' * (10 - self.stats['memory'] // 10)}]

Network:
  RX: {self.stats['network_rx']:>10,} bytes/s
  TX: {self.stats['network_tx']:>10,} bytes/s

Disk I/O:
  Read:  {self.stats['disk_read']:>10,} bytes/s
  Write: {self.stats['disk_write']:>10,} bytes/s

Processes: {self.stats['processes']:>5}
Threads:   {self.stats['threads']:>5}

Uptime: {hours:02d}:{minutes:02d}:{seconds:02d}"""


class SystemMonitor(BlinkenPlugin):
    """System monitoring plugin"""

    def create_widget(self) -> Static:
        return SystemMonitorWidget(self.config)

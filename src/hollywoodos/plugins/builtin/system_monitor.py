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

    def on_mount(self):
        """Start updating when mounted"""
        refresh_rate = self.config.get('refresh_rate', 1.0)
        self.set_interval(refresh_rate, self._update)
        self._update()

    def _generate_stats(self) -> Dict[str, Any]:
        return {
            "cpu": random.randint(0, 100),
            "memory": random.randint(0, 100),
            "network_rx": random.randint(0, 10**6),
            "network_tx": random.randint(0, 10**6),
            "disk_read": random.randint(0, 10**6),
            "disk_write": random.randint(0, 10**6),
            "processes": random.randint(100, 500),
            "threads": random.randint(1000, 3000),
            "load_avg": [random.uniform(0, 4), random.uniform(0, 4), random.uniform(0, 4)],
            "swap": random.randint(0, 100),
            "temp": random.randint(30, 80),
        }

    def _update(self) -> None:
        """Update stats with realistic variations"""
        old = self.stats.copy()
        
        # CPU and memory change gradually
        for key in ["cpu", "memory", "swap"]:
            change = random.randint(-10, 10)
            self.stats[key] = max(0, min(100, old[key] + change))
            
        # Network and disk can spike
        for key in ["network_rx", "network_tx", "disk_read", "disk_write"]:
            if random.random() < 0.1:  # 10% chance of spike
                self.stats[key] = random.randint(0, 10**7)
            else:
                change = random.randint(-10**5, 10**5)
                self.stats[key] = max(0, old[key] + change)
                
        # Process counts change slowly
        for key in ["processes", "threads"]:
            change = random.randint(-20, 20)
            self.stats[key] = max(1, old[key] + change)
            
        # Load average changes smoothly
        self.stats["load_avg"] = [
            max(0, old["load_avg"][i] + random.uniform(-0.5, 0.5))
            for i in range(3)
        ]
        
        # Temperature changes slowly
        self.stats["temp"] = max(20, min(90, old["temp"] + random.randint(-2, 2)))
        
        self.refresh()

    def render(self) -> str:
        """Render dynamically sized display"""
        width = self.size.width
        height = self.size.height
        
        if width < 30 or height < 10:
            return "Window too small"
            
        # Calculate dynamic widths
        bar_width = max(10, min(40, width - 30))
        value_width = 6
        
        uptime = int(time.time() - self.start_time)
        hours = uptime // 3600
        minutes = (uptime % 3600) // 60
        seconds = uptime % 60
        
        # Build lines
        lines = []
        
        # Title
        title = "SYSTEM MONITOR"
        lines.append(title.center(width))
        lines.append("━" * width)
        lines.append("")
        
        # CPU bar
        cpu_bar = self._make_bar(self.stats['cpu'], bar_width)
        lines.append(f"CPU:      {self.stats['cpu']:>3d}% {cpu_bar}")
        
        # Memory bar
        mem_bar = self._make_bar(self.stats['memory'], bar_width)
        lines.append(f"Memory:   {self.stats['memory']:>3d}% {mem_bar}")
        
        # Swap bar
        swap_bar = self._make_bar(self.stats['swap'], bar_width)
        lines.append(f"Swap:     {self.stats['swap']:>3d}% {swap_bar}")
        
        lines.append("")
        
        # Load average
        load = self.stats['load_avg']
        lines.append(f"Load Average: {load[0]:.2f}, {load[1]:.2f}, {load[2]:.2f}")
        
        # Temperature
        lines.append(f"CPU Temp: {self.stats['temp']}°C")
        
        lines.append("")
        
        # Network (adaptive formatting)
        if width > 50:
            lines.append(f"Network RX: {self._format_bytes(self.stats['network_rx'])}/s    "
                        f"TX: {self._format_bytes(self.stats['network_tx'])}/s")
            lines.append(f"Disk Read:  {self._format_bytes(self.stats['disk_read'])}/s    "
                        f"Write: {self._format_bytes(self.stats['disk_write'])}/s")
        else:
            lines.append(f"Net RX: {self._format_bytes(self.stats['network_rx'])}/s")
            lines.append(f"Net TX: {self._format_bytes(self.stats['network_tx'])}/s")
            lines.append(f"Disk R: {self._format_bytes(self.stats['disk_read'])}/s")
            lines.append(f"Disk W: {self._format_bytes(self.stats['disk_write'])}/s")
        
        lines.append("")
        
        # Process info
        lines.append(f"Processes: {self.stats['processes']:>4}    Threads: {self.stats['threads']:>4}")
        
        # Uptime
        lines.append(f"Uptime: {hours:02d}:{minutes:02d}:{seconds:02d}")
        
        # Fill remaining space if needed
        while len(lines) < height - 1:
            lines.append("")
            
        # Trim if too many lines
        lines = lines[:height]
        
        return '\n'.join(lines)
    
    def _make_bar(self, percentage: int, width: int) -> str:
        """Create a progress bar"""
        filled = int(width * percentage / 100)
        empty = width - filled
        return f"[{'█' * filled}{'░' * empty}]"
    
    def _format_bytes(self, bytes_value: float) -> str:
        """Format bytes to human readable"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_value < 1024:
                return f"{bytes_value:>6.1f}{unit}"
            bytes_value /= 1024
        return f"{bytes_value:>6.1f}TB"


class SystemMonitor(BlinkenPlugin):
    """System monitoring plugin"""

    def create_widget(self) -> Static:
        return SystemMonitorWidget(self.config)

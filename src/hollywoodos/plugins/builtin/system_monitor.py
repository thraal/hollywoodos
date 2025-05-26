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
            "cache": random.randint(0, 100),
            "buffers": random.randint(0, 100),
            "kernel": random.randint(0, 100),
        }

    def _update(self) -> None:
        """Update stats with realistic variations"""
        old = self.stats.copy()
        
        # CPU and memory change gradually
        for key in ["cpu", "memory", "swap", "cache", "buffers", "kernel"]:
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
        
        # Calculate dynamic widths
        bar_width = max(10, min(40, width - 20))
        
        uptime = int(time.time() - self.start_time)
        hours = uptime // 3600
        minutes = (uptime % 3600) // 60
        seconds = uptime % 60
        
        # Build lines - we'll display as many as fit
        all_lines = []
        
        # Title
        if width >= 14:
            title = "SYSTEM MONITOR"
            all_lines.append(title.center(width))
            all_lines.append("━" * width)
        
        # CPU bar
        if width >= 20:
            cpu_bar = self._make_bar(self.stats['cpu'], bar_width)
            all_lines.append(f"CPU:      {self.stats['cpu']:>3d}% {cpu_bar}")
        
        # Memory bar
        if width >= 20:
            mem_bar = self._make_bar(self.stats['memory'], bar_width)
            all_lines.append(f"Memory:   {self.stats['memory']:>3d}% {mem_bar}")
        
        # Swap bar
        if width >= 20:
            swap_bar = self._make_bar(self.stats['swap'], bar_width)
            all_lines.append(f"Swap:     {self.stats['swap']:>3d}% {swap_bar}")
        
        # Cache bar
        if width >= 20:
            cache_bar = self._make_bar(self.stats['cache'], bar_width)
            all_lines.append(f"Cache:    {self.stats['cache']:>3d}% {cache_bar}")
        
        # Kernel bar
        if width >= 20:
            kernel_bar = self._make_bar(self.stats['kernel'], bar_width)
            all_lines.append(f"Kernel:   {self.stats['kernel']:>3d}% {kernel_bar}")
        
        # Load average
        if width >= 30:
            load = self.stats['load_avg']
            all_lines.append(f"Load: {load[0]:.2f}, {load[1]:.2f}, {load[2]:.2f}")
        
        # Temperature
        if width >= 15:
            all_lines.append(f"CPU Temp: {self.stats['temp']}°C")
        
        # Network
        if width >= 25:
            all_lines.append(f"Net RX: {self._format_bytes(self.stats['network_rx'])}/s")
            all_lines.append(f"Net TX: {self._format_bytes(self.stats['network_tx'])}/s")
        
        # Disk
        if width >= 25:
            all_lines.append(f"Disk R: {self._format_bytes(self.stats['disk_read'])}/s")
            all_lines.append(f"Disk W: {self._format_bytes(self.stats['disk_write'])}/s")
        
        # Process info
        if width >= 30:
            all_lines.append(f"Procs: {self.stats['processes']}  Threads: {self.stats['threads']}")
        
        # Uptime
        if width >= 20:
            all_lines.append(f"Up: {hours:02d}:{minutes:02d}:{seconds:02d}")
        
        # Return only lines that fit in height
        if not all_lines:
            return ""
            
        return '\n'.join(all_lines[:height])
    
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

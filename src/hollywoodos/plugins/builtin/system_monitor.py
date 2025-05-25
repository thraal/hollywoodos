# plugins/system_monitor.py
from textual.widgets import Static
from src.hollywoodos.plugins.base import BlinkenPlugin
import random
import time

class SystemMonitorWidget(Static):
    """Fake system monitoring display"""
    
    def __init__(self, config: Dict[str, Any], **kwargs):
        super().__init__(**kwargs)
        self.config = config
        self.start_time = time.time()
        self.stats = self._generate_stats()
        
    def on_mount(self):
        """Start monitoring"""
        refresh_rate = self.config.get('refresh_rate', 1.0)
        self.set_interval(refresh_rate, self._update)
        
    def _generate_stats(self) -> Dict[str, Any]:
        """Generate fake system statistics"""
        return {
            'cpu': random.randint(10, 90),
            'memory': random.randint(30, 80),
            'network_rx': random.randint(1000, 9999999),
            'network_tx': random.randint(1000, 9999999),
            'disk_read': random.randint(100, 999999),
            'disk_write': random.randint(100, 999999),
            'processes': random.randint(100, 500),
            'threads': random.randint(500, 2000),
            'uptime': int(time.time() - self.start_time)
        }
        
    def _update(self):
        """Update statistics"""
        # Smoothly change values
        old_stats = self.stats
        self.stats = self._generate_stats()
        
        # Make changes more gradual
        for key in ['cpu', 'memory']:
            if key in old_stats:
                change = (self.stats[key] - old_stats[key]) * 0.3
                self.stats[key] = int(old_stats[key] + change)
                
        self.stats['uptime'] = int(time.time() - self.start_time)
        self.refresh()
        
    def render(self) -> str:
        """Render system statistics"""
        # Format uptime
        uptime = self.stats['uptime']
        hours = uptime // 3600
        minutes = (uptime % 3600) // 60
        seconds = uptime % 60
        
        # Create display
        return f"""[bold cyan]SYSTEM MONITOR[/bold cyan]
[dim]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/dim]

[green]CPU Usage:[/green]      {self.stats['cpu']:3d}% [{'█' * (self.stats['cpu'] // 10)}{'░' * (10 - self.stats['cpu'] // 10)}]
[green]Memory Usage:[/green]   {self.stats['memory']:3d}% [{'█' * (self.stats['memory'] // 10)}{'░' * (10 - self.stats['memory'] // 10)}]

[yellow]Network:[/yellow]
  RX: {self.stats['network_rx']:>10,} bytes/s
  TX: {self.stats['network_tx']:>10,} bytes/s

[yellow]Disk I/O:[/yellow]
  Read:  {self.stats['disk_read']:>10,} bytes/s
  Write: {self.stats['disk_write']:>10,} bytes/s

[cyan]Processes:[/cyan] {self.stats['processes']:>5}
[cyan]Threads:[/cyan]   {self.stats['threads']:>5}

[dim]Uptime:[/dim] {hours:02d}:{minutes:02d}:{seconds:02d}"""

class SystemMonitor(BlinkenPlugin):
    """System monitoring plugin"""
    
    def create_widget(self) -> Widget:
        return SystemMonitorWidget(self.config)

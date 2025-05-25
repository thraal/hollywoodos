from textual.widget import Widget
from textual.reactive import reactive
from plugin_interface import BlinkenPlugin
import random
import time

class NetworkDisplay(Widget):
    content = reactive("")

    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        self.config = config
        self.interface = config.get('interface', 'eth0')
        self.start_time = time.time()

    def on_mount(self):
        refresh_rate = self.config.get('refresh_rate', 1.0)
        self.set_interval(refresh_rate, self.update_stats)

    def update_stats(self):
        """Generate fake network statistics"""
        uptime = int(time.time() - self.start_time)
        rx_bytes = random.randint(1000000, 9999999)
        tx_bytes = random.randint(500000, 5000000)
        rx_packets = random.randint(1000, 9999)
        tx_packets = random.randint(800, 8000)
        
        self.content = f"""NETWORK MONITOR - {self.interface}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Uptime: {uptime:>8}s
RX Bytes: {rx_bytes:>10}
TX Bytes: {tx_bytes:>10}
RX Packets: {rx_packets:>8}
TX Packets: {tx_packets:>8}
Status: CONNECTED"""

    def render(self) -> str:
        return self.content

class NetworkMonitor(BlinkenPlugin):
    def create_widget(self):
        return NetworkDisplay(
            config=self.config,
            id=f"network-monitor-{id(self)}"
        )
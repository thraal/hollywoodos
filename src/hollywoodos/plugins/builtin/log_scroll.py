# src/hollywoodos/plugins/builtin/log_scroll.py

from textual.widgets import Static
from textual.reactive import reactive
from textual.widget import Widget
from typing import Dict, Any, List
from ..base import BlinkenPlugin
import random
import time
from datetime import datetime


class LogScrollWidget(Static):
    """Scrolling log display"""

    def __init__(self, config: Dict[str, Any], **kwargs):
        # Disable markup so raw [ ] in logs render literally
        super().__init__(markup=False, **kwargs)
        self.config = config
        self.logs: List[str] = []
        self.log_templates = [
            "INFO: Connection established from {ip}",
            "WARNING: High memory usage detected: {percent}%",
            "ERROR: Failed to connect to database",
            "DEBUG: Processing request #{id}",
            "INFO: User {user} logged in",
            "WARNING: Disk space low on /dev/{disk}",
            "INFO: Backup completed successfully",
            "ERROR: Permission denied for file {file}",
            "INFO: Service {service} started",
            "WARNING: SSL certificate expires in {days} days",
            "DEBUG: Cache hit ratio: {ratio}%",
            "INFO: Scheduled maintenance completed",
            "ERROR: Network timeout on port {port}",
            "INFO: {count} new messages in queue",
            "WARNING: CPU temperature: {temp}°C",
            "INFO: Database optimization complete",
            "ERROR: Invalid authentication token",
            "DEBUG: Memory allocation: {size}MB",
            "INFO: System update available",
            "WARNING: Unusual activity detected from {ip}",
        ]
        
    def on_mount(self):
        """Start log generation when mounted"""
        # Generate initial logs
        for _ in range(20):
            self._add_log()
            
        # Start updating
        refresh_rate = self.config.get('refresh_rate', 0.5)
        self.set_interval(refresh_rate, self._update)
        
    def _generate_ip(self) -> str:
        """Generate random IP address"""
        return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"
    
    def _add_log(self):
        """Add a new log entry"""
        template = random.choice(self.log_templates)
        
        # Replace placeholders
        replacements = {
            "{ip}": self._generate_ip(),
            "{percent}": str(random.randint(80, 99)),
            "{id}": str(random.randint(1000, 9999)),
            "{user}": random.choice(["admin", "user1", "guest", "root", "service"]),
            "{disk}": random.choice(["sda1", "sdb2", "nvme0n1", "hda3"]),
            "{file}": random.choice(["/etc/config", "/var/log/app.log", "/tmp/data", "/home/user/file"]),
            "{service}": random.choice(["nginx", "mysql", "redis", "docker", "sshd"]),
            "{days}": str(random.randint(1, 30)),
            "{ratio}": str(random.randint(0, 100)),
            "{port}": str(random.choice([80, 443, 3306, 5432, 6379, 8080])),
            "{count}": str(random.randint(1, 100)),
            "{temp}": str(random.randint(60, 85)),
            "{size}": str(random.randint(100, 2000)),
        }
        
        log_text = template
        for placeholder, value in replacements.items():
            log_text = log_text.replace(placeholder, value)
        
        # Add timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {log_text}"
        
        self.logs.append(log_entry)
        
        # Keep only last 1000 logs
        if len(self.logs) > 1000:
            self.logs = self.logs[-1000:]
    
    def _update(self):
        """Add new log entries"""
        # Random chance of adding 0-3 new logs
        new_logs = random.choices([0, 1, 2, 3], weights=[0.3, 0.5, 0.15, 0.05])[0]
        for _ in range(new_logs):
            self._add_log()
        self.refresh()

    def render(self) -> str:
        """Render the logs, showing only what fits."""
        visible_lines = self.size.height
        if visible_lines <= 0:
            return ""
            
        # Take the last `visible_lines` entries
        visible_logs = self.logs[-visible_lines:]
        
        # If we have fewer logs than lines, pad with empty lines at top
        if len(visible_logs) < visible_lines:
            padding = [""] * (visible_lines - len(visible_logs))
            visible_logs = padding + visible_logs
            
        return "\n".join(visible_logs)


class LogScroll(BlinkenPlugin):
    """Log scrolling plugin"""

    def create_widget(self) -> Widget:
        return LogScrollWidget(self.config)

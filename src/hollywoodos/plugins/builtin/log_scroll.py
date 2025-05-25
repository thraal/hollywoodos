# plugins/log_scroll.py
from textual.widgets import Static
from textual.reactive import reactive
from textual.widget import Widget
from typing import Dict, Any, List
from ..base import BlinkenPlugin
import random
import time

class LogScrollWidget(Static):
    """Scrolling log display"""
    
    logs = reactive([])
    
    def __init__(self, config: Dict[str, Any], **kwargs):
        super().__init__(**kwargs)
        self.config = config
        self.max_lines = 100
        self.logs = []
        
        # Log templates
        self.templates = [
            "[{level}] {timestamp} - {module}: {message}",
            "{timestamp} [{level}] {module} - {message}",
            "[{timestamp}] {module}.{function}() - {level}: {message}"
        ]
        
        self.modules = [
            "core.engine", "network.handler", "auth.validator",
            "data.processor", "cache.manager", "queue.worker",
            "api.gateway", "db.connector", "security.scanner"
        ]
        
        self.messages = [
            "Connection established", "Processing request",
            "Authentication successful", "Cache updated",
            "Query executed", "Task completed",
            "Handshake initiated", "Buffer flushed",
            "Checksum verified", "Pipeline activated"
        ]
        
    def on_mount(self):
        """Start log generation"""
        # Generate initial logs
        for _ in range(min(20, self.size.height)):
            self.logs.append(self._generate_log())
            
        refresh_rate = self.config.get('refresh_rate', 0.5)
        self.set_interval(refresh_rate, self._add_log)
        
    def _generate_log(self) -> str:
        """Generate a fake log entry"""
        level = random.choice(['INFO', 'WARN', 'DEBUG', 'ERROR'])
        timestamp = time.strftime('%H:%M:%S')
        module = random.choice(self.modules)
        message = random.choice(self.messages)
        function = random.choice(['init', 'process', 'handle', 'execute'])
        
        template = random.choice(self.templates)
        log = template.format(
            level=level,
            timestamp=timestamp,
            module=module,
            message=message,
            function=function
        )
        
        # Color based on level
        if level == 'ERROR':
            return f"[red]{log}[/red]"
        elif level == 'WARN':
            return f"[yellow]{log}[/yellow]"
        elif level == 'DEBUG':
            return f"[dim]{log}[/dim]"
        else:
            return f"[green]{log}[/green]"
            
    def _add_log(self):
        """Add a new log entry"""
        self.logs.append(self._generate_log())
        
        # Keep only recent logs
        if len(self.logs) > self.max_lines:
            self.logs = self.logs[-self.max_lines:]
            
        self.refresh()
        
    def render(self) -> str:
        """Render the logs"""
        # Show only what fits in the widget
        visible_lines = self.size.height
        visible_logs = self.logs[-visible_lines:] if visible_lines > 0 else []
        return '\n'.join(visible_logs)

class LogScroll(BlinkenPlugin):
    """Log scrolling plugin"""
    
    def create_widget(self) -> Widget:
        return LogScrollWidget(self.config)

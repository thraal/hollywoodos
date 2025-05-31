# src/hollywoodos/plugins/builtin/tactical_map.py

from textual.widgets import Static
from textual.widget import Widget
from typing import Dict, Any, List, Tuple, Set
from ..base import BlinkenPlugin
import random
import time


class TacticalMapWidget(Static):
    """Tactical map display with targeting crosshairs"""

    def __init__(self, config: Dict[str, Any], **kwargs):
        super().__init__(markup=False, **kwargs)
        self.config = config
        
        # Map configuration
        self.map_width = 60
        self.map_height = 30
        self.terrain_map = []
        self.boundary_map = []  # For storing boundary characters
        self.cities = []
        
        # Targeting configuration
        self.coordinates = []
        self.current_target_index = 0
        self.target_x = 0
        self.target_y = 0
        
        # Timing
        self.last_update = time.time()
        self.update_interval = config.get('target_interval', 5.0)
        self.num_coordinates = config.get('num_coordinates', 3)
        
        # Generate map and coordinates
        self._generate_map()
        self._generate_coordinates()
        
    def _generate_map(self):
        """Generate a realistic-looking terrain map"""
        # Initialize with water (0)
        self.terrain_map = [[0 for _ in range(self.map_width)] for _ in range(self.map_height)]
        
        # Add main continent with irregular shape
        self._add_landmass(20, 15, 30, 20)
        
        # Add islands
        self._add_landmass(45, 8, 12, 10)   # Eastern island
        self._add_landmass(8, 22, 10, 6)    # Southern island
        self._add_landmass(50, 20, 8, 6)    # Small eastern island
        
        # Add cities at strategic locations
        self.cities = [
            (18, 10, 'ALPHA'),
            (28, 18, 'BRAVO'),
            (45, 8, 'CHARLIE'),
            (10, 22, 'DELTA'),
            (35, 14, 'ECHO'),
            (22, 20, 'FOXTROT'),
            (50, 20, 'GOLF'),
        ]
        
        # Calculate boundaries
        self._calculate_boundaries()
        
    def _add_landmass(self, x: int, y: int, width: int, height: int):
        """Add a landmass with organic shape"""
        # Use multiple overlapping circles for more organic shapes
        for _ in range(3):
            cx = x + random.randint(-width//4, width//4)
            cy = y + random.randint(-height//4, height//4)
            
            for dy in range(max(0, cy - height//2), min(self.map_height, cy + height//2)):
                for dx in range(max(0, cx - width//2), min(self.map_width, cx + width//2)):
                    # Elliptical distance for more natural shapes
                    dist_x = abs(dx - cx) / (width/2)
                    dist_y = abs(dy - cy) / (height/2)
                    dist = (dist_x**2 + dist_y**2)**0.5
                    
                    if dist < 1 + random.uniform(-0.3, 0.1):
                        self.terrain_map[dy][dx] = 1  # 1 = land
    
    def _calculate_boundaries(self):
        """Calculate boundary characters for landmasses"""
        self.boundary_map = [[' ' for _ in range(self.map_width)] for _ in range(self.map_height)]
        
        for y in range(self.map_height):
            for x in range(self.map_width):
                if self.terrain_map[y][x] == 1:  # Land
                    # Check all 8 neighbors
                    neighbors = self._get_neighbors(x, y)
                    
                    # If any neighbor is water, this is a boundary
                    if any(self.terrain_map[ny][nx] == 0 for nx, ny in neighbors if 0 <= nx < self.map_width and 0 <= ny < self.map_height):
                        self.boundary_map[y][x] = self._get_boundary_char(x, y)
    
    def _get_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        """Get all 8 neighboring coordinates"""
        return [
            (x-1, y-1), (x, y-1), (x+1, y-1),
            (x-1, y),             (x+1, y),
            (x-1, y+1), (x, y+1), (x+1, y+1)
        ]
    
    def _get_boundary_char(self, x: int, y: int) -> str:
        """Determine the appropriate box drawing character for a boundary"""
        # Check 4-way connectivity
        n = y > 0 and self.terrain_map[y-1][x] == 1
        s = y < self.map_height-1 and self.terrain_map[y+1][x] == 1
        e = x < self.map_width-1 and self.terrain_map[y][x+1] == 1
        w = x > 0 and self.terrain_map[y][x-1] == 1
        
        # Check diagonals
        ne = x < self.map_width-1 and y > 0 and self.terrain_map[y-1][x+1] == 1
        nw = x > 0 and y > 0 and self.terrain_map[y-1][x-1] == 1
        se = x < self.map_width-1 and y < self.map_height-1 and self.terrain_map[y+1][x+1] == 1
        sw = x > 0 and y < self.map_height-1 and self.terrain_map[y+1][x-1] == 1
        
        # Determine character based on connections
        if n and s and e and w:
            return '┼'
        elif n and s and e:
            return '├'
        elif n and s and w:
            return '┤'
        elif n and e and w:
            return '┴'
        elif s and e and w:
            return '┬'
        elif n and s:
            return '│'
        elif e and w:
            return '─'
        elif n and e:
            return '└'
        elif n and w:
            return '┘'
        elif s and e:
            return '┌'
        elif s and w:
            return '┐'
        elif n:
            return '╵'
        elif s:
            return '╷'
        elif e:
            return '╶'
        elif w:
            return '╴'
        else:
            # Check for diagonal-only connections
            if (ne or se) and (nw or sw):
                return '─'
            elif (ne or nw) and (se or sw):
                return '│'
            else:
                return '·'
    
    def _generate_coordinates(self):
        """Generate random target coordinates on land"""
        self.coordinates = []
        attempts = 0
        while len(self.coordinates) < self.num_coordinates and attempts < 100:
            x = random.randint(5, self.map_width - 5)
            y = random.randint(5, self.map_height - 5)
            # Only target land areas
            if self.terrain_map[y][x] == 1:
                self.coordinates.append((x, y))
            attempts += 1
            
        # Set initial target
        if self.coordinates:
            self.target_x, self.target_y = self.coordinates[0]
            
    def on_mount(self):
        """Start the display updates"""
        self._resize_map()
        self.set_interval(0.1, self._update)  # Fast refresh for smooth animation
        
    def on_resize(self):
        """Handle widget resize"""
        self._resize_map()
        
    def _resize_map(self):
        """Adjust map size to fit widget"""
        # Get available space (accounting for headers and legend)
        new_width = max(40, min(80, self.size.width))
        new_height = max(15, min(35, self.size.height - 8))  # -8 for headers/legend
        
        if new_width != self.map_width or new_height != self.map_height:
            self.map_width = new_width
            self.map_height = new_height
            self._generate_map()
            self._generate_coordinates()
            
    def _update(self):
        """Update the display and cycle targets"""
        current_time = time.time()
        
        # Check if it's time to switch targets
        if current_time - self.last_update >= self.update_interval:
            self.last_update = current_time
            self.current_target_index = (self.current_target_index + 1) % len(self.coordinates)
            self.target_x, self.target_y = self.coordinates[self.current_target_index]
            
        self.refresh()
        
    def render(self) -> str:
        """Render the tactical map"""
        lines = []
        
        # Header with blinking indicator
        blink = "●" if int(time.time() * 2) % 2 else "○"
        lines.append(f"TACTICAL MAP DISPLAY - SECTOR 7G {blink}")
        lines.append("═" * self.map_width)
        
        # Coordinate display
        coord_str = f"TARGET: [{self.target_x:02d},{self.target_y:02d}]"
        status = ["TRACKING", "LOCKED", "SCANNING"][self.current_target_index % 3]
        time_to_next = self.update_interval - (time.time() - self.last_update)
        
        # Add progress bar for time to next
        progress_width = 10
        progress_filled = int((1 - time_to_next / self.update_interval) * progress_width)
        progress_bar = f"[{'█' * progress_filled}{'░' * (progress_width - progress_filled)}]"
        
        lines.append(f"{coord_str} | STATUS: {status} | NEXT: {time_to_next:.1f}s {progress_bar}")
        lines.append("─" * self.map_width)
        
        # Render map with crosshairs
        for y in range(self.map_height):
            line = []
            for x in range(self.map_width):
                # Check if this is a crosshair position
                if x == self.target_x and y == self.target_y:
                    # Animated center
                    center_chars = ['⊕', '⊗', '⊙', '◉']
                    line.append(center_chars[int(time.time() * 4) % 4])
                elif x == self.target_x:  # Vertical line (full height)
                    if abs(y - self.target_y) == 1:
                        line.append('║')  # Thick near center
                    else:
                        line.append('│')  # Thin elsewhere
                elif y == self.target_y:  # Horizontal line (full width)
                    if abs(x - self.target_x) == 1:
                        line.append('═')  # Thick near center
                    else:
                        line.append('─')  # Thin elsewhere
                else:
                    # Check for cities
                    city_char = None
                    for cx, cy, name in self.cities:
                        if x == cx and y == cy:
                            city_char = '◉'
                            break
                    
                    if city_char:
                        line.append(city_char)
                    elif self.boundary_map[y][x] != ' ':
                        # Draw boundary
                        line.append(self.boundary_map[y][x])
                    else:
                        # Empty space for both water and land
                        line.append(' ')
                        
            lines.append(''.join(line))
            
        # Legend
        lines.append("─" * self.map_width)
        lines.append("LEGEND: ◉ City │ ⊕ Target │ ─│ Crosshair │ Land boundaries shown")
        
        # City list with distances to target
        city_info = []
        for x, y, name in self.cities[:4]:
            dist = int(((x - self.target_x)**2 + (y - self.target_y)**2)**0.5)
            city_info.append(f"{name}:{dist}km")
        lines.append(f"CITIES: {' │ '.join(city_info)}")
        
        # Add target history
        if len(self.coordinates) > 1:
            prev_idx = (self.current_target_index - 1) % len(self.coordinates)
            prev_x, prev_y = self.coordinates[prev_idx]
            lines.append(f"PREV TARGET: [{prev_x:02d},{prev_y:02d}] │ TARGETS IN QUEUE: {len(self.coordinates) - 1}")
        
        return '\n'.join(lines)


class TacticalMap(BlinkenPlugin):
    """Tactical map plugin with targeting system"""

    def create_widget(self) -> Widget:
        return TacticalMapWidget(self.config)
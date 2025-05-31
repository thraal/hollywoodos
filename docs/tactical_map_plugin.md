# TacticalMap Plugin

## Overview

The TacticalMap plugin displays a fictional tactical map with targeting crosshairs that cycle through predefined coordinates. It creates a realistic-looking terrain map with cities, mountains, rivers, and forests.

## Features

- **Dynamic Terrain Generation**: Creates realistic landmasses with:
  - Water (animated wave effect)
  - Land areas
  - Mountain ranges with foothills
  - Rivers flowing from mountains
  - Forest patches
  - Strategic city placements

- **Targeting System**:
  - Crosshairs that move between coordinates
  - Animated center point
  - Status indicators (TRACKING, LOCKED, SCANNING)
  - Countdown timer with progress bar
  - Distance calculations to cities

- **Visual Elements**:
  - Enhanced ASCII symbols for better visualization
  - Animated water effects
  - Blinking status indicator
  - Double-line crosshairs near target
  - City markers with distance information

## Configuration

```yaml
plugin_defaults:
  TacticalMap:
    target_interval: 5.0    # Seconds between target changes
    num_coordinates: 3      # Number of coordinates to cycle through
```

## Usage

Add to your window configuration:

```yaml
windows:
- id: tactical_display
  plugins:
  - type: TacticalMap
    config:
      target_interval: 8.0   # Override default interval
      num_coordinates: 5     # More target locations
```

## Map Symbols

- `≈` / `~` / `≋` - Animated water
- `.` - Land
- `♠` - Forest
- `▪` - Hills
- `▲` - Mountains
- `◉` - City
- `═` / `─` - Horizontal crosshair
- `║` / `│` - Vertical crosshair
- `⊕` / `⊗` / `⊙` / `◉` - Animated target center

## Display Information

The plugin shows:
1. Current target coordinates
2. Targeting status
3. Time until next target with progress bar
4. City distances from current target
5. Previous target location
6. Number of targets in queue
# shared_effects.py
from typing import Dict, Any, List, Callable
from textual.timer import Timer
import random
import time
import math

class EffectRegistry:
    """Registry for shared visual effects"""
    
    def __init__(self):
        self._effects: Dict[str, Callable] = {}
        self._register_builtin_effects()
        
    def _register_builtin_effects(self):
        """Register built-in effects"""
        self.register("glitch", self.glitch_effect)
        self.register("wave", self.wave_effect)
        self.register("pulse", self.pulse_effect)
        self.register("matrix_fade", self.matrix_fade_effect)
        
    def register(self, name: str, effect_func: Callable):
        """Register an effect function"""
        self._effects[name] = effect_func
        
    def apply(self, name: str, text: str, frame: int = 0, **kwargs) -> str:
        """Apply an effect to text"""
        if name in self._effects:
            return self._effects[name](text, frame, **kwargs)
        return text
        
    @staticmethod
    def glitch_effect(text: str, frame: int, intensity: float = 0.1) -> str:
        """Apply glitch effect to text"""
        if random.random() > intensity:
            return text
            
        lines = text.split('\n')
        glitched_lines = []
        
        for line in lines:
            if random.random() < intensity:
                # Random character replacement
                chars = list(line)
                for i in range(len(chars)):
                    if random.random() < intensity:
                        chars[i] = random.choice('█▀▄░▒▓')
                glitched_lines.append(''.join(chars))
            else:
                glitched_lines.append(line)
                
        return '\n'.join(glitched_lines)
        
    @staticmethod
    def wave_effect(text: str, frame: int, speed: float = 0.1) -> str:
        """Apply wave effect to text"""
        lines = text.split('\n')
        waved_lines = []
        
        for i, line in enumerate(lines):
            offset = int(3 * math.sin((frame * speed + i) * 0.5))
            padding = ' ' * max(0, offset)
            waved_lines.append(padding + line)
            
        return '\n'.join(waved_lines)
        
    @staticmethod
    def pulse_effect(text: str, frame: int, speed: float = 0.1) -> str:
        """Apply pulse effect to text brightness"""
        brightness = (math.sin(frame * speed) + 1) / 2
        
        if brightness < 0.3:
            return f"[dim]{text}[/dim]"
        elif brightness < 0.7:
            return text
        else:
            return f"[bold]{text}[/bold]"
            
    @staticmethod
    def matrix_fade_effect(text: str, frame: int, speed: float = 0.05) -> str:
        """Apply matrix-style fade effect"""
        lines = text.split('\n')
        faded_lines = []
        
        for y, line in enumerate(lines):
            chars = list(line)
            for x in range(len(chars)):
                fade = (math.sin((frame * speed + x + y) * 0.3) + 1) / 2
                if fade < 0.3:
                    chars[x] = ' '
                elif fade < 0.6:
                    chars[x] = '░'
                elif fade < 0.8:
                    chars[x] = '▒'
                    
            faded_lines.append(''.join(chars))
            
        return '\n'.join(faded_lines)
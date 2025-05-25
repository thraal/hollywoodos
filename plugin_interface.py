from abc import ABC, abstractmethod
from textual.widget import Widget

class BlinkenPlugin(ABC):
    @abstractmethod
    def create_widget(self) -> Widget:
        pass

    def update(self, data: dict):
        pass  # Optional method for future use
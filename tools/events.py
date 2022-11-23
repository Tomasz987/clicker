"""Enum events collections."""
from enum import Enum


class Event(Enum):
    """Enum events for mouse listener."""
    MOVE = 1
    CLICK = 2
    SCROLL = 3

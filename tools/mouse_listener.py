"""Module to record mouse events"""
from datetime import datetime
from typing import List, Dict, Any

from pynput.mouse import Listener


class RecordMouseEvents:
    """ Class to record mouse events

    Methods:
        time(): Calculate time from start record to event
        on_move(*args): Is called when mouse is moved
        on_click(*args): Is called when mouse button is clicked
        on_scroll(args): Is called when mouse scroll is moved
        record(): Start record mouse events

    """
    def __init__(self):
        """ Record class constructor"""
        self.button_is_pressed = False
        self.events = []
        self.listener = None
        self.start_time = datetime.now()

    def time(self) -> float:
        """
        Returns (float): Calculate time from start record to event

        """
        return (datetime.now() - self.start_time).total_seconds()

    def on_move(self, *args) -> dict[str, dict[str, Any] | float]:
        """ Is called when mouse is moved

        Args:
            *args (): with mouse coordinates

        Returns (dict): with event type, coordinates and time

        """
        x, y = args

        return {
            'mouse_move': {
                'coordinate_x': x,
                'coordinate_y': y,
            },
            'wait': {'seconds': self.time()}
        }

    def on_click(self, *args) -> dict:
        """ Is called when button mouse is clicked

        Args:
            *args (): with name button and status button

        Returns (dict): with event type, coordinates, button, status and time

        """
        x, y, button, pressed = args

        return {
            'mouse_click': {str(button)},
            'wait': {'seconds': self.time()},
        }

    def on_scroll(self, *args: int) -> dict:
        """ Is called when mouse scroll is moved

        Args:
            *args (tuple): with mouse coordinates and scroll vector

        Returns (dict): with event type, coordinates, scroll vector and time

        """
        x, y, dx, dy = args

        return {
            'mouse_scroll': {
                'vector_dx': dx,
                'vector_dy': dy
            },
            'wait': {'seconds': self.time()}
        }

    def record(self) -> list:
        """Start record mouse events

        Returns (list): with recorded mouse events

        """
        with Listener(
                on_move=lambda *args: self.events.append(self.on_move(*args)),
                on_click=lambda *args: self.events.append(self.on_click(*args)),
                on_scroll=lambda *args: self.events.append(self.on_scroll(*args)),
        ) as self.listener:
            self.listener.join()

        return self.events

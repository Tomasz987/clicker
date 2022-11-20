"""Module to record mouse events"""
from datetime import datetime

from pynput.mouse import Listener


class RecordMouseEvents:
    """ Class to record mouse events

    Methods:
        time(): Calculate time from start record to event
        exit(pressed): Check if two buttons are pressed and stop record
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

    def exit(self, pressed: bool):
        """ If two buttons are pressed stop record

        Args:
            pressed (bool): button pressed status

        """
        if self.button_is_pressed:
            if pressed:
                self.listener.stop()
            if not pressed:
                self.button_is_pressed = False
        if pressed:
            self.button_is_pressed = True

    def on_move(self, *args) -> dict:
        """ Is called when mouse is moved

        Args:
            *args (): with mouse coordinates

        Returns (dict): with event type, coordinates and time

        """
        x, y = args

        return {
            'eventType': 'mouse_move',
            'coordinate': {'x': x, 'y': y},
            'time': self.time(),
        }

    def on_click(self, *args) -> dict:
        """ Is called when button mouse is clicked

        Args:
            *args (): with name button and status button

        Returns (dict): with event type, coordinates, button, status and time

        """
        x, y, button, pressed = args
        self.exit(pressed)

        return {
            'eventType': 'mouse_click',
            'coordinate': {'x': x, 'y': y},
            'button': str(button),
            'pressed': pressed,
            'time': self.time(),
        }

    def on_scroll(self, *args: int) -> dict:
        """ Is called when mouse scroll is moved

        Args:
            *args (tuple): with mouse coordinates and scrool vector

        Returns (dict): with event type, coordinates, scrool vector and time

        """
        x, y, dx, dy = args

        return {
            'eventType': 'mouse_scroll',
            'coordinate': {'x': x, 'y': y},
            'scroll_vector': {'dx': dx, 'dy': dy},
            'time': self.time(),
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

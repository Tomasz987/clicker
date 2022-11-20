"""Module to record keyboard events"""
from enum import Enum
from datetime import datetime
from pynput.keyboard import Listener


class RecordKeyboardEvents:
    """ Class to record keyboard events

    Methods:
         time(): Calculate time from start recording to event
         exit(): If together pressed "q" and "esc" button stop recording
         on_press(key): Is called when keyboard key is pressed
         on_release(key): Is called when keyboard key is released
         record(): Start record keyboard events

    """
    def __init__(self):
        """Record class constructor"""
        self.events = []
        self.listener = None
        self.pressed = {}
        self.start_time = datetime.now()

    def time(self) -> float:
        """ Returns (float): Calculate time from start recording to event

        """
        return (datetime.now() - self.start_time).total_seconds()

    def exit(self):
        """ If together pressed "q" and "esc" button stop recording"""
        if "'q'" in self.pressed and 'Key.esc' in self.pressed:
            self.listener.stop()

    def on_press(self, key: Enum) -> dict:
        """ Is called when keyboard key is pressed

        Args:
            key (Enum): pressed key

        Returns (dict): with event type, key, status and time

        """
        self.pressed[str(key)] = True
        self.exit()

        return {
            'eventType': 'keyboard_key_pressed',
            'key': str(key),
            'pressed': True,
            'time': self.time(),
        }

    def on_release(self, key: Enum) -> dict:
        """ Is called when keyboard key is released

        Args:
            key (Enum): released key

        Returns (dict): with event type, key, status and time

        """
        del self.pressed[str(key)]

        return {
            'eventType': 'keyboard_key_released',
            'key': str(key),
            'pressed': False,
            'time': self.time(),
        }

    def record(self) -> list:
        """ Start record keyboard events

        Returns (list): with recorded events

        """
        with Listener(
            on_press=lambda key: self.events.append(self.on_press(key)),
            on_release=lambda key: self.events.append(self.on_release(key)),
        ) as self.listener:
            self.listener.join()

        return self.events

"""Module for play recorded events"""
import time

from pynput.mouse import Controller as MouseController
from pynput.keyboard import Controller as KeyboardController


class PlayEvents:
    """ Class to play recorded events

    Methods:
        play(): Called to a method that responds to a specific event
        mouse_move(coordinates): Move the mouse to the given coordinates
        mouse_click(button): Click the passed button on the mouse
        mouse_scroll(scroll_vector): Move mouse scroll to the passed vector
        keyboard_key_press(key): Imitates press passed key on keyboard
        keyboard_key_release(key): Imitates release passed key on keyboard

    """
    def __init__(self, events: list):
        """ PlayEvents class constructor

        Args:
            events (list): with dict saved events

        """
        self.events = events
        self.mouse_controller = MouseController()
        self.keyboard_controller = KeyboardController()
        self.previous_time = 0
        self.options = {
            'wait': self.time_to_wait,
            'mouse_move': self.mouse_move,
            'mouse_click': self.mouse_click,
            'mouse_scroll': self.mouse_scroll,
            'keyboard_key_press': self.keyboard_key_press,
            'keyboard_key_release': self.keyboard_key_release,
        }

    def time_to_wait(self, time_since_start):
        self.previous_time = time_since_start
        time_to_wait = time_since_start - self.previous_time
        if time_to_wait > 1:
            return time_to_wait / 100
        return time_to_wait / 1000

    def play(self):
        """ Called to a method that responds to a specific event"""
        previous_time = 0
        for event in self.events:
            for event_name, options in event:
                self.options[event_name](**options)

    def mouse_move(self, coordinates: dict):
        """ Move the mouse to the given coordinates

        Args:
            coordinates (dict): Coordinates to move the mouse

        """
        current_x, current_y = self.mouse_controller.position
        x, y = coordinates['x'], coordinates['y']
        to_move_x = x - current_x
        to_move_y = y - current_y

        self.mouse_controller.move(to_move_x, to_move_y)

    def mouse_click(self, button: str):
        """ Click the passed button on the mouse

        Args:
            button (str): with name button to click

        """
        self.mouse_controller.click(eval(button))

    def mouse_scroll(self, scroll_vector: dict):
        """ Move mouse scroll to the passed vector

        Args:
            scroll_vector (dict): with scroll vector

        """
        dx, dy = scroll_vector['dx'], scroll_vector['dy']
        self.mouse_controller.scroll(dx, dy)

    def keyboard_key_press(self, key: str):
        """ Imitates press passed key on keyboard

        Args:
            key (str): key to press

        """
        self.keyboard_controller.press(eval(key))

    def keyboard_key_release(self, key: str):
        """ Imitates release passed key on keyboard

        Args:
            key (str): key to release

        """
        self.keyboard_controller.release(eval(key))

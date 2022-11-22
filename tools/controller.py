"""Module for play recorded events."""
import time

from pynput.keyboard import Controller as KeyboardController
from pynput.keyboard import Key
from pynput.mouse import Button
from pynput.mouse import Controller as MouseController


class PlayEvents:
    """Class to play recorded events.

    Methods:
        play(): Called to a method that responds to a specific event.
        mouse_move(coordinates): Move the mouse to the given coordinates.
        mouse_click(button): Click the passed button on the mouse.
        mouse_scroll(scroll_vector): Move mouse scroll to the passed vector.
        keyboard_key_press(key): Imitates press passed key on keyboard.
        keyboard_key_release(key): Imitates release passed key on keyboard.

    """
    def __init__(self, events: list):
        """PlayEvents class constructor.

        Args:
            events (list): with dict saved events.

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
        return time_to_wait + 0.1

    def play(self):
        """Called to a method that responds to a specific event."""
        previous_time = 0
        for event in self.events:
            for event_name, options in event.items():
                time.sleep(self.time_to_wait(options[1]['time']))
                self.options[event_name](**options[0])

    def mouse_move(self, coordinate_x: int, coordinate_y: int):
        """Move the mouse to the given coordinates.

        Args:
            coordinate_x (int): horizontal coordinate to move the mouse.
            coordinate_y (int): vertical coordinate to move the mouse.

        """
        current_x, current_y = self.mouse_controller.position
        to_move_x = coordinate_x - current_x
        to_move_y = coordinate_y - current_y

        self.mouse_controller.move(to_move_x, to_move_y)

    def mouse_click(self, button: str, pressed: bool):
        """Click the passed button on the mouse.

        Args:
            button (str): with name button to click.
            pressed (bool): button is pressed.

        """
        if pressed:
            self.mouse_controller.press(eval(button))
        else:
            self.mouse_controller.release(eval(button))

    def mouse_scroll(self, vector_dx: int, vector_dy: int):
        """Move mouse scroll to the passed vector.

        Args:
            vector_dx (int): horizontal scroll vector.
            vector_dy (int): vertical scroll vector.

        """

        self.mouse_controller.scroll(vector_dx, vector_dy)

    def keyboard_key_press(self, key: str):
        """Imitates press passed key on keyboard.

        Args:
            key (str): key to press.

        """
        self.keyboard_controller.press(eval(key))

    def keyboard_key_release(self, key: str):
        """Imitates release passed key on keyboard.

        Args:
            key (str): key to release.

        """
        self.keyboard_controller.release(eval(key))

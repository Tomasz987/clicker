"""Module for play recorded events"""
from time import sleep

from pynput.mouse import Button
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Controller as KeyboardController
from pynput.keyboard import Key


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
    def __init__(self, events: dict):
        """ PlayEvents class constructor

        Args:
            events (dict): with saved events

        """
        self.events = events
        self.mouse_controller = MouseController()
        self.keyboard_controller = KeyboardController()

    def play(self):
        """ Called to a method that responds to a specific event"""
        previous_time = 0
        for index, event in enumerate(self.events):
            print(event)
            if index != 0:
                previous_time = self.events[index - 1]['time']
            time = event['time'] - previous_time

            if time > 1:
                sleep(time/100)
            sleep(time/1000)
            if event['eventType'] == 'mouse_move':
                self.mouse_move(event['coordinate'])

            elif event['eventType'] == 'mouse_click':
                self.mouse_click(event['button'])

            elif event['eventType'] == 'mouse_scroll':
                self.mouse_scroll(event['scroll_vector'])

            elif event['eventType'] == 'keyboard_key_pressed':
                self.keyboard_key_press(event['key'])

            elif event['eventType'] == 'keyboard_key_released':
                self.keyboard_key_release(event['key'])

    def mouse_move(self, coordinates: tuple):
        """ Move the mouse to the given coordinates

        Args:
            coordinates (tuple): Coordinates to move the mouse

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

    def mouse_scroll(self, scroll_vector: tuple):
        """ Move mouse scroll to the passed vector

        Args:
            scroll_vector (tuple): with scroll vector

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

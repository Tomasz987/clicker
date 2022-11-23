"""App to record and play keyboard and mouse events."""
import concurrent.futures
import time

from tools.controller import PlayEvents
from tools.database import Database
from tools.mouse_listener import RecordMouseEvents
from tools.keyboard_listener import RecordKeyboardEvents


class Clicker:
    def __init__(self):
        self.mouse_future = None
        self.keyboard_future = None
        self.end_future = None
        self.mouse_listener = RecordMouseEvents()
        self.keyboard_listener = RecordKeyboardEvents()

    @staticmethod
    def _key_to_sort_evets(event):
        for k, v in event.items():
            return v[1]['time']

    def check_pressed_stop_record_keys(self):
        while not self.keyboard_future.done():
            time.sleep(0.5)
        self.mouse_listener.listener.stop()

    def record_events(self):
        """Start record events."""
        with concurrent.futures.ThreadPoolExecutor() as executor:
            self.mouse_future = executor.submit(self.mouse_listener.record)
            self.keyboard_future = executor.submit(self.keyboard_listener.record)
            self.end_future = executor.submit(self.check_pressed_stop_record_keys)
            events = self.mouse_future.result() + self.keyboard_future.result()
            events = sorted(events, key=lambda event: self._key_to_sort_evets(event))

        with Database('file.json', 'w') as database:
            database.save(events)

    @staticmethod
    def play_events():
        """Play saved events"""
        with Database('file.json', 'r') as database:
            events = database.load()

        PlayEvents(events).play()


if __name__ == "__main__":
    clicker = Clicker()
    clicker.record_events()
    time.sleep(5)
    print('go')
    clicker.play_events()


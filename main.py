"""App to record and play keyboard and mouse events"""
import concurrent.futures

from tools.controller import PlayEvents
from tools.database import Database
from tools.mouse_listener import RecordMouseEvents
from tools.keyboard_listener import RecordKeyboardEvents


def record_events():
    """Start record events"""
    with concurrent.futures.ThreadPoolExecutor() as executor:
        mouse_future = executor.submit(RecordMouseEvents().record)
        keyboard_future = executor.submit(RecordKeyboardEvents().record)
        events = mouse_future.result() + keyboard_future.result()
        events = sorted(events, key=lambda k: k['time'])

    with Database('file.json', 'w') as database:
        database.save(events)


def play_events():
    """Play saved events"""
    with Database('file.json', 'r') as database:
        events = database.load()

    PlayEvents(events).play()


if __name__ == "__main__":
    record_events()
    play_events()

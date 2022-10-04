"""App to record and play keyboard and mouse events"""
import concurrent.futures

from controller import PlayEvents
from database import Database
from mouse_listener import RecordMouseEvents
from keyboard_listener import RecordKeyboardEvents


def record_events():
    """Start record events"""
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(RecordMouseEvents().record)
        future1 = executor.submit(RecordKeyboardEvents().record)
        events = future.result() + future1.result()
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

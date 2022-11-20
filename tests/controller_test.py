"""Tests collection for controller.py module"""
import time
from unittest.mock import call

from pynput.mouse import Button
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Controller as KeyboardController

from tools.controller import PlayEvents
from tools.keys_collection import Key


FAKE_EVENTS = [
    {
        "eventType": "mouse_move",
        "coordinate": {"x": 4, "y": 3},
        "time": 0.861694
    },
    {
        "eventType": "mouse_click",
        "coordinate": {"x": 499, "y": 672},
        "button": "Button.right",
        "pressed": 'true',
        "time": 0.953724,
    },
    {
        'eventType': 'mouse_scroll',
        'coordinate': {'x': 21, 'y': 90},
        'scroll_vector': {'dx': 0, 'dy': -1},
        'time': 11.222,
    },
    {
        'eventType': 'keyboard_key_pressed',
        'key': "'q'",
        'pressed': True,
        'time': 19.001,
    },
    {
        'eventType': 'keyboard_key_released',
        'key': "'q'",
        'pressed': False,
        'time': 22.11111111,
    },
]


def test_create_object():
    """ Test check if the object is created correctly """
    controller = PlayEvents(FAKE_EVENTS)

    assert controller.events == FAKE_EVENTS
    assert isinstance(controller.mouse_controller, MouseController)
    assert isinstance(controller.keyboard_controller, KeyboardController)


def test_wait_time_between_events(mocker):
    """ Test check if the time between events is calculated correctly

    Args:
        mocker (pytest_mock): mock to catch called methods

    """
    mocker.patch.object(time, 'sleep')
    # need mock these methods because mouse is moved and keys are pressed
    mocker.patch.object(PlayEvents, 'mouse_move')
    mocker.patch.object(PlayEvents, 'mouse_click')
    mocker.patch.object(PlayEvents, 'mouse_scroll')
    mocker.patch.object(PlayEvents, 'keyboard_key_press')
    mocker.patch.object(PlayEvents, 'keyboard_key_release')
    controller = PlayEvents(FAKE_EVENTS)

    controller.play()

    previous_time = 0
    calls = []
    for event in FAKE_EVENTS:
        if event['time'] > 1:
            calls.append(call((event['time'] - previous_time) / 100))
        elif event['time'] < 1:
            calls.append(call((event['time'] - previous_time) / 1000))
        previous_time = event['time']

    time.sleep.assert_has_calls(calls)


def test_once_called_to_mouse_move(mocker):
    """ Test check if the mouse move event is called to the correct method

    Args:
        mocker (pytest_mock): mock to catch called methods

    """
    mocker.patch.object(PlayEvents, 'mouse_move')
    event = [
        {
            'eventType': 'mouse_move',
            'coordinate': {'x': 3, 'y': 2},
            'time': 22.0,
        },
    ]
    controller = PlayEvents(event)
    controller.play()

    PlayEvents.mouse_move.assert_called_once()
    PlayEvents.mouse_move.assert_called_with(event[0]['coordinate'])


def test_once_called_to_mouse_click(mocker):
    """ Test check if the mouse click event is called to the correct method

    Args:
        mocker (pytest_mock): mock to catch called methods

    """
    mocker.patch.object(PlayEvents, 'mouse_click')
    event = [
        {
            'eventType': 'mouse_click',
            'coordinate': {'x': 90, 'y': 6},
            'button': 'Button.right',
            'pressed': True,
            'time': 000.1,
        },
    ]
    controller = PlayEvents(event)

    controller.play()

    PlayEvents.mouse_click.assert_called_once()
    PlayEvents.mouse_click.assert_called_with(event[0]['button'])


def test_once_called_to_mouse_scroll(mocker):
    """ Test check if the mouse scroll event is called to the correct method

    Args:
        mocker (pytest_mock): mock to catch called methods

    """
    mocker.patch.object(PlayEvents, 'mouse_scroll')
    event = [
        {
            'eventType': 'mouse_scroll',
            'coordinate': {'x': 4, 'y': 3},
            'scroll_vector': {'dx': 0, 'dy': -1},
            'time': 0,
        },
    ]
    controller = PlayEvents(event)

    controller.play()

    PlayEvents.mouse_scroll.assert_called_once()
    PlayEvents.mouse_scroll.assert_called_with(event[0]['scroll_vector'])


def test_once_called_to_keyboard_key_press(mocker):
    """ Test check if the keyboard key press event is called to the correct method

    Args:
        mocker (pytest_mock): mock to catch called methods

    """
    mocker.patch.object(PlayEvents, 'keyboard_key_press')
    event = [
        {
            'eventType': 'keyboard_key_pressed',
            'key': Key.q.name,
            'pressed': True,
            'time': 21.88,
        },
    ]
    controller = PlayEvents(event)

    controller.play()

    PlayEvents.keyboard_key_press.assert_called_once()
    PlayEvents.keyboard_key_press.assert_called_with(event[0]['key'])


def test_once_called_to_keyboard_key_release(mocker):
    """ Test check if the keyboard key release event is called to the correct method

    Args:
        mocker (pytest_mock): mock to catch called methods

    """
    mocker.patch.object(PlayEvents, 'keyboard_key_release')
    event = [
        {
            'eventType': 'keyboard_key_released',
            'key': 'q',
            'pressed': False,
            'time': 0.122,
        },
    ]
    controller = PlayEvents(event)

    controller.play()

    PlayEvents.keyboard_key_release.assert_called_once()
    PlayEvents.keyboard_key_release.assert_called_with(event[0]['key'])


def test_mouse_move(mocker):
    """ Test check if the mouse_move method is correctly called to the controller

    Args:
        mocker (pytes_mock): mock to catch called methods

    """
    mocker.patch.object(
        MouseController,
        'position',
        new_callable=mocker.PropertyMock,
        return_value=(2, 1),
    )
    mocker.patch.object(MouseController, 'move')
    # difference in coordinates
    x, y = 2, 2
    coordinates = {"x": 4, "y": 3}
    controller = PlayEvents(FAKE_EVENTS)

    controller.mouse_move(coordinates)

    MouseController.move.assert_called_once_with(x, y)


def test_mouse_click(mocker):
    """ Test check if the mouse_click method is correctly called to the controller

    Args:
        mocker (pytes_mock): mock to catch called methods

    """
    mocker.patch.object(MouseController, 'click')
    controller = PlayEvents(FAKE_EVENTS)
    button = Button.right

    controller.mouse_click('Button.right')

    MouseController.click.assert_called_once()
    MouseController.click.assert_called_with(button)


def test_mouse_scroll(mocker):
    """ Test check if the mouse_scroll method is correctly called to the controller

    Args:
        mocker (pytes_mock): mock to catch called methods

    """
    mocker.patch.object(MouseController, 'scroll')
    controller = PlayEvents(FAKE_EVENTS)
    scroll_vector = {'dx': 0, 'dy': -1}

    controller.mouse_scroll(scroll_vector)

    MouseController.scroll.assert_called()
    MouseController.scroll.assert_called_with(0, -1)


def test_keyboard_key_press(mocker):
    """ Test check if the keyboard_key_press method is correctly called to the controller

    Args:
        mocker (pytes_mock): mock to catch called methods

    """
    mocker.patch.object(KeyboardController, 'press')
    controller = PlayEvents(FAKE_EVENTS)

    controller.keyboard_controller.press("'q'")

    KeyboardController.press.assert_called_once()
    KeyboardController.press.assert_called_with("'q'")


def test_keyboard_key_release(mocker):
    """ Test check if the keyboard_key_release method is correctly called to the controller

    Args:
        mocker (pytes_mock): mock to catch called methods

    """
    mocker.patch.object(KeyboardController, 'release')
    controller = PlayEvents(FAKE_EVENTS)

    controller.keyboard_controller.release('q')

    KeyboardController.release.assert_called_once()
    KeyboardController.release.assert_called_with('q')

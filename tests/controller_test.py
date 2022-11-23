"""Tests collection for controller.py module."""
import time
from unittest.mock import call

from pynput.mouse import Button
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Controller as KeyboardController

from tools.controller import PlayEvents
from tools.keys_collection import Key


FAKE_EVENTS = [
    {
        'mouse_move': (
            {
                'coordinate_x': 1,
                'coordinate_y': 200,
            },
            {'time': 0.87777},
        ),
    },
    {
        'mouse_click': (
            {'button': 'Button.right',
             'pressed': True},
            {'time': 0.91112},
        ),
    },
    {
        'mouse_scroll': (
            {
                'vector_dx': 0,
                'vector_dy': -1,
            },
            {'time': 12.0001},
        ),
    },
    {
        'keyboard_key_press': (
            {
                'key': "'q'",
            },
            {'time': 12.09},
        ),
    },
    {
        'keyboard_key_release': (
            {
                'key': "'q'",
            },
            {'time': 12.10},
        ),
    },
]


def test_create_object():
    """Test check if the object is created correctly."""
    controller = PlayEvents(FAKE_EVENTS)

    assert controller.events == FAKE_EVENTS
    assert isinstance(controller.mouse_controller, MouseController)
    assert isinstance(controller.keyboard_controller, KeyboardController)


def test_wait_time_between_events():
    """Test check if the time between events is calculated correctly."""
    controller = PlayEvents(FAKE_EVENTS)
    controller.previous_time = 2.1

    assert controller.time_to_wait(3.1) == 1.1


def test_once_called_to_mouse_move(mocker):
    """Test check if the mouse move event is called to the correct method.

    Args:
        mocker (pytest_mock): mock to catch called methods.

    """
    mocker.patch.object(PlayEvents, 'mouse_move')
    mocker.patch.object(PlayEvents, 'time_to_wait', return_value=0)
    event = [{
            'mouse_move': (
                {
                    'coordinate_x': 1,
                    'coordinate_y': 900,
                },
                {'time': 111.1},
            ),
        }]
    controller = PlayEvents(event)
    for case in event:
        args = case['mouse_move'][0]

    controller.play()

    PlayEvents.mouse_move.assert_called_once()
    PlayEvents.mouse_move.assert_called_with(
        coordinate_x=args['coordinate_x'],
        coordinate_y=args['coordinate_y'],
    )
    PlayEvents.time_to_wait.assert_called_once()


def test_once_called_to_mouse_click(mocker):
    """Test check if the mouse click event is called to the correct method.

    Args:
        mocker (pytest_mock): mock to catch called methods.

    """
    mocker.patch.object(PlayEvents, 'mouse_click')
    mocker.patch.object(PlayEvents, 'time_to_wait', return_value=0)
    event = [{
            'mouse_click': (
                {'button': 'Button.right',
                 'pressed': True},
                {'time': 1.001},
            ),
        }]
    controller = PlayEvents(event)
    for case in event:
        args = case['mouse_click'][0]

    controller.play()

    PlayEvents.mouse_click.assert_called_once()
    PlayEvents.mouse_click.assert_called_with(
        button=args['button'],
        pressed=args['pressed'],
    )
    PlayEvents.time_to_wait.assert_called_once()


def test_once_called_to_mouse_scroll(mocker):
    """Test check if the mouse scroll event is called to the correct method.

    Args:
        mocker (pytest_mock): mock to catch called methods.

    """
    mocker.patch.object(PlayEvents, 'mouse_scroll')
    mocker.patch.object(PlayEvents, 'time_to_wait', return_value=0)
    event = [
        {
            'mouse_scroll': (
                {
                    'vector_dx': 0,
                    'vector_dy': -1,
                },
                {'time': 0.001},
            ),
        }
    ]
    controller = PlayEvents(event)
    for case in event:
        args = case['mouse_scroll'][0]

    controller.play()

    PlayEvents.mouse_scroll.assert_called_once()
    PlayEvents.mouse_scroll.assert_called_with(
        vector_dx=0,
        vector_dy=-1,
    )
    PlayEvents.time_to_wait.assert_called_once()


def test_once_called_to_keyboard_key_press(mocker):
    """Test check if the keyboard key press event is called to the correct method.

    Args:
        mocker (pytest_mock): mock to catch called methods.

    """
    mocker.patch.object(PlayEvents, 'keyboard_key_press')
    mocker.patch.object(PlayEvents, 'time_to_wait', return_value=0)
    event = [
        {
            'keyboard_key_press': (
                {
                    'key': 'q',
                },
                {'time': 0.1},
            ),
        }
    ]
    controller = PlayEvents(event)
    for case in event:
        args = case['keyboard_key_press'][0]

    controller.play()

    PlayEvents.keyboard_key_press.assert_called_once()
    PlayEvents.keyboard_key_press.assert_called_with(
        key=args['key'])
    PlayEvents.time_to_wait.assert_called_once()


def test_once_called_to_keyboard_key_release(mocker):
    """Test check if the keyboard key release event is called to the correct method.

    Args:
        mocker (pytest_mock): mock to catch called methods.

    """
    mocker.patch.object(PlayEvents, 'keyboard_key_release')
    mocker.patch.object(PlayEvents, 'time_to_wait', return_value=0)
    event = [
        {
            'keyboard_key_release': (
                {
                    'key': "'q'",
                },
                {'time': 2.2},
            ),
        }
    ]
    controller = PlayEvents(event)
    for case in event:
        args = case['keyboard_key_release'][0]

    controller.play()

    PlayEvents.keyboard_key_release.assert_called_once()
    PlayEvents.keyboard_key_release.assert_called_with(
        key=args['key'])
    PlayEvents.time_to_wait.assert_called_once()


def test_mouse_move(mocker):
    """Test check if the mouse_move method is correctly called to the controller.

    Args:
        mocker (pytes_mock): mock to catch called methods.

    """
    mocker.patch.object(
        MouseController,
        'position',
        new_callable=mocker.PropertyMock,
        return_value=(2, 1),
    )
    mocker.patch.object(MouseController, 'move')
    # difference in coordinates:
    diff_coordinate_x = 2
    diff_coordinate_y = 2
    coordinates = {"x": 4, "y": 3}
    controller = PlayEvents(FAKE_EVENTS)

    controller.mouse_move(coordinates['x'], coordinates['y'])

    MouseController.move.assert_called_once_with(
        diff_coordinate_x,
        diff_coordinate_y,
    )


def test_mouse_button_is_released(mocker):
    """Test check if the mouse_click method is correctly called to the controller
    while mouse button is released.

    Args:
        mocker (pytes_mock): mock to catch called methods.

    """
    mocker.patch.object(MouseController, 'release')
    controller = PlayEvents(FAKE_EVENTS)
    button = Button.right

    controller.mouse_click('Button.right', False)

    MouseController.release.assert_called_once()
    MouseController.release.assert_called_with(button)


def test_mouse_button_is_pressed(mocker):
    """Test check if the mouse_click method is correctly called to the controller
    while mouse button is pressed.

    Args:
        mocker (pytes_mock): mock to catch called methods.

    """
    mocker.patch.object(MouseController, 'press')
    controller = PlayEvents(FAKE_EVENTS)
    button = Button.right

    controller.mouse_click('Button.right', True)

    MouseController.press.assert_called_once()
    MouseController.press.assert_called_with(button)


def test_mouse_scroll(mocker):
    """Test check if the mouse_scroll method is correctly called to the controller.

    Args:
        mocker (pytes_mock): mock to catch called methods.

    """
    mocker.patch.object(MouseController, 'scroll')
    controller = PlayEvents(FAKE_EVENTS)
    scroll_vector = {'dx': 0, 'dy': -1}

    controller.mouse_scroll(scroll_vector['dx'], scroll_vector['dy'])

    MouseController.scroll.assert_called()
    MouseController.scroll.assert_called_with(0, -1)


def test_keyboard_key_press(mocker):
    """Test check if the keyboard_key_press method is correctly called to the controller.

    Args:
        mocker (pytes_mock): mock to catch called methods.

    """
    mocker.patch.object(KeyboardController, 'press')
    controller = PlayEvents(FAKE_EVENTS)

    controller.keyboard_controller.press("'q'")

    KeyboardController.press.assert_called_once()
    KeyboardController.press.assert_called_with("'q'")


def test_keyboard_key_release(mocker):
    """Test check if the keyboard_key_release method is correctly called to the controller.

    Args:
        mocker (pytes_mock): mock to catch called methods.

    """
    mocker.patch.object(KeyboardController, 'release')
    controller = PlayEvents(FAKE_EVENTS)

    controller.keyboard_controller.release('q')

    KeyboardController.release.assert_called_once()
    KeyboardController.release.assert_called_with('q')

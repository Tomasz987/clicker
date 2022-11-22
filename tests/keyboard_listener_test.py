"""Test collection for mouse_listener.py."""
from datetime import datetime
from enum import Enum

from freezegun import freeze_time
from pynput.keyboard import Listener

from tools.keyboard_listener import RecordKeyboardEvents


class Keys(Enum):
    """Keys for test."""
    q = 0
    b = 1


@freeze_time('2012-12-01 09:08:07')
def test_create_object():
    """Test object is created correctly."""
    record_object = RecordKeyboardEvents()

    assert record_object.events == []
    assert record_object.listener is None
    assert record_object.pressed == {}
    assert record_object.start_time == datetime(2012, 12, 1, 9, 8, 7)


@freeze_time('2012-12-01 09:08:07')
def test_calculate_time_between_events():
    """Test calculate time between events."""
    record_object = RecordKeyboardEvents()

    freeze_time('2012-12-01 09:18:09').start()
    time = record_object.time()

    assert time == 602.0


def test_stop_record_buttons_are_pressed_together(mocker):
    """Test listener stop record when stop records buttons are pressed."""
    record_object = RecordKeyboardEvents()
    record_object.listener = Listener()
    stop_listener_mocker = mocker.patch.object(Listener, 'stop')

    record_object.pressed = {
        "'q'": True,
        "Key.esc": True
    }
    record_object.exit()

    stop_listener_mocker.assert_called_once()


def test_output_if_key_is_pressed():
    """Test output when key is pressed."""
    record_object = RecordKeyboardEvents()
    excepted_recult = {
            'eventType': 'keyboard_key_pressed',
            'key': Keys.q.name,
            'pressed': 'True',
            'time': 0.0,
    }

    result = record_object.on_press(Keys.q.name)
    assert result != excepted_recult


def test_two_buttons_are_pressed():
    """Test pressed buttons remain in memory."""
    record_object = RecordKeyboardEvents()

    record_object.on_press(Keys.q.name)
    record_object.on_press(Keys.b.name)

    print(record_object.pressed)
    assert len(record_object.pressed) == 2
    assert all([key in record_object.pressed for key in ('q', 'b')])


def test_output_key_is_released():
    """Test output when key is released."""
    record_object = RecordKeyboardEvents()
    record_object.pressed['b'] = True
    excepted_value = {
            'eventType': 'keyboard_key_released',
            'key': Keys.b.name,
            'pressed': False,
            'time': 0.0,
        }

    result = record_object.on_release(Keys.b.name)

    assert result == excepted_value


def test_one_of_the_two_keys_is_released():
    """Test one pressed key of the two is released and removed from memory."""
    record_object = RecordKeyboardEvents()
    record_object.pressed = {
        'b': True,
        't': True,
    }

    record_object.on_release(Keys.b.name)

    assert len(record_object.pressed) == 1
    assert record_object.pressed == {'t': True}

"""Test collection for mouse_listener.py """
from datetime import datetime

from freezegun import freeze_time
from pynput.mouse import Listener, Button

from tools.mouse_listener import RecordMouseEvents


@freeze_time('2012-01-01 00:00:00')
def test_create_object():
    """Test that the object was created correctly"""
    record_object = RecordMouseEvents()

    assert record_object.button_is_pressed is False
    assert record_object.events == []
    assert record_object.listener is None
    assert record_object.start_time == datetime.now()


@freeze_time('2020-12-31 15:12:11')
def test_calculate_time():
    """Test calculate time"""
    record_object = RecordMouseEvents()
    record_object.start_time = datetime(2020, 12, 30, 14, 11, 10)

    second_diff = record_object.time()

    assert second_diff == 90061.0
    assert isinstance(second_diff, float)


def test_check_exit_method_one_button_is_pressed(mocker):
    """Test listener is still record when one button is pressed"""
    record_object = RecordMouseEvents()
    record_object.button_is_pressed = False
    listener_mocker = mocker.patch.object(Listener, 'stop')

    record_object.exit(True)

    assert record_object.button_is_pressed is True
    assert not listener_mocker.called


def test_check_exit_method_one_button_is_released(mocker):
    """Test listener is still record when one button is released"""
    record_object = RecordMouseEvents()
    record_object.button_is_pressed = True
    listener_mocker = mocker.patch.object(Listener, 'stop')

    record_object.exit(False)

    assert record_object.button_is_pressed is False
    assert not listener_mocker.called


def test_check_exit_method_second_button_is_pressed(mocker):
    """Test listener stop record when second button is pressed"""
    record_object = RecordMouseEvents()
    record_object.button_is_pressed = True
    record_object.listener = Listener()
    listener_mocker = mocker.patch.object(Listener, 'stop')

    record_object.exit(True)

    assert record_object.button_is_pressed is True
    assert listener_mocker.called_once()


def test_result_mouse_move(mocker):
    """Test output mouse move event"""
    record_object = RecordMouseEvents()
    mocker.patch.object(RecordMouseEvents, 'time', return_value=1.1)

    result = record_object.on_move(2, 3)

    assert isinstance(result, dict)
    assert result['eventType'] == 'mouse_move'
    assert result['coordinate'] == {'x': 2, 'y': 3}
    assert result['time'] == 1.1
    assert RecordMouseEvents.time.called_once()


def test_result_mouse_click(mocker):
    """Test output mouse click event"""
    record_object = RecordMouseEvents()
    mocker.patch.object(RecordMouseEvents, 'exit')
    mocker.patch.object(RecordMouseEvents, 'time', return_value=2.0003)

    result = record_object.on_click(10, 20, Button.left, True)

    assert isinstance(result, dict)
    assert result['eventType'] == 'mouse_click'
    assert result['coordinate'] == {'x': 10, 'y': 20}
    assert result['button'] == 'Button.left'
    assert result['pressed'] is True
    assert result['time'] == 2.0003
    assert RecordMouseEvents.time.called_once()
    assert RecordMouseEvents.exit.called_once()


def test_result_mouse_scroll(mocker):
    """Test output mouse scroll event"""
    record_object = RecordMouseEvents()
    mocker.patch.object(RecordMouseEvents, 'time', return_value=0.001)

    result = record_object.on_scroll(0, 999, 0, -1)

    assert isinstance(result, dict)
    assert result['eventType'] == 'mouse_scroll'
    assert result['coordinate'] == {'x': 0, 'y': 999}
    assert result['scroll_vector'] == {'dx': 0, 'dy': -1}
    assert result['time'] == 0.001


# Test for record method...

# @freeze_time('2020-12-31 15:12:11')
# def test_correctly_read_events(mocker):
#     on_click_value = {
#             'eventType': 'mouse_click',
#             'coordinate': {'x': 90, 'y': 100},
#             'button': 'Button.right',
#             'pressed': 'true',
#             'time': 10.1,
#         }
#     on_scroll_value = {
#         'eventType': 'mouse_scroll',
#         'coordinate': {'x': 11, 'y': 90},
#         'scroll_vector': {'dx': 0, 'dy': -1},
#         'time': 2.2,
#     }
#     record_object = RecordMouseEvents()
#     mocker.patch.object(Listener, 'join')
#     mocker.patch.object(RecordMouseEvents, 'on_click', return_value=on_click_value)
#     mocker.patch.object(RecordMouseEvents, 'on_scroll', return_value=on_scroll_value)
#     print('xx'*200)
#     record_object.record()
#     print('2'*200)
#     record_object.on_click()
#
#     assert record_object.events == [on_click_value]

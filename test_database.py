import builtins
import json

from unittest.mock import MagicMock

from database import Database


def test_create_object():
    database_object = Database('database_name.db')

    assert database_object.file is None
    assert database_object.filename == 'database_name.db'
    assert database_object.mode == 'r'


def test_create_object_in_write_method():
    database_object = Database('test.db', 'w')

    assert database_object.mode == 'w'


def test_enter_method_to_use_database_as_context_manager(mocker):
    mocker.patch.object(builtins, 'open')

    with Database('test.db') as database:
        pass

    builtins.open.assert_called_once()


def test_exit_method_to_use_database_as_context_manager(mocker):
    fake_file = MagicMock()
    mocker.patch.object(builtins, 'open', return_value=fake_file)

    with Database(fake_file) as database:
        pass

    fake_file.close.assert_called_once()


def test_is_called_dump_method_when_save_data(mocker):
    mocker.patch.object(builtins, 'open')
    mocker.patch.object(json, 'dump')

    with Database('database_file.db') as database:
        database.save(['value 1', 'value 2'])

    json.dump.assert_called()


def test_passed_args_when_save_data(mocker):
    mocker.patch.object(builtins, 'open')
    mocker.patch.object(json, 'dump')

    with Database('fake_file', 'w') as database:
        database.save(['test 1', 'test 2'])

    json.dump.assert_called_with(['test 1', 'test 2'], builtins.open())


def test_is_called_load_method_when_load_data(mocker):
    mocker.patch.object(builtins, 'open')
    mocker.patch.object(json, 'load')

    with Database('test_file.db') as database:
        database.load()

    json.load.assert_called()


def test_correct_file_hanlder_in_load_method(mocker):
    mocker.patch.object(builtins, 'open')
    mocker.patch.object(json, 'load')

    with Database('test_database.db') as database:
        database.load()

    json.load.assert_called_with(builtins.open())

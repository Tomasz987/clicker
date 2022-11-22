"""Tests collection for database.py module."""
import builtins
import json

from unittest.mock import MagicMock

from tools.database import Database


def test_create_object():
    """Test check object is created correctly."""
    database_object = Database('database_name.db')

    assert database_object.file is None
    assert database_object.filename == 'database_name.db'
    assert database_object.mode == 'r'


def test_create_object_in_write_method():
    """Test check object is created in write mode."""
    database_object = Database('test.db', 'w')

    assert database_object.mode == 'w'


def test_enter_method_to_use_database_as_context_manager(mocker):
    """Test check __enter__ method opens the file.

        Args:
            mocker (pytest_mock): mock to catch 'builtins.open' method.

    """
    mocker.patch.object(builtins, 'open')

    with Database('test.db') as database:
        pass

    builtins.open.assert_called_once()
    builtins.open.assert_called_with('test.db', 'r', encoding='utf-8')


def test_exit_method_to_use_database_as_context_manager(mocker):
    """Test __exit__ method closes an open file.

    Args:
        mocker (pytest_mock): mock to catch 'builtins.open' method.

    """
    fake_file = MagicMock()
    mocker.patch.object(builtins, 'open', return_value=fake_file)

    with Database(fake_file) as database:
        pass

    fake_file.close.assert_called_once()


def test_is_called_dump_method_while_save_data(mocker):
    """Test check is called json.dump while save data.

    Args:
        mocker (pytest_mock): mock to catch 'builtins.open' and
        'json.dump' methods.

    """
    mocker.patch.object(builtins, 'open')
    mocker.patch.object(json, 'dump')

    with Database('database_file.db') as database:
        database.save(['value 1', 'value 2'])

    json.dump.assert_called()


def test_passed_args_while_save_data(mocker):
    """Test check the passed arguments while save data.

    Args:
        mocker (pytest_mock): mock to catch 'builtins.open' and
        'json.dump' methods.

    """
    mocker.patch.object(builtins, 'open')
    mocker.patch.object(json, 'dump')

    with Database('fake_file', 'w') as database:
        database.save(['test 1', 'test 2'])

    json.dump.assert_called_with(['test 1', 'test 2'], builtins.open())


def test_is_called_load_method_while_load_data(mocker):
    """Test check is called method 'json.load' while load data.

    Args:
        mocker (pytest_mock): mock to catch 'builtins.open' and
        'json.load' methods.

    """
    mocker.patch.object(builtins, 'open')
    mocker.patch.object(json, 'load')

    with Database('test_file.db') as database:
        database.load()

    json.load.assert_called()


def test_is_correct_file_handler_while_load_method(mocker):
    """Test check is correct file handler while load method is called.

    Args:
        mocker (pytest_mock): mock to catch 'builtins.open' and
        'json.load' methods.
    """
    mocker.patch.object(builtins, 'open')
    mocker.patch.object(json, 'load')

    with Database('test_database.db') as database:
        database.load()

    json.load.assert_called_with(builtins.open())

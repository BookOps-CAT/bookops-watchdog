import os
from unittest import mock

import pytest

from bookops_watchdog.config import (
    add_environ_variables,
    configure_app,
    construct_config_path,
    get_app_data_dir,
    get_config_settings,
    get_datastore_fh,
    get_log_fh,
    watchdog_logging_config,
    validate_directory,
)


@pytest.mark.parametrize(
    "arg,expectation",
    [
        ("dev", "C:\\Users\\Foo\\.bookops-watchdog\\config_variables_dev.yaml"),
        ("prod", "C:\\Users\\Foo\\.bookops-watchdog\\config_variables_prod.yaml"),
    ],
)
def test_construct_config_path(arg, expectation, mock_user):
    assert construct_config_path(arg) == expectation


def test_get_config_settings(mock_user):
    mock_open = mock.mock_open(
        read_data='---\nlog_fh: "foo"\nlog_handlers:\n  - console\n  - file'
    )
    with mock.patch("builtins.open", mock_open):
        assert get_config_settings() == dict(
            log_fh="foo", log_handlers=["console", "file"]
        )


def test_add_environ_variables():
    add_environ_variables(foo="bar", spam="baz")
    assert os.getenv("foo") == "bar"
    assert os.getenv("spam") == "baz"


@pytest.mark.parametrize(
    "arg,expectation",
    [
        ("dev", "C:\\Users\\Foo\\APPDATA\\LOCAL\\TEMP\\Bookops-Watchdog"),
        ("prod", "C:\\Users\\Foo\\APPDATA\\LOCAL\\Bookops-Watchdog"),
    ],
)
def test_get_app_data_dir(arg, expectation, mock_user):
    assert get_app_data_dir(arg) == expectation


@pytest.mark.parametrize(
    "arg,expectation",
    [
        (
            "dev",
            (
                "C:\\Users\\Foo\\APPDATA\\LOCAL\\TEMP\\Bookops-Watchdog\\watchdog.log",
                "spam",
                ["console", "file"],
            ),
        ),
        (
            "prod",
            (
                "C:\\Users\\Foo\\APPDATA\\LOCAL\\Bookops-Watchdog\\watchdog.log",
                "spam",
                ["console", "file"],
            ),
        ),
    ],
)
def test_configure_app_returns(
    arg, expectation, fake_yaml_data, mock_user, mock_app_data_directory
):
    mock_open = mock.mock_open(read_data=fake_yaml_data)
    with mock.patch("builtins.open", mock_open):
        assert configure_app(arg) == expectation


@pytest.mark.parametrize(
    "arg,exp1,exp2",
    [
        (
            "dev",
            "C:\\Users\\Foo\\APPDATA\\LOCAL\\TEMP\\Bookops-Watchdog\\datastore.db",
            "S:/BookopsWatchdog",
        ),
        (
            "prod",
            "C:\\Users\\Foo\\APPDATA\\LOCAL\\Bookops-Watchdog\\datastore.db",
            "S:/BookopsWatchdog",
        ),
    ],
)
def test_configure_app_adding_env_variables(
    arg,
    exp1,
    exp2,
    fake_yaml_data,
    mock_user,
    mock_app_data_directory,
):
    mock_open = mock.mock_open(read_data=fake_yaml_data)
    with mock.patch("builtins.open", mock_open):
        configure_app(arg)
        assert os.getenv("watchdog_store") == exp1
        assert os.getenv("watchdog_drive") == exp2


def test_get_datastore_fh():
    assert get_datastore_fh("C:\\Foo") == "C:\\Foo\\datastore.db"


def test_get_log_fh():
    assert get_log_fh("C:\\Foo") == "C:\\Foo\\watchdog.log"


def test_watchdog_logging_config_returns_dict(mock_user, fake_yaml_data):
    mock_open = mock.mock_open(read_data=fake_yaml_data)
    with mock.patch("builtins.open", mock_open):
        assert (
            type(
                watchdog_logging_config(
                    log_fh="foo", log_token="bar", handlers=["console"]
                )
            )
            is dict
        )


def test_watchdog_logging_config_log_fh():
    assert (
        watchdog_logging_config(log_fh="foo.log", log_token="bar", handlers=[])[
            "handlers"
        ]["file"]["filename"]
        == "foo.log"
    )


def test_watchdog_logging_config_log_token():
    assert (
        watchdog_logging_config(log_fh="foo.log", log_token="bar", handlers=[])[
            "handlers"
        ]["loggly"]["url"]
        == "https://logs-01.loggly.com/inputs/bar/tag/python"
    )


def test_watchdog_logging_config_handlers():
    assert watchdog_logging_config(
        log_fh="foo.log", log_token="bar", handlers=["console", "file"]
    )["loggers"]["bookops-watchdog"]["handlers"] == ["console", "file"]


def test_validate_directory(tmpdir):
    root = tmpdir.mkdir("Bookops-Watchdog")
    data_dir = os.path.join(root, "data")
    assert not os.path.isdir(data_dir)
    validate_directory(data_dir)
    assert os.path.isdir(data_dir)

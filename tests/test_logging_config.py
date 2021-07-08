import os

import pytest

from bookops_watchdog.errors import WatchdogError
from bookops_watchdog.logging_config import (
    get_config_data,
    get_token_from_file,
    watchdog_logging_config,
)


def test_no_token_in_env():
    with pytest.raises(WatchdogError) as exc:
        get_config_data("foo")
        assert (
            str(exc)
            == "Logging configuration error: loggly token missing in environmental variables."
        )


@pytest.mark.local_only
def test_local_env_handlers():
    handlers, _ = get_config_data("local")
    assert handlers == ["console", "file", "loggly"]


@pytest.mark.local_only
def test_get_token_from_file(mock_local_token):
    token_fh = os.path.join(os.environ["HOME"], ".loggly\\bwatch-log-token.json")
    assert get_token_from_file(token_fh) == "foo"


@pytest.mark.local_only
def test_get_config_data_local_env(mock_local_token):
    assert get_config_data("local") == (["console", "file", "loggly"], "foo")


@pytest.mark.parametrize("arg", ["dev", "prod"])
def test_get_config_data_server_env(arg, mock_env_var_token):
    assert get_config_data(arg) == (["file", "loggly"], "foo")


@pytest.mark.parametrize("arg", ["dev", "prod"])
def test_watchdog_logging_config_log_filename(arg, mock_env_var_token):
    conf = watchdog_logging_config(arg)
    assert conf["handlers"]["file"]["filename"] == ".\\log\\watchdog.log"


@pytest.mark.local_only
def test_watchdog_logging_config_token_local(mock_local_token):
    conf = watchdog_logging_config("local")
    assert (
        conf["handlers"]["loggly"]["url"]
        == "https://logs-01.loggly.com/inputs/foo/tag/python"
    )


@pytest.mark.parametrize("arg", ["dev", "prod"])
def test_watchdog_logging_config_token_env_var(
    arg, mock_local_token, mock_env_var_token
):
    conf = watchdog_logging_config(arg)
    assert (
        conf["handlers"]["loggly"]["url"]
        == "https://logs-01.loggly.com/inputs/foo/tag/python"
    )


@pytest.mark.local_only
def test_watchdog_logging_config_local_handlers(mock_local_token):
    conf = watchdog_logging_config("local")
    assert conf["loggers"]["bookops-watchdog"]["handlers"] == [
        "console",
        "file",
        "loggly",
    ]


@pytest.mark.parametrize("arg", ["dev", "prod"])
def test_watchdog_logging_config_server_handlers(arg, mock_env_var_token):
    conf = watchdog_logging_config(arg)
    assert conf["loggers"]["bookops-watchdog"]["handlers"] == [
        "file",
        "loggly",
    ]

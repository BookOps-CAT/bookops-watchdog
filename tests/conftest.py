# -*- coding: utf-8 -*-

import datetime

import pytest

from bookops_watchdog.worker_ftp import put_creds_to_env_var
import bookops_watchdog


@pytest.fixture
def fake_yaml_data():
    return '---\nlog_fh: "foo"\nlog_handlers:\n  - console\n  - file\nloggly_token: "spam"\nsendGrid_key: "baz"'


@pytest.fixture
def live_local_ftp_creds():
    put_creds_to_env_var()


@pytest.fixture
def mock_app_data_directory(monkeypatch):
    def mock_validate_directory(*args, **kwargs):
        return None

    monkeypatch.setattr(
        "bookops_watchdog.config.validate_directory", mock_validate_directory
    )


@pytest.fixture
def mock_env_var_token(monkeypatch):
    monkeypatch.setenv("LOG-TOKEN", "foo")


@pytest.fixture
def mock_local_ftp_creds(monkeypatch):
    def mock_ftp_creds_file(*args, **kwargs):
        return {
            "FTP_HOST": "foo",
            "FTP_USER": "bar",
            "FTP_PASSW": "spam",
            "FTP_DIR": "baz",
        }

    monkeypatch.setattr("json.load", mock_ftp_creds_file)


@pytest.fixture
def mock_local_token(monkeypatch):
    def mock_config_file(*args, **kwargs):
        return dict(token="foo")

    monkeypatch.setattr("json.load", mock_config_file)


@pytest.fixture
def mock_nlst(monkeypatch):
    def mock_files(*args, **kwargs):
        return [
            f"BookOpsQC.{datetime.datetime.now():%Y%m%d%H%M}",
            f"BookOpsQC.{datetime.datetime.now() - datetime.timedelta(days=1):%Y%m%d%H%M}",
        ]

    monkeypatch.setattr(bookops_watchdog.worker_ftp, "get_files_in_dir", mock_files)


@pytest.fixture
def mock_user(monkeypatch):
    monkeypatch.setenv("USERPROFILE", "C:\\Users\\Foo")
    monkeypatch.setenv("LOCALAPPDATA", "C:\\Users\\Foo\\APPDATA\\LOCAL")

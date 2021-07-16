# -*- coding: utf-8 -*-

import datetime
import os

import pytest
import yaml

import bookops_watchdog


@pytest.fixture
def fake_yaml_data():
    return '---\nlog_fh: "foo"\nlog_handlers:\n  - console\n  - file\nloggly_token: "spam"\nsendGrid_key: "baz"\nftp_host: "ftp.foo.com"\nftp_user: "fakeFtpUser"\nftp_passw: "fakeFtpPassw"\nftp_folder: "SPAM"'


@pytest.fixture
def live_dev_ftp_creds():
    fh = os.path.join(
        os.environ["USERPROFILE"], ".bookops-watchdog\\config_variables_dev.yaml"
    )
    with open(fh, "r") as f:
        creds = yaml.safe_load(f)
        return dict(
            host=creds["ftp_host"],
            user=creds["ftp_user"],
            passw=creds["ftp_passw"],
            folder=creds["ftp_folder"],
        )


@pytest.fixture
def mock_all_env_variables(monkeypatch):
    monkeypatch.setenv("USERPROFILE", "C:\\Users\\Foo")
    monkeypatch.setenv("LOCALAPPDATA", "C:\\Users\\Foo\\APPDATA\\LOCAL")
    monkeypatch.setenv("watchdog_ftp_host", "ftp.foo.com")
    monkeypatch.setenv("watchdog_ftp_user", "fakeFtpUser")
    monkeypatch.setenv("watchdog_ftp_passw", "fakeFtpPassw")
    monkeypatch.setenv("watchdog_ftp_folder", "SPAM")
    monkeypatch.setenv("watchdog_sendGrid", "baz")
    monkeypatch.setenv(
        "watchdog_store",
        "C:\\Users\\Foo\\APPDATA\\TEMP\\Bookops-Watchdog\\datastore.db",
    )


@pytest.fixture
def mock_app_data_directory(monkeypatch):
    def mock_validate_directory(*args, **kwargs):
        return None

    monkeypatch.setattr(
        "bookops_watchdog.config.validate_directory", mock_validate_directory
    )


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

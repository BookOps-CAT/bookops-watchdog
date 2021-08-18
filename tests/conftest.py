# -*- coding: utf-8 -*-

import pytest


# from bookops_watchdog.worker_reports import SierraExportReader
from bookops_watchdog.datastore import dal


@pytest.fixture
def fake_yaml_data():
    return '---\nlog_fh: "foo"\nlog_handlers:\n  - console\n  - file\nloggly_token: "spam"\ndrive: "S:/BookopsWatchdog"'


@pytest.fixture
def mock_all_env_variables(monkeypatch):
    monkeypatch.setenv("USERPROFILE", "C:\\Users\\Foo")
    monkeypatch.setenv("LOCALAPPDATA", "C:\\Users\\Foo\\APPDATA\\LOCAL")
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
def mock_user(monkeypatch):
    monkeypatch.setenv("USERPROFILE", "C:\\Users\\Foo")
    monkeypatch.setenv("LOCALAPPDATA", "C:\\Users\\Foo\\APPDATA\\LOCAL")


@pytest.fixture
def mock_app_data_dir(tmpdir):
    """
    Returns py.path.local obj with app test data directory
    """
    return tmpdir.mkdir("Bookops-Watchog")


@pytest.fixture
def mock_datastore_file(mock_app_data_dir, monkeypatch):
    store_fh = mock_app_data_dir.join("datastore.db")
    monkeypatch.setenv("watchdog_store", str(store_fh))


@pytest.fixture
def mock_datastore_session():
    # setUp
    dal.conn = "sqlite:///:memory:"
    dal.connect()
    session = dal.Session()
    yield session

    # tearDown
    session.rollback()
    session.close()

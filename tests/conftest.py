# -*- coding: utf-8 -*-

import pytest


@pytest.fixture
def mock_local_token(monkeypatch):
    def mock_config_file(*args, **kwargs):
        return dict(token="foo")

    monkeypatch.setattr("json.load", mock_config_file)


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

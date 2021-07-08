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

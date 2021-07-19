"""
Tests ftp worker module
"""
import ftplib
import os
from datetime import datetime, timedelta

import pytest


from bookops_watchdog.worker_ftp import (
    find_aged_out_files,
    find_unprocessed_files,
    ftp_connect,
    get_ftp_creds_from_env_var,
    get_files_in_dir,
    get_file_date,
    get_library_directory,
    is_aged_out,
)


def test_get_ftp_creds_from_env_var(mock_all_env_variables):

    assert get_ftp_creds_from_env_var() == dict(
        host="ftp.foo.com", user="fakeFtpUser", passw="fakeFtpPassw", folder="SPAM"
    )


@pytest.mark.webtest
def test_ftp_connect_live(live_dev_ftp_creds):
    creds = live_dev_ftp_creds
    ftp = ftp_connect(**creds, library="BPL")
    assert type(ftp) == ftplib.FTP


@pytest.mark.webtest
def test_get_files_in_dir_live(live_dev_ftp_creds):
    creds = live_dev_ftp_creds
    ftp = ftp_connect(**creds, library="BPL")
    assert get_files_in_dir(ftp) == [
        "BookOpsQC.20210707063001",
        "BookOpsQC.20210709063000",
    ]


def test_get_library_directory():
    assert get_library_directory("foo", "bar") == "foo/bar"


def test_find_unprocessed_files():
    retrieved = ["1.txt", "2.txt", "3.txt"]
    processed = ["1.txt", "3.txt"]
    assert find_unprocessed_files(retrieved, processed) == ["2.txt"]


def test_get_file_date():
    assert get_file_date("BookOpsQC.20210102131501") == datetime(
        year=2021, month=1, day=2, hour=13, minute=15, second=1
    )


@pytest.mark.parametrize(
    "arg1,arg2,expectation",
    [
        (datetime.now(), 1, False),
        (datetime.now() - timedelta(days=1), 2, False),
        (datetime.now() - timedelta(days=5), 4, True),
        (datetime.now() - timedelta(days=31), 30, True),
    ],
)
def test_is_aged_out(arg1, arg2, expectation):
    assert is_aged_out(file_date=arg1, days=arg2) == expectation


def test_find_aged_out_files():
    files = [
        f"BookOpsQC.{datetime.now():%Y%m%d%H%M%S}",
        f"BookOpsQC.{datetime.now() - timedelta(days=20):%Y%m%d%H%S}",
        f"BookOpsQC.{datetime.now() - timedelta(days=31):%Y%m%d%H%S}",
    ]
    assert find_aged_out_files(files=files, days=30) == [files[2]]

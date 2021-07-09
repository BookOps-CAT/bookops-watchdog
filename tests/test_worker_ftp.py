"""
Tests ftp worker module
"""
import ftplib
import os

import pytest


from bookops_watchdog.errors import WatchdogError
from bookops_watchdog.worker_ftp import (
    get_ftp_creds_from_file,
    ftp_connect,
    put_creds_to_env_var,
)


@pytest.mark.local_only
def test_get_ftp_creds_from_file(mock_local_ftp_creds):
    creds_fh = os.path.join(os.environ["HOME"], ".ftp\\bwatch-ftp-cred.json")
    assert get_ftp_creds_from_file(creds_fh) == {
        "FTP_HOST": "foo",
        "FTP_USER": "bar",
        "FTP_PASSW": "spam",
        "FTP_DIR": "baz",
    }


@pytest.mark.local_only
def test_get_fpt_creds_from_file_file_not_found():
    with pytest.raises(WatchdogError) as exc:
        get_ftp_creds_from_file("foo.json")
        assert (
            str(exc)
            == "FTP configuration error: unable to locate credentials at foo.json ."
        )


@pytest.mark.local_only
def test_put_local_creds_to_env_var(mock_local_ftp_creds):
    put_creds_to_env_var("local")
    creds = [
        os.getenv("FTP_HOST"),
        os.getenv("FTP_USER"),
        os.getenv("FTP_PASSW"),
        os.getenv("FTP_DIR"),
    ]
    assert creds == ["foo", "bar", "spam", "baz"]


@pytest.mark.parametrize("arg", ["BPL", "NYPL"])
@pytest.mark.local_only
def test_ftp_connect_local(arg):
    creds_fh = os.path.join(os.environ["HOME"], ".ftp\\bwatch-ftp-cred.json")
    creds = get_ftp_creds_from_file(creds_fh)
    ftp = ftp_connect(
        host=creds["FTP_HOST"],
        user=creds["FTP_USER"],
        passw=creds["FTP_PASSW"],
        folder=creds["FTP_DIR"],
        library=arg,
    )
    assert type(ftp) == ftplib.FTP

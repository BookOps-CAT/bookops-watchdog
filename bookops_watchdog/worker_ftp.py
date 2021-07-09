# -*- coding: utf-8 -*-

"""
This module handles communication with Watchdog's FTP
"""

from ftplib import FTP, error_reply
import json
import logging
import os
from typing import Dict

from bookops_watchdog.errors import WatchdogError

mlogger = logging.getLogger("bookops-watchdog")


def get_ftp_creds_from_file(fh: str) -> Dict:
    """
    Retrieves ftp credentials from a file and returns them as dictionary

    Args:
        fh:                 path to credentials

    Returns:
        creds:              credentials as dicitonary
    """
    mlogger.debug(f"FTP: retrieving credentails from {fh} .")
    try:
        with open(fh, "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        raise WatchdogError(
            f"FTP: configuration error, unable to locate credentials at {fh} ."
        )


def put_creds_to_env_var(env: str = "local") -> None:
    """
    Prepares ftp credentials in environmental variables depending
    on the mode (env)

    Args:
        env:                environment to run the app
    """

    if env == "local":
        creds_fh = os.path.join(os.environ["HOME"], ".ftp\\bwatch-ftp-cred.json")
        creds = get_ftp_creds_from_file(creds_fh)

        mlogger.debug("FTP: adding credentials to environment variables.")
        for k, v in creds.items():
            os.environ[k] = v


def get_ftp_creds_from_env_var() -> Dict:
    """
    Retrieves ftp credentials from environmental variables

    Returns:
        creds:              credentials as dictionary
    """

    creds = dict(
        host=os.getenv("FTP_HOST"),
        user=os.getenv("FTP_USER"),
        passw=os.getenv("FTP_PASSW"),
        folder=os.getenv("FTP_DIR"),
    )
    mlogger.info(f"FTP: credentials successfully retrieved from environment variables.")
    return creds


def ftp_connect(host: str, user: str, passw: str, folder: str, library: str):
    """

    Args:
        host:       ftp host
        user:       ftp user
        passw:      ftp password
        folder:     ftp workspace folder
        library:    'NYPL' or 'BPL'
    """
    ftp = FTP(host)
    conn = ftp.login(user, passw)
    try:
        if conn[:3] == "230":
            mlogger.info(f"FTP: successfuly connected to ({host}/{user}).")
            directory = f"{folder}/{library}/"
            ftp.cwd(directory)
            mlogger.debug(f"FTP: current folder changed to {directory}")
            return ftp

        else:
            mlogger.warning(f"FTP: failed to connect to FTP {conn}.")
            return None
    except error_reply as exc:
        mlogger.error(f"FTP: failed to connect to FTP. Error: {exc}")
        return None

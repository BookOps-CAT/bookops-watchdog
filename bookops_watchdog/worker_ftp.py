# -*- coding: utf-8 -*-

"""
This module handles communication with Watchdog's FTP
"""

from ftplib import FTP, error_reply
import logging
import os
from typing import Dict, List


mlogger = logging.getLogger("bookops-watchdog")


def get_ftp_creds_from_env_var() -> Dict:
    """
    Retrieves ftp credentials from environmental variables

    Returns:
        creds:              credentials as dictionary
    """

    creds = dict(
        host=os.getenv("watchdog_ftp_host"),
        user=os.getenv("watchdog_ftp_user"),
        passw=os.getenv("watchdog_ftp_passw"),
        folder=os.getenv("watchdog_ftp_folder"),
    )
    mlogger.info(f"FTP: credentials successfully retrieved from environment variables.")
    return creds


def get_files_in_dir(ftp: FTP) -> List:
    return ftp.nlst()


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
            mlogger.debug(f"FTP: successfully connected to '{host}'.")
            directory = f"{folder}/{library}/"
            ftp.cwd(directory)
            mlogger.debug(f"FTP: current folder changed to '{directory}'.")
            return ftp
    except error_reply as exc:
        mlogger.error(f"FTP: failed to connect to FTP with follwing error: '{exc}'.")
        return None

# -*- coding: utf-8 -*-

"""
This module handles communication with Watchdog's FTP
"""

from ftplib import FTP, error_reply
import json
import logging
import os


mlogger = logging.getLogger("bookops-watchdog")

try:
    APP_FTP = dict(
        host=os.environ["FTP-HOST"],
        user=os.environ["FTP-USER"],
        passw=os.environ["FTP-PASSW"],
        folder=os.environ["FTP-FOLDER"],
    )
except KeyError:
    try:
        ftp_fh = os.path.join(os.environ["USERPROFILE"], ".ftp\\bwatch-ftp-cred.json")
        with open(ftp_fh, "r") as file:
            data = json.load(file)
            APP_FTP = dict(
                host=data["host"],
                user=data["user"],
                passw=data["passw"],
                folder=data["folder"],
            )
    except FileNotFoundError:
        APP_FTP = None


def ftp_connect(host: str, user: str, passw: str, folder: str, library: str):
    """

    Args:
        host:       ftp host
        user:       ftp user
        passw:      ftp password
        folder:     ftp workspace folder
    """
    ftp = FTP(host)
    conn = ftp.login(user, passw)
    try:
        if conn[:3] == "230":
            mlogger.info(f"Successfuly connected to FTP ({host}/{user}).")
            ftp.cwd(folder)
            return ftp

        else:
            mlogger.warning(f"Failed to connect to FTP {conn}.")
            return None
    except error_reply as exc:
        mlogger.error(f"Failt to connect to FTP. Error: {exc}")
        return None

# -*- coding: utf-8 -*-

"""
This module handles communication with Watchdog's FTP
"""

from ftplib import FTP
import json
import logging
import os


mlogger = logging.getLogger("bookops-watchdog")


dev_fh = os.path.join(os.getenv("USERPROFILE"), ".ftp\\drivehq_dev.json")
try:
    with open(dev_fh, "r") as file:
        data = json.load(file)
        DEV_FTP = dict(
            host=data["host"],
            user=data["user"],
            passw=data["passw"],
            folder=data["folder"],
        )
except FileNotFoundError:
    DEV_FTP = None


def ftp_session(host: str, user: str, passw: str, folder: str):
    ftp = FTP(host)
    conn = ftp.login(user, passw)
    if conn[:3] == "230":
        mlogger.info(f"Successfuly connected to FTP ({host}/{user}).")
    else:
        mlogger.error(f"Failed to connect to FTP ({host}/{user}).")

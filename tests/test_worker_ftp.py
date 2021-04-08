"""
Tests ftp worker module
"""
import os

import pytest


from bookops_watchdog.worker_ftp import APP_FTP, ftp_connect


def test_temp():
    ftp = ftp_connect(**APP_FTP, library="bpl")
    print(type(ftp))
    print(ftp.retrlines("LIST"))

    ftp.quit()

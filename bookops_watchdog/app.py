# -*- coding: utf-8 -*-

"""
Main module of the BookOps-Watchdog app.
"""

import argparse
import logging
import logging.config
import os

import loggly.handlers

from bookops_watchdog.logging_config import watchdog_logging_config
from bookops_watchdog.worker_ftp import (
    APP_FTP,
    ftp_connect,
    list_files_in_current_directory,
)


# def validate_app():
#     """
#     Verifies and sets up workspace for the app.
#     """

#     #  veify log dir exists and if not create one
#     if not os.path.isdir(".\\log"):
#         os.mkdir(".\\log")


# def run(mode: str = "local"):
#     """
#     Args:
#         mode:   'local' (default), 'dev' or 'prod'
#     """
#     ftp = ftp_connect(**APP_FTP, library="NYPL")
#     files = list_files_in_current_directory(ftp)

#     if ftp is not None:
#         ftp.quit()


def createArgParser():
    parser = argparse.ArgumentParser(description="bookops-watchdog help")
    parser.add_argument(
        "--env",
        required=True,
        type=str,
        help="environment to run app, options: local | dev | prod",
    )
    return parser


if __name__ == "__main__":

    parser = createArgParser()
    args = parser.parse_args()
    print(args.env)

    # # validate app
    # validate_app()

    logging.config.dictConfig(watchdog_logging_config)
    logger = logging.getLogger("bookops-watchdog")

    # run()

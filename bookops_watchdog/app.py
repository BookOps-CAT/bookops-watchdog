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
    ftp_connect,
)


def validate_app():
    """
    Verifies and sets up workspace for the app.
    """

    #  veify log dir exists and if not create one
    if not os.path.isdir(".\\log"):
        os.mkdir(".\\log")


# def run(mode: str = "local"):
#     """
#     Args:
#         mode:   'local' (default), 'dev' or 'prod'
#     """
#     ftp = ftp_connect(**APP_FTP, library="NYPL")

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

    # confirm working space is setup correctly
    validate_app()

    parser = createArgParser()
    args = parser.parse_args()

    log_conf = watchdog_logging_config(args.env)
    logging.config.dictConfig(log_conf)
    logger = logging.getLogger("bookops-watchdog")
    logger.info(f"Initiating Watchdog in {args.env} mode...")

    # run()

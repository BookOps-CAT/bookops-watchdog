# -*- coding: utf-8 -*-

"""
Main module of the BookOps-Watchdog app.
"""

import logging
import logging.config
import os

import loggly.handlers

from logging_config import DEV_LOGGING, PROD_LOGGING
from worker_ftp import DEV_FTP, ftp_session


def validate_app():
    """
    Verifies and sets up workspace for the app.
    """

    #  veify log dir exists and if not create one
    if not os.path.isdir(".\\log"):
        os.mkdir(".\\log")


def run(mode: str = "dev"):
    """
    Args:
        mode:   'dev' or 'prod'
    """
    ftp_session(**DEV_FTP)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="bookops-watchdog help")
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--env",
        help="enviroment to run app, format: --env [dev|prod]",
        nargs=1,
        type=str,
    )

    args = parser.parse_args()

    # validate app
    validate_app()

    # select logging environment
    if args.env == "dev" or args.env is None:
        env_log = DEV_LOGGING
    elif args.env == "prod":
        env_log = PROD_LOGGING
    else:
        raise AttributeError(
            "Invalid logging environment provided. Use 'prod' or 'dev'."
        )

    logging.config.dictConfig(env_log)
    logger = logging.getLogger("bookops-watchdog")

    run()

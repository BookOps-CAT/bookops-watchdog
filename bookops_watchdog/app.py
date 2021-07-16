# -*- coding: utf-8 -*-

"""
Main module of the BookOps-Watchdog app.
"""

import argparse
import logging
import logging.config
import os

import loggly.handlers

from bookops_watchdog.config import configure_app, watchdog_logging_config
from bookops_watchdog.worker_ftp import (
    ftp_connect,
)


def run():
    logger.info(f"Current working directory: '{os.getcwd()}'.")


def createArgParser():
    parser = argparse.ArgumentParser(description="bookops-watchdog help")
    parser.add_argument(
        "--env",
        required=True,
        type=str,
        help="environment to run app, options: dev | prod",
    )
    return parser


if __name__ == "__main__":

    # confirm working space is setup correctly
    # validate_app()

    parser = createArgParser()
    args = parser.parse_args()

    log_fh, log_token, handlers = configure_app(args.env)
    log_conf = watchdog_logging_config(log_fh, log_token, handlers)
    logging.config.dictConfig(log_conf)
    logger = logging.getLogger("bookops-watchdog")
    logger.info(f"Initiating Watchdog in {args.env.upper()} mode...")

    run()

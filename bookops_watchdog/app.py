# -*- coding: utf-8 -*-

"""
Main module of the BookOps-Watchdog app.
"""

import logging
import logging.config

import loggly.handlers

from logging_config import DEV_LOGGING, PROD_LOGGING


def configure_logger(environment: str = "dev") -> None:
    """
    Configures development or production logging

    Args:
        environment:        'prod' or 'dev'
    """

    return logger


def run():
    logger.debug("DEBUG msg.")
    logger.info("INFO msg.")
    logger.error("ERROR msg.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="bookops-watchdog help")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--env", help="enviroment to run app, format: --env [dev|prod]")

    args = parser.parse_args()

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

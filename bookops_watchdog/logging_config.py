# -*- coding: utf-8 -*-

"""
Logging configuration of the BookOps-Watchdog app
"""

import json
import logging
import os
import traceback
from typing import Dict, List, Tuple

from bookops_watchdog.errors import WatchdogError

LOG_PATH = ".\\log\\watchdog.log"


def get_token_from_file(fh: str) -> str:
    with open(fh, "r") as file:
        data = json.load(file)
        return data["token"]


def get_config_data(env: str) -> Tuple[List, str]:
    """
    Determines handlers and loggly token based on the environment

    Args:
        env:                        enviroment to run

    Returns:
        handlers, token:     tuple of list of logging handlers and loggly token
    """

    if env == "local":
        token_fh = os.path.join(os.environ["HOME"], ".loggly\\bwatch-log-token.json")
        token = get_token_from_file(token_fh)
        os.environ["LOG-TOKEN"] = token
        handlers = ["console", "file", "loggly"]

    else:
        handlers = ["file", "loggly"]

    token = os.getenv("LOG-TOKEN")

    if not token:
        raise WatchdogError(
            "Logging configuration error: loggly token missing in environmental variables."
        )

    else:
        return (handlers, token)


def watchdog_logging_config(env: str = "local") -> Dict:
    """
    Returns dictionary with logger configuration based on environment

    Args:
        env:                        environment to run the app

    Returns:                        logging configuration as dictionary
    """

    handlers, token = get_config_data(env)

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "brief": {
                "format": "%(name)s-%(asctime)s-%(filename)s-%(lineno)s-%(levelname)s-%(message)s"
            },
            "json": {
                "format": '{"app":"%(name)s", "asciTime":"%(asctime)s", "fileName":"%(filename)s", "lineNo":"%(lineno)d", "levelName":"%(levelname)s", "message":"%(message)s"}'
            },
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "brief",
            },
            "file": {
                "level": "INFO",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": LOG_PATH,
                "formatter": "brief",
                "maxBytes": 1024 * 1024,
                "backupCount": 5,
            },
            "loggly": {
                "level": "ERROR",
                "class": "loggly.handlers.HTTPSHandler",
                "formatter": "json",
                "url": f"https://logs-01.loggly.com/inputs/{token}/tag/python",
            },
        },
        "loggers": {
            "bookops-watchdog": {
                "handlers": handlers,
                "level": "DEBUG",
                "propagate": True,
            }
        },
    }
    return logging_config


class LogglyAdapter(logging.LoggerAdapter):
    """
    Adapter for Loggly service that escapes JSON special characters in messages
    """

    def process(self, msg, kwargs):
        try:
            format_msg = "%s" % (
                msg.replace("\\", "/")
                .replace('"', "")
                .replace("'", "")
                .replace("\n", "\\n")
                .replace("\t", "\\t")
            )
        except AttributeError:
            format_msg = msg

        return format_msg, kwargs


def format_traceback(exc, exc_traceback=None):
    """
    Formats logging tracebacks into a string accepted by Loggly service (JSON).
    args:
        exc: type, exceptions
        exc_traceback: type, traceback obtained from sys.exc_info()
    returns:
        traceback: string of joined traceback lines
    usage:
        try:
            int('a')
        except ValueError as exc:
            _, _, exc_traceback = sys.exc_info()
            tb = format_traceback(exc, exc_traceback)
            logger.error('Unhandled error. {}'.format(tb))
    """

    if exc_traceback is None:
        exc_traceback = exc.__traceback__

    return "".join(traceback.format_exception(exc.__class__, exc, exc_traceback))

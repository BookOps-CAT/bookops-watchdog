# -*- coding: utf-8 -*-

"""
Logging configuration of the BookOps-Watchdog app
"""

import json
import logging
import os
import traceback

PROD_LOG_PATH = ".\\log\\prod-log.log"
DEV_LOG_PATH = ".\\log\\dev-log.log"

try:
    PROD_LOGGLY_TOKEN = os.environ["BWATCHDOG-LOGGLY-PROD"]
    DEV_LOGGLY_TOKEN = os.environ["BWATCHDOG-LOGGLY-DEV"]
except KeyError:
    tokens_fh = os.path.join(os.environ["USERPROFILE"], ".loggly\\loggly_tokens.json")
    with open(tokens_fh, "r") as file:
        data = json.load(file)
        PROD_LOGGLY_TOKEN = data["prod_token"]
        DEV_LOGGLY_TOKEN = data["dev_token"]


PROD_LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "brief": {
            "format": "%(name)s-%(asctime)s-%(filename)s-%(lineno)s-%(levelname)s-%(levelno)s-%(message)s"
        },
        "json": {
            "format": '{"app":"%(name)s", "asciTime":"%(asctime)s", "fileName":"%(filename)s", "lineNo":"%(lineno)d", "levelName":"%(levelname)s", "message":"%(message)s"}'
        },
    },
    "handlers": {
        "loggly": {
            "level": "ERROR",
            "class": "loggly.handlers.HTTPSHandler",
            "formatter": "json",
            "url": f"https://logs-01.loggly.com/inputs/{PROD_LOGGLY_TOKEN}/tag/python",
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": PROD_LOG_PATH,
            "formatter": "brief",
            "maxBytes": 1024 * 1024,
            "backupCount": 5,
        },
    },
    "loggers": {
        "bookops-watchdog": {
            "handlers": ["loggly", "file"],
            "level": "DEBUG",
            "propagate": True,
        }
    },
}


DEV_LOGGING = {
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
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": DEV_LOG_PATH,
            "formatter": "brief",
            "maxBytes": 1024 * 1024,
            "backupCount": 5,
        },
        "loggly": {
            "level": "ERROR",
            "class": "loggly.handlers.HTTPSHandler",
            "formatter": "json",
            "url": f"https://logs-01.loggly.com/inputs/{DEV_LOGGLY_TOKEN}/tag/python",
        },
    },
    "loggers": {
        "bookops-watchdog": {
            "handlers": ["console", "file", "loggly"],
            "level": "DEBUG",
            "propagate": True,
        }
    },
}


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

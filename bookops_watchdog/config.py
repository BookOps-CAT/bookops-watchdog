import logging
import os
import yaml
from typing import Dict, List, Tuple

from bookops_watchdog.errors import WatchdogError


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


def add_environ_variables(**kwargs) -> None:
    """
    Persist app configuration settings in the environmental variables
    """

    for k, v in kwargs.items():
        os.environ[k] = v


def validate_directory(data_dir: str) -> None:
    """
    Validates the directory structure exists and if not
    creates one

    Args:
        data_dir:               data directory path
    """

    if not os.path.isdir(data_dir):
        os.mkdir(data_dir)


def configure_app(env: str = "dev") -> Tuple:
    """
    Configures sets up workspace for the app.

    Args:
        env:            dev or prod

    Returns:
        log_fh, log_token, handlers
    """

    conf = get_config_settings(env)
    log_token = conf["loggly_token"]
    handlers = conf["log_handlers"]
    data_dir = get_app_data_dir(env)
    log_fh = get_log_fh(data_dir)
    datastore_fh = get_datastore_fh(data_dir)

    validate_directory(data_dir)

    add_environ_variables(
        watchdog_store=datastore_fh,
        watchdog_sendGrid=conf["sendGrid_key"],
        watchdog_ftp_host=conf["ftp_host"],
        watchdog_ftp_user=conf["ftp_user"],
        watchdog_ftp_passw=conf["ftp_passw"],
        watchdog_ftp_folder=conf["ftp_folder"],
    )
    return (log_fh, log_token, handlers)


def construct_config_path(env: str) -> str:
    return os.path.join(
        os.environ["USERPROFILE"], f".bookops-watchdog\\config_variables_{env}.yaml"
    )


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


def get_app_data_dir(env: str) -> str:
    """
    Returns app data directory based on dev or prod mode
    """
    data_dir = None
    if env == "dev":
        data_dir = os.path.join(os.environ["LOCALAPPDATA"], "TEMP\\Bookops-Watchdog")
    elif env == "prod":
        data_dir = os.path.join(os.environ["LOCALAPPDATA"], "Bookops-Watchdog")
    else:
        pass
    return data_dir


def get_config_settings(env: str = "dev") -> Dict:
    """
    Retrieves configuration from YAML file
    """
    config_fh = construct_config_path(env)
    with open(config_fh, "r") as f:
        data = yaml.safe_load(f)
        return data


def get_datastore_fh(data_dir: str) -> str:
    """
    Constructs datastore file handle

    Args:
        data_dir:           app data directory

    Returns:
        datastore_fh:       app datastore file handle
    """
    return os.path.join(data_dir, "datastore.db")


def get_log_fh(data_dir: str) -> str:
    """
    Constructs log file handle

    Args:
        data_dir:           app data directory

    Returns:
        log_fh:             logger file handle
    """
    return os.path.join(data_dir, "watchdog.log")


def watchdog_logging_config(log_fh: str, log_token: str, handlers: List) -> Dict:
    """
    Returns dictionary with logger configuration based on environment

    Args:
        log_fh:                     log file handle to use
        log_token:                  loggly access token
        handlers:                   list of handlers to use

    Returns:                        logging configuration as dictionary
    """

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
                "filename": log_fh,
                "formatter": "brief",
                "maxBytes": 1024 * 1024,
                "backupCount": 5,
            },
            "loggly": {
                "level": "ERROR",
                "class": "loggly.handlers.HTTPSHandler",
                "formatter": "json",
                "url": f"https://logs-01.loggly.com/inputs/{log_token}/tag/python",
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

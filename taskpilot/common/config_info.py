"""Configuration information for the TaskPilot Project"""
import logging
import sys


VERSION = "v1"
HOST = "0.0.0.0"

API_PORT = 8080
API_APP = "api_main:app"

DB_URL = "http://taskpilot-elastic:9200"

LOGGING_FORMAT = (
    "[%(asctime)s] [PID: %(process)d] [%(filename)s] "
    "[%(funcName)s: %(lineno)s] [%(levelname)s] %(message)s"
)


def get_logger():
    """
    Generates logger instance, logging messages in a specified format
    """
    logger = logging.getLogger("taskpilot")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(LOGGING_FORMAT)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    logger.handlers.clear()
    logger.addHandler(handler)

    return logger


class APIConstants:
    """Constants used in the TaskPilot API."""
    ROUTES = {

    }

"""Configuration information for the TaskPilot Project"""
import logging
import sys
import hashlib


HOST = "0.0.0.0"

API_PORT = 8080
API_APP = "api_main:app"

DB_URL = "http://taskpilot-elastic:9200"

LOGGING_FORMAT = (
    "[%(asctime)s] [PID: %(process)d] [%(filename)s] "
    "[%(funcName)s: %(lineno)s] [%(levelname)s] %(message)s"
)


def hash_password(password: str) -> str:
   password_bytes = password.encode('utf-8')
   hash_object = hashlib.sha256(password_bytes)
   return hash_object.hexdigest()


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


class Entities:
    """Constants for accepted entities"""
    USER = "user"
    PROJECT = "project"
    TICKET = "ticket"
    COMMENT = "comment"


DB_INDEXES = {
    Entities.USER: "users",
    Entities.PROJECT: "projects",
    Entities.TICKET: "tickets",
    Entities.COMMENT: "comments"
}


class APIOperations:
    """Constants used in the TaskPilot API Operations"""
    USERS_GET = "users_get"
    USERS_CREATE = "users_create"
    USERS_UPDATE = "users_update"
    USERS_DELETE = "users_delete"
    USERS_ALL = "users_all"
    USERS_SEARCH = "users_search"

    PROJECTS_GET = "projects_get"
    PROJECTS_CREATE = "projects_create"
    PROJECTS_UPDATE = "projects_update"
    PROJECTS_DELETE = "projects_delete"
    PROJECTS_ALL = "projects_all"
    PROJECTS_SEARCH = "projects_search"

    TICKETS_GET = "tickets_get"
    TICKETS_CREATE = "tickets_create"
    TICKETS_UPDATE = "tickets_update"
    TICKETS_DELETE = "tickets_delete"
    TICKETS_ALL = "tickets_all"
    TICKETS_SEARCH = "tickets_search"

    COMMENTS_GET = "comments_get"
    COMMENTS_CREATE = "comments_create"
    COMMENTS_UPDATE = "comments_update"
    COMMENTS_DELETE = "comments_delete"
    COMMENTS_ALL = "comments_all"
    COMMENTS_SEARCH = "comments_search"


API_ROUTES = {
    APIOperations.USERS_GET: "/api/users/{user_id}",
    APIOperations.USERS_CREATE: "/api/users",
    APIOperations.USERS_UPDATE: "/api/users/{user_id}",
    APIOperations.USERS_DELETE: "/api/users/{user_id}",
    APIOperations.USERS_ALL: "/api/users",
    APIOperations.USERS_SEARCH: "/api/users/search"
}

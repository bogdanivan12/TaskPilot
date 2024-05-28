"""Configuration information for the TaskPilot Project"""
import logging
import sys
import hashlib
import datetime


HOST = "0.0.0.0"

API_PORT = 8080
API_APP = "api_main:app"

DB_PORT = 9200
UI_PORT = 8081

DB_URL = f"http://taskpilot-elastic:{DB_PORT}"
API_URL = f"http://taskpilot-api:{API_PORT}"

LOGGING_FORMAT = (
    "[%(asctime)s] [PID: %(process)d] [%(filename)s] "
    "[%(funcName)s: %(lineno)s] [%(levelname)s] %(message)s"
)


def hash_password(password: str) -> str:
    """Hash a password using SHA-256 algorithm"""
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


def get_current_time() -> str:
    """Get the current time in a formatted string"""
    return str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))


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


class TicketTypes:
    """Constants for accepted ticket types"""
    EPIC = "Epic"
    STORY = "Story"
    TASK = "Task"
    BUG = "Bug"


class TicketPriorities:
    """Constants for accepted ticket priorities"""
    LOW = "Low"
    NORMAL = "Normal"
    HIGH = "High"
    CRITICAL = "Critical"


class TicketStatuses:
    """Constants for accepted ticket statuses"""
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"
    CLOSED = "Closed"


class APIOperations:
    """Constants used in the TaskPilot API Operations"""
    USERS_GET = "users_get"
    USERS_CREATE = "users_create"
    USERS_UPDATE = "users_update"
    USERS_DELETE = "users_delete"
    USERS_ALL = "users_all"
    USERS_SEARCH = "users_search"
    USERS_ALL_ASSIGNED_TICKETS = "users_all_assigned_tickets"
    USERS_ASSIGN_TICKET = "users_assign_ticket"
    USERS_UNASSIGN_TICKET = "users_unassign_ticket"
    USERS_ADD_FAVORITE_TICKET = "users_add_favorite_ticket"
    USERS_REMOVE_FAVORITE_TICKET = "users_remove_favorite_ticket"
    USERS_LOGIN = "users_login"

    PROJECTS_GET = "projects_get"
    PROJECTS_CREATE = "projects_create"
    PROJECTS_UPDATE = "projects_update"
    PROJECTS_DELETE = "projects_delete"
    PROJECTS_ALL = "projects_all"
    PROJECTS_SEARCH = "projects_search"
    PROJECTS_ALL_TICKETS = "projects_all_tickets"
    PROJECTS_ADD_MEMBER = "projects_add_member"
    PROJECTS_REMOVE_MEMBER = "projects_remove_member"

    TICKETS_GET = "tickets_get"
    TICKETS_CREATE = "tickets_create"
    TICKETS_UPDATE = "tickets_update"
    TICKETS_DELETE = "tickets_delete"
    TICKETS_ALL = "tickets_all"
    TICKETS_SEARCH = "tickets_search"
    TICKETS_ALL_COMMENTS = "tickets_all_comments"
    TICKETS_ALL_CHILDREN = "tickets_all_children"
    TICKETS_CHANGE_STATUS = "tickets_change_status"

    COMMENTS_GET = "comments_get"
    COMMENTS_CREATE = "comments_create"
    COMMENTS_DELETE = "comments_delete"
    COMMENTS_ALL = "comments_all"
    COMMENTS_SEARCH = "comments_search"


API_ROUTES = {
    APIOperations.USERS_GET: "/api/users/{user_id}",
    APIOperations.USERS_CREATE: "/api/users",
    APIOperations.USERS_UPDATE: "/api/users/{user_id}",
    APIOperations.USERS_DELETE: "/api/users/{user_id}",
    APIOperations.USERS_ALL: "/api/users",
    APIOperations.USERS_SEARCH: "/api/users/search",
    APIOperations.USERS_ALL_ASSIGNED_TICKETS: "/api/users/{user_id}/tickets"
                                              "/assigned",
    APIOperations.USERS_ASSIGN_TICKET: "/api/users/{user_id}/tickets"
                                       "/assigned/{ticket_id}",
    APIOperations.USERS_UNASSIGN_TICKET: "/api/users/{user_id}/tickets"
                                         "/assigned/{ticket_id}",
    APIOperations.USERS_ADD_FAVORITE_TICKET: "/api/users/{user_id}/tickets"
                                             "/favorites/{ticket_id}",
    APIOperations.USERS_REMOVE_FAVORITE_TICKET: "/api/users/{user_id}/tickets"
                                                "/favorites/{ticket_id}",
    APIOperations.USERS_LOGIN: "/api/users/login",

    APIOperations.PROJECTS_GET: "/api/projects/{project_id}",
    APIOperations.PROJECTS_CREATE: "/api/projects",
    APIOperations.PROJECTS_UPDATE: "/api/projects/{project_id}",
    APIOperations.PROJECTS_DELETE: "/api/projects/{project_id}",
    APIOperations.PROJECTS_ALL: "/api/projects",
    APIOperations.PROJECTS_SEARCH: "/api/projects/search",
    APIOperations.PROJECTS_ALL_TICKETS: "/api/projects/{project_id}/tickets",
    APIOperations.PROJECTS_ADD_MEMBER: "/api/projects/{project_id}/members"
                                       "/{user_id}",
    APIOperations.PROJECTS_REMOVE_MEMBER: "/api/projects/{project_id}/members"
                                          "/{user_id}",

    APIOperations.TICKETS_GET: "/api/tickets/{ticket_id}",
    APIOperations.TICKETS_CREATE: "/api/tickets",
    APIOperations.TICKETS_UPDATE: "/api/tickets/{ticket_id}",
    APIOperations.TICKETS_DELETE: "/api/tickets/{ticket_id}",
    APIOperations.TICKETS_ALL: "/api/tickets",
    APIOperations.TICKETS_SEARCH: "/api/tickets/search",
    APIOperations.TICKETS_ALL_COMMENTS: "/api/tickets/{ticket_id}/comments",
    APIOperations.TICKETS_ALL_CHILDREN: "/api/tickets/{ticket_id}"
                                        "/children-tickets",
    APIOperations.TICKETS_CHANGE_STATUS: "/api/tickets/{ticket_id}/status",

    APIOperations.COMMENTS_GET: "/api/comments/{comment_id}",
    APIOperations.COMMENTS_CREATE: "/api/comments",
    APIOperations.COMMENTS_DELETE: "/api/comments/{comment_id}",
    APIOperations.COMMENTS_ALL: "/api/comments",
    APIOperations.COMMENTS_SEARCH: "/api/comments/search"
}


class UIPages:
    """Constants for the TaskPilot UI Pages"""
    HOME = "home"
    LOGIN = "login"
    REGISTER = "register"
    PROJECTS = "projects"
    PROJECT = "project"
    TICKETS = "tickets"
    TICKET = "ticket"
    PROFILE = "profile"
    NOT_FOUND = "not_found"


UI_ROUTES = {
    UIPages.HOME: "/",
    UIPages.LOGIN: "/login",
    UIPages.REGISTER: "/register",
    UIPages.PROJECTS: "/projects",
    UIPages.PROJECT: "/projects/{project_id}",
    UIPages.TICKET: "/projects/{project_id}/tickets/{ticket_id}",
    UIPages.PROFILE: "/profile",
    UIPages.NOT_FOUND: "/404"
}

UNRESTRICTED_PAGE_ROUTES = [
    UI_ROUTES[UIPages.LOGIN],
    UI_ROUTES[UIPages.REGISTER],
    UI_ROUTES[UIPages.NOT_FOUND]
]

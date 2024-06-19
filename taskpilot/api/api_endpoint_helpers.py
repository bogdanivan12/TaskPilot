"""File containing helper functions for the endpoints of the API service."""
import datetime
import uuid

from taskpilot.api import db_operations as db
from taskpilot.api import ai_interactions as ai
from taskpilot.common import config_info, api_request_classes as api_req
from taskpilot.common import models
from taskpilot.api import api_response_classes as api_resp

logger = config_info.get_logger()


def get_user(user_id: str) -> api_resp.GetUserResponse:
    """
    Get a user by id
    """
    user_id = user_id.lower()

    index = config_info.DB_INDEXES[config_info.Entities.USER]
    db_get_result = db.get_item(index, user_id)

    if not db_get_result:
        response = api_resp.GetUserResponse(
            message=f"User with id '{user_id}' not found",
            code=404,
            result=False
        )
        logger.error(response.message)
        return response

    user = models.User.parse_obj(db_get_result)
    response = api_resp.GetUserResponse(
        message=f"User with id '{user_id}' retrieved successfully",
        user=user
    )
    logger.info(response.message)
    return response


def create_user(user_req: api_req.CreateUserRequest) -> api_resp.Response:
    """
    Create a user
    """
    index = config_info.DB_INDEXES[config_info.Entities.USER]
    if not user_req.username:
        user_req.username = str(uuid.uuid4())
    user_dict = user_req.dict()
    password = user_dict.pop("password")
    hashed_password = config_info.hash_password(password)
    user_dict["hashed_password"] = hashed_password
    user_dict["username"] = user_dict["username"].lower()
    user = models.User.parse_obj(user_dict)

    existent_user = get_user(user.username).user
    if existent_user is not None:
        response = api_resp.Response(
            message=f"Failed to create user with id '{user.username}': user"
                    f" already exists",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    db_create_result = db.create_item(index, user.dict(), user.username)

    if not db_create_result:
        response = api_resp.Response(
            message=f"Failed to create user with id '{user_req.username}'",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    response = api_resp.Response(
        message=f"User with id '{db_create_result}' created successfully"
    )
    logger.info(response.message)
    return response


def update_user(user_id: str,
                user_req: api_req.UpdateUserRequest) -> api_resp.Response:
    """
    Update a user
    """
    user_id = user_id.lower()

    index = config_info.DB_INDEXES[config_info.Entities.USER]
    user_dict = user_req.dict()
    password = user_dict.pop("password")
    hashed_password = config_info.hash_password(password)
    user_dict["hashed_password"] = hashed_password
    user_dict["username"] = user_id
    user = models.User.parse_obj(user_dict)

    db_update_result = db.update_item(index, user_id, user.dict())

    if not db_update_result:
        response = api_resp.Response(
            message=f"Failed to update user with id '{user_id}'",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    response = api_resp.Response(
        message=f"User with id '{user_id}' updated successfully"
    )
    logger.info(response.message)
    return response


def delete_user(user_id: str) -> api_resp.Response:
    """
    Delete a user
    """
    user_id = user_id.lower()

    index = config_info.DB_INDEXES[config_info.Entities.USER]
    db_delete_result = db.delete_item(index, user_id)

    if not db_delete_result:
        response = api_resp.Response(
            message=f"Failed to delete user with id '{user_id}'",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    response = api_resp.Response(
        message=f"User with id '{user_id}' deleted successfully"
    )
    logger.info(response.message)
    return response


def get_all_users() -> api_resp.GetAllUsersResponse:
    """
    Get all users
    """
    index = config_info.DB_INDEXES[config_info.Entities.USER]
    db_get_all_result = db.get_all_items(index)

    if db_get_all_result is None:
        response = api_resp.GetAllUsersResponse(
            message="Failed to retrieve all users",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    users = [models.User.parse_obj(user)
             for user in db_get_all_result.values()]

    users.sort(key=lambda user: user.username)

    response = api_resp.GetAllUsersResponse(
        message="All users retrieved successfully",
        users=users
    )
    logger.info(response.message)
    return response


def search_users(search_req: api_req.SearchUsersRequest
                 ) -> api_resp.GetAllUsersResponse:
    """
    Search for users
    """
    search_req.username = search_req.username.lower()

    index = config_info.DB_INDEXES[config_info.Entities.USER]
    query_dict = search_req.dict()
    query_dict = {
        field: value
        for field, value in query_dict.items()
        if value is not None
    }

    db_search_result = db.search_items(index, query_dict)

    if db_search_result is None:
        response = api_resp.GetAllUsersResponse(
            message="Failed to search for users",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    users = [models.User.parse_obj(user)
             for user in db_search_result.values()]

    users.sort(key=lambda user: user.username)

    response = api_resp.GetAllUsersResponse(
        message="Users retrieved successfully",
        users=users
    )
    logger.info(response.message)
    print(response)
    return response


def get_all_assigned_tickets(user_id: str) -> api_resp.GetAllTicketsResponse:
    """
    Get all tickets assigned to a user
    """
    user_id = user_id.lower()

    index = config_info.DB_INDEXES[config_info.Entities.TICKET]
    query_dict = {"assignee": user_id}

    db_search_result = db.search_items(index, query_dict)

    if db_search_result is None:
        response = api_resp.GetAllTicketsResponse(
            message=f"Failed to retrieve all tickets assigned to user with id"
                    f" '{user_id}'",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    tickets = [models.Ticket.parse_obj(ticket)
               for ticket in db_search_result.values()]

    tickets.sort(key=lambda ticket: datetime.datetime.strptime(
        ticket.modified_at, config_info.DATETIME_FORMAT), reverse=True)

    response = api_resp.GetAllTicketsResponse(
        message=f"All tickets assigned to user with id '{user_id}' retrieved"
                f" successfully",
        tickets=tickets
    )
    logger.info(response.message)
    return response


def assign_ticket(user_id: str, ticket_id: str) -> api_resp.Response:
    """
    Assign a ticket to a user
    """
    user_id = user_id.lower()

    ticket = get_ticket(ticket_id).ticket
    if ticket is None:
        response = api_resp.Response(
            message=f"Failed to assign ticket with id '{ticket_id}' to user"
                    f" with id '{user_id}' due to non-existent ticket",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    index = config_info.DB_INDEXES[config_info.Entities.TICKET]
    ticket_dict = {"assignee": user_id}

    db_update_result = db.update_item(index, ticket_id, ticket_dict)

    if not db_update_result:
        response = api_resp.Response(
            message=f"Failed to assign ticket with id '{ticket_id}' to user"
                    f" with id '{user_id}'",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    response = api_resp.Response(
        message=f"Ticket with id '{ticket_id}' assigned to user with id"
                f" '{user_id}' successfully"
    )
    logger.info(response.message)
    return response


def unassign_ticket(user_id: str, ticket_id: str) -> api_resp.Response:
    """
    Unassign a ticket from a user
    """
    user_id = user_id.lower()

    index = config_info.DB_INDEXES[config_info.Entities.TICKET]
    ticket_dict = {"assignee": None}

    db_update_result = db.update_item(index, ticket_id, ticket_dict)

    if not db_update_result:
        response = api_resp.Response(
            message=f"Failed to unassign ticket with id '{ticket_id}' from"
                    f" user with id '{user_id}'",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    response = api_resp.Response(
        message=f"Ticket with id '{ticket_id}' unassigned from user with id"
                f" '{user_id}' successfully"
    )
    logger.info(response.message)
    return response


def add_favorite_ticket(user_id: str, ticket_id: str) -> api_resp.Response:
    """
    Add a ticket to a user's favorites
    """
    user_id = user_id.lower()

    ticket = get_ticket(ticket_id).ticket
    if ticket is None:
        response = api_resp.Response(
            message=f"Failed to add ticket with id '{ticket_id}' to user with"
                    f" id '{user_id}' favorites due to non-existent ticket",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    index = config_info.DB_INDEXES[config_info.Entities.USER]
    favorite_tickets = set(get_user(user_id).user.favorite_tickets)
    favorite_tickets.add(ticket_id)
    user_update_dict = {"favorite_tickets": list(favorite_tickets)}

    db_update_result = db.update_item(index, user_id, user_update_dict)

    if not db_update_result:
        response = api_resp.Response(
            message=f"Failed to add ticket with id '{ticket_id}' to user with"
                    f" id '{user_id}' favorites",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    response = api_resp.Response(
        message=f"Ticket with id '{ticket_id}' added to user with id"
                f" '{user_id}' favorites successfully"
    )
    logger.info(response.message)
    return response


def remove_favorite_ticket(user_id: str, ticket_id: str) -> api_resp.Response:
    """
    Remove a ticket from a user's favorites
    """
    user_id = user_id.lower()

    index = config_info.DB_INDEXES[config_info.Entities.USER]
    favorite_tickets = set(get_user(user_id).user.favorite_tickets)
    favorite_tickets.discard(ticket_id)
    favorite_tickets = list(favorite_tickets)

    user_update_dict = {"favorite_tickets": favorite_tickets}

    db_update_result = db.update_item(index, user_id, user_update_dict)

    if not db_update_result:
        response = api_resp.Response(
            message=f"Failed to remove ticket with id '{ticket_id}' from user"
                    f" with id '{user_id}' favorites",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    response = api_resp.Response(
        message=f"Ticket with id '{ticket_id}' removed from user with id"
                f" '{user_id}' favorites successfully"
    )
    logger.info(response.message)
    return response


def login_user(login_req: api_req.LoginRequest) -> api_resp.Response:
    """
    Log in a user
    """
    username = login_req.username.lower()
    password = login_req.password
    hashed_password = config_info.hash_password(password)
    user = get_user(username).user

    if user is None:
        response = api_resp.Response(
            message="Failed to log in: incorrect username or password",
            code=401,
            result=False
        )
        logger.error(response.message)
        return response

    if user.hashed_password == hashed_password:
        response = api_resp.Response(
            message=f"User with id '{username}' logged in successfully"
        )
        logger.info(response.message)
        return response

    response = api_resp.Response(
        message="Failed to log in: incorrect username or password",
        code=401,
        result=False
    )
    logger.error(response.message)
    return response


def get_user_projects(user_id: str) -> api_resp.GetAllProjectsResponse:
    """
    Get all projects for a user
    """
    user_id = user_id.lower()

    all_projects = get_all_projects().projects
    user_projects = [
        project for project in all_projects
        if user_id in project.members or user_id == project.created_by
    ]

    response = api_resp.GetAllProjectsResponse(
        message=f"All projects for user with id '{user_id}' retrieved"
                f" successfully",
        projects=user_projects
    )
    logger.info(response.message)
    return response


def get_project(project_id: str) -> api_resp.GetProjectResponse:
    """
    Get a project by id
    """
    index = config_info.DB_INDEXES[config_info.Entities.PROJECT]
    db_get_result = db.get_item(index, project_id)

    if not db_get_result:
        response = api_resp.GetProjectResponse(
            message=f"Project with id '{project_id}' not found",
            code=404,
            result=False
        )
        logger.error(response.message)
        return response

    project = models.Project.parse_obj(db_get_result)
    response = api_resp.GetProjectResponse(
        message=f"Project with id '{project_id}' retrieved successfully",
        project=project
    )
    logger.info(response.message)
    return response


def create_project(
        project_req: api_req.CreateProjectRequest) -> api_resp.Response:
    """
    Create a project
    """
    index = config_info.DB_INDEXES[config_info.Entities.PROJECT]
    if not project_req.project_id:
        project_req.project_id = str(uuid.uuid4())
    project_dict = project_req.dict()
    project_dict["created_at"] = config_info.get_current_time()
    project_dict["modified_at"] = project_dict["created_at"]
    project_dict["modified_by"] = project_dict["created_by"]
    project = models.Project.parse_obj(project_dict)

    owner_user = get_user(project.created_by).user
    if owner_user is None:
        response = api_resp.Response(
            message=f"Failed to create project with id '{project.project_id}'"
                    f" due to non-existent user with id"
                    f" '{project.created_by}'",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    members = set(project.members)
    for member_id in members:
        member_user = get_user(member_id).user
        if member_user is None:
            response = api_resp.Response(
                message=f"Failed to create project with id"
                        f" '{project.project_id}' due to non-existent member"
                        f" with id '{member_id}'",
                code=424,
                result=False
            )
            logger.error(response.message)
            return response

    db_create_result = db.create_item(
        index, project.dict(), project.project_id)

    if not db_create_result:
        response = api_resp.Response(
            message=f"Failed to create project with id '{project.project_id}'",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    response = api_resp.Response(
        message=f"Project with id '{project.project_id}' created successfully"
    )
    logger.info(response.message)
    return response


def update_project(
        project_id: str,
        project_req: api_req.UpdateProjectRequest) -> api_resp.Response:
    """
    Update a project
    """
    index = config_info.DB_INDEXES[config_info.Entities.PROJECT]
    project_dict = project_req.dict()
    project_dict["modified_at"] = config_info.get_current_time()

    modified_by = project_dict.get("modified_by")
    modified_by_user = get_user(modified_by).user
    if modified_by_user is None:
        response = api_resp.Response(
            message=f"Failed to update project with id '{project_id}' due to"
                    f" non-existent user with id {modified_by}",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    members = set(project_dict.get("members", []))
    for member_id in members:
        member_user = get_user(member_id).user
        if member_user is None:
            response = api_resp.Response(
                message=f"Failed to update project with id '{project_id}' due"
                        f" to non-existent member with id '{member_id}'",
                code=424,
                result=False
            )
            logger.error(response.message)
            return response

    db_update_result = db.update_item(index, project_id, project_dict)

    if not db_update_result:
        response = api_resp.Response(
            message=f"Failed to update project with id '{project_id}'",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    response = api_resp.Response(
        message=f"Project with id '{project_id}' updated successfully"
    )
    logger.info(response.message)
    return response


def delete_project(project_id: str) -> api_resp.Response:
    """
    Delete a project
    """
    index = config_info.DB_INDEXES[config_info.Entities.PROJECT]

    child_tickets_req = api_req.SearchTicketsRequest(parent_project=project_id)
    child_tickets_resp = search_tickets(child_tickets_req)
    child_tickets = [ticket.ticket_id for ticket in child_tickets_resp.tickets]

    for ticket_id in child_tickets:
        delete_ticket_response = delete_ticket(ticket_id)
        if not delete_ticket_response.result:
            response = api_resp.Response(
                message=f"Failed to delete linked project with id"
                        f" '{project_id}' due to failed ticket deletion:"
                        f" {delete_ticket_response.message}",
                code=424,
                result=False
            )
            logger.error(response.message)
            return response

    db_delete_result = db.delete_item(index, project_id)

    if not db_delete_result:
        response = api_resp.Response(
            message=f"Failed to delete project with id '{project_id}'",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    response = api_resp.Response(
        message=f"Project with id '{project_id}' deleted successfully"
    )
    logger.info(response.message)
    return response


def get_all_projects() -> api_resp.GetAllProjectsResponse:
    """
    Get all projects
    """
    index = config_info.DB_INDEXES[config_info.Entities.PROJECT]
    db_get_all_result = db.get_all_items(index)

    if db_get_all_result is None:
        response = api_resp.GetAllProjectsResponse(
            message="Failed to retrieve all projects",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    projects = [models.Project.parse_obj(project)
                for project in db_get_all_result.values()]

    projects.sort(key=lambda project: datetime.datetime.strptime(
        project.modified_at, config_info.DATETIME_FORMAT), reverse=True)

    response = api_resp.GetAllProjectsResponse(
        message="All projects retrieved successfully",
        projects=projects
    )
    logger.info(response.message)
    return response


def search_projects(search_req: api_req.SearchProjectsRequest
                          ) -> api_resp.GetAllProjectsResponse:
    """
    Search for projects
    """
    index = config_info.DB_INDEXES[config_info.Entities.PROJECT]
    query_dict = search_req.dict()
    query_dict = {
        field: value
        for field, value in query_dict.items()
        if value is not None
    }

    db_search_result = db.search_items(index, query_dict)

    if db_search_result is None:
        response = api_resp.GetAllProjectsResponse(
            message="Failed to search for projects",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    projects = [models.Project.parse_obj(project)
                for project in db_search_result.values()]

    projects.sort(key=lambda project: datetime.datetime.strptime(
        project.modified_at, config_info.DATETIME_FORMAT), reverse=True)

    response = api_resp.GetAllProjectsResponse(
        message="Projects retrieved successfully",
        projects=projects
    )
    logger.info(response.message)

    return response


def get_all_tickets_in_project(project_id: str
                               ) -> api_resp.GetAllTicketsResponse:
    """
    Get all tickets in a project
    """
    index = config_info.DB_INDEXES[config_info.Entities.TICKET]
    query_dict = {"parent_project": project_id}

    db_search_result = db.search_items(index, query_dict)

    if db_search_result is None:
        response = api_resp.GetAllTicketsResponse(
            message=f"Failed to retrieve all tickets in project with id"
                    f" '{project_id}'",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    tickets = [models.Ticket.parse_obj(ticket)
               for ticket in db_search_result.values()]

    tickets.sort(key=lambda ticket: datetime.datetime.strptime(
        ticket.modified_at, config_info.DATETIME_FORMAT), reverse=True)

    response = api_resp.GetAllTicketsResponse(
        message=f"All tickets in project with id '{project_id}' retrieved"
                f" successfully",
        tickets=tickets
    )
    logger.info(response.message)
    return response


def add_member_to_project(project_id: str,
                          user_id: str) -> api_resp.Response:
    """
    Add a member to a project
    """
    projects_index = config_info.DB_INDEXES[config_info.Entities.PROJECT]
    project = get_project(project_id).project
    if project is None:
        response = api_resp.Response(
            message=f"Failed to add user with id '{user_id}' to project with"
                    f" id '{project_id}' due to non-existent project",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    user = get_user(user_id).user
    if user is None:
        response = api_resp.Response(
            message=f"Failed to add user with id '{user_id}' to project with"
                    f" id '{project_id}' due to non-existent user",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    project_dict = project.dict()
    members = project_dict["members"]
    members.add(user_id)
    project_dict["members"] = members

    db_update_project_result = db.update_item(projects_index, project_id,
                                              project_dict)

    if not db_update_project_result:
        response = api_resp.Response(
            message=f"Failed to add user with id '{user_id}' to project with"
                    f" id '{project_id}'",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    response = api_resp.Response(
        message=f"User with id '{user_id}' added to project with id"
                f" '{project_id}' successfully"
    )
    logger.info(response.message)
    return response


def remove_member_from_project(project_id: str,
                               user_id: str) -> api_resp.Response:
    """
    Remove a member from a project
    """
    projects_index = config_info.DB_INDEXES[config_info.Entities.PROJECT]
    project = get_project(project_id).project
    if project is None:
        response = api_resp.Response(
            message=f"Failed to remove user with id '{user_id}' from project"
                    f" with id '{project_id}' due to non-existent project",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    project_dict = project.dict()
    members = set(project_dict["members"])
    members.discard(user_id)
    project_dict["members"] = list(members)

    db_update_project_result = db.update_item(projects_index, project_id,
                                              project_dict)

    user = get_user(user_id).user
    if user is None:
        response = api_resp.Response(
            message=f"Failed to remove user with id '{user_id}' from project"
                    f" with id '{project_id}' due to non-existent user",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    if not db_update_project_result:
        response = api_resp.Response(
            message=f"Failed to remove user with id '{user_id}' from project"
                    f" with id '{project_id}'",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    response = api_resp.Response(
        message=f"User with id '{user_id}' removed from project with id"
                f" '{project_id}' successfully"
    )
    logger.info(response.message)
    return response


def is_user_owner_of_project(project_id: str,
                             user_id: str) -> api_resp.Response:
    """
    Check if a user is the owner of a project
    """
    project = get_project(project_id).project
    if project is None:
        response = api_resp.Response(
            message=f"Failed to check if user with id '{user_id}' is owner of"
                    f" project with id '{project_id}' due to non-existent"
                    f" project",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    user = get_user(user_id).user
    if user is None:
        response = api_resp.Response(
            message=f"Failed to check if user with id '{user_id}' is owner of"
                    f" project with id '{project_id}' due to non-existent"
                    f" user",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    if project.created_by == user_id or user.is_admin:
        response = api_resp.Response(
            message=f"User with id '{user_id}' is the owner of project with"
                    f" id '{project_id}'",
            result=True
        )
        logger.info(response.message)
        return response

    response = api_resp.Response(
        message=f"User with id '{user_id}' is not the owner of project with"
                f" id '{project_id}'",
        result=False
    )
    logger.info(response.message)
    return response


def is_user_member_of_project(project_id: str,
                              user_id: str) -> api_resp.Response:
    """
    Check if a user is a member of a project
    """
    project = get_project(project_id).project
    if project is None:
        response = api_resp.Response(
            message=f"Failed to check if user with id '{user_id}' is member of"
                    f" project with id '{project_id}' due to non-existent"
                    f" project",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    user = get_user(user_id).user
    if user is None:
        response = api_resp.Response(
            message=f"Failed to check if user with id '{user_id}' is member of"
                    f" project with id '{project_id}' due to non-existent"
                    f" user",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    if (user_id in project.members
            or project.created_by == user_id
            or user.is_admin):
        response = api_resp.Response(
            message=f"User with id '{user_id}' is a member of project with"
                    f" id '{project_id}'",
            result=True
        )
        logger.info(response.message)
        return response

    response = api_resp.Response(
        message=f"User with id '{user_id}' is not a member of project with"
                f" id '{project_id}'",
        result=False
    )
    logger.info(response.message)
    return response


def get_ticket(ticket_id: str) -> api_resp.GetTicketResponse:
    """
    Get a ticket by id
    """
    index = config_info.DB_INDEXES[config_info.Entities.TICKET]
    db_get_result = db.get_item(index, ticket_id)

    if not db_get_result:
        response = api_resp.GetTicketResponse(
            message=f"Ticket with id '{ticket_id}' not found",
            code=404,
            result=False
        )
        logger.error(response.message)
        return response

    ticket = models.Ticket.parse_obj(db_get_result)
    response = api_resp.GetTicketResponse(
        message=f"Ticket with id '{ticket_id}' retrieved successfully",
        ticket=ticket
    )
    logger.info(response.message)
    return response


def create_ticket(
        ticket_req: api_req.CreateTicketRequest) -> api_resp.Response:
    """
    Create a ticket
    """
    if not ticket_req.ticket_id:
        ticket_req.ticket_id = str(uuid.uuid4())
    created_by = get_user(ticket_req.created_by).user
    assignee = (
        get_user(ticket_req.assignee).user
        if ticket_req.assignee else None
    )
    if (created_by is None
            or (assignee is None and ticket_req.assignee is not None)):
        response = api_resp.Response(
            message=f"Failed to create ticket with id '{ticket_req.ticket_id}'"
                    f" due to non-existent user",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    parent_project = (
        get_project(ticket_req.parent_project).project
        if ticket_req.parent_project else None
    )
    if parent_project is None:
        response = api_resp.Response(
            message=f"Failed to create ticket with id '{ticket_req.ticket_id}'"
                    f" due to non-existent project",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    if ticket_req.parent_ticket:
        parent_ticket = get_ticket(ticket_req.parent_ticket).ticket
        if parent_ticket is None and ticket_req.parent_ticket is not None:
            response = api_resp.Response(
                message=f"Failed to create ticket with id"
                        f" '{ticket_req.ticket_id}'"
                        f" due to non-existent parent ticket",
                code=424,
                result=False
            )
            logger.error(response.message)
            return response

    index = config_info.DB_INDEXES[config_info.Entities.TICKET]
    ticket_dict = ticket_req.dict()
    ticket_dict["created_at"] = config_info.get_current_time()
    ticket_dict["modified_at"] = ticket_dict["created_at"]
    ticket_dict["modified_by"] = ticket_dict["created_by"]
    ticket = models.Ticket.parse_obj(ticket_dict)

    db_create_result = db.create_item(
        index, ticket.dict(), ticket.ticket_id)

    if not db_create_result:
        response = api_resp.Response(
            message=f"Failed to create ticket with id '{ticket.ticket_id}'",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    db.update_item(
        config_info.DB_INDEXES[config_info.Entities.PROJECT],
        ticket.parent_project,
        {"next_ticket_id": parent_project.next_ticket_id + 1}
    )

    response = api_resp.Response(
        message=f"Ticket with id '{ticket.ticket_id}' created successfully"
    )
    logger.info(response.message)
    return response


def update_ticket(
        ticket_id: str,
        ticket_req: api_req.UpdateTicketRequest) -> api_resp.Response:
    """
    Update a ticket
    """
    modified_by = get_user(ticket_req.modified_by).user
    assignee = (get_user(ticket_req.assignee).user
                if ticket_req.assignee else None)
    if (modified_by is None or
            (assignee is None and ticket_req.assignee is not None)):
        response = api_resp.Response(
            message=f"Failed to update ticket with id '{ticket_id}' due to"
                    f" non-existent user",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    parent_project = get_project(ticket_req.parent_project).project
    if parent_project is None:
        response = api_resp.Response(
            message=f"Failed to update ticket with id '{ticket_id}' due to"
                    f" non-existent project",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    parent_ticket = get_ticket(ticket_req.parent_ticket).ticket
    if parent_ticket is None and ticket_req.parent_ticket is not None:
        response = api_resp.Response(
            message=f"Failed to update ticket with id '{ticket_id}' due to"
                    f" non-existent parent ticket",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    index = config_info.DB_INDEXES[config_info.Entities.TICKET]
    ticket_dict = ticket_req.dict()
    ticket_dict["modified_at"] = config_info.get_current_time()

    db_update_result = db.update_item(index, ticket_id, ticket_dict)

    if not db_update_result:
        response = api_resp.Response(
            message=f"Failed to update ticket with id '{ticket_id}'",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    response = api_resp.Response(
        message=f"Ticket with id '{ticket_id}' updated successfully"
    )
    logger.info(response.message)
    return response


def delete_ticket(ticket_id: str) -> api_resp.Response:
    """
    Delete a ticket
    """
    index = config_info.DB_INDEXES[config_info.Entities.TICKET]

    child_comments_req = api_req.SearchCommentsRequest(ticket_id=ticket_id)
    child_comments_resp = search_comments(child_comments_req)
    child_comments = [comment.comment_id
                      for comment in child_comments_resp.comments]

    for comment_id in child_comments:
        delete_comment_resp = delete_comment(comment_id)
        if not delete_comment_resp.result:
            response = api_resp.Response(
                message=f"Failed to delete linked ticket with id '{ticket_id}'"
                        f" due to failed comment deletion:"
                        f" {delete_comment_resp.message}",
                code=424,
                result=False
            )
            logger.error(response.message)
            return response

    child_tickets_req = api_req.SearchTicketsRequest(parent_ticket=ticket_id)
    child_tickets_resp = search_tickets(child_tickets_req)
    child_tickets = child_tickets_resp.tickets

    for child_ticket in child_tickets:
        update_ticket_req = api_req.UpdateTicketRequest(
            title=child_ticket.title,
            description=child_ticket.description,
            type=child_ticket.type,
            priority=child_ticket.priority,
            status=child_ticket.status,
            assignee=child_ticket.assignee,
            modified_by=child_ticket.modified_by,
            parent_project=child_ticket.parent_project,
            parent_ticket=None
        )
        update_ticket_resp = update_ticket(child_ticket.ticket_id,
                                           update_ticket_req)
        if not update_ticket_resp.result:
            response = api_resp.Response(
                message=f"Failed to delete ticket with id '{ticket_id}'"
                        f" due to failed child ticket update:"
                        f" {update_ticket_resp.message}",
                code=424,
                result=False
            )
            logger.error(response.message)
            return response


    db_delete_result = db.delete_item(index, ticket_id)

    if not db_delete_result:
        response = api_resp.Response(
            message=f"Failed to delete ticket with id '{ticket_id}'",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    response = api_resp.Response(
        message=f"Ticket with id '{ticket_id}' deleted successfully"
    )
    logger.info(response.message)
    return response


def get_all_tickets() -> api_resp.GetAllTicketsResponse:
    """
    Get all tickets
    """
    index = config_info.DB_INDEXES[config_info.Entities.TICKET]
    db_get_all_result = db.get_all_items(index)

    if db_get_all_result is None:
        response = api_resp.GetAllTicketsResponse(
            message="Failed to retrieve all tickets",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    tickets = [models.Ticket.parse_obj(ticket)
               for ticket in db_get_all_result.values()]

    tickets.sort(key=lambda ticket: datetime.datetime.strptime(
        ticket.modified_at, config_info.DATETIME_FORMAT), reverse=True)

    response = api_resp.GetAllTicketsResponse(
        message="All tickets retrieved successfully",
        tickets=tickets
    )
    logger.info(response.message)
    return response


def search_tickets(search_req: api_req.SearchTicketsRequest
                         ) -> api_resp.GetAllTicketsResponse:
    """
    Search for tickets
    """
    index = config_info.DB_INDEXES[config_info.Entities.TICKET]
    query_dict = search_req.dict()
    query_dict = {
        field: value
        for field, value in query_dict.items()
        if value is not None
    }

    db_search_result = db.search_items(index, query_dict)

    if db_search_result is None:
        response = api_resp.GetAllTicketsResponse(
            message="Failed to search for tickets",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    tickets = [models.Ticket.parse_obj(ticket)
               for ticket in db_search_result.values()]

    tickets.sort(key=lambda ticket: datetime.datetime.strptime(
        ticket.modified_at, config_info.DATETIME_FORMAT), reverse=True)

    response = api_resp.GetAllTicketsResponse(
        message="Tickets retrieved successfully",
        tickets=tickets
    )
    logger.info(response.message)
    return response


def get_all_comments_for_ticket(ticket_id: str
                                ) -> api_resp.GetAllCommentsResponse:
    """
    Get all comments for a given ticket
    """
    index = config_info.DB_INDEXES[config_info.Entities.COMMENT]
    query_dict = {"ticket_id": ticket_id}

    db_search_result = db.search_items(index, query_dict)

    if db_search_result is None:
        response = api_resp.GetAllCommentsResponse(
            message=f"Failed to retrieve all comments for ticket with id"
                    f" '{ticket_id}'",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    comments = [models.Comment.parse_obj(comment)
                for comment in db_search_result.values()]

    comments.sort(key=lambda comment: datetime.datetime.strptime(
        comment.created_at, config_info.DATETIME_FORMAT))

    response = api_resp.GetAllCommentsResponse(
        message=f"All comments for ticket with id '{ticket_id}' retrieved"
                f" successfully",
        comments=comments
    )
    logger.info(response.message)
    return response


def get_all_children_tickets(ticket_id: str
                             ) -> api_resp.GetAllTicketsResponse:
    """
    Get all children tickets for a given ticket
    """
    index = config_info.DB_INDEXES[config_info.Entities.TICKET]
    query_dict = {"parent_ticket": ticket_id}

    db_search_result = db.search_items(index, query_dict)

    if db_search_result is None:
        response = api_resp.GetAllTicketsResponse(
            message=f"Failed to retrieve all children tickets for ticket with"
                    f" id '{ticket_id}'",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    tickets = [models.Ticket.parse_obj(ticket)
               for ticket in db_search_result.values()]

    tickets.sort(key=lambda ticket: datetime.datetime.strptime(
        ticket.modified_at, config_info.DATETIME_FORMAT), reverse=True)

    response = api_resp.GetAllTicketsResponse(
        message=f"All children tickets for ticket with id '{ticket_id}'"
                f" retrieved successfully",
        tickets=tickets
    )
    logger.info(response.message)
    return response


def change_ticket_status(ticket_id: str, status: str) -> api_resp.Response:
    """
    Change the status of a ticket
    """
    index = config_info.DB_INDEXES[config_info.Entities.TICKET]
    ticket_dict = {"status": status}

    db_update_result = db.update_item(index, ticket_id, ticket_dict)

    if not db_update_result:
        response = api_resp.Response(
            message=f"Failed to change status of ticket with id '{ticket_id}'"
                    f" to '{status}'",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    response = api_resp.Response(
        message=f"Status of ticket with id '{ticket_id}' changed to '{status}'"
                f" successfully"
    )
    logger.info(response.message)
    return response


def get_comment(comment_id: str) -> api_resp.GetCommentResponse:
    """
    Get a comment by id
    """
    index = config_info.DB_INDEXES[config_info.Entities.COMMENT]
    db_get_result = db.get_item(index, comment_id)

    if not db_get_result:
        response = api_resp.GetCommentResponse(
            message=f"Comment with id '{comment_id}' not found",
            code=404,
            result=False
        )
        logger.error(response.message)
        return response

    comment = models.Comment.parse_obj(db_get_result)
    response = api_resp.GetCommentResponse(
        message=f"Comment with id '{comment_id}' retrieved successfully",
        comment=comment
    )
    logger.info(response.message)
    return response


def is_user_owner_of_ticket(ticket_id: str,
                            user_id: str) -> api_resp.Response:
    """
    Check if a user is the owner of a ticket
    """
    user = get_user(user_id).user
    if user is None:
        response = api_resp.Response(
            message=f"Failed to check if user with id '{user_id}' is owner of"
                    f" ticket with id '{ticket_id}' due to non-existent user",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    ticket = get_ticket(ticket_id).ticket
    if ticket is None:
        response = api_resp.Response(
            message=f"Failed to check if user with id '{user_id}' is owner of"
                    f" ticket with id '{ticket_id}' due to non-existent"
                    f" ticket",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    project = get_project(ticket.parent_project).project
    if project is None:
        response = api_resp.Response(
            message=f"Failed to check if user with id '{user_id}' is owner of"
                    f" ticket with id '{ticket_id}' due to non-existent"
                    f" parent project",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    if (user.username == ticket.created_by
            or user.username == project.created_by
            or user.is_admin
            or is_user_owner_of_ticket(ticket.parent_ticket, user_id).result):
        response = api_resp.Response(
            message=f"User with id '{user.username}' is the owner of ticket"
                    f" with id '{ticket_id}'"
        )
        logger.info(response.message)
        return response

    response = api_resp.Response(
        message=f"User with id '{user.username}' is not the owner of ticket"
                f" with id '{ticket_id}'",
        result=False
    )
    logger.info(response.message)
    return response


def create_comment(
        comment_req: api_req.CreateCommentRequest) -> api_resp.Response:
    """
    Create a comment
    """
    if not comment_req.comment_id:
        comment_req.comment_id = str(uuid.uuid4())
    user = get_user(comment_req.created_by).user
    if user is None:
        response = api_resp.Response(
            message=f"Failed to create comment with id"
                    f" '{comment_req.comment_id}' due to non-existent user"
                    f" with id '{comment_req.created_by}'",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    ticket = get_ticket(comment_req.ticket_id).ticket
    if ticket is None:
        response = api_resp.Response(
            message=f"Failed to create comment with id"
                    f" '{comment_req.comment_id}' due to non-existent ticket"
                    f" with id '{comment_req.ticket_id}'",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    index = config_info.DB_INDEXES[config_info.Entities.COMMENT]
    comment_dict = comment_req.dict()
    comment_dict["created_at"] = config_info.get_current_time()
    comment_dict["modified_at"] = comment_dict["created_at"]
    comment_dict["modified_by"] = comment_dict["created_by"]
    comment = models.Comment.parse_obj(comment_dict)

    db_create_result = db.create_item(
        index, comment.dict(), comment.comment_id)

    if not db_create_result:
        response = api_resp.Response(
            message=f"Failed to create comment with id '{comment.comment_id}'",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    db.update_item(
        config_info.DB_INDEXES[config_info.Entities.TICKET],
        comment.ticket_id,
        {"next_comment_id": ticket.next_comment_id + 1}
    )

    response = api_resp.Response(
        message=f"Comment with id '{comment.comment_id}' created successfully"
    )
    logger.info(response.message)
    return response


def delete_comment(comment_id: str) -> api_resp.Response:
    """
    Delete a comment
    """
    index = config_info.DB_INDEXES[config_info.Entities.COMMENT]
    db_delete_result = db.delete_item(index, comment_id)

    if not db_delete_result:
        response = api_resp.Response(
            message=f"Failed to delete comment with id '{comment_id}'",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    response = api_resp.Response(
        message=f"Comment with id '{comment_id}' deleted successfully"
    )
    logger.info(response.message)
    return response


def get_all_comments() -> api_resp.GetAllCommentsResponse:
    """
    Get all comments
    """
    index = config_info.DB_INDEXES[config_info.Entities.COMMENT]
    db_get_all_result = db.get_all_items(index)

    if db_get_all_result is None:
        response = api_resp.GetAllCommentsResponse(
            message="Failed to retrieve all comments",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    comments = [models.Comment.parse_obj(comment)
                for comment in db_get_all_result.values()]

    comments.sort(key=lambda comment: datetime.datetime.strptime(
        comment.modified_at, config_info.DATETIME_FORMAT))

    response = api_resp.GetAllCommentsResponse(
        message="All comments retrieved successfully",
        comments=comments
    )
    logger.info(response.message)
    return response


def search_comments(search_req: api_req.SearchCommentsRequest
                          ) -> api_resp.GetAllCommentsResponse:
    """
    Search for comments
    """
    index = config_info.DB_INDEXES[config_info.Entities.COMMENT]
    query_dict = search_req.dict()
    query_dict = {
        field: value
        for field, value in query_dict.items()
        if value is not None
    }

    db_search_result = db.search_items(index, query_dict)

    if db_search_result is None:
        response = api_resp.GetAllCommentsResponse(
            message="Failed to search for comments",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    comments = [models.Comment.parse_obj(comment)
                for comment in db_search_result.values()]

    comments.sort(key=lambda comment: datetime.datetime.strptime(
        comment.created_at, config_info.DATETIME_FORMAT))

    response = api_resp.GetAllCommentsResponse(
        message="Comments retrieved successfully",
        comments=comments
    )
    logger.info(response.message)
    return response


def is_user_owner_of_comment(comment_id: str,
                             user_id: str) -> api_resp.Response:
    """
    Check if a user is the owner of a comment
    """
    user = get_user(user_id).user
    if user is None:
        response = api_resp.Response(
            message=f"Failed to check if user with id '{user_id}' is owner of"
                    f" comment with id '{comment_id}' due to non-existent"
                    f" user",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    comment = get_comment(comment_id).comment
    if comment is None:
        response = api_resp.Response(
            message=f"Failed to check if user with id '{user_id}' is owner of"
                    f" comment with id '{comment_id}' due to non-existent"
                    f" comment",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    if (user.username == comment.created_by
            or user.is_admin
            or is_user_owner_of_ticket(comment.ticket_id, user_id).result):
        response = api_resp.Response(
            message=f"User with id '{user.username}' is the owner of comment"
                    f" with id '{comment_id}'"
        )
        logger.info(response.message)
        return response

    response = api_resp.Response(
        message=f"User with id '{user.username}' is not the owner of comment"
                f" with id '{comment_id}'",
        result=False
    )
    logger.info(response.message)
    return response


def ai_endpoint(ai_req: api_req.AIRequest) -> api_resp.AIResponse:
    """
    AI endpoint
    """
    response_message, chat_history = ai.get_openai_response(**ai_req.dict())

    if not response_message or not chat_history:
        response = api_resp.AIResponse(
            message="Failed to retrieve response from OpenAI GPT-4o model",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    response = api_resp.AIResponse(
        message="Successfully retrieved response from OpenAI GPT-4o model",
        response=response_message,
        chat_history=chat_history
    )
    logger.info(response.message)
    return response

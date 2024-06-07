"""Main project file for API service."""
import fastapi
import uvicorn

from fastapi.responses import RedirectResponse

from taskpilot.common import config_info, api_request_classes as api_req
from taskpilot.api import api_endpoint_helpers as api_help
from taskpilot.api import api_response_classes as api_resp


app = fastapi.FastAPI(
    title="TaskPilot",
    description="Project Management Platform",
    version="1.0"
)


@app.get("/", include_in_schema=False)
async def redirect_to_docs() -> RedirectResponse:
    """Redirect to the API documentation."""
    return RedirectResponse(url="/docs")


@app.get(config_info.API_ROUTES[config_info.APIOperations.USERS_GET],
         tags=["Users"])
async def get_user(user_id: str) -> api_resp.GetUserResponse:
    """
    Get a user by id
    """
    response = api_help.get_user(user_id)
    return response


@app.post(config_info.API_ROUTES[config_info.APIOperations.USERS_CREATE],
          tags=["Users"])
async def create_user(
        user_req: api_req.CreateUserRequest) -> api_resp.Response:
    """
    Create a user
    """
    response = api_help.create_user(user_req)
    return response


@app.put(config_info.API_ROUTES[config_info.APIOperations.USERS_UPDATE],
         tags=["Users"])
async def update_user(
        user_id: str,
        user_req: api_req.UpdateUserRequest) -> api_resp.Response:
    """
    Update a user
    """
    response = api_help.update_user(user_id, user_req)
    return response


@app.delete(config_info.API_ROUTES[config_info.APIOperations.USERS_DELETE],
            tags=["Users"])
async def delete_user(user_id: str) -> api_resp.Response:
    """
    Delete a user
    """
    response = api_help.delete_user(user_id)
    return response


@app.get(config_info.API_ROUTES[config_info.APIOperations.USERS_ALL],
         tags=["Users"])
async def get_all_users() -> api_resp.GetAllUsersResponse:
    """
    Get all users
    """
    response = api_help.get_all_users()
    return response


@app.post(config_info.API_ROUTES[config_info.APIOperations.USERS_SEARCH],
         tags=["Users"])
async def search_users(search_req: api_req.SearchUsersRequest
                       ) -> api_resp.GetAllUsersResponse:
    """
    Search for users
    """
    response = api_help.search_users(search_req)
    return response


@app.get(config_info.API_ROUTES[
             config_info.APIOperations.USERS_ALL_ASSIGNED_TICKETS],
         tags=["Users"])
async def get_all_assigned_tickets(user_id: str
                                   ) -> api_resp.GetAllTicketsResponse:
    """
    Get all tickets assigned to a user
    """
    response = api_help.get_all_assigned_tickets(user_id)
    return response


@app.post(config_info.API_ROUTES[
              config_info.APIOperations.USERS_ASSIGN_TICKET],
          tags=["Users"])
async def assign_ticket(user_id: str, ticket_id: str) -> api_resp.Response:
    """
    Assign a ticket to a user
    """
    response = api_help.assign_ticket(user_id, ticket_id)
    return response


@app.delete(config_info.API_ROUTES[
                config_info.APIOperations.USERS_UNASSIGN_TICKET],
            tags=["Users"])
async def unassign_ticket(user_id: str, ticket_id: str) -> api_resp.Response:
    """
    Unassign a ticket from a user
    """
    response = api_help.unassign_ticket(user_id, ticket_id)
    return response


@app.post(config_info.API_ROUTES[
              config_info.APIOperations.USERS_ADD_FAVORITE_TICKET],
          tags=["Users"])
async def add_favorite_ticket(user_id: str,
                              ticket_id: str) -> api_resp.Response:
    """
    Add a ticket to a user's favorites
    """
    response = api_help.add_favorite_ticket(user_id, ticket_id)
    return response


@app.delete(config_info.API_ROUTES[
                config_info.APIOperations.USERS_REMOVE_FAVORITE_TICKET],
            tags=["Users"])
async def remove_favorite_ticket(user_id: str,
                                 ticket_id: str) -> api_resp.Response:
    """
    Remove a ticket from a user's favorites
    """
    response = api_help.remove_favorite_ticket(user_id, ticket_id)
    return response


@app.post(config_info.API_ROUTES[config_info.APIOperations.USERS_LOGIN],
          tags=["Users"])
async def login_user(login_req: api_req.LoginRequest) -> api_resp.Response:
    """
    Log in a user
    """
    response = api_help.login_user(login_req)
    return response


@app.get(config_info.API_ROUTES[config_info.APIOperations.USERS_ALL_PROJECTS],
         tags=["Users"])
async def get_user_projects(user_id: str) -> api_resp.GetAllProjectsResponse:
    """
    Get all projects for a user
    """
    response = api_help.get_user_projects(user_id)
    return response


@app.get(config_info.API_ROUTES[config_info.APIOperations.PROJECTS_GET],
         tags=["Projects"])
async def get_project(project_id: str) -> api_resp.GetProjectResponse:
    """
    Get a project by id
    """
    response = api_help.get_project(project_id)
    return response


@app.post(config_info.API_ROUTES[config_info.APIOperations.PROJECTS_CREATE],
          tags=["Projects"])
async def create_project(
        project_req: api_req.CreateProjectRequest) -> api_resp.Response:
    """
    Create a project
    """
    response = api_help.create_project(project_req)
    return response


@app.put(config_info.API_ROUTES[config_info.APIOperations.PROJECTS_UPDATE],
         tags=["Projects"])
async def update_project(
        project_id: str,
        project_req: api_req.UpdateProjectRequest) -> api_resp.Response:
    """
    Update a project
    """
    response = api_help.update_project(project_id, project_req)
    return response


@app.delete(config_info.API_ROUTES[config_info.APIOperations.PROJECTS_DELETE],
            tags=["Projects"])
async def delete_project(project_id: str) -> api_resp.Response:
    """
    Delete a project
    """
    response = api_help.delete_project(project_id)
    return response


@app.get(config_info.API_ROUTES[config_info.APIOperations.PROJECTS_ALL],
         tags=["Projects"])
async def get_all_projects() -> api_resp.GetAllProjectsResponse:
    """
    Get all projects
    """
    response = api_help.get_all_projects()
    return response


@app.post(config_info.API_ROUTES[config_info.APIOperations.PROJECTS_SEARCH],
          tags=["Projects"])
async def search_projects(search_req: api_req.SearchProjectsRequest
                          ) -> api_resp.GetAllProjectsResponse:
    """
    Search for projects
    """
    response = api_help.search_projects(search_req)
    return response


@app.get(config_info.API_ROUTES[
             config_info.APIOperations.PROJECTS_ALL_TICKETS],
         tags=["Projects"])
async def get_all_tickets_in_project(project_id: str
                                     ) -> api_resp.GetAllTicketsResponse:
    """
    Get all tickets in a project
    """
    response = api_help.get_all_tickets_in_project(project_id)
    return response


@app.post(config_info.API_ROUTES[
              config_info.APIOperations.PROJECTS_ADD_MEMBER],
            tags=["Projects"])
async def add_member_to_project(project_id: str,
                                user_id: str) -> api_resp.Response:
    """
    Add a member to a project
    """
    response = api_help.add_member_to_project(project_id, user_id)
    return response


@app.delete(config_info.API_ROUTES[
                config_info.APIOperations.PROJECTS_REMOVE_MEMBER],
            tags=["Projects"])
async def remove_member_from_project(project_id: str,
                                     user_id: str) -> api_resp.Response:
    """
    Remove a member from a project
    """
    response = api_help.remove_member_from_project(project_id, user_id)
    return response


@app.get(config_info.API_ROUTES[config_info.APIOperations.TICKETS_GET],
         tags=["Tickets"])
async def get_ticket(ticket_id: str) -> api_resp.GetTicketResponse:
    """
    Get a ticket by id
    """
    response = api_help.get_ticket(ticket_id)
    return response


@app.post(config_info.API_ROUTES[config_info.APIOperations.TICKETS_CREATE],
          tags=["Tickets"])
async def create_ticket(
        ticket_req: api_req.CreateTicketRequest) -> api_resp.Response:
    """
    Create a ticket
    """
    response = api_help.create_ticket(ticket_req)
    return response


@app.put(config_info.API_ROUTES[config_info.APIOperations.TICKETS_UPDATE],
         tags=["Tickets"])
async def update_ticket(
        ticket_id: str,
        ticket_req: api_req.UpdateTicketRequest) -> api_resp.Response:
    """
    Update a ticket
    """
    response = api_help.update_ticket(ticket_id, ticket_req)
    return response


@app.delete(config_info.API_ROUTES[config_info.APIOperations.TICKETS_DELETE],
            tags=["Tickets"])
async def delete_ticket(ticket_id: str) -> api_resp.Response:
    """
    Delete a ticket
    """
    response = api_help.delete_ticket(ticket_id)
    return response


@app.get(config_info.API_ROUTES[config_info.APIOperations.TICKETS_ALL],
         tags=["Tickets"])
async def get_all_tickets() -> api_resp.GetAllTicketsResponse:
    """
    Get all tickets
    """
    response = api_help.get_all_tickets()
    return response


@app.post(config_info.API_ROUTES[config_info.APIOperations.TICKETS_SEARCH],
          tags=["Tickets"])
async def search_tickets(search_req: api_req.SearchTicketsRequest
                         ) -> api_resp.GetAllTicketsResponse:
    """
    Search for tickets
    """
    response = api_help.search_tickets(search_req)
    return response


@app.get(config_info.API_ROUTES[
             config_info.APIOperations.TICKETS_ALL_COMMENTS],
         tags=["Tickets"])
async def get_all_comments_for_ticket(ticket_id: str
                                      ) -> api_resp.GetAllCommentsResponse:
    """
    Get all comments for a given ticket
    """
    response = api_help.get_all_comments_for_ticket(ticket_id)
    return response


@app.get(config_info.API_ROUTES[
             config_info.APIOperations.TICKETS_ALL_CHILDREN],
         tags=["Tickets"])
async def get_all_children_tickets(ticket_id: str
                                   ) -> api_resp.GetAllTicketsResponse:
    """
    Get all children tickets for a given ticket
    """
    response = api_help.get_all_children_tickets(ticket_id)
    return response


@app.put(config_info.API_ROUTES[
             config_info.APIOperations.TICKETS_CHANGE_STATUS],
         tags=["Tickets"])
async def change_ticket_status(ticket_id: str,
                               status: str) -> api_resp.Response:
    """
    Change the status of a ticket
    """
    response = api_help.change_ticket_status(ticket_id, status)
    return response


@app.get(config_info.API_ROUTES[
             config_info.APIOperations.TICKETS_IS_USER_OWNER],
         tags=["Tickets"])
async def is_user_owner_of_ticket(ticket_id: str,
                                  user_id: str) -> api_resp.Response:
    """
    Check if a user is the owner of a ticket
    """
    response = api_help.is_user_owner_of_ticket(ticket_id, user_id)
    return response


@app.get(config_info.API_ROUTES[config_info.APIOperations.COMMENTS_GET],
         tags=["Comments"])
async def get_comment(comment_id: str) -> api_resp.GetCommentResponse:
    """
    Get a comment by id
    """
    response = api_help.get_comment(comment_id)
    return response


@app.post(config_info.API_ROUTES[config_info.APIOperations.COMMENTS_CREATE],
          tags=["Comments"])
async def create_comment(
        comment_req: api_req.CreateCommentRequest) -> api_resp.Response:
    """
    Create a comment
    """
    response = api_help.create_comment(comment_req)
    return response


@app.delete(config_info.API_ROUTES[config_info.APIOperations.COMMENTS_DELETE],
            tags=["Comments"])
async def delete_comment(comment_id: str) -> api_resp.Response:
    """
    Delete a comment
    """
    response = api_help.delete_comment(comment_id)
    return response


@app.get(config_info.API_ROUTES[config_info.APIOperations.COMMENTS_ALL],
         tags=["Comments"])
async def get_all_comments() -> api_resp.GetAllCommentsResponse:
    """
    Get all comments
    """
    response = api_help.get_all_comments()
    return response


@app.post(config_info.API_ROUTES[config_info.APIOperations.COMMENTS_SEARCH],
          tags=["Comments"])
async def search_comments(search_req: api_req.SearchCommentsRequest
                          ) -> api_resp.GetAllCommentsResponse:
    """
    Search for comments
    """
    response = api_help.search_comments(search_req)
    return response


if __name__ == "__main__":
    uvicorn.run(
        app=config_info.API_APP,
        host=config_info.HOST,
        port=config_info.API_PORT,
        reload=True
    )

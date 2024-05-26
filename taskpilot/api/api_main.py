"""Main project file for API service."""
import fastapi
import uvicorn

from fastapi.responses import RedirectResponse

from taskpilot.common import config_info
from taskpilot.api import api_request_classes as api_req
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


if __name__ == "__main__":
    uvicorn.run(
        app=config_info.API_APP,
        host=config_info.HOST,
        port=config_info.API_PORT,
        reload=True
    )

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


if __name__ == "__main__":
    uvicorn.run(
        app=config_info.API_APP,
        host=config_info.HOST,
        port=config_info.API_PORT,
        reload=True
    )

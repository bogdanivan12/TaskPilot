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
async def get_user(user_id: str) -> api_resp.Response:
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


if __name__ == "__main__":
    uvicorn.run(
        app=config_info.API_APP,
        host=config_info.HOST,
        port=config_info.API_PORT,
        reload=True
    )

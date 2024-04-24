"""Main project file for API service."""
import fastapi
import uvicorn

from taskpilot.common import config_info


app = fastapi.FastAPI(
    title="TaskPilot",
    description="Project Management Platform",
    version=config_info.VERSION
)


@app.get("/", include_in_schema=False)
def redirect_to_docs():
    """Redirect to the API documentation."""
    return fastapi.responses.RedirectResponse(url="/docs")


if __name__ == "__main__":
    uvicorn.run(
        app=config_info.API_APP,
        host=config_info.HOST,
        port=config_info.API_PORT,
        reload=True
    )

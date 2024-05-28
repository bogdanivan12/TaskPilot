"""Main UI file for the TaskPilot application"""
from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from nicegui import Client, app, ui

from taskpilot.common import config_info
from taskpilot.ui import ui_page_helpers as ui_help


class AuthMiddleware(BaseHTTPMiddleware):
    """This middleware restricts access to all pages.

    It redirects the user to the login page if they are not authenticated.
    """
    async def dispatch(self, request: Request, call_next):
        if not app.storage.user.get("authenticated", False):
            if (request.url.path in Client.page_routes.values()
                    and request.url.path not in
                    config_info.UNRESTRICTED_PAGE_ROUTES):
                app.storage.user["referrer_path"] = request.url.path  # remember where the user wanted to go
                return RedirectResponse("/login")
        return await call_next(request)


app.add_middleware(AuthMiddleware)


@ui.page(config_info.UI_ROUTES[config_info.UIPages.HOME])
def main_page() -> None:
    """Main page for the TaskPilot application"""
    return ui_help.main_page()


@ui.page("/subpage")
def test_page() -> None:
    """Test subpage for the TaskPilot application"""
    return ui_help.test_page()


@ui.page("/login")
def login() -> None:
    """Login page for the TaskPilot application"""
    return ui_help.login()


@ui.page("/register")
def register() -> None:
    """Register page for the TaskPilot application"""
    return ui_help.register()


@ui.page("/projects")
def projects() -> None:
    """Projects page for the TaskPilot application"""
    return ui_help.projects()


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        title="TaskPilot",
        host=config_info.HOST,
        port=config_info.UI_PORT,
        storage_secret="taskpilot_secret_key"
    )

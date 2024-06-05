"""Main UI file for the TaskPilot application"""
import re
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
        path = request.url.path

        routes = Client.page_routes.values()

        is_authenticated = app.storage.user.get("authenticated", False)

        if (not is_authenticated
                and path not in config_info.UNRESTRICTED_PAGE_ROUTES):
            is_valid_route = False

            for route in routes:
                route_pattern = re.sub(
                    r"\{[^{}]*\}", r"[^/]+", route)
                pattern = re.compile(f"^{route_pattern}$")
                if pattern.fullmatch(path):
                    is_valid_route = True
                    break

            if is_valid_route:
                app.storage.user["referrer_path"] = path
                return RedirectResponse(
                    config_info.UI_ROUTES[config_info.UIPages.LOGIN]
                )

        return await call_next(request)


app.add_middleware(AuthMiddleware)


@ui.page(config_info.UI_ROUTES[config_info.UIPages.HOME])
def main_page() -> None:
    """Main page for the TaskPilot application"""
    return ui_help.main_page()


@ui.page(config_info.UI_ROUTES[config_info.UIPages.LOGIN])
def login() -> None:
    """Login page for the TaskPilot application"""
    return ui_help.login()


@ui.page(config_info.UI_ROUTES[config_info.UIPages.REGISTER])
def register() -> None:
    """Register page for the TaskPilot application"""
    return ui_help.register()


@ui.page(config_info.UI_ROUTES[config_info.UIPages.PROJECTS])
def projects() -> None:
    """Projects page for the TaskPilot application"""
    return ui_help.projects()


@ui.page(config_info.UI_ROUTES[config_info.UIPages.TICKETS])
def tickets() -> None:
    """Tickets page for the TaskPilot application"""
    return ui_help.tickets()


@ui.page(config_info.UI_ROUTES[config_info.UIPages.PROJECT])
def project(project_id: str) -> None:
    """Project page for the TaskPilot application"""
    return ui_help.project(project_id)


@ui.page(config_info.UI_ROUTES[config_info.UIPages.TICKET])
def ticket(ticket_id: str) -> None:
    """Ticket page for the TaskPilot application"""
    return ui_help.ticket(ticket_id)


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        title="TaskPilot",
        host=config_info.HOST,
        port=config_info.UI_PORT,
        storage_secret="taskpilot_secret_key"
    )

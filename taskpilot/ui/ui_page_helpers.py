"""Page helpers for the TaskPilot application"""
import requests
from typing import Optional
from fastapi.responses import RedirectResponse
from nicegui import app, ui

from taskpilot.common import config_info
from taskpilot.common import api_request_classes as api_req
from taskpilot.common.config_info import APIOperations as APIOps


def apply_header(func):
    """Apply the header to the page"""
    def wrapper(*args, **kwargs):
        header_page()
        func(*args, **kwargs)
    return wrapper


def is_user_authenticated() -> bool:
    """Check if the user is authenticated"""
    return app.storage.user.get("authenticated", False)


def header_page() -> None:
    with ui.header().classes(replace="row items-center min-h-4") as header:
        if is_user_authenticated():
            ui.button(on_click=lambda: left_drawer.toggle(), icon="menu").props(
                "flat color=white")
        ui.label("TaskPilot").classes("text-2xl font-bold text-white absolute-center")
        if is_user_authenticated():
            ui.chip(
                text="Logout",
                on_click=lambda: (
                    app.storage.user.clear(),
                    ui.navigate.to(
                        config_info.UI_ROUTES[config_info.UIPages.LOGIN]
                    )
                ),
                icon="logout"
            ).props("flat color=white").classes(replace="absolute-right")

    with ui.left_drawer().classes('bg-blue-100') as left_drawer:
        ui.label('Side menu')


@apply_header
def main_page() -> None:
    """Main page for the TaskPilot application"""
    with ui.column().classes("absolute-center items-center"):
        ui.label(f"Hello, {app.storage.user['username']}!").classes("text-2xl")
        ui.button(
            on_click=lambda: (
                app.storage.user.clear(),
                ui.navigate.to(
                    config_info.UI_ROUTES[config_info.UIPages.LOGIN]
                )
            ),
            icon="logout"
        ).props("outline round")


@apply_header
def test_page() -> None:
    """Test subpage for the TaskPilot application"""
    with ui.header().classes(replace='row items-center') as header:
        ui.button(on_click=lambda: left_drawer.toggle(), icon="menu").props(
            "flat color=white")
        ui.label("TaskPilot").classes("text-2xl font-bold text-white")

    with ui.footer(value=False) as footer:
        ui.label('Footer')

    with ui.left_drawer().classes('bg-blue-100') as left_drawer:
        ui.label('Side menu')
        with ui.tabs() as tabs:
            ui.tab('A')
            ui.tab('B')
            ui.tab('C')

    with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
        ui.button(on_click=footer.toggle, icon='contact_support').props('fab')

    with ui.tab_panels(tabs, value='A').classes('w-full'):
        with ui.tab_panel('A'):
            ui.label('Content of A')
        with ui.tab_panel('B'):
            ui.label('Content of B')
        with ui.tab_panel('C'):
            ui.label('Content of C')

    ui.label("This is a sub page.")


@apply_header
def login() -> Optional[RedirectResponse]:
    """Login page for the TaskPilot application"""
    def try_login() -> None:
        """
        Local function to avoid passing username and password as arguments
        """
        url = (
            f"{config_info.API_URL}"
            f"/{config_info.API_ROUTES[APIOps.USERS_LOGIN]}"
        )
        login_response = requests.post(
            url=url,
            json={
                "username": username.value,
                "password": password.value
            }
        )
        if login_response.json().get("result", False):
            app.storage.user.update(
                {
                    "username": username.value,
                    "authenticated": True
                }
            )
            ui.navigate.to(app.storage.user.get("referrer_path", "/"))  # go back to where the user wanted to go
        else:
            ui.notify("Wrong username or password", color="negative")

    if is_user_authenticated():
        return RedirectResponse("/")
    with ui.card().classes("absolute-center"):
        username = ui.input("Username").on("keydown.enter", try_login)
        password = ui.input(
            label="Password",
            password=True,
            password_toggle_button=True
        ).on("keydown.enter", try_login)
        ui.button("Log in", on_click=try_login)
    return None


@apply_header
def register() -> Optional[RedirectResponse]:
    """Register page for the TaskPilot application"""
    def create_user() -> None:
        """
        Local function to avoid passing username and password as arguments
        """
        url = (
            f"{config_info.API_URL}"
            f"/{config_info.API_ROUTES[APIOps.USERS_CREATE]}"
        )
        create_user_request = api_req.CreateUserRequest(
            username=username.value,
            email=email.value,
            full_name=full_name.value,
            password=password.value
        )
        register_response = requests.post(
            url=url,
            json=create_user_request.dict()
        )
        if register_response.json().get("result", False):
            app.storage.user.update(
                {
                    "username": username.value,
                    "authenticated": True
                }
            )
            ui.navigate.to(config_info.UI_ROUTES[config_info.UIPages.HOME])
        else:
            ui.notify(register_response.json().get(
                "message", "Unable to register"), color="negative")

    with ui.card().classes("absolute-center"):
        username = ui.input("Username").on("keydown.enter", create_user)
        email = ui.input("Email").on("keydown.enter", create_user)
        full_name = ui.input("Full name").on("keydown.enter", create_user)
        password = ui.input(
            label="Password",
            password=True,
            password_toggle_button=True
        ).on("keydown.enter", create_user)
        ui.button("Register", on_click=create_user)
    return None

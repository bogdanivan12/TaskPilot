import requests
from nicegui import app, ui

from taskpilot.common import config_info, api_request_classes as api_req
from taskpilot.common.config_info import APIOperations as APIOps


def is_user_authenticated() -> bool:
    """Check if the user is authenticated"""
    return app.storage.user.get("authenticated", False)


def login_page() -> None:
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
            ui.navigate.to(
                app.storage.user.get(
                    "referrer_path",
                    config_info.UI_ROUTES[config_info.UIPages.HOME]
                )
            )  # go back to where the user wanted to go
        else:
            ui.notify("Wrong username or password", color="negative")

    if is_user_authenticated():
        ui.navigate.to(config_info.UI_ROUTES[config_info.UIPages.HOME])

    with ui.card().classes("absolute-center"):
        username = ui.input("Username").on("keydown.enter", try_login)
        password = ui.input(
            label="Password",
            password=True,
            password_toggle_button=True
        ).on("keydown.enter", try_login)
        ui.button("Log in", on_click=try_login).classes(
            "place-self-center")
        ui.chip(
            text="New user? Register",
            on_click=lambda: ui.navigate.to(
                config_info.UI_ROUTES[config_info.UIPages.REGISTER]
            ),
            icon="arrow_right"
        ).props("flat color=white").classes("place-self-center")
    return None


def register_page() -> None:
    """Register page for the TaskPilot application"""
    def create_user() -> None:
        """
        Local function to avoid passing username and password as arguments
        """
        if password.value != confirm_password.value:
            ui.notify("Passwords do not match", color="negative")
            return

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

    if is_user_authenticated():
        ui.navigate.to(config_info.UI_ROUTES[config_info.UIPages.HOME])

    with ui.card().classes("absolute-center"):
        username = ui.input("Username").on("keydown.enter", create_user)
        email = ui.input("Email").on("keydown.enter", create_user)
        full_name = ui.input("Full name").on("keydown.enter", create_user)
        password = ui.input(
            label="Password",
            password=True,
            password_toggle_button=True
        ).on("keydown.enter", create_user)
        confirm_password = ui.input(
            label="Confirm Password",
            password=True,
            password_toggle_button=True
        ).on("keydown.enter", create_user)
        ui.button("Register", on_click=create_user).classes(
            "place-self-center")
        ui.chip(
            text="Already registered? Log in",
            on_click=lambda: ui.navigate.to(
                config_info.UI_ROUTES[config_info.UIPages.LOGIN]
            ),
            icon="arrow_right"
        ).props("flat color=white").classes("place-self-center")
    return

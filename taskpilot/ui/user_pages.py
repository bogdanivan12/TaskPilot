import requests
from nicegui import app, ui

from taskpilot.common import config_info, api_request_classes as api_req
from taskpilot.common import models
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


def profile_page(user_id: str) -> None:
    """Profile page for the TaskPilot application"""
    if app.storage.user.get("username", "") != user_id:
        ui.navigate.to(
            config_info.UI_ROUTES[config_info.UIPages.HOME]
        )
    user = models.User.parse_obj(
        requests.get(
            config_info.API_URL
            + "/"
            + config_info.API_ROUTES[APIOps.USERS_GET].format(
                user_id=user_id
            )
        ).json()["user"]
    )

    def save_profile() -> None:
        """Save the profile"""
        url = (
            f"{config_info.API_URL}"
            f"/{config_info.API_ROUTES[APIOps.USERS_UPDATE]}"
        )
        update_user_request = api_req.UpdateUserRequest(
            email=email.value,
            full_name=full_name.value,
            password=password.value
        )
        update_response = requests.put(
            url=url,
            json=update_user_request.dict()
        )
        if update_response.json().get("result", False):
            ui.notify("Profile updated", color="positive")
        else:
            ui.notify(update_response.json().get(
                "message", "Unable to update profile"), color="negative")

    with ui.dialog() as password_dialog, ui.card():
        ui.label("Change Password")
        new_pass = ui.input("New Password", password=True)
        confirm_new_pass = ui.input("Confirm New Password", password=True)
        ui.button(
            "Save",
            on_click=lambda: (
                password.set_value(
                    new_pass.value
                    if new_pass.value == confirm_new_pass.value
                    else ""
                ),
                password_dialog.close()
                if new_pass.value == confirm_new_pass.value
                else ui.notify("Passwords do not match", color="negative")
            )
        )
        ui.button("Cancel").on_click(
            lambda: password_dialog.close()
        )

    with ui.dialog() as edit_dialog, ui.card().classes("items-center"):
        ui.label("Edit Profile")
        full_name = ui.input("Full Name", value=user.full_name)
        email = ui.input("Email", value=user.email)
        password = ui.input(value="")
        password.set_visibility(False)
        ui.button("Change Password").on_click(
            lambda: password_dialog.open()
        )
        ui.button("Save").on_click(
            lambda: save_profile()
        )

    with ui.card():
        ui.label(f"Username: {user.username}")
        ui.label(f"Full Name: {user.full_name}")
        ui.label(f"Email: {user.email}")
        ui.button("Edit Profile").on_click(
            lambda: edit_dialog.open()
        )

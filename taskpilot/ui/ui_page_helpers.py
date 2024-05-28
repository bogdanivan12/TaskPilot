"""Page helpers for the TaskPilot application"""
import requests
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


def header_page():
    """Header page for the TaskPilot application"""
    is_user_auth = is_user_authenticated()
    with ui.header().classes(
            replace="row items-center fixed-top bg-sky-500") as header:
        header.default_style("height: 35px; z-index: 1000;")
        if is_user_auth:
            ui.button(
                on_click=lambda: left_drawer.toggle(),
                icon="menu"
            ).props("flat color=white")
        ui.label("TaskPilot").classes(
            "text-2xl font-bold text-white absolute-center")
        if is_user_auth:
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


    with ui.left_drawer(value=is_user_auth).classes(
            "bg-sky-100") as left_drawer:
        ui.button(
            text="Home",
            on_click=lambda: ui.navigate.to(
                config_info.UI_ROUTES[config_info.UIPages.HOME]
            )
        ).classes("w-full")
        ui.button(
            text="Projects",
            on_click=lambda: ui.navigate.to(
                config_info.UI_ROUTES[config_info.UIPages.PROJECTS]
            )
        ).classes("w-full")
        ui.button(
            text="Tickets",
            on_click=lambda: ui.navigate.to(
                config_info.UI_ROUTES[config_info.UIPages.TICKETS]
            )
        ).classes("w-full")



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
        ).props("outline round outline-sky-500")


@apply_header
def test_page() -> None:
    """Test subpage for the TaskPilot application"""
    ui.label("This is a test page")
    return


@apply_header
def login() -> None:
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


@apply_header
def register() -> None:
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
    return None


@apply_header
def projects() -> None:
    """Projects page for the TaskPilot application"""
    with ui.dialog() as dialog, ui.card().classes("w-full h-1/2 items-center"):
        ui.label("Create Project").classes("text-2xl")
        project_id = ui.input("Project ID").classes("w-4/5")
        title = ui.input("Title").classes("w-4/5")
        description = ui.textarea("Description").classes("w-4/5")

        all_users = requests.get(
            f"{config_info.API_URL}"
            f"/{config_info.API_ROUTES[APIOps.USERS_ALL]}"
        ).json()["users"]
        all_user_ids = [user["username"] for user in all_users]
        all_user_ids.remove(app.storage.user.get("username", ""))

        # Create a dictionary to store the checkboxes
        checkboxes = {}

        with ui.expansion("Members", icon="people").classes(
                "w-4/5") as all_users_expansion:
            for user_id in all_user_ids:
                checkboxes[user_id] = ui.checkbox(user_id).classes("w-4/5")

        def create_button_clicked():
            selected_user_ids = [
                user_id for user_id, checkbox in checkboxes.items()
                if checkbox.value
            ]
            dialog.close()
            selected_user_ids.append(app.storage.user.get("username", ""))
            create_project_request = api_req.CreateProjectRequest(
                project_id=project_id.value,
                title=title.value,
                description=description.value,
                created_by=app.storage.user.get("username", ""),
                members=selected_user_ids
            )
            url = (
                f"{config_info.API_URL}"
                f"/{config_info.API_ROUTES[APIOps.PROJECTS_CREATE]}"
            )
            create_project_response = requests.post(
                url=url,
                json=create_project_request.dict()
            )
            ui.notify(
                create_project_response.json().get(
                    "message", "Unable to create project"
                ),
                color="positive" if create_project_response.json().get(
                    "result", False) else "negative"
            )

        with ui.row().classes("items-center justify-between"):  # Add this line
            ui.button("Create").on(
                "click",
                lambda: create_button_clicked()
            ).classes("text-white mr-2")
            ui.button("Cancel", color="negative").on(
                "click",
                lambda: dialog.close()
            ).classes("text-white")

    def open_dialog():
        # Clear the input fields
        project_id.value = ""
        title.value = ""
        description.value = ""
        all_users_expansion.close()
        # Uncheck all checkboxes
        for checkbox in checkboxes.values():
            checkbox.value = False
        dialog.open()

    with ui.column().classes("absolute-center items-center"):
        ui.label("Projects").classes("text-2xl")
        ui.button("Create Project").on(
            "click",
            open_dialog
        ).classes("text-white")

    return None

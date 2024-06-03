"""Page helpers for the TaskPilot application"""
import time
import requests
from nicegui import app, ui

from taskpilot.common import config_info
from taskpilot.common import api_request_classes as api_req
from taskpilot.common.config_info import APIOperations as APIOps
from taskpilot.common import models


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
    ui.markdown(
        f"Welcome back, **{app.storage.user.get('username', '')}**!"
    ).classes("text-5xl items-center justify-between w-full self-center"
              " px-6 py-2")
    ui.label(
        "Here is a list of your assigned tickets that aren't yet closed:"
    ).classes("text-2xl items-center justify-between w-full self-center"
              " px-6 py-2")

    ui.separator()

    with ui.column().classes("items-center w-full self-center px-6 py-2"):
        assigned_tickets = requests.get(
            config_info.API_URL
            + "/"
            + config_info.API_ROUTES[APIOps.USERS_ALL_ASSIGNED_TICKETS].format(
                user_id=app.storage.user.get("username", ""))
        ).json()["tickets"]

        assigned_tickets = [
            models.Ticket.parse_obj(ticket) for ticket in assigned_tickets
            if ticket["status"] != config_info.TicketStatuses.CLOSED
        ]

        if not assigned_tickets:
            ui.label("No assigned tickets").classes("text-2xl")
            return

        for ticket in assigned_tickets:
            with ui.card().classes("w-full"):
                with ui.row().classes("items-center justify-between w-full"):
                    ui.chip(
                        text=ticket.ticket_id,
                        icon="arrow_right",
                        on_click=lambda: ui.navigate.to(
                            config_info.UI_ROUTES[
                                config_info.UIPages.TICKET].format(
                                ticket_id=ticket.ticket_id
                            )
                        )
                    ).classes("text-white text-base")
                    ui.label(ticket.title).classes("text-2xl font-bold")
                    ui.space()
                    ui.chip(
                        text=f"Parent Project: {ticket.parent_project}",
                        icon="arrow_right",
                        on_click=lambda: ui.navigate.to(
                            config_info.UI_ROUTES[
                                config_info.UIPages.PROJECT].format(
                                project_id=ticket.parent_project
                            )
                        )
                    ).classes("text-white text-base")
                ui.label(ticket.description).classes("text-lg")
                ui.separator()
                with ui.row().classes("items-center justify-between w-full"):
                    ui.label(f"Created by {ticket.created_by}"
                             f" at {ticket.created_at}")
                    ui.space()
                    ui.label(f"Modified by {ticket.modified_by}"
                             f" at {ticket.modified_at}")
            ui.separator()


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
    return


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

        with ui.expansion("Add Members", icon="people").classes(
                "w-4/5") as all_users_expansion:
            search_member = ui.input(
                label="Search Member",
                on_change=lambda: [
                    checkbox.set_visibility(
                        search_member.value.lower() in user_id.lower()
                        or not search_member
                    )
                    for user_id, checkbox in checkboxes.items()
                ]
            ).classes("w-full")
            for user_id in all_user_ids:
                checkboxes[user_id] = ui.checkbox(user_id).classes("w-full")

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
            time.sleep(1)
            ui.navigate.reload()

        with ui.row().classes("items-center justify-between"):  # Add this line
            ui.button("Create").on(
                "click",
                create_button_clicked
            ).classes("text-white mr-2")
            ui.button("Cancel", color="negative").on(
                "click",
                dialog.close
            ).classes("text-white")

    def open_dialog():
        # Clear the input fields
        project_id.value = ""
        title.value = ""
        description.value = ""
        search_member.value = ""
        all_users_expansion.close()
        # Uncheck all checkboxes
        for checkbox in checkboxes.values():
            checkbox.value = False
        dialog.open()

    with ui.row().classes("items-center justify-between w-full self-center"
                          " px-6 py-2"):
        ui.label("Projects").classes("text-5xl")
        ui.button(
            text="Create Project",
            on_click=open_dialog
        ).classes("text-white")

    ui.separator()

    with ui.column().classes("items-center w-full self-center px-6 py-2"):
        username = app.storage.user.get("username", "")

        get_user_projects_url = (
            config_info.API_URL
            + "/"
            + config_info.API_ROUTES[APIOps.USERS_ALL_PROJECTS].format(
                user_id=username
            )
        )
        user_projects_response = requests.get(get_user_projects_url).json()
        user_projects = [
            models.Project.parse_obj(project)
            for project in user_projects_response["projects"]
        ]

        if not user_projects:
            ui.label("No projects").classes("text-2xl")
            return

        for project in user_projects:
            with ui.card().classes("w-full"):
                with ui.row().classes("items-center justify-between"):
                    ui.chip(
                        text=project.project_id,
                        icon="arrow_right",
                        on_click=lambda: ui.navigate.to(
                            config_info.UI_ROUTES[
                                config_info.UIPages.PROJECT].format(
                                project_id=project.project_id
                            )
                        )
                    ).classes("text-white text-base")
                    ui.label(project.title).classes("text-2xl font-bold")
                ui.label(project.description).classes("text-lg")
                ui.markdown(f"**Members:** {', '.join(project.members)}")
                ui.separator()
                with ui.row().classes("items-center justify-between w-full"):
                    ui.label(f"Created by {project.created_by}"
                             f" at {project.created_at}")
                    ui.space()
                    ui.label(f"Modified by {project.modified_by}"
                             f" at {project.modified_at}")
            ui.separator()

    return None


@apply_header
def tickets() -> None:
    """Tickets page for the TaskPilot application"""
    with ui.dialog() as dialog, ui.card().classes("w-full h-1/2 items-center"):
        ui.label("Create Ticket").classes("text-2xl")
        ticket_id = ui.input("Ticket ID").classes("w-4/5")
        title = ui.input("Title").classes("w-4/5")
        description = ui.textarea("Description").classes("w-4/5")
        ticket_type = ui.select(config_info.TICKET_TYPES,
                                label="Type").classes("w-4/5")
        priority = ui.select(config_info.TICKET_PRIORITIES,
                             label="Priority").classes("w-4/5")

        get_user_projects_url = (
            config_info.API_URL
            + "/"
            + config_info.API_ROUTES[APIOps.USERS_ALL_PROJECTS].format(
                user_id=app.storage.user.get("username", "")
            )
        )
        user_projects = requests.get(get_user_projects_url).json()["projects"]
        user_project_ids = [project["project_id"] for project in user_projects]

        parent_project = ui.select(
            user_project_ids,
            label="Parent Project"
        ).classes("w-4/5")

        def create_button_clicked():
            if not parent_project.value:
                ui.notify("Please select a parent project", color="negative")
                return

            create_ticket_request = api_req.CreateTicketRequest(
                ticket_id=ticket_id.value,
                title=title.value,
                description=description.value,
                type=ticket_type.value,
                priority=priority.value,
                status=config_info.TicketStatuses.NOT_STARTED,
                created_by=app.storage.user.get("username", ""),
                parent_project=parent_project.value
            )
            url = (
                f"{config_info.API_URL}"
                f"/{config_info.API_ROUTES[APIOps.TICKETS_CREATE]}"
            )
            create_ticket_response = requests.post(
                url=url,
                json=create_ticket_request.dict()
            )
            ui.notify(
                create_ticket_response.json().get(
                    "message", "Unable to create ticket"
                ),
                color="positive" if create_ticket_response.json().get(
                    "result", False) else "negative"
            )
            dialog.close()
            time.sleep(1)
            ui.navigate.reload()

        with ui.row().classes("items-center justify-between"):
            ui.button("Create").on(
                "click",
                create_button_clicked
            ).classes("text-white mr-2")
            ui.button("Cancel", color="negative").on(
                "click",
                dialog.close
            ).classes("text-white")

    def open_dialog():
        # Clear the input fields
        ticket_id.value = ""
        title.value = ""
        description.value = ""
        ticket_type.value = config_info.TicketTypes.TASK
        priority.value = config_info.TicketPriorities.NORMAL
        parent_project.value = ""
        dialog.open()

    with ui.row().classes("items-center justify-between w-full self-center"
                          " px-6 py-2"):
        ui.label("Tickets").classes("text-5xl")
        ui.button(
            text="Create Ticket",
            on_click=open_dialog
        ).classes("text-white")
    ui.label(
        "Here is a list of all the tickets that you have access to:"
    ).classes("text-2xl items-center justify-between w-full self-center"
              " px-6 py-2")

    ui.separator()

    with ui.column().classes("items-center w-full self-center px-6 py-2"):
        username = app.storage.user.get("username", "")

        get_user_projects_url = (
            config_info.API_URL
            + "/"
            + config_info.API_ROUTES[APIOps.USERS_ALL_PROJECTS].format(
                user_id=username
            )
        )
        user_projects_response = requests.get(get_user_projects_url).json()
        user_projects = [
            models.Project.parse_obj(project)
            for project in user_projects_response["projects"]
        ]

        user_tickets = []
        for project in user_projects:
            get_project_tickets_url = (
                config_info.API_URL
                + "/"
                + config_info.API_ROUTES[APIOps.PROJECTS_ALL_TICKETS].format(
                    project_id=project.project_id
                )
            )
            project_tickets_response = requests.get(
                get_project_tickets_url).json()
            project_tickets = [
                models.Ticket.parse_obj(ticket)
                for ticket in project_tickets_response["tickets"]
            ]
            user_tickets.extend(project_tickets)

        if not user_tickets:
            ui.label("No tickets").classes("text-2xl")
            return

        for ticket in user_tickets:
            with ui.card().classes("w-full"):
                with ui.row().classes("items-center justify-between w-full"):
                    ui.chip(
                        text=ticket.ticket_id,
                        icon="arrow_right",
                        on_click=lambda: ui.navigate.to(
                            config_info.UI_ROUTES[
                                config_info.UIPages.TICKET].format(
                                ticket_id=ticket.ticket_id
                            )
                        )
                    ).classes("text-white text-base")
                    ui.label(ticket.title).classes("text-2xl font-bold")
                    ui.space()
                    ui.chip(
                        text=f"Parent Project: {ticket.parent_project}",
                        icon="arrow_right",
                        on_click=lambda: ui.navigate.to(
                            config_info.UI_ROUTES[
                                config_info.UIPages.PROJECT].format(
                                project_id=ticket.parent_project
                            )
                        )
                    ).classes("text-white text-base")
                ui.label(ticket.description).classes("text-lg")
                ui.separator()
                ui.label(f"{ticket.type} | Priority: {ticket.priority}"
                         f" | Status: {ticket.status}").classes("text-base")
                ui.label(f"Assignee: {ticket.assignee}")
                ui.separator()
                with ui.row().classes("items-center justify-between w-full"):
                    ui.label(f"Created by {ticket.created_by}"
                             f" at {ticket.created_at}")
                    ui.space()
                    ui.label(f"Modified by {ticket.modified_by}"
                             f" at {ticket.modified_at}")

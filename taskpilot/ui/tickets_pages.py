import time

import requests
from nicegui import ui, app

from taskpilot.common import config_info, api_request_classes as api_req, \
    models
from taskpilot.common.config_info import APIOperations as APIOps


def tickets_page() -> None:
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
        ui.chip(
            text="Create Ticket",
            icon="add",
            on_click=open_dialog
        ).classes("text-white text-base")
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
                        on_click=lambda t=ticket: ui.navigate.to(
                            config_info.UI_ROUTES[
                                config_info.UIPages.TICKET].format(
                                ticket_id=t.ticket_id
                            )
                        )
                    ).classes("text-white text-base")
                    ui.label(ticket.title).classes("text-2xl font-bold")
                    ui.space()
                    ui.chip(
                        text=f"Parent Project: {ticket.parent_project}",
                        icon="arrow_right",
                        on_click=lambda t=ticket: ui.navigate.to(
                            config_info.UI_ROUTES[
                                config_info.UIPages.PROJECT].format(
                                project_id=t.parent_project
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


def ticket_page(ticket_id: str) -> None:  # TODO Functionalities for buttons
    """Ticket page for the TaskPilot application"""
    get_ticket_url = (
        config_info.API_URL
        + "/"
        + config_info.API_ROUTES[APIOps.TICKETS_GET].format(
            ticket_id=ticket_id
        )
    )
    ticket_response = requests.get(get_ticket_url).json()
    ticket = models.Ticket.parse_obj(ticket_response["ticket"])

    with ui.row().classes("items-center justify-between w-full self-center"
                          " px-6 py-2"):
        ui.chip(
            text=ticket.ticket_id,
        ).classes("text-white text-2xl")
        ui.label(ticket.title).classes("text-5xl")
        ui.space()
        with ui.button_group():
            with ui.dropdown_button(f"Type: {ticket.type}",
                                    auto_close=True):
                for ticket_type in config_info.TICKET_TYPES:
                    ui.item(
                        ticket_type,
                        on_click=lambda e=ticket_type, t=ticket: (
                            requests.put(
                                config_info.API_URL
                                + "/"
                                + config_info.API_ROUTES[
                                    APIOps.TICKETS_UPDATE].format(
                                    ticket_id=ticket_id
                                ),
                                json=api_req.UpdateTicketRequest(
                                    title=t.title,
                                    description=t.description,
                                    type=e,
                                    priority=t.priority,
                                    status=t.status,
                                    assignee=t.assignee,
                                    modified_by=app.storage.user.get(
                                        "username", ""),
                                    parent_project=t.parent_project,
                                    parent_ticket=t.parent_ticket
                                ).dict()
                            ),
                            time.sleep(1),
                            ui.navigate.reload()
                        )
                    )
            with ui.dropdown_button(f"Priority: {ticket.priority}",
                                    auto_close=True):
                for ticket_priority in config_info.TICKET_PRIORITIES:
                    ui.item(
                        ticket_priority,
                        on_click=lambda e=ticket_priority, t=ticket: (
                            requests.put(
                                config_info.API_URL
                                + "/"
                                + config_info.API_ROUTES[
                                    APIOps.TICKETS_UPDATE].format(
                                    ticket_id=ticket_id
                                ),
                                json=api_req.UpdateTicketRequest(
                                    title=t.title,
                                    description=t.description,
                                    type=t.type,
                                    priority=e,
                                    status=t.status,
                                    assignee=t.assignee,
                                    modified_by=app.storage.user.get(
                                        "username", ""),
                                    parent_project=t.parent_project,
                                    parent_ticket=t.parent_ticket
                                ).dict()
                            ),
                            time.sleep(1),
                            ui.navigate.reload()
                        )
                    )
            with ui.dropdown_button(f"Status: {ticket.status}",
                                    auto_close=True):
                for ticket_status in config_info.TICKET_STATUSES:
                    ui.item(
                        ticket_status,
                        on_click=lambda e=ticket_status, t=ticket: (
                            requests.put(
                                config_info.API_URL
                                + "/"
                                + config_info.API_ROUTES[
                                    APIOps.TICKETS_UPDATE].format(
                                    ticket_id=ticket_id
                                ),
                                json=api_req.UpdateTicketRequest(
                                    title=t.title,
                                    description=t.description,
                                    type=t.type,
                                    priority=t.priority,
                                    status=e,
                                    assignee=t.assignee,
                                    modified_by=app.storage.user.get(
                                        "username", ""),
                                    parent_project=t.parent_project,
                                    parent_ticket=t.parent_ticket
                                ).dict()
                            ),
                            time.sleep(1),
                            ui.navigate.reload()
                        )
                    )

    with ui.row().classes("items-center justify-between w-full self-center"
                          " px-6 py-2"):
        ui.label(ticket.description).classes("text-3xl")
        parent_project = models.Project.parse_obj(
            requests.get(
                config_info.API_URL
                + "/"
                + config_info.API_ROUTES[APIOps.PROJECTS_GET].format(
                    project_id=ticket.parent_project
                )
            ).json()["project"]
        )
        ui.select(
            label="Assignee",
            value=ticket.assignee if ticket.assignee else "Unassigned",
            options=["Unassigned"] + parent_project.members,
            on_change=lambda e: (requests.put(
                config_info.API_URL
                + "/"
                + config_info.API_ROUTES[APIOps.TICKETS_UPDATE].format(
                    ticket_id=ticket_id
                ),
                json=api_req.UpdateTicketRequest(
                    title=ticket.title,
                    description=ticket.description,
                    type=ticket.type,
                    priority=ticket.priority,
                    status=ticket.status,
                    assignee=e.value if e.value != "Unassigned" else None,
                    modified_by=app.storage.user.get("username", ""),
                    parent_project=ticket.parent_project,
                    parent_ticket=ticket.parent_ticket
                ).dict()
            ), time.sleep(1), ui.navigate.reload())
        ).classes("text-lg w-1/6")

    with ui.row().classes("items-center justify-between w-full self-center"
                          " px-6 py-2"):
        ui.chip(
            text=f"Parent Project: {ticket.parent_project}",
            icon="arrow_right",
            on_click=lambda t=ticket: ui.navigate.to(
                config_info.UI_ROUTES[
                    config_info.UIPages.PROJECT].format(
                    project_id=t.parent_project
                )
            )
        ).classes("text-white text-base")
        if ticket.parent_ticket is not None:
            ui.chip(
                text=f"Parent Ticket: {ticket.parent_ticket}",
                icon="arrow_right",
                on_click=lambda t=ticket: ui.navigate.to(
                    config_info.UI_ROUTES[
                        config_info.UIPages.TICKET].format(
                        ticket_id=t.parent_ticket
                    )
                )
            ).classes("text-white text-base")
        ui.space()
        ui.chip(
            text="Modify Ticket",
            icon="edit",
            color="warning",
            on_click=lambda: None
        ).classes("text-white text-base")
        ui.chip(
            text="Delete Ticket",
            icon="delete",
            color="negative",
            on_click=lambda: None
        ).classes("text-white text-base")

    ui.separator()
    with ui.row().classes("items-center justify-between w-full"):
        ui.label(f"Created by {ticket.created_by}"
                 f" at {ticket.created_at}")
        ui.space()
        ui.label(f"Modified by {ticket.modified_by}"
                 f" at {ticket.modified_at}")
    ui.separator()

    with ui.row().classes("items-center justify-between w-full self-center"
                          " p-6"):
        ui.label("Child Tickets").classes("text-3xl font-bold")
        ui.space()
        ui.chip(
            text="Create Child Ticket",
            icon="add",
            on_click=lambda: None
        ).classes("text-white text-base")
        ui.separator()

    get_child_tickets_url = (
        config_info.API_URL
        + "/"
        + config_info.API_ROUTES[APIOps.TICKETS_ALL_CHILDREN].format(
            ticket_id=ticket_id
        )
    )
    child_tickets_response = requests.get(get_child_tickets_url).json()
    child_tickets = [
        models.Ticket.parse_obj(ticket)
        for ticket in child_tickets_response["tickets"]
    ]

    if not child_tickets:
        ui.label("No child tickets").classes("text-2xl self-center")

    for ticket in child_tickets:
        with ui.card().classes("w-full"):
            with ui.row().classes("items-center justify-between w-full"):
                ui.chip(
                    text=ticket.ticket_id,
                    icon="arrow_right",
                    on_click=lambda t=ticket: ui.navigate.to(
                        config_info.UI_ROUTES[
                            config_info.UIPages.TICKET].format(
                            ticket_id=t.ticket_id
                        )
                    )
                ).classes("text-white text-base")
                ui.label(ticket.title).classes("text-2xl font-bold")
                ui.space()
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
    ui.separator()

    with ui.row().classes("items-center justify-between w-full self-center"
                          " p-6"):
        ui.label("Comments").classes("text-3xl font-bold")
        ui.space()
        ui.chip(
            text="Create Comment",
            icon="add",
            on_click=lambda: None
        ).classes("text-white text-base")
        ui.separator()

    get_ticket_comments_url = (
        config_info.API_URL
        + "/"
        + config_info.API_ROUTES[APIOps.TICKETS_ALL_COMMENTS].format(
            ticket_id=ticket_id
        )
    )
    ticket_comments_response = requests.get(get_ticket_comments_url).json()
    ticket_comments = [
        models.Comment.parse_obj(comment)
        for comment in ticket_comments_response["comments"]
    ]

    if not ticket_comments:
        ui.label("No comments").classes("text-2xl")
        return

    for comment in ticket_comments:
        ui.chat_message(
            comment.text,
            name=comment.created_by,
            stamp=comment.created_at
        ).classes("w-full self-center px-6 py-2").props("color: blue;")

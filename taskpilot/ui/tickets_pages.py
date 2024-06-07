import datetime
import time

import requests
from nicegui import ui, app

from taskpilot.common import config_info, api_request_classes as api_req, \
    models
from taskpilot.common.config_info import APIOperations as APIOps


def tickets_page() -> None:
    """Tickets page for the TaskPilot application"""
    with ui.dialog() as dialog, ui.card().classes("w-full items-center"):
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

        user_tickets.sort(key=lambda ticket: datetime.datetime.strptime(
            ticket.modified_at, "%d-%m-%Y %H:%M:%S"), reverse=True)

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


def ticket_page(ticket_id: str) -> None:
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

    is_user_member_of_project = requests.get(
        config_info.API_URL
        + "/"
        + config_info.API_ROUTES[APIOps.PROJECTS_IS_USER_MEMBER].format(
            project_id=ticket.parent_project,
            user_id=app.storage.user.get("username", "")
        )
    ).json()["result"]
    if not is_user_member_of_project:
        ui.navigate.to(
            config_info.UI_ROUTES[config_info.UIPages.PROJECTS]
        )

    is_user_owner_of_ticket = requests.get(
        config_info.API_URL
        + "/"
        + config_info.API_ROUTES[APIOps.TICKETS_IS_USER_OWNER].format(
            ticket_id=ticket_id,
            user_id=app.storage.user.get("username", "")
        )
    ).json()["result"]

    with ui.dialog() as modify_ticket_dialog, ui.card().classes(
            "w-full items-center"):
        ui.label("Modify Ticket").classes("text-2xl")
        title = ui.input("Title", value=ticket.title).classes("w-4/5")
        description = ui.textarea("Description",
                                    value=ticket.description).classes("w-4/5")
        parent_ticket = ui.select(
            label="Parent Ticket",
            options=["None"] + [ticket["ticket_id"]
             for ticket in requests.get(
                config_info.API_URL
                + "/"
                + config_info.API_ROUTES[APIOps.PROJECTS_ALL_TICKETS].format(
                    project_id=ticket.parent_project
                )
            ).json()["tickets"]],
            value=ticket.parent_ticket if ticket.parent_ticket else "None"
        ).classes("w-4/5")
        with ui.row().classes("items-center justify-between"):
            ui.button(
                "Modify",
                color="warning",
                on_click=lambda: (
                    requests.put(
                        config_info.API_URL
                        + "/"
                        + config_info.API_ROUTES[APIOps.TICKETS_UPDATE].format(
                            ticket_id=ticket_id
                        ),
                        json=api_req.UpdateTicketRequest(
                            title=title.value,
                            description=description.value,
                            type=ticket.type,
                            priority=ticket.priority,
                            status=ticket.status,
                            assignee=ticket.assignee,
                            modified_by=app.storage.user.get("username", ""),
                            parent_project=ticket.parent_project,
                            parent_ticket=(parent_ticket.value
                                           if parent_ticket.value != "None"
                                           else None)
                        ).dict()
                    ),
                    modify_ticket_dialog.close(),
                    time.sleep(1),
                    ui.navigate.reload()
                )
            ).classes("text-white mr-2")
            ui.button("Cancel", on_click=modify_ticket_dialog.close
                      ).classes("text-white")

    with ui.dialog() as delete_ticket_dialog, ui.card().classes(
            "w-full items-center"):
        ui.label("Delete Ticket").classes("text-2xl")
        ui.label("Are you sure you want to delete this ticket?").classes(
            "text-lg")
        with ui.row().classes("items-center justify-between"):
            ui.button(
                "Delete",
                color="negative",
                on_click=lambda: (
                    requests.delete(
                        config_info.API_URL
                        + "/"
                        + config_info.API_ROUTES[APIOps.TICKETS_DELETE].format(
                            ticket_id=ticket_id
                        )
                    ),
                    delete_ticket_dialog.close(),
                    time.sleep(1),
                    ui.navigate.to(
                        config_info.UI_ROUTES[config_info.UIPages.TICKETS]
                    )
                )
            ).classes("text-white mr-2")
            ui.button("Cancel", on_click=delete_ticket_dialog.close
                      ).classes("text-white")

    with ui.dialog() as create_child_ticket_dialog, ui.card().classes(
            "w-full items-center"):
        ui.label("Create Child Ticket").classes("text-2xl")
        child_ticket_id = ui.input("Ticket ID").classes("w-4/5")
        child_title = ui.input("Title").classes("w-4/5")
        child_description = ui.textarea("Description").classes("w-4/5")
        child_ticket_type = ui.select(config_info.TICKET_TYPES,
                                        label="Type").classes("w-4/5")
        child_priority = ui.select(config_info.TICKET_PRIORITIES,
                                   label="Priority").classes("w-4/5")
        with ui.row().classes("items-center justify-between"):
            ui.button(
                "Create",
                on_click=lambda t=ticket: (
                    requests.post(
                        config_info.API_URL
                        + "/"
                        + config_info.API_ROUTES[APIOps.TICKETS_CREATE],
                        json=api_req.CreateTicketRequest(
                            ticket_id=child_ticket_id.value,
                            title=child_title.value,
                            description=child_description.value,
                            type=child_ticket_type.value,
                            priority=child_priority.value,
                            status=config_info.TicketStatuses.NOT_STARTED,
                            created_by=app.storage.user.get("username", ""),
                            parent_project=t.parent_project,
                            parent_ticket=ticket_id
                        ).dict()
                    ),
                    create_child_ticket_dialog.close(),
                    time.sleep(1),
                    ui.navigate.reload()
                )
            ).classes("text-white mr-2")
            ui.button("Cancel", on_click=create_child_ticket_dialog.close
                      ).classes("text-white")

    def open_create_child_ticket_dialog():
        # Clear the input fields
        child_ticket_id.value = ""
        child_title.value = ""
        child_description.value = ""
        child_ticket_type.value = config_info.TicketTypes.TASK
        child_priority.value = config_info.TicketPriorities.NORMAL

        create_child_ticket_dialog.open()

    with ui.dialog() as create_comment_dialog, ui.card().classes(
            "w-full items-center"):
        ui.label("Create Comment").classes("text-2xl")
        comment_content = ui.textarea("Comment").classes("w-4/5")
        with ui.row().classes("items-center justify-between"):
            ui.button(
                "Add Comment",
                on_click=lambda: (
                    requests.post(
                        config_info.API_URL
                        + "/"
                        + config_info.API_ROUTES[APIOps.COMMENTS_CREATE],
                        json=api_req.CreateCommentRequest(
                            ticket_id=ticket_id,
                            text=comment_content.value,
                            created_by=app.storage.user.get("username", "")
                        ).dict()
                    ),
                    create_comment_dialog.close(),
                    time.sleep(1),
                    ui.navigate.reload()
                )
            ).classes("text-white mr-2")
            ui.button("Cancel", on_click=create_comment_dialog.close
                      ).classes("text-white")

    def open_create_comment_dialog():
        # Clear the input fields
        comment_content.value = ""
        create_comment_dialog.open()

    with ui.row().classes("items-center justify-between w-full self-center"
                          " px-6 py-2"):
        ui.chip(
            text=ticket.ticket_id,
        ).classes("text-white text-2xl")
        ui.label(ticket.title).classes("text-5xl")
        ui.space()
        with ui.button_group():
            if is_user_owner_of_ticket:
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
            else:
                ui.button(f"Type: {ticket.type}")
                ui.button(f"Priority: {ticket.priority}")
            if (is_user_owner_of_ticket or
                    ticket.assignee == app.storage.user.get("username", "")):
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
            else:
                ui.button(f"Status: {ticket.status}")

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
            options=(
                ["Unassigned"] + parent_project.members
                if is_user_owner_of_ticket
                else list(
                    {ticket.assignee, app.storage.user.get("username", "")}
                )
            ),
            on_change=lambda e, t=ticket: (requests.put(
                config_info.API_URL
                + "/"
                + config_info.API_ROUTES[APIOps.TICKETS_UPDATE].format(
                    ticket_id=ticket_id
                ),
                json=api_req.UpdateTicketRequest(
                    title=t.title,
                    description=t.description,
                    type=t.type,
                    priority=t.priority,
                    status=t.status,
                    assignee=e.value if e.value != "Unassigned" else None,
                    modified_by=app.storage.user.get("username", ""),
                    parent_project=t.parent_project,
                    parent_ticket=t.parent_ticket
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
        if is_user_owner_of_ticket:
            ui.chip(
                text="Modify Ticket",
                icon="edit",
                color="warning",
                on_click=modify_ticket_dialog.open
            ).classes("text-white text-base")
            ui.chip(
                text="Delete Ticket",
                icon="delete",
                color="negative",
                on_click=delete_ticket_dialog.open
            ).classes("text-white text-base")

    with ui.row().classes("items-center justify-between w-full px-6 py-2"):
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
            on_click=open_create_child_ticket_dialog
        ).classes("text-white text-base")

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

    with ui.column().classes("items-center w-full self-center px-6 py-2"):
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
            text="Add Comment",
            icon="add",
            on_click=open_create_comment_dialog
        ).classes("text-white text-base")

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
        ui.label("No comments").classes("text-2xl self-center")
        return

    with ui.column().classes("items-center w-full self-center px-6 py-2"):
        for ticket_comment in ticket_comments:
            with ui.card().classes("w-full justify-between"):
                with ui.row().classes("items-center justify-between w-full"):
                    ui.label(ticket_comment.created_by).classes("text-lg px-4")
                    ui.space()
                    ui.label(ticket_comment.created_at).classes("text-base"
                                                                " px-4")
                    if requests.get(
                            config_info.API_URL
                            + "/"
                            + config_info.API_ROUTES[
                                APIOps.COMMENTS_IS_USER_OWNER].format(
                                comment_id=ticket_comment.comment_id,
                                user_id=app.storage.user.get("username", "")
                            )
                    ).json()["result"]:
                        ui.chip(
                            "Delete",
                            icon="delete",
                            color="negative",
                            on_click=lambda c=ticket_comment: (
                                requests.delete(
                                    config_info.API_URL
                                    + "/"
                                    + config_info.API_ROUTES[
                                        APIOps.COMMENTS_DELETE].format(
                                        comment_id=c.comment_id
                                    )
                                ),
                                time.sleep(1),
                                ui.navigate.reload()
                            )
                        ).classes("text-white text-base")
                ui.separator()
                ui.label(ticket_comment.text).classes("text-2xl p-4")

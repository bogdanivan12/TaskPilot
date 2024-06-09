import time

import requests
from nicegui import ui, app

from taskpilot.common import config_info, api_request_classes as api_req, \
    models
from taskpilot.common.config_info import APIOperations as APIOps


def projects_page() -> None:
    """Projects page for the TaskPilot application"""
    with ui.dialog() as dialog, ui.card().classes("w-full items-center"):
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
        ui.chip(
            text="Create Project",
            icon="add",
            on_click=open_dialog
        ).classes("text-white text-base")

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
                        on_click=lambda p=project: ui.navigate.to(
                            config_info.UI_ROUTES[
                                config_info.UIPages.PROJECT].format(
                                project_id=p.project_id
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


def project_page(project_id: str) -> None:
    """Project page for the TaskPilot application"""
    app.storage.user.update({
        "context": {
            "project": project_id,
            "ticket": None
        }
    })
    is_user_member_of_project = requests.get(
        config_info.API_URL
        + "/"
        + config_info.API_ROUTES[APIOps.PROJECTS_IS_USER_MEMBER].format(
            project_id=project_id,
            user_id=app.storage.user.get("username", "")
        )
    ).json()["result"]
    if not is_user_member_of_project:
        ui.navigate.to(
            config_info.UI_ROUTES[config_info.UIPages.PROJECTS]
        )

    with ui.dialog() as dialog, ui.card().classes("w-full items-center"):
        ui.label("Create Ticket").classes("text-2xl")
        ticket_title = ui.input("Title").classes("w-4/5")
        ticket_description = ui.textarea("Description").classes("w-4/5")
        ticket_type = ui.select(config_info.TICKET_TYPES,
                                label="Type").classes("w-4/5")
        priority = ui.select(config_info.TICKET_PRIORITIES,
                             label="Priority").classes("w-4/5")

        parent_project = ui.select(
            [project_id],
            value=project_id,
            label="Parent Project"
        ).classes("w-4/5")

        def create_button_clicked():
            next_ticket_id = requests.get(
                config_info.API_URL
                + "/"
                + config_info.API_ROUTES[APIOps.PROJECTS_GET].format(
                    project_id=parent_project.value
                )
            ).json()["project"]["next_ticket_id"]

            create_ticket_request = api_req.CreateTicketRequest(
                ticket_id=f"{parent_project.value}-{next_ticket_id}",
                title=ticket_title.value,
                description=ticket_description.value,
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
        ticket_title.value = ""
        ticket_description.value = ""
        ticket_type.value = config_info.TicketTypes.TASK
        priority.value = config_info.TicketPriorities.NORMAL
        parent_project.value = project.project_id
        dialog.open()

    project = models.Project.parse_obj(
        requests.get(
            config_info.API_URL
            + "/"
            + config_info.API_ROUTES[APIOps.PROJECTS_GET].format(
                project_id=project_id
            )
        ).json()["project"]
    )

    with ui.dialog() as edit_dialog, ui.card().classes("w-full items-center"):
        ui.label("Edit Project").classes("text-2xl")
        title = ui.input("Title", value=project.title).classes("w-4/5")
        description = ui.textarea("Description",
                                  value=project.description).classes("w-4/5")

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
                checkboxes[user_id] = ui.checkbox(
                    user_id,
                    value=user_id in project.members
                ).classes("w-full")

        def edit_button_clicked():
            selected_user_ids = [
                user_id for user_id, checkbox in checkboxes.items()
                if checkbox.value
            ] + [app.storage.user.get("username", "")]
            edit_dialog.close()
            edit_project_request = api_req.UpdateProjectRequest(
                title=title.value,
                description=description.value,
                modified_by=app.storage.user.get("username", ""),
                members=selected_user_ids
            )
            url = (
                config_info.API_URL
                + "/"
                + config_info.API_ROUTES[APIOps.PROJECTS_UPDATE].format(
                    project_id=project_id
                )
            )
            edit_project_response = requests.put(
                url=url,
                json=edit_project_request.dict()
            )
            ui.notify(
                edit_project_response.json().get(
                    "message", "Unable to edit project"
                ),
                color="positive" if edit_project_response.json().get(
                    "result", False) else "negative"
            )
            time.sleep(1)
            ui.navigate.reload()

        with ui.row().classes("items-center justify-between"):
            ui.button(
                "Modify",
                on_click=edit_button_clicked,
                color="warning"
            ).classes("text-white mr-2")
            ui.button(
                "Cancel",
                on_click=edit_dialog.close
            ).classes("text-white")

    with ui.dialog() as delete_dialog, ui.card().classes(
            "w-full items-center"):
        ui.label("Delete Project").classes("text-2xl")
        ui.label(
            "Are you sure you want to delete this project?"
        ).classes("text-lg")
        ui.label(
            "This action cannot be undone."
        ).classes("text-lg")

        def delete_button_clicked():
            delete_dialog.close()
            delete_project_response = requests.delete(
                config_info.API_URL
                + "/"
                + config_info.API_ROUTES[APIOps.PROJECTS_DELETE].format(
                    project_id=project_id
                )
            )
            ui.notify(
                delete_project_response.json().get(
                    "message", "Unable to delete project"
                ),
                color="positive" if delete_project_response.json().get(
                    "result", False) else "negative"
            )
            time.sleep(1)
            ui.navigate.to(
                config_info.UI_ROUTES[config_info.UIPages.PROJECTS]
            )

        with ui.row().classes("items-center justify-between"):
            ui.button(
                "Delete",
                on_click=delete_button_clicked,
                color="negative"
            ).classes("text-white mr-2")
            ui.button(
                "Cancel",
                on_click=delete_dialog.close
            ).classes("text-white")

    get_project_url = (
        config_info.API_URL
        + "/"
        + config_info.API_ROUTES[APIOps.PROJECTS_GET].format(
            project_id=project_id
        )
    )
    project_response = requests.get(get_project_url).json()
    project = models.Project.parse_obj(project_response["project"])

    with ui.row().classes("items-center justify-between w-full self-center"
                          " px-6 py-2"):
        ui.chip(text=project.project_id).classes("text-white text-2xl")
        ui.label(project.title).classes("text-5xl")
        ui.space()
        ui.chip(
            text="Create Ticket",
            on_click=open_dialog,
            icon="add"
        ).classes("text-white text-base")

    ui.label(project.description
             ).classes("text-3xl items-center justify-between w-full"
                       " self-center px-6 py-2")

    ui.label(
        f"Members: {', '.join(project.members)}"
    ).classes("text-xl items-center justify-between w-full self-center"
              " px-6 py-2")

    is_user_owner_of_project = requests.get(
        config_info.API_URL
        + "/"
        + config_info.API_ROUTES[APIOps.PROJECTS_IS_USER_OWNER].format(
            project_id=project_id,
            user_id=app.storage.user.get("username", "")
        )
    ).json()["result"]
    if is_user_owner_of_project:
        with ui.row().classes("items-center justify-between w-full self-center"
                              " px-6 py-2"):
            ui.space()
            ui.chip(
                "Modify Project",
                on_click=edit_dialog.open,
                icon="edit",
                color="warning"
            ).classes("text-white text-base")
            ui.chip(
                "Delete Ticket",
                on_click=delete_dialog.open,
                icon="delete",
                color="negative"
            ).classes("text-white text-base")

    with ui.row().classes("items-center justify-between w-full self-center"
                          " px-6 py-2"):
        ui.label(f"Created by {project.created_by} at {project.created_at}")
        ui.space()
        ui.label(f"Modified by {project.modified_by} at {project.modified_at}")

    ui.separator()

    with ui.column().classes("items-center w-full self-center px-6 py-2"):
        get_project_tickets_url = (
                config_info.API_URL
                + "/"
                + config_info.API_ROUTES[APIOps.PROJECTS_ALL_TICKETS].format(
            project_id=project_id
        )
        )
        project_tickets_response = requests.get(get_project_tickets_url).json()
        project_tickets = [
            models.Ticket.parse_obj(ticket)
            for ticket in project_tickets_response["tickets"]
        ]

        if not project_tickets:
            ui.label("No tickets").classes("text-2xl")
            return

        for ticket in project_tickets:
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

import requests

from nicegui import ui, app

from taskpilot.common import config_info
from taskpilot.common import models
from taskpilot.common.config_info import APIOperations as APIOps
from taskpilot.common import api_request_classes as api_req
from taskpilot.ui.auth_pages import is_user_authenticated


def get_overall_context(username: str) -> str:
    """
    Get the overall context for the user about the projects and the tickets
    they have access to
    """
    overall_context = []

    projects = requests.get(
        config_info.API_URL
        + "/"
        + config_info.API_ROUTES[APIOps.USERS_ALL_PROJECTS].format(
            user_id=username)
    ).json()["projects"]

    projects = [
        models.Project.parse_obj(project) for project in projects
    ]

    for project in projects:
        project_dict = project.dict()
        project_dict["tickets"] = []

        tickets = requests.get(
            config_info.API_URL
            + "/"
            + config_info.API_ROUTES[APIOps.PROJECTS_ALL_TICKETS].format(
                project_id=project.project_id)
        ).json()["tickets"]

        tickets = [
            models.Ticket.parse_obj(ticket) for ticket in tickets
        ]

        for ticket in tickets:
            ticket_dict = ticket.dict()
            ticket_dict["comments"] = []

            comments = requests.get(
                config_info.API_URL
                + "/"
                + config_info.API_ROUTES[APIOps.TICKETS_ALL_COMMENTS].format(
                    ticket_id=ticket.ticket_id)
            ).json()["comments"]

            comments = [
                models.Comment.parse_obj(comment) for comment in comments
            ]

            for comment in comments:
                ticket_dict["comments"].append(comment.dict())

            project_dict["tickets"].append(ticket_dict)

        overall_context.append(project_dict)

    return (
        f"The user has access the following resources of the app:"
        f" {overall_context}. Help him by providing the necessary information"
        f" related to the projects, tasks and comments they have access to."
    )


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
            "text-3xl font-bold text-white absolute-center")
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

    if is_user_auth:
        with ui.element("q-fab").props(
                "icon=chat label=TaskPilotAI direction=up color=blue"
                " vertical-actions-align=right").classes("fixed bottom-4"
                                                         " right-4"):
            with ui.card().classes("w-96 h-96 bg-sky-100"
                                   " self-end") as chat_card:
                @ui.refreshable
                def get_chat_history():
                    chat_history = app.storage.user.get("chat_history", [])
                    for chat in chat_history:
                        if chat["role"] == "assistant":
                            ui.chat_message(
                                text=chat["content"],
                                name="TaskPilot"
                            ).classes("self-start")
                        elif chat["role"] == "user":
                            ui.chat_message(
                                text=chat["content"],
                                name=app.storage.user.get("username", ""),
                                sent=True
                            ).classes("self-end")


                with ui.scroll_area().classes("w-full h-4/5"):
                    ui.label("Chat with TaskPilot AI").classes("text-lg"
                                                               " font-bold")
                    ui.separator()
                    ui.chat_message(
                        text="Hi! I am TaskPilot, your AI Project Manager."
                             " How can I help you?",
                        name="TaskPilot"
                    )

                    get_chat_history()

                with ui.row().classes("w-96 fixed bottom-4 items-center"
                                      " self-center justify-center px-4"):
                    def send_message():
                        message = user_message.value
                        user_message.value = ""
                        if not message.strip():
                            return

                        chat_history = app.storage.user.get("chat_history", [])
                        openai_request = api_req.AIRequest(
                            prompt=message,
                            chat_history=chat_history
                        )
                        if not chat_history:
                            openai_request.system_prompt = (
                                config_info.AI_INSTRUCTIONS
                                + get_overall_context(
                                    app.storage.user.get("username", "")
                                )
                            )

                        chat_history.append({
                            "role": "user",
                            "content": message
                        })
                        app.storage.user.update({
                            "chat_history": chat_history
                        })
                        get_chat_history.refresh()

                        openai_response = requests.post(
                            url=f"{config_info.API_URL}"
                                f"/{config_info.API_ROUTES[APIOps.AI]}",
                            json=openai_request.dict()
                        ).json()
                        app.storage.user.update(
                            {
                                "chat_history": openai_response["chat_history"]
                            }
                        )
                        get_chat_history.refresh()

                    user_message = ui.input("Type your message here").on(
                        "keydown.enter",
                        lambda: send_message()
                    ).classes("w-8/12")

                    ui.chip(
                        text="Send",
                        icon="send",
                        on_click=lambda: send_message(),
                        text_color="white"
                    )

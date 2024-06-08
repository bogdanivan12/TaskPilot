from nicegui import ui, app

from taskpilot.common import config_info
from taskpilot.ui.auth_pages import is_user_authenticated


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
                with ui.scroll_area().classes("w-full h-4/5"):
                    ui.label("Chat with TaskPilot AI").classes("text-lg"
                                                               " font-bold")
                    ui.separator()
                    ui.chat_message(
                        text="Hi! I am TaskPilot, your AI Project Manager."
                             " How can I help you?",
                        name="TaskPilot"
                    )

                    @ui.refreshable
                    def get_chat_history():
                        chat_history = app.storage.user.get("chat_history", [])
                        for chat in chat_history:
                            ui.chat_message(
                                text=chat["content"],
                                name=(
                                    "TaskPilot" if chat["role"] == "system"
                                    else app.storage.user.get("username", "")
                                ),
                                sent=chat["role"] == "user"
                            ).classes(
                                f"self-{'end' if chat['role'] == 'user' else 'start'}"
                            )

                    get_chat_history()

                with ui.row().classes("w-96 fixed bottom-4 items-center"
                                      " self-center justify-center px-4"):
                    user_message = ui.input("Type your message here").on(
                        "keydown.enter",
                        lambda: add_message_chat_history(user_message.value,
                                                         "user")
                    ).classes("w-8/12")

                    def add_message_chat_history(message: str, role: str):
                        app.storage.user.update(
                            {
                                "chat_history": app.storage.user.get(
                                    "chat_history", [])
                                                + [{"content": message,
                                                    "role": role}]
                            }
                        )
                        get_chat_history.refresh()
                        user_message.value = ""

                    ui.chip(
                        text="Send",
                        icon="send",
                        on_click=lambda: add_message_chat_history(
                            user_message.value, "user"),
                        text_color="white"
                    )

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

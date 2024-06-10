"""Page helpers for the TaskPilot application"""
import requests
from nicegui import app, ui

from taskpilot.common import config_info
from taskpilot.common.config_info import APIOperations as APIOps
from taskpilot.common import models
from taskpilot.ui import header_page
from taskpilot.ui import projects_pages
from taskpilot.ui import tickets_pages
from taskpilot.ui import user_pages

from typing import List, Dict


def apply_header(func):
    """Apply the header to the page"""
    def wrapper(*args, **kwargs):
        header_page.header_page()
        func(*args, **kwargs)
    return wrapper


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
    return user_pages.login_page()


@apply_header
def register() -> None:
    """Register page for the TaskPilot application"""
    return user_pages.register_page()


@apply_header
def projects() -> None:
    """Projects page for the TaskPilot application"""
    return projects_pages.projects_page()


@apply_header
def project(project_id: str) -> None:
    """Project page for the TaskPilot application"""
    return projects_pages.project_page(project_id)


@apply_header
def tickets() -> None:
    """Tickets page for the TaskPilot application"""
    return tickets_pages.tickets_page()


@apply_header
def ticket(ticket_id: str) -> None:
    """Ticket page for the TaskPilot application"""
    return tickets_pages.ticket_page(ticket_id)


@apply_header
def profile(user_id: str) -> None:
    """Profile page for the TaskPilot application"""
    return user_pages.profile_page(user_id)

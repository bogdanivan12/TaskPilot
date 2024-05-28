import requests

from taskpilot.common import config_info, api_request_classes as api_req

CREATE_USER_REQUESTS = [
    api_req.CreateUserRequest(
        username="bogdan_ivan",
        email="bogdan.ivan@s.unibuc.ro",
        full_name="Bogdan Ivan",
        password="PassBogdan!123"
    ),
    api_req.CreateUserRequest(
        username="admin",
        email="admin@taskpilot.com",
        full_name="Admin TaskPilot",
        password="admin",
        is_admin=True
    ),
    api_req.CreateUserRequest(
        username="user",
        email="user@taskpilot.com",
        full_name="User TaskPilot",
        password="user"
    )
]

CREATE_PROJECT_REQUESTS = [
    api_req.CreateProjectRequest(
        project_id="TaskPilot",
        title="TaskPilot",
        description="Project Management Platform",
        created_by="bogdan_ivan",
        members=["user", "bogdan_ivan"]
    ),
    api_req.CreateProjectRequest(
        project_id="Licenta",
        title="Redactarea Lucrarii de Licenta",
        description="",
        created_by="bogdan_ivan",
        members=["bogdan_ivan", "admin"]
    )
]

CREATE_TASK_REQUESTS = [
    api_req.CreateTicketRequest(
        ticket_id="TaskPilot-1",
        title="Create API",
        description="Create the API for TaskPilot",
        type="Story",
        priority="High",
        status="Open",
        created_by="bogdan_ivan",
        parent_project="TaskPilot",
        assignee="bogdan_ivan"
    ),
    api_req.CreateTicketRequest(
        ticket_id="TaskPilot-2",
        title="Create Frontend",
        description="Create the Frontend for TaskPilot",
        type="Story",
        priority="Normal",
        status="Open",
        created_by="bogdan_ivan",
        parent_project="TaskPilot",
        assignee="bogdan_ivan"
    ),
    api_req.CreateTicketRequest(
        ticket_id="TaskPilot-3",
        title="Create Database",
        description="Create the Database for TaskPilot",
        type="Task",
        priority="High",
        status="Open",
        created_by="bogdan_ivan",
        parent_project="TaskPilot",
        assignee="bogdan_ivan"
    ),
    api_req.CreateTicketRequest(
        ticket_id="TaskPilot-4",
        title="Create API Models",
        description="Create the API Models for TaskPilot",
        type="Task",
        priority="High",
        status="Open",
        created_by="bogdan_ivan",
        parent_project="TaskPilot",
        parent_ticket="TaskPilot-1",
        assignee="user"
    ),
    api_req.CreateTicketRequest(
        ticket_id="Licenta-1",
        title="Capitolul 1",
        description="Redactarea Capitolului 1",
        type="Task",
        priority="Normal",
        status="Open",
        created_by="bogdan_ivan",
        parent_project="Licenta",
        assignee="bogdan_ivan"
    )
]

CREATE_COMMENT_REQUESTS = [
    api_req.CreateCommentRequest(
        comment_id="TaskPilot-1-1",
        ticket_id="TaskPilot-1",
        text="I will create the API for TaskPilot",
        created_by="bogdan_ivan"
    ),
    api_req.CreateCommentRequest(
        comment_id="TaskPilot-1-2",
        ticket_id="TaskPilot-1",
        text="Update: I have created the project structure for TaskPilot",
        created_by="bogdan_ivan"
    ),
    api_req.CreateCommentRequest(
        comment_id="TaskPilot-2-1",
        ticket_id="TaskPilot-2",
        text="I will create the Frontend for TaskPilot",
        created_by="bogdan_ivan"
    ),
    api_req.CreateCommentRequest(
        comment_id="TaskPilot-3-1",
        ticket_id="TaskPilot-3",
        text="I will create the Database for TaskPilot",
        created_by="bogdan_ivan"
    ),
    api_req.CreateCommentRequest(
        comment_id="TaskPilot-4-1",
        ticket_id="TaskPilot-4",
        text="I will create the API Models for TaskPilot",
        created_by="user"
    ),
    api_req.CreateCommentRequest(
        comment_id="Licenta-1-1",
        ticket_id="Licenta-1",
        text="Do the needful",
        created_by="admin"
    )
]


def create_users():
    """Create users"""
    url = (
        f"http://{config_info.HOST}:{config_info.API_PORT}"
        f"/{config_info.API_ROUTES[config_info.APIOperations.USERS_CREATE]}"
    )
    for request in CREATE_USER_REQUESTS:
        response = requests.post(
            url=url,
            json=request.dict()
        )
        print(f"[{response.json()['result']}] Create User Response for request"
              f" {request}: {response.json()}")


def create_projects():
    """Create projects"""
    url = (
        f"http://{config_info.HOST}:{config_info.API_PORT}"
        f"/{config_info.API_ROUTES[config_info.APIOperations.PROJECTS_CREATE]}"
    )
    for request in CREATE_PROJECT_REQUESTS:
        response = requests.post(
            url=url,
            json=request.dict()
        )
        print(f"[{response.json()['result']}] Create Project Response for"
              f" request {request}: {response.json()}")


def create_tasks():
    """Create tasks"""
    url = (
        f"http://{config_info.HOST}:{config_info.API_PORT}"
        f"/{config_info.API_ROUTES[config_info.APIOperations.TICKETS_CREATE]}"
    )
    for request in CREATE_TASK_REQUESTS:
        response = requests.post(
            url=url,
            json=request.dict()
        )
        print(f"[{response.json()['result']}] Create Task Response for request"
              f" {request}: {response.json()}")


def create_comments():
    """Create comments"""
    url = (
        f"http://{config_info.HOST}:{config_info.API_PORT}"
        f"/{config_info.API_ROUTES[config_info.APIOperations.COMMENTS_CREATE]}"
    )
    for request in CREATE_COMMENT_REQUESTS:
        response = requests.post(
            url=url,
            json=request.dict()
        )
        print(f"[{response.json()['result']}] Create Comment Response for"
              f" request {request}: {response.json()}")


if __name__ == "__main__":
    create_users()
    create_projects()
    create_tasks()
    create_comments()

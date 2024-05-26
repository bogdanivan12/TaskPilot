"""API request classes"""
from typing import List, Optional
from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    """Create user request model"""
    username: str
    email: str
    full_name: str
    password: str
    is_admin: bool = False
    disabled: bool = False


class UpdateUserRequest(BaseModel):
    """Update user request model"""
    email: str
    full_name: str
    password: str
    is_admin: bool = False
    disabled: bool = False
    favorite_tickets: List[str] = []
    projects: List[str] = []


class SearchUsersRequest(BaseModel):
    """Search users request model"""
    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_admin: Optional[bool] = None
    disabled: Optional[bool] = None


class CreateProjectRequest(BaseModel):
    """Create project request model"""
    project_id: str
    title: str
    description: str
    created_by: str
    members: List[str] = []


class UpdateProjectRequest(BaseModel):
    """Update project request model"""
    title: str
    description: str
    modified_by: str
    members: List[str] = []


class SearchProjectsRequest(BaseModel):
    """Search projects request model"""
    title: Optional[str] = None
    description: Optional[str] = None
    created_by: Optional[str] = None
    modified_by: Optional[str] = None
    members: Optional[List[str]] = None


class CreateTicketRequest(BaseModel):
    """Create ticket request model"""
    ticket_id: str
    title: str
    description: str
    type: str
    priority: str
    status: str
    assignee: Optional[str] = None
    created_by: str
    parent_project: str
    parent_ticket: Optional[str] = None


class UpdateTicketRequest(BaseModel):
    """Update ticket request model"""
    title: str
    description: str
    type: str
    priority: str
    status: str
    assignee: Optional[str] = None
    modified_by: str
    parent_project: str
    parent_ticket: Optional[str] = None


class SearchTicketsRequest(BaseModel):
    """Search tickets request model"""
    title: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    assignee: Optional[str] = None
    created_by: Optional[str] = None
    modified_by: Optional[str] = None
    parent_project: Optional[str] = None
    parent_ticket: Optional[str] = None

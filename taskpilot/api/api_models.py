"""API models"""
import datetime

from typing import List, Optional
from pydantic import BaseModel


class User(BaseModel):
    """User model"""
    username: str
    email: str
    full_name: str
    hashed_password: str
    is_admin: bool = False
    favorite_tickets: List[str] = []
    projects: List[str] = []


class Ticket(BaseModel):
    """Ticket model"""
    ticket_id: str
    title: str
    description: str
    type: str
    priority: str
    status: str
    assignee: Optional[str] = None
    created_by: str
    created_at: str
    modified_by: str
    modified_at: str
    parent_project: str
    parent_ticket: Optional[str] = None


class Comment(BaseModel):
    """Comment model"""
    comment_id: str
    ticket_id: str
    text: str
    created_by: str
    created_at: str


class Project(BaseModel):
    """Project model"""
    project_id: str
    title: str
    description: str
    created_by: str
    created_at: str
    modified_by: str
    modified_at: str

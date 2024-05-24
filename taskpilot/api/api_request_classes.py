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


class UpdateUserRequest(BaseModel):
    """Update user request model"""
    email: str
    full_name: str
    password: str
    is_admin: bool = False
    favorite_tickets: List[str] = []
    projects: List[str] = []


class SearchUsersRequest(BaseModel):
    """Search users request model"""
    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_admin: Optional[bool] = None

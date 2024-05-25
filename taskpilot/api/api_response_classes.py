"""API response classes"""
from typing import List, Optional
from pydantic import BaseModel

from taskpilot.api import api_models as models


class Response(BaseModel):
    """Response model"""
    message: str
    code: int = 200
    result: bool = True


class GetUserResponse(Response):
    """Get user response model"""
    user: Optional[models.User] = None


class GetAllUsersResponse(Response):
    """Get all users response model"""
    users: Optional[List[models.User]] = None


class GetProjectResponse(Response):
    """Get project response model"""
    project: Optional[models.Project] = None


class GetAllProjectsResponse(Response):
    """Get all projects response model"""
    projects: Optional[List[models.Project]] = None

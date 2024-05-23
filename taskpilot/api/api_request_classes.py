"""API request classes"""
from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    """Create user request model"""
    username: str
    email: str
    full_name: str
    password: str

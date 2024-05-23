"""API response classes"""
from typing import Any
from pydantic import BaseModel


class Response(BaseModel):
    """Response model"""
    message: str
    code: int = 200
    result: bool = True
    data: Any = None

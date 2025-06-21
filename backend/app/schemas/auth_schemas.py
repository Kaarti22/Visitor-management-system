"""
schemas/auth_schemas.py — Schemas related to authentication workflows like login and token generation.
"""

from pydantic import BaseModel


class LoginInput(BaseModel):
    """
    Schema used when a user logs in.
    """
    email: str
    password: str


class TokenResponse(BaseModel):
    """
    Schema for sending the JWT access token back to the client after successful login.
    """
    access_token: str
    token_type: str = "bearer"

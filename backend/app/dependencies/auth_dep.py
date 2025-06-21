"""
dependencies/auth_dep.py — Dependency for extracting the current authenticated user from JWT token.
"""

from fastapi import Depends, HTTPException, Header
from app.utils.auth import decode_token


def get_current_user(authorization: str = Header(...)) -> dict:
    """
    Dependency function to extract and validate the current user from a Bearer JWT token.

    Args:
        authorization (str): The Authorization header (expected format: Bearer <token>).

    Returns:
        dict: Decoded token payload representing the user.

    Raises:
        HTTPException: If the token is missing, invalid, or expired.
    """
    scheme, _, token = authorization.partition(" ")

    if scheme.lower() != "bearer" or not token:
        raise HTTPException(status_code=401, detail="Invalid authorization schema")

    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return payload

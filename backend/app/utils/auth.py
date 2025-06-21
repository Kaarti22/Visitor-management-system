"""
auth.py — Utility functions for handling authentication in the Visitor Management System.

Includes:
- Password hashing/verification (bcrypt)
- JWT access token creation and decoding
"""

from passlib.context import CryptContext
from jose import JWTError, jwt
import os
from datetime import datetime, timedelta

# ------------------------
# Configuration Constants
# ------------------------

# Fallback secret key for development if not set in environment
SECRET_KEY = os.getenv("JWT_SECRET", "secret-key")
ALGORITHM = "HS256"

# Default token expiration (30 minutes)
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ------------------------
# Password Utilities
# ------------------------

def hash_password(password: str) -> str:
    """
    Hashes a plain password using bcrypt.

    Args:
        password (str): Raw password string.

    Returns:
        str: Secure hashed password.
    """
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    """
    Verifies if a plain password matches its hash.

    Args:
        plain (str): Raw password string.
        hashed (str): Hashed password from DB.

    Returns:
        bool: True if match, else False.
    """
    return pwd_context.verify(plain, hashed)


# ------------------------
# JWT Token Utilities
# ------------------------

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Creates a signed JWT access token.

    Args:
        data (dict): Payload data to encode.
        expires_delta (timedelta, optional): Expiry duration.

    Returns:
        str: Encoded JWT token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict | None:
    """
    Decodes a JWT token and returns its payload.

    Args:
        token (str): Encoded JWT token.

    Returns:
        dict | None: Payload if valid, else None (invalid/expired).
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None  # You can optionally log the failure here

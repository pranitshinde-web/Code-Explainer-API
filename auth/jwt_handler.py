# auth/jwt_handler.py

import time
from typing import Literal, Dict

import jwt
from fastapi import HTTPException, status

from config import settings
from utils.logger import log_error

SECRET = settings.JWT_SECRET
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRY = 15 * 60          # 15 minutes
REFRESH_TOKEN_EXPIRY = 7 * 24 * 3600   # 7 days


def _create_token(username: str, expires_in: int, token_type: Literal["access", "refresh"]) -> str:
    now = int(time.time())
    payload = {
        "sub": username,
        "type": token_type,
        "iat": now,
        "exp": now + expires_in,
    }
    try:
        return jwt.encode(payload, SECRET, algorithm=ALGORITHM)
    except Exception as e:
        log_error(f"JWT creation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create JWT token"
        )


def create_access_token(username: str) -> str:
    return _create_token(username, ACCESS_TOKEN_EXPIRY, "access")


def create_refresh_token(username: str) -> str:
    return _create_token(username, REFRESH_TOKEN_EXPIRY, "refresh")


def verify_access_token(token: str) -> Dict:
    """
    Verifies JWT access token and returns decoded payload.
    """
    try:
        decoded = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        if decoded.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
            )
        return decoded

    except jwt.ExpiredSignatureError:
        log_error("JWT Error: Access token expired")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token expired"
        )
    except jwt.InvalidTokenError:
        log_error("JWT Error: Invalid access token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token"
        )


def verify_refresh_token(token: str) -> Dict:
    """
    Verifies JWT refresh token and returns decoded payload.
    """
    try:
        decoded = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        if decoded.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token type",
            )
        return decoded

    except jwt.ExpiredSignatureError:
        log_error("JWT Error: Refresh token expired")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired"
        )
    except jwt.InvalidTokenError:
        log_error("JWT Error: Invalid refresh token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

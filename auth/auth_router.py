# auth/auth_router.py
import datetime
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from fastapi import Depends
from auth.jwt_handler import (
    create_access_token,
    create_refresh_token,
    verify_access_token,
    verify_refresh_token,
)
from auth.user_store import (
    create_user,
    get_user,
    verify_password,
    save_refresh_token,
    get_refresh_token,
    delete_refresh_token,
    delete_user_refresh_tokens,
)
from utils.logger import log_info

router = APIRouter(prefix="/auth", tags=["Auth"])


# ---------- Pydantic models ----------

class RegisterRequest(BaseModel):
    username: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


# ---------- Routes ----------

@router.post("/register", status_code=201)
async def register(payload: RegisterRequest):
    """
    Register a new user and store in JSON DB.
    """
    try:
        user = create_user(payload.username, payload.password)
        log_info(f"User registered: {user['username']}")
        return {"message": "User registered successfully"}
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest):
    """
    Authenticate user and return access + refresh tokens.
    """
    user = get_user(payload.username)

    if not user or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    access_token = create_access_token(payload.username)
    refresh_token = create_refresh_token(payload.username)

    # Persist refresh token in JSON DB
    import time
    expires_at = (
            datetime.datetime.utcnow() + datetime.timedelta(days=7)
        ).isoformat() + "Z"
    save_refresh_token(payload.username, refresh_token, expires_at)

    log_info(f"User logged in: {payload.username}")

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh(payload: RefreshRequest):
    """
    Exchange a valid refresh token for a new access token (and rotated refresh).
    """
    stored = get_refresh_token(payload.refresh_token)
    if not stored:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unknown or revoked refresh token",
        )

    # Verify JWT (signature + expiry + type)
    decoded = verify_refresh_token(payload.refresh_token)
    username = decoded.get("sub")

    # Optional: also check expiry stored in JSON DB
    import time
    now = int(time.time())
    if stored["expires_at"] < now:
        delete_refresh_token(payload.refresh_token)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired",
        )

    # Rotate refresh token: delete old and create new
    delete_refresh_token(payload.refresh_token)

    new_access_token = create_access_token(username)
    new_refresh_token = create_refresh_token(username)
    new_expires_at = now + 7 * 24 * 3600
    save_refresh_token(username, new_refresh_token, new_expires_at)

    log_info(f"Refresh token used for user: {username}")

    return TokenResponse(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
    )



@router.post("/logout")
async def logout(user=Depends(verify_access_token)):
    """
    Logs out the current user by deleting their refresh token(s).
    Access token will expire naturally.
    """
    username = user["sub"]

    delete_user_refresh_tokens(username)
    log_info(f"User logged out: {username}")

    return {"message": "Logged out successfully"}
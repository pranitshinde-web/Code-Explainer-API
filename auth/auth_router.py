# auth/auth_router.py

from fastapi import APIRouter, HTTPException
from auth.jwt_handler import create_access_token
from utils.logger import log_info

router = APIRouter(prefix="/auth", tags=["Auth"])

# Simple hardcoded user (replace with DB later)
FAKE_USER = {
    "username": "admin",
    "password": "1234"
}


@router.post("/login")
async def login(user: dict):
    """
    Authenticates a user and returns a JWT token.
    """

    username = user.get("username")
    password = user.get("password")

    if not username or not password:
        raise HTTPException(status_code=400, detail="Username & password required")

    if username != FAKE_USER["username"] or password != FAKE_USER["password"]:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(username)
    log_info(f"User logged in: {username}")

    return {"access_token": token, "token_type": "bearer"}

# auth/jwt_handler.py

import time
import jwt
from config import settings
from utils.logger import log_error

SECRET = settings.JWT_SECRET
ALGORITHM = "HS256"
TOKEN_EXPIRY = 3600  # 1 hour


def create_access_token(username: str) -> str:
    """
    Creates a JWT token for a given username.
    """
    try:
        payload = {
            "sub": username,
            "iat": int(time.time()),
            "exp": int(time.time()) + TOKEN_EXPIRY
        }

        token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)
        return token

    except Exception as e:
        log_error(f"JWT creation error: {str(e)}")
        raise RuntimeError("Failed to create JWT token")


def verify_access_token(token: str) -> dict:
    """
    Verifies JWT and returns decoded payload.
    """
    try:
        decoded = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        return decoded

    except jwt.ExpiredSignatureError:
        log_error("JWT Error: Token expired")
        raise RuntimeError("Token expired")

    except jwt.InvalidTokenError:
        log_error("JWT Error: Invalid token")
        raise RuntimeError("Invalid token")

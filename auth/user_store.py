# auth/user_store.py

import json
import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List

from passlib.context import CryptContext

DB_PATH = Path("data/users.json")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _load_db() -> Dict[str, Any]:
    if not DB_PATH.exists():
        data = {"users": [], "refresh_tokens": []}
        _save_db(data)
        return data

    with open(DB_PATH, "r") as f:
        return json.load(f)


def _save_db(data: Dict[str, Any]) -> None:
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=2)


# ---------- Password helpers ----------

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# ---------- User helpers ----------

def get_user(username: str) -> Optional[Dict[str, Any]]:
    db = _load_db()
    for user in db["users"]:
        if user["username"] == username:
            return user
    return None


def create_user(username: str, password: str) -> Dict[str, Any]:
    db = _load_db()

    if any(u["username"] == username for u in db["users"]):
        raise ValueError("User already exists")

    user = {
        "username": username,
        "password_hash": hash_password(password),
        "created_at": datetime.datetime.utcnow().isoformat() + "Z"
    }

    db["users"].append(user)
    _save_db(db)
    return user


# ---------- Refresh token helpers ----------

def save_refresh_token(username: str, token: str, expires_at: int) -> None:
    db = _load_db()

    # Optional: remove old tokens for this user (single active refresh token)
    db["refresh_tokens"] = [
        rt for rt in db["refresh_tokens"] if rt["username"] != username
    ]

    db["refresh_tokens"].append(
        {"username": username, "token": token, "expires_at": expires_at}
    )
    _save_db(db)


def get_refresh_token(token: str) -> Optional[Dict[str, Any]]:
    db = _load_db()
    for rt in db["refresh_tokens"]:
        if rt["token"] == token:
            return rt
    return None


def delete_refresh_token(token: str) -> None:
    db = _load_db()
    db["refresh_tokens"] = [rt for rt in db["refresh_tokens"] if rt["token"] != token]
    _save_db(db)

def delete_user_refresh_tokens(username: str):
    db = _load_db()
    db["refresh_tokens"] = [
        rt for rt in db["refresh_tokens"] if rt["username"] != username
    ]
    _save_db(db)

"""
auth - user registration and login
"""
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash
from api.models.db import get_connection

class AuthService:
    @staticmethod
    def register(username: str, password: str) -> int:
        """ new user record, returns new user.id """
        hashed = generate_password_hash(password)
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO users (username, password) VALUES (%s, %s)",
                    (username, hashed),
                )
                conn.commit()
                return cur.lastrowid

    @staticmethod
    def login(username: str, password: str) -> Optional[int]:
        """ verify, returns user.id if password matches, else None """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, password FROM users WHERE username = %s", (username,))
                rows = cur.fetchall()
                if not rows:
                    return None
                user_id, stored_hash = rows[0]["id"], rows[0]["password"]
                if check_password_hash(stored_hash, password):
                    return user_id
                return None

    @staticmethod
    def logout(user_id: int) -> None:
        """ cleanup on logout """
        pass
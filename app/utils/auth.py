import os
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Request

SECRET = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"


def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)


def get_token_from_header(request: Request):
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid auth header")
    return auth.split(" ")[1]


def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        return payload  # Or return user from DB
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

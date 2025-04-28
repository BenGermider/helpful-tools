import os
from datetime import datetime, timedelta

import jwt
from fastapi import (
    status,
    HTTPException
)
from fastapi.security import (
    OAuth2PasswordBearer
)

from app.security.config import ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise RuntimeError("Missing key as environment variable, terminating...")

async def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Receives data of user and makes a JWT of it
    :param data: user's data
    :param expires_delta: time for token
    :return: JWT
    """

    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def verify_token(token: str) -> str:
    """
    Pulls username from a verified JWT
    :param token: suspected as jwt
    :return: username if token is jwt.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return username
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
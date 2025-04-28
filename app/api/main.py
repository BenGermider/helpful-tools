from datetime import timedelta

from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.security.authenticator import (
    create_access_token,
    verify_token, oauth2_scheme
)
from app.security.config import ACCESS_TOKEN_EXPIRE_MINUTES

app = FastAPI()

current_fake_db = {
    "ben": {
        "username": "ben",
        "password": "123"
    }
}


@app.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = current_fake_db.get(form_data.username, None)
    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail='Incorrect username or password')

    token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"sub": user["username"]},
        expires_delta=token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@app.get('/protected')
async def protected(token: str = Depends(oauth2_scheme)):
    username = await verify_token(token)
    return {"message": f"Welcome to the Command Base, {username}"}


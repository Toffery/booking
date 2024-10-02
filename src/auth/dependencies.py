from fastapi import Depends, HTTPException, Query, Request
from pydantic import BaseModel

from typing import Annotated

from src.auth.service import AuthService


def get_token(request: Request):
    token = request.cookies.get("access_token", None)
    if token is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return token


def get_current_user_id(token: str = Depends(get_token)):
    data = AuthService().decode_access_token(token)
    return data.get("user_id")


GetUserIdDep = Annotated[int, Depends(get_current_user_id)]

from fastapi import Depends, HTTPException, Request

from typing import Annotated

from src.exceptions import TokenHasExpiredException, InvalidTokenException
from src.httpexceptions import InvalidTokenHTTPException, TokenHasExpiredHTTPException
from src.services.auth import AuthService


def get_token(request: Request):
    token = request.cookies.get("access_token", None)
    if token is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return token


def get_current_user_id(token: str = Depends(get_token)):
    try:
        data = AuthService().decode_access_token(token)
    except TokenHasExpiredException:
        raise TokenHasExpiredHTTPException
    except InvalidTokenException:
        raise InvalidTokenHTTPException
    return data.get("user_id")


def get_current_admin_id(token: str = Depends(get_token)):
    try:
        data = AuthService().decode_access_token(token)
    except TokenHasExpiredException:
        raise TokenHasExpiredHTTPException
    except InvalidTokenException:
        raise InvalidTokenHTTPException
    if not data.get("is_admin"):
        raise HTTPException(status_code=403, detail="Forbidden")
    return data.get("user_id")


def get_current_superuser_id(token: str = Depends(get_token)):
    try:
        data = AuthService().decode_access_token(token)
    except TokenHasExpiredException:
        raise TokenHasExpiredHTTPException
    except InvalidTokenException:
        raise InvalidTokenHTTPException
    if not data.get("is_superuser"):
        raise HTTPException(status_code=403, detail="Forbidden")
    return data.get("user_id")


GetUserIdDep = Annotated[int, Depends(get_current_user_id)]
GetSuperuserIdDep = Annotated[int, Depends(get_current_superuser_id)]
GetAdminIdDep = Annotated[int, Depends(get_current_admin_id)]

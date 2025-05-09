from fastapi import APIRouter, Response

from src.httpexceptions import (
    UserAlreadyExistHTTPException,
    IncorrectPasswordHTTPException,
    UserNotFoundHTTPException,
    InvalidTokenHTTPException,
    TokenHasExpiredHTTPException,
)
from src.services.auth import AuthService
from src.auth.dependencies import GetUserIdDep
from src.dependencies import DBDep
from src.exceptions import (
    UserNotFoundException,
    UserAlreadyExistsException,
    IncorrectPasswordException,
    TokenHasExpiredException,
    InvalidTokenException,
)
from src.users.schemas import UserIn
from src.config import settings


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup")
async def sign_up(user_data: UserIn, db: DBDep):
    try:
        await AuthService(db).sign_up(user_data)
        return {"message": "User successfully created"}
    except UserAlreadyExistsException:
        raise UserAlreadyExistHTTPException


@router.post("/login")
async def login(user_data: UserIn, response: Response, db: DBDep):
    try:
        access_token = await AuthService(db).login(user_data)
        response.set_cookie(
            key="access_token", value=access_token, httponly=True, secure=settings.is_production
        )
        return {"access_token": access_token, "token_type": "cookie", "message": "HELLO"}
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException
    except UserNotFoundException:
        raise UserNotFoundHTTPException


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")

    return {"message": "You successfully logged out"}


@router.get("/me", summary="Получить текущего аутентифицированного пользователя")
async def get_me(user_id: GetUserIdDep, db: DBDep):
    """
    Ручка для получения текущего аутентифицированного пользователя.

    Проверка на аутентификацию производится через jwt токен.
    """
    try:
        user = await AuthService(db).get_me(user_id)
        return {
            "message": f"Hello, {user.username or user.email}! Welcome back!",
            "data": user,
        }
    except UserNotFoundException:
        raise UserNotFoundHTTPException
    except TokenHasExpiredException:
        raise TokenHasExpiredHTTPException
    except InvalidTokenException:
        raise InvalidTokenHTTPException

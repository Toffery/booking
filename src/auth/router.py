import datetime
from fastapi import APIRouter, Response
from sqlalchemy.exc import IntegrityError

from src.auth.service import AuthService
from src.auth.dependencies import GetUserIdDep
from src.dependencies import DBDep
from src.users.schemas import UserIn, UserCreate, UserInDB, UserOut


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup")
async def sign_up(
        user_data: UserIn,
        db: DBDep
):
    hashed_password = AuthService().get_password_hash(user_data.password)
    new_user = UserCreate(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password
    )

    try:
        await db.auth.add(new_user)
    except IntegrityError:
        return {
            "message": "User with this email or username already exist"
        }
    await db.commit()

    return {
        "message": "User successfully created"
    }


@router.post("/login")
async def login(
        user_data: UserIn,
        response: Response,
        db: DBDep
):
    user: UserInDB = await db.auth.get_user_in_db(
        email=user_data.email,
        username=user_data.username
    )

    if user is None:
        return {"message": "User with this email doesn't exist"}

    if not AuthService().verify_password(user_data.password, user.hashed_password):
        return {
            "message": "Incorrect password"
        }

    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True
    )

    return {
        "access_token": access_token,
        "token_type": "cookie"
    }


@router.post("/logout")
async def logout(
        response: Response
):
    response.delete_cookie(key="access_token")

    return {
        "message": "You successfully logged out"
    }


@router.get(
        "/me",
        summary="Получить текущего аутентифицированного пользователя"
)
async def get_me(
        user_id: GetUserIdDep,
        db: DBDep
):
    """
    Ручка для получения текущего аутентифицированного пользователя.
    
    Проверка на аутентификацию производится через jwt токен.
    """
    user = await db.auth.get_one_or_none(id=user_id)
    if user is None:
        return {
            "message": "User not found"
        }
    
    user_out: UserOut = UserOut(
        **user.model_dump(
            exclude=[
                "hashed_password"
            ]
        )
    )
    return {
        "message": f"Hello, {user_out.username or user_out.email}! Welcome back!",
        "data": user_out
    }

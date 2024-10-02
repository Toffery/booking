from fastapi import APIRouter, Request, Response
from sqlalchemy.exc import IntegrityError

from src.auth.dependencies import GetUserIdDep
from src.auth.schemas import UserIn, UserCreate, UserInDB
from database import async_session_maker

from src.repositories.auth import AuthRepository
from src.auth.service import AuthService

router= APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup")
async def sign_up(user_data: UserIn):
    hashed_password = AuthService().get_password_hash(user_data.password)
    new_user = UserCreate(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password
    )
    async with async_session_maker() as session:
        try:
            await AuthRepository(session=session).add(
                data=new_user
            )
        except IntegrityError:
            return {
                "message": "User with this email or username already exist"
            }
        await session.commit()

    return {
        "message": "User successfully created"
    }


@router.post("/login")
async def login(
    user_data: UserIn,
    response: Response
):
    async with async_session_maker() as session:
        user: UserInDB = await AuthRepository(session=session).get_user_in_db(
            email=user_data.email
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
    user_id: GetUserIdDep
):
    """
    Ручка для получения текущего аутентифицированного пользователя.
    
    Проверка на аутентификацию производится через jwt токен.
    """
    async with async_session_maker() as session:
        user = await AuthRepository(session=session).get_one_or_none(
            id=user_id
        )
    if user is None:
        return {
            "message": "User not found"
        }
    return {"message": f"Hello, {user.username or user.email}! Welcome back!"}

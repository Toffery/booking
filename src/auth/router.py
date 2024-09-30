from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Response
from sqlalchemy.exc import IntegrityError

from src.auth.schemas import UserIn, UserCreate
from database import async_session_maker

from passlib.context import CryptContext
import jwt 

from repositories.auth import AuthRepository

import jwt
from src.repositories.auth import AuthRepository
from src.config import auth_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "c7c3a5944c21320762a0755f302d81362ee773ad016fc7287451d88a40b0443d"
ALGHORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router= APIRouter(prefix="/auth", tags=["Auth"])
SECRET_KEY = auth_settings.JWT_SECRET
ALGORITHM = auth_settings.JWT_ALG
ACCESS_TOKEN_EXPIRE_MINUTES = auth_settings.JWT_EXP
REFRESH_TOKEN_EXPIRE_MINUTES = auth_settings.REFRESH_TOKEN_EXP


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: int | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGHORITHM)
    return encoded_jwt

@router.post("/signup")
async def sign_up(user_data: UserIn):
    hashed_password = get_password_hash(user_data.password)
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
            return {"message": "User with this email or username already exist"}
        await session.commit()
    return {"message": "User successfully created"}


@router.post("/login")
async def login(
    user_data: UserIn,
    response: Response
):
    async with async_session_maker() as session:
        user: UserInDB = await AuthRepository(session=session).get_one_or_none(
            email=user_data.email
        )
        if user is None:
            return {"message": "User with this email doesn't exist"}
        if not verify_password(user_data.password, user.hashed_password):
            return {"message": "Incorrect password"}
        access_token = create_access_token({"user_id": user.id})
        response.set_cookie(key="access_token", value=access_token, httponly=True)
        return {"access_token": access_token, "token_type": "bearer"}

from fastapi import APIRouter

from auth.schemas import UserIn, UserCreate
from database import async_session_maker

from passlib.context import CryptContext

from repositories.auth import AuthRepository


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router= APIRouter(prefix="/auth", tags=["Auth"])

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

@router.post("/")
async def register(user: UserIn):
    print(user)
    hashed_password = get_password_hash(user.password)
    new_user = UserCreate(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    async with async_session_maker() as session:
        ret_user = await AuthRepository(session=session).add(
            data=new_user
        )
        await session.commit()
    return ret_user

from datetime import datetime, timezone, timedelta
import jwt
from passlib.context import CryptContext

from src.services.base import BaseService
from src.users.schemas import UserIn, UserCreate, UserInDB, UserOut
from src.auth.config import auth_settings
from src.exceptions import TokenHasExpiredException, InvalidTokenException, ObjectAlreadyExistsException, \
    UserAlreadyExistsException, IncorrectPasswordException, ObjectNotFoundException, UserNotFoundException

SECRET_KEY = auth_settings.JWT_SECRET
ALGORITHM = auth_settings.JWT_ALG
ACCESS_TOKEN_EXPIRE_MINUTES = auth_settings.JWT_EXP
REFRESH_TOKEN_EXPIRE_MINUTES = auth_settings.REFRESH_TOKEN_EXP


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        return encoded_jwt

    @staticmethod
    def decode_access_token(token: str) -> dict[str, str]:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise TokenHasExpiredException
        except jwt.InvalidTokenError:
            raise InvalidTokenException

    async def sign_up(self, user_data: UserIn):
        hashed_password = self.get_password_hash(user_data.password)
        new_user = UserCreate(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password
        )
        try:
            await self.db.auth.add(new_user)
            await self.db.commit()
        except ObjectAlreadyExistsException:
            raise UserAlreadyExistsException

    async def login(self, user_data: UserIn):
        user: UserInDB = await self.db.auth.get_user_in_db(
            email=user_data.email, username=user_data.username
        )

        if not self.verify_password(user_data.password, user.hashed_password):
            raise IncorrectPasswordException

        access_token = self.create_access_token({"user_id": user.id})

        return access_token


    async def get_me(self, user_id: int):
        try:
            user = await self.db.auth.get_one(id=user_id)
            user_out: UserOut = UserOut(**user.model_dump(exclude=["hashed_password"]))
            return user_out
        except ObjectNotFoundException:
            raise UserNotFoundException

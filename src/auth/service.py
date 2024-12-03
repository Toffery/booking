from datetime import datetime, timezone, timedelta

from fastapi import HTTPException
from src.auth.config import auth_settings

import jwt
from passlib.context import CryptContext


SECRET_KEY = auth_settings.JWT_SECRET
ALGORITHM = auth_settings.JWT_ALG
ACCESS_TOKEN_EXPIRE_MINUTES = auth_settings.JWT_EXP
REFRESH_TOKEN_EXPIRE_MINUTES = auth_settings.REFRESH_TOKEN_EXP


class AuthService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    @staticmethod
    def create_access_token(
            data: dict, 
            expires_delta: timedelta | None = None
    ) -> str:
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
            raise HTTPException(
                status_code=401, 
                detail="Token has been expired"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=401, 
                detail="Invalid token"
            )

import datetime
from pydantic import BaseModel, ConfigDict, EmailStr


class UserIn(BaseModel):
    email: EmailStr | None = None
    password: str
    username: str | None = None

    def __repr__(self):
        return f"User(email={self.email}, username={self.username})"


class UserCreate(BaseModel):
    email: EmailStr | None = None
    hashed_password: str
    username: str | None = None


class UserBase(BaseModel):
    id: int
    email: EmailStr | None = None
    username: str | None = None


class UserOut(UserBase):
    first_name: str | None = None
    last_name: str | None = None
    patronymic: str | None = None

    created_at: datetime.datetime
    updated_at: datetime.datetime

    is_admin: bool | None = None
    is_superuser: bool | None = None


class UserInDB(UserOut):
    hashed_password: str

    model_config = ConfigDict(from_attributes=True)

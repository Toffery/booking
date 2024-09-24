from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserIn(BaseModel):
    email: EmailStr
    password: str


class UserSchema(BaseModel):
    email: EmailStr
    hashed_password: str
    username: str | None = None


class UserInDB(BaseModel):
    id: int
    email: EmailStr
    username: str | None = None

    model_config = ConfigDict(from_attributes=True)

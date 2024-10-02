from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserIn(BaseModel):
    email: EmailStr
    password: str
    username: str | None = None

    def __repr__(self):
        return f"User(email={self.email}, username={self.username})"


class UserCreate(BaseModel):
    email: EmailStr
    hashed_password: str
    username: str | None = None


class UserSchema(BaseModel):
    id: int
    email: EmailStr
    username: str | None = None
    model_config = ConfigDict(from_attributes=True)


class UserInDB(UserSchema):
    hashed_password: str
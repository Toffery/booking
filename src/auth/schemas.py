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


class UserInDB(UserCreate):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

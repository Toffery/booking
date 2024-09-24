from sqlalchemy import String
from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    username: Mapped[str | None] = mapped_column(String(100), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(200))

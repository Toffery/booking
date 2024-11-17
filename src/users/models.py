import datetime
from sqlalchemy import String, func, Boolean
from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    username: Mapped[str | None] = mapped_column(String(100), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(200))

    first_name: Mapped[str | None] = mapped_column(String(30))
    last_name: Mapped[str | None] = mapped_column(String(50))
    patronymic: Mapped[str | None] = mapped_column(String(50))

    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    is_admin: Mapped[bool | None] = mapped_column(Boolean, default=False)
    is_superuser: Mapped[bool | None] = mapped_column(Boolean, default=False)

    @hybrid_property
    def full_name(self):
        return f"{self.first_name} {self.last_name} {self.patronymic}"

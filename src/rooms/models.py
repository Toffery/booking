import typing

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from src.database import Base

if typing.TYPE_CHECKING:
    from src.facilities.models import Facility


class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(String(1000))
    price: Mapped[int]
    quantity: Mapped[int]
    facilities: Mapped[list["Facility"]] = relationship(
        back_populates="rooms",
        secondary="rooms_facilities",
    )

"""added ondelete cascade for RoomFacility table

Revision ID: ccd75d6ac5aa
Revises: c9c99c60eaa6
Create Date: 2024-12-17 16:34:59.472196

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "ccd75d6ac5aa"
down_revision: Union[str, None] = "c9c99c60eaa6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(
        "rooms_facilities_facility_id_fkey",
        "rooms_facilities",
        type_="foreignkey",
    )
    op.drop_constraint(
        "rooms_facilities_room_id_fkey", "rooms_facilities", type_="foreignkey"
    )
    op.create_foreign_key(
        None,
        "rooms_facilities",
        "rooms",
        ["room_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        None,
        "rooms_facilities",
        "facilities",
        ["facility_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint(None, "rooms_facilities", type_="foreignkey")
    op.drop_constraint(None, "rooms_facilities", type_="foreignkey")
    op.create_foreign_key(
        "rooms_facilities_room_id_fkey",
        "rooms_facilities",
        "rooms",
        ["room_id"],
        ["id"],
    )
    op.create_foreign_key(
        "rooms_facilities_facility_id_fkey",
        "rooms_facilities",
        "facilities",
        ["facility_id"],
        ["id"],
    )

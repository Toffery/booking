"""Added new fields to users table

Revision ID: 6a0468f913ed
Revises: 103b1386d1d5
Create Date: 2024-10-21 20:12:40.772637

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6a0468f913ed"
down_revision: Union[str, None] = "103b1386d1d5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users", sa.Column("first_name", sa.String(length=30), nullable=True)
    )
    op.add_column(
        "users", sa.Column("last_name", sa.String(length=50), nullable=True)
    )
    op.add_column(
        "users", sa.Column("patronymic", sa.String(length=50), nullable=True)
    )
    op.add_column(
        "users",
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.add_column(
        "users",
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.add_column("users", sa.Column("is_admin", sa.Boolean(), nullable=True))
    op.add_column(
        "users", sa.Column("is_superuser", sa.Boolean(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("users", "is_superuser")
    op.drop_column("users", "is_admin")
    op.drop_column("users", "updated_at")
    op.drop_column("users", "created_at")
    op.drop_column("users", "patronymic")
    op.drop_column("users", "last_name")
    op.drop_column("users", "first_name")

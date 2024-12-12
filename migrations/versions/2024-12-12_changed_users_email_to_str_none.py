"""changed users email to str | None

Revision ID: c9c99c60eaa6
Revises: e7e48991309b
Create Date: 2024-12-12 15:39:28.568514

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c9c99c60eaa6"
down_revision: Union[str, None] = "e7e48991309b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "users", "email", existing_type=sa.VARCHAR(length=100), nullable=True
    )


def downgrade() -> None:
    op.alter_column(
        "users", "email", existing_type=sa.VARCHAR(length=100), nullable=False
    )

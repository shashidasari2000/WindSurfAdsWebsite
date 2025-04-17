"""Add icon_class to Category

Revision ID: 4896a3fc8e64
Revises: ae1027a6acf
Create Date: 2025-04-17 12:40:20.668611

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4896a3fc8e64'
down_revision: Union[str, None] = 'ae1027a6acf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

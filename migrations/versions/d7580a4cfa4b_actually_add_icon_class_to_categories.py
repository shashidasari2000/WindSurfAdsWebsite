"""Actually add icon_class to categories

Revision ID: d7580a4cfa4b
Revises: 4896a3fc8e64
Create Date: 2025-04-17 12:45:56.985667

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd7580a4cfa4b'
down_revision: Union[str, None] = '4896a3fc8e64'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('categories', sa.Column('icon_class', sa.String(length=100), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('categories', 'icon_class')

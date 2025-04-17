"""Add is_withdraw to job_applications

Revision ID: 6c4f8efb0a61
Revises: 9a952e088ab1
Create Date: 2025-04-17 14:09:44.100633

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6c4f8efb0a61'
down_revision: Union[str, None] = '9a952e088ab1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

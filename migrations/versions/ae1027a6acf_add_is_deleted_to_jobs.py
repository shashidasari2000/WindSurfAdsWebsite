revision = 'ae1027a6acf'
down_revision = 'manual_add_role_column'
branch_labels = None
depends_on = None

"""add is_deleted to jobs"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('jobs', sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default=sa.false()))


def downgrade():
    op.drop_column('jobs', 'is_deleted')

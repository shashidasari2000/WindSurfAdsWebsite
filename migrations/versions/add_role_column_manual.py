"""manual add role column to users table

Revision ID: manual_add_role_column
Revises: 9a7839d62411
Create Date: 2025-04-17

"""
revision = 'manual_add_role_column'
down_revision = '9a7839d62411'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('users', sa.Column('role', sa.String(length=20), nullable=False, server_default='viewer'))

def downgrade():
    op.drop_column('users', 'role')

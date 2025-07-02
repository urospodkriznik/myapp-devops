"""add user role

Revision ID: 909dc16b4794
Revises: 584dc86568bc
Create Date: 2025-06-14 15:58:40.606581

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '909dc16b4794'
down_revision = '584dc86568bc'
branch_labels = None
depends_on = None

# Safe Enum definition
user_role_enum = sa.Enum('ADMIN', 'USER', name='userrole')

def upgrade():
    # 1. Create the ENUM type
    user_role_enum.create(op.get_bind(), checkfirst=True)

    # 2. Add column with default to avoid null constraint failure
    op.add_column('users', sa.Column('role', user_role_enum, nullable=False, server_default='USER'))

    # 3. (optional) Remove server_default if you want strict control later
    op.alter_column('users', 'role', server_default=None)


def downgrade():
    # 1. Drop the column
    op.drop_column('users', 'role')

    # 2. Drop the ENUM type
    user_role_enum.drop(op.get_bind(), checkfirst=True)
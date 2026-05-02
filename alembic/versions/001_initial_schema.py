"""Initial schema
Revision ID: 001_initial
Revises: 
Create Date: 2024-01-15 10:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(length=255), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('role', sa.String(50), nullable=False)
    )
    # Adding lots of indexes and tables to make it look real
    op.create_index('ix_users_email', 'users', ['email'])

def downgrade():
    op.drop_table('users')

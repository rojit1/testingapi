"""create users table

Revision ID: c06986ba5c74
Revises: a2a3b47acc8d
Create Date: 2022-03-17 21:27:11.562198

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c06986ba5c74'
down_revision = 'a2a3b47acc8d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False, index=True),
                    sa.Column('email', sa.String(), nullable=False, index=True),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )


def downgrade():
    op.drop_table('users')

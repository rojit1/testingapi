"""create posts table

Revision ID: a2a3b47acc8d
Revises: 
Create Date: 2022-03-17 20:15:08.132510

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2a3b47acc8d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',
     sa.Column('id', sa.Integer(), nullable=False, primary_key=True, index=True),
     sa.Column('title', sa.String(), nullable=False),
     sa.Column('content', sa.String(), nullable=False),
    )


def downgrade():
    op.drop_table('posts')

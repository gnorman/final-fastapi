"""add content column to posts table

Revision ID: 97055c937bd7
Revises: 816982baa77c
Create Date: 2023-11-22 05:44:40.380272

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '97055c937bd7'
down_revision: Union[str, None] = '816982baa77c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass

"""add content column to posts table

Revision ID: c60db0eeff1e
Revises: ddc8dbcb395e
Create Date: 2023-11-29 20:21:20.254902

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c60db0eeff1e'
down_revision: Union[str, None] = 'ddc8dbcb395e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass

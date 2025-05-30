"""Add remind inactive column for users

Revision ID: 95d8ff98b480
Revises: ccbbac126633
Create Date: 2025-05-18 21:04:19.117407

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '95d8ff98b480'
down_revision: Union[str, None] = 'ccbbac126633'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('remind_inactive', sa.Boolean(), server_default='1', nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'remind_inactive')
    # ### end Alembic commands ###

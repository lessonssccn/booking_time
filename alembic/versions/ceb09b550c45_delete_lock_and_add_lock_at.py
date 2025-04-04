"""delete lock and add lock_at

Revision ID: ceb09b550c45
Revises: 15de5c98a554
Create Date: 2025-02-27 19:55:04.830281

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ceb09b550c45'
down_revision: Union[str, None] = '15de5c98a554'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('lock_at', sa.DateTime(), nullable=True))
    op.drop_column('users', 'lock')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('lock', sa.INTEGER(), nullable=False))
    op.drop_column('users', 'lock_at')
    # ### end Alembic commands ###

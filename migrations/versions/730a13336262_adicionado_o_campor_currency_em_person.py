"""Adicionado o campor currency em person

Revision ID: 730a13336262
Revises: 41523ee7e23e
Create Date: 2024-04-13 16:58:14.502991

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '730a13336262'
down_revision: Union[str, None] = '41523ee7e23e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('person', sa.Column('currency', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('person', 'currency')
    # ### end Alembic commands ###
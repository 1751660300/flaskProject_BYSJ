"""empty message

Revision ID: b5ed5c4a50c4
Revises: aad0971360cb
Create Date: 2021-02-15 20:48:08.804875

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b5ed5c4a50c4'
down_revision = 'aad0971360cb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('menu', 'isuse')
    op.add_column('menutem', sa.Column('isuse', sa.CHAR(length=1), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('menutem', 'isuse')
    op.add_column('menu', sa.Column('isuse', mysql.CHAR(length=1), nullable=False))
    # ### end Alembic commands ###

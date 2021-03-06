"""empty message

Revision ID: 9ce30f17f52a
Revises: b5ed5c4a50c4
Create Date: 2021-02-20 17:21:46.280841

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ce30f17f52a'
down_revision = 'b5ed5c4a50c4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('free', sa.Column('comment', sa.VARCHAR(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('free', 'comment')
    # ### end Alembic commands ###

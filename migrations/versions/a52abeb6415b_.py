"""empty message

Revision ID: a52abeb6415b
Revises: 
Create Date: 2021-02-10 14:18:40.044713

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a52abeb6415b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('age', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('phone', sa.VARCHAR(length=11), nullable=True))
    op.add_column('users', sa.Column('sex', sa.CHAR(length=1), nullable=True))
    op.alter_column('users', 'username',
               existing_type=mysql.VARCHAR(length=64),
               nullable=True)
    op.drop_index('password', table_name='users')
    op.drop_index('username', table_name='users')
    op.drop_column('users', 'password')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password', mysql.VARCHAR(length=64), nullable=False))
    op.create_index('username', 'users', ['username'], unique=True)
    op.create_index('password', 'users', ['password'], unique=True)
    op.alter_column('users', 'username',
               existing_type=mysql.VARCHAR(length=64),
               nullable=False)
    op.drop_column('users', 'sex')
    op.drop_column('users', 'phone')
    op.drop_column('users', 'age')
    # ### end Alembic commands ###

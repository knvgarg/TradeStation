"""re

Revision ID: 16e115ee7814
Revises: 
Create Date: 2021-11-29 19:44:20.217431

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '16e115ee7814'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stock_daily_value',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sname', sa.String(length=64), nullable=True),
    sa.Column('date', sa.String(length=64), nullable=True),
    sa.Column('value', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('pasword_hash', sa.String(length=128), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(length=128), nullable=True),
    sa.Column('funds', sa.Float(), nullable=True),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('mode', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_table('stock_list',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('stockname', sa.String(length=64), nullable=True),
    sa.Column('curr_value', sa.Float(), nullable=True),
    sa.Column('no_of_stocks', sa.Integer(), nullable=True),
    sa.Column('invested', sa.Float(), nullable=True),
    sa.Column('userId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['userId'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('transactions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('amount', sa.Float(), nullable=True),
    sa.Column('type', sa.Integer(), nullable=True),
    sa.Column('stock', sa.String(length=64), nullable=True),
    sa.Column('date', sa.String(length=64), nullable=True),
    sa.Column('userId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['userId'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transactions')
    op.drop_table('stock_list')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('stock_daily_value')
    # ### end Alembic commands ###
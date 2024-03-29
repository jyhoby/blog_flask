"""empty message

Revision ID: e984177c85e4
Revises: 2543af6ee1ce
Create Date: 2019-06-28 16:37:22.836866

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e984177c85e4'
down_revision = '2543af6ee1ce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('loginlog',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=20), nullable=True),
    sa.Column('remote_ip', sa.String(length=30), nullable=True),
    sa.Column('logintime', sa.DateTime(), nullable=True),
    sa.Column('is_delete', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('loginlog')
    # ### end Alembic commands ###

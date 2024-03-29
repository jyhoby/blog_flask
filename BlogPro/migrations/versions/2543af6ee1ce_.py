"""empty message

Revision ID: 2543af6ee1ce
Revises: 6bf14dafad27
Create Date: 2019-06-26 19:47:31.911522

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2543af6ee1ce'
down_revision = '6bf14dafad27'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('blog', sa.Column('create_time', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('blog', 'create_time')
    # ### end Alembic commands ###

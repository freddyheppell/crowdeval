"""empty message

Revision ID: b4604a339ce5
Revises: e548cfba9560
Create Date: 2021-04-02 15:58:09.269017

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = 'b4604a339ce5'
down_revision = 'e548cfba9560'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ratings', sa.Column('created_at', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ratings', 'created_at')
    # ### end Alembic commands ###

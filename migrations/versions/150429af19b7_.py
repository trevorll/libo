"""empty message

Revision ID: 150429af19b7
Revises: d311eb4f8f18
Create Date: 2020-07-31 19:59:12.183119

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '150429af19b7'
down_revision = 'd311eb4f8f18'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('borrowed_books', sa.Column('id', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('borrowed_books', 'id')
    # ### end Alembic commands ###

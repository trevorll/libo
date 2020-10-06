"""empty message

Revision ID: c5a352bbb710
Revises: c8ab289ab371
Create Date: 2020-08-01 14:49:17.459646

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c5a352bbb710'
down_revision = 'c8ab289ab371'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('hostel',
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('hostel')
    # ### end Alembic commands ###
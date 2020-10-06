"""empty message

Revision ID: 8981480405b8
Revises: c5a352bbb710
Create Date: 2020-08-01 15:03:32.527582

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8981480405b8'
down_revision = 'c5a352bbb710'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('booked_hostel',
    sa.Column('bookeddate', sa.DateTime(), nullable=True),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('hostel', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['name'], ['fixed.name'], ),
    sa.PrimaryKeyConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('booked_hostel')
    # ### end Alembic commands ###
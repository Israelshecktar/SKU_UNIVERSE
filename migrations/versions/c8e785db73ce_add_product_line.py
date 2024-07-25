"""add product line

Revision ID: c8e785db73ce
Revises: 894cfba78697
Create Date: 2024-07-25 02:23:14.543772

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c8e785db73ce'
down_revision = '894cfba78697'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('skus', schema=None) as batch_op:
        batch_op.add_column(sa.Column('product_line', sa.String(length=255), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('skus', schema=None) as batch_op:
        batch_op.drop_column('product_line')

    # ### end Alembic commands ###

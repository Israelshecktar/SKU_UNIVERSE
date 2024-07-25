"""Initial migration

Revision ID: 894cfba78697
Revises: 846683180bf0
Create Date: 2024-07-25 01:50:23.601750

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '894cfba78697'
down_revision = '846683180bf0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('skus', schema=None) as batch_op:
        batch_op.drop_column('price')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('skus', schema=None) as batch_op:
        batch_op.add_column(sa.Column('price', mysql.DECIMAL(precision=10, scale=2), nullable=True))

    # ### end Alembic commands ###

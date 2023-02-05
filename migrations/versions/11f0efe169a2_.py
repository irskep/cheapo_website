"""empty message

Revision ID: 11f0efe169a2
Revises: 71cff8962617
Create Date: 2023-02-05 12:12:11.554266

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11f0efe169a2'
down_revision = '71cff8962617'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(), nullable=False))
        batch_op.add_column(sa.Column('pronouns', sa.String(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('pronouns')
        batch_op.drop_column('name')

    # ### end Alembic commands ###

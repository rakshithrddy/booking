"""empty message

Revision ID: dd7c035d8f93
Revises: fa1495678db3
Create Date: 2020-07-30 23:29:39.082768

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd7c035d8f93'
down_revision = 'fa1495678db3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('driver', sa.Column('cost_per_km', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('driver', 'cost_per_km')
    # ### end Alembic commands ###

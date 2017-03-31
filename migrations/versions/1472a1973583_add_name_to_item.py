"""add name to item

Revision ID: 1472a1973583
Revises: c839078ffe6e
Create Date: 2017-03-29 20:45:31.382062

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1472a1973583'
down_revision = 'c839078ffe6e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('mqtt_items', sa.Column('label', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('mqtt_items', 'label')
    # ### end Alembic commands ###

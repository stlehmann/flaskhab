"""add value types, save values to db

Revision ID: f5d707713ae0
Revises: 1472a1973583
Create Date: 2017-04-02 13:00:39.694083

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f5d707713ae0'
down_revision = '1472a1973583'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('mqtt_items', sa.Column('value_bool', sa.Boolean(), nullable=True))
    op.add_column('mqtt_items', sa.Column('value_float', sa.Float(), nullable=True))
    op.add_column('mqtt_items', sa.Column('value_int', sa.Integer(), nullable=True))
    op.add_column('mqtt_items', sa.Column('value_string', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('mqtt_items', 'value_string')
    op.drop_column('mqtt_items', 'value_int')
    op.drop_column('mqtt_items', 'value_float')
    op.drop_column('mqtt_items', 'value_bool')
    # ### end Alembic commands ###

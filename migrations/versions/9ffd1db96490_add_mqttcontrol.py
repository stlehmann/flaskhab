"""add MQTTControl

Revision ID: 9ffd1db96490
Revises: eef456f73654
Create Date: 2017-04-08 18:08:18.500726

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ffd1db96490'
down_revision = 'eef456f73654'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mqtt_controls',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('label', sa.String(), nullable=True),
    sa.Column('control_type', sa.Integer(), nullable=True),
    sa.Column('topic', sa.String(), nullable=True),
    sa.Column('message', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('mqtt_controls')
    # ### end Alembic commands ###

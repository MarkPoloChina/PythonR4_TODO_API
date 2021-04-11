"""'time'

Revision ID: 7a84fc1ec81e
Revises: 4f4342fa0d3d
Create Date: 2021-03-26 23:32:33.358039

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7a84fc1ec81e'
down_revision = '4f4342fa0d3d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('timestamp', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_task_timestamp'), 'task', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_task_timestamp'), table_name='task')
    op.drop_column('task', 'timestamp')
    # ### end Alembic commands ###
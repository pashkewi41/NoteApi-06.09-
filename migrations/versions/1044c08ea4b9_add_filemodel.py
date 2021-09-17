"""add FileModel

Revision ID: 1044c08ea4b9
Revises: 78f0650a599e
Create Date: 2021-09-17 06:56:45.298107

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1044c08ea4b9'
down_revision = '78f0650a599e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('file_model',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('url')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('file_model')
    # ### end Alembic commands ###
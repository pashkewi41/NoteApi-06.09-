"""archive

Revision ID: 78f0650a599e
Revises: 5ab0b491b1f4
Create Date: 2021-09-14 11:03:22.784366

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78f0650a599e'
down_revision = '5ab0b491b1f4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('note_model', sa.Column('archive', sa.Boolean(), server_default='false', nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('note_model', 'archive')
    # ### end Alembic commands ###
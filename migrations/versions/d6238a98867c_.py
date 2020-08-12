"""empty message

Revision ID: d6238a98867c
Revises: d92bb0315c7b
Create Date: 2020-08-08 20:12:25.155418

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd6238a98867c'
down_revision = 'd92bb0315c7b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('recipe', sa.Column('cover_image', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('recipe', 'cover_image')
    # ### end Alembic commands ###

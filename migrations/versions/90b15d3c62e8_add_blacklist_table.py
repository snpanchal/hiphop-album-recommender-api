"""add blacklist table

Revision ID: 90b15d3c62e8
Revises: 0e8ad39233c7
Create Date: 2021-01-23 22:29:29.859134

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90b15d3c62e8'
down_revision = '0e8ad39233c7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blacklist_tokens',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('token', sa.String(length=500), nullable=False),
    sa.Column('blacklisted_on', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('token')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('blacklist_tokens')
    # ### end Alembic commands ###

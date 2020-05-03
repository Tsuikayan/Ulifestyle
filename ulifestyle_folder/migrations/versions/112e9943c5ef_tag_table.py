"""tag table

Revision ID: 112e9943c5ef
Revises: 0b7f39331dd0
Create Date: 2020-05-03 18:24:24.278488

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '112e9943c5ef'
down_revision = '0b7f39331dd0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tag', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tag_tag'), 'tag', ['tag'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_tag_tag'), table_name='tag')
    op.drop_table('tag')
    # ### end Alembic commands ###

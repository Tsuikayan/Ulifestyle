"""video post table

Revision ID: f14d290e731a
Revises: c9ec9a8d72ed
Create Date: 2020-12-10 20:45:29.017040

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f14d290e731a'
down_revision = 'c9ec9a8d72ed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('beautyvideopost',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.Column('author', sa.String(length=30), nullable=True),
    sa.Column('body1', sa.String(length=100), nullable=True),
    sa.Column('video', sa.String(length=100), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['author'], ['author.username'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_beautyvideopost_timestamp'), 'beautyvideopost', ['timestamp'], unique=False)
    op.create_table('foodvideopost',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.Column('author', sa.String(length=30), nullable=True),
    sa.Column('body1', sa.String(length=100), nullable=True),
    sa.Column('video', sa.String(length=100), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['author'], ['author.username'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_foodvideopost_timestamp'), 'foodvideopost', ['timestamp'], unique=False)
    op.create_table('travelvideopost',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.Column('author', sa.String(length=30), nullable=True),
    sa.Column('body1', sa.String(length=100), nullable=True),
    sa.Column('video', sa.String(length=100), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['author'], ['author.username'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_travelvideopost_timestamp'), 'travelvideopost', ['timestamp'], unique=False)
    op.drop_column('contact', 'hyperlink')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contact', sa.Column('hyperlink', sa.VARCHAR(), nullable=True))
    op.drop_index(op.f('ix_travelvideopost_timestamp'), table_name='travelvideopost')
    op.drop_table('travelvideopost')
    op.drop_index(op.f('ix_foodvideopost_timestamp'), table_name='foodvideopost')
    op.drop_table('foodvideopost')
    op.drop_index(op.f('ix_beautyvideopost_timestamp'), table_name='beautyvideopost')
    op.drop_table('beautyvideopost')
    # ### end Alembic commands ###

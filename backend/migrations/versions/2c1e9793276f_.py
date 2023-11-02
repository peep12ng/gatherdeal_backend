"""empty message

Revision ID: 2c1e9793276f
Revises: 
Create Date: 2023-11-02 17:56:36.200364

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c1e9793276f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('hotdeal_model',
    sa.Column('id', sa.VARCHAR(length=30), nullable=False),
    sa.Column('title', sa.TEXT(), nullable=True),
    sa.Column('original_price', sa.DOUBLE(), nullable=True),
    sa.Column('price_to_krw', sa.DOUBLE(), nullable=True),
    sa.Column('currency_type', sa.VARCHAR(length=30), nullable=True),
    sa.Column('store_link', sa.TEXT(), nullable=True),
    sa.Column('source_link', sa.TEXT(), nullable=True),
    sa.Column('scrape_at', sa.DATETIME(), nullable=True),
    sa.Column('is_done', sa.BOOLEAN(), nullable=True),
    sa.Column('is_blind', sa.BOOLEAN(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('hotdeal_model')
    # ### end Alembic commands ###

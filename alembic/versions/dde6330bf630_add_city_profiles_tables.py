"""
add_city_profiles_tables

Revision ID: dde6330bf630
Revises: None
Create Date: 2026-01-20 09:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = 'dde6330bf630'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### Создаём таблицу city_profiles ###
    op.create_table('city_profiles',
        sa.Column('city_name', sa.String(length=100), nullable=False),
        sa.Column('country', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('image_url', sa.String(length=500), nullable=True),
        sa.Column('total_landmarks', sa.Integer(), server_default=sa.text('0'), nullable=False),
        sa.Column('total_reviews', sa.Integer(), server_default=sa.text('0'), nullable=False),
        sa.Column('total_discussions', sa.Integer(), server_default=sa.text('0'), nullable=False),
        sa.Column('average_rating', sa.Float(), server_default=sa.text('0.0'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True)),
        sa.PrimaryKeyConstraint('city_name')
    )
    
    op.create_index(op.f('ix_city_profiles_city_name'), 'city_profiles', ['city_name'])
    op.create_index('idx_city_country', 'city_profiles', ['country'])
    
    # ### Создаём таблицу city_category_stats ###
    op.create_table('city_category_stats',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('city_name', sa.String(length=100), nullable=False),
        sa.Column('category', sa.String(length=100), nullable=False),
        sa.Column('count', sa.Integer(), server_default=sa.text('0'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('city_name', 'category', name='unique_city_category')
    )
    
    op.create_index(op.f('ix_city_category_stats_city_name'), 'city_category_stats', ['city_name'])
    op.create_index(op.f('ix_city_category_stats_category'), 'city_category_stats', ['category'])
    op.create_index('idx_city_category_composite', 'city_category_stats', ['city_name', 'category'])


def downgrade():
    op.drop_table('city_category_stats')
    op.drop_table('city_profiles')
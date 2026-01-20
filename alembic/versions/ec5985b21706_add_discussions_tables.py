"""add_discussions_tables

Revision ID: [автоматически сгенерируется]
Revises: None
Create Date: [текущая дата]

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '[ID]'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### Создаём таблицу discussions ###
    op.create_table('discussions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('landmark_id', sa.Integer(), nullable=True),
        sa.Column('city', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True)),
        sa.Column('is_closed', sa.Boolean(), server_default=sa.text('false')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['landmark_id'], ['landmarks.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Создаём индексы для discussions
    op.create_index(op.f('ix_discussions_city'), 'discussions', ['city'])
    op.create_index('idx_discussion_city_created', 'discussions', ['city', 'created_at'])
    op.create_index('idx_discussion_landmark_created', 'discussions', ['landmark_id', 'created_at'])
    
    # ### Создаём таблицу discussion_answers ###
    op.create_table('discussion_answers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('discussion_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True)),
        sa.Column('is_helpful', sa.Boolean(), server_default=sa.text('false')),
        sa.Column('helpful_votes', sa.Integer(), server_default=sa.text('0')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['discussion_id'], ['discussions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    # ### Удаляем таблицы в обратном порядке ###
    op.drop_table('discussion_answers')
    op.drop_table('discussions')
"""
add_notifications_table

Revision ID: a2f0e886090d
Revises: dde6330bf630
Create Date:2026-01-20 09:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = 'a2f0e886090d'
down_revision = 'dde6330bf630'
branch_labels = None
depends_on = None


def upgrade():
    # ### Создаём таблицу notifications ###
    op.create_table('notifications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('type', sa.String(length=50), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('related_id', sa.Integer(), nullable=True),
        sa.Column('related_type', sa.String(length=50), nullable=True),
        sa.Column('is_read', sa.Boolean(), server_default=sa.text('false')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Создаём индексы
    op.create_index(op.f('ix_notifications_user_id'), 'notifications', ['user_id'])
    op.create_index(op.f('ix_notifications_type'), 'notifications', ['type'])
    op.create_index('idx_notifications_user_read', 'notifications', ['user_id', 'is_read'])
    op.create_index('idx_notifications_created', 'notifications', ['created_at'])


def downgrade():
    # ### Удаляем таблицу ###
    op.drop_table('notifications')
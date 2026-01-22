"""add_notification_table

Revision ID: 12e045cfd437
Revises: a2f0e886090d
Create Date: 2026-01-21 11:22:25.515758

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '12e045cfd437'
down_revision: Union[str, None] = 'a2f0e886090d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

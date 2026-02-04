"""update_user_role_to_admin

Revision ID: 80a702004a6d
Revises: 41d2b1d37828
Create Date: 2026-02-04 22:56:46.298444

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# ---- added by me ----- 
import sqlmodel
# ---- added by me ----- 

# revision identifiers, used by Alembic.
revision: str = '80a702004a6d'
down_revision: Union[str, Sequence[str], None] = '41d2b1d37828'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        "UPDATE authtable SET role = 'ADMIN', updated_at = NOW() WHERE id = 1"
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass

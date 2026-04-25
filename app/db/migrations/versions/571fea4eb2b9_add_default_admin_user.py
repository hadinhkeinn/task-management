"""Add default admin user

Revision ID: 571fea4eb2b9
Revises: 653730bda487
Create Date: 2026-04-25 07:48:26.242621

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '571fea4eb2b9'
down_revision: Union[str, None] = '653730bda487'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    from app.core.security import hash_password
    from app.core.config import settings

    admin_email = settings.ADMIN_EMAIL
    admin_password = settings.ADMIN_PASSWORD
    hashed_pwd = hash_password(admin_password)
    op.execute(
        f"INSERT INTO users (email, password, role) VALUES ('{admin_email}', '{hashed_pwd}', 'admin') ON CONFLICT DO NOTHING"
    )


def downgrade() -> None:
    from app.core.config import settings
    admin_email = settings.ADMIN_EMAIL
    op.execute(f"DELETE FROM users WHERE email='{admin_email}'")

"""add_users

Revision ID: 5b28af7fa5f4
Revises: 6dbf42a4309f
Create Date: 2023-07-21 14:37:15.600707

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "5b28af7fa5f4"
down_revision = "6dbf42a4309f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created", sa.TIMESTAMP(), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated", sa.TIMESTAMP(), server_default=sa.text("now()"), nullable=False),
        sa.Column("username", sa.String(length=32), nullable=False),
        sa.Column("hashed_password", sa.String(length=256), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )
    op.add_column("orders", sa.Column("user_id", sa.Integer(), nullable=True))
    op.create_foreign_key(None, "orders", "users", ["user_id"], ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "orders", type_="foreignkey")
    op.drop_column("orders", "user_id")
    op.drop_table("users")
    # ### end Alembic commands ###
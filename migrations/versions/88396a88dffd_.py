"""empty message

Revision ID: 88396a88dffd
Revises: bb0879f93a8d
Create Date: 2020-11-03 19:08:33.859907

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '88396a88dffd'
down_revision = 'bb0879f93a8d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password_hash', sa.String(length=128), nullable=False))
    op.drop_column('users', 'password')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('users', 'password_hash')
    # ### end Alembic commands ###
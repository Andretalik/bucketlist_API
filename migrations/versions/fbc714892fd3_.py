"""empty message

Revision ID: fbc714892fd3
Revises: 9dfc4aa14ead
Create Date: 2017-06-21 14:09:30.594716

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fbc714892fd3'
down_revision = '9dfc4aa14ead'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('email', sa.String(length=60), nullable=False))
    op.add_column('users', sa.Column('password', sa.String(length=200), nullable=False))
    op.alter_column('users', 'name',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.create_unique_constraint(None, 'users', ['email'])
    op.create_unique_constraint(None, 'users', ['name'])
    op.drop_column('users', 'password_encrypt')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password_encrypt', sa.VARCHAR(length=200), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_constraint(None, 'users', type_='unique')
    op.alter_column('users', 'name',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.drop_column('users', 'password')
    op.drop_column('users', 'email')
    # ### end Alembic commands ###
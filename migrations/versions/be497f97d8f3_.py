"""empty message

Revision ID: be497f97d8f3
Revises: e9d211c0c5d4
Create Date: 2020-08-27 00:34:43.725945

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be497f97d8f3'
down_revision = 'e9d211c0c5d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bots', sa.Column('background_image_url', sa.Text(), nullable=True, comment='twitterプロフィールの背景画像のurl'))
    op.add_column('bots', sa.Column('profile_image_url', sa.Text(), nullable=True, comment='twitterプロフィール画像のurl'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('bots', 'profile_image_url')
    op.drop_column('bots', 'background_image_url')
    # ### end Alembic commands ###

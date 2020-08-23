"""empty message

Revision ID: 772d65af6168
Revises: e85c926ce3e2
Create Date: 2020-08-23 19:32:20.417885

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '772d65af6168'
down_revision = 'e85c926ce3e2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bots',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.Column('twitter_user_id', sa.Text(), nullable=False, comment='ツイッターのユーザーID'),
    sa.Column('screen_name', sa.String(length=15), nullable=False, comment='@の付いているユーザー名'),
    sa.Column('profile_name', sa.String(length=20), nullable=True, comment='twitterで一番表示される名前'),
    sa.Column('url', sa.String(length=100), nullable=True, comment='twitterプロフィールに関連付けるurl'),
    sa.Column('location', sa.String(length=30), nullable=True, comment='twitterプロフィールのロケーション'),
    sa.Column('description', sa.String(length=160), nullable=True, comment='twitterプロフィールの自己紹介'),
    sa.Column('link_color', sa.String(length=6), nullable=True, comment='twitterプロフィールに関連付けるリンクの色'),
    sa.Column('profile_image_path', sa.Text(), nullable=True, comment='twitterプロフィール画像のファイルパス'),
    sa.Column('background_image_path', sa.Text(), nullable=True, comment='twitterプロフィールの背景画像のファイルパス'),
    sa.Column('access_token', sa.Text(), nullable=False, comment='twitter認証ユーザー(bot)のアクセストークン'),
    sa.Column('secret_token', sa.Text(), nullable=False, comment='twitter認証ユーザー(bot)のシークレットトークン'),
    sa.Column('create_at', sa.DateTime(), nullable=False),
    sa.Column('update_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('twitter_user_id', 'access_token', 'secret_token')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bots')
    # ### end Alembic commands ###

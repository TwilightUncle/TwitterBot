from werkzeug.security import check_password_hash, generate_password_hash
from app.database import db
from app.const import constant
from datetime import datetime


class Bot(db.Model):
    __tablename__ = 'bots'
    __table_args__ = (db.UniqueConstraint('twitter_user_id', 'access_token', 'secret_token'), {})
    
    id                      = db.Column(db.Integer, primary_key=True)
    owner_id                = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    twitter_user_id         = db.Column(db.Text, nullable=False, comment='ツイッターのユーザーID')
    screen_name             = db.Column(db.String(15), nullable=False, comment='@の付いているユーザー名')
    profile_name            = db.Column(db.String(20), comment='twitterで一番表示される名前')
    url                     = db.Column(db.String(100), comment='twitterプロフィールに関連付けるurl')
    location                = db.Column(db.String(30), comment='twitterプロフィールのロケーション')
    description             = db.Column(db.String(160), comment='twitterプロフィールの自己紹介')
    link_color              = db.Column(db.String(6), comment='twitterプロフィールに関連付けるリンクの色')
    profile_image_path      = db.Column(db.Text, comment='twitterプロフィール画像のファイルパス')
    background_image_path   = db.Column(db.Text, comment='twitterプロフィールの背景画像のファイルパス')
    access_token            = db.Column(db.Text, default='', nullable=False, comment='twitter認証ユーザー(bot)のアクセストークン')
    secret_token            = db.Column(db.Text, default='', nullable=False, comment='twitter認証ユーザー(bot)のシークレットトークン')
    create_at               = db.Column(db.DateTime, default=datetime.now, nullable=False)
    update_at               = db.Column(db.DateTime, default=datetime.now, nullable=False)


    @classmethod
    def create(cls, owner_id, twitter_user_id, screen_name, access_token='', secret_token=''):
        bot = cls(owner_id=owner_id, twitter_user_id=twitter_user_id, screen_name=screen_name, access_token=access_token, secret_token=secret_token)
        db.session.add(bot)
        return bot
    

    @classmethod
    def get_all(cls):
        return db.session.query(cls).all()
    

    def update(self, screen_name=None, profile_name=None, url=None, location=None, description=None, link_color=None, profile_image_path=None, background_image_path=None, access_token=None, secret_token=None):
        if screen_name:
            self.screen_name = screen_name
        if profile_name:
            self.profile_name = profile_name
        if url:
            self.url = url
        if location:
            self.location = location
        if description:
            self.description = description
        if link_color:
            self.link_color = link_color
        if profile_image_path:
            self.profile_image_path = profile_image_path
        if background_image_path:
            self.background_image_path = background_image_path
        if access_token:
            self.access_token = access_token
        if secret_token:
            self.secret_token = secret_token
        self.update_at = datetime.now()

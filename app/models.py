from werkzeug.security import check_password_hash, generate_password_hash
from app.database import db
from app.const import constant
from datetime import datetime

class TweetType(db.Model):
    __tablename__   = 'tweet_types'
    id              = db.Column(db.Integer, primary_key=True)
    type_num        = db.Column(db.Integer, nullable=False)
    interval        = db.Column(db.Integer, nullable=False)
    name            = db.Column(db.Text, nullable=False)
    create_at       = db.Column(db.DateTime, default=datetime.now, nullable=False)
    update_at       = db.Column(db.DateTime, default=datetime.now, nullable=False)
    tweets          = db.relationship("Tweet", backref="tweet_type")

class Tweet(db.Model):
    __tablename__   = 'tweets'
    id              = db.Column(db.Integer, primary_key=True)
    type_id         = db.Column(db.Integer, db.ForeignKey('tweet_types.id'), nullable=False)
    user_id         = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    text            = db.Column(db.Text, nullable=False)
    create_at       = db.Column(db.DateTime, default=datetime.now, nullable=False)
    update_at       = db.Column(db.DateTime, default=datetime.now, nullable=False)

class User(db.Model):
    __tablename__   = 'users'
    id              = db.Column(db.Integer, primary_key=True)
    name            = db.Column(db.Text, nullable=False)
    password        = db.Column(db.Text, nullable=False)
    permission      = db.Column(db.Integer, default=constant.PERMISSION_NOMAL, nullable=False)
    create_at       = db.Column(db.DateTime, default=datetime.now, nullable=False)
    update_at       = db.Column(db.DateTime, default=datetime.now, nullable=False)
    tweets          = db.relationship("Tweet", backref="tweets")


    @classmethod
    def create(cls, name, password, permission=3):
        user = cls(name=name, password=generate_password_hash(password), permission=permission)
        db.session.add(user)
        return user
    

    @classmethod
    def get_all(cls):
        return db.session.query(cls).all()
    

    def update(self, name=None, password=None, permission=None):
        if name:
            self.name = name
        if password:
            self.password = generate_password_hash(password)
        if permission:
            self.permission = permission

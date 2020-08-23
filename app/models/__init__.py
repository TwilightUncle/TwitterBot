from werkzeug.security import check_password_hash, generate_password_hash
from app.database import db
from app.const import constant
from datetime import datetime

from app.models.user import User


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

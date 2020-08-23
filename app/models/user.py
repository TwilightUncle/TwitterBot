from werkzeug.security import check_password_hash, generate_password_hash
from app.database import db
from app.const import constant
from datetime import datetime


class User(db.Model):
    __tablename__   = 'users'
    id              = db.Column(db.Integer, primary_key=True)
    name            = db.Column(db.Text, nullable=False)
    password        = db.Column(db.Text, nullable=False)
    permission      = db.Column(db.Integer, default=constant.PERMISSION_NOMAL, nullable=False)
    twitter_user_id = db.Column(db.Text)
    create_at       = db.Column(db.DateTime, default=datetime.now, nullable=False)
    update_at       = db.Column(db.DateTime, default=datetime.now, nullable=False)
    tweets          = db.relationship("Tweet", backref="tweets")


    @classmethod
    def create(cls, name, password, permission=3, twitter_user_id=None):
        user = cls(name=name, password=generate_password_hash(password), permission=permission, twitter_user_id=twitter_user_id)
        db.session.add(user)
        return user
    

    @classmethod
    def get_all(cls):
        return db.session.query(cls).all()
    

    def update(self, name=None, password=None, permission=None, twitter_user_id=None):
        if name:
            self.name = name
        if password:
            self.password = generate_password_hash(password)
        if permission:
            self.permission = permission
        if twitter_user_id:
            self.twitter_user_id = twitter_user_id

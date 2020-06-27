from app.database import db

class TweetType(db.Model):
    __tablename__   = 'tweet_types'
    id              = db.Column(db.Integer, primary_key=True)
    type_num        = db.Column(db.Integer)
    interval        = db.Column(db.Integer)
    name            = db.Column(db.Text)
    create_at       = db.Column(db.DateTime)
    update_at       = db.Column(db.DateTime)
    tweets          = db.relationship("Tweet", backref="tweet_type")

class Tweet(db.Model):
    __tablename__   = 'tweets'
    id              = db.Column(db.Integer, primary_key=True)
    type_id         = db.Column(db.Integer, db.ForeignKey('tweet_types.id'))
    text            = db.Column(db.Text)
    create_at       = db.Column(db.DateTime)
    update_at       = db.Column(db.DateTime)

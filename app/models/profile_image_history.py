from app.database import db
from app.const import constant
from datetime import datetime


class ProfileImageHistory(db.Model):
    __tablename__ = 'profile_image_historys'

    id          = db.Column(db.Integer, primary_key=True)
    bot_id      = db.Column(db.Integer, db.ForeignKey('bots.id'), nullable=False)
    image_path  = db.Column(db.Text, comment='ファイルパス', nullable=False)
    create_at   = db.Column(db.DateTime, default=datetime.now, nullable=False)
    update_at   = db.Column(db.DateTime, default=datetime.now, nullable=False)
    

    @classmethod
    def create(cls, bot_id, image_path):
        image_info = cls(bot_id=bot_id, image_path=image_path)
        db.session.add(image_info)
        db.session.flush()
        return image_info

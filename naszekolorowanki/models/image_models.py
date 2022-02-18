from datetime import datetime

from naszekolorowanki import db


class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80),  nullable=False)
    image = db.Column(db.String(150), nullable=False)
    thumbnail = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(300))
    info = db.Column(db.String(300))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Boolean, default=False)

    @staticmethod
    def get_by_username(username):
        return Image.query.filter_by(username=username)



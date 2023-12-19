from app import db, login_manager, bcrypt
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import Enum

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    text = db.Column(db.String, nullable=False)
    image_file = db.Column(db.String(100), nullable=False, default='default.jpg')
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    type = db.Column(Enum('news', 'publication', 'other'), nullable=False, default='news')
    enabled = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post(id={self.id}, title={self.title}, type={self.type}, created={self.created})"
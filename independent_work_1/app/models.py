from app import db

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120))
    message = db.Column(db.Text)
from app import db

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120))
    message = db.Column(db.Text)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(255))  # Нове поле "description"
    complete = db.Column(db.Boolean)

    def __init__(self, title, description, complete=False):
        self.title = title
        self.description = description
        self.complete = complete
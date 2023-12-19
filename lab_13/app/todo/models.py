from app import db




class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(255))
    complete = db.Column(db.Boolean)

    def __init__(self, title, description, complete=False):
        self.title = title
        self.description = description
        self.complete = complete


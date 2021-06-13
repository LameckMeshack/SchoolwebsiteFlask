from school2 import db




class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    regno = db.Column(db.String(length=10), nullable=False, unique=True)
    course = db.Column(db.String(length=50), nullable=False, unique=False)
    password = db.Column(db.String(100), unique=False, nullable=False)


def __repr__(self):
    return '<User %r>' % self.name

db.create_all()
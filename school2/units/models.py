from enum import unique
from school2 import db

from datetime import datetime


class Addunit(db.Model):
    __searchable__ = ['name','unitcode','lecname']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    unitcode = db.Column(db.String(80), nullable=False)
    lecname = db.Column(db.String(80), nullable=False)
    link = db.Column(db.String(255), nullable=False)

    
    pub_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)

    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'),
        nullable=False)
    faculty = db.relationship('Faculty',
        backref=db.backref('faculties', lazy=True))

    course_id = db.Column(db.Integer, db.ForeignKey('course.id'),
        nullable=False)
    course = db.relationship('Course',
        backref=db.backref('courses', lazy=True))

    def __repr__(self):
        return '<Addunit %r>' % self.name

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)

    def __repr__(self):
        return '<Course %r>' % self.name

class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)

    def __repr__(self):
        return '<Faculty %r>' % self.name


db.create_all()
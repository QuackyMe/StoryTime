from app import db
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


class Account(db.Model):
    __tablename__ = 'Account'
    id = db.Column(db.Integer, primary_key=True)
    type = username = db.Column(db.String(10), nullable=False)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(200), nullable=False)

    def __init__(self, username, password, type):
        self.username = username
        self.password = password
        self.type = type

    def __str__(self):
        return f"""ID: {self.id}
        Username: {self.username}
        Password: {self.password}
        Type: {self.type}"""


class Activity(db.Model):
    __tablename__ = 'Activity'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('Course.id'))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    deadline = db.Column(db.DateTime, nullable=True)

    def __init__(self, course_id, deadline):
        self.course_id = course_id
        self.deadline = deadline


class Announcement(db.Model):
    __tablename__ = 'Announcement'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('Course.id'))
    title = db.Column(db.String(90), nullable=False)
    message = db.Column(db.String(300))
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, course_id, title, message):
        self.course_id = course_id
        self.title = title
        self.message = message


class Course(db.Model):
    __tablename__ = 'Course'
    id = db.Column(db.Integer, primary_key=True)
    host = db.Column(db.Integer, db.ForeignKey('Account.id'))
    name = db.Column(db.String(20), unique=True)
    code = db.Column(db.String(5), unique=True)

    def __init__(self, host, name, code):
        self.host = host
        self.name = name
        self.code = code

    def __str__(self):
        return f"""
        ID: {self.id}\n
        host: {self.host}\n
        name: {self.name}\n
        code: {self.code}"""


class Choice(db.Model):
    __tablename__ = 'Choice'
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey(
        'Question.id'), nullable=False)
    item = db.Column(db.String(100), nullable=False)

    def __init__(self, question_id, item):
        self.question_id = question_id
        self.item = item


class Grade(db.Model):
    __tablename__ = 'Grade'
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('Account.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('Activity.id'))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    grade = db.Column(db.String(5))

    def __init__(self, account_id, activity_id, grade):
        self.account_id = account_id
        self.activity_id = activity_id
        self.grade = grade


class Material(db.Model):
    __tablename__ = 'Material'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('Course.id'))
    title = db.Column(db.String(90), nullable=False)
    content = db.Column(db.String(300), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, course_id, title, content):
        self.course_id = course_id
        self.title = title
        self.content = content


class Member(db.Model):
    __tablename__ = 'Member'
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('Account.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('Course.id'))

    def __init__(self, member_id, course_id):
        self.member_id = member_id
        self.course_id = course_id


class Question(db.Model):
    __tablename__ = 'Question'
    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('Activity.id'))
    question_number = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(20), nullable=False)
    ques = db.Column(db.String(100), nullable=False)
    answer = db.Column(db.String(50), nullable=False)

    def __init__(self, activity_id, question_number, type, ques, answer):
        self.activity_id = activity_id
        self.question_number = question_number
        self.type = type
        self.ques = ques
        self.answer = answer

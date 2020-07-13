from app import db
from datetime import datetime


class Account(db.Model):
    __tablename__ = 'Account'
    id = db.Column(db.Integer, primary_key=True)
    type = username = db.Column(db.String(10))
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(200))

    def __init__(self, username, password, type):
        self.username = username
        self.password = password
        self.type = type

    def __str__(self):
        return f"""ID: {self.id}
        Username: {self.username}
        Password: {self.password}
        Type: {self.type}"""


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


class Member(db.Model):
    __tablename__ = 'Member'
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('Account.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('Course.id'))

    def __init__(self, member_id, course_id):
        self.member_id = member_id
        self.course_id = course_id


class Announcement(db.Model):
    __tablename__ = 'Announcement'
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('Course.id'))
    title = db.Column(db.String(90))
    message = db.Column(db.String(300))
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, room_id, title, message):
        self.room_id = room_id
        self.title = title
        self.message = message


class Activity(db.Model):
    __tablename__ = 'Activity'
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('Course.id'))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    deadline = db.Column(db.DateTime, nullable=True)

    def __init__(self, room_id, deadline):
        self.room_id = room_id
        self.deadline = deadline


class Grade(db.Model):
    __tablename__ = 'Grade'
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('Course.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('Activity.id'))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    grade = db.Column(db.String(5))

    def __init__(self, room_id, activity_id, grade):
        self.room_id = room_id
        self.activity_id = activity_id
        self.grade = grade


class Question(db.Model):
    __tablename__ = 'Question'
    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('Activity.id'))
    type = db.Column(db.String(20))
    ques = db.Column(db.String(100))
    answer = db.Column(db.String(50))

    def __init__(self, activity_id, type, ques, answer):
        self.activity_id = activity_id
        self.type = type
        self.ques = ques
        self.answer = answer


class Choice(db.Model):
    __tablename__ = 'Choice'
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('Question.id'))
    name = db.Column(db.String(100))

    def __init__(self, question_id, name):
        self.question_id = question_id
        self.name = name

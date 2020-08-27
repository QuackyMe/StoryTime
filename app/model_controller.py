from app import db
from .models import Account, Course, Announcement
from flask import request


class CourseModel():
    def __init__(self, code, name, host):
        self.code = code
        self.name = name
        self.host = host


class MemberName():
    def __init__(self, name):
        self.name = name


class ActivityModel():
    def __init__(self, question, answer, choice):
        self.question = question
        self.answer = answer
        self.choice = choice


def get_name(account_id):
    return Account.query.filter_by(id=account_id).first().username


def get_course_id(course_code):
    return Course.query.filter_by(code=course_code).first().id


def student_courses(student_id):
    sql = f"""SELECT c.code, c.name, c.host
        FROM public."Course" AS "c"
        INNER JOIN public."Member" AS "m" ON c.id=m.course_id
        WHERE m.member_id = {student_id}"""
    query = db.engine.execute(sql)
    courses = [CourseModel(course[0], course[1], get_name(course[2]))
               for course in query]
    return courses


def class_members(course_code):
    sql = f"""SELECT ac.username
    FROM "Account" "ac"
    INNER JOIN "Member" AS "m" ON m.member_id = ac.id
    WHERE m.course_id = {get_course_id(course_code)};"""
    query = db.engine.execute(sql)
    students = [MemberName(student[0]) for student in query]
    return students


def get_choice(activity_id, question_number):
    sql = f"""SELECT q.ques, q.answer, c,item FROM "Choice" AS "c"
    INNER JOIN "Question" AS "q" ON c.question_id = q.id
    WHERE q.activity_id = {activity_id} AND q.question_number = {question_number};"""
    query = db.engine.execute(sql)
    for x in query:
        print(x)

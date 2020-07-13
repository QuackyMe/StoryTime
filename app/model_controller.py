from app import db
from .models import Account


class CourseModel():
    def __init__(self, code, name, host):
        self.code = code
        self.name = name
        self.host = host


def student_courses(student_id):
    sql = f"""SELECT c.code, c.name, c.host
        FROM public."Course" AS "c"
        INNER JOIN public."Member" AS "m"
            ON c.id=m.course_id
        WHERE m.member_id = {student_id}"""
    query = db.engine.execute(sql)
    courses = [CourseModel(course[0], course[1], get_name(course[2])) for course in query]
    return courses


def get_name(account_id):
    name = Account.query.filter_by(id=account_id).first().username
    return name

# def login_validation():


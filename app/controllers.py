from app import app, db
from flask import request, render_template, redirect, session, url_for
from .models import Account, Course, Member, Announcement, Question, Activity, Choice, Material
from .controller.randomGenerator import generate_alphanumeric
from .model_controller import student_courses, class_members, get_course_id, get_choice

from random import shuffle


# Default Route
@app.route('/')
def to_home():
    return redirect(url_for('test', activity=10))


# Login Page Render
@app.route('/login/')
def login():
    return render_template('login.html')


# Login Submit
@app.route('/login/submit', methods=['POST'])
def login_process():
    session.pop("acc_id", None)
    session.pop("acc_type", None)
    username = request.form['username']
    password = request.form['password']

    # Login Validation
    user = Account.query.filter_by(username=username).first()
    if Account.query.filter_by(username=username).first() is None:
        return render_template('login.html', error='Username not found')
    elif username == '' or password == '':
        return render_template('login.html', error='Please enter required fields')
    elif user.password != password:
        return render_template('login.html', error='Username/Password does not match')
    else:
        session["acc_id"] = user.id
        session["acc_type"] = str(user.type)
        print('account: ' + str(session["acc_id"]))
        print('type: ' + str(session['acc_type']))
        return redirect(url_for('manage_course'))


# Register Page Render
@app.route('/register/')
def register_page():
    return render_template('register.html')


# Register Submit
@app.route('/register/submit', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    conf_password = request.form['conf_password']
    type = request.form['acc_type']

    # Register Validation
    # Checks the database if username already exist
    if Account.query.filter_by(username=username).first() is not None:
        return render_template('register.html', error='Username Already Exist')
    elif (conf_password != password):  # Checks if password and confirm password match
        return render_template('register.html', error='Password does not match')
    else:
        data = Account(username, password, type)
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('login', message='Registration Successful'))


# Logout Handler
@app.route('/logout')
def logout():
    session.pop('acc_id', None)
    return redirect(url_for('login'))


# Display Course Page Render
@app.route('/course/')
def manage_course():
    courses = student_courses(session['acc_id'])
    if session['acc_type'] == "student":
        return render_template('mc_student.html', courses=courses)
    else:
        courses = Course.query.filter_by(host=session['acc_id']).all()
        for course in courses:
            print(str(course))
        return render_template('mc_teacher.html', courses=courses)


# Course Page Render
@app.route('/course/<course_code>/')
def course(course_code):
    print(course_code)
    students = class_members(course_code)
    announcements = Announcement.query.filter_by(course_id=get_course_id(course_code)).all()
    materials = Material.query.filter_by(course_id=get_course_id(course_code)).all()
    activities = Activity.query.filter_by(course_id=get_course_id(course_code)).all()
    num_students = len(students)

    if session['acc_type'] == "student":
        return render_template('cr_student.html', students=students, announcements=announcements, course_code=course_code, num_students=num_students, materials=materials, activities=activities)
    else:
        return render_template('cr_teacher.html', students=students, announcements=announcements, course_code=course_code, num_students=num_students, materials=materials, activities=activities)


# Create Course Handler
@app.route('/course/create/submit', methods=['POST'])
def create_course():
    course_name = request.form['course_name']
    host_id = session["acc_id"]

    if Course.query.filter_by(name=course_name).first() is not None:
        return render_template('mc_teacher.html', error='Course Name Already Exist')
    else:
        code = generate_alphanumeric(5)
        data = Course(host_id, course_name, code)
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('course', course_code=code))


# Join Handler
@app.route('/course/join/submit', methods=['POST'])
def add_member():
    join_code = request.form.getlist('joincode[]')
    join_code = ''.join(join_code).upper()
    course = Course.query.filter_by(code=join_code).first()
    student_code = session["acc_id"]

    print(join_code)
    if course is None:
        return render_template('mc_student.html', message='Course does not exist')
    elif Member.query.filter_by(member_id=student_code).filter_by(course_id=get_course_id(join_code)).first() is not None:
        return render_template('mc_student.html', message='Already Joined')
    elif session['acc_type'] != "student":
        return render_template('mc_student.html', message='Only students can join')
    else:
        data = Member(student_code, course.id)
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('manage_course'))


# Create Learning Material Render
@app.route('/course/<course_code>/material/create')
def material(course_code):
    print(f'COURSE CODE: {course_code}')
    return render_template('add_material.html', course_code=course_code)


# Create Learning Material Handler
@app.route('/create-material/<course_code>', methods=['POST'])
def create_material(course_code):
    print(f'COURSE CODE: {course_code}')
    title = request.form['title']
    content = request.form['content']
    course = Course.query.filter_by(code=course_code).first()

    data = Material(course.id, title, content)
    db.session.add(data)
    db.session.commit()

    return redirect(url_for('course', course_code=course_code))


# Read Learning Material Render
@app.route('/course/<course_code>/material/view/<material_id>', methods=['POST'])
def read_material(course_code, material_id):
    material = Material.query.filter_by(id=material_id).first()
    return render_template('read_material.html', material=material)


# Create Announcement Handler
@app.route('/create-announcement')
def create_announcement(course_code):
    print(f"COURSE CODE: {str(course_code)}")
    course = Course.query.filter_by(code=course_code).first()
    title = request.form['title']
    content = request.form['content']

    data = Announcement(course.id, title, content)
    db.session.add(data)
    db.session.commit()
    return render_template('cr_teacher.html', message='Successfully posted an announcement')


# Create Activity Page Render
@app.route('/course/<course_code>/create-activity/')
def activity(course_code):
    # Erases the data when activity page is load (temporary code)
    Choice.query.delete()
    Question.query.delete()
    Activity.query.delete()
    db.session.commit()
    return render_template('add_activity.html', course_code=course_code)


# Create Activity Handler
@app.route('/course/<course_code>/create-activity/create', methods=['POST'])
def add_activity(course_code):
    question = request.form.getlist('question[]')
    question_type = request.form.getlist('type[]')
    question_ans = request.form.getlist('answer[]')

    print(f"question {question} - answer {question_ans}")
    # Replace with Deadline input
    data = Activity(get_course_id(course_code), None)
    db.session.add(data)
    db.session.commit()

    activity = Activity.query.order_by(Activity.id.desc()).first()
    print(activity.id)
    question_list = []
    for i in range(1, len(question)):
        print(
            f"TEEEEEEEEEEEES{activity.id}, {question_type[i]}, {question[i]}, {question_ans[i]}")
        question_list.append(
            Question(activity.id, i, question_type[i], question[i], question_ans[i]))
    db.session.bulk_save_objects(question_list)
    db.session.commit()
    choice_list = []

    for i in range(1, len(question)):
        choices = request.form.getlist(f'choice_{str(i)}')
        for j in range(len(choices)):
            ques = Question.query.filter_by(
                activity_id=activity.id).filter_by(question_number=i).first()
            choice_list.append(Choice(ques.id, choices[0]))
            choices.pop(0)
    db.session.bulk_save_objects(choice_list)
    db.session.commit()

    return render_template('add_activity.html', course_code=course_code, message="Success!")


# Activity Page Render
@app.route('/course/<course_code>/activity/<activity_id>/<question_number>')
def perform_activity(course_code, activity_id, question_number):
    question = Question.query.filter_by(activity_id=activity_id).filter_by(question_number=question_number).first()
    choice = Choice.query.filter_by(question_id=question.id).all()
    return render_template('activity.html', course_code=course_code, activity_id=activity_id, question=question, choice=choice)


# TEST PAGE
@app.route('/test/<activity>')
def test(activity):
    questions = Question.query.filter_by(activity_id=activity).all()
    choice_li = []
    for question in questions:
        li = []
        choices = Choice.query.filter_by(question_id=question.id).all()
        li.append(question.answer)
        for choice in choices:
            li.append(choice.item)
        shuffle(li)
        choice_li.append(str(li).replace("[", "").replace("]", ""))
    
    print(choice_li)
    print(choice_li[0])

    return render_template("activity.html", questions=questions, choice=choice_li)


# TEST
@app.route('/test/result', methods=['POST'])
def test_page():
    li = request.form.getlist('test[]')
    for item in li:
        print(item)
    return str(li)

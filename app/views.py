from app import app, db
from flask import request, render_template, redirect, session, url_for
from .models import Account, Course, Member, Announcement
from .controller.randomGenerator import generate_alphanumeric
from .model_controller import student_courses


# Default Route
@app.route('/')
def to_home():
    return redirect(url_for('login'))


# Login Page
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


# Register Page
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
    if Account.query.filter_by(username=username).first() is not None:  # Checks the database if username already exist
        return render_template('register.html', error='Username Already Exist')
    elif (conf_password != password):  # Checks if password and confirm password match
        return render_template('register.html', error='Password does not match')
    else:
        data = Account(username, password, type)
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('login'))


# Logout Handler
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('acc_id', None)
    return redirect(url_for('login'))


# Display Course Page
@app.route('/manage-course/')
def manage_course():
    courses = student_courses(session['acc_id'])
    if session['acc_type'] == "student":
        return render_template('mc_student.html', courses=courses)
    else:
        courses = Course.query.filter_by(host=session['acc_id']).all()
        for course in courses:
            print(str(course))
        return render_template('mc_teacher.html', courses=courses)


# Create Course Page
@app.route('/course/create')
def create_course():
    print('account2: ' + str(session["acc_id"]))
    return render_template('mc_teacher_test.html')


# Create Course Handler
@app.route('/course/create/submit', methods=['POST'])
def submit_create_course():
    course_name = request.form['course_name']
    host_id = session["acc_id"]

    if Course.query.filter_by(name=course_name).first() is not None:
        return render_template('mc_teacher_test.html', error='Course Name Already Exist')
    else:
        code = generate_alphanumeric(5)
        data = Course(host_id, course_name, code)
        db.session.add(data)
        db.session.commit()
        return render_template('mc_teacher_test.html', error='Success')


# Add Student Handler
@app.route('/course/join/submit', methods=['POST'])
def add_member():
    join_code = request.form['join_code']
    room = Course.query.filter_by(code=join_code).first()
    student_code = session["acc_id"]

    if room is None:
        return render_template('mc_student_test.html', message='Course does not exist')
    elif Member.query.filter_by(member_id=student_code).first() is not None:
        return render_template('mc_student_test.html', message='Already Joined')
    elif session['acc_type'] != "Student":
        return render_template('mc_student_test.html', message='Only students can join')
    else:
        data = Member(student_code, room.id)
        db.session.add(data)
        db.session.commit()
        return render_template('mc_student_test.html', message='Sucessfully Joined Course')


# Create Announcement Page
@app.route('/course/code=<course_code>/announcement')
def announcement(course_code):
    return render_template('mc_student_test.html', course_code=course_code)


# Create Announcement Handler
@app.route('/course/code=<course_code>/announcement/create', methods=['POST'])
def create_announcement(course_code):
    print("COURSE CODE: " + str(course_code))
    course = Course.query.filter_by(code=course_code).first()
    title = request.form['title']
    content = request.form['content']

    data = Announcement(course.id, title, content)
    db.session.add(data)
    db.session.commit()
    return render_template('create_announcement.html', message='Success')


# TEST PAGE
@app.route('/test')
def test_page():
    return render_template("test.html")


# TEST
@app.route('/test/result', methods=['POST'])
def test():
    li = request.form.getlist('test[]')
    for item in li:
        print(item)
    return str(li)

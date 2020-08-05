from app import app, db
from flask import request, render_template, redirect, session, url_for
from .models import Account, Course, Member, Announcement, Question, Activity, Choice
from .controller.randomGenerator import generate_alphanumeric
from .model_controller import student_courses, class_members, get_course_id


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
    # Checks the database if username already exist
    if Account.query.filter_by(username=username).first() is not None:
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
# @app.route('/course/create')
# def create_course():
#     print('account2: ' + str(session["acc_id"]))
#     return render_template('mc_teacher.html')


# Create Course Handler
@app.route('/course/create/submit', methods=['POST'])
def submit_create_course():
    course_name = request.form['course_name']
    host_id = session["acc_id"]

    if Course.query.filter_by(name=course_name).first() is not None:
        return render_template('mc_teacher.html', error='Course Name Already Exist')
    else:
        code = generate_alphanumeric(5)
        data = Course(host_id, course_name, code)
        db.session.add(data)
        db.session.commit()
        return render_template('mc_teacher.html', error='Success')


# Join Handler
@app.route('/course/join/submit', methods=['POST'])
def add_member():
    join_code = request.form.getlist('joincode[]')
    join_code = ''.join(join_code).upper()
    room = Course.query.filter_by(code=join_code).first()
    student_code = session["acc_id"]

    print(join_code)
    if room is None:
        return render_template('mc_student.html', message='Course does not exist')
    elif Member.query.filter_by(member_id=student_code).first() is not None:
        return render_template('mc_student.html', message='Already Joined')
    elif session['acc_type'] != "student":
        return render_template('mc_student.html', message='Only students can join')
    else:
        data = Member(student_code, room.id)
        db.session.add(data)
        db.session.commit()
        return render_template('mc_student.html', message='Sucessfully Joined Course')


# Course Room Page
@app.route('/manage-course/code=<course_code>/', methods=['POST'])
def course_room(course_code):
    print(course_code)
    students = class_members(course_code)
    announcements = Announcement.query.filter_by(
        room_id=get_course_id(course_code)).all()

    num_students = len(students)

    #   return render_template('cr_student.html', students=students, announcements=announcements)
    if session['acc_type'] == "student":
        return render_template('cr_student.html', students=students, announcements=announcements, course_code=course_code, num_students=num_students)
    else:
        return render_template('cr_teacher.html', students=students, announcements=announcements, course_code=course_code, num_students=num_students)


# Create Announcement Page
@app.route('/manage-course/code=<course_code>/announcement')
def announcement(course_code):
    return render_template('add_announcement.html', course_code=course_code)


# Create Announcement Handler
@app.route('/manage-course/code=<course_code>/announcement/create', methods=['POST'])
def create_announcement(course_code):
    print("COURSE CODE: " + str(course_code))
    course = Course.query.filter_by(code=course_code).first()
    title = request.form['title']
    content = request.form['content']

    data = Announcement(course.id, title, content)
    db.session.add(data)
    db.session.commit()
    return render_template('cr_teacher.html', announcement_message='Success')


# Create Activity Page
@app.route('/manage-course/code=<course_code>/create-activity/', methods=['POST'])
def activity(course_code):
    Question.query.delete()
    Choice.query.delete()
    Activity.query.delete()
    db.session.commit()
    return render_template('add_activity.html', course_code=course_code)


# Create Activity Handler
@app.route('/manage-course/code=<course_code>/create-activity/create', methods=['POST'])
def add_activity(course_code):
    question = request.form.getlist('question[]')
    question_type = request.form.getlist('type[]')
    question_ans = request.form.getlist('answer[]')

    print(f"question {question} - answer {question_ans}")
    data = Activity(get_course_id(course_code), None)  # Replace with Deadline input
    db.session.add(data)
    db.session.commit()

    activity = Activity.query.order_by(Activity.id.desc()).first()
    print(activity.id)
    question_list = []
    for i in range(1, len(question)):
        print(f"TEEEEEEEEEEEES{activity.id}, {question_type[i]}, {question[i]}, {question_ans[i]}")
        question_list.append(Question(activity.id, i, question_type[i], question[i], question_ans[i]))
    db.session.bulk_save_objects(question_list)
    db.session.commit()
    choice_list = []

    for i in range(1, len(question)):
        choices = request.form.getlist(f'choice_{str(i)}')
        for j in range(len(choices)):
            ques = Question.query.filter_by(activity_id=activity.id).filter_by(question_number=i).first()
            choice_list.append(Choice(ques.question_number, choices[i - 1]))
    db.session.bulk_save_objects(choice_list)
    db.session.commit()

    return render_template('add_activity.html', course_code=course_code, message="Success!")


# TEST PAGE
@app.route('/test')
def test():
    return render_template("base.html")


# TEST
@app.route('/test/result', methods=['POST'])
def test_page():
    li = request.form.getlist('test[]')
    for item in li:
        print(item)
    return str(li)

# course/code=AAAAA/create-activity/
# nextval('"Question_id_seq"'::regclass)

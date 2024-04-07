import random
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Define a username and password for demonstration purposes
USERNAME = "sam"
PASSWORD = "1234"

def generate_timetable_with_rooms(subjects, labs, subject_classrooms, lab_rooms):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    regular_subjects = subjects.split(',')
    lab_subjects = labs.split(',')
    subject_classrooms_list = subject_classrooms.split(',')
    lab_rooms_list = lab_rooms.split(',')
    dummy_timetable = {}
    labs_assigned = []

    for day in days:
        dummy_timetable[day] = []

        for i in range(9, 13):
            subject = random.choice(regular_subjects)
            classroom = random.choice(subject_classrooms_list)
            dummy_timetable[day].append({'time': f"{i}:00 AM to {i+1}:00 AM", 'subject': subject, 'classroom': classroom})

        dummy_timetable[day].append({'time': '1:00 PM to 1:30 PM', 'subject': 'lunch', 'classroom': '-'})
        
        available_labs = [lab for lab in lab_subjects if lab not in labs_assigned]
        if available_labs:
            lab_subject = random.choice(available_labs)
            lab_room = random.choice(lab_rooms_list)
            dummy_timetable[day].append({'time': '1:30 PM to 3:30 PM', 'subject': lab_subject, 'classroom': lab_room})
            labs_assigned.append(lab_subject)

    return dummy_timetable

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == USERNAME and password == PASSWORD:
            return redirect(url_for('index'))
        else:
            error_message = "Invalid username or password."
            return render_template('login.html', error=error_message)
    else:
        return render_template('login.html', error=None)


@app.route('/timetable', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        subjects = request.form['subjects']
        labs = request.form['labs']
        subject_classrooms = request.form['subject_classrooms']
        lab_rooms = request.form['lab_rooms']
        
        if not subjects.strip() or not labs.strip() or not subject_classrooms.strip() or not lab_rooms.strip():
            error_message = "Please fill out all fields."
            return render_template('index.html', error=error_message)
        
        timetable = generate_timetable_with_rooms(subjects, labs, subject_classrooms, lab_rooms)
        return render_template('index.html', timetable=timetable, days=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
    else:
        return render_template('index.html', timetable=None, days=None)


if __name__ == '__main__':
    app.run(debug=True)
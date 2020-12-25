from flask import Flask, render_template, request, session, url_for, redirect, flash,\
jsonify
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from wtforms import StringField, SubmitField, SelectField, FormField
from wtforms.validators import DataRequired
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

import requests
import json, sys


basedir =os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#cors = CORS(app, resources={r"/sessions/*": {"origins": "*"}})
cors = CORS(app, resources={r"/sessions/*": {"origins": "*"},\
							r"/roster/": {"origins": "*"}, r"/classes/": {"origins": "*"},
							r"/studentsIn/*": {"origins": "*"}})
#roster_cors = CORS(app, resources={r"/roster/": {"origins": "*"}})
#classes_cors = CORS(app, resources={r"/classes/": {"origins": "*"}})

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)
moment = Moment(app)

from models import *
from queries import *
from forms import *

#shell context
@app.shell_context_processor
def make_shell_context():
	return dict(db=db, Student=Student, Class=Class, Teacher=Teacher, ClassHours=ClassHours)





@app.route('/view', methods=['GET', 'POST'])
def view_query():

	data = None
	show_add_button = None
	show_drop_button = None
	option = "Clear"
	all_classes = view_all_entries(Class, simple=True)
	class_sessions = None
	classfield = None


	

	if request.method == 'POST':
	

		if request.form.get('confirm_add_button') == 'Confirm Add':
			print("here")
			#end_hour = request.form.get('end-hour')
			#print(request.form)
			#print(type(end_hour))
			
			course = request.form.get("classfield")
			day = request.form.get("days-dropdown")
			start_hour = int(request.form.get('start-hour'))
			start_minute = int(request.form.get('start-minute'))
			end_hour = int(request.form.get('end-hour'))
			end_minute = int(request.form.get('end-minute'))
			room = request.form.get('room-dropdown')
			print(type(end_hour))
			set_time(course, get_day_id(day), start_hour, start_minute, end_hour, end_minute, room)
			
		if request.form.get('drop_button') == 'drop':
			
			classfield = request.form.get("classfield")
			#drop_confirm = request.form.get("classfield")
			#dc_check = True
			#print(drop_confirm)
			if classfield != "Classes":
				show_drop_button = "true"
				class_sessions = parse_class_schedule(\
					view_all_class_sessions(classfield))

		
		if request.form.get('confirm_modify_button') == 'Confirm Modify':
			#print(request.form)
			session_id = int(request.form.get('sessionfield'))
			#print(test2["class-name"])
			classfield = request.form.get("classfield")
			print('******* this is the confirm button')
			#print(classfield)
			#print(sessionfield)
			course = request.form.get("classfield")
			day = request.form.get("days-dropdown")
			start_hour = int(request.form.get('start-hour'))
			start_minute = int(request.form.get('start-minute'))
			end_hour = int(request.form.get('end-hour'))
			end_minute = int(request.form.get('end-minute'))
			room = request.form.get('room-dropdown')

			#print("{}{}{}{}{}{}{}".format(course,day,start_hour,start_minute,end_hour,end_minute,room))
			
			modify_session(classfield, session_id, day, start_hour,start_minute,end_hour,end_minute,room)

		if request.form.get('confirm-drop-button') == 'Confirm Drop':
			session_id = int(request.form.get('sessionfield'))
			#print(test2["class-name"])
			classfield = request.form.get("classfield")
			print('*******')
			print(classfield)
			if classfield != "Classes":
				delete_session(classfield, session_id)




		if request.form.get('submit_button') == 'query':
			query_choice = request.form.get("queries")
			search = request.form['searchfield']
			if classfield != "Classes":
				classfield = request.form.get('classfield')
			
			print('******')
			print(search)
			
			if query_choice == "View All Classes":
				data = view_all_entries(Class)
				option = "View All Classes"
			#
			if query_choice == "View Schedule of a Class":
				data = view_all_class_sessions_schedule(search)
				option = "View Schedule of a Class"

			if query_choice == "View All Students":
				data = view_all_entries(Student)
				option = "View All Students"

			if query_choice == "View All Teachers":
				data = view_all_entries(Teacher)
				option = "View All Teachers"

			if query_choice == "View Schedule of a Student":
				data = view_entry_schedule(search, Student)
				option = "View Schedule of a Student"
			#
			if query_choice == "View Schedule of a Teacher":
				data = view_entry_schedule(search, Teacher)
				option = "View Schedule of a Teacher"
			#
			if query_choice == "View All Students in a Class":
				data = view_objects_in_entry(Student, Class, search)
				#data = jsonify({"students":data})
				option = "View All Students in a Class"

			if query_choice == "Clear":
				data = ""
				option = "Clear"

			if query_choice == "New student":
				data = add_entry(search, Student)
				option = "New student"

			if query_choice == "New class":
				data = add_entry(search, Class)
				option = "New class"

			if query_choice == "New teacher":
				data = add_entry(search, Teacher)
				option = "New teacher"

			if query_choice == "Delete student":
				data = remove_entry(search, Student)
				option = "Delete student"

			if query_choice == "Delete class":
				data = remove_entry(search, Class)
				option = "Delete class"

			if query_choice == "Delete teacher":
				data = remove_entry(search, Teacher)
				option = "Delete teacher"

			if query_choice == "Add class for student":
				data = add_drop_class_to_target(True, classfield, search, Student)
				option = "Add class for student"

			if query_choice == "Remove class for student":
				data = add_drop_class_to_target(False, classfield, search, Student)
				option = "Remove class for student"

			if query_choice == "Add class for teacher":
				print(classfield)
				data = add_drop_class_to_target(True, classfield, search, Teacher)
				option = "Add class for teacher"

			if query_choice == "Remove class for teacher":
				data = add_drop_class_to_target(False, classfield, search, Teacher)
				option = "Remove class for teacher"

			if query_choice == "View master schedule (days)":
				data = view_master_schedule_days()
				option = "View master schedule (days)"

			if query_choice == "Add a class session":
				data = set_time(classfield, day, start_hour, start_minute, end_hour, end_minute, room)
				option = "Add a class session"

			if query_choice == "Remove a class session":
				data = delete_time(session_field)
				option = "Remove a class session"



	return render_template("view.html", data=data, option=option, all_classes=all_classes, 
							show_add_button=show_add_button, show_drop_button=show_drop_button,\
							class_sessions=class_sessions, classfield=classfield)

@app.route('/sessions/<string:class_name>', methods=['GET', 'POST'])
def sessions(class_name):
	class_sessions = parse_class_schedule(\
					view_all_class_sessions(class_name))

	return jsonify({
		"className": class_name,
		"sessions": class_sessions
		})

@app.route('/roster/', methods=['GET', 'POST'])
def roster():
	
	students = view_all_entries(Student, parse=True)
	teachers = view_all_entries(Teacher, parse=True)
		
	return jsonify({
		"students": students,
		"teachers": teachers
		})

@app.route('/studentsIn/<string:class_name>', methods=['GET', 'POST'])
def students_in_class(class_name):
	
	students = view_objects_in_entry(Student, Class, class_name)

		
	return jsonify({
		"students": students
		})

@app.route('/classes/', methods=['GET', 'POST'])
def classes():
	
	classes = view_all_entries(Class, parse=True)
	classesJSON = json.dumps(classes, indent=4)	
			
	return classesJSON

#class TeacherForm(FlaskForm):
	#print([(view_all_entries(Teacher)[i], view_all_entries(Teacher)[i]) for i in range( len(view_all_entries(Teacher)) )])
#	select = SelectField(u'Teacher Name', choices=[(view_all_entries(Teacher)[i], view_all_entries(Teacher)[i]) for i in range( len(view_all_entries(Teacher)) )])
#	search_teacher = SubmitField('Search Teacher')
'''

class TeacherForm(FlaskForm):

	select = SelectField(u'Teacher Name', choices=[(view_all_entries(Teacher)[i], view_all_entries(Teacher)[i]) for i in range( len(view_all_entries(Teacher)) )])
	search_teacher = SubmitField('Search Teacher')

class ClassForm(FlaskForm):

	select = SelectField(u'Class Name', choices=[(view_all_entries(Class, simple=True)[i], view_all_entries(Class, simple=True)[i]) for i in range( len(view_all_entries(Class, simple=True)) )])
	search_class = SubmitField('Search Class')

'''


@app.route('/jpi', methods=['GET', 'POST'])
def jpi():
	
	form = ViewForm()

	if request.method == 'POST':
		print(request.form)


		if request.form.get('entry') == "Search Student":
			#let me see if i can make a function to factor this out
			entry = request.form.get('student')
			error = None
			max_day = None
			rows = None
			if get_one_entry(entry, Student) == None:
				flash("This student is not in the database, check spelling please")
				return render_template('jpi.html', form=form)
			
			try:
				max_day = max_day_in_week(entry, Student)	
				rows = parsed_rows(entry, Student)
			except:
				flash("{} has no classes scheduled".format(entry))
				return render_template('jpi.html', form=form, entry=entry)
			return render_template('jpi.html', form=form, entry=entry, max_day=max_day, rows=rows)
			#except:
				#error = "This student has no classes scheduled"
			#return render_template('jpi.html', form=form, entry=entry, max_day=max_day, rows=rows, error=error)#


		if request.form.get('search_teacher') == "Search Teacher":
			#let me see if i can make a function to factor this out
			entry = request.form.get('select')
			error = None
			max_day = None
			rows = None
			try:
				max_day = max_day_in_week(entry, Teacher)	
				rows = parsed_rows(entry, Teacher)
			except:
				flash("{}.format has no classes scheduled".format(entry))
				return render_template('jpi.html', form=form, entry=entry)
			return render_template('jpi.html', form=form, entry=entry, max_day=max_day, rows=rows)

		if request.form.get('search_class') == "Search Class":
			
			course = request.form.get('select')
			error = None
			max_day = None
			rows = None
			try:
				max_day = max_day_in_week(course, Class)	
				rows = parsed_rows(course, Class)
			except:
				flash("{} has no sessions scheduled".format(course))
				return render_template('jpi.html', form=form)
			return render_template('jpi.html', form=form, course=course, max_day=max_day, rows=rows)




	if form.validate_on_submit():
		
		classes = False
		
		if form.select.data == 'single_student':
			second_form = StudentForm()
			return render_template('jpi.html', form=form, second_form=second_form)
		if form.select.data == 'single_teacher':
			second_form = TeacherForm.new()	
			return render_template('jpi.html', form=form, second_form=second_form)

		if form.select.data == 'single_class':
			second_form = ClassForm.new()
			return render_template('jpi.html', form=form, second_form=second_form)
		if form.select.data == 'teachers':
			entries = view_all_entries(Teacher)
			return render_template('jpi.html', form=form, entries=entries)
		if form.select.data == 'students':
			entries = view_all_entries(Student)
			return render_template('jpi.html', form=form, entries=entries)

		if form.select.data == 'classes': 	
			classes = True
			teachers = []
			entries = view_all_entries(Class, simple=True)
			for entry in entries:
				try:
					teachers.append(view_objects_in_entry(Teacher, Class, entry.name)[0])
				except:
					teachers.append("No teacher assigned")
			length = len(entries)		
			return render_template('jpi.html', form=form, entries=entries, classes=classes, teachers=teachers, length=length)

		if form.select.data == 'master':
			max_day = max_day_in_week()	
			rows = parsed_rows()
			return render_template('jpi.html', form=form, max_day=max_day, rows=rows)

	return render_template('jpi.html', form=form)
'''
class TeacherDropForm(FlaskForm):

	select = SelectField(u'Teacher Name', choices=[(view_all_entries(Teacher)[i], view_all_entries(Teacher)[i]) for i in range( len(view_all_entries(Teacher)) )])
	drop_teacher = SubmitField('Drop Teacher')

class ClassDropForm(FlaskForm):

	select = SelectField(u'Class Name', choices=[(view_all_entries(Class, simple=True)[i], view_all_entries(Class, simple=True)[i]) for i in range( len(view_all_entries(Class, simple=True)) )])
	drop_class = SubmitField('Drop Class')		

class AddClassToStudentForm(FlaskForm):

	select = SelectField(u'Class Name', choices=[(view_all_entries(Class, simple=True)[i], view_all_entries(Class, simple=True)[i]) for i in range( len(view_all_entries(Class, simple=True)) )])
	student = StringField('Enter Student to Give Class To')
	add_class = SubmitField('Add Class')

class AddClassToTeacherForm(FlaskForm):

	select = SelectField(u'Class Name', choices=[(view_all_entries(Class, simple=True)[i], view_all_entries(Class, simple=True)[i]) for i in range( len(view_all_entries(Class, simple=True)) )])
	teacher = SelectField(u'Select Teacher to Give Class To', choices=[(view_all_entries(Teacher)[i], view_all_entries(Teacher)[i]) for i in range( len(view_all_entries(Teacher)) )])
	add_class = SubmitField('Add Class')
'''
		
@app.route('/addDrop', methods=['GET', 'POST'])
def addDrop():

	#fix, there's an issue with case sensitivity
	print(1)
	print(request.values)
	print(request.form)
	print("liverpool tied everton")
	view_form = ViewForm()
	add_drop_form = AddDropForm()

	if request.method == 'POST':
		
		if add_drop_form.select.data == 'single_student_add':
			followup_form = StudentAddForm()

			return render_template('addDrop.html', view_form=view_form, add_drop_form=add_drop_form, followup_form=followup_form)

		if add_drop_form.select.data == 'single_teacher_add':
			followup_form = TeacherAddForm()
			return render_template('addDrop.html', view_form=view_form, add_drop_form=add_drop_form, followup_form=followup_form)

		if add_drop_form.select.data == 'single_class_add':
			followup_form = ClassAddForm()
			return render_template('addDrop.html', view_form=view_form, add_drop_form=add_drop_form, followup_form=followup_form)

		if add_drop_form.select.data == 'single_student_add_class':
			followup_form = AddClassToStudentForm()
			return render_template('addDrop.html', view_form=view_form, add_drop_form=add_drop_form, followup_form=followup_form)

		if add_drop_form.select.data == 'single_teacher_add_class':
			followup_form = AddClassToTeacherForm()
			return render_template('addDrop.html', view_form=view_form, add_drop_form=add_drop_form, followup_form=followup_form)

		if add_drop_form.select.data == 'single_student_remove':
			followup_form = StudentDropForm()
			return render_template('addDrop.html', view_form=view_form, add_drop_form=add_drop_form, followup_form=followup_form)

		if add_drop_form.select.data == 'single_teacher_remove':
			followup_form = TeacherDropForm.new()
			return render_template('addDrop.html', view_form=view_form, add_drop_form=add_drop_form, followup_form=followup_form)

		if add_drop_form.select.data == 'single_class_remove':
			followup_form = ClassDropForm.new()
			return render_template('addDrop.html', view_form=view_form, add_drop_form=add_drop_form, followup_form=followup_form)

		## must fix what is a random Bob doing here!??!?!?!
		## is this superfluous code?
		if add_drop_form.select.data == 'single_student_remove_class':
			followup_form = PickStudent()
			return render_template('addDrop.html', view_form=view_form, add_drop_form=add_drop_form, followup_form=followup_form)
		
		if request.form.get('student'):
			#print('tottenham won')
			name = request.form.get('student')
			#print(name)
			followup_form = PickStudent()
			followup_form.student = name
			drop_form = RemoveStudentClass()
			drop_form.select.choices = [(view_objects_in_entry(Class, Student, name)[i],\
				view_objects_in_entry(Class, Student, name)[i]) \
				for i in range( len(view_objects_in_entry(Class, Student, name)) )]
			return render_template('addDrop.html', view_form=view_form, add_drop_form=add_drop_form, followup_form=followup_form, drop_form=drop_form)

		if request.form.get('remove_class'):
			course = request.form.get('select')
			print(followup_form.student.data)
			name = request.form.get('student')
			flash("{} was dropped from {}'s schedule".format(course, name))
			return render_template('addDrop.html', view_form=view_form, add_drop_form=add_drop_form)

		if request.form.get('add') == 'Add Student':
			if request.form.get('name'):
				name = request.form.get('name')
				add_entry(name, Student)
				flash("{} was added to the student list".format(name))
				return render_template('addDrop.html', view_form=view_form, add_drop_form=add_drop_form)
			else:
				flash("Please enter a name to add.")
				followup_form = StudentAddForm()
				return render_template('addDrop.html', view_form=view_form, add_drop_form=add_drop_form, followup_form=followup_form)

		if request.form.get('add') == 'Add Teacher':
			if request.form.get('name'):
				name = request.form.get('name')
				add_entry(name, Teacher)
				if get_one_entry(name, Class):
					flash('That teacher is already in the system')
					followup_form = TeacherAddForm()
					return render_template('addDrop.html', view_form=view_form, add_drop_form=add_drop_form, followup_form=followup_form)
				flash("{} was added to the teacher list".format(name))
				return render_template('addDrop.html', view_form=view_form, add_drop_form=add_drop_form)
			else:
				flash("Please enter a name to add.")
				followup_form = TeacherAddForm()
				return render_template('addDrop.html', view_form=view_form, add_drop_form=add_drop_form, followup_form=followup_form)

		if request.form.get('add') == 'Add Class':
			if request.form.get('name'):
				name = request.form.get('name')
				if get_one_entry(name, Class):
					flash('That class already exists')
					followup_form = ClassAddForm()
					return render_template('addDrop.html', view_form=view_form, add_drop_form=add_drop_form, followup_form=followup_form)
				add_entry(name, Class)
				flash("{} was added to the class list".format(name))
				return render_template('addDrop.html', view_form=view_form, add_drop_form=add_drop_form)
			else:
				flash("Please enter a name to add.")
				followup_form = TeacherAddForm()
				return render_template('addDrop.html', view_form=view_form, add_drop_form=add_drop_form, followup_form=followup_form)

		if request.form.get('add_class') == 'Add Class':
			#this is add class to student
			if request.form.get('student'):
				name = request.form.get('student')
				course = request.form.get('select')
				conflicts = add_drop_class_to_target(True, course, name, Student)	
				if conflicts == 0:
					flash("{} has a conflicting class in their schedule".format(name))
					followup_form = AddClassToStudentForm()
					return render_template('addDrop.html', view_form=view_form, add_drop_form=add_drop_form, followup_form=followup_form)
				if conflicts == 1:	
					flash("{} already has {} in their schedule".format(name, course))
					followup_form = AddClassToStudentForm()
					return render_template('addDrop.html', view_form=view_form, add_drop_form=add_drop_form, followup_form=followup_form)
				elif not name:
					flash("Please enter a student to add class to.")
					followup_form = AddClassToStudentForm()
					return render_template('addDrop.html', view_form=view_form, add_drop_form=add_drop_form, followup_form=followup_form)	
				flash("{} was added to {}'s schedule".format(course, name))
				return render_template('addDrop.html', view_form=view_form, add_drop_form=add_drop_form)
					

		if request.form.get('add_class') == 'Add Class':
			#fix, there is an issue with double-booking a class for a teacher
			#this is add class to teacher
			if request.form.get('teacher'):
				name = request.form.get('teacher')
				course = request.form.get('select')
				
				conflicts = add_drop_class_to_target(True, course, name, Teacher)	
				if conflicts == 0:
					flash("{} has a conflicting class in their schedule".format(name))
					followup_form = AddClassToTeacherForm()
					return render_template('addDrop.html', view_form=view_form, add_drop_form=add_drop_form, followup_form=followup_form)
				if conflicts == 1:	
					flash("{} already has {} in their schedule".format(name, course))
					followup_form = AddClassToTeacherForm()
					return render_template('addDrop.html', view_form=view_form, add_drop_form=add_drop_form, followup_form=followup_form)
				if conflicts == 2:	
					teacher = view_objects_in_entry(Teacher, Class, course)
					flash("{} already has teacher {} assigned to it".format(course, teacher[0]))
					followup_form = AddClassToTeacherForm()
					return render_template('addDrop.html', view_form=view_form, add_drop_form=add_drop_form, followup_form=followup_form)
				
				flash("{} was added to {}'s schedule".format(course, name))
				return render_template('addDrop.html', view_form=view_form, add_drop_form=add_drop_form)

		if request.form.get('drop') == 'Drop Student':
			if request.form.get('name'):
				name = request.form.get('name')
				print(name)
				if get_one_entry(name, Student) == None:
					flash("{} is not in the student list, check spelling if in doubt.".format(name))
					followup_form = StudentDropForm()
					return render_template('addDrop.html', view_form=view_form, add_drop_form=add_drop_form, followup_form=followup_form)

				remove_entry(name, Student)
				flash("{} was removed from the student list".format(name))
				return render_template('addDrop.html', view_form=view_form, add_drop_form=add_drop_form)
			else:
				flash("Please enter a student name to remove.")
				followup_form = StudentDropForm()
				return render_template('addDrop.html', view_form=view_form, add_drop_form=add_drop_form, followup_form=followup_form)

		if request.form.get('drop_teacher') == 'Drop Teacher':
		
			name = request.form.get('select')
			remove_entry(name, Teacher)
			flash("{} was removed from the teacher list".format(name))
			return render_template('addDrop.html', view_form=view_form, add_drop_form=add_drop_form)
		
		if request.form.get('drop_class') == 'Drop Class':
		
			name = request.form.get('select')
			remove_entry(name, Class)
			flash("{} was removed from the class list".format(name))
			return render_template('addDrop.html', view_form=view_form, add_drop_form=add_drop_form)
			


		if view_form in request.form:
			print("I was here")
			print(view_form.submit.data)
		
		if request.form.get('entry') == "Search Student":
			entry = request.form.get('student')
			print("hey there")
			print(entry)
			error = None
			max_day = None
			rows = None
			if get_one_entry(entry, Student) == None:
				flash("This student is not in the database, check spelling please")
				return render_template('addDrop.html', view_form=view_form, add_drop_form=add_drop_form)
			
			try:
				max_day = max_day_in_week(entry, Student)	
				rows = parsed_rows(entry, Student)
			except:
				flash("{} has no classes scheduled".format(entry))
				return render_template('addDrop.html', view_form=view_form, entry=entry, add_drop_form=add_drop_form)
			return render_template('addDrop.html', view_form=view_form, entry=entry, max_day=max_day, rows=rows, add_drop_form=add_drop_form)


		if request.form.get('search_teacher') == "Search Teacher":
			#let me see if i can make a function to factor this out
			entry = request.form.get('select')
			error = None
			max_day = None
			rows = None
			try:
				max_day = max_day_in_week(entry, Teacher)	
				rows = parsed_rows(entry, Teacher)
			except:
				flash("{} has no classes scheduled".format(entry))
				return render_template('addDrop.html', view_form=view_form, entry=entry, add_drop_form=add_drop_form)
			return render_template('addDrop.html', view_form=view_form, entry=entry, max_day=max_day, rows=rows, add_drop_form=add_drop_form)

		if request.form.get('search_class') == "Search Class":
			
			course = request.form.get('select')
			error = None
			max_day = None
			rows = None
			try:
				max_day = max_day_in_week(course, Class)	
				rows = parsed_rows(course, Class)
			except:
				flash("{} has no sessions scheduled".format(course))
				return render_template('addDrop.html', view_form=view_form, add_drop_form=add_drop_form)
			return render_template('addDrop.html', view_form=view_form, course=course, max_day=max_day, rows=rows, add_drop_form=add_drop_form)


	if view_form.validate_on_submit():
		
		classes = False
		
		if view_form.select.data == 'single_student':
			second_form = StudentForm()
			return render_template('addDrop.html', view_form=view_form, second_form=second_form, add_drop_form=add_drop_form)
		if view_form.select.data == 'single_teacher':
			second_form = TeacherForm.new()	
			return render_template('addDrop.html', view_form=view_form, second_form=second_form, add_drop_form=add_drop_form)
		if view_form.select.data == 'single_class':
			second_form = ClassForm.new()
			return render_template('addDrop.html', view_form=view_form, second_form=second_form, add_drop_form=add_drop_form)
		if view_form.select.data == 'teachers':
			entries = view_all_entries(Teacher)
			return render_template('addDrop.html', view_form=view_form, entries=entries, add_drop_form=add_drop_form)
		if view_form.select.data == 'students':
			entries = view_all_entries(Student)
			return render_template('addDrop.html', view_form=view_form, entries=entries, add_drop_form=add_drop_form)

		if view_form.select.data == 'classes': 	
			classes = True
			teachers = []
			entries = view_all_entries(Class, simple=True)
			for entry in entries:
				try:
					teachers.append(view_objects_in_entry(Teacher, Class, entry.name)[0])
				except:
					teachers.append("No teacher assigned")
			length = len(entries)		
			return render_template('addDrop.html', view_form=view_form, entries=entries, classes=classes, teachers=teachers, length=length, add_drop_form=add_drop_form)

		if view_form.select.data == 'master':
			max_day = max_day_in_week()	
			rows = parsed_rows()
			return render_template('addDrop.html', view_form=view_form, max_day=max_day, rows=rows, add_drop_form=add_drop_form)

	return render_template('addDrop.html', view_form=view_form, add_drop_form=add_drop_form)

@app.route('/modify', methods=['GET', 'POST'])
def modify():

	form = ClassModifyForm()

	if request.method == 'POST':
		print(request.form)

		if request.form.get('modify_class') == "Modify Class":
				
			course = request.form.get('select')
			error = None
			max_day = None
			rows = None
			session_form = SessionView()

			try:
				max_day = max_day_in_week(course, Class)	
				rows = parsed_rows(course, Class)
			except:
				return render_template('modify.html', form=form, session_form=session_form)
			return render_template('modify.html', form=form, session_form=session_form, course=course, max_day=max_day, rows=rows)

	#if form.validate_on_submit():
		
	#	classes = False

	#	if form.select.data == 'single_class':
	#		second_form = ClassModifyForm()
	#		return render_template('modify.html', form=form, second_form=second_form)
	
	

	return render_template('modify.html', form=form)

@app.route('/setTime', methods=['GET', 'POST'])
def setTime():

	form = CreateSession()


	if request.method == 'POST':
		print(request.form)

		if request.form.get('see_times') == "See times (if removing)":
				
			course = request.form.get('select')
			if view_all_class_sessions_schedule(course, check_empty=True):
				session_form = SessionViewDrop()
				session_form.sessions.choices=[(view_all_class_sessions_schedule(course, dropdown=True)[i], view_all_class_sessions_schedule(course, dropdown=True)[i]) for i in range( len(view_all_class_sessions_schedule(course, dropdown=True)) )]

			else:
				flash("That class has no set sessions yet...")
				return render_template('setTime.html', form=form)
			

			return render_template('setTime.html', form=form, session_form=session_form)

		if request.form.get('confirm_add_button'):
			flash("Session was added")
			test = request.form.get("start-hour")
			print(test)
			print("the sun is out")

	#if form.validate_on_submit():
		
	#	classes = False

	#	if form.select.data == 'single_class':
	#		second_form = ClassModifyForm()
	#		return render_template('modify.html', form=form, second_form=second_form)
	
	

	return render_template('setTime.html', form=form)
	




if __name__ == '__main__':
	app.run()

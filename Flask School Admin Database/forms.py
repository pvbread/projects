
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from queries import *

class ViewForm(FlaskForm):	
	select = SelectField(u'View rosters and schedules', render_kw={'id':'select-view'},\
			choices=[('single_student', 'View Specific Student'), ('single_teacher', 'View Specific Teacher'),\
			('single_class', 'View Specific Class'), ('students', 'View All Students'), \
			('classes', 'View All Classes'), ('teachers', 'View All Teachers'), ('master', 'Master Schedule')])
	submit = SubmitField('View', render_kw={'id':'view-button'})

class ModifyForm(FlaskForm):	
	select = SelectField(u'Modify rosters and schedules', render_kw={'id':'select-view'},\
			choices=[('single_student', 'Modify Student'), ('single_teacher', 'Modify Teacher'),\
			('single_class', 'Modify Class'), \
			('master', 'View Master Schedule')])
	submit = SubmitField('Modify', render_kw={'id':'modify-button'})
	
class StudentForm(FlaskForm):
	
	student = StringField(u'Student Name')
	entry = SubmitField('Search Student')

class StudentModifyForm(FlaskForm):
	
	student = StringField(u'Student Name')
	entry = SubmitField('Modify Student')

class AddDropForm(FlaskForm):
	select = SelectField(u'Add or Drop Student/Teacher/Class', render_kw={'id':'addDrop-view'},\
			choices=[('single_student_add', 'Add a Student'), ('single_teacher_add', 'Add a Teacher'),\
			('single_class_add', 'Add a Class'), ('single_student_add_class', 'Assign a Class to a Student'),\
			('single_teacher_add_class', 'Assign a Class to a Teacher'),\
			('single_student_remove', 'Remove a Student'), ('single_teacher_remove', 'Remove a Teacher'),\
			('single_class_remove', 'Remove a Class'), ('single_student_remove_class', "Remove a Student's Class"),\
			('single_teacher_remove_class', "Remove a Teacher's Class")])
	add_drop_submit = SubmitField('Select', render_kw={'id':'select-button'})

class StudentAddForm(FlaskForm):

	name = StringField('Student to Add')
	add = SubmitField('Add Student')

class TeacherAddForm(FlaskForm):
	name = StringField('Teacher to Add')
	add = SubmitField('Add Teacher')

class ClassAddForm(FlaskForm):
	name = StringField('Class to Add')
	add = SubmitField('Add Class')

class StudentDropForm(FlaskForm):
	name = StringField('Student to Drop')
	drop = SubmitField('Drop Student')


####

class TeacherForm(FlaskForm):
	#print([(view_all_entries(Teacher)[i], view_all_entries(Teacher)[i]) for i in range( len(view_all_entries(Teacher)) )])
	select = SelectField(u'Teacher Name', choices=[(view_all_entries(Teacher)[i], view_all_entries(Teacher)[i]) for i in range( len(view_all_entries(Teacher)) )])
	search_teacher = SubmitField('Search Teacher')

	@classmethod
	def new(cls):
		form = cls()
		form.select.choices = [(view_all_entries(Teacher)[i], view_all_entries(Teacher)[i]) for i in range( len(view_all_entries(Teacher)) )]
		return form

class TestTeacherForm(FlaskForm):
	#print([(view_all_entries(Teacher)[i], view_all_entries(Teacher)[i]) for i in range( len(view_all_entries(Teacher)) )])
	select = SelectField(u'Teacher Name', choices=[(view_all_entries(Teacher)[i], view_all_entries(Teacher)[i]) for i in range( len(view_all_entries(Teacher)) )])
	search_teacher = SubmitField('Search Teacher')


class TeacherModifyForm(FlaskForm):

	select = SelectField(u'Teacher Name', choices=[(view_all_entries(Teacher)[i], view_all_entries(Teacher)[i]) for i in range( len(view_all_entries(Teacher)) )])
	modify_teacher = SubmitField('Modify Teacher')

class ClassForm(FlaskForm):

	select = SelectField(u'Class Name', choices=[(view_all_entries(Class, simple=True)[i], view_all_entries(Class, simple=True)[i]) for i in range( len(view_all_entries(Class, simple=True)) )])
	search_class = SubmitField('Search Class')

	@classmethod
	def new(cls):
		form = cls()
		form.select.choices = [(view_all_entries(Class, simple=True)[i], view_all_entries(Class, simple=True)[i]) for i in range( len(view_all_entries(Class, simple=True)) )]
		return form

class ClassModifyForm(FlaskForm):

	select = SelectField(u'Class Name', choices=[(view_all_entries(Class, simple=True)[i], view_all_entries(Class, simple=True)[i]) for i in range( len(view_all_entries(Class, simple=True)) )])
	modify_class = SubmitField('Modify Class')

class TeacherDropForm(FlaskForm):

	select = SelectField(u'Teacher Name', choices=[(view_all_entries(Teacher)[i], view_all_entries(Teacher)[i]) for i in range( len(view_all_entries(Teacher)) )])
	drop_teacher = SubmitField('Drop Teacher')

	@classmethod
	def new(cls):
		form = cls()
		form.select.choices = [(view_all_entries(Teacher)[i], view_all_entries(Teacher)[i]) for i in range( len(view_all_entries(Teacher)) )]
		return form

class ClassDropForm(FlaskForm):

	select = SelectField(u'Class Name', choices=[(view_all_entries(Class, simple=True)[i], view_all_entries(Class, simple=True)[i]) for i in range( len(view_all_entries(Class, simple=True)) )])
	drop_class = SubmitField('Drop Class')

	@classmethod
	def new(cls):
		form = cls()
		form.select.choices = [(view_all_entries(Class, simple=True)[i], view_all_entries(Class, simple=True)[i]) for i in range( len(view_all_entries(Class, simple=True)) )]
		return form	

class AddClassToStudentForm(FlaskForm):

	select = SelectField(u'Class Name', choices=[(view_all_entries(Class, simple=True)[i], view_all_entries(Class, simple=True)[i]) for i in range( len(view_all_entries(Class, simple=True)) )])
	student = StringField('Enter Student to Give Class To')
	add_class = SubmitField('Add Class')

class AddClassToTeacherForm(FlaskForm):

	select = SelectField(u'Class Name', choices=[(view_all_entries(Class, simple=True)[i], view_all_entries(Class, simple=True)[i]) for i in range( len(view_all_entries(Class, simple=True)) )])
	teacher = SelectField(u'Select Teacher to Give Class To', choices=[(view_all_entries(Teacher)[i], view_all_entries(Teacher)[i]) for i in range( len(view_all_entries(Teacher)) )])
	add_class = SubmitField('Add Class')

class PickStudent(FlaskForm):
	student = StringField('Enter Student to Remove Class From')
	remove_class = SubmitField("Select student")

class RemoveStudentClass(FlaskForm):

	select = SelectField(u'Class Name')
	remove_class = SubmitField('Remove Class')

class RemoveTeacherClass(FlaskForm):
	pass

class SessionViewDrop(FlaskForm):
	sessions = SelectField(u'Class Session')
	drop_session = SubmitField('Confirm Drop Session')

class CreateSession(FlaskForm):
	select = SelectField(u'Class Name', choices=[(view_all_entries(Class, simple=True)[i], view_all_entries(Class, simple=True)[i]) for i in range( len(view_all_entries(Class, simple=True)) )])

	@classmethod
	def new(cls):
		form = cls()
		form.select.choices = [(view_all_entries(Class, simple=True)[i], view_all_entries(Class, simple=True)[i]) for i in range( len(view_all_entries(Class, simple=True)) )]
		return form	

	see_times = SubmitField('See times (if removing)')

	#needs to check for time classhes

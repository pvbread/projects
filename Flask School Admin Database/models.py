from main import db

registrations = db.Table('registrations', 
				db.Column('student_id', db.Integer, db.ForeignKey('students.id')),
				db.Column('class_id', db.Integer, db.ForeignKey('classes.id')),
				db.Column('teacher_id', db.Integer, db.ForeignKey('teachers.id')),
				db.UniqueConstraint('student_id', 'class_id', name='UC_student_id_class_id'),
				db.UniqueConstraint('teacher_id', 'class_id', name='UC_teacher_id_class_id')
				)

daysOfWeek = db.Table('daysOfWeek', 
				db.Column('id', db.Integer, db.Sequence('daysOfWeek_id_seq'), primary_key=True),
				db.Column('day', db.String(12))
				)
				

class ClassHours(db.Model):
	__tablename__ = 'class_hours'

	id = db.Column(db.Integer, db.Sequence('class_hours_id_seq'), primary_key=True)
	class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
	daysOfWeek_id = db.Column(db.Integer, db.ForeignKey('daysOfWeek.id'))
	start_hour = db.Column(db.Integer)
	start_minute = db.Column(db.Integer)
	end_hour = db.Column(db.Integer)
	end_minute = db.Column(db.Integer)
	room = db.Column(db.String(50))


	def __repr__(self):
		return "%s, %s, %s, %s, %s, %s" % (self.daysOfWeek_id, self.start_hour,\
						self.start_minute, self.end_hour, self.end_minute,\
						self.room)

class Student(db.Model):
	__tablename__ = 'students'

	id = db.Column(db.Integer, db.Sequence('student_id_seq'), primary_key=True)
	name = db.Column(db.String(50))
	email = db.Column(db.String(120), nullable=True)
	classes = db.relationship('Class', secondary=registrations,
							backref=db.backref('students', lazy='dynamic'),
							lazy="dynamic")

	def __repr__(self):
		return "%s" % (self.name)

class Teacher(db.Model):
	#
	__tablename__ = 'teachers'

	id = db.Column(db.Integer, db.Sequence('teacher_id_seq'), primary_key=True)
	name = db.Column(db.String(50), unique=True)
	email = db.Column(db.String(120), nullable=True)
	classes = db.relationship('Class', secondary=registrations,
							backref=db.backref('teachers', lazy='dynamic'),
							lazy="dynamic")

	def __repr__(self):
		return "%s" % (self.name)

class Class(db.Model):
	__tablename__ = 'classes'

	id = db.Column(db.Integer, db.Sequence('class_id_seq'), primary_key=True) ## the sequence? is this right? check docs
	name = db.Column(db.String(50), unique=True)
	abbreviated = db.Column(db.String(50), nullable=True)
	is_private = db.Column(db.Boolean, nullable=True)
	class_hours = db.relationship("ClassHours")

	def __repr__(self):
		return "%s" % (self.name)



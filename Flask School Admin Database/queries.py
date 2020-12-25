from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *

engine = create_engine('sqlite:///data.sqlite', connect_args={'check_same_thread': False})
Session = sessionmaker(bind=engine)
Session.configure(bind=engine) 
dbsession = Session()

def view_all_entries(kind, simple=False, parse=False):

	entries = []
	for entry in dbsession.query(kind):
		entries.append(entry)
		if simple==False and kind == Class:
			entries.append(entry.teachers.all())

	if parse == True:
		
		parsed_list = []

		if kind == Class:
			#classes = {"classes":[]}
			classes = {}
			for i in range(len(entries)-2):
				if i % 2 == 0:
					#classes["classes"].append({entries[i].name: entries[i+1][0].name})
					classes[entries[i].name] = entries[i+1][0].name

			return classes
		else:
			for entry in entries:
				parsed_list.append(entry.name)

		dbsession.commit()
		return parsed_list


	dbsession.commit()

	return entries



def time_is_earlier(this_start_hour, this_start_minute,\
				existing_start_hour, existing_start_minute):
	
	valid = True
	
	this_start_minutes= time_to_minutes_start(this_start_hour,\
						this_start_minute)
	existing_start_minutes = time_to_minutes_start(existing_start_hour,\
						existing_start_minute)

	if this_start_minutes < existing_start_minutes:
		pass
	else:
		valid = False

	return valid

def get_class_name(search_id):

	name = None
	
	for course in dbsession.query(Class).\
				filter(Class.id==search_id):
		name = course.name

	dbsession.commit()

	return name

def view_objects_in_entry(target, entry, entry_name):
	#confirmed works in code, try in page
	results = []
	entry_target = None

	if entry_name == '':
		return "Please enter text in the text-field if searching"

	for i in dbsession.query(entry).\
				filter(entry.name==entry_name):
		entry_target = i

	if entry_target == None:
		dbsession.commit()
		return "{} is not in file as a {}, please check spelling".format(entry_name, target.name)

	if entry == Class and target == Student:
		for i in entry_target.students.all():
			results.append(i.name)
	if entry == Class and target == Teacher:
		for i in entry_target.teachers.all():
			results.append(i.name)
	if target == Class:
		for i in entry_target.classes.all():
			results.append(i.name)

	dbsession.commit()

	return results


def view_entry_schedule(entry, kind, simple=False):
	#it works, maybe format the return somehow
	#last two numbers signify the max classes in a single day
	# and the amount of sessions total, respectively

	#works

	schedule = []
	entry_target = None

	if entry == '':
		return "Please enter text in the text-field if searching"

	for i in dbsession.query(kind).\
				filter(kind.name==entry):
		entry_target = i

	if entry_target == None:
		dbsession.commit()
		return "{} is not in file as a {}, please check spelling".format(entry_target, kind.name)

	for course in entry_target.classes.all():
		for session in view_all_class_sessions(str(course)):
			schedule.append(session)

	if schedule == []:
		dbsession.commit()
		return None

	if simple == True:
		return schedule
	dbsession.commit()

	day_count = {}
	course_names = []
	teacher_names = []
	organized_schedule = organize_schedule(schedule)
	

	for session in organized_schedule:
		try:
			day_count[session.daysOfWeek_id] += 1
		except:
			day_count[session.daysOfWeek_id] = 1
		course = get_class_name(session.class_id)
		course_names.append(course)
		teacher_names.append(view_objects_in_entry(Teacher, Class, course))


	max_value = max(day_count.values())
	

	return organized_schedule, course_names, teacher_names, max_value, len(schedule)

def view_master_schedule_days():
	
	courses = []
	schedule = []
	
	for course in view_all_entries(Class):
		courses.append(course)
	
	for course in courses:
		for session in view_all_class_sessions(str(course)):
			schedule.append(session)


	day_count = {}
	course_names = []
	teacher_names = []
	organized_schedule = organize_schedule(schedule)

	for session in organized_schedule:
		try:
			day_count[session.daysOfWeek_id] += 1
		except:
			day_count[session.daysOfWeek_id] = 1
		course = get_class_name(session.class_id)
		course_names.append(course)
		teacher_names.append(view_objects_in_entry(Teacher, Class, course))


	max_value = max(day_count.values())
	
	return organized_schedule, course_names, teacher_names, max_value, len(schedule)

def view_list_schedule(name, kind):
	for i in view_entry_schedule(name, kind):
		print(i)

def organize_schedule(schedule):
	
	'''
	organized_schedule = []
	
	week = []
	for i in range(7):
		week.append([])
	for session in schedule:
		week[session.daysOfWeek_id-1].append(time_to_minutes_start\
								(session.start_hour, session.start_minute))

	for day in week:
		day.sort()

	for day in week:
		for slot in day:
			for session in schedule:
				try:
					if slot == time_to_minutes_start\
					(session.start_hour, session.start_minute)\
					and session not in organized_schedule:
						organized_schedule.append(session)
				except:
					pass
	'''
	organized_schedule = []
	week = {}
	for i in range(7):
		week[i+1]=[]

	for session in schedule:
		week[session.daysOfWeek_id].append(time_to_minutes_start\
								(session.start_hour, session.start_minute))

	for day in week.keys():
		week[day].sort()

	for day in week.keys():
		for slot in week[day]:
			for session in schedule:
				if session.daysOfWeek_id == day:
					if slot == time_to_minutes_start\
							(session.start_hour, session.start_minute)\
							and session not in organized_schedule:
						organized_schedule.append(session)

	return organized_schedule

def get_nth_row(row, name=None, kind=None):
	#all sessions
	if kind == Class:
		sessions = organize_schedule(view_all_class_sessions_schedule(name, simple=True))
	elif name:
		sessions = organize_schedule(view_entry_schedule(name, kind, simple=True))
	else:
		sessions = organize_schedule(view_all_sessions())
	week = {}
	row_data = []

	for i in range(1, 8):
		week[i]=[]

	
	for session in sessions:
		week[session.daysOfWeek_id].append(session)
		
	for day in week.keys():
		try:
			row_data.append(week[day][row])
		except:
			pass
	
	return row_data

def get_organized_rows(name=None, kind=None):
	rows = {}
	max_day = max_day_in_week(name, kind)
	for row in range(max_day):
		rows[row] = get_nth_row(row, name, kind)

	return rows

def parsed_rows(name=None, kind=None):
	rows = get_organized_rows(name, kind)
	filtered = {}
	for row in rows:
		filtered[row] = {}

	for row in rows:
		for session in rows[row]:
			filtered[row] = {}

	for row in rows:
		for session in rows[row]:
			class_name = get_class_name(session.class_id)
			filtered[row][rows[row].index(session)]=[]
			filtered[row][rows[row].index(session)].append(session)
			filtered[row][rows[row].index(session)].append(view_objects_in_entry(Teacher, Class, class_name)[0])
			filtered[row][rows[row].index(session)].append(class_name)
			
	return filtered

def add_drop_class_to_target(add, course, name, kind):
	#to-do
	#auto generate dropdown of classes to add

	## tested, works
	#change class times can create potential conflicts
	target_name = None
	class_name = None

	for i in dbsession.query(kind).\
				filter(kind.name==name):
		target_name = i

	for i in dbsession.query(Class).\
					filter(Class.name==course):
		class_name = i

	if class_name and target_name:
		
		if add:
		
			if name not in view_objects_in_entry(kind, Class, course):
				valid = True
				
				if view_objects_in_entry(Class, kind, name) != [] :
					## gotta fix this 191
					schedule = view_entry_schedule(name, kind, simple=True)

					## still must fix # added a new thing check
					if not schedule:
						pass
					else:
						for existing in schedule:
							for session in view_all_class_sessions(course):
								#sets earliest time
								if existing.daysOfWeek_id == session.daysOfWeek_id:
									if time_does_not_conflict(existing.start_hour,\
									existing.start_minute, existing.end_hour,\
									existing.end_minute, session.start_hour,\
									session.start_minute, session.end_hour,\
									session.end_minute) == False:
										valid = False
				
				if kind == Teacher:
					if view_objects_in_entry(Teacher,Class, course):
						valid = False
						dbsession.commit()
						#class already has a teacher
						return 2
				
				if valid:
					target_name.classes.append(class_name)
					dbsession.add(target_name)
					dbsession.commit()
					return "{} added to {}'s schedule".format(class_name.name, target_name.name)
				else:
					dbsession.commit()
					#conflicting schedule
					return 0
			else:
				dbsession.commit()
				#already in class
				return 1
		
		else:
			dbsession.commit()

			if name in view_objects_in_entry(kind, Class, course):
				target_name.classes.remove(class_name)
				
				return "{} removed from {}'s schedule".format(class_name.name, target_name.name)
			else:
				#is not in this class
				return 2		

	dbsession.commit()

	if not target_name:
		return "No such {}, please check spelling".format(str(kind))
	if not class_name:

		return "No such class, please check spelling" # maybe also flash it

def add_entry(entry, kind):

	#tested works!
	if entry == '':
		return "Name-field is empty, try again"

	if entry not in view_all_entries(kind):
		new_entry = kind(name=entry)
		dbsession.add(new_entry)
		dbsession.commit()
		return "{} added".format(new_entry)
	else:
		dbsession.commit()
		return "{} is already in file".format(entry)

def remove_entry(entry, kind):

	#tested works!
	to_remove = None
	
	for i in dbsession.query(kind).\
		filter(kind.name==entry):
		to_remove = i

	if to_remove == None:
		dbsession.commit()
		return "{} not in database, check spelling and try again".format(entry)
	
	dbsession.delete(to_remove)
	dbsession.commit()

	return "{} removed from student list".format(entry)

def modify_entry_name(kind, name, new_name):
	#tested, works!
	entry = None
	
	for i in dbsession.query(kind).\
					filter(kind.name==name):
		entry = i

	if entry == None:
		dbsession.commit()
		return "{} not in file, check spelling and try again".format(name)

	entry.name = new_name
	dbsession.add(entry)
	dbsession.commit()

	return "{}'s new name is now: {}".format(name, new_name)	

# this could potentially stay
def modify_class_abbreviation(name, new_name):
	course = None
	for item in dbsession.query(Class).\
					filter(Class.name==name):
		course = item

	if course == None:
		dbsession.commit()
		return "{} not in database, check spelling and try again".format(name)

	course.abbreviated = new_name
	dbsession.add(course)
	dbsession.commit()
	return "{}'s new abbreviation is now: {}".format(name, new_name)

def is_class_in_day(course, day):
	return day in view_all_class_days(course)


def get_class_id(course):
	id = None
	for item in dbsession.query(Class).filter(Class.name==course):
		id = item.id

	return id

def get_class_name(id):
	
	name = ''

	for item in dbsession.query(Class).filter(Class.id==id):
		name = item.name

	return name

def set_time(course, day, start_hour, start_minute, end_hour, end_minute, room):
	# works!
	start_minutes, end_minutes = time_to_minutes(start_hour, start_minute, end_hour, end_minute)
	

	if type(day) != int:
		day = get_day_id(day)

	if start_minutes > end_minutes:
		return "It seems the start-time selected is after the end-time, please check the time and try again"

	#that middle return statement in view_all_classdays might be trouble
	# maybe need to adjust or make helper function

	#this logic might serve better inside its own function
	#particularly when we do modify session time
	#high candidate for refactor
	valid = True
	for session in view_all_sessions():
		if room == session.room and day == session.daysOfWeek_id:
			if time_does_not_conflict(start_hour, start_minute, end_hour, end_minute,\
				session.start_hour, session.start_minute,\
				session.end_hour, session.end_minute):
				pass
			else:
				valid = False
				dbsession.commit()
				return "There's conflict with {}' session: {}".format(course, session)


	time = ClassHours(class_id=get_class_id(course),\
		daysOfWeek_id=day,\
		start_hour=start_hour, start_minute=start_minute, end_hour=end_hour, end_minute=end_minute, room=room)

	dbsession.add(time)
	dbsession.commit()
	

	return "New time for {0}: {1}, START: {2}:{3}-{4}:{5} Room: {6}".format(course, get_day(day), start_hour, start_minute, end_hour, end_minute, room)

def delete_time(class_hours_id):
	# so this goes by session id, interesting
	to_remove = None

	for i in dbsession.query(ClassHours).\
				filter(ClassHours.id==class_hours_id):
		to_remove = i

	if to_remove == None:
		dbsession.commit()
		return "Class is not in file, please check spelling if it is"

	confirmation = to_remove

	dbsession.delete(to_remove)
	dbsession.commit()

	return "Deleted entry: {}".format(confirmation)

def view_all_class_sessions(course):
	if course == '':
		return "Please enter text in the text-field if searching"

	sessions = []
	for i in dbsession.query(ClassHours).\
				filter(ClassHours.class_id==get_class_id(course)):
		sessions.append(i)

	if sessions == None:
		dbsession.commit()
		return "Class is not in file, please check spelling if it is"

	dbsession.commit()

	return sessions	

def view_all_class_sessions_schedule(course, simple=False, dropdown=False, check_empty=False):

	if course == '':
		return "Please enter text in the text-field if searching"

	sessions = []
	for i in dbsession.query(ClassHours).\
				filter(ClassHours.class_id==get_class_id(course)):
		sessions.append(i)

	if sessions == None or sessions == []:
		dbsession.commit()
		if check_empty == True:
			return None
		return "Class is not in file, please check spelling if it is"

	dbsession.commit()

	if simple:
		return sessions

	if dropdown:
		organized_sessions = organize_schedule(sessions)
		organized_parsed = []
		days = ["",'Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

		for session in organized_sessions:	
			day = days[session.daysOfWeek_id]
			if session.start_minute == 0:
				start_minute = "00"
			else:
				start_minute = session.start_minute
			if session.end_minute == 0:
				end_minute = "00"
			else:
				end_minute = session.end_minute
			parsed_string = "{} {}:{}-{}:{} {}".format(day,session.start_hour,start_minute,session.end_hour,end_minute,session.room)
			organized_parsed.append(parsed_string)

		return organized_parsed
		#return "{} {}:{}-{}:{} {}".format(sessions[0],sessions[1],sessions[2],sessions[3],sessions[4],sessions[5])

	organized_sessions = organize_schedule(sessions)

	day_count = {}
	course_names = []
	teacher_names = []

	for session in organized_sessions:
		try:
			day_count[session.daysOfWeek_id] += 1
		except:
			day_count[session.daysOfWeek_id] = 1
		course = get_class_name(session.class_id)
		course_names.append(course)
		teacher_names.append(view_objects_in_entry(Teacher, Class, course))

	max_value = max(day_count.values())

	##think about the formatting of the result

	return organized_sessions, course_names, teacher_names, max_value, len(sessions)

def view_all_sessions():
	## tested, works
	sessions = []
	for i in dbsession.query(ClassHours):
		sessions.append(i)

	if sessions == None:
		dbsession.commit()
		return "No sessions is not in file"

	dbsession.commit()

	return sessions


def max_day_in_week(name=None, kind=None):
	day_count={}
	for i in range(1,8):
		day_count[i]=0

	if kind == Class:
		for session in organize_schedule(view_all_class_sessions_schedule(name, simple=True)):
			day_count[session.daysOfWeek_id] += 1
		return max(day_count.values())
	elif name:
		for session in organize_schedule(view_entry_schedule(name, kind, simple=True)):
			day_count[session.daysOfWeek_id] += 1
		return max(day_count.values())

	else:
		for session in view_all_sessions():
			day_count[session.daysOfWeek_id] += 1

	return max(day_count.values())


def delete_session(course, session_id):

	sessions = []
	for i in dbsession.query(ClassHours).\
				filter(ClassHours.class_id==get_class_id(course)):
		sessions.append(i)

	if sessions == None:
		dbsession.commit()
		return "Class is not in file, please check spelling if it is"

	session_to_remove = sessions[session_id]
	
	dbsession.delete(sessions[session_id])

	dbsession.commit()

	return "{} dropped from {} sessions".format(session_to_remove, course)


def modify_session(course, session_id, new_day, new_start_hour, new_start_minute,\
					new_end_hour, new_end_minute, new_room):
	
	#tested

	start_minutes, end_minutes = time_to_minutes(new_start_hour, new_start_minute, new_end_hour, new_end_minute)
	

	if start_minutes > end_minutes:
		return "It seems the start-time selected is after the end-time, please check the time and try again"

	sessions = []
	for i in dbsession.query(ClassHours).\
				filter(ClassHours.class_id==get_class_id(course)):
		sessions.append(i)

	target_session = sessions[session_id]

	valid = True
	for session in view_all_sessions():
		if new_room == session.room and get_day_id(new_day) == session.daysOfWeek_id:
			if time_does_not_conflict(new_start_hour, new_start_minute, new_end_hour, new_end_minute,\
				session.start_hour, session.start_minute,\
				session.end_hour, session.end_minute):
				pass
			else:
				valid = False
				dbsession.commit()
				return "There's conflict with {}' session: {}".format(course, session)


	target_session.daysOfWeek_id = get_day_id(new_day)
	target_session.start_hour = new_start_hour
	target_session.start_minute = new_start_minute
	target_session.end_hour = new_end_hour
	target_session.end_minute = new_end_minute
	target_session.room = new_room

	dbsession.add(target_session)
	dbsession.commit()

	return "New session info: {}".format(target_session)

############## Helper functions

def get_day(day_id):
	#works
	day_id = int(day_id)
	with engine.connect() as con:
		result = con.execute("SELECT * FROM daysOfWeek")

		rows = []
		for row in result:
			rows.append(row)

		day_id -= 1

		dbsession.commit()

		return rows[day_id].day

def get_day_id(day):
	#think about this

	with engine.connect() as con:
		result = con.execute("SELECT * FROM daysOfWeek")

		rows = []
		target = None
		for row in result:
			rows.append(row)

		for i in rows:
			if i[1] == day:
				target = i[0]

		dbsession.commit()

		return target

def parse_class_schedule(sessions):

	schedule = {}
	for session in sessions:
		schedule[session.id] = []
	#review if i need this at all
	for session in sessions:
		schedule[session.id].append(get_day(session.daysOfWeek_id))
		schedule[session.id].append(session.start_hour)
		schedule[session.id].append(session.start_minute)
		schedule[session.id].append(session.end_hour)
		schedule[session.id].append(session.end_minute)
		schedule[session.id].append(session.room)

	parsed_list = []
	
	parsed_strings = []
	
	for values in schedule.values():	
		parsed_list.append(values)
		
	for i in parsed_list:
		if i[2] == 0:
			i[2] = "00"
		if i[4] == 0:
			i[4] = "00"
		parsed_strings.append([i[0]+ " " + str(i[1]) + ":" + \
			str(i[2]) + "-" + str(i[3]) + ":" + str(i[4]) + " " + i[5]])


	return parsed_strings


def time_to_minutes(start_hour, start_minute, end_hour, end_minute):
	start_minutes = (start_hour * 60) + start_minute
	end_minutes = (end_hour * 60) + end_minute

	return start_minutes, end_minutes

def time_to_minutes_start(start_hour, start_minute):
	start_minutes = (start_hour * 60) + start_minute
	return start_minutes


def time_does_not_conflict(this_start_hour, this_start_minute, this_end_hour, this_end_minute,\
				existing_start_hour, existing_start_minute, existing_end_hour, existing_end_minute):
	
	## tested, works
	valid = True
	
	this_start_minutes, this_end_minutes = time_to_minutes(this_start_hour,\
						this_start_minute, this_end_hour, this_end_minute)
	existing_start_minutes, existing_end_minutes = time_to_minutes(existing_start_hour,\
						existing_start_minute, existing_end_hour, existing_end_minute)

	if this_start_minutes < existing_start_minutes and this_end_minutes <= existing_start_minutes or \
		this_start_minutes >= existing_end_minutes:
		pass
	else:
		valid = False

	return valid


def get_one_entry(entry, kind):
	if kind == ClassHours:
		for item in dbsession.query(ClassHours).\
				filter(ClassHours.id==entry):
			one_entry = item
		dbsession.commit()
		return one_entry


	one_entry = None
	for item in dbsession.query(kind).\
				filter(kind.name==entry):
		one_entry = item

	dbsession.commit()

	return one_entry
#

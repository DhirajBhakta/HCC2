from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from . import login_manager 
from flask import current_app


import datetime



class USER():
	#this name attribute shall not be put into DB.!!
	name = None

	ID = None
	emailID = None
	passwordHash = None
	usertype = {1:"Student",2:"Employee"}
	idtype   = {1:"rollno" ,3:"emp_id"}
	

	def generate_confirmation_token(self, expiration=3600):
		s = Serializer(current_app.config['SECRET_KEY'], expiration)
		return s.dumps({'confirm': self.ID})

	#data stored into object to be later put into Database
	def storeData(self,name,id,email,password):
		self.name = name
		self.ID = id
		self.emailID = email
		self.passwordHash =  generate_password_hash(password)
	    

	#Database to object
	def storeTuple(self,cursor,id):
		cursor.execute("SELECT * FROM User WHERE id='"+id+"'")
		tuple = cursor.fetchone()
		self.ID = tuple[0]
		self.emailID = tuple[1]
		self.passwordHash = tuple[2]

	#overloaded
	def storeTuple(self,tuple):
		self.ID = tuple[0]
		self.emailID = tuple[1]
		self.passwordHash = tuple[2]


	def checkIfExistsInDB(cursor,patientType,id,email):
		cursor.execute("SELECT * FROM Student WHERE rollno=%s AND email_id=%s",(id,email))
		return cursor.fetchone()


	def insertIntoDB(self,cursor):
		cursor.execute("INSERT INTO User VALUES('"+self.ID+"','"+self.emailID+"','"+self.passwordHash+"')")
	
	def checkIfIDExists(cursor,id):
		cursor.execute("SELECT * FROM User WHERE id='"+id+"'")
		tuple = cursor.fetchone()
		if tuple is None:
			return None
		user = USER()
		user.storeTuple(tuple)
		return user

		

	def checkIfEmailExists(cursor,email):
		cursor.execute("SELECT * FROM User WHERE email_id='"+email+"'")
		return cursor.fetchone()


	def verify_password(self,password):
		return check_password_hash(self.passwordHash,password)


	def __repr__(self):
		return '<User %r>' %self.ID












class STUDENT(UserMixin):
	rollno = None
	name = None
	DOB = None
	sex = None
	phno = None
	email = None
	guardianPhno = None
	locAddr = None
	permAddr = None
	patientID = None
	dept = None
	course = None
	blood = None

	def get_id(self):
		return str(self.patientID)

	#Database to object
	def storeTuple(self,cursor,rollno):
		cursor.execute("SELECT * FROM Student WHERE rollno='"+rollno+"'")
		tuple = cursor.fetchone()
		
		self.rollno 	  = tuple[0]
		self.name   	  = tuple[1]
		self.DOB		  = tuple[2]
		self.sex 		  = tuple[3]
		self.phno   	  = tuple[4]
		self.email  	  = tuple[5]
		self.guardianPhno = tuple[6]
		self.locAddr      = str(tuple[7])
		self.permAddr	  = str(tuple[8])
		self.patientID    = tuple[9]
		
		cursor.execute("SELECT dept_name FROM Department WHERE dept_id='"+str(tuple[10])+"'")
		tupledept   = cursor.fetchone()
		cursor.execute("SELECT course_name FROM Course WHERE course_id='"+str(tuple[11])+"'")
		tuplecourse = cursor.fetchone()

		self.dept   = tupledept[0]
		self.course = tuplecourse[0]
		self.blood  = tuple[12]









@login_manager.user_loader
def load_user(patientID):
    return STUDENT.get(patientID)


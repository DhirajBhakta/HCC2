from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from . import login_manager 
from flask import current_app
from . import mysql


import datetime



class USER(UserMixin):
	#this name attribute shall not be put into DB.!!
	name = None

	ID = None
	emailID = None
	passwordHash = None
	usertype = {1:"Student",2:"Employee"}
	idtype   = {1:"rollno" ,3:"emp_id"}


	def get_id(self):
		return str(self.ID)

	def get(ID):
		cursor = mysql.connect().cursor()
		loggedInUser = USER()
		loggedInUser.storeTuple(cursor,"id",ID)
		return loggedInUser
	
    #----token related--------------------------------------------------
	def generate_confirmation_token(self, expiration=3600):
		s = Serializer(current_app.config['SECRET_KEY'], expiration)
		return s.dumps({'confirm': self.ID})

	def confirm(self, token,cursor):
		s = Serializer(current_app.config['SECRET_KEY'])
		data = s.loads(token)
		USER.confirmUser(self,cursor) 

	def getUserIDFromToken(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		data = s.loads(token)
		return data.get('confirm')
	#-------------------------------------------------------------------	

	#data stored into object to be later put into Database
	def storeData(self,name,id,email,password):
		self.name = name
		self.ID = id
		self.emailID = email
		self.passwordHash =  generate_password_hash(password)
	    

	#Database to object
	def storeTuple(self,cursor,column,value):
		cursor.execute("SELECT * FROM User WHERE "+column+" = %s",(value,))
		tuple = cursor.fetchone()
		if tuple is None:
			return False
		self.ID = tuple[0]
		self.passwordHash = tuple[1]
		self.emailID = tuple[2]
		return True

	def checkIfExistsInDB(cursor,patientType,id,email):
		cursor.execute("SELECT * FROM Student WHERE rollno=%s AND email_id=%s",(id,email))
		return cursor.fetchone()


	def insertIntoDB(self,cursor):
		userIfPresent = USER.checkIfIDExists(cursor,self.ID)
		if (userIfPresent is not None) and (not userIfPresent.isConfirmed(cursor)):
			cursor.execute("DELETE FROM User WHERE id=%s",(userIfPresent.ID,))
		cursor.execute("INSERT INTO User VALUES(%s,%s,%s,%s)",(self.ID,self.passwordHash,self.emailID,"NO"))
	
	def checkIfIDExists(cursor,id):
		user = USER()
		if user.storeTuple(cursor,"id",id):
			return user
		else:
			return None

	def checkIfEmailExists(cursor,email):
		user = USER()
		if user.storeTuple(cursor,"email_id",email):
			return user
		else:
			return None


	def verify_password(self,password):
		return check_password_hash(self.passwordHash,password)

	def isConfirmed(self,cursor):
		cursor.execute("SELECT confirmed from User WHERE id=%s",(self.ID,))
		tuple = cursor.fetchone()
		if tuple[0] == "NO":
			return 0
		else:
			return 1

	def confirmUser(self,cursor):
		cursor.execute("UPDATE User SET confirmed='YES' WHERE id=%s",(self.ID,))



	def __repr__(self):
		return '<User %r>' %self.ID












class STUDENT():
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
def load_user(ID):
    return USER.get(ID)


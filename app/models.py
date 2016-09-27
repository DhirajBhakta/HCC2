from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from . import login_manager 
from . import mysql





class StudentUser():
	rollno = None
	name = None
	email = None
	passwordhash = None



	
	def storeData(self,rollno,name,email,passwordhash):
		self.rollno = rollno
		self.name = name
		self.email = email
		self.passwordhash = passwordhash
		StudentUser.make_passwordHash(self,passwordhash)



	def storeTuple(self, tuple):
		self.rollno = tuple[0]
		self.name = tuple[1]
		self.email = tuple[2]
		self.passwordhash = tuple[3]

	def commit(self,cursor):
		cursor.execute("INSERT INTO StudentUser VALUES('"+self.rollno+"','"+self.name+"','"+self.email+"','"+self.passwordhash+"')")
	
	def checkIfRollnoExists(cursor,given_roll):
		cursor.execute("SELECT * FROM StudentUser WHERE rollno='"+given_roll+"'")
		return cursor.fetchone()

	def checkIfEmailExists(cursor,given_email):
		cursor.execute("SELECT * FROM StudentUser WHERE email='"+given_email+"'")
		return cursor.fetchone()


	def verify_password(self,password):
		return check_password_hash(self.passwordhash,password)

	def make_passwordHash(self,password):
		self.passwordhash = generate_password_hash(password)

	def __repr__(self):
		return '<User %r>' %self.name


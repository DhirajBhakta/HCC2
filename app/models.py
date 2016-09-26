from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from . import db, login_manager

class StudentUser(db.Model):
	__tablename__="StudentUser"
	rollno = db.Column("rollno",db.String(8),primary_key=True)
	name = db.Column("name",db.String(64),unique=True)
	email = db.Column("email",db.String(64),unique=True,index=True)
	passwordhash = db.Column("passwordhash",db.String(128))

	def verify_password(self,password):
		return check_password_hash(self.passwordhash,password)

	def make_passwordHash(self,password):
		self.passwordhash = generate_password_hash(password)

	def __repr__(self):
		return '<User %r>' %self.name


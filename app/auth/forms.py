from flask_wtf import Form 
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import StudentUser
from .. import mysql


class LoginForm(Form):
	rollno = StringField("Roll Number",validators=[Required(),Length(7,7,"Roll numbers are 7 characters in length (Eg: 14CV102")])
	password = PasswordField("Password",validators=[Required()])
	submit = SubmitField("Log in")



class RegistrationForm(Form):
	rollno = StringField('Roll number',validators=[Required(),Length(7,7,"NITK Student Roll Numbers are 7 characters long (eg:14ME142)")])
	name = StringField('Full Name',validators=[Required()])
	email = StringField('Email',validators=[Required(),Email()])
	password = PasswordField('Password',validators=[Required()])
	password2 = PasswordField('Confirm Password',validators=[Required(),EqualTo('password',message='Passwords must match!')])
	submit = SubmitField('Register')

	def validate_email(self,field):
		cursor = mysql.connect().cursor()
		if StudentUser.checkIfEmailExists(cursor,field.data):
			raise ValidationError('Email already registered.')

	def validate_rollno(self,field):
		cursor = mysql.connect().cursor()
		if StudentUser.checkIfRollnoExists(cursor,field.data):
			raise ValidationError('RollNumber already registered.')

			

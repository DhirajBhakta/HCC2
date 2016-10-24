from flask_wtf import Form 
from wtforms import RadioField,StringField,PasswordField,SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import USER, DOCTOR
from .. import mysql


class LoginForm(Form):
	patientType = RadioField('Status :',choices=[('STUDENT','Student'),('EMPLOYEE','Employee')])
	ID 		 = StringField("ID ",validators=[Required()])
	password = PasswordField("Password",validators=[Required()])
	submit   = SubmitField("Log in")



class RegistrationForm(Form):
	ID 		 	= StringField('ID',validators=[Required()])
	patientType = RadioField('Status :',choices=[('STUDENT','Student'),('EMPLOYEE','Employee')])
	name 	 	= StringField('Full Name',validators=[Required()])
	email 	 	= StringField('Email',validators=[Required(),Email()])
	password 	= PasswordField('Password',validators=[Required()])
	password2	= PasswordField('Confirm Password',validators=[Required(),EqualTo('password',message='Password mismatch!')])
	submit   	= SubmitField('Register')

	def validate_email(self,field):
		cursor = mysql.connect().cursor()
		thisUser = USER()
		thisUser = USER.checkIfEmailExists(cursor,field.data)
		if (thisUser is not None) and (thisUser.isConfirmed(cursor)):
			raise ValidationError('Email already registered.')

	def validate_ID(self,field):
		cursor = mysql.connect().cursor()
		thisUser = USER()
		thisUser = USER.checkIfIDExists(cursor,field.data)
		if (thisUser is not None) and (thisUser.isConfirmed(cursor)):
			raise ValidationError('ID already registered.')
		tuple = USER.checkIfExistsInDB(cursor, self.patientType.data, field.data, self.email.data)
		if tuple is None:
			raise ValidationError('ID not recognized . probably this ID isnt present in College Database')


			
class DoctorLoginForm(Form):
	doctorID = StringField("ID ",validators=[Required()])
	password = PasswordField("Password",validators=[Required()])
	submit   = SubmitField("Log in")

	def validate_doctorID(self,field):
		cursor = mysql.connect().cursor()
		if not DOCTOR.checkIfExistsInDB(cursor,field.data):
			raise ValidationError("Doctor ID Not recognized")


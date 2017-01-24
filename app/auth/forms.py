from flask_wtf import Form 
from wtforms import RadioField,StringField,PasswordField,SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import USER, DOCTOR
from .. import mysql


class LoginForm(Form):
	ID 		 = StringField("",validators=[Required()], render_kw={"placeholder": "Enter your ID"})
	password = PasswordField("",validators=[Required()], render_kw={"placeholder": "Enter your password"})
	submit   = SubmitField("Log in")



class RegistrationForm(Form):
	ID 		 	= StringField('',validators=[Required()],render_kw={"placeholder" : "Your Student/Employee ID"} )
	patientType = RadioField('',choices=[('STUDENT','Student'),('EMPLOYEE','Employee')])
	name 	 	= StringField('',validators=[Required()], render_kw={"placeholder": "Enter your full name"})
	email 	 	= StringField('',validators=[Required(),Email()], render_kw={"placeholder": "Enter your email"})
	password 	= PasswordField('',validators=[Required()], render_kw={"placeholder": "Enter your password"})
	password2	= PasswordField('',validators=[Required(),EqualTo('password',message='Password mismatch!')], render_kw={"placeholder": "Enter your password again"})
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
	doctorID = StringField("",validators=[Required()], render_kw={"placeholder": "Enter your Doctor ID"})
	password = PasswordField("",validators=[Required()], render_kw={"placeholder": "Enter your Password"})
	submit   = SubmitField("Log in")

	def validate_doctorID(self,field):
		cursor = mysql.connect().cursor()
		if not DOCTOR.checkIfExistsInDB(cursor,field.data):
			raise ValidationError("Doctor ID Not recognized")


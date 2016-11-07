from flask_wtf import Form 
from wtforms import RadioField,StringField,PasswordField,SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import USER, DOCTOR
from .. import mysql



			
class DoctorLoginForm(Form):
	doctorID = StringField("ID ",validators=[Required()])
	password = PasswordField("Password",validators=[Required()])
	submit   = SubmitField("Log in")

	def validate_doctorID(self,field):
		cursor = mysql.connect().cursor()
		if not DOCTOR.checkIfExistsInDB(cursor,field.data):
			raise ValidationError("Doctor ID Not recognized")


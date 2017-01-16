from flask_wtf import Form 
from wtforms import RadioField,StringField,SubmitField
from wtforms.validators import Required
from wtforms import ValidationError
from ..models import STUDENT,EMPLOYEE
from .. import mysql


class PatientArrival(Form):
	patientType = RadioField('Patient :',choices=[('STUDENT','Student'),('EMPLOYEE','Employee')])
	ID 			= StringField('ID',validators=[Required()])
	submit 		= SubmitField('OK ')

	def validate_ID(self,field):
		cursor = mysql.connect().cursor()
		if(self.patientType.data == 'STUDENT'):
			if not STUDENT.checkIfExistsInDB(cursor,self.ID.data):
				raise ValidationError('ID not recognized!')
		elif(self.patientType.data == 'EMPLOYEE'):
			if not EMPLOYEE.checkIfExistsInDB(cursor,self.ID.data):
				raise ValidationError('ID not recognized!')
	








from flask_wtf import Form 
from wtforms import RadioField,StringField,SubmitField
from wtforms.validators import Required
from wtforms import ValidationError
from ..models import STUDENT
from .. import mysql


class WorkbenchForm1(Form):
	patientType = RadioField('Patient :',choices=[('1','Student'),('2','Employee')])
	ID = StringField('ID',validators=[Required()])
	submit = SubmitField('OK ')

	def validate_ID(self,field):
		cursor = mysql.connect().cursor()
		if(self.patientType.data == '1'):
			if not STUDENT.checkIfExistsInDB(cursor,self.ID.data):
				raise ValidationError('ID not recognized!')








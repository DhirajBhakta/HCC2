from flask import render_template, redirect ,request,url_for ,flash, current_app,jsonify
from flask_login import login_user , logout_user, current_user,login_required
from . import admin
from ..models import USER,STUDENT,Appointment
from .. import mysql,mail
from ..email import send_email
from flask_mail import Message
import json


@admin.route('/reschedule',methods=['GET','POST'])
def reschedule():
	conn = mysql.connect()
	cursor = conn.cursor()
	if request.method == 'POST':
		lastDate = request.form.get('LASTDATE')
		print(lastDate)
		if lastDate is not None:
			datestr = lastDate.split('-')
			lastDateStr = datestr[2]+"-"+datestr[1]+"-"+datestr[0]
			cursor.execute("CALL fill_calendar(%s)",(lastDateStr,))
			conn.commit()
			flash('Appointment Slots Created! till '+lastDate)
			return redirect(url_for('auth.reschedule'))
		#AppointmentDetails =
	return render_template('admin/reschedule.html') 


@admin.route('/retrieveBookedAppointments',methods=['GET'])
def retrieveBookedAppointments():
	conn = mysql.connect()
	cursor = conn.cursor()
	date = request.args.get('DATE')
	datestr = date.split('-')
	date = datestr[2]+'-'+datestr[1]+'-'+datestr[0]
	category = request.args.get('CATEGORY')
	print(date)
	print(category)
	bookedAppointments=Appointment.retrieveBookedAppointments(cursor,[date,category],"ADMIN")
	json_string = json.dumps([obj.__dict__ for obj in bookedAppointments])
	return json_string

@admin.route('/getViableDatesForCategory',methods=['GET'])
def getViableDatesForCategory():
	conn = mysql.connect()
	cursor = conn.cursor()
	category = request.args.get('CATEGORY')
	print(category)
	print(category)
	print(category)
	print(category)
	viableDates = Appointment.getViableDatesForCategory_admin(cursor,category)
	json_string = json.dumps([obj.__dict__ for obj in viableDates])
	return json_string


@admin.route('/getPatientDetails',methods=['GET'])
def getPatientDetails():
	conn = mysql.connect()
	cursor = conn.cursor()
	patientID = request.args.get('PATIENTID')
	print(patientID)
	print("\n\n\n\n\n")
	thisStudent = STUDENT()
	thisStudent.storeTuple(cursor,"rollno",patientID)
	#json_string = json.dumps(thisStudent.__dict__)
	return thisStudent.name

@admin.route('/submitAppointment',methods=['POST'])
def submitAppointment():
	conn = mysql.connect()
	cursor = conn.cursor()
	patientID = request.form.get('PATIENTID')
	calendarID = request.form.get('CALENDARID')
	Appointment.commitSubmittedAppointmentIntoDB_admin(cursor,calendarID,patientID)
	conn.commit()
	return "true"


	



@admin.route('/appointments',methods=['GET','POST'])
def appointments():
	conn = mysql.connect()
	cursor = conn.cursor()
	if request.method == 'POST':
		pass

	else:
		return render_template('admin/appointment.html')
		
		
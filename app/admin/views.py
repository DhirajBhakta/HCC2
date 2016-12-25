from flask import render_template, redirect ,request,url_for ,flash, current_app,jsonify
from flask_login import login_user , logout_user, current_user,login_required
from . import admin
from ..models import STUDENT,DOCTOR,Appointment,Schedule
from .. import mysql,mail
from ..email import send_email
from flask_mail import Message
import json 
import datetime


@admin.route('/reschedule',methods=['GET','POST'])
def reschedule():
	conn = mysql.connect()
	cursor = conn.cursor()
	if request.method == 'POST':
		lastDate = request.form.get('LASTDATE')
		print(lastDate)
		if lastDate is not None:
			cursor.execute("CALL fill_calendar('"+lastDate+"')")
			conn.commit()
			flash('Appointment Slots Created! till '+lastDate)
			return redirect(url_for('admin.reschedule'))
		#AppointmentDetails =
	doclist = DOCTOR.getAllDoctorDetails(cursor)
	return render_template('admin/reschedule.html',doclist=doclist) 


@admin.route('/getAppointmentCalendarForDoctor',methods=['GET'])
def getAppointmentCalendarForDoctor():
	conn = mysql.connect()
	cursor = conn.cursor()
	doctorID = request.args.get('DOCTORID')
	schedulelist = Schedule.getCalendar(cursor,doctorID)
	json_string = json.dumps([obj.__dict__ for obj in schedulelist])
	return json_string


@admin.route('/modifyCalendarSchedule',methods=['POST'])
def modifyCalendarSchedule():
	conn = mysql.connect()
	cursor = conn.cursor()
	calendarID = request.form.get('CALENDARID')
	date = request.form.get('DATE');
	stime = request.form.get('STIME');
	etime = request.form.get('ETIME');
	Schedule.replace(cursor,calendarID,date,stime,etime)
	conn.commit()
	return 'true'




@admin.route('/deleteCalendarSchedule',methods=['POST'])
def deleteCalendarSchedule():
	conn = mysql.connect()
	cursor = conn.cursor()
	calendarID = request.form.get('CALENDARID')
	print("\n\n\n")
	print(calendarID)
	print("\n\n\n")
	cursor.execute("DELETE FROM Appointment_calendar WHERE calendar_id=%s",(calendarID,))
	conn.commit()
	return 'true'



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
		
		
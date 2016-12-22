from flask import render_template, request ,redirect
from .. import mysql
from ..models import STUDENT, PRESCRIPTION, Appointment
from . import student
from flask_login import current_user, login_required
import json
import rdflib

@student.route("/profile")
@login_required
def showStudentProfile():
	conn = mysql.connect()
	cursor = conn.cursor()
	id = current_user.get_id()

	studentUser = STUDENT()
	studentUser.storeTuple(cursor,"rollno",id)
	return render_template("student/studentprofile.html",studentUser = studentUser)


@student.route('/medicalhistory')
def showMedicalHistory():
	conn = mysql.connect()
	cursor = conn.cursor()
	id = current_user.get_id()

	prescriptionList = []
	cursor.execute("SELECT prescription_id FROM Prescription WHERE patient_id = (SELECT patient_id FROM Student WHERE rollno=%s)",(id,))
	prescList = cursor.fetchall()
	for prescriptionID in prescList:
		prescription = PRESCRIPTION()
		prescription.storeTuple(cursor,prescriptionID)
		prescriptionList.append(prescription)
	id = current_user.get_id()

	studentUser = STUDENT()
	studentUser.storeTuple(cursor,"rollno",id)

	return render_template('student/medicalhistory.html',prescriptionList=prescriptionList,studentUser=studentUser)



@student.route('/bookAppointment',methods=['GET'])
def bookAppointment():
	conn = mysql.connect()
	cursor = conn.cursor()
	id = current_user.get_id()
	studentUser = STUDENT()
	studentUser.storeTuple(cursor,"rollno",id)

	category = request.args.get('CATEGORY')
	if category is not None:
		appointmentDates = Appointment.getViableDatesForCategory(cursor,category)
		json_string = json.dumps([obj.__dict__ for obj in appointmentDates])
		return json_string
	return render_template('student/bookappointment.html',studentUser=studentUser)


@student.route('/submitAppointment',methods=['POST'])
def submitAppointment():
	conn = mysql.connect()
	cursor = conn.cursor()
	id = current_user.get_id()
	studentUser = STUDENT()
	studentUser.storeTuple(cursor,"rollno",id)
	
	calendarID = request.form.get('CALENDARID')
	appointmentStatus = request.form.get('APPSTATUS')
	Appointment.commitSubmittedAppointmentIntoDB(cursor,calendarID,studentUser.patientID,appointmentStatus)
	conn.commit()
	return render_template('student/success.html',studentUser=studentUser)

@student.route('/retrieveBookedAppointments',methods=['GET'])
def retrieveBookedAppointments():
	conn = mysql.connect()
	cursor = conn.cursor()
	id = current_user.get_id()
	studentUser = STUDENT()
	studentUser.storeTuple(cursor,"rollno",id)
	bookedAppointments = Appointment.retrieveBookedAppointments(cursor,studentUser.patientID,"PATIENT")
	json_string = json.dumps([obj.__dict__ for obj in bookedAppointments])
	return json_string

@student.route('/deleteBookedAppointment',methods=['POST'])
def deleteBookedAppointment():
	conn = mysql.connect()
	cursor = conn.cursor()
	slotID = request.form.get('SLOTID')
	print(slotID)
	Appointment.deleteBookedAppointment(cursor,slotID)
	conn.commit()
	return "true"




	


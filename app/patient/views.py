from flask import render_template, request ,redirect
from .. import mysql
from ..models import STUDENT,EMPLOYEE,DEPENDANT ,PRESCRIPTION, Appointment
from ..utils import specific_login_required
from . import patient
from flask_login import current_user, login_required
import json

#------------------------------------------------------
class DB:
	conn   = mysql.connect()
	cursor = conn.cursor()

def classifyAndGetCurrentUser():
	userType = current_user.get_utype()
	ID       = current_user.get_id()
	if(userType == "STUDENT"):
		patient = STUDENT()
		patient.storeTuple(DB.cursor,"rollno",ID)
	else:
		patient = EMPLOYEE()
		patient.storeTuple(DB.cursor,"emp_id",ID)
	return patient
#-------------------------------------------------------


@patient.route("/profile",methods=["GET"])
@specific_login_required(urole="PATIENT")
def showPatientProfile():
	patient = classifyAndGetCurrentUser()
	return render_template("patient/patientprofile.html",patient=patient)


@patient.route('/medicalhistory',methods=["GET"])
@specific_login_required(urole="PATIENT")
def showMedicalHistory():
	patient   = classifyAndGetCurrentUser()
	patientID = current_user.getPatientID(DB.cursor)
	prescriptionList = PRESCRIPTION.getPrescriptionList(DB.cursor,"BY_PATIENTID",patientID)
	return render_template('patient/medicalhistory.html',prescriptionList=prescriptionList,patient=patient)



@patient.route('/bookAppointment',methods=['GET','POST'])
@specific_login_required(urole="PATIENT")
def bookAppointment():
	patient  = classifyAndGetCurrentUser()
	if(request.method == "POST"):
		calendarID 		  = request.form.get('CALENDARID')
		appointmentStatus = request.form.get('APPSTATUS')
		Appointment.commitSubmittedAppointmentIntoDB(DB.cursor,calendarID,patient.patientID,appointmentStatus)
		DB.conn.commit()
		return render_template('patient/success.html',patient=patient)

	category = request.args.get('CATEGORY')
	if category is not None:
		appointmentDates = Appointment.getViableDatesForCategory(DB.cursor,category)
		json_string = json.dumps([obj.__dict__ for obj in appointmentDates])
		return json_string
	return render_template('patient/bookappointment.html',patient=patient)

	

@patient.route('/getBookedAppointments',methods=['GET'])
@specific_login_required(urole="PATIENT")
def getBookedAppointments():
	patient = classifyAndGetCurrentUser()
	bookedAppointments = Appointment.getBookedAppointments(DB.cursor,patient.patientID,"PATIENT")
	json_string = json.dumps([obj.__dict__ for obj in bookedAppointments]), 200, {'ContentType':'application/json'} 
	return json_string


@patient.route('/deleteBookedAppointment',methods=['POST'])
@specific_login_required(urole="PATIENT")
def deleteBookedAppointment():
	slotID = request.form.get('SLOTID')
	Appointment.deleteBookedAppointment(DB.cursor,slotID)
	DB.conn.commit()
	return "true"




	


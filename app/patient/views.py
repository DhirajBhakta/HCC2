from flask import render_template, request ,redirect,url_for, session
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

#session['mode']
#  is -1 for student
#  is -1 when employee uses for himself
#  is  0,1,2,3... when employee uses for his dependants

def classifyAndGetCurrentUser():
	userType = current_user.get_utype()
	ID       = current_user.get_id()
	mode     = session['mode']
	print("MODE in classifyAndGetCurrentUser:"+str(mode))
	print("MODE"+str(mode))
	print("utype:"+userType)
	if(userType == "STUDENT"):
		patient = STUDENT()
		patient.storeTuple(DB.cursor,"rollno",ID)
	elif((userType == "EMPLOYEE") and (mode == -1)):
		patient = EMPLOYEE()
		patient.storeTuple(DB.cursor,"emp_id",ID)
	elif((userType == "EMPLOYEE") and (mode != -1)):
		patient = DEPENDANT()
		patient._storeTuple(DB.cursor,ID,mode)
	return patient
#-------------------------------------------------------


@patient.route("/profile",methods=["GET"])
@specific_login_required(urole="PATIENT")
def showPatientProfile():
	print("\n\nshowPatientProfile called classifyAndGetCurrentUser")
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
		slotID = Appointment.commitSubmittedAppointmentIntoDB(DB.cursor,calendarID,patient.patientID,appointmentStatus)
		DB.conn.commit()
		return str(slotID)

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


@patient.route('/switchUser',methods=['GET','POST'])
@specific_login_required(urole="PATIENT")
def switchUser():
	if(request.method == 'POST'):
		dependantID = request.form.get('DEPENDANT_ID')
		session['mode']= int(dependantID)
		return redirect(url_for('patient.showPatientProfile'))

	session['mode']=-1
	patient = classifyAndGetCurrentUser()
	return render_template('patient/switchUser.html',patient=patient)





	


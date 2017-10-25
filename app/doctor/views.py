from flask import render_template ,request ,redirect ,url_for
from .. import mysql
from ..models import DOCTOR , PrescriptionDrug, PRESCRIPTION, STUDENT,EMPLOYEE,DEPENDANT,DRUG, Appointment
from . import doctor
from .forms import PatientArrival
from ..utils import specific_login_required
from flask_login import current_user, login_required
import datetime

class DB:
	conn   = mysql.connect()
	cursor = conn.cursor()


def getCurrentDoctor():
	empID  = current_user.ID
	doctor = DOCTOR()
	doctor.storeTuple(DB.cursor,"emp_id",empID)
	return doctor

@doctor.route('/',methods=['GET','POST'] )
@specific_login_required("DOCTOR")
def showWorkbench():
	form   = PatientArrival()
	doctor = getCurrentDoctor()
	if form.validate_on_submit():
		patientType = form.patientType.data
		ID 			= form.ID.data
		druglist    = DRUG.retrieveDBdrugs(DB.cursor)
		druglist    = [""]+druglist
		if (patientType == 'STUDENT'):
			studentPatient = STUDENT()
			studentPatient.storeTuple(DB.cursor,"rollno",ID)
			return render_template('doctor/diagnosis.html',patient=studentPatient,doctorUser=doctor,druglist=druglist)
		elif(patientType == 'EMPLOYEE'):
			empl = EMPLOYEE()
			empl.storeTuple(DB.cursor,"emp_id",ID)
			return render_template('doctor/choosePatient.html',employee=empl,doctorUser=doctor)
	return render_template('doctor/patientarrival.html',form=form,doctorUser=doctor)

@doctor.route('/acceptSpecialPatient',methods=['POST'])
def acceptSpecialPatient():
	doctor = getCurrentDoctor()
	empID = request.form.get('EMP_ID')
	depID = request.form.get('PATIENT')
	depID = int(depID)
	druglist    = DRUG.retrieveDBdrugs(DB.cursor)
	druglist    = [""]+druglist
	if (depID == -1):
		patient = EMPLOYEE()
		patient.storeTuple(DB.cursor,'emp_id',empID)
	else:
		patient = DEPENDANT()
		patient._storeTuple(DB.cursor,empID,depID)
	return render_template('doctor/diagnosis.html',patient=patient,doctorUser=doctor,druglist=druglist)




@doctor.route('/addPrescription',methods=['GET','POST'])
@specific_login_required("DOCTOR")
def addPrescription():
	prescription = PRESCRIPTION()
	doctorID  = request.form.get('DOCTORID')
	patientID = request.form.get('PATIENTID')
	indication = request.form.get('INDICATION')

	for row in range(5):
		DRUG_NAME = "DRUG_NAME"+str(row)
		DRUG_QTY="DRUG_QTY"+str(row)
		DRUG_SCHEDULE="DRUG_SCHEDULE"+str(row)
		DRUG_COMMENTS="DRUG_COMMENTS"+str(row)

		drugName = request.form.get(DRUG_NAME)
		if not drugName:
			break
		drugQty      = request.form.get(DRUG_QTY)
		drugSchedule = request.form.get(DRUG_SCHEDULE)
		drugComments = request.form.get(DRUG_COMMENTS)

		thisDrug = PrescriptionDrug()
		thisDrug.storeData(0,drugName,drugQty,drugSchedule,drugComments)
		prescription.addDrug(thisDrug)
	prescription.insertIntoDB(DB.conn,doctorID,patientID,indication)
	DB.conn.commit()
	return redirect(url_for('doctor.success'))






@doctor.route('/viewPatientProfile/<patientID>')
@specific_login_required("DOCTOR")
def viewPatientProfile(patientID):
	doctor = getCurrentDoctor()
	patient = DOCTOR.retrievePatientDetails(DB.cursor,patientID)
	prescriptionList = PRESCRIPTION.getPrescriptionList(DB.cursor,"BY_PATIENTID",patientID)
	return render_template("doctor/patientprofile.html",patient=patient,prescriptionList=prescriptionList,doctorUser=doctor)


@doctor.route('/profile')
@specific_login_required("DOCTOR")
def showDoctorProfile():
	doctor = getCurrentDoctor()
	return render_template("doctor/doctorprofile.html",doctorUser=doctor)






@doctor.route('/viewHistory',methods=['GET','POST'])
@specific_login_required("DOCTOR")
def showHistory():
	doctor = getCurrentDoctor()
	if request.method == 'GET':
		return render_template('doctor/history.html',doctorUser=doctor)
	else:
		date = request.form.get('DATE')
		if date is not None:
			date = datetime.datetime.strptime(date,"%Y-%m-%d").date()
			prescriptionList = PRESCRIPTION.getPrescriptionList(DB.cursor,"BY_DATE",date)
			return render_template('doctor/history.html',doctorUser=doctor,prescriptionList=prescriptionList)

		return render_template('doctor/history.html',doctorUser=doctor)




@doctor.route('/showUpcomingAppointments')
@specific_login_required("DOCTOR")
def showUpcomingAppointments():
	doctor = getCurrentDoctor()
	bookedApps 	 = Appointment.getBookedAppointments(DB.cursor,doctor.doctorID,"DOCTOR")
	bookedAppsOrdered = sorted(bookedApps,key=lambda x:x.date ,reverse=True)
	print(bookedApps)
	if bookedApps == []:
		pass

	else:
		bookedAppointments = [[]]
		bookedAppointments[-1].append(bookedAppsOrdered[0])
		DATE = bookedAppsOrdered[0].date
		for app in bookedAppsOrdered:
			if app.date!=DATE:
				bookedAppointments.append(list())
			bookedAppointments[-1].append(app)




	return render_template('doctor/viewAppointments.html',doctorUser=doctor,bookedAppointments=bookedAppsOrdered)




@doctor.route('/success')
@specific_login_required("DOCTOR")
def success():
	doctor = getCurrentDoctor()
	return render_template("doctor/success.html",doctorUser=doctor)

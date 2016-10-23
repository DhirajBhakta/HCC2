from flask import render_template ,request ,redirect ,url_for
from .. import mysql
from ..models import DOCTOR , PrescriptionDrug, PRESCRIPTION, STUDENT
from . import doctor
from .forms import WorkbenchForm1
from flask_login import current_user, login_required


@doctor.route('/',methods=['GET','POST'] )
def showWorkbench():
	form = WorkbenchForm1()
	conn = mysql.connect()
	cursor = conn.cursor()

	empID = current_user.ID
	doctor = DOCTOR()
	doctor.storeTuple(cursor,"emp_id",empID)

	if form.validate_on_submit():
		patientType = form.patientType.data
		ID = form.ID.data
		if (patientType == '1'):
			studentPatient = STUDENT()
			studentPatient.storeTuple(cursor,ID)
			return render_template('doctor/doctorworkbench2.html',patient=studentPatient,doctor=doctor,doctorUser=doctor)
	return render_template('doctor/doctorworkbench1.html',form=form,doctorUser=doctor)



@doctor.route('/addPrescription',methods=['GET','POST'])
def addPrescription():
	conn = mysql.connect()
	cursor = conn.cursor()
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
		thisDrug.storeData(drugName,drugQty,drugSchedule,drugComments)
		prescription.addDrug(thisDrug)
	prescription.insertIntoDB(conn,doctorID,patientID,indication)
	conn.commit()

	return redirect(url_for('doctor.success'))




@doctor.route('/profile')
@login_required
def showDoctorProfile():
	cursor = mysql.connect().cursor()
	empID = current_user.ID
	doctor = DOCTOR()
	doctor.storeTuple(cursor,"emp_id",empID)

	return render_template('doctor/doctorprofile.html',doctorUser=doctor)


@doctor.route('/success')
def success():
	cursor = mysql.connect().cursor()
	empID = current_user.ID
	doctor = DOCTOR()
	doctor.storeTuple(cursor,"emp_id",empID)
	return render_template("doctor/success.html",doctorUser=doctor)




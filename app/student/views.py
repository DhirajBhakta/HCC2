from flask import render_template
from .. import mysql
from ..models import STUDENT, PRESCRIPTION
from . import student
from flask_login import current_user, login_required

@student.route("/profile")
@login_required
def showStudentProfile():
	conn = mysql.connect()
	cursor = conn.cursor()
	id = current_user.get_id()

	studentUser = STUDENT()
	studentUser.storeTuple(cursor,id)
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
	studentUser.storeTuple(cursor,id)

	return render_template('student/medicalhistory.html',prescriptionList=prescriptionList,studentUser=studentUser)


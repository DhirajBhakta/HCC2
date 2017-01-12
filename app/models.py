from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from . import login_manager 
from flask import current_app
from . import mysql
import datetime




class USER(UserMixin):
	#this name attribute shall not be put into DB.!!
	name = None

	ID = None
	emailID = None
	passwordHash = None
	userType = None


	def get_id(self):
		return str(self.ID)

	def get(ID):
		cursor = mysql.connect().cursor()
		loggedInUser = USER()
		loggedInUser.storeTuple(cursor,"id",ID)
		return loggedInUser
	
    #----token related--------------------------------------------------
	def generate_confirmation_token(self, expiration=3600):
		s = Serializer(current_app.config['SECRET_KEY'], expiration)
		return s.dumps({'confirm': self.ID})

	def confirm(self, token,cursor):
		s = Serializer(current_app.config['SECRET_KEY'])
		data = s.loads(token)
		USER.confirmUser(self,cursor) 

	def getUserIDFromToken(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		data = s.loads(token)
		return data.get('confirm')
	#-------------------------------------------------------------------	

	#data stored into object to be later put into Database
	def storeData(self,name,id,email,password,usertype):
		self.name = name
		self.ID = id
		self.emailID = email
		self.userType = usertype
		self.passwordHash =  generate_password_hash(password)
	    

	#Database to object
	def storeTuple(self,cursor,column,value):
		cursor.execute("SELECT * FROM User WHERE "+column+" = %s",(value,))
		tuple = cursor.fetchone()
		if tuple is None:
			return False
		self.ID = tuple[0]
		self.passwordHash = tuple[1]
		self.emailID = tuple[2]
		self.userType = tuple[4]
		return True

	def checkIfExistsInDB(cursor,patientType,id,email):
		if(patientType=='STUDENT'):
			cursor.execute("SELECT * FROM Student WHERE rollno=%s AND email_id=%s",(id,email))
		else:
			cursor.execute("SELECT * FROM Employee WHERE emp_id=%s AND email_id=%s",(id,email))	
		return cursor.fetchone()


	def insertIntoDB(self,cursor):
		userIfPresent = USER.checkIfIDExists(cursor,self.ID)
		if (userIfPresent is not None) and (not userIfPresent.isConfirmed(cursor)):
			cursor.execute("DELETE FROM User WHERE id=%s",(userIfPresent.ID,))
		cursor.execute("INSERT INTO User VALUES(%s,%s,%s,%s,%s)",(self.ID,self.passwordHash,self.emailID,"NO",self.userType))
	
	def checkIfIDExists(cursor,id):
		user = USER()
		if user.storeTuple(cursor,"id",id):
			return user
		else:
			return None

	def checkIfEmailExists(cursor,email):
		user = USER()
		if user.storeTuple(cursor,"email_id",email):
			return user
		else:
			return None


	def verify_password(self,password):
		return check_password_hash(self.passwordHash,password)

	def isConfirmed(self,cursor):
		cursor.execute("SELECT confirmed from User WHERE id=%s",(self.ID,))
		tuple = cursor.fetchone()
		if tuple[0] == "NO":
			return 0
		else:
			return 1

	def confirmUser(self,cursor):
		cursor.execute("UPDATE User SET confirmed='YES' WHERE id=%s",(self.ID,))



	def __repr__(self):
		return '<User %r>' %self.ID





@login_manager.user_loader
def load_user(ID):
    return USER.get(ID)








class STUDENT():
	rollno = None
	name = None
	DOB = None
	sex = None
	phno = None
	email = None
	guardianPhno = None
	locAddr = None
	permAddr = None
	patientID = None
	dept = None
	course = None
	blood = None




	#Database to object
	def storeTuple(self,cursor,colname,value):
		cursor.execute("SELECT * FROM Student WHERE "+colname+"=%s",(value,))
		tuple = cursor.fetchone()
		
		self.rollno 	  = tuple[0]
		self.name   	  = tuple[1]
		self.DOB		  = tuple[2]
		self.sex 		  = tuple[3]
		self.phno   	  = tuple[4]
		self.email  	  = tuple[5]
		self.guardianPhno = tuple[6]
		self.locAddr      = str(tuple[7])
		self.permAddr	  = str(tuple[8])
		self.patientID    = tuple[9]
		
		cursor.execute("SELECT dept_name FROM Department WHERE dept_id='"+str(tuple[10])+"'")
		tupledept   = cursor.fetchone()
		cursor.execute("SELECT course_name FROM Course WHERE course_id='"+str(tuple[11])+"'")
		tuplecourse = cursor.fetchone()

		self.dept   = tupledept[0]
		self.course = tuplecourse[0]
		self.blood  = tuple[12]

	def checkIfExistsInDB(cursor,rollno):
		cursor.execute("SELECT * FROM Student WHERE rollno=%s",(rollno,))
		return cursor.fetchone()



class EMPLOYEE():
	empID = None
	name = None
	DOB = None
	sex = None
	phno = None
	email = None
	locAddr = None
	permAddr = None
	workStatus = None
	designation = None
	patientID = None
	dept = None
	blood = None


	#Database to object
	def storeTuple(self,cursor,empID):
		cursor.execute("SELECT * FROM Employee WHERE emp_id='"+empID+"'")
		tuple = cursor.fetchone()
		
		self.empID 	      = tuple[0]
		self.name   	  = tuple[1]
		self.DOB		  = tuple[2]
		self.sex 		  = tuple[3]
		self.phno   	  = tuple[4]
		self.email  	  = tuple[5]
		self.locAddr      = str(tuple[6])
		self.permAddr	  = str(tuple[7])
		self.workStatus   = tuple[8]
		self.designation  = tuple[9]
		self.patientID    = tuple[9]
		
		cursor.execute("SELECT dept_name FROM Department WHERE dept_id='"+str(tuple[10])+"'")
		tupledept   = cursor.fetchone()

		self.dept   = tupledept[0]
		self.blood  = tuple[12]

	def checkIfExistsInDB(cursor,rollno):
		cursor.execute("SELECT * FROM Student WHERE rollno=%s",(rollno,))
		return cursor.fetchone()








class DOCTOR():
	doctorID = None
	doctorName = None
	doctorSpecialization = None
	doctorEmployeeID = None
	treatmentCount = 0

    #Database to object
	def storeTuple(self,cursor,colName,value):
		cursor.execute("SELECT * FROM Doctor WHERE "+colName+" = %s",(value,))
		tuple = cursor.fetchone()
		if tuple is None:
			return False
		self.doctorID = tuple[0]
		self.doctorName = tuple[1]
		self.doctorSpecialization = tuple[2]
		self.doctorEmployeeID = tuple[3]
		DOCTOR.updateTreatmentCount(self,cursor)
		return True


	def checkIfExistsInDB(cursor,docID):
		cursor.execute("SELECT * FROM Doctor WHERE doctor_id = %s",(docID,))
		return cursor.fetchone()

	def updateTreatmentCount(self,cursor):
		cursor.execute("SELECT COUNT(*) FROM Prescription WHERE doctor_id=%s",(self.doctorID,))
		self.treatmentCount = cursor.fetchone()[0] 

	def retrievePatientDetails(cursor,patientID):
		studentPatient = STUDENT()
		cursor.execute("SELECT rollno FROM Student WHERE patient_id=%s",patientID)
		rollno = cursor.fetchone()[0]
		studentPatient.storeTuple(cursor,"rollno",rollno)
		return studentPatient

	def getAllDoctorDetails(cursor):
		docList =list()
		cursor.execute("SELECT doctor_id ,name FROM Doctor WHERE doctor_id>0")
		tuples = cursor.fetchall()
		for tuple in tuples:
			doc = DOCTOR()
			doc.doctorID = tuple[0]
			doc.doctorName = tuple[1]
			docList.append(doc)
		return docList









class PrescriptionDrug():
	drugName = None
	drugQty  = None
	drugSchedule = None
	drugComments = None

	def storeData(self,drugName,drugQty,drugSchedule,drugComments):
		self.drugName 	  = drugName
		self.drugQty  	  = drugQty
		self.drugSchedule = drugSchedule
		self.drugComments = drugComments



class PRESCRIPTION():
	prescriptionID = None
	prescriptionDrugs = None
	prescriptionDateTime = datetime.datetime.now()
	doctor = DOCTOR()
	patientID = None
	indication = None

	def __init__(self):
		self.prescriptionDrugs = list()


	def addDrug(self,drug):
		self.prescriptionDrugs.append(drug)

	#Database to object	
	def storeTuple(self,cursor,prescID):
		cursor.execute("SELECT * FROM Prescription WHERE prescription_id=%s ",(prescID,))
		tuple = cursor.fetchone()
		self.prescriptionID = tuple[0]
		self.prescriptionDateTime = tuple[1]
		#self.doctorID = tuple[2]
		self.patientID = tuple[3]
		self.indication = tuple[4]
		self.doctor.storeTuple(cursor,"doctor_id",tuple[2])

		cursor.execute("SELECT * FROM Prescription_drug_map WHERE prescription_id=%s",(self.prescriptionID,))
		drugtuples = cursor.fetchall()
		for drugtuple in drugtuples:
			cursor.execute("SELECT trade_name FROM Drug WHERE drug_id=%s",(drugtuple[1]))
			drugName = cursor.fetchone()[0]

			prescriptionDrug = PrescriptionDrug()
			prescriptionDrug.storeData(drugName,drugtuple[2],drugtuple[3],drugtuple[4])
			self.prescriptionDrugs.append(prescriptionDrug)


	def insertIntoDB(self,conn,docID,patientID,indication):
		cursor = conn.cursor()
		self.doctor.storeTuple(cursor,"doctor_id",docID)
		self.patientID = patientID
		self.indication = indication
		cursor.execute("INSERT INTO Prescription (date_time,doctor_id,patient_id,indication) VALUES (%s,%s,%s,%s)",(self.prescriptionDateTime,self.doctor.doctorID,self.patientID,self.indication))
		cursor.execute("SELECT MAX(prescription_id) from Prescription")
		tuple = cursor.fetchone()
		self.prescriptionID = tuple[0]
		for drug in self.prescriptionDrugs:
			cursor.execute("SELECT drug_id FROM Drug WHERE trade_name=%s",(drug.drugName,))
			tuple = cursor.fetchone()
			drugID = tuple[0]
			cursor.execute("INSERT INTO Prescription_drug_map VALUES(%s,%s,%s,%s,%s)",(self.prescriptionID,drugID,drug.drugQty,drug.drugSchedule,drug.drugComments))
		conn.commit()		

	def getPrescriptionList(cursor,date):
		prescriptionList = list()
		cursor.execute("SELECT prescription_id FROM Prescription WHERE DATE(date_time)=%s",(date,))
		prescIDtuples = cursor.fetchall()
		for prescIDtuple in prescIDtuples:
			prescription = PRESCRIPTION()
			prescription.storeTuple(cursor,prescIDtuple[0])
			prescriptionList.append(prescription)
		return prescriptionList



class DRUG():

	def __init__(self):
		self.drugName = None
		self.quantity = None
		self.batchNumber = None
		self.expiryDate = None

	def retrieveDBdrugs(cursor):
		drugNamesList = list()
		cursor.execute("SELECT DISTINCT trade_name FROM Drug")
		drugNames = cursor.fetchall()
		for drugName in drugNames:
			print(drugName)
			drugNamesList.append(drugName[0])
		return drugNamesList

	def stockUpdate(cursor,drugList):
		for drug in drugList:
			cursor.execute("SELECT drug_id FROM Drug WHERE trade_name=%s",(drug.drugName,))
			tuple = cursor.fetchone()
			drugID = tuple[0]
			cursor.execute("INSERT INTO Batch VALUES(%s,%s,%s,%s)",(drug.batchNumber,drugId,drug.quantity,drug.expiryDate))











class Appointment():
	calendarID = None
	slotID = None
	date = None
	doctorName = None
	category = None
	startTime = None
	endTime = None
	sessionLimit = None
	status = None


	def getViableDatesForCategory(cursor,specialization):
		appointmentDates = list()
		cursor.execute("SELECT * from Appointment_calendar JOIN Doctor ON Appointment_calendar.doctor_id = Doctor.doctor_id AND Doctor.specialization = %s ",specialization)
		tuples = cursor.fetchall()
		for tuple in tuples:
			print(tuple)
			appointmentDate = Appointment()
			appointmentDate.calendarID = tuple[0]
			date = tuple[1]
			appointmentDate.date = str(date)
			appointmentDate.doctorName = tuple[7]
			time = tuple[3]
			appointmentDate.startTime = str(time)
			time = tuple[4]
			appointmentDate.endTime = str(time)
			appointmentDate.sessionLimit = tuple[5];
			appointmentDates.append(appointmentDate)
		return appointmentDates

	def getViableDatesForCategory_admin(cursor,specialization):
		appointmentDates = list()
		cursor.execute("SELECT * from Appointment_calendar JOIN Doctor ON Appointment_calendar.doctor_id = Doctor.doctor_id AND Doctor.specialization = %s",specialization)
		tuples = cursor.fetchall()
		for tuple in tuples:
			print(tuple)
			appointmentDate = Appointment()
			appointmentDate.calendarID = tuple[0]
			date = tuple[1]
			appointmentDate.date = str(date)
			appointmentDate.doctorName = tuple[7]
			time = tuple[3]
			appointmentDate.startTime = str(time)
			time = tuple[4]
			appointmentDate.endTime = str(time)
			appointmentDates.append(appointmentDate)
		return appointmentDates

	def commitSubmittedAppointmentIntoDB(cursor,calendarID,patientID,appStatus):
		cursor.execute("INSERT INTO Appointment_slot (patient_id,calendar_id,status) VALUES (%s,%s,%s)",(patientID,calendarID,appStatus))
		cursor.execute("UPDATE Appointment_calendar SET session_limit = session_limit -1 WHERE calendar_id=%s",calendarID)



	def commitSubmittedAppointmentIntoDB_admin(cursor,calendarID,rollno):
		cursor.execute("INSERT INTO Appointment_slot (patient_id,calendar_id) VALUES ((SELECT patient_id FROM Student WHERE rollno=%s),%s)",(rollno,calendarID))
		cursor.execute("UPDATE Appointment_calendar SET session_limit = session_limit -1 WHERE calendar_id=%s",calendarID)


	def retrieveBookedAppointments(cursor,ID,forWHOM):
		appointments = list()
		print("\n\n\n"+str(ID)+"\n\n\n")
		if forWHOM == "PATIENT":
			cursor.execute("SELECT * FROM View_patient_appointment WHERE patient_id=%s",ID)
			tuples = cursor.fetchall()
			for tuple in tuples:
				appointment = Appointment()
				appointment.slotID = tuple[0]
				appointment.doctorName = tuple[1]
				appointment.date = str(tuple[2])
				appointment.startTime = str(tuple[3])
				appointment.endTime = str(tuple[4])
				appointment.category = tuple[6]
				appointment.status = tuple[7]
				appointments.append(appointment)
		elif forWHOM == "DOCTOR":
			cursor.execute("SELECT date,patient_id,patient_type FROM View_appointment_patient_ref_map WHERE doctor_id=%s ORDER BY date",ID)
			tuples = cursor.fetchall()
			for tuple in tuples:
				appointment = Appointment()
				appointment.date = tuple[0]
				appointment.patientID = tuple[1]
				patientType = tuple[2]
				if(patientType == "STUDENT"):
					cursor.execute("SELECT name,rollno,Course.course_name  FROM Student JOIN Course ON Student.course_id=Course.course_id AND patient_id=%s",(appointment.patientID,))
					stu = cursor.fetchone()
					print("\n\n\n")
					print(stu)
					print("\n\n\n")
					appointment.patientName = stu[0]
					appointment.rollno = stu[1]
					appointment.courseName = stu[2]
				appointments.append(appointment)
		elif forWHOM == "ADMIN":
			date = ID[0]
			category = ID[1]
			cursor.execute("SELECT date,patient_id,patient_type,name,slot_id FROM View_appointment_admin WHERE specialization=%s AND date=%s ORDER BY date",(category,date))
			tuples = cursor.fetchall()
			for tuple in tuples:
				appointment = Appointment()
				appointment.patientID = tuple[1]
				patientType = tuple[2]
				appointment.doctorName = tuple[3]
				appointment.slotID = tuple[4]
				if(patientType == "STUDENT"):
					cursor.execute("SELECT name,rollno,Course.course_name  FROM Student JOIN Course ON Student.course_id=Course.course_id AND patient_id=%s",(appointment.patientID,))
					stu = cursor.fetchone()
					print("\n\n\n")
					print(stu)
					print("\n\n\n")
					appointment.patientName = stu[0]
					appointment.rollno = stu[1]
					appointment.courseName = stu[2]
				appointments.append(appointment)

			
		return appointments



	def deleteBookedAppointment(cursor,slotID):
		cursor.execute("SELECT calendar_id FROM Appointment_slot WHERE slot_id=%s",(slotID,))
		calendarID = cursor.fetchone()[0]
		cursor.execute("SELECT slot_id FROM Appointment_slot WHERE calendar_id=%s AND status='WAITING' LIMIT 1",(calendarID,))
		tuple = cursor.fetchone()
		if tuple is not None:
			slotIDnew = tuple[0]
			cursor.execute("UPDATE Appointment_slot SET status='BOOKED' WHERE slot_id=%s",slotIDnew)
		cursor.execute("DELETE FROM Appointment_slot WHERE slot_id=%s",(slotID,))
		cursor.execute("UPDATE Appointment_calendar SET session_limit = session_limit +1 WHERE calendar_id=%s",calendarID)

	def removeOldAppointmentSlots(cursor):
		todaysDate = datetime.date.today()
		cursor.execute("DELETE FROM Appointment_calendar WHERE DATE(date)<%s",todaysDate.strftime("%Y-%m-%d"))



class Schedule():
	calendarID = None
	startTime = None
	endTime =None
	date = None

	def getCalendar(cursor,doctorID):
		schedules = list()
		cursor.execute("SELECT calendar_id,date,start_time,end_time FROM Appointment_calendar WHERE doctor_id=%s",doctorID)
		tuples = cursor.fetchall()
		for tuple in tuples:
			schedule = Schedule()
			schedule.calendarID = tuple[0]
			schedule.date = str(tuple[1])
			schedule.startTime = str(tuple[2])
			schedule.endTime = str(tuple[3])
			schedules.append(schedule)
		return schedules

	def replace(cursor,calendarID,date,startTime,endTime):
		cursor.execute('UPDATE Appointment_calendar SET date=%s ,start_time=%s ,end_time=%s WHERE calendar_id=%s',(date,startTime,endTime,calendarID))
		return True





























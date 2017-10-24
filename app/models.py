from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from . import login_manager
from flask import current_app
from . import mysql
import datetime
from itertools import groupby



class JsonSerializable:
	def getJSON(self):
		jsonDict = dict()
		for key,value in self.__dict__.items():
			if(hasattr(value,"getJSON")):
				print("KEY:"+str(key))
				jsonDict[key] = value.getJSON()
			elif(type(value) is list):
				tempList = list()
				for item in value:
					if(hasattr(item,"getJSON")):
						tempList.append(item.getJSON())
					else:
						tempList.append(item)
				jsonDict[key] = tempList

			else:
				if(isinstance(value,datetime.datetime)):
					print("\n\n"+str(key)+"\n\n")
					jsonDict[key] = str(value.strftime("%x %X"))#date time
				else:
					jsonDict[key] = value
		return jsonDict





class USER(UserMixin):
	#this name attribute shall not be put into DB.!!
	role_patient = ['STUDENT','EMPLOYEE']
	role_staff   = ['DOCTOR','PHARMA','ADMIN']
	def __init__(self):
		self.name 		  = None
		self.ID   		  = None
		self.emailID 	  = None
		self.passwordHash = None
		self.userType     = None #{DOCTOR,PHARMA,ADMIN,STUDENT,EMPLOYEE}  'ppl who can log in'
		self.userRole     = None #{PATIENT,STAFF}   'Broader category'

	def get_utype(self):
		return str(self.userType)

	def get_urole(self):
		return str(self.userRole)

	def get_mode(self):
		return self.mode
	def set_mode(self,mode):
		self.mode = mode

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
		if(USER.role_patient.__contains__(str(self.userType))):
			self.userRole = "PATIENT"
		elif(USER.role_staff.__contains__(str(self.userType))):
			self.userRole = "STAFF"
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

	def getPatientID(self,cursor):
		if(self.userType=="STUDENT"):
			cursor.execute("SELECT patient_id FROM Student WHERE rollno=%s",(self.ID,))
		else:
			cursor.execute("SELECT patient_id FROM Employee WHERE emp_id=%s",(self.ID,))
		return cursor.fetchone()[0]

	def confirmUser(self,cursor):
		cursor.execute("UPDATE User SET confirmed='YES' WHERE id=%s",(self.ID,))



	def __repr__(self):
		return '<User %r>' %self.ID





@login_manager.user_loader
def load_user(ID):
    return USER.get(ID)








class STUDENT(JsonSerializable):
	def __init__(self):
		self.rollno       = None
		self.name         = None
		self.DOB          = None
		self.sex 		  = None
		self.phno   	  = None
		self.email  	  = None
		self.guardianPhno = None
		self.locAddr      = None
		self.permAddr	  = None
		self.patientID    = None

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



class EMPLOYEE(JsonSerializable):
	def __init__(self):
		self.empID        = None
		self.name         = None
		self.DOB          = None
		self.sex 		  = None
		self.phno   	  = None
		self.email  	  = None
		self.locAddr      = None
		self.permAddr	  = None
		self.workStatus   = None
		self.designation  = None
		self.patientID    = None
		self.dependants   = None #list


	#Database to object
	def storeTuple(self,cursor,colname,value):
		cursor.execute("SELECT * FROM Employee WHERE "+colname+"=%s",(value,))
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
		self.patientID    = tuple[10]

		cursor.execute("SELECT dept_name FROM Department WHERE dept_id='"+str(tuple[11])+"'")
		tupledept         = cursor.fetchone()

		self.dept   	  = tupledept[0]
		self.blood  	  = tuple[12]
		self.dependants   = DEPENDANT.getAllDependants(cursor,self.empID)


	def checkIfExistsInDB(cursor,empID):
		cursor.execute("SELECT * FROM Employee WHERE emp_id=%s",(empID,))
		return cursor.fetchone()




class DEPENDANT(JsonSerializable):
	def __init__(self):
		self.dependantID = None
		self.empID 		 = None
		self.name  		 = None
		self.DOB 		 = None
		self.phno        = None
		self.email     = None
		self.relationship= None
		self.patientID   = None
		self.blood     = None


	def storeTuple(self,cursor,colname,value):
		cursor.execute("SELECT * FROM Dependant WHERE "+colname+"=%s ",value)
		tuple = cursor.fetchone()
		self.dependantID = tuple[0]
		self.empID 		 = tuple[1]
		self.name  		 = tuple[2]
		self.DOB 		 = tuple[3]
		self.sex		 = tuple[4]
		self.phno        = tuple[5]
		self.email       = tuple[6]
		self.relationship= tuple[7]
		self.patientID   = tuple[8]
		self.blood       = tuple[9]

	#Database to Object
	#particular dependant of a particular employee
	def _storeTuple(self,cursor,empID,dependantID):
		cursor.execute("SELECT * FROM Dependant WHERE emp_id=%s AND dependant_id=%s",(empID,dependantID))
		tuple = cursor.fetchone()
		self.dependantID = tuple[0]
		self.empID 		 = tuple[1]
		self.name  		 = tuple[2]
		self.DOB 		 = tuple[3]
		self.sex		 = tuple[4]
		self.phno        = tuple[5]
		self.email       = tuple[6]
		self.relationship= tuple[7]
		self.patientID   = tuple[8]
		self.blood       = tuple[9]


	#all dependants of a given employee
	def getAllDependants(cursor,empID):
		dependants = list()
		cursor.execute("SELECT dependant_id FROM Dependant WHERE emp_id=%s",(empID,))
		tuples = cursor.fetchall()
		for tuple in tuples:
			dependantID = tuple[0]
			dependant   = DEPENDANT()
			dependant._storeTuple(cursor,empID,dependantID)
			dependants.append(dependant)
		return dependants








class DOCTOR(JsonSerializable):
	def __init__(self):
		self.doctorID = None
		self.doctorName = None
		self.doctorSpecialization = None
		self.doctorEmployeeID = None
		self.treatmentCount = 0

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
		self.updateTreatmentCount(cursor)
		return True


	def checkIfExistsInDB(cursor,docID):
		cursor.execute("SELECT * FROM Doctor WHERE doctor_id = %s",docID)
		return cursor.fetchone()

	def updateTreatmentCount(self,cursor):
		cursor.execute("SELECT COUNT(*) FROM Prescription WHERE doctor_id=%s",self.doctorID)
		self.treatmentCount = cursor.fetchone()[0]

	def retrievePatientDetails(cursor,patientID):
		cursor.execute("SELECT patient_type FROM Patient WHERE patient_id=%s",patientID)
		type = cursor.fetchone()[0]
		if(type=="STUDENT"):
			patient = STUDENT()
		elif(type=="EMPLOYEE"):
			patient = EMPLOYEE()
		elif(type=="DEPENDANT"):
			patient = DEPENDANT()
		patient.storeTuple(cursor,"patient_id",patientID)
		return patient

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









class PrescriptionDrug(JsonSerializable):
	def __init__(self):
		self.drugName = None
		self.drugQty  = None
		self.drugSchedule = None
		self.drugComments = None
		self.drugInventory = None

	def storeData(self, drugName, drugQty, drugSchedule, drugComments, drugInventory = None):
		self.drugName 	  = drugName
		self.drugQty  	  = drugQty
		self.drugSchedule = drugSchedule
		self.drugComments = drugComments
		self.drugInventory = drugInventory




class PRESCRIPTION(JsonSerializable):


	def __init__(self):
		self.prescriptionDrugs = list()
		self.prescriptionID = None
		self.prescriptionDateTime = datetime.datetime.now()
		self.doctor = DOCTOR()
		self.patientID = None
		self.patient = None  #will become either STUDENT() or EMPLOYEEE() at run time
		self.indication = None


	def addDrug(self,drug):
		self.prescriptionDrugs.append(drug)

	#Database to object
	def storeTuple(self,cursor,prescID, view = "OTHER"):
		cursor.execute("SELECT * FROM Prescription WHERE prescription_id=%s ",(prescID,))
		tuple = cursor.fetchone()
		self.prescriptionID = tuple[0]
		self.prescriptionDateTime = tuple[1]
		#self.doctorID = tuple[2]
		self.patientID = tuple[3]
		self.indication = tuple[4]
		self.doctor.storeTuple(cursor,"doctor_id",tuple[2])

		#convention : Employees Patient ID always <9999....
		#			  Dependants :10000 - 99999
		#			  Students :  99999 - ...
		if(int(self.patientID) > 9999):
			#student
			self.patient = STUDENT()
		else:
			#employee
			self.patient = EMPLOYEE()
		self.patient.storeTuple(cursor,"patient_id",self.patientID)
		self.patient.__dict__.pop("DOB")
		if view == "PHARMA":
			cursor.execute("select P.*, SUM(B.qty) as inventory \
							from Prescription_drug_map as P, Batch as B \
							where P.drug_id = B.drug_id  \
							and prescription_id= %s \
							group by B.drug_id ", (prescID,))
		else :
			cursor.execute(" select * from Prescription_drug_map WHERE prescription_id = %s", (prescID,))

		drugtuples = cursor.fetchall()
		for drugtuple in drugtuples:
			if drugtuple[0] == None:
				return
			print(drugtuple)
			cursor.execute("SELECT trade_name FROM Drug WHERE drug_id=%s",(drugtuple[1]))
			drugName = cursor.fetchone()[0]
			prescriptionDrug = PrescriptionDrug()
			if view == "PHARMA":
				prescriptionDrug.storeData(drugName,drugtuple[2],drugtuple[3],drugtuple[4], int(drugtuple[5]))
			else:
				prescriptionDrug.storeData(drugName,drugtuple[2],drugtuple[3],drugtuple[4])
			self.prescriptionDrugs.append(prescriptionDrug)

	def modInventory(cursor, prescID):
		cursor.execute("SELECT drug_id, qty FROM Prescription_drug_map WHERE prescription_id = {} ".format(prescID))
		drugIDList = cursor.fetchall()
		remaining = []
		for (drugID, drugQty) in drugIDList:
			drugQty = int(drugQty)
			cursor.execute("SELECT * FROM Batch WHERE drug_id = {} ORDER BY exp_date ASC".format(drugID))
			batchList = cursor.fetchall()
			for batch in batchList:
				batchNo = batch[0]
				batchQty = int(batch[2])
				if batchQty >= drugQty:
					cursor.execute("UPDATE Batch SET qty = %s WHERE batch_no = %s ", (batchQty - drugQty, batchNo, ))
					break
				else:
					drugQty = drugQty - batchQty
					cursor.execute("UPDATE Batch SET qty = 0 WHERE batch_no = %s ", (batchNo,))
			remaining.append(drugQty)
		return remaining






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
		self.pushNotification(cursor)
		conn.commit()

	def pushNotification(self,cursor):
		cursor.execute("INSERT INTO Notification_buffer VALUES(%s,%s)",(self.prescriptionID,"NOT_SENT",))

	def getPrescriptions(cursor, status='NOT_SENT', view = "OTHER"):
		cursor.execute("SELECT prescription_id FROM Notification_buffer WHERE status= %s", (status,))
		tuples = cursor.fetchall()
		prescList = list()
		for tuple in tuples:
			presc = PRESCRIPTION()
			prescID = tuple[0]
			print("PRESC ID =="+str(prescID))
			presc.storeTuple(cursor,prescID, view)
			prescList.append(presc)
		if status == 'NOT_SENT':
			cursor.execute("UPDATE Notification_buffer SET status='SENT' WHERE status='NOT_SENT'")
		return prescList


	def setPrescriptionAck(cursor, presId , ackType = "ACK"):
		PRESCRIPTION.modInventory(cursor, presId)
		cursor.execute("UPDATE Notification_buffer SET status = %s WHERE prescription_id = %s", ( ackType, presId, ))

	def getPrescriptionList(cursor,mode,value):
		prescriptionList = list()
		if(mode=="BY_DATE"):
			cursor.execute("SELECT prescription_id FROM Prescription WHERE DATE(date_time)=%s",(value,))
		elif(mode=="BY_PATIENTID"):
			cursor.execute("SELECT prescription_id FROM Prescription WHERE patient_id = %s",(value,))

		prescIDtuples = cursor.fetchall()
		for prescIDtuple in prescIDtuples:
			prescription = PRESCRIPTION()
			prescription.storeTuple(cursor,prescIDtuple[0])
			prescriptionList.append(prescription)
		return prescriptionList



class DRUG(JsonSerializable):

	def __init__(self):
		self.drugName = None
		self.quantity = None
		self.batchNumber = None
		self.expiryDate = None
		self.rackID = None

	def retrieveDBdrugs(cursor):
		drugNamesList = list()
		cursor.execute("SELECT DISTINCT trade_name FROM Drug")
		drugNames = cursor.fetchall()
		for drugName in drugNames:
			drugNamesList.append(drugName[0])
		return drugNamesList

	def addNewDrug(cursor, trade_name, generic_name, rack_id):
		drugID = None
		cursor.execute("SELECT  drug_id FROM Drug WHERE trade_name=%s",trade_name)
		tuple = cursor.fetchone()
		if tuple == None:
			cursor.execute("SELECT MAX(drug_id) FROM Drug")
			drugID = cursor.fetchone()[0] + 1
		else:
			return
		print("drug id is :",drugID)
		print("genname is :",generic_name)
		print("trade_name:",trade_name)
		print("rack id :",rack_id)

		cursor.execute("INSERT INTO Drug VALUES(%s,%s,%s,%s,%s)",(drugID, generic_name, trade_name,"0", rack_id))



	def stockUpdate(cursor,drugList):
		for drug in drugList:
			cursor.execute("SELECT  drug_id FROM Drug WHERE trade_name=%s",drug.drugName)
			tuple = cursor.fetchone()
			if tuple == None:
				cursor.execute("SELECT MAX(drug_id) FROM Drug")
				drugID = cursor.fetchone()[0] + 1
				cursor.execute("INSERT INTO Drug VALUES ( {}, \"\", %s, 0) ".format(drugID), (drug.drugName,))
			else:
				drugID = tuple[0]
			cursor.execute("SELECT * FROM Batch WHERE batch_no = %s", (drug.batchNumber, ))
			batchExists = cursor.fetchone()
			print("BatchDebug = " + str(batchExists))
			if(batchExists == None):
				cursor.execute("INSERT INTO Batch VALUES(%s,%s,%s,%s)",(drug.batchNumber,drugID,drug.quantity,drug.expiryDate.strftime('%Y-%m-%d')))
			else:
				cursor.execute("UPDATE Batch SET qty = qty + {} WHERE drug_id = {}".format(int(drug.quantity), drugID,))


	def loadFullInventory(cursor):
		_druglist = []
		cursor.execute("select * from View_drug_batch_inventory")
		tuples = cursor.fetchall()
		for tuple in tuples:
			_drug = {}
			_drug["drug_id"] = tuple[0]
			_drug["generic_name"] = tuple[1]
			_drug["trade_name"] = tuple[2]
			_drug["rack_id"] = tuple[3]
			_drug["batch_no"] = tuple[4]
			_drug["qty"] = tuple[5]
			_drug["exp_date"] = str(tuple[6])
			_druglist.append(_drug)

		druglist = {}
		for _drug in _druglist:
			if(_drug["drug_id"] not in druglist):
				druglist[_drug["drug_id"]] = {"generic_name": _drug["generic_name"],
											  "trade_name"  : _drug["trade_name"],
											  "rack_id"     : _drug["rack_id"],
											  "batches": []}
			druglist[_drug["drug_id"]]["batches"].append({"batch_number":_drug["batch_no"],
														  "qty"         :_drug["qty"],
														  "exp_date"    :_drug["exp_date"]})
		return druglist




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
		cursor.execute("SELECT slot_id FROM Appointment_slot WHERE patient_id=%s AND calendar_id=%s",(patientID,calendarID))
		return cursor.fetchone()[0]

	def commitSubmittedAppointmentIntoDB_admin(cursor,calendarID,rollno):
		cursor.execute("INSERT INTO Appointment_slot (patient_id,calendar_id) VALUES ((SELECT patient_id FROM Student WHERE rollno=%s),%s)",(rollno,calendarID))
		cursor.execute("UPDATE Appointment_calendar SET session_limit = session_limit -1 WHERE calendar_id=%s",calendarID)


	def getBookedAppointments(cursor,ID,forWHOM):
		appointments = list()
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
				cursor.execute("SELECT name  FROM {} WHERE patient_id={}".format(patientType.title(), appointment.patientID))
				pat = cursor.fetchone()
				appointment.patientName = pat[0]
				appointment.patientType = patientType.title()
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
		print(calendarID, date, startTime, endTime)
		cursor.execute('UPDATE Appointment_calendar SET date=%s ,start_time=%s ,end_time=%s WHERE calendar_id=%s',(date,startTime,endTime,calendarID))
		return True

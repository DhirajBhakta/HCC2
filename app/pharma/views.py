from flask import render_template, request ,redirect
from .. import mysql
from ..models import STUDENT, PRESCRIPTION, Appointment,DRUG
from ..utils import specific_login_required
from . import pharma
from flask_login import current_user, login_required
import json
from datetime import datetime

@pharma.route("/",methods=['GET'])
@specific_login_required("PHARMA")
def showNotifications():
	return render_template("pharma/notifications.html")



@pharma.route("/stockUpdate",methods=['GET','POST'])
@specific_login_required("PHARMA")
def stockUpdate():
	conn = mysql.connect()
	cursor = conn.cursor()
	if request.method == 'POST':
		jsonDict = request.get_json(silent=True)
		drugList = []
		for value in jsonDict:
			drug = DRUG()
			drug.batchNumber=value['batchnumber']
			drug.drugName   =value['drugname']
			drug.quantity   =value['quantity']
			date = value['expirydate']
			drug.expiryDate = datetime.strptime(date,'%d/%m/%Y')
			drugList.append(drug)
		print(drugList)
		DRUG.stockUpdate(cursor,drugList)
		conn.commit()	
		return json.dumps({"success" : "true"}), 200	
	
	druglist = DRUG.retrieveDBdrugs(cursor)
	druglist = [""]+druglist
	return render_template('pharma/stockUpdate.html',druglist=druglist)



@pharma.route("/getDruglist",methods=['GET'])
@specific_login_required("PHARMA")
def getDruglist():
	conn = mysql.connect()
	cursor = conn.cursor()
	druglist = DRUG.retrieveDBdrugs(cursor)
	druglist = [""]+druglist
	json_string = json.dumps(druglist)
	return json_string




@pharma.route("/getNOT_SENT",methods=['GET'])
@specific_login_required("PHARMA")
def getNOT_SENT():
	conn = mysql.connect()
	cursor = conn.cursor()
	presclist = PRESCRIPTION.getNOT_SENTprescriptions(cursor)
	conn.commit()
	json_string = json.dumps([obj.__dict__ for obj in presclist])
	return json_string


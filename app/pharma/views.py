from flask import render_template, request ,redirect
from .. import mysql
from ..models import STUDENT, PRESCRIPTION, Appointment,DRUG
from . import pharma
from flask_login import current_user, login_required
import json

@pharma.route("/",methods=['GET'])
def stockUpdate():
	conn = mysql.connect()
	cursor = conn.cursor()
	druglist = DRUG.retrieveDBdrugs(cursor)
	druglist = [""]+druglist

	return render_template('pharma/stockUpdate.html',druglist=druglist)


@pharma.route("/stockUpdateSubmit",methods=['POST'])
def stockUpdateSubmit():
	json = request.get_json(silent=True)
	print (json)
	return render_template('pharma/success.html')

@pharma.route("/getDruglist",methods=['GET'])
def getDruglist():
	conn = mysql.connect()
	cursor = conn.cursor()
	druglist = DRUG.retrieveDBdrugs(cursor)
	druglist = [""]+druglist
	json_string = json.dumps(druglist)
	return json_string





from flask import render_template, redirect ,request,url_for ,flash, current_app,jsonify
from flask_login import login_user , logout_user, current_user,login_required
from . import admin
from ..models import USER,STUDENT,DOCTOR
from .. import mysql,mail
from ..email import send_email
from flask_mail import Message


@admin.route('/reschedule',methods=['GET','POST'])
def reschedule():
	conn = mysql.connect()
	cursor = conn.cursor()
	if request.method == 'POST':
		lastDate = request.form.get('LASTDATE')
		if lastDate is not None:
			datestr = lastDate.split('-')
			lastDateStr = datestr[2]+"-"+datestr[1]+"-"+datestr[0]
			cursor.execute("CALL fill_calendar(%s)",(lastDateStr,))
			conn.commit()
			flash('Appointment Slots Created! till '+lastDate)
			return redirect(url_for('auth.reschedule'))
		#AppointmentDetails =
	return render_template('admin/reschedule.html') 


@admin.route('/retrieveBookedAppointments',methods=['GET'])
def retrieveBookedAppointments():
	conn = mysql.connect()
	cursor = conn.cursor()
	date = request.args.get('DATE')
	category = request.args.get('CATEGORY')
	print(date)
	print(category)
	



@admin.route('/appointments',methods=['GET','POST'])
def appointments():
	conn = mysql.connect()
	cursor = conn.cursor()
	if request.method == 'POST':
		pass

	else:
		return render_template('admin/appointment.html')
		
		
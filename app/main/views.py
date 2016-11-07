from flask import session, render_template, url_for, redirect
from . import main
from flask_login import current_user
from .. import mysql
from ..models import Appointment


@main.route('/')
def index():
	'''if current_user.is_authenticated:
		return redirect(url_for('student.showStudentProfile'))'''
	conn = mysql.connect()
	cursor = conn.cursor()
	conn.commit()
	return redirect(url_for("auth.login"))







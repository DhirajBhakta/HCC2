from flask import render_template
from .. import mysql
from ..models import STUDENT
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
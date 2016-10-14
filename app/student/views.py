from flask import render_template
from . import student

@student.route("/profile")
def showStudentProfile():
	return render_template("student/studentprofile.html")
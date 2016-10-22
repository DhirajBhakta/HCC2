from flask import session, render_template, url_for, redirect
from . import main
from flask_login import current_user


@main.route('/')
def index():
	'''if current_user.is_authenticated:
		return redirect(url_for('student.showStudentProfile'))'''
	return render_template('index.html')







from flask import session, render_template
from . import main
from flask_login import current_user


@main.route('/')
def index():
	if current_user.is_authenticated:
		return render_template("student/studentprofile.html")
	return render_template('index.html')







from flask import render_template, redirect ,request,url_for ,flash, current_app,jsonify
from flask_login import login_user
from . import auth
from ..models import StudentUser
from .forms import LoginForm ,RegistrationForm
from .. import mysql


@auth.route('/login',methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		cursor = mysql.connect().cursor()
		student_data = StudentUser.checkIfRollnoExists(cursor,form.rollno.data)
		if student_data is not None:
			student_this = StudentUser()
			student_this.storeTuple(student_data)
			if student_this.verify_password(form.password.data):
				#login_user(student_this)
				cursor.execute("SELECT * FROM Student WHERE rollno='"+student_this.rollno+"'")
				studentdata = cursor.fetchone()
				return  render_template('studentprofile.html',stu = studentdata)
		flash('Invalid UserName or Password.')
	return render_template('auth/login.html',form=form)



@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        student_new = StudentUser()
        student_new.storeData(form.rollno.data,form.name.data,form.email.data,form.password.data)
        
        cursor = mysql.connect().cursor()
        student_new.commit(cursor)
   
       # token = student_new.generate_confirmation_token()
        '''send_email(student_new.email, 'Confirm Your Account',
                   'auth/email/confirm', user=user, token=token)'''
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)




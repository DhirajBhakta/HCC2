from flask import render_template, redirect ,request,url_for ,flash, current_app,jsonify
from flask_login import login_user , logout_user, current_user,login_required
from . import auth
from ..models import USER,STUDENT
from .forms import LoginForm ,RegistrationForm
from .. import mysql,mail
from ..email import send_email
from flask_mail import Message


@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        cursor = mysql.connect().cursor()
        user   = USER.checkIfIDExists(cursor,form.ID.data)
        if user is not None:
            if user.verify_password(form.password.data):
                type = form.patientType.data
                if (type=='1'):
                    studentUser = STUDENT()
                    studentUser.storeTuple(cursor,user.ID)
                    login_user(studentUser)
                    return  render_template('studentprofile.html',stu = studentUser)
				
				#do this after Employee model is finalized
            else:
                flash('Invalid UserName or Password.')
        else:
            flash('Invalid UserName or Password. user object is None')
    return render_template('auth/login.html',form=form)


@auth.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('main.index'))



@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        newUser = USER()
        newUser.storeData(form.name.data,form.ID.data,form.email.data,form.password.data)
        conn = mysql.connect()
        cursor = conn.cursor()
        newUser.insertIntoDB(cursor)
        conn.commit()
        token = newUser.generate_confirmation_token()
        send_email(newUser.emailID, 'Confirm Your Account',
                   'auth/email/confirm', user=newUser, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('main.index'))
    if (request.method == "POST"):
    	flash(form.errors)
    return render_template('auth/register.html', form=form)



@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))









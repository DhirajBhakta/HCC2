from flask import render_template, redirect ,request,url_for ,flash, current_app,jsonify
from flask_login import login_user , logout_user, current_user,login_required
from . import auth
from ..models import USER,STUDENT,DOCTOR
from .forms import LoginForm ,RegistrationForm ,DoctorLoginForm
from .. import mysql,mail
from ..email import send_email
from flask_mail import Message

#patient Login(STUDENT,EMPLOYEE)
@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        cursor = mysql.connect().cursor()
        user   = USER.checkIfIDExists(cursor,form.ID.data)
        if user is not None:
            if not user.isConfirmed(cursor):
                flash('Email ID not confirmed! Please click on the link given to you via email', 'danger')
                return render_template('auth/login.html',form=form)          
            if user.verify_password(form.password.data):
                login_user(user)
                return  redirect(url_for('patient.showPatientProfile'))
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
        newUser.storeData(form.name.data,form.ID.data,form.email.data,form.password.data,form.patientType.data)
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
def confirm(token):
    ID = USER.getUserIDFromToken(token)
    conn = mysql.connect()
    cursor = conn.cursor()
    
    user = USER()
    user = USER.checkIfIDExists(cursor,ID)

    if user is not None:    
        user.confirm(token,cursor)
        flash('You have confirmed your account. Thanks!')
        conn.commit()
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))



@auth.route('/login/doctor',methods=['GET','POST'])
def loginDoctor():
    form = DoctorLoginForm()
    if form.validate_on_submit():
        cursor = mysql.connect().cursor()
        thisDoctor = DOCTOR()
        thisDoctor.storeTuple(cursor,"doctor_id",form.doctorID.data)
        thisUser = USER()
        thisUser = USER.checkIfIDExists(cursor,thisDoctor.doctorEmployeeID)
        if thisUser.verify_password(form.password.data):
            login_user(thisUser)
            print(thisUser.get_utype())
            return redirect(url_for('doctor.showWorkbench'))
        else:
            flash('Invalid doctorID or password.')
    return render_template('auth/doctorlogin.html',form=form)

@auth.route('/login/admin',methods=['GET','POST'])
def loginAdmin():
    if request.method == 'POST':
        cursor = mysql.connect().cursor()
        password = request.form.get('PASSWORD')
        thisUser = USER.checkIfIDExists(cursor,"admin")
        if thisUser.verify_password(password):
            login_user(thisUser)
            return redirect(url_for('admin.appointments'))
        else:
            flash('Invalid Password')
    return render_template('auth/adminlogin.html')


@auth.route('/login/pharma',methods=['GET','POST'])
def loginPharma():
    if request.method == 'POST':
        cursor = mysql.connect().cursor()
        password = request.form.get('PASSWORD')
        thisUser = USER.checkIfIDExists(cursor,"pharma")
        if thisUser.verify_password(password):
            login_user(thisUser)
            return redirect(url_for('pharma.stockUpdate'))
        else:
            flash('Invalid Password')
    return render_template('auth/pharmalogin.html')







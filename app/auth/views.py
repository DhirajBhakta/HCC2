from flask import render_template, redirect ,request,url_for ,flash
from flask_login import login_user
from . import auth
from ..models import StudentUser
from .. import db
from .forms import LoginForm ,RegistrationForm

@auth.route('/login',methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		student_this = StudentUser.query.filter_by(rollno = form.rollno.data).first()
		if student_this is not None and student_this.verify_password(form.password.data):
			login_user(student_this)
			return redirect(request.args.get('next') or usrl_for('main.index'))
		flash('Invalid UserName or Password.')
	return render_template('auth/login.html',form=form)



@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        student_new = StudentUser(rollno=form.rollno.data,name=form.name.data,email=form.email.data)
        student_new.make_passwordHash(form.password.data)
 
        db.session.add(student_new)
        db.session.commit()
       # token = student_new.generate_confirmation_token()
        '''send_email(student_new.email, 'Confirm Your Account',
                   'auth/email/confirm', user=user, token=token)'''
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)
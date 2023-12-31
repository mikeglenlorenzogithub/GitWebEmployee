from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from .models import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_admin = User.query.filter_by(user_name='admin').first()
        if not user_admin:
            user_name = 'admin'
            user_email = 'admin@inticorporatechnology.com'
            user_password = 'admin'
            user_password = generate_password_hash(user_password, method='scrypt')

            #create admin to the database
            new_admin = User(user_name, user_email, user_password)
            db.session.add(new_admin)
            db.session.commit()

        else:
            pass

        email_name = request.form.get('email-name')
        password = request.form.get('password')

        user = User.query.filter_by(user_email=email_name).first()
        user = User.query.filter_by(user_name=email_name).first() if not user else user

        if user:
            if check_password_hash(user.user_password, password):
                flash('Logged in succesfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again!', category='error')
        else:
            flash('Email Address or User Name does not exist!', category='error')
    
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
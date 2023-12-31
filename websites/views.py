from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from flask_login import login_required, current_user
import pandas as pd
from io import BytesIO, StringIO
from . import db
from .models import Employees

views = Blueprint('views', __name__)

# ===== VIEWS(ROUTE) =====>
@views.route('/')
def home():
    all_employees = Employees.query.all()

    return render_template('home.html', employees=all_employees, user=current_user)

@views.route('/create', methods=['POST'])
@login_required
def create():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']

        exist_email = Employees.query.filter_by(email=email).first()

        if exist_email:
            flash('Email already exist.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(name) < 2:
            flash('Name must be greater than 1 characters.', category='error')
        elif len(phone) < 8 or len(phone) > 13:
            flash('Phone number must be greater than 7 characters and less than 13 characters.', category='error')
        elif len(address) < 4:
            flash('Address must be greater than 3 characters.', category='error')
        else:
            #create employee to the database
            new_employee = Employees(name, email, phone, address)
            db.session.add(new_employee)
            db.session.commit()

            flash('New Employee Added Successfully!', category='success')

        return redirect(url_for('views.home'))

@views.route('/update', methods=['GET', 'POST'])
@login_required
def update():

    if request.method == 'POST':
        exist_employee = Employees.query.get(request.form.get('id'))

        new_name = request.form['name']
        new_email = request.form['email']
        new_phone = request.form['phone']
        new_address = request.form['address']

        exist_email = Employees.query.filter_by(email=new_email).first()

        print(exist_email)
        print(exist_employee)

        if exist_email != exist_employee and exist_email:
            flash('Email already exist.', category='error')
        elif len(new_email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(new_name) < 2:
            flash('Name must be greater than 1 characters.', category='error')
        elif len(new_phone) < 8 or len(new_phone) > 13:
            flash('Phone number must be greater than 7 characters and less than 14 characters.', category='error')
        elif len(new_address) < 6:
            flash('Address must be greater than 5 characters.', category='error')
        else:
            #update employee to the database
            exist_employee.name = new_name
            exist_employee.email = new_email
            exist_employee.phone = new_phone
            exist_employee.address = new_address
            db.session.commit()

            flash('Employee Edited Successfully!', category='success')

        return redirect(url_for('views.home'))

@views.route('/delete/<id>/', methods=['GET', 'POST'])
@login_required
def delete(id):
    exist_employee = Employees.query.get(id)
    db.session.delete(exist_employee)
    db.session.commit()

    flash('Employee Deleted Successfully!', category='success')

    return redirect(url_for('views.home'))

@views.route('/multi', methods=['GET', 'POST'])
@login_required
def multi():
    if request.method == 'POST':
        file = request.files['upload']
        if 'csv' not in file.filename:
            flash('File extension should be csv', category='error')
        else:
            file_upload = pd.read_csv(file)
            if 'Name' not in list(file_upload.columns):
                flash('Column Name not found in file!', category='error')
                return redirect(url_for('views.home'))
            elif 'Email' not in list(file_upload.columns):
                flash('Column Email not found in file!', category='error')
                return redirect(url_for('views.home'))
            elif 'Phone' not in list(file_upload.columns):
                flash('Column Phone not found in file!', category='error')
                return redirect(url_for('views.home'))
            elif 'Address' not in list(file_upload.columns):
                flash('Column Address not found in file!', category='error')
                return redirect(url_for('views.home'))
            elif 'No' not in list(file_upload.columns):
                flash('Column No. not found in file!', category='error')
                return redirect(url_for('views.home'))
            else:
                file_upload.rename(columns={'Name': 'name', 'Email': 'email', 'Phone': 'phone', 'Address': 'address'}, inplace=True)

            count_before = len(Employees.query.all())
            for index in range(len(file_upload)):
                row = file_upload.loc[index]

                name = row['name']
                email = row['email']
                phone = str(row['phone'])
                phone = f'0{phone}' if not phone.startswith('0') else phone
                address = row['address']

                exist_email = Employees.query.filter_by(email=email).first()

                if exist_email:
                    flash(f'{row["No"]}, {row["email"]} Email already exist.', category='error')
                elif len(email) < 4:
                    flash(f'{row["No"]}, {row["email"]} Email must be greater than 3 characters.', category='error')
                elif len(name) < 2:
                    flash(f'{row["No"]}, {row["name"]} Name must be greater than 1 characters.', category='error')
                elif len(phone) < 8 or len(phone) > 13:
                    flash(f'{row["No"]}, {row["phone"]} Phone number must be greater than 7 characters and less than 14 characters.', category='error')
                elif len(address) < 4:
                    flash(f'{row["No"]}, {row["address"]} Address must be greater than 3 characters.', category='error')
                else:
                    #create employee to the database
                    new_employee = Employees(name, email, phone, address)
                    db.session.add(new_employee)
                    db.session.commit()

            count_after = len(Employees.query.all())
            if count_after == count_before:
                flash(f'Fail to Add Multiple New Employee from {file.filename}!', category='error')
            else:
                flash(f'Multiple New Employee Added Successfully from {file.filename}!', category='success')

        return redirect(url_for('views.home'))

@views.route('/download', methods=['GET', 'POST'])
def download():
    content = list()
    all_employees = Employees.query.all()
    for employee in all_employees:
        data_dict = {}
        data_dict['ID'] = employee.id
        data_dict['Name'] = employee.name
        data_dict['Email'] = employee.email
        data_dict['Phone'] = employee.phone
        data_dict['Address'] = employee.address

        content.append(data_dict)
        print(data_dict)
    
    df = pd.DataFrame(content)

    csv_df = df.to_csv(index=False, header=True)
    string_df = StringIO(csv_df)

    return send_file(BytesIO(string_df.read().encode("utf-8")), mimetype="text/csv", download_name='employees_data.csv')

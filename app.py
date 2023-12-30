from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

DB_NAME = 'database.db'
app.config['SECRET_KEY'] = 'abcdfghi jklmnopq rstuvwxy'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
# initialize the app with Flask-SQLAlchemy
db = SQLAlchemy(app)

class Employees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    phone = db.Column(db.String(150))

    def __init__(self, name, email, phone): 
        self.name = name
        self.email = email
        self.phone = phone

with app.app_context():
    db.create_all()
    print('Create Database!')

@app.route('/')
def home():
    all_employees = Employees.query.all()

    return render_template('home.html', employees=all_employees)

@app.route('/create', methods=['POST'])
def create():

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        exist_email = Employees.query.filter_by(email=email).first()

        if exist_email:
            flash('Email already exist.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(name) < 2:
            flash('First name must be greater than 1 characters.', category='error')
        elif len(phone) < 8 or len(phone) > 13:
            flash('Phone number must be greater than 7 characters and less than 13 characters.', category='error')
        else:
            #create employee to the database
            new_employee = Employees(name, email, phone)
            db.session.add(new_employee)
            db.session.commit()

            flash('New Employee Added Successfully!', category='success')

        return redirect(url_for('home'))

@app.route('/update', methods=['GET', 'POST'])
def update():

    if request.method == 'POST':
        exist_employee = Employees.query.get(request.form.get('id'))

        new_name = request.form['name']
        new_email = request.form['email']
        new_phone = request.form['phone']

        if len(new_email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(new_name) < 2:
            flash('First name must be greater than 1 characters.', category='error')
        elif len(new_phone) < 8 or len(new_phone) > 13:
            flash('Phone number must be greater than 7 characters and less than 13 characters.', category='error')
        else:
            #update employee to the database
            exist_employee.name = new_name
            exist_employee.email = new_email
            exist_employee.phone = new_phone
            db.session.commit()

            flash('Employee Edited Successfully!', category='success')

        return redirect(url_for('home'))

@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    exist_employee = Employees.query.get(id)
    db.session.delete(exist_employee)
    db.session.commit()

    flash('Employee Deleted Successfully!', category='success')

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
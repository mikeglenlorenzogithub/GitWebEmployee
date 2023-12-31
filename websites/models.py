from flask_login import UserMixin
from . import db

class Employees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    phone = db.Column(db.String(150))
    address = db.Column(db.String(150))

    def __init__(self, name, email, phone, address): 
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(150))
    user_email = db.Column(db.String(150), unique=True)
    user_password = db.Column(db.String(150))

    def __init__(self, user_name, user_email, user_password): 
        self.user_name = user_name
        self.user_email = user_email
        self.user_password = user_password
from . import db
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.sql import func


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(30), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    payment_method = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    mobile_number = db.Column(db.String(10))
    password = db.Column(db.String(20))
    expenses = db.relationship('Expense', backref='user', lazy=True)

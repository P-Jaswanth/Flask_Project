from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from collections import defaultdict
from .models import Expense
from datetime import datetime



from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        date_str = request.form.get('date')
        date = datetime.strptime(date_str, '%Y-%m-%d')
        category = request.form.get('category')
        amount = request.form.get('amount')
        description = request.form.get('description')
        payment_method = request.form.get('payment_method')
        expense = Expense(date = date,category=category, amount = amount,description= description,payment_method= payment_method,user_id = current_user.id)
        db.session.add(expense) #adding the note to the database 
        db.session.commit()
        flash('Successfully Added', category='success')

    return render_template("home.html", user=current_user)



@views.route('/pie_chart')
def pie_chart():
    expenses = Expense.query.all()
    category_expenses = defaultdict(int)
    for expense in expenses:
        category_expenses[expense.category] += expense.amount
    chart_data = [['Category', 'Total Expenses']]
    for category, total in category_expenses.items():
        chart_data.append([category, total])
    return render_template('pie_chart.html', chart_data=chart_data)


@views.route('/records', methods=['GET'])
@login_required
def records():
    expenses = current_user.expenses
    if expenses:
        return render_template('records.html',expenses = expenses, user=current_user)
    else:
        flash('No records to display')
        return render_template('home.html',user=current_user)

@views.route('/profile', methods=['GET'])
@login_required
def profile():
    return render_template("profile.html", user=current_user)



@views.route('/daily_chart')
def daily_chart():
    expenses = Expense.query.all()
    daily_expenses = {}
    for expense in expenses:
        day = expense.date.strftime('%d %b %Y')
        if day not in daily_expenses:
            daily_expenses[day] = 0
        daily_expenses[day] += expense.amount
    chart_data = [['Day', 'Total Expenses']]
    for day, total in daily_expenses.items():
        chart_data.append([day, total])
    return render_template('daily_chart.html', chart_data=chart_data, user=current_user)
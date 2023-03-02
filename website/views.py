from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from collections import defaultdict
from .models import Expense
from datetime import datetime
from sqlalchemy import func,extract,desc
import calendar



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
    
    expenses = Expense.query.filter_by(user_id=current_user.id).order_by(desc(Expense.date)).all()
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
@login_required
def daily_chart():
    expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.date).all()
    total_expenses = sum(expense.amount for expense in expenses)
    current_month = datetime.now().month
    current_year = datetime.now().year
    month_number = current_month
    month_name = calendar.month_name[month_number]

    # Query the expenses for the current month and year
    exp = Expense.query.filter(
        extract('month', Expense.date) == current_month,
        extract('year', Expense.date) == current_year
    ).filter_by(user_id=current_user.id).order_by(Expense.date).all()

    # Calculate the total expenses
    monthly_expenses = sum(expense.amount for expense in exp)
    if expenses:
        daily_expenses = {}
        for expense in expenses:
            day = expense.date.strftime('%d %b %Y')
            if day not in daily_expenses:
                daily_expenses[day] = 0
            daily_expenses[day] += expense.amount
        chart_data = [['Day', 'Total Expenses']]
        for day, total in daily_expenses.items():
            chart_data.append([day, total])
        return render_template('daily_chart.html', chart_data=chart_data, user=current_user,monthly_expenses=monthly_expenses,total_expenses=total_expenses,month_name=month_name)
      
    else:
        flash('No Epenses Added')
        return render_template('home.html',user=current_user,total_expenses=total_expenses)
    
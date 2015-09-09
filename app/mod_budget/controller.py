from flask import Blueprint, flash, redirect, render_template, request, session, \
    url_for
from wtforms.fields.html5 import DecimalRangeField
from bson.objectid import ObjectId

from app import logger
from app.mod_budget.form import AddEntryForm, EditBudgetForm
from app.mod_budget.model import Category, CategoryBudget, Expense, Income
from app.mod_auth.helper import requireAuth
from app.mod_auth.model import User

budget = Blueprint('budget', __name__, template_folder = 'templates')

@budget.route('/')
@requireAuth()
def default():
    return "Hello World!"

@budget.route('/income/add', methods = ['GET', 'POST'])
@requireAuth()
def addIncome():
    form = AddEntryForm(request.form)
    # Load the categories from the DB into the SelectField
    form.loadCategories()

    if request.method == 'POST' and form.validate():
        income = Income()
        form.populate_obj(income)

        # Insert category into the ReferenceField.
        income.category = Category.objects(id = ObjectId(income.category)).first()
        # Insert owner into the ReferenceField.
        userId = ObjectId(session.get('user')['_id']['$oid'])
        income.owner = User.objects(id = userId).first()
        income.save()

        logger.debug('{0} added Income({1}, {2}, {3})'.format(
            session.get('user')['username'], income.amount, income.description,
                income.category.name))

        flash('Your income has been added.')
        return redirect(url_for('budget.default'))
    return render_template('budget/income/add.html', form = form)

@budget.route('/income/delete/<id>')
@requireAuth()
def deleteIncome(id):
    # Fetch the appropiate entry from the collection.
    userId = ObjectId(session.get('user')['_id']['$oid'])
    income = Income.objects(id = ObjectId(id), owner = userId).first()
    logger.debug('Trying to delete ({0}, {1})'.format(ObjectId(id), userId))

    if income is not None:
        logger.debug('Trying to delete income {0}'.format(income.id))
        income.delete()

        flash('Your entry has been deleted.')
    else:
        flash('You are not authorized to delete this entry.')
    return redirect(url_for('budget.default'))

@budget.route('/expense/add', methods = ['GET', 'POST'])
@requireAuth()
def addExpense():
    form = AddEntryForm(request.form)
    # Load the categories from the DB into the SelectField
    form.loadCategories()

    if request.method == 'POST' and form.validate():
        expense = Expense()
        form.populate_obj(expense)

        # Insert category into the ReferenceField.
        expense.category = Category.objects(id = ObjectId(expense.category)).first()
        # Insert owner into the ReferenceField.
        userId = ObjectId(session.get('user')['_id']['$oid'])
        expense.owner = User.objects(id = userId).first()
        expense.save()

        logger.debug('{0} added Income({1}, {2}, {3})'.format(
            session.get('user')['username'], expense.amount, expense.description,
                expense.category.name))

        flash('Your expense has been added.')
        return redirect(url_for('budget.default'))
    return render_template('budget/expense/add.html', form = form)

@budget.route('/expense/delete/<id>')
@requireAuth()
def deleteExpense(id):
    # Fetch the appropiate entry from the collection.
    userId = ObjectId(session.get('user')['_id']['$oid'])
    expense = Expense.objects(id = ObjectId(id), owner = userId).first()
    logger.debug('Trying to delete ({0}, {1})'.format(ObjectId(id), userId))

    if expense is not None:
        logger.debug('Trying to delete expense {0}'.format(expense.id))
        expense.delete()

        flash('Your entry has been deleted.')
    else:
        flash('You are not authorized to delete this entry.')
    return redirect(url_for('budget.default'))

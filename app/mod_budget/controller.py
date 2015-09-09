from flask import Blueprint, flash, redirect, render_template, request, session, \
    url_for
from wtforms.fields.html5 import DecimalRangeField
from bson.objectid import ObjectId

from app import logger
from app.mod_budget.form import AddEntryForm, EditBudgetForm
from app.mod_budget.model import Category, Entry
from app.mod_auth.helper import requireAuth
from app.mod_auth.model import User

budget = Blueprint('budget', __name__, template_folder = 'templates')

@budget.route('/')
@requireAuth()
def default():
    return "Hello World!"

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

@budget.route('/income/add', methods = ['GET', 'POST'])
@requireAuth()
def addIncome():
    return addEntry('/budget/income/add.html', asAsset = True)

@budget.route('/expense/add', methods = ['GET', 'POST'])
@requireAuth()
def addExpense():
    return addEntry('/budget/expense/add.html', asAsset = False)

def addEntry(template, asAsset = False):
    form = AddEntryForm(request.form)
    # Load the categories from the DB into the SelectField
    form.loadCategories()

    if request.method == 'POST' and form.validate():
        entry = Entry()
        form.populate_obj(entry)

        # If this is an expense, multiply the amount by (-1).
        if not asAsset:
            entry.amount = entry.amount * (-1)

        # Insert category into the ReferenceField.
        entry.category = Category.objects(id = ObjectId(entry.category)).first()
        # Insert owner into the ReferenceField.
        userId = ObjectId(session.get('user')['_id']['$oid'])
        entry.owner = User.objects(id = userId).first()
        entry.save()

        logger.debug('{0} added Income({1}, {2}, {3})'.format(
            session.get('user')['username'], entry.amount, entry.description,
                entry.category.name))

        flash('Your entry has been added.')
        return redirect(url_for('budget.default'))
    return render_template(template, form = form)

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
    return redirect(url_for('budget.showSummary'))

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

@budget.route('/entry/delete/<id>')
@requireAuth()
def deleteEntry(id):
    # Fetch the appropiate entry from the collection.
    userId = ObjectId(session.get('user')['_id']['$oid'])
    expense = Entry.objects(id = ObjectId(id), owner = userId).first()
    logger.debug('Trying to delete ({0}, {1})'.format(ObjectId(id), userId))

    if expense is not None:
        logger.debug('Trying to delete expense {0}'.format(expense.id))
        expense.delete()

        flash('Your entry has been deleted.')
    else:
        flash('You are not authorized to delete this entry.')
    return redirect(url_for('budget.default'))

@budget.route('/summary')
@requireAuth()
def showSummary():
    # # Get the sum of all assets the user added.
    # userId = ObjectId(session.get('user')['_id']['$oid'])
    # assetSum = sum([entry.amount for entry in Entry.objects(owner = userId).all()
    #     if entry.amount > 0])
    #
    # expensePerCategory = {}
    # for category in Category.objects().all():
    #     expensePerCategory.update({category.name : 0})
    #
    # for entry in Entry.objects(owner = userId).all():
    #     categoryName = Category.objects(id = entry.category.id).first().name
    #     if entry.amount < 0:
    #         expensePerCategory[categoryName] = expensePerCategory[categoryName] - \
    #             entry.amount
    #
    # expenseSum = 0
    # for _, amount in expensePerCategory.items():
    #     expenseSum = expenseSum + amount
    #
    # return render_template('/budget/summary.html', total = assetSum, expenseSum = expenseSum,
    #     expensePerCategory = expensePerCategory)

    # Load all entries of the current user into a list.
    entries = []

    sumIncome = 0

    expensePerCategory = {}
    for category in Category.objects().all():
        expensePerCategory.update({category.name : 0})

    userId = ObjectId(session.get('user')['_id']['$oid'])
    for entry in Entry.objects(owner = userId).all():
        e = {'_id' : entry.id, 'amount' : entry.amount,
            'description' : entry.description,
                'category' : Category.objects(id = entry.category.id).first().name}
        entries.append(e)

        if e['amount'] > 0:
            sumIncome = sumIncome + e['amount']
        else:
            expensePerCategory[e['category']] = \
                expensePerCategory[e['category']] - e['amount']


    logger.debug('Currency: {0}'.format(session.get('currency')))

    return render_template('/budget/summary.html',
        entries = entries, sumIncome = sumIncome,
            expensePerCategory = expensePerCategory)

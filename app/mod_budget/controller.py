from flask import Blueprint, flash, redirect, render_template, request, url_for

from bson.objectid import ObjectId

from app import logger
from app.mod_budget.form import AddEntryForm
from app.mod_budget.model import Category, Entry, loadCategories

from app.mod_auth.helper import requireAuth

budget = Blueprint('budget', __name__, template_folder = 'templates')

@budget.route('/')
@requireAuth()
def default():
    return "Hello World!"

@budget.route('/entry/add', methods = ['GET', 'POST'])
@requireAuth()
def addEntry():
    form = AddEntryForm(request.form)
    # Load the categories from the db into the SelectField
    form.category.choices = loadCategories()

    if request.method == 'POST' and form.validate():
        entry = Entry()
        form.populate_obj(entry)

        logger.debug(form.category.data)
        # Insert category into reference field.
        entry.category = Category.objects(id = ObjectId(entry.category)).first()

        entry.save()
        logger.info('A new entry has been saved.')
        flash('Your entry has been added.')
        return redirect(url_for('budget.default'))
    return render_template('budget/entry/add.html', form = form)

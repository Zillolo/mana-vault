from flask import Blueprint, render_template, request

from app.mod_budget.form import AddEntryForm
from app.mod_budget.model import loadCategories

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
    form.category.choices = loadCategories()

    if request.method == 'POST' and form.validate():
        return "Lettn"
    return render_template('budget/entry/add.html', form = form)

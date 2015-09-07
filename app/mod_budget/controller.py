from flask import Blueprint

budget = Blueprint('budget', __name__, template_folder = 'templates')

@budget.route('/')
def default():
    return "Hello World!"

"""
This module holds all view functions for the authentication module.

These functions include the following:
"""

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.mod_auth.form import RegistrationForm
from app.mod_auth.helper import requireAuth, generateHash
from app.mod_auth.model import AuthLevel, User

auth = Blueprint('auth', __name__, template_folder = 'templates')

@auth.route('/')
def default():
    return redirect(url_for('auth.info'))

@auth.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)

    if request.method == 'POST' and form.validate():
        print("POST called and validated.")

        user = User()
        form.populate_obj(user)
        user.password = generateHash(user.password)

        user.save()
        flash('Your user account has been created.')
        return redirect(url_for('auth.info'))
    return render_template('auth/registration.html', form = form)

@auth.route('/info')
def info():
    return "This is a test."

"""
This module holds all view functions for the authentication module.

These functions include the following:
"""

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.mod_auth.form import LoginForm, RegistrationForm
from app.mod_auth.helper import onAuthRedirect, requireAuth, generateHash
from app.mod_auth.model import AuthLevel, User

auth = Blueprint('auth', __name__, template_folder = 'templates')

@auth.route('/')
def default():
    return redirect(url_for('auth.info'))

@auth.route('/register', methods = ['GET', 'POST'])
@onAuthRedirect()
def register():
    form = RegistrationForm(request.form)

    if request.method == 'POST' and form.validate():
        user = User()
        form.populate_obj(user)
        user.password = generateHash(user.password)
        user.authLevel = AuthLevel.USER

        user.save()

        logger.debug('A user has been added.')
        flash('Your user account has been created.')
        return redirect(url_for('auth.default'))
    return render_template('auth/registration.html', form = form)

@auth.route('/login', methods = ['GET', 'POST'])
@onAuthRedirect()
def login():
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        user = User.objects(username = form.username.data).first()
        if user is not None:
            if user.password == generateHash(form.password.data):
                session['user'] = user
                return redirect(url_for('auth.default'))

        logger.debug('User %s has logged in.' % user.username)
        flash('The specified username and/or password were incorrect.')
    return render_template('auth/login.html', form = form)

@auth.route('/logout')
@requireAuth()
def logout():
    logger.debug('User %s has logged out.' % session.get('user').username)
    session.pop('user')
    return redirect(url_for('auth.default'))

@auth.route('/info')
def info():
    return "This is a test."

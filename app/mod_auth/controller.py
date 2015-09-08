"""
This module holds all view functions for the authentication module.

These functions include the following:
"""

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app import logger
from app.mod_auth.form import LoginForm, RegistrationForm
from app.mod_auth.helper import onAuthRedirect, requireAuth, generateHash
from app.mod_auth.model import AuthLevel, User

auth = Blueprint('auth', __name__, template_folder = 'templates')

@auth.route('/')
def default():
    """The default route for the authentication-module.
    """
    return redirect(url_for('auth.info'))

@auth.route('/register', methods = ['GET', 'POST'])
@onAuthRedirect()
def register():
    """This function allows to register a new user to the system.
        Upon a GET request a RegistrationForm will be shown to the user.
        Upon a POST request the form will be validated and if valid the user
            will get assigned a AuthLevel and his password will be hashed.
            He will then be added to the database and redirect to the default
            route of the authentication-module.
            Should the form be invalid, the user will be shown the form again.
    """
    form = RegistrationForm(request.form)

    if request.method == 'POST' and form.validate():
        user = User()
        form.populate_obj(user)
        user.password = generateHash(user.password)
        user.authLevel = AuthLevel.USER

        user.save()

        logger.info('A user has been added.')
        flash('Your user account has been created.')
        return redirect(url_for('auth.default'))
    return render_template('auth/registration.html', form = form)

@auth.route('/login', methods = ['GET', 'POST'])
@onAuthRedirect()
def login():
    """This function logs a user into the system.
        Upon a GET request a LoginForm will be shown to the user.
        Upon a POST request the form will be validated and if valid the users
            specified password will be hashed and compared to the stored
            password.
            Should they be equal the user will be logged in (as such
                his User object will be stored in the session) and redirected to
                    the default page of the authentication-module.
                Is this not the case or if the form was invalid in the first
                    place, he will be shown the form again.
    """
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        user = User.objects(username = form.username.data).first()
        if user is not None:
            if user.password == generateHash(form.password.data):
                session['user'] = user
                return redirect(url_for('auth.default'))

        logger.info('User %s has logged in.' % user.username)
        flash('The specified username and/or password were incorrect.')
    return render_template('auth/login.html', form = form)

@auth.route('/logout')
@requireAuth()
def logout():
    """This function logs a user out of the system.
        Should the user be logged in, his User object will be poped from the
            session and he will be redirected to the default page for the
            authentication-module.
        Should he not be logged in, please see: app.mod_auth.helper.requireAuth
    """
    logger.info('User %s has logged out.' % session.get('user').username)
    session.pop('user')
    return redirect(url_for('auth.default'))

@auth.route('/info')
def info():
    return "This is a test."

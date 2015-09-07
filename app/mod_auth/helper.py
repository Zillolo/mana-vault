"""This module contains helper functions for the authentication-module.
"""
from flask import abort, flash, redirect, request, session, url_for
from functools import update_wrapper
import hashlib

from app import app
from app.mod_auth.model import AuthLevel, User

def requireAuth(level = AuthLevel.USER):
    """A decorator that checks whether a user is logged in and has the right
        AuthLevel to execute a function. If so the function will be executed.

        Args:
            -) level (AuthLevel): The minimum AuthLevel needed to execute the
                decorated function.

        Returns:
            -) The decorated function.
            -) A redirect to the login page of the authentication-module, if the
                user is not logged in.
            Note: Should the users AuthLevel be lower than the one specified, he
                will receive a 403 HTTP Status code.


        'level' indicates the minimum AuthLevel needed to access the page.
        If the user accessing the page has an AuthLevel higher than the one
        specified by 'level', he is still allowed to access the page.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            user = session.get('user', None)
            if user is None:
                return redirect(url_for('auth.login'))
            if user['authLevel'] < level:
                logger.info('A user tried to access a higher-level area.')
                abort(403)
            return func(*args, **kwargs)
        return update_wrapper(wrapper, func)
    return decorator

def generateHash(password):
    logger.info('A hash has been generated.')
    return hashlib.sha512(password.encode('utf-8')).hexdigest()
def onAuthRedirect():
    """A decorator that checks whether a user is already logged in, and if so
        does not execute the decorated function, but redirects him to the
        default page of the authentication-module.

        Returns:
            -) The decorated function.
            -) A redirect to the default page of the authentication-module, if
                the user is already logged in.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            if session.get('user', None):
                flash('You are already logged in.')
                return redirect(url_for('auth.default'))
            else:
                return func(*args, **kwargs)
        return update_wrapper(wrapper, func)
    return decorator

def generateHash(password):
    """Generates the SHA512-hash of a specified password and returns its
        hex-digest.

        Args:
            -) password (String): The password whose hash will be generated.

        Returns:
            -) The hex-digest of the hashed password.
    """
    return hashlib.sha512(password.encode('utf-8')).hexdigest()

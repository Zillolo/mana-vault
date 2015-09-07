"""
This module contains helper functions for the authentication module.
"""
from flask import abort, redirect, request, session, url_for
from functools import update_wrapper
import hashlib

from app import app
from app.mod_auth.model import AuthLevel, User

def requireAuth(level = AuthLevel.USER):
    def decorator(func):
        def wrapper(*args, **kwargs):
            user = session.get('user', None)
            if user is None:
                return redirect(url_for('auth.info'))
            if user.authLevel < level:
                abort(403)
            return func(*args, **kwargs)
        return update_wrapper(wrapper, func)
    return decorator

def generateHash(password):
    return hashlib.sha512(password.encode('utf-8')).hexdigest()

"""
This module holds all view functions for the authentication module.

These functions include the following:
"""

from flask import Blueprint, redirect, session, url_for

from app.mod_auth.helper import requireAuth
from app.mod_auth.model import AuthLevel, User

auth = Blueprint('auth', __name__, template_folder = 'templates')

@auth.route('/register', methods = ['GET', 'POST'])
@requireAuth(AuthLevel.ADMIN)
def register():
    return "Decorator doesnt work :("

@auth.route('/info')
def info():
    return "This is a test."

from app import db

from enum import IntEnum

class AuthLevel(IntEnum):
    UNKNOWN = 0,
    USER = 1,
    ADMIN = 2

"""
A class that represents the user as a MongoEngine document.
"""
class User(db.Document):
    # Personal details
    firstName = db.StringField(min_length = 2, max_length = 20, required = True)
    lastName = db.StringField(min_length = 2, max_length = 30, required = True)

    # Login credentials
    username = db.StringField(min_length = 4, max_length = 20, required = True)
    password = db.StringField(required = True)

    # Email
    email = db.EmailField(required = True)

    authLevel = AuthLevel.USER

    meta = {
        'allow_inheritance' : True,
        'indexes' : [
            {
                'fields' : ['username'],
                'unique' : True
            },
            {
                'fields' : ['email'],
                'unique' : True
            }
        ]
    }

from enum import IntEnum

from app import db

"""
Describes the authentication level of a user as a series of constants.
IntEnum has been chosen as this provides a nice way to use < and > for permission checking.
"""
class AuthLevel(IntEnum):
    UNKNOWN = 0,
    USER = 1,
    ADMIN = 2

"""
A class that represents the schema of a User as a MongoEngine document.
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

    # Authentication-level
    authLevel = db.IntField(required = True)

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

from app import db
from app.mod_auth.model import User

class Category(db.Document):
    # The name of the category.
    name = db.StringField(required = True)

class Entry(db.Document):
    # The amount of the entry.
    amount = db.DecimalField(precision = 2, required = True)

    # A short description for the entry.
    description = db.StringField(required = True)

    # The owner of the entry.
    # Should the owner be deleted, we also want to delete all of his entries.
    owner = db.ReferenceField(User, reverse_delete_rule = db.CASCADE, required = True)

    # The category of this entry.
    category = db.ReferenceField(Category, required = True)

def sumEntries():
    return sum([entry.amount for entry in Entry.objects if entry.amount > 0])

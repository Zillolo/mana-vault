from wtforms import Form, DecimalField, SelectField, TextField, validators
from wtforms.fields.html5 import DecimalRangeField

from bson.objectid import ObjectId

class AddEntryForm(Form):
    amount = DecimalField('Amount', places = 2, validators = [validators.Required()])
    description = TextField('Description', validators = [validators.Required()])

    category = SelectField(coerce = ObjectId)

class EditBudgetForm(Form):
    pass

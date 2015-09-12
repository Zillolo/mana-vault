from wtforms import Form, DecimalField, SelectField, TextField, validators
from wtforms.fields.html5 import DecimalRangeField

from bson.objectid import ObjectId

from app.mod_budget.model import Category

class AddEntryForm(Form):
    amount = DecimalField('Amount', places = 2, validators = [validators.Required()])
    description = TextField('Description', validators = [validators.Required()])

    category = SelectField(coerce = ObjectId, validators = [validators.Optional()])

    def loadCategories(self):
        self.category.choices = [(c.id, c.name) for c in Category.objects().all()]

class EditBudgetForm(Form):
    pass

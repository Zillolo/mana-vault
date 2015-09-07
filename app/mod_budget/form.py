from wtforms import Form, DecimalField, SelectField, TextField, validators

class AddEntryForm(Form):
    amount = DecimalField('Amount', places = 2, validators = [validators.Required()])
    description = TextField('Description', validators = [validators.Required()])

    category = SelectField()

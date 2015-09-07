from wtforms import Form, TextField, PasswordField, DateTimeField, validators
from wtforms.fields.html5 import EmailField

class RegistrationForm(Form):
    firstName = TextField('First Name', validators = [
        validators.Length(min=2, max=20),
        validators.Required()
        ])
    lastName = TextField('Last Name', validators = [
        validators.Length(min=2, max=30),
        validators.Required()
        ])

    email = EmailField('Email', validators = [
        validators.Required(),
        validators.Email()
        ])

    username = TextField('Username', validators = [
        validators.Length(min=4, max=20),
        validators.Required()
        ])
    password = PasswordField('Password', validators = [
        validators.Length(min=6, max=30),
        validators.Required(),
        validators.EqualTo('passwordConfirm', message='The passwords must be equal.')
        ])
    passwordConfirm = PasswordField('Confirm Password', validators = [])

class LoginForm(Form):
    username = TextField('Username', validators = [
        validators.Required()
        ])
    password = PasswordField('Password', validators = [
        validators.Required()
    ])

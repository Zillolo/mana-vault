from wtforms import Form, TextField, PasswordField, DateTimeField, validators
from wtforms.fields.html5 import EmailField

class RegistrationForm(Form):
    """A class that encapsulates the form of the registration dialog as a
        WTForm.

        Attributes:
            -) firstName (TextField): A textfield containing the first name of
                the user.
            -) lastName (TextField): A textfield containg the last name of the
                user.
            -) email (EmailField): A textfield with an Email-Regex containing
                the email of the user.
            -) username (TextField): A textfield containg the username of the
                user.
            -) password (PasswordField): A passwordfield containg the users
                password.
            -) passwordConfirm (PasswordField): A passwordfield containg the
                users confirmation password.
    """
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
    """A class representing the form of the login dialog as a WTForm.

        Attributes:
            -) username (TextField): A textfield containg the users username.
            -) password (PasswordField): A passwordfield containg the users
                password.
    """
    username = TextField('Username', validators = [
        validators.Required()
        ])
    password = PasswordField('Password', validators = [
        validators.Required()
    ])

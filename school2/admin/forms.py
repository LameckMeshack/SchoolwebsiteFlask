from wtforms import Form, BooleanField, StringField, PasswordField, validators


class RegistrationForm(Form):
    # name = StringField('Name', [validators.Length(min=4, max=25)])
    username = StringField('Username', [validators.Length(min=3, max=25)])
    regno = StringField('Regno', [validators.Length(min=6, max=10)])
    # phone = StringField('Phone', [validators.Length(min=10, max=35)])
    course = StringField('Course', [validators.Length(min=3, max=25)])
    # faculty = StringField('Faculty', [validators.Length(min=3, max=25)])

    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

class LoginForm(Form):
        username = StringField('Username', [validators.Length(min=3, max=25)])
        password = PasswordField('Password', [validators.DataRequired()])
        

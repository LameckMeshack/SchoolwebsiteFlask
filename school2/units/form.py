from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form, BooleanField, DecimalField, TextAreaField, StringField,IntegerField, validators
from wtforms.validators import DataRequired



class Addunits(Form):
    name = StringField('Name', [validators.DataRequired()])
    unitcode = StringField('Unit Code', [validators.DataRequired()])
    lecName = StringField('Lecturer', [validators.DataRequired()])
    link = StringField('Whatsapp Link', [validators.DataRequired()])

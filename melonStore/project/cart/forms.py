from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField

class EditForm(FlaskForm):

    quantity = IntegerField('Quantity: ')
    submit = SubmitField('Update')
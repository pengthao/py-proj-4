from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField

class AddForm(FlaskForm):

    quantity = IntegerField('Quantity: ')
    submit = SubmitField('Add to Cart')
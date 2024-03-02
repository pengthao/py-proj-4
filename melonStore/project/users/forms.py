from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo
from wtforms import ValidationError
from project.models import get_by_username


class LoginForm(FlaskForm):
    username = StringField('Username: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    submit = SubmitField('Log in')

class RegistrationForm(FlaskForm):
    username = StringField('Username: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired(),EqualTo('pass_confirm', message='Passwords must match!')])
    pass_confirm = PasswordField('Confirm Password: ', validators=[DataRequired()])
    name = StringField('Name: ', validators=[DataRequired()])
    submit = SubmitField('Register!')

    @staticmethod    
    def check_username(username):
        if get_by_username(username):
            raise ValidationError('Username is taken')
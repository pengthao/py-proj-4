from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, EqualTo
from wtforms import ValidationError
from myproject.models import Team, User


class LoginForm(FlaskForm):
    username = StringField('Username: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    submit = SubmitField('Log in')

class RegistrationForm(FlaskForm):
    username = StringField('Username: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired(),EqualTo('pass_confirm', message='Passwords must match!')])
    pass_confirm = PasswordField('Confirm Password: ', validators=[DataRequired()])
    team = SelectField('Team Name: ', validators=[DataRequired()])
    submit = SubmitField('Register!')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.team.choices = [(team.team_name, team.team_name) for team in Team.query.all()]


    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already taken. Try again')

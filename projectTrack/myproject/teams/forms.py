from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from myproject.models import Team

class AddTeam(FlaskForm):
    team_name = StringField('Team name: ', validators=[DataRequired()])
    submit = SubmitField('Create New Team')

class SwitchTeam(FlaskForm):
    team = SelectField('New Team: ', validators=[DataRequired()])
    submit = SubmitField('Submit Change')

    def __init__(self, *args, **kwargs):
        super(SwitchTeam, self).__init__(*args, **kwargs)
        self.team.choices = [(team.team_name, team.team_name) for team in Team.query.all()]

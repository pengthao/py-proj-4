from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, SubmitField, SelectField,TextAreaField, BooleanField
from wtforms.validators import DataRequired
from myproject.models import Team, Project

class NewProject(FlaskForm):
    project_name = StringField('Project name: ', validators=[DataRequired()])
    description = TextAreaField('Description: ', validators=[DataRequired()])
    team_name = SelectField('Team: ', validators=[DataRequired()])
    submit = SubmitField('Create New Project')

    def __init__(self, *args, **kwargs):
        super(NewProject, self).__init__(*args, **kwargs)
        self.team_name.choices = [(team.team_name, team.team_name) for team in Team.query.all()]


class SelectProject(FlaskForm):
    project = SelectField('Select Project to Update: ', validators=[DataRequired()])
    submit = SubmitField('Confirm')

    def __init__(self, *args, **kwargs):
        super(SelectProject, self).__init__(*args, **kwargs)
        user_team_id = current_user.team_id
        team_projects = Project.query.filter_by(team_id=user_team_id).all()
        self.project.choices = [(project.id, project.project_name) for project in team_projects]


        
class UpdateProject(FlaskForm):
    name_update = StringField('Update project name: ')
    description_update = TextAreaField('Update Description: ')
    team_update = SelectField('Update Team: ')
    completed = BooleanField('Completed: ')
    submit = SubmitField('Update')

    def __init__(self, *args, **kwargs):
        super(UpdateProject, self).__init__(*args, **kwargs)
        self.team_update.choices = [(team.team_name, team.team_name) for team in Team.query.all()]

    def set_default_project_values(self, project_id):
        project = Project.query.get(project_id)
        print(project.json())
        if project:
            self.name_update.data = project.project_name
            self.description_update.data = project.description
            self.completed.data = project.completed
            team = Team.query.get(project.team_id)
            if team:
                self.team_update.data = team.id
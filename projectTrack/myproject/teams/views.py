from flask import Blueprint, render_template, redirect, request, url_for, flash , session
from myproject.models import User, get_by_username, Team
from myproject.teams.forms import AddTeam, SwitchTeam
from flask_login import login_required, current_user
from myproject import db

teams_blueprint = Blueprint('teams', __name__, template_folder='templates/teams')

@teams_blueprint.route('/hub')
@login_required
def hub():
    user_team = int(current_user.team_id)

    teamInfo = Team.query.filter_by(id=user_team).first()

    if teamInfo:
        teamName = teamInfo.team_name
    else:
        teamName="Team Not Found"

    print(teamName)

    teamMembers = [user.username for user in User.query.filter_by(team_id=user_team)]


    return render_template('hub.html', teamMembers=teamMembers, teamName = teamName)


@teams_blueprint.route('/add_change', methods=['GET', 'POST'])
@login_required
def add_change():

    addForm = AddTeam()
    
    if addForm.validate_on_submit():

        newTeam = Team(team_name=addForm.team_name.data)
        db.session.add(newTeam)
        db.session.commit()
        print(newTeam.json())
        return redirect(url_for('teams.add_change'))
    
    
    changeForm = SwitchTeam()
    
    if changeForm.validate_on_submit():

        user = current_user
        team = Team.query.filter_by(team_name=changeForm.team.data).first()

        if team:
            user.team_id = team.id
            db.session.commit()
        else:
            flash('Team not found', 'error')
        return redirect(url_for('teams.hub'))
    
    return render_template('add_change.html', addForm=addForm, changeForm=changeForm)
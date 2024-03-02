from flask import Blueprint, render_template, redirect, url_for, flash , session
from myproject.models import User, get_by_username, Team, Project
from myproject.projects.forms import NewProject, UpdateProject, SelectProject
from flask_login import login_required, current_user
from myproject import db

projects_blueprint = Blueprint('projects', __name__, template_folder='templates/projects')

@projects_blueprint.route('/hub')
@login_required
def project_hub():
    user_team_id = int(current_user.team_id)
    team_name = Team.query.filter_by(id = user_team_id).first()
    open = Project.query.filter(Project.team_id==user_team_id, Project.completed==False)
    closed  = Project.query.filter(Project.team_id==user_team_id, Project.completed==True)

    return render_template('project_hub.html', open=open, closed=closed, team_name=team_name)      


@projects_blueprint.route('/new_project', methods=['GET', 'POST'])
@login_required
def new_project():

    form = NewProject()

    if form.validate_on_submit():

        project_team_id = Team.query.filter_by(team_name = form.team_name.data).first()

        if project_team_id:
            project_team_id = project_team_id.id
        else:
            flash('Team not found', 'error')
            return redirect(url_for('projects.new_project'))

        newProject = Project(
            project_name = form.project_name.data,
            description = form.description.data,
            team_id = project_team_id
        )
        db.session.add(newProject)
        db.session.commit()
        print(newProject.json())
        return redirect(url_for('projects.project_hub'))
    
    return render_template('new_project.html', form=form)


@projects_blueprint.route('/select_project', methods=['GET', 'POST'])
@login_required
def select_project():

    form = SelectProject()

    if form.validate_on_submit():
        project = Project.query.filter_by(id = form.project.data).first()
        project_id = project.id
        return redirect(url_for('projects.update_project', project_id=project_id))
    return render_template('select_project.html', form=form)

@projects_blueprint.route('/update_project/<int:project_id>', methods=['GET', 'POST'])
@login_required
def update_project(project_id):
    print("Route accessed!")
    form = UpdateProject(project_id=project_id)

    if form.validate_on_submit():
        print('Validation success')
        print(f'Update project_id pass {project_id}')
        
        project = Project.query.get(project_id)

        if project is not None:
            if (
                form.name_update.data != project.project_name or
                form.description_update.data != project.description or
                form.completed.data != project.completed or
                form.team_update.data != project.team.team_name
            ):
                project.project_name = form.name_update.data
                project.description = form.description_update.data
                project.completed = form.completed.data
                new_team_name = form.team_update.data
                new_team = Team.query.filter_by(team_name=new_team_name).first()
                if new_team:
                    project.team_id = new_team.id
                else:
                    flash('Team not found', 'error')
            else:
                flash('No updates provided', 'info')

            db.session.commit()
            return redirect(url_for('projects.project_hub'))
        else:
            flash('Project not found', 'error')
    else:
        flash('Validation failed', 'error')

    form.set_default_project_values(project_id)
    
    return render_template('update_project.html', form=form, project_id=project_id)


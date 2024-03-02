import sys
import os
from faker import Faker

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from myproject.models import User, Team, Project
from myproject import db, app

fake = Faker()

app.app_context().push()

def generate_dummy_users(num_users):
    for _ in range(num_users):
        username = fake.user_name()
        password = fake.password()
        team = Team.query.order_by(db.func.random()).first()
        user = User(username=username, password=password, team_id=team.id)
        db.session.add(user)
    db.session.commit()

def generate_dummy_teams(num_teams):
    for _ in range(num_teams):
        team_name = fake.word()
        team = Team(team_name=team_name)
        db.session.add(team)
    db.session.commit()

def generate_dummy_projects(num_projects):
    for _ in range(num_projects):
        project_name = fake.word()
        description = fake.sentence()
        team = Team.query.order_by(db.func.random()).first()
        project = Project(project_name=project_name, description=description, team_id=team.id)
        db.session.add(project)
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        generate_dummy_users(1)
        generate_dummy_teams(1)
        generate_dummy_projects(20)

    print("Dummy data generation complete.")

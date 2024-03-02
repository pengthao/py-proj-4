from flask import request
from flask_bcrypt import Bcrypt, generate_password_hash
from flask_restful import Resource, Api
from flask_login import UserMixin
from myproject import login_manager, app, db

api = Api(app)
bcrypt = Bcrypt()


class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(255), unique = True, nullable = False)
    password_hash = db.Column(db.String(255), nullable = False)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable = False)

    def __init__(self, username, password, team_id):
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.team_id = team_id

    def __str__(self):
        return f"User Id: {self.id}"
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def json(self):
        return f"'id' : {self.id}, 'username' : {self.username}, 'password' : {self.password_hash}, 'team_id' : {self.team_id}"

@login_manager.user_loader
def get_by_username(username):
    user_data = User.get(username)
    return User.json(user_data) if user_data else None

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


class Team(db.Model):

    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    team_name = db.Column(db.String(255), unique = True, nullable = False)

    users = db.relationship("User", backref = "Team", lazy = True)
    projects = db.relationship("Project", backref = "Team", lazy = True)

    def __init__(self, team_name):
        self.team_name = team_name

    def json(self):
        return f"'id' : {self.id}, 'team_name' : {self.team_name}"

def all_team_names():
    teams = Team.query.all()
    return [team.team_name for team in teams]


class Project(db.Model):

    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    project_name = db.Column(db.String(255), nullable = False)
    description = db.Column(db.String(255), nullable = True)
    completed = db.Column(db.Boolean, default = False)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable = False)

    
    def __init__(self, project_name, description, team_id):
        self.project_name = project_name
        self.description = description
        self.completed = False
        self.team_id = team_id

    def json(self):
        return f"'id' : {self.id}, 'project_name' : {self.project_name}, 'description' : {self.description}, 'completed' : {self.completed}, 'team_id' : {self.team_id}"


############### Rest ###########
##### user api #################

class userDetails(Resource):
    def get(self, username):
        user = User.query.filter_by(username=username).first()

        if user:
            return user.json()
        else:
            return {'name': None},  404
        
class addUser(Resource):
    def post(self):

        data = request.get_json()

        username = data.get('username')
        password_h = data.get('password_h')
        team_id = data.get('team_id')
    
        user = User(
            username,
            password_h,
            team_id
        )

        db.session.add(user)
        db.session.commit()

        return user.json()

class deleteUser(Resource):

    def delete(self,username):
        user = User.query.filter_by(username=username).first()
        db.session.delete(user)
        db.session.commit()

        return {'note': 'delete success'}
    
class allUsers(Resource):

    def get(self):
        users = User.query.all()
        return [user.json() for user in users]
    

api.add_resource(userDetails,'/userinfo/<string:name>')
api.add_resource(allUsers,'/allusers')
api.add_resource(addUser,'/adduser')
api.add_resource(deleteUser,'/deleteuser/<string:name>')



######### Team api ###############

class allTeams(Resource):

    def get(self):
        teams = Team.query.all()
        return [team.json() for team in teams]


class teamDetails(Resource):
    def get(self, team_name):
        team = Team.query.filter_by(team_name=team_name).first()

        if team:
            return team.json()
        else:
            return {'name': None},  404

class addTeam(Resource):
    def post(self):
    
        data = request.get_json()

        team_name = data.get('team_name')

        team = Team(
            team_name
        )

        db.session.add(team)
        db.session.commit()

        return team.json()

class deleteTeam(Resource):

    def delete(self,team_name):
        team = Team.query.filter_by(team_name=team_name).first()
        db.session.delete(team)
        db.session.commit()

        return {'note': 'delete success'}
    
api.add_resource(teamDetails,'/teaminfo/<string:name>')
api.add_resource(allTeams,'/allteams')
api.add_resource(addTeam ,'/addteam')
api.add_resource(deleteTeam,'/deleteteam/<string:team_name>')
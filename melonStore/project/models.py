import os
from flask import request
from flask_bcrypt import Bcrypt
from flask_restful import Resource, Api
from flask_login import UserMixin
#from flask_jwt import JWT, jwt_required
from project import login_manager, app, db
from pprint import pprint

api = Api(app)

class Melon(db.Model):

    __tablename__='melons'

    id = db.Column(db.Text, primary_key = True)
    name = db.Column(db.Text)
    price = db.Column(db.Float)
    image_url = db.Column(db.Text)
    color = db.Column(db.Text)
    seedless = db.Column(db.Boolean)

    def __init__(self, id, name, price, image_url, color, seedless):

        self.id = id
        self.name = name
        self.price = price
        self.image_url = image_url
        self.color = color
        self.seedless = seedless

    def to_dict(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'price' : self.price,
            'image_url' : self.image_url,
            'color' : self.color,
            'seedless' : self.seedless
        }
    
    @classmethod
    def from_dict(cls, melon):
        return cls(
            melon['id'],
            melon['name'],
            melon['price'],
            melon['image_url'],
            melon['color'],
            melon['seedless']
        )
    
    def __str__(self):
        return f"{self.name} (ID: {self.id})"
    
    def display_img(self):
        return self.image_url
    
    def all_melon_display(self):
        return f"Melon: {self.name}\n Price:{self.price}\n Seedless: {self.seedless}"
    
    def display_details(self):
        return f"""
            Name: {self.name}
            Price: {self.price}
            Color: {self.color}
            Seedless: {self.seedless}
        """

#######USERS###########

bcrypt = Bcrypt()

customers = {
    'mel': {'username': 'mel', 'password': 'password', 'name': 'Mel Wilson'},
    'squash': {'username': 'squash', 'password': '1234', 'name': 'Sara Squash'},
    'bunsen': {'username': 'bunsen', 'password': 'muppet', 'name': 'Bunsen Honeydew'},
    'hoon': {'username': 'hoon', 'password': 'blindmelon', 'name': 'Shannon Hoon'}
}



class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.Column(db.String(64)))

    def __init__(self, username, password_hash, name):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.name = name

    def to_dict(self):
        return {
            'username' : self.username,
            'password' : self.password_hash,
            'name' : self.name
        }
    
    def __str__(self):
        return f"User Id: {self.id}"

    @classmethod
    def from_dict(cls, user):
        return cls(
            user['username'],
            user['password'],
            user['name']
        )

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

@login_manager.user_loader
def get_by_username(username):
    user_data = customers.get(username)
    return User.from_dict(user_data) if user_data else None


'''username_table = {u.username: u for u in customers}
userid_table = {u.id: u for u in customers}

def authenticate(username, password):
    user = username_table.get(username, None)
    if user and bcrypt.check_password_hash(user.password_hash, password=password) == True:
        return user
    
def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)'''

#jwt = JWT(app, authenticate, identity)

########### REST #########################

class MelonInfo(Resource):
    #@jwt_required()
    def get(self, name):
        
        melon = Melon.query.filter_by(name=name).first()

        if melon:
            return melon.to_dict()
        else:
            return {'name': None}, 404
            
class AddMelon(Resource):
    #@jwt_required()
    def post(self):

        data = request.get_json()

        id = data.get('melon_id')
        name = data.get('common_name')
        price = data.get('price')
        image_url = data.get('image_url')
        color = data.get('color')
        seedless = data.get('seedless')

        melon = Melon(
            id,
            name,
            price,
            image_url,
            color,
            seedless
        )
        db.session.add(melon)
        db.session.commit()

        return melon.to_dict()
            
        
class deleteMelon(Resource):
    #@jwt_required()
    def delete(self, name):
        melon = Melon.query.filter_by(name=name).first()
        db.session.delete(melon)
        db.session.commit()

        return {'note': 'delete success'}


class AllMelons(Resource):
    #@jwt_required()
    def get(self):
        melons = Melon.query.all()
        return [melon.to_dict() for melon in melons]
    


api.add_resource(AllMelons, '/allmelons')
api.add_resource(MelonInfo, '/meloninfo/<string:name>')
api.add_resource(AddMelon, '/addmelon/')
api.add_resource(deleteMelon, '/deletemelon/<string:id>')


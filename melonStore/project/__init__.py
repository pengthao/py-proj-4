import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

login_manager = LoginManager()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

from project.melons.views import melons_blueprint
from project.users.views import users_blueprint
from project.cart.views import cart_blueprint
#from project.orders.views import orders_blueprint

app.register_blueprint(melons_blueprint, url_prefix='/melons')
app.register_blueprint(users_blueprint, url_prefix='/users')
app.register_blueprint(cart_blueprint, url_prefix='/cart')
#app.register_blueprint(orders_blueprint, url_prefix='/orders')'''

login_manager.init_app(app)
login_manager.login_view = 'login'


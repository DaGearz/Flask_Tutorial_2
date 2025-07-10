from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, UserMixin, current_user
from flask_bcrypt import Bcrypt


def create_database(app):
    if not path.exists('../instance/market.db'):
        with app.app_context():
            db.create_all()
        print('Database created')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = '44601de742d2d4f247453254'
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login_page'
login_manager.login_message_category = 'info'

from market import routes

create_database(app)
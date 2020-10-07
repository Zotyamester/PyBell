import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)

configs = {
    'SECRET_KEY' : 'my-secret-key',
    'SQLALCHEMY_DATABASE_URI' : 'sqlite:///app.db',
    'SQLALCHEMY_TRACK_MODIFICATIONS' : False,
    'SOUND_FOLDER' : './sounds',
    'CONFIG_FOLDER' : './configs',
    'CURRENT_CONFIG' : 'BellConfig_normal.xml'
}

for config, default in configs.items():
    app.config[config] = os.environ.get(config, default)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
login.login_message = ''

from app import routes

import os

from flask import Flask


app = Flask(__name__)

configs = {
    'SECRET_KEY' : 'my-secret-key',
    'SOUND_FOLDER' : './sounds',
    'CONFIG_FOLDER' : './configs',
    'CURRENT_CONFIG' : 'BellConfig.xml'
}

for config, default in configs.items():
    app.config[config] = os.environ.get(config, default)

from app import routes

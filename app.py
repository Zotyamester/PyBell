import os

from flask import Flask


app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'my-secret-key')
app.config['SOUND_FOLDER'] = os.environ.get('SOUND_FOLDER', './sounds')
app.config['CONFIG_FOLDER'] = os.environ.get('CONFIG_FOLDER', './configs')
app.config['CURRENT_CONFIG'] = os.environ.get('CURRENT_CONFIG', 'BellConfig.xml')

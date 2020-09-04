from flask import Flask

SOUND_FOLDER = './sounds'
CONFIG_FOLDER = './configs'
CURRENT_CONFIG = 'BellConfig.xml'

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SOUND_FOLDER'] = SOUND_FOLDER
app.config['CONFIG_FOLDER'] = CONFIG_FOLDER
app.config['CURRENT_CONFIG'] = CURRENT_CONFIG

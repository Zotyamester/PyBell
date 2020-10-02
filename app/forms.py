from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import (BooleanField, FileField, PasswordField, RadioField,
                     SelectField, StringField, SubmitField)
from wtforms.validators import DataRequired, InputRequired

ALLOWED_SOUND_EXTENSIONS = ['wav']
ALLOWED_CONFIG_EXTENSIONS = ['xml']

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class SoundUploadForm(FlaskForm):
    file = FileField('Sound', validators=[FileRequired('No soundfile selected for uploading'), \
        FileAllowed(ALLOWED_SOUND_EXTENSIONS, 'You can only upload soundfiles')])
    submit = SubmitField('Upload')

class ConfigUploadForm(FlaskForm):
    file = FileField('Config', validators=[FileRequired('No configfile selected for uploading'), \
        FileAllowed(ALLOWED_CONFIG_EXTENSIONS, 'You can only upload configfiles')])
    submit = SubmitField('Upload')

class ConfigManagerForm(FlaskForm):
    config = SelectField('Config', validators=[InputRequired()])
    submit = SubmitField('Select')

class BellManagerForm(FlaskForm):
    state = RadioField('State', choices=['Start', 'Stop', 'Restart'], validators=[InputRequired()])
    submit = SubmitField('Ok')

class PlayInstantForm(FlaskForm):
    sound = SelectField('Sound', validators=[InputRequired()])
    submit = SubmitField('Play')

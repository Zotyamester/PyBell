from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import (BooleanField, FieldList, FileField, Form, FormField,
                     HiddenField, PasswordField, RadioField, SelectField,
                     StringField, SubmitField, Label)
from wtforms.validators import InputRequired, ValidationError

ALLOWED_SOUND_EXTENSIONS = ['wav']
ALLOWED_CONFIG_EXTENSIONS = ['xml']

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class UploadedFileForm(Form):
    name = HiddenField('Name')
    remove = SubmitField('Remove')

class FileManagerForm(FlaskForm):
    files = FieldList(FormField(UploadedFileForm))

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

    def __init__(self, *args, **kwargs):
        super(ConfigManagerForm, self).__init__(*args, **kwargs)
        self.config.choices = kwargs['choices'].copy()

class BellManagerForm(FlaskForm):
    state = RadioField('State', choices=['Start', 'Stop', 'Restart'], validators=[InputRequired()])
    submit = SubmitField('Ok')

class PlayInstantForm(FlaskForm):
    sound = SelectField('Sound', validators=[InputRequired()])
    submit = SubmitField('Play')

    def __init__(self, *args, **kwargs):
        super(PlayInstantForm, self).__init__(*args, **kwargs)
        self.sound.choices = kwargs['choices'].copy()

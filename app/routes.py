import logging
import os
import sys
import urllib.request

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename

from app import app
from app import bell as b
from app import db
from app.forms import (BellManagerForm, ConfigManagerForm, ConfigUploadForm,
                       LoginForm, PlayInstantForm, SoundUploadForm, FileManagerForm)
from app.models import User


def flash_info(message):
    flash(message, 'info')

def flash_error(message):
    flash(message, 'error')

def flash_form_errors(form):
    for _, errors in form.errors.items():
        for error in errors:
            flash_error('%s' % error)

def list_all_files(dirname):
    all_files = []
    for _, _, files in os.walk(dirname):
        for filename in files:
            all_files.append(filename)
    return all_files

def list_sound_files():
    return list_all_files(app.config['SOUND_FOLDER'])

def list_config_files():
    return list_all_files(app.config['CONFIG_FOLDER'])

def upload_file(form, folder):
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        form.file.data.save(os.path.join(app.config[folder], filename))
        flash_info('File "%s" uploaded' % filename)
    else:
        flash_form_errors(form)
    return redirect(url_for('upload'))

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash_error('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    else:
        flash_form_errors(form)
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

@app.route('/upload', methods=['GET'])
@login_required
def upload():
    form1 = FileManagerForm(files=[{'name': name} for name in list_sound_files()])
    form2 = SoundUploadForm()
    form3 = FileManagerForm(files=[{'name': name} for name in list_config_files()])
    form4 = ConfigUploadForm()
    return render_template('uploader.html', \
        form1=form1, form2=form2, form3=form3, form4=form4)

@app.route('/manage_sound_uploads', methods=['POST'])
@login_required
def manage_sound_uploads():
    form = FileManagerForm(files=[{'name': name} for name in list_sound_files()])
    if form.validate_on_submit():
        for file in form.files:
            if file.remove.data:
                name = file.data['name']
                filename = os.path.join(app.config['SOUND_FOLDER'], name)
                if os.path.exists(filename):
                    os.remove(filename)
                    flash_info('File "%s" removed' % name)
                else:
                    flash_error('File "%s" does not exist' % name)
    else:
        flash_form_errors(form)
    return redirect(url_for('upload'))

@app.route('/upload_sound', methods=['POST'])
@login_required
def upload_sound():
    form = SoundUploadForm()
    return upload_file(form, 'SOUND_FOLDER')

@app.route('/manage_config_uploads', methods=['POST'])
@login_required
def manage_config_uploads():
    form = FileManagerForm(files=[{'name': name} for name in list_config_files()])
    if form.validate_on_submit():
        for file in form.files:
            if file.remove.data:
                name = file.data['name']
                filename = os.path.join(app.config['CONFIG_FOLDER'], name)
                if os.path.exists(filename):
                    os.remove(filename)
                    flash_info('File "%s" removed' % name)
                else:
                    flash_error('File "%s" does not exist' % name)
    else:
        flash_form_errors(form)
    return redirect(url_for('upload'))

@app.route('/upload_config', methods=['POST'])
@login_required
def upload_config():
    form = ConfigUploadForm()
    return upload_file(form, 'CONFIG_FOLDER')

@app.route('/manage_configs', methods=['GET', 'POST'])
@login_required
def manage_configs():
    form = ConfigManagerForm(choices=list_config_files())
    if form.validate_on_submit():
        filename = secure_filename(form.config.data)
        app.config['CURRENT_CONFIG'] = filename
        b.load_schedule(os.path.join(app.config['CONFIG_FOLDER'], app.config['CURRENT_CONFIG']))
        flash_info('Config updated')
    else:
        flash_form_errors(form)
    return render_template('config_manager.html', form=form, current_config=app.config['CURRENT_CONFIG'])

@app.route('/manage_bell', methods=['GET'])
@login_required
def manage_bell():
    form1 = BellManagerForm()
    form2 = PlayInstantForm(choices=list_sound_files())
    return render_template('bell_manager.html', form1=form1, form2=form2, state=b.running)

@app.route('/manage_scheduler', methods=['POST'])
@login_required
def manage_scheduler():
    form = BellManagerForm()
    if form.validate_on_submit():
        selected = form.state.data
        if selected == 'Start':
            b.bell_start()
            flash_info('Bell started')
        elif selected == 'Stop':
            b.bell_stop()
            flash_info('Bell stopped')
        else:
            b.bell_stop()
            b.bell_start()
            flash_info('Bell restarted')
    else:
        flash_form_errors(form)
    return redirect(url_for('manage_bell'))

@app.route('/play_instant', methods=['POST'])
@login_required
def play_instant():
    form = PlayInstantForm(choices=list_sound_files())
    if form.validate_on_submit():
        filename = secure_filename(form.sound.data)
        b.play_instant(os.path.join(app.config['SOUND_FOLDER'], filename))
        flash_info('Now playing "%s".' % filename)
    else:
        flash_form_errors(form)
    return redirect(url_for('manage_bell'))

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
                       LoginForm, PlayInstantForm, SoundUploadForm)
from app.models import User

def flash_info(message):
	flash(message, 'info')

def flash_error(message):
	flash(message, 'error')

def list_all_files(dirname):
	all_files = []
	for _, _, files in os.walk(dirname):
		for filename in files:
			all_files.append(filename)
	return all_files

def upload_file(form, folder):
	if form.validate_on_submit():
		filename = secure_filename(form.file.data.filename)
		form.file.data.save(os.path.join(app.config[folder], filename))
		flash_info('File "%s" uploaded' % filename)
	else:
		for error in form.file.errors:
			flash_error(error)
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
	form1 = SoundUploadForm()
	form2 = ConfigUploadForm()
	return render_template('uploader.html', form1=form1, form2=form2)

@app.route('/upload_sound', methods=['POST'])
@login_required
def upload_sound():
	form = SoundUploadForm()
	return upload_file(form, 'SOUND_FOLDER')

@app.route('/upload_config', methods=['POST'])
@login_required
def upload_config():
	form = ConfigUploadForm()
	return upload_file(form, 'CONFIG_FOLDER')

@app.route('/manage_configs', methods=['GET', 'POST'])
@login_required
def manage_configs():
	form = ConfigManagerForm()
	if request.method == 'POST':
		filename = secure_filename(form.config.data)
		app.config['CURRENT_CONFIG'] = filename
		b.load_schedule(os.path.join(app.config['CONFIG_FOLDER'], app.config['CURRENT_CONFIG']))
		flash_info('Config updated')
		return redirect(request.url)
	form.config.choices = list_all_files(app.config['CONFIG_FOLDER'])
	return render_template('config_manager.html', form=form, current_config=app.config['CURRENT_CONFIG'])

@app.route('/manage_bell', methods=['GET'])
@login_required
def manage_bell():
	form1 = BellManagerForm()
	form2 = PlayInstantForm()
	form2.sound.choices = list_all_files(app.config['SOUND_FOLDER'])
	return render_template('bell_manager.html', form1=form1, form2=form2, state=b.running)

@app.route('/manage_scheduler', methods=['POST'])
@login_required
def manage_scheduler():
	form = BellManagerForm()
	selected = form.state.data
	if selected == 'Start':
		b.bell_start()
		flash_info('Bell started')
	elif selected == 'Stop':
		b.bell_stop()
		flash_info('Bell stopped')
	elif selected == 'Restart':
		b.bell_stop()
		b.bell_start()
		flash_info('Bell restarted')
	else:
		flash_error('Selection error')
	return redirect(url_for('manage_bell'))

@app.route('/play_instant', methods=['POST'])
@login_required
def play_instant():
	form = PlayInstantForm()
	filename = secure_filename(form.sound.data)
	b.play_instant(os.path.join(app.config['SOUND_FOLDER'], filename))
	flash_info('Now playing "%s".' % filename)
	return redirect(url_for('manage_bell'))

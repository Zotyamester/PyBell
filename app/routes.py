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
from app.forms import LoginForm
from app.models import User

ALLOWED_SOUND_EXTENSIONS = {'mp3', 'wav'}
ALLOWED_CONFIG_EXTENSIONS = {'xml', 'bellxml'}

def list_all_files(dirname):
	all_files = []
	for _, _, files in os.walk(dirname):
		for filename in files:
			all_files.append(filename)
	return all_files

def allowed_file(filename, allowed_exts):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_exts

def upload(request, allowed_exts, folder):
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No file selected for uploading')
		return redirect(request.url)
	if file and allowed_file(file.filename, allowed_exts):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config[folder], filename))
		flash('File uploaded')
		return redirect(request.url)
	else:
		flash('Allowed file types are {}'.format(', '.join(allowed_exts)))
		return redirect(request.url)

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
            flash('Invalid username or password')
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
	db.session.rollback()
	return render_template('500.html'), 500

@app.route('/upload_sound', methods=['GET', 'POST'])
@login_required
def upload_sound():
	if request.method == 'POST':
		return upload(request, ALLOWED_SOUND_EXTENSIONS, 'SOUND_FOLDER')
	return render_template('uploader.html', filetype='sound', action_url='/upload_sound')

@app.route('/upload_config', methods=['GET', 'POST'])
@login_required
def upload_config():
	if request.method == 'POST':
		return upload(request, ALLOWED_CONFIG_EXTENSIONS, 'CONFIG_FOLDER')
	return render_template('uploader.html', filetype='config', action_url='/upload_config')

@app.route('/manage_configs', methods=['GET', 'POST'])
@login_required
def manage_configs():
	if request.method == 'POST':
		config_select = request.form['config_select']
		filename = secure_filename(config_select)
		app.config['CURRENT_CONFIG'] = filename
		b.load_schedule(os.path.join(app.config['CONFIG_FOLDER'], app.config['CURRENT_CONFIG']))
		flash('Config updated')
		return redirect(request.url)
	all_files = list_all_files(app.config['CONFIG_FOLDER'])
	return render_template('config_manager.html', files=all_files, current_config=app.config['CURRENT_CONFIG'])

@app.route('/manage_bell', methods=['GET', 'POST'])
@login_required
def manage_bell():
	if request.method == 'POST':
		selected = request.form['state']
		if selected == 'start':
			b.bell_start()
			flash('Bell started')
		elif selected == 'stop':
			b.bell_stop()
			flash('Bell stopped')
		elif selected == 'restart':
			b.bell_stop()
			b.bell_start()
			flash('Bell restarted')
		else:
			flash('Selection error')
		return redirect(request.url)
	all_files = list_all_files(app.config['SOUND_FOLDER'])
	return render_template('bell_manager.html', files=all_files, state=b.running)

@app.route('/play_instant', methods=['POST'])
@login_required
def play_instant():
	sound_select = request.form['sound_select']
	filename = secure_filename(sound_select)
	b.play_instant(os.path.join(app.config['SOUND_FOLDER'], filename))
	flash('Now playing "%s".' % filename)
	return redirect(url_for('manage_bell'))

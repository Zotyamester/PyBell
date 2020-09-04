import logging
import os
import sys
import urllib.request

from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from app import app
import bell as b

ALLOWED_SOUND_EXTENSIONS = {'mp3', 'wav'}
ALLOWED_CONFIG_EXTENSIONS = {'xml', 'bellxml'}

def list_all_files(dirname):
	all_files = []
	for root, dirs, files in os.walk(dirname):
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
def home_():
	return render_template('home.html')

@app.route('/upload_sound', methods=['GET', 'POST'])
def upload_sound_():
	if request.method == 'POST':
		return upload(request, ALLOWED_SOUND_EXTENSIONS, 'SOUND_FOLDER')
	return render_template('uploader.html', filetype='sound', action_url='/upload_sound')

@app.route('/upload_config', methods=['GET', 'POST'])
def upload_config_():
	if request.method == 'POST':
		return upload(request, ALLOWED_CONFIG_EXTENSIONS, 'CONFIG_FOLDER')
	return render_template('uploader.html', filetype='config', action_url='/upload_config')

@app.route('/manage_configs', methods=['GET', 'POST'])
def manage_configs_():
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
def manage_bell_():
	if request.method == 'POST':
		selected = request.form['state']
		if selected == 'start':
			b.bell_start()
			flash('Bell started')
		elif selected == 'stop':
			b.bell_stop()
			flash('Bell stopped')
		else:
			b.bell_stop()
			b.bell_start()
			flash('Bell restarted')
		return redirect(request.url)
	all_files = list_all_files(app.config['SOUND_FOLDER'])
	return render_template('bell_manager.html', files=all_files, state=b.running)

@app.route('/play_instant', methods=['POST'])
def play_instant_():
	sound_select = request.form['sound_select']
	filename = secure_filename(sound_select)
	b.play_instant(os.path.join(app.config['SOUND_FOLDER'], filename))
	flash('Now playing the requested sound')
	return redirect('/manage_bell')

if __name__ == "__main__":
    b.load_schedule(os.path.join(app.config['CONFIG_FOLDER'], app.config['CURRENT_CONFIG']))
    b.bell_start()
    app.run(host='0.0.0.0')

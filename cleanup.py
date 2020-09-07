import os

from app import app


def list_all_files(dirname):
	all_files = []
	for root, dirs, files in os.walk(dirname):
		for filename in files:
			all_files.append(filename)
	return all_files

for config in list_all_files(app.config['CONFIG_FOLDER']):
    config = os.path.join('configs', config)
    content = ''
    with open(config, 'r') as f:
        content = f.read()
    content = content.replace('C:\\Users\\Bethlen\\Desktop\\Bell\\', '')
    with open(config, 'w') as f:
        f.write(content)

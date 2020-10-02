import os

from app import app


def list_all_files(dirname):
    all_files = []
    for _, _, files in os.walk(dirname):
        for filename in files:
            all_files.append(filename)
    return all_files

for config in list_all_files(app.config['CONFIG_FOLDER']):
    config = os.path.join(app.config['CONFIG_FOLDER'], config)
    content = ''
    with open(config, 'r') as f:
        content = f.read()
    content = content.replace('C:\\Users\\Bethlen\\Desktop\\Bell\\', '')
    with open(config, 'w') as f:
        f.write(content)

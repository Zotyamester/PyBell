import os
import sys
import datetime

from cx_Freeze import setup, Executable


def files_under_dir(dir_name):
    file_list = []
    for root, _, files in os.walk(dir_name):
        for name in files:
            file_list.append(os.path.join(root, name))
    return file_list


includefiles = []
for directory in ('static', 'templates'):
    includefiles += files_under_dir(directory)

dt = datetime.datetime.now()

setup(name='PyBell',
      version='2.0',
      description='Web Server',
      options={
          'build_exe': {
              'packages': ['jinja2.ext',
                           'flask_sqlalchemy',
                           'flask_login',
                           'flask_wtf',
                           'simpleaudio',
                           'schedule',
                           'os',
                           'flask_sqlalchemy._compat',
                           'sqlalchemy.dialects.sqlite',
                           'sqlalchemy'],
              'include_files': includefiles,
              'include_msvcr': True}},
      executables=[Executable(script='exe_entry.py', target_name='pybell.exe')]
      )

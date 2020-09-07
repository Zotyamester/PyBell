import os
import threading
import time
from xml.dom import minidom

import schedule
from playsound import playsound

from app import app

WEEK_ = ['mo', 'tu', 'we', 'th', 'fr', 'sa', 'su']
TIME_ = ['h', 'm', 's']

th = None
running = False

def load_schedule(filename):
    schedule.clear()
    doc = minidom.parse(filename)
    rings = doc.getElementsByTagName('ring')
    for ring in rings:
        soundfile = os.path.join(app.config['SOUND_FOLDER'], ring.getElementsByTagName('media')[0].firstChild.nodeValue)
        days_node = ring.getElementsByTagName('days')[0]
        days = {x : (days_node.attributes[x].firstChild.nodeValue == '1') for x in WEEK_}
        time_nodes = ring.getElementsByTagName('time')
        times = [{x : int(time_node.attributes[x].firstChild.nodeValue) for x in TIME_} for time_node in time_nodes]
        if days['mo']:
            for timestamp in times:
                schedule.every().monday.at('{:02d}:{:02d}:{:02d}'.format(timestamp['h'], timestamp['m'], timestamp['s'])).do(playsound, soundfile, False)
        if days['tu']:
            for timestamp in times:
                schedule.every().tuesday.at('{:02d}:{:02d}:{:02d}'.format(timestamp['h'], timestamp['m'], timestamp['s'])).do(playsound, soundfile, False)
        if days['we']:
            for timestamp in times:
                schedule.every().wednesday.at('{:02d}:{:02d}:{:02d}'.format(timestamp['h'], timestamp['m'], timestamp['s'])).do(playsound, soundfile, False)
        if days['th']:
            for timestamp in times:
                schedule.every().thursday.at('{:02d}:{:02d}:{:02d}'.format(timestamp['h'], timestamp['m'], timestamp['s'])).do(playsound, soundfile, False)
        if days['fr']:
            for timestamp in times:
                schedule.every().friday.at('{:02d}:{:02d}:{:02d}'.format(timestamp['h'], timestamp['m'], timestamp['s'])).do(playsound, soundfile, False)
        if days['sa']:
            for timestamp in times:
                schedule.every().saturday.at('{:02d}:{:02d}:{:02d}'.format(timestamp['h'], timestamp['m'], timestamp['s'])).do(playsound, soundfile, False)
        if days['su']:
            for timestamp in times:
                schedule.every().sunday.at('{:02d}:{:02d}:{:02d}'.format(timestamp['h'], timestamp['m'], timestamp['s'])).do(playsound, soundfile, False)

def play_instant(filename):
    soundfile = os.path.join(app.config['SOUND_FOLDER'], filename)
    playsound(filename, False)

def bell_start():
    global running, th
    if not running:
        running = True
        th = threading.Thread(target=bell_main)
        th.start()

def bell_stop():
    global running
    if running:
        running = False

def bell_main():
    while running:
        schedule.run_pending()
        time.sleep(1)

import os
import threading
import time

import schedule
from playsound import playsound

from app import app
from app.bellconfig import BellConfig

th = None
running = False

def load_schedule(filename):
    schedule.clear()
    config = BellConfig()
    config.load(filename)
    for ring in config.rings:
        soundfile = os.path.join(app.config['SOUND_FOLDER'], ring.soundfile)
        days = ring.days
        times = ring.times
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

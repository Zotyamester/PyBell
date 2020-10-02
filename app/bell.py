import os
import threading
import time

import schedule as sch
from simpleaudio import WaveObject

from app import app
from app.bellconfig import BellConfig


def play_sound(filename):
    WaveObject.from_wave_file(filename).play()

th = None
running = False

def load_schedule(filename):
    sch.clear()
    config = BellConfig()
    config.load(filename)
    for ring in config.rings:
        soundfile = os.path.join(app.config['SOUND_FOLDER'], ring.soundfile)
        days = ring.days
        times = ring.times
        if days['mo']:
            for timestamp in times:
                sch.every().monday.at('{:02d}:{:02d}:{:02d}'.format(timestamp['h'], timestamp['m'], timestamp['s'])).do(play_sound, soundfile)
        if days['tu']:
            for timestamp in times:
                sch.every().tuesday.at('{:02d}:{:02d}:{:02d}'.format(timestamp['h'], timestamp['m'], timestamp['s'])).do(play_sound, soundfile)
        if days['we']:
            for timestamp in times:
                sch.every().wednesday.at('{:02d}:{:02d}:{:02d}'.format(timestamp['h'], timestamp['m'], timestamp['s'])).do(play_sound, soundfile)
        if days['th']:
            for timestamp in times:
                sch.every().thursday.at('{:02d}:{:02d}:{:02d}'.format(timestamp['h'], timestamp['m'], timestamp['s'])).do(play_sound, soundfile)
        if days['fr']:
            for timestamp in times:
                sch.every().friday.at('{:02d}:{:02d}:{:02d}'.format(timestamp['h'], timestamp['m'], timestamp['s'])).do(play_sound, soundfile)
        if days['sa']:
            for timestamp in times:
                sch.every().saturday.at('{:02d}:{:02d}:{:02d}'.format(timestamp['h'], timestamp['m'], timestamp['s'])).do(play_sound, soundfile)
        if days['su']:
            for timestamp in times:
                sch.every().sunday.at('{:02d}:{:02d}:{:02d}'.format(timestamp['h'], timestamp['m'], timestamp['s'])).do(play_sound, soundfile)

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
        sch.run_pending()
        time.sleep(1)

def play_instant(filename):
    play_sound(filename)

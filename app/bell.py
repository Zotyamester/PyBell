import os
import threading
import time

import schedule as sch
from simpleaudio import WaveObject

from app import app
from app.bellconfig import BellConfig


def format_time(h, m, s):
    return '{:02d}:{:02d}:{:02d}'.format(h, m, s)

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
            for time in times:
                sch.every().monday.at(format_time(time['h'], time['m'], time['s'])).do(play_sound, soundfile)
        if days['tu']:
            for time in times:
                sch.every().tuesday.at(format_time(time['h'], time['m'], time['s'])).do(play_sound, soundfile)
        if days['we']:
            for time in times:
                sch.every().wednesday.at(format_time(time['h'], time['m'], time['s'])).do(play_sound, soundfile)
        if days['th']:
            for time in times:
                sch.every().thursday.at(format_time(time['h'], time['m'], time['s'])).do(play_sound, soundfile)
        if days['fr']:
            for time in times:
                sch.every().friday.at(format_time(time['h'], time['m'], time['s'])).do(play_sound, soundfile)
        if days['sa']:
            for time in times:
                sch.every().saturday.at(format_time(time['h'], time['m'], time['s'])).do(play_sound, soundfile)
        if days['su']:
            for time in times:
                sch.every().sunday.at(format_time(time['h'], time['m'], time['s'])).do(play_sound, soundfile)

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

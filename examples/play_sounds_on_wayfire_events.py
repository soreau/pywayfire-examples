#!/usr/bin/python3

import sys
import subprocess

# Check if pygame is installed, and install it if not
try:
    import pygame
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
    import pygame

from wayfire import WayfireSocket

# Initialize pygame mixer for playing sounds
pygame.mixer.init()

# Define sound file paths, set the var None for no sound to the event
MINIMIZE_SOUND = "/path/to/minimize_sound.mp3"
UNMINIMIZE_SOUND = "/path/to/unminimize_sound.mp3"
MAXIMIZE_SOUND = "/path/to/maximize_sound.mp3"
UNMAXIMIZE_SOUND = "/path/to/unmaximize_sound.mp3"
OPEN_SOUND = "/path/to/open_sound.mp3"
CLOSE_SOUND = "/path/to/close_sound.mp3"
VIEW_FOCUSED = "/path/to/view_focused_sound.mp3"
OUTPUT_GAIN_FOCUS = "/path/to/output_gain_focus.mp3"

# Function to play a sound
def play_sound(sound_path):
    try:
        if sound_path:
            pygame.mixer.music.load(sound_path)
            pygame.mixer.music.play()
    except pygame.error:
        print("file {} does not exist".format(sound_path))

sock = WayfireSocket()
sock.watch()

while True:
    try:
        msg = sock.read_next_event()
        if "event" in msg:
            if msg["event"] == "view-minimized":
                if msg["view"]["minimized"]:
                    play_sound(MINIMIZE_SOUND)
                else:
                    play_sound(UNMINIMIZE_SOUND)
            elif msg["event"] == "view-tiled":
                if msg["view"]["tiled-edges"] == 0:
                    play_sound(UNMAXIMIZE_SOUND)
                else:
                    play_sound(MAXIMIZE_SOUND)
            elif msg["event"] == "view-mapped":
                play_sound(OPEN_SOUND)
            elif msg["event"] == "view-unmapped":
                play_sound(CLOSE_SOUND)
            elif msg["event"] == "view-focused":
                play_sound(VIEW_FOCUSED)
            elif msg["event"] == "output-gain-focus":
                play_sound(OUTPUT_GAIN_FOCUS)
            elif msg["event"] == "plugin-activation-state-changed":
                if msg["plugin"] == "scale":
                    print("play a sound for scale")
                if msg["plugin"] == "expo":
                    print("play a sound for expo")
    except KeyboardInterrupt:
        exit(0)


"# KeyboardIllumination" 
import numpy as np
import sounddevice as sd
from pynput import keyboard
from pynput.keyboard import Controller, Key
import threading
import time
import tkinter as tk

keyboard_controller = Controller()

# Parameters
fs = 100000
block_duration = 0.02
threshold = 0.05
last_bass_state = False
running = True
current_bass = 0

# GUI globals
root = None
bass_label = None
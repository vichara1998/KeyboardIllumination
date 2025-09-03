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

def detect_bass(indata):
    if len(indata.shape) > 1:
        audio_data = indata[:, 0]
    else:
        audio_data = indata

    windowed = audio_data * np.hanning(len(audio_data))
    fft = np.abs(np.fft.rfft(windowed))

    fft_length = len(windowed)
    freq_resolution = fs / fft_length
    bass_max_bin = int(250 / freq_resolution)
    bass_min_bin = max(1, int(20 / freq_resolution))

    bass_energy = np.sum(fft[bass_min_bin:bass_max_bin])
    return bass_energy

def set_scroll_lock(on: bool):
    global last_bass_state
    if on != last_bass_state:
        try:
            keyboard_controller.press(Key.scroll_lock)
            time.sleep(0.01)
            keyboard_controller.release(Key.scroll_lock)
            last_bass_state = on
        except Exception as e:
            print(f"\nKeyboard error: {e}")

def update_gui(bass):
    global bass_label
    bar_len = min(int(bass * 200), 50)
    bar = '█' * bar_len + '.' * (50 - bar_len)
    state_indicator = "🔊 ON" if last_bass_state else "🔇 OFF"
    text = f"Bass [{bar}] Level: {bass:.3f} | Threshold: {threshold:.3f} | {state_indicator}"
    bass_label.config(text=text)

def audio_callback(indata, frames, time_info, status):
    global running, current_bass, threshold
    if not running:
        return
    try:
        bass = detect_bass(indata)
        current_bass = bass
        bass_detected = bass > threshold
        set_scroll_lock(bass_detected)
        if root:
            root.after(0, update_gui, bass)
    except Exception as e:
        print(f"\nAudio callback error: {e}")
        running = False

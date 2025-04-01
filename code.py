# PTDeck
# A powerful 14-key customizable macro pad powered by Raspberry Pi Pico designed for Purple Teaming.
# Author - WireBits

import os
import time
import board
import usb_hid
import digitalio
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

# Initialize HID Keyboard
kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

CONFIG_FILE = "pins.conf"
payload_dir = "/payloads/"

default_config = {pin: {1: pin + 1} for pin in range(14)}

def load_config():
    config = default_config.copy()
    try:
        with open(CONFIG_FILE, "r") as f:
            lines = f.readlines()
            pin_settings = {}
            for line in lines:
                line = line.strip()
                if line.startswith("PIN="):
                    if pin_settings:
                        pin_num = pin_settings["pin"]
                        press_count = pin_settings["press_count"]
                        payload_count = pin_settings["payload_count"]
                        config.setdefault(pin_num, {}).update({press_count: payload_count})
                    pin_settings = {"pin": int(line.split("=")[1])}
                elif line.startswith("PRESS_COUNT="):
                    pin_settings["press_count"] = int(line.split("=")[1])
                elif line.startswith("PAYLOAD_COUNT="):
                    pin_settings["payload_count"] = int(line.split("=")[1])
            if pin_settings:
                pin_num = pin_settings["pin"]
                press_count = pin_settings["press_count"]
                payload_count = pin_settings["payload_count"]
                config.setdefault(pin_num, {}).update({press_count: payload_count})
    except FileNotFoundError:
        print("Configuration file not found! Using default settings.")
    return config

config = load_config()

button_pins = list(config.keys())

buttons = {}
for pin in button_pins:
    btn = digitalio.DigitalInOut(getattr(board, f"GP{pin}"))
    btn.direction = digitalio.Direction.INPUT
    btn.pull = digitalio.Pull.UP
    buttons[pin] = btn

last_press_time = {pin: 0 for pin in button_pins}
press_count = {pin: 0 for pin in button_pins}

def load_hid_script_from_file(filename):
    try:
        with open(payload_dir + filename, 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"Payload {filename} not found!")
        return None

def execute_payload(payload_number):
    payload_filename = f"payload-{payload_number}.txt"
    print(f"Executing {payload_filename}")
    hidScript = load_hid_script_from_file(payload_filename)
    if hidScript:
        generateHID(hidScript)

def generateHID(hidScript):
    index = 0
    length = len(hidScript)
    while index < length:
        hidLine = hidScript[index].strip()

        if hidLine.startswith("LOOP"):
            try:
                loop_count = int(hidLine.split(" ")[1])
            except (IndexError, ValueError):
                print("Invalid LOOP command!")
                index += 1
                continue
            index += 1
            command_lines = []
            while index < length and hidScript[index].strip() != "EXIT":
                command_lines.append(hidScript[index])
                index += 1
            for _ in range(loop_count):
                executeHID(command_lines)
        elif hidLine == "INF":
            index += 1
            command_lines = []
            while index < length and hidScript[index].strip() != "EXIT":
                command_lines.append(hidScript[index])
                index += 1
            while True:
                executeHID(command_lines)
        elif hidLine == "EXIT":
            break
        else:
            executeHID([hidLine])
        index += 1

def executeHID(hidScript):
    for hidLine in hidScript:
        hidLine = hidLine.strip()
        if hidLine.startswith("WAIT"):
            try:
                time.sleep(float(hidLine.split(" ")[1]) / 1000)
            except (IndexError, ValueError):
                print("Invalid WAIT command!")
        elif hidLine.startswith("TYPE"):
            text_to_type = hidLine.split(" ", 1)[1]
            if text_to_type.endswith("-"):
                layout.write(text_to_type[:-1].strip())
                layout.write("\n")
            else:
                layout.write(text_to_type)
        else:
            newScriptLine = convertHID(hidLine)
            keyTrigger(newScriptLine)

def convertHID(hidLine):
    hidKeys = {
        'A': Keycode.A, 'B': Keycode.B, 'C': Keycode.C, 'D': Keycode.D, 'E': Keycode.E,
        'F': Keycode.F, 'G': Keycode.G, 'H': Keycode.H, 'I': Keycode.I, 'J': Keycode.J,
        'K': Keycode.K, 'L': Keycode.L, 'M': Keycode.M, 'N': Keycode.N, 'O': Keycode.O,
        'P': Keycode.P, 'Q': Keycode.Q, 'R': Keycode.R, 'S': Keycode.S, 'T': Keycode.T,
        'U': Keycode.U, 'V': Keycode.V, 'W': Keycode.W, 'X': Keycode.X, 'Y': Keycode.Y,
        'Z': Keycode.Z, 'F1': Keycode.F1, 'F2': Keycode.F2, 'F3': Keycode.F3, 'F4': Keycode.F4,
        'F5': Keycode.F5, 'F6': Keycode.F6, 'F7': Keycode.F7, 'F8': Keycode.F8, 'F9': Keycode.F9,
        'F10': Keycode.F10, 'F11': Keycode.F11, 'F12': Keycode.F12, 'LEFT': Keycode.LEFT_ARROW,
        'UP': Keycode.UP_ARROW, 'RIGHT': Keycode.RIGHT_ARROW, 'DOWN': Keycode.DOWN_ARROW,
        'TAB': Keycode.TAB, 'HOME': Keycode.HOME, 'END': Keycode.END, 'PGUP': Keycode.PAGE_UP,
        'PGDN': Keycode.PAGE_DOWN, 'CAPS': Keycode.CAPS_LOCK, 'NUM': Keycode.KEYPAD_NUMLOCK,
        'SCROLL': Keycode.SCROLL_LOCK, 'CTRL': Keycode.CONTROL, 'SHIFT': Keycode.SHIFT, 'ALT': Keycode.ALT,
        'GUI': Keycode.GUI, 'ESC': Keycode.ESCAPE, 'PRTSCR': Keycode.PRINT_SCREEN, 'PAUSE': Keycode.PAUSE,
        'SPACE': Keycode.SPACE, 'DEL': Keycode.DELETE, 'INSERT': Keycode.INSERT, 'BKSP': Keycode.BACKSPACE,
        'ENTER': Keycode.ENTER, 'APP': Keycode.APPLICATION
    }
    return [hidKeys.get(k.upper(), Keycode.SPACE) for k in hidLine.split()]

def keyTrigger(hidLine):
    for kd in hidLine:
        kbd.press(kd)
    kbd.release_all()

while True:
    current_time = time.monotonic()
    for pin, button in buttons.items():
        if not button.value:
            if (current_time - last_press_time[pin]) < 10:
                press_count[pin] += 1
            else:
                press_count[pin] = 1
            last_press_time[pin] = current_time
            time.sleep(0.2)
        elif (current_time - last_press_time[pin]) >= 0.5 and press_count[pin] > 0:
            payload_number = config.get(pin, {}).get(press_count[pin], pin + 1)
            execute_payload(payload_number)
            press_count[pin] = 0
    time.sleep(0.05)
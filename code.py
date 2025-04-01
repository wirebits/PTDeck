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

kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

button_pins = [
    board.GP0, board.GP1, board.GP2, board.GP3,
    board.GP4, board.GP5, board.GP6, board.GP7,
    board.GP8, board.GP9, board.GP10, board.GP11,
    board.GP12, board.GP13
]

buttons = []
for pin in button_pins:
    btn = digitalio.DigitalInOut(pin)
    btn.direction = digitalio.Direction.INPUT
    btn.pull = digitalio.Pull.UP
    buttons.append(btn)

payload_dir = "/payloads/"

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

def convertHID(hidLine):
    newline = []
    for key in filter(None, hidLine.split(" ")):
        key = key.upper()
        command_keycode = hidKeys.get(key, None)
        if command_keycode is not None:
            newline.append(command_keycode)
        elif hasattr(Keycode, key):
            newline.append(getattr(Keycode, key))
        else:
            print("Unknown key!")
    return newline

def keyTrigger(hidLine):
    for kd in hidLine:
        kbd.press(kd)
    kbd.release_all()

def typeText(hidLine):
    layout.write(hidLine)

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
                typeText(text_to_type[:-1].strip())
                layout.write("\n")
            else:
                typeText(text_to_type)
        else:
            newScriptLine = convertHID(hidLine)
            keyTrigger(newScriptLine)

def load_hid_script_from_file(filename):
    try:
        with open(payload_dir + filename, 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"Payload {filename} not found!")
        return None

while True:
    for i, button in enumerate(buttons):
        if not button.value:
            payload_filename = f"payload-{i}.txt"
            print(f"Executing {payload_filename}")
            hidScript = load_hid_script_from_file(payload_filename)
            if hidScript:
                generateHID(hidScript)
            time.sleep(0.3)
    time.sleep(0.05)
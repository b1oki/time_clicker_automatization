# -*- coding: utf-8 -*-
"""Time Clickers Auto upgrade & Auto-Clicker Tool.
It makes the increment game look like the idle game.
Made by b1oki & hakonw
"""
import sys
import time
# dis_pylint: disable=locally-disabled, no-name-in-module, no-member
from win32gui import GetWindowText, GetForegroundWindow, GetWindowRect
import win32api
import win32con

__author__ = 'b1oki, hakonw'

GAMENAME = 'Time Clickers'
SLEEPS_DELAY_NOT_PLAY = 0.3
SLEEPS_DELAY_AFTER_CLICK = 0.5
SLEEPS_DELAY_BETWEEN_STEPS = 0.002
COUNTER_LIMIT_BETWEEN_UPGRADES = 1000
COUNTER_INITIAL = 0

# upgrade keys
KEY_A = 0x41 # Pulse Pistol
KEY_S = 0x53 # Flak Cannon
KEY_D = 0x44 # Spread Rifle
KEY_F = 0x46 # Rocket Launcher
KEY_G = 0x47 # Particle Ball
KEY_H = 0x48 # Weapon Cubesc
KEY_C = 0x43 # Active Abilities

# skills keys
KEY_1 = 0x10 # Automatic Fire
KEY_2 = 0x10 # Spread Shots
KEY_3 = 0x10 # Team Work
KEY_4 = 0x10 # Augmented Aim
KEY_5 = 0x10 # Overcharged
KEY_6 = 0x10 # Gold Rush
KEY_7 = 0x10
KEY_8 = 0x10
KEY_9 = 0x10
KEY_0 = 0x10

# first of all update the expensive stuff
UPGRADES_KEYS = (KEY_C, KEY_H, KEY_G, KEY_F, KEY_D, KEY_S, KEY_A)
# first activate all, then reset skills, after try activate again
SKILLS_KEYS = (KEY_7, win32con.VK_SPACE, KEY_0, KEY_7, win32con.VK_SPACE)


def print_oneline(string, one_line_string_flag=False):
    """ Print text to the same line if flag is True """
    if not one_line_string_flag:
        one_line_string_flag = True
    sys.stdout.write(string)
    # remove string after print for writing to same line
    sys.stdout.write('\r')
    sys.stdout.flush()
    return one_line_string_flag


def print_oneline_clear():
    """ Just print newline character """
    sys.stdout.write('\n') # clean up

def print_newline(string, one_line_string_flag=False):
    """" Default print wrapper with flag corrector """
    if one_line_string_flag:
        print_oneline_clear()
        one_line_string_flag = False
    print string
    return one_line_string_flag


def win_check(win_name):
    """ Is current focused windows has title win_name?
    __contributer__ = 'hakonw' """
    hwnd = GetForegroundWindow()
    win_current_name = GetWindowText(hwnd)

    if win_current_name != win_name:
        # sleeps for a short time if not in game to reduce stress on pc
        time.sleep(SLEEPS_DELAY_NOT_PLAY)
        return False
    rect = GetWindowRect(hwnd) # get the window posission
    width = rect[2] - rect[0]
    height = rect[3] - rect[1]

    # auto click window field, numbers is the % of pixels that needs to be removed on the side
    x_min = rect[0] + 0.25 * width
    x_max = rect[2] - 0.25 * width
    y_min = rect[1] + 0.16 * height
    y_max = rect[3] - 0.05 * height
    pos_x, pos_y = win32api.GetCursorPos()
    # checks if the mouse is inside the field
    return x_max > pos_x > x_min and y_max > pos_y > y_min


def mouse_click(pos_x, pos_y):
    """ Just click mouse in this point """
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, pos_x, pos_y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, pos_x, pos_y, 0, 0)


def key_push(key_code):
    """ Press button by hex code """
    win32api.keybd_event(key_code, 0, win32con.KEYEVENTF_EXTENDEDKEY, 0)
    win32api.keybd_event(key_code, 0, win32con.KEYEVENTF_KEYUP, 0)


def run():
    """ Main loop """
    one_line_string_flag = False
    is_click = False
    in_focus = False
    focus_last_state = in_focus
    counter = COUNTER_INITIAL

    one_line_string_flag = print_newline(
        'Running Time Clickers Auto upgrade & Auto-Clicker', one_line_string_flag)
    one_line_string_flag = print_newline(
        'Use "CTRL" to turn it on/off', one_line_string_flag)
    one_line_string_flag = print_newline(
        'Use "INSERT" to shut down the script', one_line_string_flag)
    one_line_string_flag = print_newline(
        'Made by b1oki & hakonw', one_line_string_flag)

    one_line_string_flag = print_newline(
        '--- HINT: Just activate Idle mode for more effective farm ---', one_line_string_flag)
    one_line_string_flag = print_newline(
        '--- Press "E" some times and your pistol will target on the cubes by himself ---',
        one_line_string_flag)

    while True:
        if win32api.GetAsyncKeyState(win32con.VK_INSERT):
            one_line_string_flag = print_newline('Exit', one_line_string_flag)
            break
        if win32api.GetAsyncKeyState(win32con.VK_CONTROL):
            one_line_string_flag = print_newline(
                'Script off' if is_click else 'Script on', one_line_string_flag)
            is_click = not is_click
            time.sleep(SLEEPS_DELAY_AFTER_CLICK)

        in_focus = win_check(GAMENAME)

        if in_focus != focus_last_state:
            focus_last_state = in_focus
            # space in "Get focus" for equal length
            one_line_string_flag = print_oneline(
                'Get game window ' if in_focus else 'Lost game window', one_line_string_flag)

        if is_click and in_focus:

            pos_x, pos_y = win32api.GetCursorPos()
            mouse_click(pos_x, pos_y)

            if counter > COUNTER_LIMIT_BETWEEN_UPGRADES:
                counter = COUNTER_INITIAL
                # upgrade fisrt
                for key_code in UPGRADES_KEYS:
                    key_push(key_code)
                # after activate skills
                for key_code in SKILLS_KEYS:
                    key_push(key_code)

            counter += 1

        time.sleep(SLEEPS_DELAY_BETWEEN_STEPS)


if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        pass # if user press Ctrl + C in command line
    exit(0)

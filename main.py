from __future__ import unicode_literals
from win32gui import GetWindowText, GetForegroundWindow, GetWindowRect
import time
import win32api
import win32con

__author__ = 'b1oki, hakonw'

# upgrade keys
KEY_A = 0x41
KEY_S = 0x53
KEY_D = 0x44
KEY_F = 0x46
KEY_G = 0x47

# skills keys
KEY_1 = 0x10
KEY_2 = 0x10
KEY_3 = 0x10
KEY_4 = 0x10
KEY_5 = 0x10
KEY_6 = 0x10
KEY_7 = 0x10
KEY_8 = 0x10
KEY_9 = 0x10
KEY_0 = 0x10

upgrades_keys = (KEY_G, KEY_F, KEY_S, KEY_D, KEY_A)
skills_keys = (win32con.VK_SPACE, )

gamename = 'Time Clickers'
sleeps_delay_not_play = 0.3
sleeps_delay_after_click = 0.5
sleeps_delay_between_steps = 0.002


def win_check(win_name): # __contributer__ = 'hakonw'
    hwnd = GetForegroundWindow()
    try:
        if GetWindowText(hwnd) != win_name:
            time.sleep(sleeps_delay_not_play) # sleeps for a short time if not in game to reduce stress on pc
            return False
    except UnicodeWarning as error:
        print 'UnicodeWarning: ', error
        return False
    rect = GetWindowRect(hwnd) # get the window posission
    width = rect[2] - rect[0] 
    height = rect[3] - rect[1] 

    # auto click window field, numbers is the % of pixels that needs to be removed on the side
    x_min = rect[0] + 0.25 * width
    x_max = rect[2] - 0.25 * width
    y_min = rect[1] + 0.16 * height
    y_max = rect[3] - 0.05 * height
    x, y = win32api.GetCursorPos()
    if x_max > x > x_min and y_max > y > y_min: # checks if the mouse is inside the field
        return True
    else:
        return False

def mouse_click(x, y):
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

def key_push(key_code):
    win32api.keybd_event(key_code, 0, win32con.KEYEVENTF_EXTENDEDKEY, 0)
    win32api.keybd_event(key_code, 0, win32con.KEYEVENTF_KEYUP, 0)

def run():
    print 'Running Time Clickers Auto upgrade & Auto-Clicker'
    print 'Use CTRL to turn it on/off and use Insert to shut down the script'
    print 'Made by b1oki & hakonw'
    is_click = False
    in_focus = False
    focus_last_state = in_focus
    counter = 0
    while True:
        if win32api.GetAsyncKeyState(win32con.VK_INSERT):
            print 'exit'
            break
        if win32api.GetAsyncKeyState(win32con.VK_CONTROL):
            if is_click:
                is_click = False
                print 'Script off'
            else:
                is_click = True
                print 'Script on'
            time.sleep(sleeps_delay_after_click)
        in_focus = win_check(gamename)
        if in_focus != focus_last_state:
            focus_last_state = in_focus
            if in_focus:
                print 'Get focus'
            else:
                print 'Lost focus'
        if is_click and in_focus:
            x, y = win32api.GetCursorPos()
            mouse_click(x, y)
            if counter > 1000:
                counter = 0
                # upgrade DPS
                for key_code in upgrades_keys:
                    key_push(key_code)
                # activate skills
                for key_code in skills_keys:
                    key_push(key_code)
        counter += 1
        time.sleep(sleeps_delay_between_steps)

if __name__ == '__main__':
    run()

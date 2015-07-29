from __future__ import unicode_literals
from win32gui import GetWindowText, GetForegroundWindow
import time
import win32api
import win32con

__author__ = 'b1oki'

LEFT = 1
MIDDLE = 2
RIGHT = 3
KEY_A = 0x41
KEY_S = 0x53
KEY_D = 0x44
KEY_F = 0x46
KEY_G = 0x47


def mouse_click(x, y, button=LEFT):
    win32api.SetCursorPos((x, y))
    if button == LEFT:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    elif button == MIDDLE:
        win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN, x, y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP, x, y, 0, 0)
    elif button == RIGHT:
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y, 0, 0)


def key_push(key_code):
    win32api.keybd_event(key_code, 0, win32con.KEYEVENTF_EXTENDEDKEY, 0)
    win32api.keybd_event(key_code, 0, win32con.KEYEVENTF_KEYUP, 0)


def run():
    is_click = False
    counter = 0
    while True:
        if win32api.GetAsyncKeyState(win32con.VK_INSERT):
            print 'exit'
            break
        if win32api.GetAsyncKeyState(win32con.VK_CONTROL):
            if is_click:
                is_click = False
            else:
                is_click = True
            time.sleep(0.1)
        if is_click and GetWindowText(GetForegroundWindow())=='Time Clickers':
            x, y = win32api.GetCursorPos()
            mouse_click(x, y)
            if counter > 1000:
                counter = 0
                # upgrade DPS
                for key_code in (KEY_G, KEY_F, KEY_S, KEY_D, KEY_A, win32con.VK_SPACE):
                    key_push(key_code)
        counter += 1
        time.sleep(0.002)


if __name__ == '__main__':
    run()

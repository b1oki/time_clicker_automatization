from win32gui import GetWindowText, GetForegroundWindow, GetWindowRect
import sys
import time
import win32api
import win32con

__author__ = 'b1oki, hakonw'

gamename = 'Time Clickers'
sleeps_delay_not_play = 0.3
sleeps_delay_after_click = 0.5
sleeps_delay_between_steps = 0.002
counter_limit_between_upgrades = 1000
counter_initial = 0
one_line_string_flag = False

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
upgrades_keys = (KEY_C, KEY_H, KEY_G, KEY_F, KEY_D, KEY_S, KEY_A)
# first activate all, then reset skills, after try activate again
skills_keys = (KEY_7, win32con.VK_SPACE, KEY_0, KEY_7, win32con.VK_SPACE)


def print_oneline(string):
    global one_line_string_flag
    if not one_line_string_flag:
        one_line_string_flag = True
    sys.stdout.write(string) # string for output
    sys.stdout.write('\r')
    sys.stdout.flush()


def print_oneline_clear():
    sys.stdout.write('\n') # clean up


def print_newline(string):
    global one_line_string_flag
    if one_line_string_flag:
        print_oneline_clear()
        one_line_string_flag = False
    print string


def win_check(win_name): # __contributer__ = 'hakonw'
    hwnd = GetForegroundWindow()
    win_current_name = GetWindowText(hwnd)

    if win_current_name != win_name:
        time.sleep(sleeps_delay_not_play) # sleeps for a short time if not in game to reduce stress on pc
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
    print_newline('Running Time Clickers Auto upgrade & Auto-Clicker')
    print_newline('Use "CTRL" to turn it on/off')
    print_newline('Use "INSERT" to shut down the script')
    print_newline('Made by b1oki & hakonw')

    print_newline('--- HINT: Just activate Idle mode for more effective farm ---')
    print_newline('--- Press "E" some times and your pistol will target on the cubes by himself ---')

    is_click = False
    in_focus = False
    focus_last_state = in_focus
    counter = counter_initial

    while True:
        if win32api.GetAsyncKeyState(win32con.VK_INSERT):
            print_newline('Exit')
            break
        if win32api.GetAsyncKeyState(win32con.VK_CONTROL):
            print_newline('Script off' if is_click else 'Script on')
            is_click = not is_click
            time.sleep(sleeps_delay_after_click)

        in_focus = win_check(gamename)

        if in_focus != focus_last_state:
            focus_last_state = in_focus
            # space in "Get focus" for equal length
            print_oneline('Get game window ' if in_focus else 'Lost game window')

        if is_click and in_focus:

            x, y = win32api.GetCursorPos()
            mouse_click(x, y)
            
            if counter > counter_limit_between_upgrades:
                counter = counter_initial
                # upgrade fisrt
                for key_code in upgrades_keys:
                    key_push(key_code)
                # after activate skills
                for key_code in skills_keys:
                    key_push(key_code)

            counter += 1

        time.sleep(sleeps_delay_between_steps)


if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        pass # if user press Ctrl + C in command line
    exit(0)

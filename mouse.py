import pyautogui as pag
import time

def mouse_location():
    try:
        while True:
            x, y = pag.position()
            positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
            print(positionStr)
            time.sleep(1)
    except KeyboardInterrupt:
        print('\n')

mouse_location()
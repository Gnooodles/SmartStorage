import pyfirmata.util
from arduino_util import *
import time


# Setup
board = pyfirmata.Arduino('/dev/tty.usbmodem1201', baudrate=9600)

pin1 = 8
pin2 = 4
button = board.get_pin('d:2:i')
last_button_state = 'False'

board.digital[pin1].write(0)
board.digital[pin2].write(0)

# Logic
led1On = 0
led2On = 0

iterator = pyfirmata.util.Iterator(board)
iterator.start()

time.sleep(1)
button.enable_reporting()

current_button_state = str(button.read())

if current_button_state != last_button_state:
    if current_button_state == 'True':
        if led1On == 0:
            led2On = 0
            led1On = 1
        else:
            led2On = 1
            led1On = 0
    board.pass_time(0.5)

last_button_state = current_button_state

if led1On == 1:
    board.digital[pin1].write(1)
    board.digital[pin2].write(0)
else:
    board.digital[pin2].write(1)
    board.digital[pin1].write(0)

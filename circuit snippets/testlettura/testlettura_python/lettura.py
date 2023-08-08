from arduino_functions import *
import time, serial
from pyfirmata import util

# board = setup('/dev/tty.usbmodem1201')
#board.digital[3].mode = pyfirmata.INPUT

time.sleep(1)

ser = serial.Serial('/dev/tty.usbmodem1201', 9600, timeout=0.1)

while True:
    line = ser.readline()

    if line:
        string = line.decode()
        num = int(string)
        print(num)

ser.close()



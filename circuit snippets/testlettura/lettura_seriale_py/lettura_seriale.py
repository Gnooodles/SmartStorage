import serial
import time

ser = serial.Serial("/dev/tty.usbmodem1201", 9600, timeout=0)
scan_duration = 5


def start_scan():
    scan_command = b"\x7E\x00\x08\x01\x00\x02\x01\xAB\xCD"

    ser.write(scan_command)

    time.sleep(0.1)

    while True:
        if ser.read().decode() == "1" or ser.read().decode() == "":
            break


def recieve_data():
    start_time = time.time()
    data = ""

    while (time.time() - start_time) <= scan_duration:
        byte = ser.read().decode()
        if byte == "\r":
            break
        else:
            data += byte

    return data


while True:
    start_scan()
    print(recieve_data())

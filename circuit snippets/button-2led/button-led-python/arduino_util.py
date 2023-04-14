import pyfirmata


def set_on_pin(pin: int, board: pyfirmata.Arduino):
    board.digital[pin].write(1)
    print(f'set pin: {pin} on')


def set_off_pin(pin: int, board: pyfirmata.Arduino):
    board.digital[pin].write(0)
    print(f'set pin: {pin} off')


def read_pin(pin: int, board: pyfirmata.Arduino):
    return board.digital[pin].read()

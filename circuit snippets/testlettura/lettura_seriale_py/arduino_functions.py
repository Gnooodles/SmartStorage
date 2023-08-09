import pyfirmata


def setup(port: str) -> pyfirmata.Arduino:
    """
    Crea la board di Arduino e inizializza e fa partire l'Iterator
    @return board di Arduino
    """
    print('start setup...')
    board = pyfirmata.Arduino(port)
    it = pyfirmata.util.Iterator(board)
    it.start()
    print('setup completed!')
    return board


def get_digital_pin(board: pyfirmata.Arduino, pin: int):
    """
    @return pin specificato della board
    """
    return board.digital[pin]

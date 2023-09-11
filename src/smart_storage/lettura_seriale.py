import time
import serial


# "/dev/tty.usbmodem1201"
class SerialReader:
    def __init__(self, serial_port_path: str) -> None:
        # Establish a serial connection
        self.ser = serial.Serial(serial_port_path, 9600, timeout=0)
        self.SCAN_DURATION = 5

    def start_scan(self):
        """
        Start a scan by sending the appropriate command to the serial source.

        This function sends a scan command through the specified serial source
        and waits for a response. The scan is initiated with a short delay of 0.1 seconds.

        Args:
            ser (serial.Serial): The Serial object for serial communication.
        """
        scan_command = b"\x7E\x00\x08\x01\x00\x02\x01\xAB\xCD"
        self.ser.write(scan_command)
        time.sleep(0.1)

        while True:
            response = self.ser.read().decode()
            if response == "1" or response == "":
                break

    def recieve_data(self) -> str:
        """
        Receive data from a serial source until the SCAN_DURATION timeout is reached.

        This function reads bytes from a serial source until a carriage return ('\r') character
        is detected or until the maximum scanning time defined by SCAN_DURATION is exceeded.

        Returns:
            str: The data received from the serial source.
        """
        start_time = time.time()
        received_data = ""

        while (time.time() - start_time) <= self.SCAN_DURATION:
            byte = self.ser.read().decode()
            if byte == "\r":
                break
            else:
                received_data += byte

        return received_data

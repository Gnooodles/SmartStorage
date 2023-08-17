import time
import serial
from setup_database import *

ser = serial.Serial("/dev/tty.usbmodem1201", 9600, timeout=0)
SCAN_DURATION = 5


def start_scan():
    """
    Avvia una scansione inviando il comando appropriato alla sorgente seriale.

    Questa funzione invia un comando di scansione attraverso la sorgente seriale specificata
    e attende una risposta. La scansione viene avviata con un breve ritardo di 0.1 secondi.

    Args:
        ser (serial.Serial): L'oggetto Serial per la comunicazione seriale.
    """
    scan_command = b"\x7E\x00\x08\x01\x00\x02\x01\xAB\xCD"
    ser.write(scan_command)
    time.sleep(0.1)

    while True:
        if ser.read().decode() == "1" or ser.read().decode() == "":
            break


def recieve_data() -> str:
    """
    Riceve dati da una sorgente seriale fino al raggiungimento del timeout SCAN_DURATION.

    Questa funzione legge i byte da una sorgente seriale fino a quando non viene rilevato
    un carattere di ritorno a capo ('\r')
    o fino a quando non è trascorso il tempo massimo di scansione definito da SCAN_DURATION.

    Returns:
        str: I dati ricevuti dalla sorgente seriale.
    """
    start_time = time.time()
    data = ""

    while (time.time() - start_time) <= SCAN_DURATION:
        byte = ser.read().decode()
        if byte == "\r":
            break
        else:
            data += byte

    return data


status = ""

while True:
    start_scan()
    recieved_data = recieve_data()

    if recieved_data == "CARICA":
        status = "CARICA"
    elif recieved_data == "SCARICA":
        status = "SCARICA"
    elif recieved_data != "":
        if status == "CARICA":
            # carica su db
            print(f"{status} - {recieved_data}")
            add_item(recieved_data)
        elif status == "SCARICA":
            # scarica dal db e mette nella lista
            print(f"{status} - {recieved_data}")
            remove_one_item(recieved_data)
        else:
            # TODO caso in cui status è vuoto
            pass
    else:
        pass

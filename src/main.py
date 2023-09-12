from smart_storage.lettura_seriale import SerialReader
from smart_storage.magazzino import Magazzino
from smart_storage.prodotti import Prodotti
from smart_storage.lista_spesa import ListaSpesa
from smart_storage.scraper import Scraper
import time

# Create an instance of the Magazzino class, initializing the storage system
prodotti = Prodotti("prodotti.db", Scraper())
magazzino = Magazzino("magazzino.db", prodotti)
lista_spesa = ListaSpesa("listaspesa.db", prodotti)

# Initialize the status variable to track the current operation mode
status = ""

serial_reader = SerialReader("/dev/tty.usbmodem1201")

while True:
    # Continuously monitor and process data from serial input
    serial_reader.start_scan()
    received_data = serial_reader.recieve_data()
    if received_data == "CARICA":
        status = "CARICA"
    elif received_data == "SCARICA":
        status = "SCARICA"
    elif received_data != "":
        if status == "CARICA":
            # Load product into the database
            print(f"{status} - {received_data}")
            magazzino.add_item(received_data)
            lista_spesa.remove_one_item(received_data)
        elif status == "SCARICA":
            # Remove product from the database
            print(f"{status} - {received_data}")
            magazzino.remove_one_item(received_data)
            lista_spesa.add_item(received_data)
        else:
            pass
    else:
        pass

    # time.sleep(0.3)

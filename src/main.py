from lettura_seriale import *
from magazzino import Magazzino

magazzino = Magazzino("magazzino.db")

status = ""
while True:
    start_scan()
    received_data = recieve_data()

    if received_data == "CARICA":
        status = "CARICA"
    elif received_data == "SCARICA":
        status = "SCARICA"
    elif received_data != "":
        if status == "CARICA":
            # Load product into the database
            print(f"{status} - {received_data}")
            magazzino.add_item(received_data)
        elif status == "SCARICA":
            # Remove product from the database
            print(f"{status} - {received_data}")
            magazzino.remove_one_item(received_data)
        else:
            # TODO: Handle case when status is empty
            pass
    else:
        pass

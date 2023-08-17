import sqlite3
import os

con = sqlite3.connect("magazzino.db")
cur = con.cursor()

def setup_database():
    cur.execute("CREATE TABLE magazzino(barcode, name, quantity)")


def add_item(barcode: str) -> None:
    # TODO name = get_name_from_barcode(barcode)
    name = ""
    if cur.execute(f"SELECT * FROM magazzino WHERE barcode = '{barcode}'").fetchone() is None:
        cur.execute(f"INSERT INTO magazzino VALUES ('{barcode}', '{name}', 1)")
        con.commit()
    else:
        quantity = get_item_quantity(barcode)
        cur.execute(f"UPDATE magazzino SET quantity = {quantity+1} WHERE barcode = '{barcode}'")
        con.commit()

def get_items():
    res = cur.execute("SELECT * FROM magazzino")
    return res.fetchall()

def erase_database():
    os.remove("magazzino.db")

def get_item_quantity(barcode: str) -> int:
    current_quantity = cur.execute(f"SELECT quantity FROM magazzino WHERE barcode = '{barcode}'").fetchone()[0]
    return current_quantity

def remove_one_item(barcode: str):
    quantity = get_item_quantity(barcode)

    if quantity == 1:
        cur.execute(f"DELETE FROM magazzino WHERE barcode = '{barcode}'")
        con.commit()
    else:
        cur.execute(f"UPDATE magazzino SET quantity = {quantity-1} WHERE barcode = '{barcode}'")
        con.commit()

#setup_database()

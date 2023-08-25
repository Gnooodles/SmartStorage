import sqlite3

conn = sqlite3.connect('barcode.db')
cur = conn.cursor()

def get_name_from_barcode(barcode: str):
    
    # Check if the item already exists in the database
    find_item = cur.execute(
        f"SELECT * FROM barcode WHERE ean = '{barcode}'"
    ).fetchone()

    return find_item
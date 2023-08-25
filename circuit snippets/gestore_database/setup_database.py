from barcode_name_finder import get_name_from_barcode
import sqlite3
import os

# Establish a connection to the SQLite database "magazzino.db"
con = sqlite3.connect("magazzino.db")
cur = con.cursor()


def setup_database():
    """
    Set up the initial database structure.

    This function creates a table named 'magazzino' with columns for barcode, name, and quantity.
    """
    cur.execute(
        "CREATE TABLE magazzino(barcode TEXT PRIMARY KEY, name TEXT, quantity INTEGER)"
    )


def add_item(barcode: str) -> None:
    """
    Add an item to the database or update its quantity if it already exists.

    Args:
        barcode (str): The barcode of the item to be added.

    If the item with the given barcode doesn't exist in the database, a new entry is added.
    If the item already exists, its quantity is incremented by 1.
    """
    # Fetch the item's name based on the barcode.
    name = get_name_from_barcode(barcode)

    # Check if the item already exists in the database
    existing_item = cur.execute(
        f"SELECT * FROM magazzino WHERE barcode = '{barcode}'"
    ).fetchone()

    if existing_item is None:
        # Insert a new item into the database with initial quantity of 1
        cur.execute(f"INSERT INTO magazzino VALUES ('{barcode}', '{name}', 1)")
    else:
        # Increment the quantity of the existing item
        quantity = get_item_quantity(barcode)
        cur.execute(
            f"UPDATE magazzino SET quantity = {quantity + 1} WHERE barcode = '{barcode}'"
        )

    # Commit the changes to the database
    con.commit()


def get_items():
    """
    Retrieve all items from the database.

    Returns:
        list: A list of tuples representing items in the format (barcode, name, quantity).
    """
    res = cur.execute("SELECT * FROM magazzino")
    return res.fetchall()


def erase_database():
    """
    Delete the database file "magazzino.db".

    Caution: This operation is irreversible and will result in permanent data loss.
    """
    os.remove("magazzino.db")


def get_item_quantity(barcode: str) -> int:
    """
    Get the quantity of a specific item based on its barcode.

    Args:
        barcode (str): The barcode of the item.

    Returns:
        int: The quantity of the item.
    """
    current_quantity = cur.execute(
        f"SELECT quantity FROM magazzino WHERE barcode = '{barcode}'"
    ).fetchone()[0]
    return current_quantity


def remove_one_item(barcode: str):
    """
    Remove one quantity of the specified item from the database.

    Args:
        barcode (str): The barcode of the item to be removed.

    If the item's quantity is greater than 1, its quantity is decremented by 1.
    If the item's quantity is 1, the item is completely removed from the database.
    """
    existing_item = cur.execute(
        f"SELECT * FROM magazzino WHERE barcode = '{barcode}'"
    ).fetchone()

    if existing_item is not None:
        quantity = get_item_quantity(barcode)

        if quantity == 1:
            cur.execute(f"DELETE FROM magazzino WHERE barcode = '{barcode}'")
        else:
            cur.execute(
                f"UPDATE magazzino SET quantity = {quantity - 1} WHERE barcode = '{barcode}'"
            )

        # Commit the changes to the database
        con.commit()


# Call the setup_database function to initialize the database table
# setup_database()

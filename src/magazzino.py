import sqlite3
import os
from prodotti import Prodotti


class Magazzino:
    """
    A class representing a storage system.

    This class provides methods to manage an SQLite-based storage system for items
    identified by barcodes. It allows adding, removing, and querying items in the database.

    Args:
        path (str): The path to the SQLite database file.
    """

    def __init__(self, path: str, prodotti: Prodotti) -> None:
        self.path = path
        self.prodotti = prodotti
        self.con = sqlite3.connect(self.path)
        self.cur = self.con.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS magazzino(barcode TEXT PRIMARY KEY, name TEXT, quantity INTEGER)"
        )

    def add_item(self, barcode: str) -> None:
        """
        Add an item to the database or update its quantity if it already exists.

        Args:
            barcode (str): The barcode of the item to be added.

        If the item with the given barcode doesn't exist in the database, a new entry is added.
        If the item already exists, its quantity is incremented by 1.
        """
        # Fetch the item's name based on the barcode.
        name = self.prodotti.get_name_from_barcode(barcode)

        # Check if the item already exists in the database
        existing_item = self.cur.execute(
            f"SELECT * FROM magazzino WHERE barcode = '{barcode}'"
        ).fetchone()

        if existing_item is None:
            # Insert a new item into the database with initial quantity of 1
            self.cur.execute(f"INSERT INTO magazzino VALUES ('{barcode}', '{name}', 1)")
        else:
            # Increment the quantity of the existing item
            quantity = self._get_item_quantity(barcode)
            self.cur.execute(
                f"UPDATE magazzino SET quantity = {quantity + 1} WHERE barcode = '{barcode}'"
            )

        # Commit the changes to the database
        self.con.commit()

    def get_items(self):
        """
        Retrieve all items from the database.

        Returns:
            list: A list of tuples representing items in the format (barcode, name, quantity).
        """
        res = self.cur.execute("SELECT * FROM magazzino")
        return res.fetchall()

    def erase_database(self):
        """
        Delete the database file.

        Caution: This operation is irreversible and will result in permanent data loss.
        """
        os.remove(self.path)

    def _get_item_quantity(self, barcode: str) -> int:
        """
        Get the quantity of a specific item based on its barcode.

        Args:
            barcode (str): The barcode of the item.

        Returns:
            int: The quantity of the item.
        """
        current_quantity = self.cur.execute(
            f"SELECT quantity FROM magazzino WHERE barcode = '{barcode}'"
        ).fetchone()[0]
        return current_quantity

    def remove_one_item(self, barcode: str):
        """
        Remove one quantity of the specified item from the database.

        Args:
            barcode (str): The barcode of the item to be removed.

        If the item's quantity is greater than 1, its quantity is decremented by 1.
        If the item's quantity is 1, the item is completely removed from the database.
        """
        existing_item = self.cur.execute(
            f"SELECT * FROM magazzino WHERE barcode = '{barcode}'"
        ).fetchone()

        if existing_item is not None:
            quantity = self._get_item_quantity(barcode)

            if quantity == 1:
                self.cur.execute(f"DELETE FROM magazzino WHERE barcode = '{barcode}'")
            else:
                self.cur.execute(
                    f"UPDATE magazzino SET quantity = {quantity - 1} WHERE barcode = '{barcode}'"
                )

            # Commit the changes to the database
            self.con.commit()

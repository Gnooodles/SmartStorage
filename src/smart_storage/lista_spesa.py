import sqlite3

from smart_storage.interfaces import ProductFinderInterface
from smart_storage.item import Item


class ListaSpesa:
    """
    A class representing a storage system.

    This class provides methods to manage an SQLite-based storage system for items
    identified by barcodes. It allows adding, removing, and querying items in the database.

    Args:
        path (str): The path to the SQLite database file.
    """

    def __init__(self, path: str, prodotti: ProductFinderInterface) -> None:
        self.path = path
        self.prodotti = prodotti
        self.con = sqlite3.connect(self.path)
        self.cur = self.con.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS lista(barcode TEXT PRIMARY KEY, name TEXT, quantity INTEGER)"
        )

    def add_item(self, barcode: str, quantity: int = 1) -> None:
        """
        Add an item to the database or update its quantity if it already exists.

        Args:
            barcode (str): The barcode of the item to be added.

        If the item with the given barcode doesn't exist in the database, a new entry is added.
        If the item already exists, its quantity is incremented by 1.
        """
        if barcode == "":
            return

        name = self.prodotti.get_name_from_barcode(barcode)

        with self.con:
            # Use a parameterized query to avoid SQL injection
            self.cur.execute(
                """
                INSERT INTO lista (barcode, name, quantity)
                VALUES (?, ?, 1)
                ON CONFLICT(barcode) DO UPDATE
                SET quantity = quantity + 1;
                """,
                (barcode, name),
            )

    def get_items(self) -> list[Item]:
        """
        Retrieve all items from the database.

        Returns:
            list: A list of Items.
        """
        res = self.cur.execute("SELECT * FROM lista")
        results = res.fetchall()

        items = []
        for result in results:
            items.append(Item(result[0], result[1], result[2]))
        return items

    def erase_database(self) -> None:
        """
        Delete the database file.

        Caution: This operation is irreversible and will result in permanent data loss.
        """
        self.cur.execute("DELETE FROM lista")
        self.con.commit()

    def get_item_quantity(self, barcode: str) -> int:
        """
        Get the quantity of a specific item based on its barcode.

        Args:
            barcode (str): The barcode of the item.

        Returns:
            int: The quantity of the item.
        """
        current_quantity = self.cur.execute(
            f"SELECT quantity FROM lista WHERE barcode = '{barcode}'"
        ).fetchone()

        if current_quantity is None:
            return 0

        return current_quantity[0]

    def remove_one_item(self, barcode: str, quantity: int = 1) -> None:
        """
        Remove one quantity of the specified item from the database.

        Args:
            barcode (str): The barcode of the item to be removed.

        If the item's quantity is greater than 1, its quantity is decremented by 1.
        If the item's quantity is 1, the item is completely removed from the database.
        """
        existing_item = self.cur.execute(
            f"SELECT * FROM lista WHERE barcode = '{barcode}'"
        ).fetchone()

        if existing_item is not None:
            old_quantity = self.get_item_quantity(barcode)

            if old_quantity == 1:
                self.cur.execute(f"DELETE FROM lista WHERE barcode = '{barcode}'")
            else:
                self.cur.execute(
                    f"UPDATE lista SET quantity = {old_quantity - quantity} WHERE barcode = '{barcode}'"
                )

            # Commit the changes to the database
            self.con.commit()

import sqlite3
from smart_storage.interfaces import ProductFinderInterface
from smart_storage.item import StorageItem


class Magazzino:
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
            "CREATE TABLE IF NOT EXISTS magazzino(barcode TEXT PRIMARY KEY, name TEXT, quantity INTEGER, threshold INTEGER)"
        )

    def add_item(self, barcode: str) -> None:
        """
        Add an item to the database or update its quantity if it already exists.

        Args:
            barcode (str): The barcode of the item to be added.

        If the item with the given barcode doesn't exist in the database, a new entry is added.
        If the item already exists, its quantity is incremented by 1.
        """
        if barcode == "":
            return
        # Fetch the item's name based on the barcode.
        name = self.prodotti.get_name_from_barcode(barcode)

        # Check if the item already exists in the database
        existing_item = self.cur.execute(
            f"SELECT * FROM magazzino WHERE barcode = '{barcode}'"
        ).fetchone()

        if existing_item is None:
            # Insert a new item into the database with initial quantity of 1
            self.cur.execute(
                f"INSERT INTO magazzino VALUES ('{barcode}', '{name}', 1, 0)"
            )
        else:
            # Increment the quantity of the existing item
            quantity = self.get_item_quantity(barcode)
            self.cur.execute(
                f"UPDATE magazzino SET quantity = {quantity + 1} WHERE barcode = '{barcode}'"
            )

        # Commit the changes to the database
        self.con.commit()

    def get_items(self) -> list[StorageItem]:
        """
        Retrieve all items from the database.

        Returns:
            list: A list of StorageItems.
        """
        res = self.cur.execute("SELECT * FROM magazzino")
        results = res.fetchall()

        items = []
        for result in results:
            items.append(StorageItem(result[0], result[1], result[2], result[3]))
        return items

    def erase_database(self) -> None:
        """
        Delete the database file.

        Caution: This operation is irreversible and will result in permanent data loss.
        """
        self.cur.execute("DELETE FROM magazzino")
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
            f"SELECT quantity FROM magazzino WHERE barcode = '{barcode}'"
        ).fetchone()
        if current_quantity is None:
            return 0

        return current_quantity[0]

    def remove_one_item(self, barcode: str) -> None:
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
            quantity = self.get_item_quantity(barcode)

            if quantity == 1:
                self.cur.execute(f"DELETE FROM magazzino WHERE barcode = '{barcode}'")
            else:
                self.cur.execute(
                    f"UPDATE magazzino SET quantity = {quantity - 1} WHERE barcode = '{barcode}'"
                )

            # Commit the changes to the database
            self.con.commit()

    def update_threshold(self, barcode: str, new_threshold: int) -> None:
        """
        Update the threshold quantity for a product in the warehouse.

        Args:
            barcode (str): The barcode of the product to update.
            new_threshold (int): The new threshold quantity for the product.
        """
        self.cur.execute(
            f"UPDATE magazzino SET threshold = {new_threshold} WHERE barcode = '{barcode}'"
        )
        self.con.commit()

    def get_missing_product_quantity(self) -> list[dict]:
        """
        Retrieve a list of products with quantities below their respective thresholds.

        Returns:
            list[dict]: A list of dictionaries containing information about missing products.
                Each dictionary has the keys 'barcode' and 'difference', representing the
                product's barcode and the difference between its threshold and current quantity.
        """
        missing_list = self.cur.execute(
            """SELECT barcode, quantity, threshold
                FROM magazzino
                WHERE quantity < threshold
            """
        ).fetchall()
        difference = []

        for miss in missing_list:
            difference.append({"barcode": miss[0], "difference": miss[2] - miss[1]})

        return difference

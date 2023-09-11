import sqlite3
from smart_storage.interfaces import ProductFinderInterface
from smart_storage.item import StorageItem, MissingItem
from smart_storage.lista_spesa import ListaSpesa


class Magazzino(ListaSpesa):
    """
    A class representing a storage system.

    This class provides methods to manage an SQLite-based storage system for items
    identified by barcodes. It allows adding, removing, and querying items in the database.

    Args:
        path (str): The path to the SQLite database file.
    """

    def __init__(self, path: str, prodotti: ProductFinderInterface) -> None:
        self.table_name = "magazzino"
        self.path = path
        self.prodotti = prodotti
        self.con = sqlite3.connect(self.path)
        self.cur = self.con.cursor()
        self.cur.execute(
            f"CREATE TABLE IF NOT EXISTS {self.table_name}(barcode TEXT PRIMARY KEY, name TEXT, quantity INTEGER, threshold INTEGER)"
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

        with self.con:
            # Use a parameterized query to avoid SQL injection
            self.cur.execute(
                f"""
                INSERT INTO {self.table_name} (barcode, name, quantity, threshold)
                VALUES (?, ?, 1, 0)
                ON CONFLICT(barcode) DO UPDATE
                SET quantity = quantity + 1;
                """,
                (barcode, name),
            )

    def get_items(self) -> list[StorageItem]:
        """
        Retrieve all items from the database.

        Returns:
            list: A list of StorageItems.
        """
        res = self.cur.execute(f"SELECT * FROM {self.table_name}")
        results = res.fetchall()

        items = [
            StorageItem(*result) for result in results
        ]  # StorageItem(*result) per passare tutti gli elementi
        # della tupla result come argomenti al costruttore di StorageItem
        return items

    def get_missing_products_quantity(self) -> list[MissingItem]:
        """
        Retrieve a list of products with quantities below their respective thresholds.

        Returns:
            list[MissingItem]: A list of MissingItems
        """
        missing_list = self.cur.execute(
            """SELECT barcode, quantity, threshold
                FROM magazzino
                WHERE quantity < threshold
            """
        ).fetchall()
        missing_products = []

        for row in missing_list:
            missing_products.append(
                MissingItem(barcode=row[0], difference=row[2] - row[1])
            )

        return missing_products

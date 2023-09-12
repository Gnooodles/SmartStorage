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
        self.table_name = "lista"
        self.path = path
        self.prodotti = prodotti
        self.con = sqlite3.connect(self.path)
        self.cur = self.con.cursor()
        self.cur.execute(
            f"CREATE TABLE IF NOT EXISTS {self.table_name}(barcode TEXT PRIMARY KEY, name TEXT, quantity INTEGER, threshold INTEGER)"
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
                f"""
                INSERT INTO {self.table_name} (barcode, name, quantity, threshold)
                VALUES (?, ?, ?, 0)
                ON CONFLICT(barcode) DO UPDATE
                SET quantity = quantity + ?;
                """,
                (barcode, name, quantity, quantity),
            )

    def get_items(self) -> list[Item]:
        """
        Retrieve all items from the database.

        Returns:
            list: A list of Items.
        """
        res = self.cur.execute(f"SELECT * FROM {self.table_name}")
        results = res.fetchall()

        items = []
        for result in results:
            items.append(
                Item(result[0], result[1], result[2] + result[3])
            )  # sommo la quantità + la soglia che è
            # stata aggiornata dalla funzione add_missing_to_list per risolvere il problema della doppia aggiunta
            # dei prodotti mancanti
        return items

    def erase_database(self) -> None:
        """
        Delete all data from the database table.

        Caution: This operation is irreversible and will result in permanent data loss.
        """
        self.cur.execute(f"DELETE FROM {self.table_name}")
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
            f"SELECT quantity FROM {self.table_name} WHERE barcode = ?", (barcode,)
        ).fetchone()

        if current_quantity is None:
            return 0

        return current_quantity[0]

    def remove_one_item(self, barcode: str, quantity: int = 1) -> None:
        """
        Remove one or more quantities of the specified item from the database.

        Args:
            barcode (str): The barcode of the item to be removed.
            quantity (int, optional): The quantity to be removed (default is 1).

        This function removes one or more quantities of the specified item from the database. If the item's
        quantity is greater than the specified quantity, its quantity is decremented accordingly. If the
        item's quantity is equal to or less than the specified quantity, the item is completely removed
        from the database.
        """
        existing_item = self.cur.execute(
            f"SELECT * FROM {self.table_name} WHERE barcode = '{barcode}'"
        ).fetchone()

        if existing_item is not None:
            old_quantity = self.get_item_quantity(barcode)

            if old_quantity == 1:
                self.cur.execute(
                    f"DELETE FROM {self.table_name} WHERE barcode = '{barcode}'"
                )
            else:
                self.cur.execute(
                    f"UPDATE {self.table_name} SET quantity = {old_quantity - quantity} WHERE barcode = '{barcode}'"
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
            f"UPDATE {self.table_name} SET threshold = ? WHERE barcode = ?",
            (new_threshold, barcode),
        )
        self.con.commit()

    def delete_item(self, barcode: str) -> None:
        """
        Delete a product from the database based on the barcode.

        Args:
            barcode (str): The barcode of the product to delete.
        """
        with self.con:
            self.cur.execute(
                f"DELETE from {self.table_name} WHERE barcode = ?", (barcode,)
            )

    def update_item(
        self, barcode: str, name: str, quantity: int, threshold: int
    ) -> None:
        with self.con:
            self.cur.execute(
                f"""
            UPDATE {self.table_name} 
            SET name = ?, quantity = ?, threshold = ?
            WHERE barcode = ?
            """,
                (name, quantity, threshold, barcode),
            )

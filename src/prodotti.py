import sqlite3

class Prodotti:

    def __init__(self, path: str) -> None:
        self.path = path
        self.con = sqlite3.connect(self.path)
        self.cur = self.con.cursor()

    def get_name_from_barcode(self, barcode: str) -> str:
        """
        Retrieve the name of an item from the database using its barcode.

        Args:
            barcode (str): The barcode of the item to look up in the database.

        Returns:
            str: The name of the item associated with the given barcode.
        """
                
        # Retrieve the name of the item from the database using the provided barcode
        item_name = self.cur.execute(
            f"SELECT product_name FROM prodotti WHERE barcode = '{barcode}'"
        ).fetchone()[0]
        return item_name
import sqlite3
from smart_storage.interfaces import ScraperInterface


class Prodotti:
    def __init__(self, path: str, scraper: ScraperInterface) -> None:
        self.path = path
        self.con = sqlite3.connect(self.path)
        self.cur = self.con.cursor()
        self.scraper = scraper

    def get_name_from_barcode(self, barcode: str) -> str:
        """
        Retrieve the name of an item from the database using its barcode.

        Args:
            barcode (str): The barcode of the item to look up in the database.

        Returns:
            str: The name of the item associated with the given barcode.
        """

        self.cur.execute("SELECT name FROM prodotti WHERE code = ?", (barcode,))
        item_name = self.cur.fetchone()

        if item_name is not None:
            return item_name[0]

        # If the item's barcode is not found in the database, search the barcode on the internet
        return self.scrape_barcode_name(barcode)

    def scrape_barcode_name(self, barcode: str) -> str:
        """
        Scrapes the name associated with a barcode from a Google search result.
        And update the database with the barcode and the associate name finded.

        Args:
            barcode (str): The barcode for which the associated name needs to be scraped.

        Returns:
            str: The name associated with the given barcode. Returns an empty string if no result is found.
        """
        # setup driver and options
        result_name = self.scraper.get_name_from_barcode(barcode)
        self._update_product(barcode, result_name)
        return result_name

    def _update_product(self, barcode: str, name: str):
        """
        Update the database with the barcode and the associate name.
        """
        # Funzione per aggiornare il database con il barcode e il nome trovato tramite lo scraper
        self.cur.execute(
            "INSERT INTO prodotti (code, name) VALUES (?, ?)", (barcode, name)
        )
        self.con.commit()

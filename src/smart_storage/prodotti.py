import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


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
            f"SELECT product_name FROM prodotti WHERE code = '{barcode}'"
        ).fetchone()

        if item_name is None:
            # if the item's barcode is not finded in the database, search the barcode on the internet
            # self.scrape_barcode_name(barcode)
            return ""

        return item_name[0]

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
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)

        # get the google search url for the barcode
        driver.get(f"https://www.google.com/search?q={barcode}")
        driver.implicitly_wait(1)

        # find and click the button for the privacy consense pop-up
        button = driver.find_element(By.ID, "L2AGLb")
        button.click()
        driver.implicitly_wait(2)

        # find and return the first result, if None return an empty string
        # first_result = driver.find_element(By.CSS_SELECTOR, ".tF2Cxc") # another way to get the first result
        first_result = driver.find_element(By.CSS_SELECTOR, "h3.LC20lb")
        driver.quit()

        if first_result is None:
            return ""

        # get the first line if it is a multiline
        result_name = first_result.text.split("\n")[0]
        self._update_product(barcode, result_name)
        return result_name

    def _update_product(self, barcode: str, name: str):
        # TODO implementare la funzione per aggiornare il database
        # con il barcode e il nome trovato tramite lo scraper
        # cur.execute(f"INSERT INTO prodotti VALUES ('{received_data}', '{name}')")
        # con.commit()
        pass

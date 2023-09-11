from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


class Scraper:
    def __init__(self) -> None:
        options = Options()
        options.add_argument("--headless")
        # options.add_argument('--disable-blink-features=AutomationControlled')
        self.driver = webdriver.Chrome(options=options)

    def _get_url(self, url: str):
        self.driver.get(url)
        self.driver.implicitly_wait(1)

    def _click_privacy_consense(self, button_id):
        button = self.driver.find_element(By.ID, button_id)  # "L2AGLb"
        button.click()
        self.driver.implicitly_wait(2)

    def _find_element_by_css_selector(self, selector: str):
        first_result = self.driver.find_element(
            By.CSS_SELECTOR, selector
        )  # "h3.LC20lb"
        return first_result

    def _get_name_string(self, result) -> str:
        if result is None:
            return ""

        # get the first line if it is a multiline
        result_name = (
            result.text.split("\n")[0].strip().replace("'", "").replace('"', "")
        )
        return result_name

    def get_name_from_barcode(self, barcode) -> str:
        """
        Retrieve the name of a product from the internet using its barcode.
        """
        # f"https://www.google.com/search?q={barcode}"
        try:
            self._get_url(f"https://www.google.com/search?q={barcode}")
            self._click_privacy_consense("L2AGLb")
            result = self._find_element_by_css_selector("h3.LC20lb")
            name = self._get_name_string(result)
            return name
        except:
            return ""

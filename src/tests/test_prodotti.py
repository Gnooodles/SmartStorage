from smart_storage.prodotti import Prodotti


class MockScraper:
    def get_name_from_barcode(self, barcode) -> str:
        if barcode == "555555":
            return "Finded"
        else:
            return ""


mock_scraper = MockScraper()


def test_search_barcode_in_database():
    prodotti = Prodotti("prodotti.db", mock_scraper)
    current_name = prodotti.get_name_from_barcode("111111")
    expected_name = "test"
    assert current_name == expected_name


def test_search_barcode_in_internet_result():
    prodotti = Prodotti("prodotti.db", mock_scraper)
    current_name = prodotti.get_name_from_barcode("555555")
    assert current_name != ""


def test_search_barcode_in_internet_no_result():
    prodotti = Prodotti("prodotti.db", mock_scraper)
    current_name = prodotti.get_name_from_barcode("444444")
    assert current_name == ""

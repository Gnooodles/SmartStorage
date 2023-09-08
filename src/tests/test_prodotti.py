from smart_storage.prodotti import Prodotti
from smart_storage.scraper import Scraper


def test_search_barcode_in_database():
    prodotti = Prodotti("prodotti.db")
    current_name = prodotti.get_name_from_barcode("111111", Scraper())
    expected_name = "test"
    assert current_name == expected_name


def test_search_barcode_in_internet():
    prodotti = Prodotti("prodotti.db")
    current_name = prodotti.get_name_from_barcode("20457125", Scraper())
    print(current_name)
    assert current_name != ""


def test_search_barcode_in_internet_with_name():
    prodotti = Prodotti("prodotti.db")
    current_name = prodotti.get_name_from_barcode("80945147", Scraper())
    print(current_name)
    # barcode of the Vivident Blast chewing gum
    assert current_name.find("Vivident") != -1

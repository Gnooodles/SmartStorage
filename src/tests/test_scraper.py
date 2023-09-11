from smart_storage.scraper import Scraper


def test_barcode_find():
    scraper = Scraper()
    current_name = scraper.get_name_from_barcode("80945147")
    assert current_name.find("Vivident") != -1


def test_barcode_find_not_null():
    scraper = Scraper()
    current_name = scraper.get_name_from_barcode("20457105")
    assert current_name != ""

from smart_storage.prodotti import Prodotti


def test_search_barcode_in_database():
    prodotti = Prodotti("prodotti.db")
    current_name = prodotti.get_name_from_barcode("111111")
    expected_name = "test"
    assert current_name == expected_name


def test_search_barcode_in_internet():
    prodotti = Prodotti("prodotti.db")
    current_name = prodotti.get_name_from_barcode("80007852")
    print(current_name)
    assert current_name != ""

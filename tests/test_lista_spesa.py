from src.lista_spesa import ListaSpesa
import os


MOCK_PATH = "tests/mock_lista_spesa.db"


def test_database_creation():
    lista_spesa = ListaSpesa(MOCK_PATH)
    assert os.path.isfile(MOCK_PATH)
    os.remove(MOCK_PATH)


def test_add_one_item():
    lista_spesa = ListaSpesa(MOCK_PATH)
    lista_spesa.add_item("001")
    expected_items = [("001", "", 1)]
    current_items = lista_spesa.get_items()
    os.remove(MOCK_PATH)
    assert current_items == expected_items


def test_add_one_item_empty():
    lista_spesa = ListaSpesa(MOCK_PATH)
    lista_spesa.add_item("")
    expected_items = []
    current_items = lista_spesa.get_items()
    os.remove(MOCK_PATH)
    assert current_items == expected_items
    # FIXME gestire il caso in cui il barcode sia stringa vuota,
    # non dovrebbe aggiungere nulla, invece aggiunge un item ("", "", 1) che non va bene


def test_add_multiple_items():
    lista_spesa = ListaSpesa(MOCK_PATH)
    lista_spesa.add_item("001")
    lista_spesa.add_item("002")
    expected_items = [("001", "", 1), ("002", "", 1)]
    current_items = lista_spesa.get_items()
    os.remove(MOCK_PATH)
    assert current_items == expected_items


def test_add_item_multiple_times():
    lista_spesa = ListaSpesa(MOCK_PATH)
    lista_spesa.add_item("001")
    lista_spesa.add_item("001")
    lista_spesa.add_item("001")
    expected_items = [("001", "", 3)]
    current_items = lista_spesa.get_items()
    os.remove(MOCK_PATH)
    assert current_items == expected_items


def test_get_items():
    lista_spesa = ListaSpesa(MOCK_PATH)
    lista_spesa.add_item("001")
    lista_spesa.add_item("002")
    current_items = lista_spesa.get_items()
    os.remove(MOCK_PATH)
    assert len(current_items) == 2


def test_get_items_non_present():
    lista_spesa = ListaSpesa(MOCK_PATH)
    current_items = lista_spesa.get_items()
    os.remove(MOCK_PATH)
    assert len(current_items) == 0


def test_erase_database():
    lista_spesa = ListaSpesa(MOCK_PATH)
    lista_spesa.erase_database()
    assert not os.path.isfile(MOCK_PATH)


def test_get_item_quantity():
    lista_spesa = ListaSpesa(MOCK_PATH)
    lista_spesa.add_item("001")
    lista_spesa.add_item("001")
    current_quantity = lista_spesa.get_item_quantity("001")
    os.remove(MOCK_PATH)
    assert current_quantity == 2


def test_get_item_quantity_non_present():
    lista_spesa = ListaSpesa(MOCK_PATH)
    current_quantity = lista_spesa.get_item_quantity("001")
    os.remove(MOCK_PATH)
    assert current_quantity == 0
    # FIXME se provo a fare get_item_quantity per un item che non c'è nel database mi ritorna None,
    # dato che la funzione dovrebbe ritornare un intero è opportuno gestire
    # il caso in cui l'item non esista ritornando 0


def test_remove_one_item():
    lista_spesa = ListaSpesa(MOCK_PATH)
    lista_spesa.add_item("001")
    lista_spesa.remove_one_item("001")
    expected_items = []
    current_items = lista_spesa.get_items()
    os.remove(MOCK_PATH)
    assert current_items == []


def test_remove_one_item_where_there_are_multiple():
    lista_spesa = ListaSpesa(MOCK_PATH)
    lista_spesa.add_item("001")
    lista_spesa.add_item("001")
    lista_spesa.remove_one_item("001")
    expected_items = [("001", "", 1)]
    current_items = lista_spesa.get_items()
    os.remove(MOCK_PATH)
    assert current_items == expected_items


def test_remove_one_item_non_present():
    lista_spesa = ListaSpesa(MOCK_PATH)
    lista_spesa.remove_one_item("001")
    expected_items = []
    current_items = lista_spesa.get_items()
    os.remove(MOCK_PATH)
    assert current_items == expected_items


def test_remove_one_item_non_present_with_other_items():
    lista_spesa = ListaSpesa(MOCK_PATH)
    lista_spesa.add_item("002")
    lista_spesa.add_item("002")
    lista_spesa.add_item("003")
    lista_spesa.remove_one_item("001")
    expected_items = [("002", "", 2), ("003", "", 1)]
    current_items = lista_spesa.get_items()
    os.remove(MOCK_PATH)
    assert current_items == expected_items

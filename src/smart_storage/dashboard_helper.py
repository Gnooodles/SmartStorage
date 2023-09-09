from smart_storage.interfaces import MagazzinoInterface, ListaSpesaInterface


def add_missing_to_list(
    magazzino: MagazzinoInterface, lista_spesa: ListaSpesaInterface
):
    """
    Add missing products to the shopping list.
    Checks for products in the warehouse with quantities below the threshold and adds them to the shopping list.
    """
    missing_products = magazzino.get_missing_products_quantity()
    for missing in missing_products:
        current_quantity = lista_spesa.get_item_quantity(missing.barcode)
        lista_spesa.remove_one_item(missing.barcode)
        new_quantity = current_quantity + missing.difference
        lista_spesa.add_item(missing.barcode, quantity=new_quantity)


# Function to highlight the 'Quantity' column if it's below the 'Threshold'
def highlight_threshold(row):
    highlight = (
        "background-color: firebrick; color: white"  # Colors: orangered, firebrick
    )
    default = ""
    if row["Quantity"] < row["Threshold"]:
        return [highlight, default]
    else:
        return [default, default]

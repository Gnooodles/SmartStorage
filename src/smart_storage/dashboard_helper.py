from smart_storage.interfaces import MagazzinoInterface, ListaSpesaInterface


def add_missing_to_list(
    magazzino: MagazzinoInterface, lista_spesa: ListaSpesaInterface
):
    """
    Checks for products in the warehouse with quantities below the threshold
    and adds them to the shopping list. It iterates through the missing products and
    adjusts the quantity in the shopping list accordingly.
    """
    missing_products = magazzino.get_missing_products_quantity()
    for missing in missing_products:
        current_quantity = lista_spesa.get_item_quantity(missing.barcode)
        lista_spesa.remove_one_item(missing.barcode)
        new_quantity = current_quantity + missing.difference
        lista_spesa.add_item(missing.barcode, quantity=new_quantity)


def update_row(magazzino, barcode: str, name: str, quantity: int, threshold: int):
    """
    Updates an existing row in the 'magazzino' table with the provided data.
    The row to update is identified by its barcode. If a row with the given barcode
    does not exist in the table, no changes are made.
    """
    query = """
            UPDATE magazzino 
            SET name = ?, quantity = ?, threshold = ?
            WHERE barcode = ?
        """
    magazzino.cur.execute(query, (name, quantity, threshold, barcode))
    magazzino.con.commit()


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

import streamlit as st
from smart_storage.magazzino import Magazzino
from smart_storage.prodotti import Prodotti
from smart_storage.lista_spesa import ListaSpesa
import pandas as pd

# Set Streamlit page configuration
st.set_page_config(page_title="Dashboard Smart Storage", layout="wide")

# Create instances of the storage classes
prodotti = Prodotti("prodotti.db")
magazzino = Magazzino("magazzino.db", prodotti)
lista_spesa = ListaSpesa("listaspesa.db", prodotti)

st.title("Dashboard")


def add_missing_to_list():
    """
    Add missing products to the shopping list.
    Checks for products in the warehouse with quantities below the threshold and adds them to the shopping list.
    """
    missing_products = magazzino.get_missing_product_quantity()
    for missing in missing_products:
        already_in_list = lista_spesa.get_item_quantity(missing["barcode"])
        print(already_in_list)
        if already_in_list < missing["difference"]:
            lista_spesa.add_item(missing["barcode"], quantity=missing["difference"])


# Create horizontal buttons
col_button_1, col_button_2 = st.columns([3, 20])
with col_button_1:
    st.button("Refresh")
    # TODO: Implement a button to refresh data

with col_button_2:
    if st.button("Add missing groceries to shopping list"):
        add_missing_to_list()
    # TODO: Implement adding items with quantities below the threshold to the shopping list

# Create a DataFrame for the storage items
df = pd.DataFrame(
    magazzino.get_items(), columns=["Code", "Name", "Quantity", "Threshold"]
)


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


# Create an editable table from the DataFrame with row highlighting
st.data_editor(
    df,  # .style.apply(highlight_threshold, subset=["Quantity", "Threshold"], axis=1),
    hide_index=True,
    use_container_width=True,
    key="data_editor",
)
# Disabled: Disable editing on the 'Code', 'Name', and 'Quantity' columns


# Function to get modified item data from the editable table
def get_modified_item(column: str):
    """
    Get modified item data from the editable table.

    Args:
        column (str): The column name to retrieve modified data from.

    This function retrieves the changes made in the editable table and
    returns information about the modified rows and columns.
    """
    edited_changes = st.session_state["data_editor"]["edited_rows"]
    rows_changed = edited_changes.keys()
    codes_changed = []
    for r in rows_changed:
        codes_changed.append(df[column].values[r])
    return rows_changed, codes_changed, edited_changes


# Update the threshold in the 'magazzino.db' database
rows_changed, codes_changed, edited_changes = get_modified_item("Code")
for row, barcode in zip(rows_changed, codes_changed):
    threshold = edited_changes.get(row)["Threshold"]
    magazzino.update_threshold(barcode, threshold)

# FIXME: Error in dashboard when changing the threshold

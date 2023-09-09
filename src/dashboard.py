import streamlit as st
from smart_storage.magazzino import Magazzino
from smart_storage.prodotti import Prodotti
from smart_storage.lista_spesa import ListaSpesa
from smart_storage.scraper import Scraper
import pandas as pd
import time

# Set Streamlit page configuration
st.set_page_config(page_title="Dashboard Smart Storage", layout="wide")

# Create instances of the storage classes
prodotti = Prodotti("prodotti.db", Scraper())
magazzino = Magazzino("magazzino.db", prodotti)
lista_spesa = ListaSpesa("listaspesa.db", prodotti)

st.title("Dashboard")


def add_missing_to_list():
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


# Create horizontal buttons
col_button_1, col_button_2 = st.columns([3, 20])
with col_button_1:
    st.button("Refresh")

with col_button_2:
    if st.button("Add missing groceries to shopping list"):
        add_missing_to_list()
    # TODO: Implement adding items with quantities below the threshold to the shopping list

# Create a DataFrame for the storage items
df = pd.DataFrame([vars(item) for item in magazzino.get_items()])
df.rename(
    columns={
        "barcode": "Code",
        "name": "Name",
        "quantity": "Quantity",
        "threshold": "Threshold",
    },
    inplace=True,
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
edited_data = st.data_editor(
    df,  # .style.apply(highlight_threshold, subset=["Quantity", "Threshold"], axis=1),
    hide_index=True,
    use_container_width=True,
    key="data_editor",
    disabled=["Code"],
)
# Disabled: Disable editing on the 'Code', 'Name', and 'Quantity' columns


if st.button("Salva modifiche"):
    for i, row in edited_data.iterrows():
        barcode = row["Code"]
        name = row["Name"]
        quantity = row["Quantity"]
        threshold = row["Threshold"]

        # Utilizza una query parametrica per evitare l'iniezione SQL
        query = """
            UPDATE magazzino 
            SET barcode = ?, name = ?, quantity = ?, threshold = ?
            WHERE barcode = ?
        """
        magazzino.cur.execute(query, (barcode, name, quantity, threshold, barcode))
        magazzino.con.commit()

    st.success("Modifiche salvate con successo!")
    time.sleep(0.5)
    st.experimental_rerun()

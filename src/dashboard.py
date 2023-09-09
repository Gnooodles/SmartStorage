import streamlit as st
from smart_storage.magazzino import Magazzino
from smart_storage.prodotti import Prodotti
from smart_storage.lista_spesa import ListaSpesa
from smart_storage.scraper import Scraper
from smart_storage.dashboard_helper import add_missing_to_list, update_row
import pandas as pd
import time

# Set Streamlit page configuration
st.set_page_config(page_title="Dashboard Smart Storage", layout="wide")

# Create instances of the storage classes
prodotti = Prodotti("prodotti.db", Scraper())
magazzino = Magazzino("magazzino.db", prodotti)
lista_spesa = ListaSpesa("listaspesa.db", prodotti)

st.title("Dashboard")


# Create horizontal buttons
col_button_1, col_button_2 = st.columns([3, 20])
with col_button_1:
    st.button("Refresh")

with col_button_2:
    if st.button("Add missing groceries to shopping list"):
        add_missing_to_list(magazzino, lista_spesa)

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
        update_row(magazzino, barcode, name, quantity, threshold)

    st.success("Modifiche salvate con successo!")
    time.sleep(0.5)
    st.experimental_rerun()

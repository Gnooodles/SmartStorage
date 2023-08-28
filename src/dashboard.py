import streamlit as st
from magazzino import Magazzino
import pandas as pd

st.set_page_config(page_title="Dashboard Smart Storage", layout="wide")
magazzino = Magazzino("magazzino.db")
#st.write(magazzino.get_items())

st.title("Dashboard")

st.button("Refresh")

#df = pd.DataFrame(magazzino.get_items(), columns=['Code', 'Name', 'Quantity'])

#st.dataframe(df, hide_index=True, use_container_width=True)


items: list = magazzino.get_items()

cols = st.columns(5)
fields = ['Code', 'Name', 'Quantity', 'Threshold', 'Button']

for col, field in zip(cols, fields):
    col.write(field)

for item in items:
    col_code, col_name, col_quantity, col_threshold, col_button = st.columns(5)
    col_code.write(item[0])
    col_name.write(item[1])
    col_quantity.write(f"{item[2]}")
    col_threshold.write("0")
    button_type = "Add to list"
    button_phold = col_button.empty()  # create a placeholder
    do_action = button_phold.button(button_type, key=item[0])
    if do_action:
        pass # do some action with a row's data
        #button_phold.empty()  #  remove button




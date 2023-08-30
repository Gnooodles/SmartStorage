import sqlite3
import pandas as pd

# Establish a connection to the SQLite database named "prodotti.db"
con = sqlite3.connect("prodotti.db")
cur = con.cursor()

# Create a table named "prodotti" with specified columns
cur.execute("CREATE TABLE IF NOT EXISTS prodotti(id, code TEXT, name, quantity, brands, brands_tag, categories, categories_en)")

# Load data from a CSV file named "dati_ita_filtered.csv" using pandas
data = pd.read_csv("dati_ita_filtered.csv")

# TODO: Convert the 'code' column to string type (uncomment the line below)
data["code"] = data["code"].astype(str).str.split(".").str[0]

# Write the data from the pandas DataFrame into the "prodotti" table in the database
data.to_sql("prodotti", con, if_exists="replace", index=False)

# Commit the changes and close the database connection
con.commit()
con.close()



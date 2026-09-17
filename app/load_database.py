import pandas as pd
import sqlite3

# Load cleaned data
csv_file = "data/transactions_clean.csv"

df = pd.read_csv(csv_file)

# Connect to SQLite database
connection = sqlite3.connect("data/finixicon.db")

# Load data into a SQL table
df.to_sql(
    "transactions",
    connection,
    if_exists="replace",
    index=False
)

connection.close()

print("Finixicon database created successfully.")
print("Rows loaded:", len(df))
print("Table created: transactions")
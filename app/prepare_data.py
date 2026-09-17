import pandas as pd

# Source dataset
file_path = "data/laramee26openBankTransactionData.xlsx"

# Read transactions
df = pd.read_excel(
    file_path,
    sheet_name="Transactions"
)

# Clean column names
df.columns = [
    column.strip().lower().replace(" ", "_")
    for column in df.columns
]

# Convert transaction date
df["transaction_date"] = pd.to_datetime(
    df["transaction_date"],
    format="%d/%m/%Y",
    errors="coerce"
)

# Handle missing categorical values
df["transaction_type"] = df["transaction_type"].fillna("Unknown")
df["category"] = df["category"].fillna("Uncategorized")
df["location_city"] = df["location_city"].fillna("Unknown")
df["location_country"] = df["location_country"].fillna("Unknown")

# Missing debit/credit means the transaction was on the other side.
# Keep the original distinction for now.

# Create a single transaction amount
df["amount"] = df["debit_amount"].fillna(
    df["credit_amount"]
)

# Determine transaction direction
df["direction"] = df.apply(
    lambda row: "credit"
    if pd.notna(row["credit_amount"])
    else "debit",
    axis=1
)

# Save cleaned dataset
output_file = "data/transactions_clean.csv"

df.to_csv(
    output_file,
    index=False
)

print("Finixicon data preparation complete.")
print("Rows:", len(df))
print("Columns:", len(df.columns))
print("Saved to:", output_file)

print("\nDirection:")
print(df["direction"].value_counts())

print("\nCategories:")
print(df["category"].value_counts().head(10))
import pandas as pd

file_path = "data/laramee26openBankTransactionData.xlsx"

df = pd.read_excel(file_path, sheet_name="Transactions")

print("Rows:", len(df))

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isna().sum())

print("\nCategories:")
print(df["Category"].value_counts(dropna=False))
import sqlite3

connection = sqlite3.connect("data/finixicon.db")

query = """
SELECT
    substr(transaction_date, 1, 7) AS month,
    SUM(amount) AS total_debits
FROM transactions
WHERE direction = 'debit'
GROUP BY month
ORDER BY month;
"""

results = connection.execute(query).fetchall()

print("=== MONTHLY DEBITS ===")

for month, total in results:
    print(f"{month}: {total:.2f}")

connection.close()
import sqlite3


def get_spending_by_category(category: str):
    connection = sqlite3.connect("data/finixicon.db")
    connection.row_factory = sqlite3.Row

    query = """
    SELECT
        category,
        SUM(amount) AS total_spending
    FROM transactions
    WHERE direction = 'debit'
      AND category = ?
    GROUP BY category;
    """

    row = connection.execute(query, (category,)).fetchone()

    connection.close()

    if row is None:
        return {
            "category": category,
            "total_spending": 0
        }

    return {
    "category": row["category"],
    "total_spending": row["total_spending"],
    "currency": "GBP"
}
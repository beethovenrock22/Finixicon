from fastapi import FastAPI
import sqlite3

app = FastAPI(title="Finixicon API")


@app.get("/")
def home():
    return {
        "message": "Finixicon API is running"
    }


@app.get("/transactions")
def get_transactions(
    category: str = None,
    direction: str = None
):
    connection = sqlite3.connect("data/finixicon.db")
    connection.row_factory = sqlite3.Row

    query = """
    SELECT
        transaction_number,
        transaction_date,
        transaction_type,
        transaction_description,
        amount,
        direction,
        category,
        location_city,
        location_country
    FROM transactions
    WHERE 1=1
    """

    parameters = []

    if category:
        query += " AND category = ?"
        parameters.append(category)

    if direction:
        query += " AND direction = ?"
        parameters.append(direction)

    query += " LIMIT 20;"

    rows = connection.execute(
        query,
        parameters
    ).fetchall()

    connection.close()

    return [dict(row) for row in rows]
@app.get("/analytics/spending-by-category")
def spending_by_category():
    connection = sqlite3.connect("data/finixicon.db")
    connection.row_factory = sqlite3.Row

    query = """
    SELECT
        category,
        SUM(amount) AS total_spending
    FROM transactions
    WHERE direction = 'debit'
    GROUP BY category
    ORDER BY total_spending DESC;
    """

    rows = connection.execute(query).fetchall()

    connection.close()

    return [dict(row) for row in rows]
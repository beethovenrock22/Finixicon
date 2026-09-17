from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import os
import json

from dotenv import load_dotenv
from google import genai
from app.tools import get_spending_by_category


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

app = FastAPI(title="Finixicon API")


class AgentRequest(BaseModel):
    question: str


spending_tool = {
    "type": "function",
    "name": "get_spending_by_category",
    "description": "Gets the total debit spending for a specific transaction category.",
    "parameters": {
        "type": "object",
        "properties": {
            "category": {
                "type": "string",
                "description": "The transaction category, such as Amazon, Groceries, or Travel."
            }
        },
        "required": ["category"]
    }
}


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


@app.post("/agent")
def ask_agent(request: AgentRequest):

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=request.question,
        tools=[spending_tool]
    )

    for step in interaction.steps:

        if step.type == "function_call":

            if step.name == "get_spending_by_category":

                result = get_spending_by_category(
                    step.arguments["category"]
                )

                final_interaction = client.interactions.create(
                    model="gemini-3.6-flash",
                    previous_interaction_id=interaction.id,
                    input=[
                        {
                            "type": "function_result",
                            "name": step.name,
                            "call_id": step.id,
                            "result": [
                                {
                                    "type": "text",
                                    "text": json.dumps(result)
                                }
                            ]
                        }
                    ],
                    tools=[spending_tool]
                )

                return {
                    "question": request.question,
                    "answer": final_interaction.output_text
                }

    return {
        "question": request.question,
        "answer": interaction.output_text
    }
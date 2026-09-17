import os
import json
from dotenv import load_dotenv
from google import genai
from tools import get_spending_by_category

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


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


interaction = client.interactions.create(
    model="gemini-3.6-flash",
    input="How much did I spend on Amazon?",
    tools=[spending_tool]
)


for step in interaction.steps:

    if step.type == "function_call":

        print("Gemini requested tool:", step.name)
        print("Arguments:", step.arguments)

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

            print("\nFinixicon Agent:")
            print(final_interaction.output_text)
import os
import json
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types

from tools import get_order, search_products, get_product


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(api_key=api_key)

MODEL_NAME = "gemini-3.7-flash"


# ============================================================
# TOOL DECLARATIONS
# ============================================================

get_order_declaration = types.FunctionDeclaration(
    name="get_order",
    description="Get order details using an order ID.",
    parameters=types.Schema(
        type="OBJECT",
        properties={
            "order_id": types.Schema(
                type="STRING",
                description="The order ID, for example ORD-1002"
            )
        },
        required=["order_id"]
    )
)


search_products_declaration = types.FunctionDeclaration(
    name="search_products",
    description="Search for products using a keyword such as shoes, shirt, laptop, etc.",
    parameters=types.Schema(
        type="OBJECT",
        properties={
            "query": types.Schema(
                type="STRING",
                description="Product search keyword"
            )
        },
        required=["query"]
    )
)


get_product_declaration = types.FunctionDeclaration(
    name="get_product",
    description="Get complete product information using a product ID.",
    parameters=types.Schema(
        type="OBJECT",
        properties={
            "product_id": types.Schema(
                type="STRING",
                description="The product ID, for example P101"
            )
        },
        required=["product_id"]
    )
)


# ============================================================
# STORE TOOLS
# ============================================================

store_tools = types.Tool(
    function_declarations=[
        get_order_declaration,
        search_products_declaration,
        get_product_declaration
    ]
)


# ============================================================
# PYTHON FUNCTION MAPPING
# ============================================================

available_tools = {
    "get_order": get_order,
    "search_products": search_products,
    "get_product": get_product
}


# ============================================================
# SYSTEM INSTRUCTION
# ============================================================

SYSTEM_INSTRUCTION = """
You are an AI Store Assistant.

You help customers with:

1. Order tracking
2. Product information
3. Product searching

IMPORTANT RULES:

- If the customer asks about an order, use get_order.
- If the customer asks about a product using a product ID, use get_product.
- If the customer asks to search for products, use search_products.
- If one tool result gives you information needed for another tool,
  use the second tool.
- You can call multiple tools in the same conversation.
- Do not invent order or product information.
- Give a simple and helpful final answer.
"""


# ============================================================
# GEMINI REQUEST WITH RETRY
# ============================================================

def generate_with_retry(contents):
    """
    Send a request to Gemini.

    If Gemini temporarily returns a 503 error,
    automatically retry the request.

    Retry delays:
        Attempt 1 -> immediate
        Attempt 2 -> wait 2 seconds
        Attempt 3 -> wait 4 seconds
        Attempt 4 -> wait 8 seconds
    """

    max_attempts = 4

    for attempt in range(1, max_attempts + 1):

        try:

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=contents,
                config=types.GenerateContentConfig(
                    tools=[store_tools],
                    system_instruction=SYSTEM_INSTRUCTION
                )
            )

            return response

        except Exception as e:

            error_text = str(e)

            # ------------------------------------------------
            # Check whether this looks like a temporary 503
            # ------------------------------------------------

            is_temporary_error = (
                "503" in error_text
                or "UNAVAILABLE" in error_text
                or "high demand" in error_text
            )

            if not is_temporary_error:

                raise e

            # ------------------------------------------------
            # If final attempt failed
            # ------------------------------------------------

            if attempt == max_attempts:

                raise e

            # ------------------------------------------------
            # Calculate retry delay
            # ------------------------------------------------

            wait_time = 2 ** attempt

            print()
            print(
                f"Gemini temporarily unavailable. "
                f"Retrying in {wait_time} seconds..."
            )

            time.sleep(wait_time)

    return None


# ============================================================
# AGENT FUNCTION
# ============================================================

def run_agent(question):

    # --------------------------------------------------------
    # Start conversation
    # --------------------------------------------------------

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=question)
            ]
        )
    ]

    # --------------------------------------------------------
    # Maximum number of tool rounds
    # --------------------------------------------------------

    for round_number in range(1, 6):

        print()
        print(f"[Agent Round {round_number}]")

        try:

            # ------------------------------------------------
            # Ask Gemini with automatic retry
            # ------------------------------------------------

            response = generate_with_retry(contents)

        except Exception as e:

            print()
            print("Gemini Error:")
            print(e)

            return (
                "Sorry, the AI service is temporarily unavailable. "
                "Please try again."
            )

        # ----------------------------------------------------
        # Get model response
        # ----------------------------------------------------

        model_content = response.candidates[0].content

        # Add Gemini response to conversation
        contents.append(model_content)

        # ----------------------------------------------------
        # Find function calls
        # ----------------------------------------------------

        function_calls = []

        for part in model_content.parts:

            if part.function_call:
                function_calls.append(part.function_call)

        # ----------------------------------------------------
        # No tool required
        # ----------------------------------------------------

        if not function_calls:

            return response.text

        # ----------------------------------------------------
        # Execute tools
        # ----------------------------------------------------

        tool_response_parts = []

        for function_call in function_calls:

            tool_name = function_call.name
            tool_args = dict(function_call.args)

            print()
            print("----------------------------------------")
            print("TOOL CALL")
            print("----------------------------------------")

            print(f"Tool: {tool_name}")
            print(f"Arguments: {tool_args}")

            # ------------------------------------------------
            # Check if tool exists
            # ------------------------------------------------

            if tool_name not in available_tools:

                result = {
                    "success": False,
                    "error": f"Unknown tool: {tool_name}"
                }

            else:

                try:

                    # ----------------------------------------
                    # Get Python function
                    # ----------------------------------------

                    tool_function = available_tools[tool_name]

                    # ----------------------------------------
                    # Execute Python function
                    # ----------------------------------------

                    result = tool_function(**tool_args)

                except Exception as e:

                    result = {
                        "success": False,
                        "error": str(e)
                    }

            # ------------------------------------------------
            # Print tool result
            # ------------------------------------------------

            print()
            print("----------------------------------------")
            print("TOOL RESULT")
            print("----------------------------------------")

            print(result)

            # ------------------------------------------------
            # Create Gemini function response
            # ------------------------------------------------

            tool_response_parts.append(
                types.Part.from_function_response(
                    name=tool_name,
                    response={
                        "result": result
                    }
                )
            )

        # ----------------------------------------------------
        # Send tool results back to Gemini
        # ----------------------------------------------------

        contents.append(
            types.Content(
                role="user",
                parts=tool_response_parts
            )
        )

    # --------------------------------------------------------
    # Maximum tool rounds reached
    # --------------------------------------------------------

    return (
        "I was unable to complete the request after "
        "several processing steps."
    )


# ============================================================
# TERMINAL CHATBOT
# ============================================================

def main():

    print()
    print("=" * 48)
    print("           🛒 AGENTIC AI STORE")
    print("=" * 48)

    print()
    print("AI Store Assistant is ready!")

    print()
    print("You can ask questions such as:")
    print()
    print("  Where is my order ORD-1002?")
    print("  Tell me about product P101")
    print("  Show me shoes")
    print("  What product is in my order ORD-1002?")

    print()
    print("Type 'exit' to close the program.")

    print()
    print("=" * 48)

    while True:

        print()

        question = input("You: ").strip()

        # ----------------------------------------------------
        # Exit
        # ----------------------------------------------------

        if question.lower() == "exit":

            print()
            print("Thank you for using AI Store Assistant!")
            break

        # ----------------------------------------------------
        # Empty input
        # ----------------------------------------------------

        if not question:

            print("Please enter a question.")
            continue

        # ----------------------------------------------------
        # Run agent
        # ----------------------------------------------------

        answer = run_agent(question)

        print()
        print("----------------------------------------")
        print("FINAL ANSWER")
        print("----------------------------------------")

        print(answer)


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":
    main()
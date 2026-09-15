# 🛒 Agentic AI Store

An AI-powered customer support assistant for an online shopping store.

The application allows customers to ask questions about orders and products using natural language. The AI agent understands the customer's request, selects the appropriate tool, retrieves information from the database, and generates a clear response.

---

## 📌 Project Objective

The objective of this project is to build an **Agentic AI Store Assistant** that can:

- Track customer orders
- Search available products
- Provide product information
- Perform multiple tool calls when required
- Handle invalid orders and products
- Return customer-friendly responses
- Provide a web-based chat interface

The project demonstrates how an AI agent can use external tools instead of generating answers only from its own knowledge.

---

# 🧠 System Architecture

```text
                    CUSTOMER
                       |
                       v
              ┌─────────────────┐
              │  Streamlit UI   │
              └────────┬────────┘
                       |
                       v
              ┌─────────────────┐
              │   AI AGENT      │
              │    Gemini       │
              └────────┬────────┘
                       |
          ┌────────────┼────────────┐
          |            |            |
          v            v            v
     get_order    get_product   search_products
          |            |            |
          └────────────┼────────────┘
                       |
                       v
              ┌─────────────────┐
              │  SQLite DB      │
              └────────┬────────┘
                       |
                       v
                 TOOL RESULT
                       |
                       v
              ┌─────────────────┐
              │   Gemini Agent  │
              └────────┬────────┘
                       |
                       v
                FINAL RESPONSE
                       |
                       v
                    CUSTOMER
                    🤖 Agentic AI Workflow

The system does not use a fixed response for every question.

Instead, the AI agent determines which tool is required.

For example:

Customer:
"What is the status of my order ORD-1002?"

The agent understands that order information is required.

It calls:

get_order("ORD-1002")

The tool returns:

Order ID: ORD-1002
Product ID: P101
Quantity: 1
Status: Shipped
Expected Delivery: 2026-09-15

The agent then converts the result into a customer-friendly response.

🔗 Multi-Tool Chaining

The agent can use multiple tools for a single question.

Example:

Customer:
"What product is in my order ORD-1002?"

The agent performs:

Step 1
   |
   v
get_order("ORD-1002")
   |
   v
Product ID = P101
   |
   v
Step 2
   |
   v
get_product("P101")
   |
   v
Nike Running Shoes
   |
   v
Final Answer

This demonstrates agentic tool chaining.

🛠️ Available Tools
1. get_order
Purpose

Retrieves information about a customer's order.

Input
order_id

Example:

ORD-1002
Output
{
    "success": true,
    "order_id": "ORD-1002",
    "product_id": "P101",
    "quantity": 1,
    "status": "Shipped",
    "expected_delivery": "2026-09-15"
}
2. get_product
Purpose

Retrieves detailed information about a product.

Input
product_id

Example:

P101
Output
{
    "success": true,
    "product_id": "P101",
    "name": "Nike Running Shoes",
    "category": "shoes",
    "price": 2999.0,
    "stock": 15,
    "description": "Comfortable running shoes for daily use"
}
3. search_products
Purpose

Searches the product database using a natural-language keyword.

Input
query

Example:

shoes
Output

A list of matching products.

Example products include:

Nike Running Shoes
Adidas Sports Shoes
Puma Casual Shoes
💬 Sample Questions

The customer can ask questions such as:

Where is my order ORD-1002?
Tell me about product P101
Show me shoes
What product is in my order ORD-1002?
📦 Example: Order Tracking
User
Where is my order ORD-1002?
Agent

The agent calls:

get_order
Result
Status: Shipped
Expected Delivery: 2026-09-15
Final Response
Your order ORD-1002 has been shipped.

Expected delivery: September 15, 2026.
👟 Example: Product Search
User
Show me shoes
Agent

Calls:

search_products
Result

The system finds available shoes.

Example:

Nike Running Shoes
Price: ₹2,999
Stock: 15

Adidas Sports Shoes
Price: ₹2,499
Stock: 10

Puma Casual Shoes
Price: ₹1,999
Stock: 20
🔄 Example: Multi-Tool Request
User
What product is in my order ORD-1002?
Tool 1
get_order("ORD-1002")

Returns:

product_id = P101
Tool 2
get_product("P101")

Returns:

Nike Running Shoes
Price: ₹2,999
Final Response
Your order ORD-1002 contains:

Product: Nike Running Shoes
Quantity: 1
Price: ₹2,999
Status: Shipped
Expected Delivery: September 15, 2026
❌ Error Handling

The application handles invalid requests without inventing information.

Invalid Order

Example:

Where is my order ORD-9999?

The system returns:

Order not found
Invalid Product

Example:

Tell me about product P999

The system returns:

Product not found
Product Not Found During Search

If the customer searches for something that is not available, the system returns:

No products found

The agent does not fabricate product information.

🧰 Technologies Used
Technology	Purpose
Python	Application development
Google Gemini	AI reasoning and response generation
Google GenAI SDK	Gemini API integration
SQLite	Store/order database
Streamlit	Web user interface
python-dotenv	Environment variable management
📁 Project Structure
AGENTIC_AI_STORE/
│
├── data/
│   └── store.db
│
├── venv/
│
├── agent.py
├── app.py
├── database.py
├── tools.py
├── test_gemini.py
│
├── .env
├── .gitignore
├── README.md
└── requirements.txt
📄 File Responsibilities
agent.py

Contains the main AI agent logic.

Responsibilities:

Receive user questions
Communicate with Gemini
Select tools
Execute tool calls
Handle multiple tool calls
Generate final answers
tools.py

Contains the tools available to the AI agent.

Tools include:

get_order()
get_product()
search_products()
database.py

Handles interaction with the SQLite database.

app.py

Contains the Streamlit web application.

Provides:

Chat interface
Conversation history
Sidebar
Feature information
Clear conversation button
Customer-friendly UI
test_gemini.py

Used to verify that the Gemini API connection is working.

🖥️ User Interface

The project includes a modern Streamlit interface.

The interface provides:

🛒 Agentic AI Store branding
🟢 AI online indicator
💬 Chat interface
📦 Order tracking
🔎 Product search
🏷️ Product information
🧠 Agentic reasoning
🗑️ Clear conversation
Modern gradient/glass-style UI
🔐 Environment Variables

The Gemini API key is stored in a .env file.

Example:

GEMINI_API_KEY=your_api_key_here

The actual API key must never be committed to GitHub.

The .env file is included in .gitignore.

⚙️ Installation
1. Clone the repository
git clone YOUR_GITHUB_REPOSITORY_URL
2. Open the project
cd AGENTIC_AI_STORE
3. Create virtual environment
python -m venv venv
4. Activate virtual environment

Windows PowerShell:

venv\Scripts\Activate.ps1
5. Install dependencies
pip install -r requirements.txt
▶️ Running the Project
Run the Terminal Agent
python agent.py
Run the Streamlit Web Application
streamlit run app.py

The application will normally be available at:

http://localhost:8501
🧪 Testing

The tools can be tested using:

python tools.py

The test suite covers:

1. Valid order
2. Invalid order
3. Product search
4. Empty product search
5. Valid product
6. Invalid product
🛡️ Reliability

The application includes handling for:

Invalid orders
Invalid products
Empty product searches
Gemini service errors
Temporary API availability issues
Tool execution failures

The agent should rely on actual tool results rather than inventing store information.

🎯 Assignment Requirements
Requirement	Status
AI Agent	✅
Gemini Integration	✅
Tool Calling	✅
get_order	✅
get_product	✅
search_products	✅
Multiple Tool Calls	✅
Tool Chaining	✅
Error Handling	✅
No Fabricated Store Data	✅
Terminal Interface	✅
Streamlit Interface	✅
SQLite Database	✅
Documentation	✅
🚀 Future Improvements

Possible future improvements include:

Customer authentication
Shopping cart
Product recommendations
Order cancellation
Order placement
Payment integration
Customer profiles
Voice-based shopping assistant
Admin dashboard
Analytics dashboard
Deployment to cloud
👨‍💻 Project Summary

This project demonstrates an Agentic AI architecture where an LLM is connected to external tools and a database.

Instead of simply generating text, the AI agent can:

Understand
    ↓
Reason
    ↓
Select Tool
    ↓
Execute Tool
    ↓
Read Result
    ↓
Call Another Tool if Required
    ↓
Generate Final Answer

This makes the application more useful, reliable, and closer to a real-world AI customer-support system.


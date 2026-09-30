<div align="center">

# 🛒 Agentic AI Store

### An AI-powered customer support assistant that uses real tools, not guesses.

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Streamlit-FF4B4B?style=for-the-badge)](https://agenticaistore-nn6g8svpytyd5uajasmytf.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Gemini](https://img.shields.io/badge/Google-Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

**[👉 Try the live app](https://agenticaistore-nn6g8svpytyd5uajasmytf.streamlit.app/)**

</div>

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Live Demo](#-live-demo)
- [System Architecture](#-system-architecture)
- [How the Agent Works](#-how-the-agent-works)
- [Available Tools](#-available-tools)
- [Example Conversations](#-example-conversations)
- [Error Handling](#-error-handling)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Deploying to Streamlit Cloud](#-deploying-to-streamlit-cloud)
- [Testing](#-testing)
- [Reliability](#-reliability)
- [Future Improvements](#-future-improvements)

---

## 📌 Overview

**Agentic AI Store** is a customer support assistant for an online shopping store. Customers ask questions in plain language, and the AI agent decides which tool to use, fetches the data from a database, and replies in a clear, friendly way.

The project shows how an LLM can work with **external tools** instead of answering only from its own knowledge, so the answers come from real store data and are never made up.

## ✨ Features

| | Feature | Description |
|---|---|---|
| 📦 | **Order tracking** | Look up status and expected delivery by order ID |
| 🔎 | **Product search** | Find products with natural-language keywords |
| 🏷️ | **Product details** | Get price, stock, category, and description |
| 🔗 | **Tool chaining** | Combine several tools to answer one question |
| 🛡️ | **No fabricated data** | Answers rely only on actual tool results |
| ♻️ | **Automatic retries** | Handles temporary Gemini 503 errors with backoff |
| 💬 | **Web chat UI** | Streamlit interface with conversation history |
| 🖥️ | **Terminal mode** | Run the same agent from the command line |

## 🚀 Live Demo

The app is deployed on Streamlit Community Cloud:

**🔗 https://agenticaistore-nn6g8svpytyd5uajasmytf.streamlit.app/**

Try these questions:

```text
Where is my order ORD-1002?
Tell me about product P101
Show me shoes
What product is in my order ORD-1002?
```

> 💡 Free Streamlit apps go to sleep after a period of inactivity. If you see a sleeping page, click the wake-up button and give it a few seconds.

## 🧠 System Architecture

```text
                   CUSTOMER
                      │
                      ▼
             ┌─────────────────┐
             │  Streamlit UI   │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │    AI AGENT     │
             │     (Gemini)    │
             └────────┬────────┘
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
   get_order     get_product   search_products
        │             │             │
        └─────────────┼─────────────┘
                      ▼
             ┌─────────────────┐
             │   SQLite DB     │
             └────────┬────────┘
                      │
                      ▼
                 TOOL RESULT
                      │
                      ▼
             ┌─────────────────┐
             │  Gemini Agent   │
             └────────┬────────┘
                      │
                      ▼
               FINAL RESPONSE
                      │
                      ▼
                  CUSTOMER
```

## 🤖 How the Agent Works

The system does not use fixed replies. The agent reads the question, picks the right tool, runs it, and turns the result into a friendly answer.

```text
Understand → Reason → Select Tool → Execute Tool → Read Result
        → Call Another Tool if Required → Generate Final Answer
```

**Example**

> **Customer:** "What is the status of my order ORD-1002?"

The agent calls `get_order("ORD-1002")` and receives:

```text
Order ID:          ORD-1002
Product ID:        P101
Quantity:          1
Status:            Shipped
Expected Delivery: 2026-09-15
```

It then writes a customer-friendly response from that result.

### 🔗 Multi-Tool Chaining

For some questions one tool is not enough. The agent uses the output of one tool as the input to the next.

> **Customer:** "What product is in my order ORD-1002?"

```text
get_order("ORD-1002")
        │
        ▼
  product_id = P101
        │
        ▼
get_product("P101")
        │
        ▼
Nike Running Shoes
        │
        ▼
   Final Answer
```

The agent can run up to **5 tool rounds** per question before stopping.

## 🛠️ Available Tools

### 1️⃣ `get_order`

Retrieves information about a customer's order.

| Input | Example |
|---|---|
| `order_id` | `ORD-1002` |

```json
{
  "success": true,
  "order_id": "ORD-1002",
  "product_id": "P101",
  "quantity": 1,
  "status": "Shipped",
  "expected_delivery": "2026-09-15"
}
```

### 2️⃣ `get_product`

Retrieves detailed information about a product.

| Input | Example |
|---|---|
| `product_id` | `P101` |

```json
{
  "success": true,
  "product_id": "P101",
  "name": "Nike Running Shoes",
  "category": "shoes",
  "price": 2999.0,
  "stock": 15,
  "description": "Comfortable running shoes for daily use"
}
```

### 3️⃣ `search_products`

Searches the product database using a keyword and returns a list of matching products.

| Input | Example |
|---|---|
| `query` | `shoes` |

Sample results: **Nike Running Shoes**, **Adidas Sports Shoes**, **Puma Casual Shoes**.

## 💬 Example Conversations

### 📦 Order tracking

**User:** Where is my order ORD-1002?
**Tool used:** `get_order`

> Your order **ORD-1002** has been shipped.
> Expected delivery: **September 15, 2026**.

### 👟 Product search

**User:** Show me shoes
**Tool used:** `search_products`

| Product | Price | Stock |
|---|---|---|
| Nike Running Shoes | ₹2,999 | 15 |
| Adidas Sports Shoes | ₹2,499 | 10 |
| Puma Casual Shoes | ₹1,999 | 20 |

### 🔄 Multi-tool request

**User:** What product is in my order ORD-1002?
**Tools used:** `get_order` → `get_product`

> Your order **ORD-1002** contains:
>
> - **Product:** Nike Running Shoes
> - **Quantity:** 1
> - **Price:** ₹2,999
> - **Status:** Shipped
> - **Expected Delivery:** September 15, 2026

## ❌ Error Handling

The app handles invalid requests without inventing information.

| Situation | Example | Result |
|---|---|---|
| Invalid order | `Where is my order ORD-9999?` | Order not found |
| Invalid product | `Tell me about product P999` | Product not found |
| Empty search | Searching for an unavailable item | No products found |

## 🧰 Tech Stack

| Technology | Purpose |
|---|---|
| **Python** | Application development |
| **Google Gemini** | AI reasoning and response generation |
| **Google GenAI SDK** | Gemini API integration |
| **SQLite** | Store and order database |
| **Streamlit** | Web user interface |
| **python-dotenv** | Environment variable management |

## 📁 Project Structure

```text
AGENTIC_AI_STORE/
│
├── data/
│   └── store.db          # SQLite database
│
├── agent.py              # AI agent logic + terminal chatbot
├── app.py                # Streamlit web application
├── database.py           # SQLite database handling
├── tools.py              # get_order, get_product, search_products
├── test_gemini.py        # Gemini API connection check
│
├── .env                  # Local API key (never committed)
├── .gitignore
├── README.md
└── requirements.txt
```

| File | Responsibility |
|---|---|
| `agent.py` | Receives questions, talks to Gemini, selects and runs tools, handles multiple tool calls, returns the final answer |
| `tools.py` | Defines the tools available to the agent |
| `database.py` | Handles all SQLite interaction |
| `app.py` | Chat interface, conversation history, sidebar, feature info, clear-conversation button |
| `test_gemini.py` | Verifies the Gemini API connection |

## ⚙️ Getting Started

### Prerequisites

- Python 3.10 or newer
- A Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey)

### Installation

```bash
# 1. Clone the repository
git clone YOUR_GITHUB_REPOSITORY_URL

# 2. Open the project
cd AGENTIC_AI_STORE

# 3. Create a virtual environment
python -m venv venv

# 4. Activate it
#    Windows PowerShell:
venv\Scripts\Activate.ps1
#    macOS / Linux:
source venv/bin/activate

# 5. Install dependencies
pip install -r requirements.txt
```

### 🔐 Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

> ⚠️ Never commit your real API key to GitHub. The `.env` file is already listed in `.gitignore`.

### ▶️ Run the project

**Terminal agent**

```bash
python agent.py
```

**Streamlit web app**

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

## ☁️ Deploying to Streamlit Cloud

1. Push the project to GitHub (without `.env`).
2. Create a new app on [Streamlit Community Cloud](https://share.streamlit.io) and select `app.py` as the main file.
3. Open **App settings → Secrets** and add your key in TOML format, with straight double quotes:

```toml
GEMINI_API_KEY = "your_api_key_here"
```

4. Save and wait about a minute for the change to propagate, then reboot the app if needed.

The agent first checks the environment (`.env` locally) and then falls back to Streamlit secrets, so the same code runs in both places.

## 🧪 Testing

Test the tools with:

```bash
python tools.py
```

The test suite covers:

1. ✅ Valid order
2. ✅ Invalid order
3. ✅ Product search
4. ✅ Empty product search
5. ✅ Valid product
6. ✅ Invalid product

## 🛡️ Reliability

- Invalid orders and products
- Empty product searches
- Gemini service errors
- Temporary API availability issues (automatic retry with exponential backoff)
- Tool execution failures

The agent relies on actual tool results rather than inventing store information.

## 🚀 Future Improvements

- [ ] Customer authentication
- [ ] Shopping cart
- [ ] Product recommendations
- [ ] Order cancellation
- [ ] Order placement
- [ ] Payment integration
- [ ] Customer profiles
- [ ] Voice-based shopping assistant
- [ ] Admin dashboard
- [ ] Analytics dashboard

## 👨‍💻 Project Summary

This project demonstrates an agentic AI architecture where an LLM is connected to external tools and a database. Instead of only generating text, the agent can understand a request, reason about it, choose and run tools, read the results, call more tools if needed, and produce a final answer.

That makes it more useful, more reliable, and closer to a real-world AI customer-support system.

---

<div align="center">

**⭐ If you like this project, consider giving it a star!**

[🚀 Live Demo](https://agenticaistore-nn6g8svpytyd5uajasmytf.streamlit.app/)

</div>

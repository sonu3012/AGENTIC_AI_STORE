import os

from dotenv import load_dotenv
from google import genai


# Load variables from .env
load_dotenv()


# Get API key
api_key = os.getenv("GEMINI_API_KEY")


# Check API key
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")


# Create Gemini client
client = genai.Client(api_key=api_key)


# Send a simple question to Gemini
response = client.models.generate_content(
    model="gemini-3.7-flash",
    contents="Say hello in one simple sentence."
)


# Print Gemini's response
print(response.text)


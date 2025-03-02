import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch Google API Key
google_api_key = os.getenv("GOOGLE_API_KEY")

# Ensure API key is not None before using it
if not google_api_key:
    raise ValueError("Error: GOOGLE_API_KEY is not set in the environment variables!")
print(google_api_key)
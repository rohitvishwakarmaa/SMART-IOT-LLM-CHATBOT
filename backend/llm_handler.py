import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Correctly get the API key from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set in environment")

# Configure Gemini client
genai.configure(api_key=GEMINI_API_KEY)

# Initialize Gemini model (use a valid model name)
model = genai.GenerativeModel("models/gemini-1.5-pro-001")


def parse_command(user_input):
    """
    Use Gemini API to extract structured IoT command JSON.
    Returns a dict.
    """
    prompt = (
        "Extract a structured IoT command from this sentence:\n"
        f"\"{user_input}\"\n\n"
        "Return only JSON with keys: device, action, location, value."
    )

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
    except Exception as e:
        return {"error": str(e)}

    # Try to extract the first JSON block from the text
    start = text.find("{")
    end = text.rfind("}") + 1
    if start == -1 or end == 0:
        # No JSON found, return error with raw text
        return {"error": "No JSON found in model output", "raw_text": text}

    json_text = text[start:end]
    try:
        return json.loads(json_text)  # Return dict
    except json.JSONDecodeError:
        return {"error": "Invalid JSON in model output", "raw_text": text}

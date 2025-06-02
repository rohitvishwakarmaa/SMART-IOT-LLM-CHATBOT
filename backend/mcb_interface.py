import requests
import json
from requests.exceptions import RequestException

def send_to_mcb(action_json):
    """
    Send structured command to microcontroller via HTTP POST.

    Args:
        action_json (dict or str): JSON object or JSON-formatted string containing:
            {
                "device": "light",
                "action": "turn on",
                "location": "living room",
                "value": "7 PM"
            }

    Returns:
        dict: Response from MCB or error message.
    """
    # Ensure payload is a dictionary
    try:
        if isinstance(action_json, str):
            payload = json.loads(action_json)
        elif isinstance(action_json, dict):
            payload = action_json
        else:
            return {"error": "Invalid input type. Expected dict or JSON string."}
    except json.JSONDecodeError as e:
        return {"error": f"Invalid JSON format: {e}"}

    # Send the command to the MCB
    try:
        response = requests.post(
            "http://192.168.4.1/command",  # Replace with actual IP if different
            json=payload,
            timeout=5
        )
        response.raise_for_status()
        # Attempt to parse JSON response; if not JSON, return text
        try:
            return response.json()
        except json.JSONDecodeError:
            return {"response_text": response.text}
    except RequestException as e:
        return {"error": f"Failed to connect to MCB: {e}"}

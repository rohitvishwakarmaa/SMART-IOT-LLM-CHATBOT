from flask import Flask, request, jsonify, render_template
from backend.llm_handler import parse_command
from backend.mcb_interface import send_to_mcb

app = Flask(__name__, template_folder="../frontend", static_folder="../frontend/static")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    action_json = parse_command(user_input)

    # action_json is now a dict (from llm_handler)
    if "error" in action_json:
        # Return error message to frontend
        return jsonify({"reply": action_json["error"], "mcb": None})

    mcb_response = send_to_mcb(action_json)
    return jsonify({"reply": action_json, "mcb": mcb_response})


if __name__ == "__main__":
    app.run(debug=True)

# import google.generativeai as genai
# import os
# from dotenv import load_dotenv
#
# load_dotenv()
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
#
# models = list(genai.list_models())  # convert generator to list
#
# for model in models:
#     print(model)


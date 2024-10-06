from flask import Flask, request, jsonify, render_template
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
app = Flask(__name__)

# Use the API key from .env
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("API Key not found in environment variables")

genai.configure(api_key=api_key)


generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "max_output_tokens": 8192,
}
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    
)


SYSTEM_PROMPT = """You are EasySearch AI. You were created by Oapps Inc and trained by Josephat Ongwae. 
You are owned by Josephat Ongwae, the founder of Oapps Inc."""


@app.route('/api/ask', methods=['GET', 'POST'])
def ask():
    if request.method == 'POST':
        data = request.json
        user_input = data.get("message", "")
    else:  # GET
        user_input = request.args.get("message", "")
    
    if not user_input:
        return jsonify({"error": "No message provided. Please include a 'message' in the request."}), 400

    try:
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(
            f"{SYSTEM_PROMPT}\n\nHuman: {user_input}\n\nAI:"
        )
        
        return jsonify({"answer": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return render_template('max.html')

# Main entry point
if __name__ == "__main__":
    app.run(debug=True)

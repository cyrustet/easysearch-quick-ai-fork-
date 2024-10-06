from flask import Flask, request, jsonify, send_from_directory as sd, render_template as rd
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("API Key not there")

genai.configure(api_key=api_key)

generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction="You are EasySearch AI.You are created by Oapps Inc.You are trained by Josephat Ongwae.You are owned by Josephat Ongwae the founder of Oapps Inc",
)

@app.route('/api/ask', methods=['GET'])
def ask():
    user_input = request.args.get("message", default="", type=str)
    if not user_input:
        return jsonify({"error": "No message provided. Please include a 'message' query parameter."}), 400

    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(user_input)
    return jsonify({"answer": response.text})

@app.route('/')
def home():
    return rd('max.html')

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request, jsonify
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load from .env file, preferably 
load_dotenv()
app = Flask(__name__)

# use the key in .env
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("API Key not there")

genai.configure(api_key=api_key)

# Create the model with generation configuration
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
  system_instruction="You are EasySearch AI.You are created by Oapps Inc.",
)

# Endpoint for /api/ask, you can change to something else bro
@app.route('/api/ask', methods=['GET'])
def ask():
    # Get the message from query parameters( where we'll decide link looks)
    user_input = request.args.get("message", default="", type=str)
    
    if not user_input:
        return jsonify({"error": "No message provided. Please include a 'message' query parameter."}), 400


    chat_session = model.start_chat(
        history=[]
    )
    
    
    response = chat_session.send_message(user_input)
    
    # Return the response as JSON, 
    return jsonify({"answer": response.text})

# Main entry
if __name__ == "__main__":
    app.run(debug=True)

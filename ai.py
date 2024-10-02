from flask import Flask, request, jsonify
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load from .env file
load_dotenv()

# Use the key from .env
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("API Key not there")

genai.configure(api_key=api_key)

# Create the model with generation configuration
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "max_output_tokens": 2048,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.0-pro",
    generation_config=generation_config
)

# Flask
app = Flask(__name__)

# Restricted topics
restricted_topics = ["hacking", "racism", "sexual activities"]

# Helper function to check for restricted content
def contains_restricted_content(user_input):
    for topic in restricted_topics:
        if topic in user_input.lower():
            return True
    return False

# Endpoint for /api/ask
@app.route('/api/ask', methods=['GET'])
def ask():
    # Get the message from query parameters
    user_input = request.args.get("message", default="", type=str)
    
    if not user_input:
        return jsonify({"error": "No message provided. Please include a 'message' query parameter."}), 400
    
    # Check for restricted content
    if contains_restricted_content(user_input):
        return jsonify({"error": "The AI does not support or encourage discussions on hacking, racism, or sexual activities."}), 403

    # Start a new chat session and send the message
    chat_session = model.start_chat(
        history=[]
    )
    
    response = chat_session.send_message(user_input)
    
    # Return the response as JSON
    return jsonify({"answer": response.text})

# Endpoint to return details about the AI model
@app.route('/api/details', methods=['GET'])
def get_details():
    details = {
        "model_name": "EasySearch AI",
        "description": "I am an AI language model designed for general search and information retrieval. I strictly avoid engaging in or promoting hacking, racism, or sexual content."
    }
    return jsonify(details)

# Main entry
if __name__ == "__main__":
    app.run(debug=True)

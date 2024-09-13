import os
import requests
import json

# Replace with your actual Gemini API key
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"

# Sensitive topics to avoid (adjust as needed)
SENSITIVE_TOPICS = ["hacking", "racism", "sexual content"]


def generate_text(prompt):
    """
    Generates text using the Gemini Flash API, filtering out sensitive topics.

    Args:
        prompt (str): The prompt to use for text generation.

    Returns:
        str: The generated text, or an error message if unsuccessful.
    """

    if any(topic in prompt.lower() for topic in SENSITIVE_TOPICS):
        return "I'm sorry, I can't answer questions about those topics. Would you like me to try generating something different?"

    url = "https://api.gemini.ai/v1/text-davinci/flash"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GEMINI_API_KEY}"
    }
    data = {
        "prompt": prompt,
        # Adjust max_tokens and temperature as needed
        "max_tokens": 1024,
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for non-200 status codes

        response_json = response.json()
        if "generated_text" in response_json:
            return response_json["generated_text"]
        else:
            return "An error occurred while processing the request."
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        return "There was an error generating text. Please try again later."
    except Exception as e:  # Catch any unexpected errors
        print(f"Unexpected error: {e}")
        return "An unexpected error occurred. Please try again later."


def about_me():
    """
    Returns a short description about the AI.
    """
    return "I am EasySearch AI, a large language model for informative responses using the Gemini Flash API."


def handle_request(request):
    """
    Handles incoming HTTP requests and returns appropriate responses.

    Args:
        request (http.HTTPStatusRequest): The incoming HTTP request.

    Returns:
        dict: A dictionary containing the response status code, headers, and body.
    """

    query = request.args.get("query", "What can I ask you?")

    if query.lower() == "about you":
        response_text = about_me()
    else:
        response_text = generate_text(query)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/plain"
        },
        "body": response_text
    }


# Vercel deployment doesn't require this section (comment out)
if __name__ == "__main__":
    from flask import Flask, request

    app = Flask(__name__)

    @app.route("/", methods=["GET"])
    def index():
        return handle_request(request)

    if __name__ == "__main__":
        app.run(debug=True)

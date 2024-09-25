from flask import Flask, request
import os
import requests
import json
from logging import getLogger  # Import for logging

logger = getLogger(__name__)  # Create logger for error messages


class GeminiClient:
    """
    Class to handle interactions with the Gemini Flash API.

    Attributes:
        api_key (str): The Gemini API key.
        url (str): The Gemini Flash API endpoint URL.
    """

    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://api.gemini.ai/v1/text-davinci/flash"

    def generate_text(self, prompt, max_tokens=1024, temperature=0.7):
        """
        Generates text using the Gemini Flash API.

        Args:
            prompt (str): The prompt to use for text generation.
            max_tokens (int, optional): The maximum number of tokens to generate. Defaults to 1024.
            temperature (float, optional): The temperature parameter for controlling creativity. Defaults to 0.7.

        Returns:
            str: The generated text, or an error message if unsuccessful.
        """

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        data = {"prompt": prompt, "max_tokens": max_tokens, "temperature": temperature}

        try:
            response = requests.post(self.url, headers=headers, json=data)
            response.raise_for_status()  # Raise exception for non-200 status codes

            response_json = response.json()
            if "generated_text" in response_json:
                return response_json["generated_text"]
            else:
                return "An error occurred while processing the request."
        except requests.exceptions.RequestException as e:
            logger.error(f"Error making API request: {e}")
            return "There was an error generating text. Please try again later."
        except Exception as e:  # Catch any unexpected errors
            logger.error(f"Unexpected error: {e}")
            return "An unexpected error occurred. Please try again later."


class EasySearchAI:
    """
    Class to handle user requests and interact with the GeminiClient.

    Attributes:
        client (GeminiClient): The Gemini client instance for API calls.
    """

    def __init__(self, api_key):
        self.client = GeminiClient(api_key)

    def about_me(self):
        """
        Returns a short description about the AI.
        """
        return "I am EasySearch AI, a large language model for informative responses using the Gemini Flash API."

    def handle_request(self, request):
        """
        Handles incoming HTTP requests and returns appropriate responses.

        Args:
            request (http.HTTPStatusRequest): The incoming HTTP request.

        Returns:
            dict: A dictionary containing the response status code, headers, and body.
        """

        query = request.args.get("query", "What can I ask you?")

        if query.lower() == "about you":
            response_text = self.about_me()
        else:
            response_text = self.client.generate_text(query)

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "text/plain"
            },
            "body": response_text
        }


# Create the Flask app
app = Flask(__name__)

# Create an instance of EasySearchAI with your API key (store securely)
easy_search_ai = EasySearchAI(os.environ.get("GEMINI_API_KEY"))

# Route the root path to the handle_request function within EasySearchAI
@app.route("/", methods=["GET"])
def index():
    return easy_search_ai.handle_request(request)


if __name__ == "__main__":
    app.run(debug=True)

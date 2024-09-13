import os
import requests
import sympy

# Replace with your actual Gemini API key (store securely)
API_KEY = os.environ.get('GEMINI_API_KEY')

# Define sensitive topics to avoid
SENSITIVE_TOPICS = ['hacking', 'racism', 'sexual content']

def generate_text(prompt):
    if any(topic in prompt.lower() for topic in SENSITIVE_TOPICS):
        return "I'm sorry, I can't answer questions about those topics. Would you like me to try generating something different?"

    url = "https://api.openai.com/v1/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    data = {
        "model": "text-davinci-003",  # Adjust model as needed
        "prompt": prompt,
        "max_tokens": 1024,
        "n": 1,
        "stop": None,
        "temperature": 0.7  # Adjust for desired creativity
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["text"]
    else:
        print("Error:", response.text)
        return "There was an error generating text. Please try again later."

def about_me():
    return "I am EasySearch Ai, a large language model trained to be informative and comprehensive."

def app(request):
    """
    This function handles incoming HTTP requests.
    """
    query = request.args.get('query', 'What can I ask you?')

    if query.lower() == 'about you':
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

# Vercel deployment doesn't require this section
if __name__ == "__main__":
    from flask import Flask, request  # Import Flask for local testing

    app = Flask(__name__)

    @app.route("/", methods=["GET"])
    def index():
        return app(request)

    if __name__ == "__main__":
        app.run(debug=True)

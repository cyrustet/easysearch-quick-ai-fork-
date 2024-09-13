import os
import requests
import sympy

# Replace 'YOUR_API_KEY' with your actual Gemini API key
API_KEY = os.environ.get('GEMINI_API_KEY')  # Secure API key storage

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

def app(environ, start_response):
    """
    This function simulates a basic web application using Gunicorn.
    You might need to adjust it based on your specific Gunicorn configuration.
    """
    try:
        # Retrieve the port from the environment variable (optional, adjust as needed)
        port = int(os.environ.get('PORT', 8000))

        # Simulate user input (replace with actual interaction logic if needed)
        query = environ['QUERY_STRING'].split('=')[1] if 'QUERY_STRING' in environ else 'What can I ask you?'

        # Process the query
        if query.lower() == 'about you':
            response_text = about_me()
        else:
            response_text = generate_text(query)

        # Set the response status and headers
        start_response('200 OK', [('Content-Type', 'text/plain')])

        # Return the generated text
        return [response_text.encode()]
    except Exception as e:
        print(f"Error: {e}")
        start_response('500 Internal Server Error', [])
        return [b"An error occurred."]

if __name__ == "__main__":
    # This section is for development purposes, not deployment on Render.com
    from wsgiref.simple_server import make_server
    httpd = make_server('', 8000, app)
    print("Serving on port 8000...")
    httpd.serve_forever()

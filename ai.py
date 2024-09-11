import requests
import os
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

def main():
    while True:
        prompt = input("Ask me anything (or type 'quit' to exit): ")
        if prompt.lower() == 'quit':
            break
        elif prompt.lower() == 'about you':
            print(about_me())
        else:
            try:
                # Check if the prompt contains a mathematical expression
                if sympy.sympify(prompt).is_number:
                    # Evaluate the expression using SymPy
                    result = sympy.sympify(prompt).evalf()
                    print(f"The result of the calculation is: {result}")
                else:
                    generated_text = generate_text(prompt)
                    print(generated_text)
            except sympy.SympifyError:
                # If SymPy cannot parse the expression, proceed with text generation
                generated_text = generate_text(prompt)
                print(generated_text)

if __name__ == "__main__":
    main()

import os
from flask import Flask, request, jsonify
import google.generativeai as genai
from flask_cors import CORS

# Initialize Flask app and configure static files
app = Flask(__name__, static_url_path='/static', static_folder='static')
CORS(app)  # Enable CORS for all routes

# Get the API key from the environment variable
api_key = os.getenv("GOOGLE_GENERATIVEAI_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    raise ValueError("API Key is missing!")

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    prompt = data.get('prompt', '')

    try:
        # Attempt to generate content using Google Generative AI
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        
        # Log the response from the model for debugging
        print(f"Response from model: {response.text}")

        # Return the generated reply as JSON
        return jsonify({'reply': response.text})

    except Exception as e:
        # Log any errors that occur
        print(f"Error: {e}")
        
        # Return an error message as JSON with a 500 status code
        return jsonify({'error': str(e)}), 500

# Route to serve static files (HTML, CSS, JS)
@app.route('/')
def index():
    return app.send_static_file('index.html')  # Make sure index.html is in the 'static' folder

if __name__ == '__main__':
    app.run(debug=True)

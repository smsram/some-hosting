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
    try:
        # Log incoming request
        app.logger.info("Incoming request: %s", request.json)
        
        if not request.is_json:
            return jsonify({'error': 'Invalid request format. JSON expected'}), 400

        data = request.get_json()
        prompt = data.get('prompt', '')

        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400

        # Generate response
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        reply = getattr(response, 'text', 'No response generated')
        return jsonify({'reply': reply})

    except Exception as e:
        app.logger.error("Error occurred: %s", str(e))
        return jsonify({'error': 'Internal server error: ' + str(e)}), 500

# Route to serve static files (HTML, CSS, JS)
@app.route('/')
def index():
    return app.send_static_file('index.html')  # Make sure index.html is in the 'static' folder

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify
import google.generativeai as genai
from flask_cors import CORS  # Importing CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

genai.configure(api_key="AIzaSyAhCuyUiRZqnIYskynMkZuuTd-1WFbTo-A")

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    prompt = data.get('prompt', '')

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return jsonify({'reply': response.text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

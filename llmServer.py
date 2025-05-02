from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)

@app.route("/response", methods=["POST"])
def generateAnswer():
    try:
        message = request.get_json(force=True)
        print("Received JSON Data:", message)
        
        #Request to Ollama and llama 3.2:latest and response
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "llama3.2:latest",
            "prompt": message["text"],
            "stream": False
        })
        return jsonify(response.json())

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

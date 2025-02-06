from flask import Flask, request, jsonify
import json
import re

app = Flask(__name__)

def extract_json_from_response(response_text):
    """Extract JSON content from a string using regex"""
    match = re.search(r'```json\n(.*?)\n```', response_text, re.DOTALL)
    if match:
        json_str = match.group(1)
        try:
            return json.loads(json_str)  # Convert string to JSON
        except json.JSONDecodeError:
            return {"error": "Invalid JSON format"}
    return {"error": "No JSON found in response"}

@app.route('/parse', methods=['POST'])
def parse_response():
    """API endpoint to parse raw response and return structured JSON"""
    data = request.json  # Expecting {"response": "..."} in request body
    if 'response' not in data:
        return jsonify({"error": "Missing 'response' field"}), 400
    
    parsed_json = extract_json_from_response(data['response'])
    return jsonify(parsed_json)

if __name__ == '__main__':
    app.run(debug=True)

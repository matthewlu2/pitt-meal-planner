from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})


@app.route('/api/chat', methods=['POST', 'GET'])
def chat():
    data = request.get_json()
    return {"message":  'received!!!'}

if __name__ == "__main__":
    app.run(debug=True, port=5001)
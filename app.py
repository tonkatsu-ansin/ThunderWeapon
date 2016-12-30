from flask import Flask, request, jsonify
from firebase import firebase
import json
import os


firebase = firebase.FirebaseApplication(os.getenv("FIREBASE_URL"), None)
app = Flask("ChatServer")

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

@app.route("/", methods=["POST"])
def chat():
    data = request.data.decode('utf-8')
    print(data)
    firebase.post('/boards/chat', json.loads(data))
    response = jsonify({"status": "ok"})
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.status_code = 201
    return response

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8403)

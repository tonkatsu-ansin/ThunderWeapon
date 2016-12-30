from flask import Flask, request, jsonify
from firebase import firebase
import json
import os


firebase = firebase.FirebaseApplication(os.getenv("FIREBASE_URL"), None)
app = Flask("ChatServer")

@app.after_request
def after_request(response):
    response = jsonify({"status": "ok"})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    response.status_code = 200
    return response

@app.route("/", methods=["OPTIONS"])
def preflight():
    response = jsonify({"status": "ok"})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'OPTIONS, GET,PUT,POST,DELETE')
    response.status_code = 201
    return response

@app.route("/", methods=["POST"])
def chat():
    data = request.data.decode('utf-8')
    try:
        firebase.post('/boards/chat', json.loads(data))

        response = jsonify({"status": "ok"})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'OPTIONS, GET,PUT,POST,DELETE')
        response.status_code = 201
        return response
    except:
        response = jsonify({"status": "fail"})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'OPTIONS, GET,PUT,POST,DELETE')
        response.status_code = 400
        return response

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8403)

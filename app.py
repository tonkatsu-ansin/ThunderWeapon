# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from firebase import firebase
import json
import os
from flask_cors import CORS

firebase = firebase.FirebaseApplication(os.getenv("FIREBASE_URL"), None)
app = Flask("ChatServer")
cors = CORS(app)

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

@app.route("/", methods=["POST"])
def upload():
    f = request.files['file']
    print(f)
    response = jsonify({"status": "ok"})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'OPTIONS, GET,PUT,POST,DELETE')
    response.status_code = 201
    return response

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8403)

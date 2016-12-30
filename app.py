from flask import Flask, request, jsonify
from firebase import firebase
import json
import os


firebase = firebase.FirebaseApplication(os.getenv("FIREBASE_URL"), None)
app = Flask("ChatServer")


@app.route("/", methods=["POST"])
def chat():
    data = request.data.decode('utf-8')
    print(data)
    firebase.post('/boards/chat', json.loads(data))
    response = jsonify({"status": "ok"})
    response.header['Access-Control-Allow-Origin'] = '*'
    response.header['Access-Control-Allow-Methods'] = 'POST'
    response.status_code = 201
    return response

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8403)

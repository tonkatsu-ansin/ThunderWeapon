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
    response.status_code = 201
    return response

if __name__ == '__main__':
    app.run()

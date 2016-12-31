# -*- coding: utf-8 -*-
from os.path import join, dirname
import os
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
from ThunderWeapon import Uploader, DiceBot
from flask import Flask, request, jsonify
from firebase import firebase
import json
from flask_cors import CORS

firebase = firebase.FirebaseApplication(os.getenv("FIREBASE_URL"), None)
app = Flask("ChatServer")
cors = CORS(app)

@app.route("/", methods=["POST"])
def chat():
    data = json.loads(request.data.decode('utf-8'))
    try:
        firebase.post('/boards/chat', data)
        dicebot = DiceBot()
        roll_result = dicebot.roll(data["text"])
        if roll_result is not None:
            res = {}
            res["text"] = dicebot.template(roll_result, data["user"])
            res["color"] = "#0F7001"
            res["user"] = "DiceBot"
            firebase.post('/boards/chat', res)
        response = jsonify({"status": "ok"})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'OPTIONS, GET,PUT,POST,DELETE')
        response.status_code = 201
        return response
    except Exception as e:
        print(e)
        response = jsonify({"status": "fail"})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'OPTIONS, GET,PUT,POST,DELETE')
        response.status_code = 400
        return response

@app.route("/upload", methods=["POST"])
def upload():
    try:
        f = request.files['file']
        uploader = Uploader()
        result = uploader.upload(f)
        firebase.post('/boards/assets', result)
        result.update({"status":"ok"})
        response = jsonify(result)
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'OPTIONS, GET,PUT,POST,DELETE')
        response.status_code = 201
        print(response)
        return response
    except Exception as e:
        print(e)
        response = jsonify({"status": "fail"})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'OPTIONS, GET,PUT,POST,DELETE')
        response.status_code = 400
        return response

if __name__ == '__main__':
    app.run()

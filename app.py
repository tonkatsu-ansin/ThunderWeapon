# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from werkzeug.exceptions import RequestEntityTooLarge
from firebase import firebase
import json
import re
from flask_cors import CORS
from ThunderWeapon import Uploader, DiceBot
from datetime import datetime, tzinfo, timedelta
from os.path import join, dirname
import os
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

firebase = firebase.FirebaseApplication(os.getenv("FIREBASE_URL"), None)
app = Flask("ChatServer")
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 * 1024 - 1
cors = CORS(app)


class JST(tzinfo):

    def utcoffset(self, dt):
        return timedelta(hours=9)

    def dst(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return 'JST'


@app.route("/", methods=["POST"])
def chat():
    def validator(data):
        for i in ["user", "text", "color"]:
            a = data.get(i, None)
            if a is None:
                raise ValueError(i)
            elif a == "":
                raise ValueError(i)
        if not re.match(r"^#[0-9a-fA-F]{6}$", data.get("color")):
            raise ValueError("invalid color code")

    try:
        data = json.loads(request.data.decode('utf-8'))
        validator(data)
        firebase.post('/boards/chat', data)
        dicebot = DiceBot()
        roll_result = dicebot.roll(data["text"])
        if roll_result is not None:
            res = {}
            res["text"] = dicebot.template(roll_result, data["user"])
            res["color"] = "#0F7001"
            res["user"] = "DiceBot"
            res["time"] = datetime.now(tz=JST()).strftime("%H:%M")
            firebase.post('/boards/chat', res)
        res = jsonify({"status": "ok"})
        res.headers.add('Access-Control-Allow-Origin', '*')
        res.headers.add('Access-Control-Allow-Methods',
                        'OPTIONS, GET,PUT,POST,DELETE')
        res.status_code = 201
        return res
    except Exception as e:
        print(e)
        res = jsonify({"status": "fail"})
        res.headers.add('Access-Control-Allow-Origin', '*')
        res.headers.add('Access-Control-Allow-Methods',
                        'OPTIONS, GET,PUT,POST,DELETE')
        res.status_code = 400
        return res


@app.route("/upload", methods=["POST"])
def upload():
    try:
        f = request.files['file']
        uploader = Uploader()
        result = uploader.upload(f)
        firebase.post('/boards/assets', result)
        result.update({"status": "ok"})
        response = jsonify(result)
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods',
                             'OPTIONS, GET,PUT,POST,DELETE')
        response.status_code = 201
        return response
    except RequestEntityTooLarge as e:
        app.logger.debug(e)
        response = jsonify({"status": "fail", "message": e.args})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods',
                             'OPTIONS, GET,PUT,POST,DELETE')
        response.status_code = 413
        return response

    except Exception as e:
        app.logger.debug(e)
        response = jsonify({"status": "fail", "message": e.args})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods',
                             'OPTIONS, GET,PUT,POST,DELETE')
        response.status_code = 400
        return response


if __name__ == '__main__':
    app.run(host="0.0.0.0")

# -*- coding: utf-8 -*-
from app import app
import json


class TestChat:

    @classmethod
    def setup_class(cls):
        cls.client = app.test_client()

    def test_valid(self):
        data = json.dumps({
            "color": "#000000",
            "user": "testUser",
            "text": "これはテストなんだぞ！"
        })
        response = self.client.post("/", data=data)
        assert response.status_code == 201

    def test_invalid_empty_color(self):
        data = json.dumps({
            "user": "testUser",
            "text": "これはテストなんだぞ！"
        })
        response = self.client.post("/", data=data)
        assert response.status_code == 400

    def test_invalid_empty_user(self):
        data = json.dumps({
            "color": "#000000",
            "text": "これはテストなんだぞ！"
        })
        response = self.client.post("/", data=data)
        assert response.status_code == 400

    def test_invalid_empty_text(self):
        data = json.dumps({
            "color": "#000000",
            "user": "testUser",
        })
        response = self.client.post("/", data=data)
        assert response.status_code == 400

    def test_invalid_empty_text_string(self):
        data = json.dumps({
            "color": "#000000",
            "user": "testUser",
            "text": ""
        })
        response = self.client.post("/", data=data)
        assert response.status_code == 400

    def test_invalid_empty_text_user(self):
        data = json.dumps({
            "color": "#000000",
            "user": "",
            "text": "これはテストなんだぞ"
        })
        response = self.client.post("/", data=data)
        assert response.status_code == 400

    def test_invalid_empty_text_color(self):
        data = json.dumps({
            "color": "",
            "user": "testUser",
            "text": "これはテストなんだぞ"
        })
        response = self.client.post("/", data=data)
        assert response.status_code == 400

    def test_invalid_color_code(self):
        data = json.dumps({
            "color": "ningensei",
            "user": "testUser",
            "text": "これはテストなんだぞ"
        })
        response = self.client.post("/", data=data)
        assert response.status_code == 400

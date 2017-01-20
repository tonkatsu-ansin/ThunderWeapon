# -*- coding: utf-8 -*-

from io import BytesIO
from app import app
from faker import Factory
from json import loads


class TestUpload:

    @classmethod
    def setup_class(cls):
        cls.client = app.test_client()
        cls.fake = Factory.create()

    def test_valid(self):
        response = self.client.post('/upload', data={'file': (BytesIO(
            self.fake.paragraph().encode('utf-8')), 'helloWorld.txt')})
        assert response.status_code == 201
        assert loads(response.data.decode('utf-8')).get('status') == 'ok'

    def test_invalid_over_filesize(self):
        response = self.client.post('/upload', data={'file': (BytesIO(
            b'a' * 1024 * 1024  * 16), 'fuga.txt')}) # 16MB file upload
        assert response.status_code == 413
        assert loads(response.data.decode('utf-8')).get('status') == 'fail'

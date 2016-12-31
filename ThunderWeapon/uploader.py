# coding:utf-8
import os
from firebase import firebase
import boto

class Uploader(object):
    """Uploader"""
    def __init__(self):
        self.s3 = boto.connect_s3()
        self.bucket = self.s3.get_bucket("glender")

    def upload(self, filename):
        pass


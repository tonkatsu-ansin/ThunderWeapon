# coding:utf-8
import os
from firebase import firebase
import boto
import uuid

class Uploader(object):
    """Uploader"""
    def __init__(self):
        try:
            self.s3 = boto.connect_s3()
            self.bucket = self.s3.get_bucket("glendar")
        except boto.exception.S3ResponseError:
            self.bucket = self.s3.create_bucket("glendar")

    def upload(self, f):
        fp = f.stream
        name = f.filename
        data = boto.s3.key.Key(self.bucket)
        uniq_filename = str(uuid.uuid4())
        data.key = uniq_filename+'.'+".".join(name.split('.')[1:])
        data.set_contents_from_file(fp)

        return {
                "key": name,
                "filename": data.key
               }

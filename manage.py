# -*- coding: utf-8 -*-

from flask_script import Manager
from os.path import join, dirname
from dotenv import load_dotenv
from app import app
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
manager = Manager(app)

if __name__ == "__main__":
    manager.run()
